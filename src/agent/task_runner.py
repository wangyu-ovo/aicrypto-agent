from __future__ import annotations

from pathlib import Path
from datetime import datetime
import json
import shutil
import os
from typing import Any, Dict, Optional

from src.agent.crypto_agent import CryptoAgent
from src.agent.server_manager import ServerManager
from src.utils import (
    Logger,
    load_task_file,
    truncate_long_string,
    create_task_prompt_from_task,
    get_model_config,
)


class TaskRunner:
    """Run a single CTF task end-to-end with an LLM-powered *CryptoAgent*."""

    _MAX_STDOUT_PREVIEW = 4096  # truncate command output above this length

    def __init__(self, args) -> None:  # noqa: D401 – CLI wrapper passes argparse.Namespace
        self.args = args
        self.task_path: Path = Path(args.task_path)
        
        self.model_config: Dict[str, Any] = get_model_config(args.model)
        self.max_iterations: int = args.max_iterations

        # Always start a *fresh* run – previous artefacts are ignored.
        # The legacy "--fresh" flag has been removed so we simply disable the
        # resume mechanism unconditionally.
        self.resume: bool = False

        # Optional experiment identifier provided via CLI (e.g. "--id 1").
        # This is used to route all artefacts into a dedicated
        # outputs/CTF-<id>/… directory so that several parallel experiment
        # batches can coexist without interfering with each other.
        self.output_id: Optional[str] = getattr(args, "id", None)

        # Resolve output directory (auto-generate if requested)
        self.output_dir: Path = (
            self._auto_output_dir() if args.output_dir == "auto" else Path(args.output_dir)
        )

        self.logger = Logger(
            f"{args.model}_{self.task_path}", (self.output_dir / "run.log").as_posix()
        )

        self.dialog_record_path: Path = self.output_dir / "record.json"
        self.state_path: Path = self.output_dir / "state.json"
        self.dialog_record: list[Dict[str, Any]] = []

        self.server_manager: Optional[ServerManager] = None
        self.agent: Optional[CryptoAgent] = None

        self._init_task()
        self._init_agent()

        # Determine starting user input and iteration counter.
        self._prepare_initial_input()

    # ---------------------------------------------------------------------
    # Initialisation helpers
    # ---------------------------------------------------------------------

    def _auto_output_dir(self) -> Path:
        """Derive ``./outputs/<category>/<sub>/<task>/<model>/run``.

        The optional *output_id* (from the ``--id`` CLI option) is injected
        between ``outputs/`` and the task hierarchy so that multiple runs can
        be isolated, e.g. ``outputs/CTF-1/<category>/…``.
        """

        parts = self.task_path.parts
        if len(parts) < 4:
            raise ValueError(f"Invalid task path: {self.task_path}")

        category, sub, task_name = parts[-3:]
        root = Path("./outputs")

        if self.output_id:
            # outputs/CTF-<id>/... (skip redundant 'CTF' segment coming from
            # the task path itself)
            root = root / f"CTF-{self.output_id}"
            if category == "CTF":
                base = root / sub / task_name / self.model_config["model_name"]
            else:
                base = root / category / sub / task_name / self.model_config["model_name"]
        else:
            base = root / category / sub / task_name / self.model_config["model_name"]

        base.mkdir(parents=True, exist_ok=True)

        run_dir = base / "run"
        # Always force a clean directory for each execution.
        if os.path.exists(run_dir):
            shutil.rmtree(run_dir)

        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir

    def _init_task(self) -> None:
        """Populate *self.task_info* and spin-up server if dynamic."""

        self.task_info: Dict[str, Any] = load_task_file(self.task_path / "config.yaml")
        self.task_info["write_path"] = (self.output_dir / "write").as_posix()
        self.task_info["read_path"] = (Path(self.task_info["write_path"]) / "public").as_posix()

        # Scale the provided time-limit – shorter tasks get generous multiplier.
        self.task_info["time"] = 300 if self.task_info["time"] < 60 else self.task_info["time"] * 3

        if not (self.resume and Path(self.task_info["read_path"]).exists()):
            shutil.copytree(self.task_path / "public", self.task_info["read_path"], dirs_exist_ok=True, ignore=shutil.ignore_patterns("._*"))

        # Move helper scripts next to write_path for easier import.
        for helper in ("helper.py", "helper.sage"):
            src = Path(self.task_info["read_path"]) / helper
            if src.exists():
                src.rename(Path(self.task_info["write_path"]) / helper)

        self.flag_path = Path(self.task_info["write_path"]) / "flag.txt"
        self.true_flag = self.task_info.get("flag", "")
        if not self.true_flag:
            raise ValueError("No true flag found in the task config")

        # Dynamic challenge – launch accompanying server.
        if self.task_info.get("type") == "dynamic":
            self.task_info["server_work_dir"] = (self.task_path / "server").as_posix()
            self.server_manager = ServerManager(self.task_info)
            self.server_manager.start()
            self.init_user_prompt = create_task_prompt_from_task(
                self.task_info, self.server_manager.get_port()
            )
        else:
            self.init_user_prompt = create_task_prompt_from_task(self.task_info)

    def _init_agent(self) -> None:
        prompt_path = getattr(self.args, "system_prompt", "src/prompts/CTF/system_prompt")
        system_prompt = Path(prompt_path).read_text()
        self.log(f'System Prompt:\n\n{system_prompt}\n\n')
        self.agent = CryptoAgent(
            model_config=self.model_config,
            system_prompt=system_prompt,
            logger=self.logger,
            task_info=self.task_info,
            state_callback=self._save_state_callback,
        )

    # Callback passed into CryptoAgent so that every message append triggers
    # an immediate state.json flush.
    def _save_state_callback(self) -> None:
        self._save_state("Running")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self) -> bool:
        """Drive the agent through the task until success, give-up or limit."""

        get_flag = False
        next_user_input = self.next_user_input  # set by _prepare_initial_input
        time_start = datetime.now()
        self._log_event("Session started", time_start)

        # If resuming and *previous_state* indicates a terminal status
        # (True, False or "error: …"), exit immediately.
        prev_state = getattr(self, "previous_state", "Running")
        if prev_state != "Running":
            self.log("Nothing to do – returning stored outcome.")
            return prev_state is True

        for iteration in range(self.start_iteration, self.max_iterations + 1):
            # Keep instance attribute in sync for state persistence callbacks.
            self.next_user_input = next_user_input

            self._log_iteration(iteration, next_user_input)
            result = self.agent.run(next_user_input)
            self.dialog_record.append({"model": result["response"]})

            action = result["action_type"]
            if action == "verification":
                next_user_input = self._handle_flag_verification()
                if next_user_input is None:  # Success
                    get_flag = True
                    break
            elif action == "give up":
                self.log("Agent has given up on the task")
                break
            elif action == "command":
                next_user_input = self._format_command_output(result.get("output", ""))
            elif action == "create file":
                next_user_input = (
                    f"File creation result: {result.get('output', '')}\n\nContinue with the next step."
                )
            else:
                self.log(f"Unknown action: {action}")
                next_user_input = (
                    "I didn't understand your response. Please use the correct format with "\
                    "### Reasoning, ### Action, and ### Action Content sections."
                )

            # Persist intermediate state after each iteration so that we can
            # recover seamlessly if the process is interrupted.
            self._save_state("Running", next_user_input)

        self._finalise(get_flag, time_start)
        return get_flag

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _log_event(self, title: str, now: datetime) -> None:
        self.log(f"{title}: {now:%Y-%m-%d %H:%M:%S}")

    def _log_iteration(self, iteration: int, user_input: str) -> None:
        self.log(f"Starting iteration {iteration}/{self.max_iterations}")
        self.log(f"User input: {user_input}")
        self.dialog_record.append({"user": user_input})

    def _format_command_output(self, output: str) -> str:
        if len(output) > self._MAX_STDOUT_PREVIEW:
            output = truncate_long_string(output)
        return (
            "Command output:\n\n" + output + "\n\n" "Continue with the next step based on the command output."
        )

    # ----------------- flag verification --------------------------------

    def verify_flag(self) -> bool:
        """Compare file flag with ground-truth."""
        try:
            submitted_flag = self.flag_path.read_text().strip()
            return submitted_flag == self.true_flag
        except Exception as exc:  # noqa: BLE001 – propagate for higher-level handling
            self.log(f"Error reading flag file: {exc}")
            raise

    def _handle_flag_verification(self) -> Optional[str]:
        if not self.flag_path.exists():
            self.log("Flag verification failed – flag file not found.")
            return "Flag verification failed: flag file not found."

        try:
            if self.verify_flag():
                self.log("Flag verification successful! Task completed.")
                return None
            return "Flag incorrect. Please continue solving the challenge."
        except Exception as exc:
            self.log(f"Error during flag verification: {exc}")
            return f"Flag verification error: {exc}"

    # ----------------- teardown -----------------------------------------

    def _finalise(self, success: bool, start_time: datetime) -> None:
        if success:
            self.log("Task completed successfully!")
        else:
            self.log("Task failed.")

        self._log_event("Session ended", datetime.now())
        self.log(f"Total duration: {datetime.now() - start_time}")

        # Clean-up resources
        if self.server_manager:
            self.server_manager.stop()
        self.logger.close()

        # Persist dialog history & final state
        self.dialog_record_path.write_text(json.dumps(self.dialog_record, indent=2))
        self._save_state(success)

    # ------------------------------------------------------------------
    # Logging helper
    # ------------------------------------------------------------------

    def log(self, message: str) -> None:
        """Proxy to the configured :class:`Logger` instance."""
        self.logger.log(message)

    # ------------------------------------------------------------------
    # Resume helpers
    # ------------------------------------------------------------------

    def _resume_from_state(self) -> None:
        """If *state.json* exists, restore conversation & decide next steps."""

        if not self.state_path.exists():
            self.log("No previous state found – starting fresh.")
            return

        try:
            data = json.loads(self.state_path.read_text())
        except Exception as exc:  # noqa: BLE001
            self.log(f"Failed to load state.json: {exc}. Ignoring and starting fresh.")
            return

        self.previous_state = data.get("state", "Running")
        if self.previous_state is True:
            self.log("state.json indicates task already solved – will skip execution.")
        elif self.previous_state is False:
            self.log("state.json indicates task previously failed – will skip execution.")
        else:
            # Keep any non-boolean state string (e.g. "error: …") for the
            # caller to inspect; treat it as terminal for run().
            pass

        messages = data.get("messages", [])
        if messages:
            try:
                self.agent.model.load_messages(messages)
                self.log(f"Loaded {len(messages)} messages from previous session.")
            except Exception as exc:
                self.log(f"Could not load messages into model – {exc}")

        # Restore dialog_record similarly if desirable (optional).
        self.dialog_record = data.get("dialog_record", self.dialog_record)

    # ------------------------------------------------------------------
    # State persistence helpers
    # ------------------------------------------------------------------

    def _save_state(self, status: str | bool, next_user_input: Optional[str] = None) -> None:
        """Write *state.json* containing current status & conversation."""

        try:
            payload: Dict[str, Any] = {
                "state": status,
                "messages": self.agent.model.dump_messages(),
            }
            if next_user_input is None:
                # Use self.next_user_input tracked by run loop
                next_user_input = getattr(self, "next_user_input", None)
            if next_user_input is not None:
                payload["next_user_input"] = next_user_input

            self.state_path.write_text(json.dumps(payload, indent=2))
        except Exception as exc:  # noqa: BLE001
            self.log(f"Failed to persist state.json: {exc}")

    # ------------------------------------------------------------------
    # Initial input / iteration setup
    # ------------------------------------------------------------------

    def _prepare_initial_input(self) -> None:
        """Set *self.next_user_input* and *self.start_iteration* based on resume state."""

        if hasattr(self, "previous_state") and self.previous_state == "Running":
            # We resumed from an unfinished session.
            try:
                data = json.loads(self.state_path.read_text())
            except Exception:
                data = {}

            pending_input = data.get("next_user_input")

            # Append pending_input to messages if last message is assistant to
            # ensure the conversation ends with a user turn.
            if pending_input:
                if not self.agent.model.messages or self.agent.model.messages[-1]["role"] != "user":
                    self.agent.model.add_user_message(pending_input)

                self.next_user_input = pending_input
            else:
                # Fallback: re-use init prompt
                self.next_user_input = self.init_user_prompt

            self.start_iteration = len(self.agent.model.messages) // 2 + 1
        else:
            # Fresh run
            self.next_user_input = self.init_user_prompt
            self.start_iteration = 1


