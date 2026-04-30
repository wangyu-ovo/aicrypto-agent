import subprocess
import sys
import os
import signal
import time
import yaml  # Added to read the default model from the member config
from datetime import datetime

def run_benchmarks(member, task, model):
    prompt_modes = [
        "original", "prompt-charlie", "prompt-juan", 
        "prompt-justus", "prompt-miguel-i", "prompt-miguel-p", "prompt-ryan"
    ]
    TIMEOUT_SECONDS = 1200 

    for mode in prompt_modes:
        print(f"\n{'='*70}")
        print(f"MEMBER: {member}")
        print(f"TASK  : {os.path.basename(task.strip('/'))}")
        print(f"MODEL : {model}")
        print(f"PROMPT: {mode} | START: {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*70}")

        cmd = [
            "python", "run_member copy.py", 
            "--member", member, 
            "--task", task, 
            "--prompt-mode", mode
        ]

        proc = subprocess.Popen(cmd, preexec_fn=os.setsid)

        try:
            proc.wait(timeout=TIMEOUT_SECONDS)
            print(f"[SUCCESS] Completed {mode}")
            
        except subprocess.TimeoutExpired:
            print(f"\n[!] TIMEOUT: Killing run '{mode}' for {member} after 20 minutes...")
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            time.sleep(2) 
            print(f"[!] Cleaned up {mode}")
            
        except Exception as e:
            print(f"\n[!] ERROR: {e}")
            if proc.poll() is None:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python run_all_prompts.py <member_name> <task_path> [model_name]")
        sys.exit(1)

    MEMBER_NAME = sys.argv[1]
    TASK_PATH = sys.argv[2]
    
    # Check if model_name is provided as the 3rd argument
    if len(sys.argv) >= 4:
        MODEL_NAME = sys.argv[3]
    else:
        # Default: Load model from the member's YAML config
        config_path = f"config/members/{MEMBER_NAME}.yaml"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                MODEL_NAME = config.get("model", "unknown_model")
        else:
            print(f"Error: Config for {MEMBER_NAME} not found at {config_path}")
            sys.exit(1)

    if not os.path.exists(TASK_PATH):
        print(f"Error: Path '{TASK_PATH}' not found.")
        sys.exit(1)
        
    run_benchmarks(MEMBER_NAME, TASK_PATH, MODEL_NAME)