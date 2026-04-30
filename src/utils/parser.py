import argparse


def single_task_args():
    parser = argparse.ArgumentParser(description="LLM Crypto Agent")
    parser.add_argument("--model", type=str, default="claude-3.7-sonnet", 
                        help="The LLM model to use (default: claude-3.7)")
    parser.add_argument("--task-path", type=str, default="./data/data2/02-DLP/",
                        help="Path to the task.json file")
    parser.add_argument("--max-iterations", type=int, default=100,
                        help="Maximum number of iterations before stopping") 
    parser.add_argument("--output-dir", type=str, default="auto",
                        help="Directory to save outputs including records and parameters (default: auto)")
    parser.add_argument("--system-prompt", type=str, default="src/prompts/CTF/system_prompt",
                        help="Path to system prompt file")
    
    return parser.parse_args()