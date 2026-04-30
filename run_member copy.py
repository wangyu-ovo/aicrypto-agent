"""run_member.py
----------------
Per-member entry point for the AICrypto CTF benchmark.

Each team member has a config in config/members/<name>.yaml defining
their model and providing altered prompt pathways. The CTF challenge 
and selected prompt are specified on the command line.

Usage Examples:
    python run_member.py --member charlie --task data/CTF/04-RSA/01-blue-hens-2023 --prompt-mode prompt-charlie
    python run_member.py --member charlie --task data/CTF/04-RSA/01-blue-hens-2023 --prompt-mode prompt-justus
    python run_member.py --member charlie --task data/CTF/04-RSA/01-blue-hens-2023 --prompt-mode prompt-miguel-p
    python run_member.py --member charlie --task data/CTF/04-RSA/01-blue-hens-2023 --prompt-mode original

Results saved to: outputs/CTF-<member>/<category>/<challenge>/<model>/run/
"""

import argparse
import json
import os
import signal
import sys
import traceback
from pathlib import Path
from types import SimpleNamespace

import yaml

from src.agent.task_runner import TaskRunner
from datetime import datetime

# ---------------------------------------------------------------------------
# Limit thread-hungry math libraries (OpenBLAS, MKL, OpenMP, etc.) to a single
# worker thread **before** they are imported anywhere else.  This prevents
# errors such as "OpenBLAS blas_thread_init: pthread_create failed… Resource
# temporarily unavailable" when many tasks run concurrently.
# Users can override the limits by explicitly exporting the variables with a
# different value *before* invoking this script.
# ---------------------------------------------------------------------------
for _var in (
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "OMP_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
):
    os.environ.setdefault(_var, "1")

#Defines acceptable input and reads it from the command line
def parse_args():
    parser = argparse.ArgumentParser(
        description="Run a CTF task for a specific team member."
    )
    parser.add_argument(
        "--member", required = True,
        help="Member name — must match config/members/<name>.yaml (e.g. charlie)"
    )
    parser.add_argument(
        "--task", required = True,
        help="CTF task path (e.g. data/CTF/04-RSA/01-blue-hens-2023)"
    )
    parser.add_argument(
        "--prompt-mode", required = True,
        choices=["original", "prompt-charlie", "prompt-juan", "prompt-justus", "prompt-miguel-i", "prompt-miguel-p", "prompt-ryan"],
        help="Which prompt variant to use"
    )
    # Note: model is specified per-member in config/members/<member>.yaml,
    return parser.parse_args()

#Constructs path and checks if it exists
def load_member_config(member: str) -> dict:
    config_path = Path(f"config/members/{member}.yaml")
    if not config_path.exists():
        print(f"Error: No config found at {config_path}")
        print(f"Create one by copying config/members/charlie.yaml")
        sys.exit(1)
    with open(config_path) as f:
        return yaml.safe_load(f)

# Looks up path, checks if it exists, and returns path string
def resolve_prompt_path(config: dict, prompt_mode: str) -> str:
    prompt_path = config["prompts"].get(prompt_mode)
    if not prompt_path:
        print(f"Error: No prompt defined for mode '{prompt_mode}' in member config")
        sys.exit(1)
    if not Path(prompt_path).exists():
        print(f"Error: Prompt file not found: {prompt_path}")
        print(f"       Create the file and add your prompt text.")
        sys.exit(1)
    return prompt_path

#Returns a namespace for TaskRunner
def build_args(config: dict, task: str, prompt_mode: str, prompt_path: str) -> SimpleNamespace:
    # 1. Generate the timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # 2. Extract category and challenge from the task path
    # Removes 'data/' and splits the remaining path
    parts = Path(task).parts
    # Assuming path is: data / CTF / <category> / <challenge>
    category = parts[2] if len(parts) > 2 else "unknown_cat"
    challenge = parts[3] if len(parts) > 3 else "unknown_task"
    
    # 3. Construct the new nested path
    # Format: outputs/CTF-<member>/<category>/<challenge>/<model>/<time>/run/
    dynamic_path = os.path.join(
        "outputs", 
        f"CTF-{config['member']}-{prompt_mode}", 
        category, 
        challenge, 
        config["model"].replace("/", "_"), # Replace slashes in model names for valid paths
        timestamp,
        "run"
    )

    return SimpleNamespace(
        task_path=task,
        model=config["model"],
        max_iterations=100,
        output_dir=dynamic_path, # Pass the new nested path here
        system_prompt=prompt_path,
        id=config["member"],
    )

_ACTIVE_RUNNER = None

def _graceful_shutdown(signum, frame):  # noqa: D401 – callback, ignore frame
    """Signal handler to terminate the TaskRunner and its server cleanly."""
    global _ACTIVE_RUNNER  # noqa: PLW0603 – required to modify global

    if _ACTIVE_RUNNER is not None:
        try:
            _ACTIVE_RUNNER.log(f"Received signal {signum}; shutting down gracefully…")
            if _ACTIVE_RUNNER.server_manager:
                _ACTIVE_RUNNER.server_manager.stop()
        except Exception:
            pass

    # Exit with 128 + signal number (conventional for Unix)
    sys.exit(128 + signum)

def main():
    global _ACTIVE_RUNNER

    args = parse_args()
    config = load_member_config(args.member)
    prompt_path = resolve_prompt_path(config, args.prompt_mode)

    print(f"\nAICrypto CTF — Member Run")
    print(f"  Member      : {config['member']}")
    print(f"  Task        : {args.task}")
    print(f"  Model       : {config['model']}")
    print(f"  Prompt mode : {args.prompt_mode}")
    print(f"  Prompt file : {prompt_path}")
    
    # Initialize the arguments first
    runner_args = build_args(config, args.task, args.prompt_mode, prompt_path)
    print(f"  Output dir  : {runner_args.output_dir}\n")

    # Create the full directory structure before starting the task
    Path(runner_args.output_dir).mkdir(parents=True, exist_ok=True)


    try:
        #Register signal handlers **before** heavy processing starts so that
        # we can react to Ctrl-C or SIGTERM.
        signal.signal(signal.SIGINT, _graceful_shutdown)
        signal.signal(signal.SIGTERM, _graceful_shutdown)

        runner = TaskRunner(runner_args)
        _ACTIVE_RUNNER = runner

        task_result = runner.run()  # ``True`` when flag verified successfully.

        summary = {
            "member": config["member"],
            "task": args.task,
            "model": config["model"],
            "prompt_mode": args.prompt_mode,
            "result": task_result,
        }
        print(json.dumps(summary, indent=2))

    except Exception as exc:  # noqa: BLE001 – we want to catch everything
        # If 'runner' exists it means TaskRunner initialised successfully – log
        # the error through its logger.  Otherwise fall back to stderr.
        if 'runner' in locals():
            runner.log(f"Unexpected error in run_member.py: {exc}\n{traceback.format_exc()}")
            try:
                # Persist failure reason so that parallel runner can resume correctly.
                runner._save_state(f"error: {exc}")  # type: ignore[attr-defined]
            except Exception:
                # Ignore any issues during error persistence.
                pass
        else:
            print(f"Unexpected error before TaskRunner initialisation: {exc}", file=sys.stderr)
        
        print(json.dumps({
            "member": config["member"],
            "task": args.task,
            "model": config["model"],
            "prompt_mode": args.prompt_mode,
            "result": False,
            "error": str(exc),
        }, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()




