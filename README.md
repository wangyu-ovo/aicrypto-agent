# AICrypto — Group 11 Fork

[![Paper](https://img.shields.io/badge/Paper-arXiv-red)](https://arxiv.org/abs/2507.09580)
[![Original Repo](https://img.shields.io/badge/Original-Repo-gray)](https://github.com/wangyu-ovo/aicrypto-agent)
[![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/yuuwwang/aicrypto)

Fork of the [AICrypto benchmark](https://github.com/wangyu-ovo/aicrypto-agent) for a Systems Security course group project. We reproduced the paper's results and extended the benchmark with a per-member prompt injection system.

---

## Setup

> All steps must be run on Linux (Ubuntu 20.04 recommended).
>
> **Important:** These setup steps are for Linux (Ubuntu 20.04) running on an x86_64 machine. The conda environment will not work on macOS (including Apple Silicon or Intel Macs) due to Linux-only dependencies. Use the VirtualBox VM provided in class.

### Prerequisites

- Python 3.10.15
- SageMath 10.5
- yafu 1.34.5
- VirtualBox VM (Not strictly necessary if the environment can be replicated; an excess of 5000 MB base memory is recommended for some operations)

### Installation

1. **Install Git and clone:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install git -y
   cd ~/Documents
   git clone https://github.com/CharlieBoi2148/aicrypto-agent.git
   cd aicrypto-agent
   git checkout main
   ```

2. **Install Miniconda:**
   ```bash
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh
   source ~/.bashrc
   ```
   During installation: accept the license, confirm the default install location, and type `yes` to initialize Miniconda.

3. **Create the conda environment:**

   > The original `environment.yml` has a Cascadelake CPU constraint that fails on VirtualBox. Use the fix below — do **not** run `conda env create -f environment.yml` directly.

   ```bash
   grep -v "_x86_64-microarch-level" environment.yml > environment_fixed.yml
   conda env create -f environment_fixed.yml --solver=classic
   ```
   This step takes 20–40 minutes. Once complete:
   ```bash
   conda activate crypto
   ```

4. **Install SageMath dependencies:**
   ```bash
   sage -pip install -r sage-requirements.txt
   ```

5. **Install flatter:**
   ```bash
   sudo apt install libgmp-dev libmpfr-dev fplll-tools libfplll-dev libeigen3-dev libopenblas-dev cmake -y
   cd ~/Documents
   git clone https://github.com/keeganryan/flatter.git
   cd flatter && mkdir build && cd build
   cmake .. && make && sudo make install && sudo ldconfig
   cd ~/Documents/aicrypto-agent
   ```

6. **Install yafu:**
   ```bash
   sudo apt install libgmp-dev libecm-dev -y
   cd ~/Documents
   git clone https://github.com/bbuhrow/yafu.git
   cd yafu
   make -f Makefile.gcc yafu
   sudo cp ~/Documents/yafu/yafu /usr/local/bin/
   cd ~/Documents/aicrypto-agent
   ```

7. **Fix proof data path:**
   ```bash
   ln -s proof_problems data/Proof
   ```

8. **Configure API keys:**
   ```bash
   nano .env
   ```
   ```
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   ```
   > Do not commit this file to GitHub.

9. **Install additional dependencies:**
   ```bash
   pip install pyyaml
   ```

---

## Usage

### Run Single CTF Challenge

```shell
python run_single_ctf_task.py --task-path data/CTF/04-RSA/01-blue-hens-2023 --model gpt-4.1 --id 0
```

Results are saved to `./outputs/CTF-0/04-RSA/01-blue-hens-2023/gpt-4.1/run`.

### Run CTF Challenges in Parallel for Evaluation

```shell
python batch_run_ctf.py --jobs 4 --id 0
```

Uses 4 processes to run tasks with run ID 0. Results saved to `./outputs/CTF-0`. Models are specified in `config/model.yaml`.

### Run Single MCQ Evaluation

```shell
python run_choice_question.py --model gpt-4.1
```

Results are saved to `./outputs/MultipleChoice_EDIT/<model_name>/`.

### Run MCQ Evaluation in Parallel

```shell
python batch_run_choice_question.py --parallel --jobs 4
# Optionally select specific models:
python batch_run_choice_question.py --parallel --jobs 4 --models gpt-4.1 o3
```

### Run Single Proof Task

```shell
python run_proof_task.py --exam 1 --model gpt-4.1
```

Outputs:
- Proofs: `./outputs/proof/exam1/proof/gpt-4.1_proof_results.tex`
- Reasoning: `./outputs/proof/exam1/reasoning/gpt-4.1_reasoning_results.tex`
- Logs: `./outputs/proof/exam1/log/`

### Run Proof Tasks in Parallel

```shell
python batch_run_proof_tasks.py --exam-values 1 2 3 --jobs 4
```

---

## Our Extension — Prompt Engineering

We added `run_member.py`, a new run command that lets each team member swap the CTF agent's system prompt with a custom technique. Each member has a config in `config/members/<name>.yaml` that declares their model and includes available prompt paths. One exception is listed below:
- ryan-thinking.yaml
This member file is made to handle an additional model handled by member Ryan. The -thinking appended at the end of the file name is for organizational and testing purposes, referencing the related model name stored within.

Below are example instructions for running prompts through member "charlie".

```bash
python run_member.py --member charlie --task data/CTF/04-RSA/01-blue-hens-2023 --prompt-mode original
python run_member.py --member charlie --task data/CTF/04-RSA/01-blue-hens-2023 --prompt-mode prompt-charlie
python run_member.py --member charlie --task data/CTF/04-RSA/01-blue-hens-2023 --prompt-mode prompt-justus
```

It is important to note that all prompts can be run on any member. However, the model is member-dependent for testing and running purposes. Additionally, while most altered prompts follow a `prompt-<member name>` format, three exceptions exist as listed below:
- original
- prompt-miguel-i
- prompt-miguel-p
Running the "original" prompt through any member will cause the program to reference the original, unaltered system prompt. Both prompt-miguel-i and prompt-miguel-p run altered prompts, wherein prompt-miguel-i is "instructional," attempting to increase success rate and reduce iterations, and prompt-miguel-p is "poisoned," attempting to decrease success rate and increase iterations.

`--prompt-mode` accepts: `original | prompt-charlie | prompt-juan | prompt-justus | prompt-miguel-i | prompt-miguel-p | prompt-ryan`. Model is pulled from `config/members/<member>.yaml`, not from the CLI, so each member's results use their declared model consistently.

For testing purposes, another function named `run_all_prompts.py` was created to streamline prompt running. Instead of requiring manual input of each prompt for the same test, this function can be called as a run command and will automatically run the original prompt and our added custom prompts sequentially. It includes a failsafe, automatically terminating the program after 20 minutes to prevent excessive token usage in cases of expected failure (as, for our project, this is a serious concern and limitation).

Below are example instructions for running all prompts through member "charlie".

```bash
python run_all_prompts.py charlie data/CTF/04-RSA/01-blue-hens-2023
python run_all_prompts.py charlie data/CTF/01-Classic/01-greek-cipher
python run_all_prompts.py charlie data/CTF/03-Stream-PRNG-Hash/01-babycharge
```

To add a new member, copy an existing member file, rename it to `<name>.yaml`, and update associated name and model values.

---

## Purpose of our Extension

This extension was created to test the influence of prompts on LLM performance in multi-step scenarios. The performance of each LLM when given a specific altered prompt reveals a bit about its abilities; for example, prompt-justus includes 'prompt injection' inspired instructions intended to slow and impair CTF problem solving. The results, relative to base performance, can help reveal how well the tested model successfully interprets and organizes the information it receives. Other prompts provide insight into the way LLMs process information, such as prompt-ryan recontextualizing the question as a confidentiality breach that the LLM is prompted to better understand prior to solving.

## Configuration

- **Models**: Configure available models in `config/model.yaml`
- **Custom Models**: Add custom model implementations in `src/model/`
- **API Keys**: Set up your API keys in the `.env` file


## What Works / What Doesn't

**Works:**
- MCQ benchmark (all 135 questions)
- CTF challenges in the RSA category
- Proof generation (exam 1, all 6 problems)
- Per-member prompt running via `run_member.py`
- Gemini 3.1 compatibility
- Claude Opus 4.7 compatibility
- Claude Opus 4.7 Thinking compatibility

**Does not work:**
- Proof grading — requires `gpt-5.1` and `gemini-3-pro-preview` as graders; these are not included in the repository. Only proof generation can be reproduced.
- Full LLM Compatibility with custom prompts — For testing purposes, custom prompts are run through individual member files where each member is associated with a particular model. As a result, only 6 LLMs (1 per associated member, with the exception of Ryan who has 2) can be tested with custom prompts. However, model values inside each member file can be updated to work with any models in config > model.yaml or a new member can be created to handle a new model inside config > model.yaml with ease.
- CTF Parallelization for custom prompts — Our custom prompts are incompatible with batch_run_ctf.py as implementation is handled by custom runners run_member.py and run_all_prompts.py. Parallelization is efficient but incredibly draining on our limited tokens and may significantly impact runtime calculations, so single-prompt runs have been prioritized.

---

## Scholarly References

**Prior/Foundational Work:**

* **Yang, Y., Yamada, H., & Tokunaga, T. (2025).** *Evaluating Robustness of LLMs to Numerical Variations in Mathematical Reasoning.* The Sixth Workshop on Insights from Negative Results in NLP.
    * **Contribution:** Proposes the GSM-ALT dataset to test how LLMs handle numerical perturbations in math word problems. The study concludes that LLMs are highly vulnerable to numerical variations, indicating that their mathematical reasoning is often a reliance on superficial pre-training patterns and that they fundamentally struggle with arithmetic operations.

* **Maskey, U., Zhu, C., & Naseem, U. (2025).** *Benchmarking Large Language Models for Cryptanalysis and Side-Channel Vulnerabilities.* arXiv preprint arXiv:2505.24621v2.
    * **Contribution:** Evaluates LLM cryptanalysis capabilities across various ciphers, revealing that models generally only comprehend obfuscation methods that appear frequently in their pre-training corpora. It establishes a critical baseline for LLM limitations, demonstrating that models struggle to generalize when faced with high token-inflation methods or arbitrary character substitution.

* **Luong, T., et al. (2025).** *Towards Robust Mathematical Reasoning.* Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing.
    * **Contribution:** Introduces IMO-Bench (AnswerBench, ProofBench, and GradingBench) to evaluate models on International Mathematical Olympiad-level problems. The paper demonstrates that while frontier models are becoming adept at short-answer tasks, rigorous proof generation remains a significant hurdle, pushing the evaluation landscape to focus on deep, verifiable reasoning rather than final-answer matching.

**Contemporary Work:**

*Recent advancements (late 2025–2026) showcasing the shift toward autonomous agents, reinforcement learning, and real-world vulnerability discovery.*

* **Muzsai, L., Imolai, D., & Lukács, A. (2025).** *Improving LLM Agents with Reinforcement Learning on Cryptographic CTF Challenges.* Eötvös Loránd University.
    * **Contribution:** Introduces the **RANDOM-CRYPTO** dataset to fine-tune tool-augmented LLM agents using **Group Relative Policy Optimization (GRPO)**. The study proves that reinforcement learning significantly improves procedural reasoning and secure tool execution, with capabilities successfully generalizing to external benchmarks like picoCTF and AICrypto.
* **Cui, Y., Fu, H., Zhang, H., Wang, L., & Zuo, C. (2025).** *FREE-MAD: Consensus-Free Multi-Agent Debate.* arXiv preprint arXiv:2509.11035v1.
    * **Contribution:** Proposes a "consensus-free" Multi-Agent Debate (MAD) framework designed to mitigate the inherent conformity of LLMs during multi-agent interactions. Instead of relying on a final consensus or majority vote, FREE-MAD introduces a score-based mechanism that evaluates the entire debate trajectory. This approach achieves higher reasoning accuracy and fairness while significantly reducing token overhead by operating effectively as a single-round debate.
* **Anthropic. (2026).** *Partnering with Mozilla to Improve Firefox's Security.*
    * **Contribution:** An industry case study documenting how **Claude Opus 4.6** autonomously discovered 22 zero-day vulnerabilities (including 14 high-severity flaws) in the highly complex Firefox codebase over two weeks. It highlights the rapid transition of LLMs toward real-world vulnerability discovery at scale, while critically noting that the model's ability to actually *exploit* these vulnerabilities remains limited and currently requires disabled security sandboxes to succeed.
* **Mastrodonato, M. (2026).** *How Good Are Today's AIs at Cryptography and Mathematics?* Medium.
    * **Contribution:** A practitioner’s perspective on the "zero-tolerance" nature of cryptography. It argues that unlike general software engineering, the binary success/failure state of cryptographic tasks provides a more rigorous measure of an LLM's true reasoning depth.

---
