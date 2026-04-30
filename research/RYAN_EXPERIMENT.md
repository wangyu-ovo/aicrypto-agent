# Ryan's Experiment

For the Student Researcher part of the project I wanted to see if I could get
the LLM to solve CTF problems faster by changing the system prompt. Our paper
said LLMs struggle with multi-step reasoning, and our proposal mentioned that
CTF challenges are basically "a breach in confidentiality", so I figured if
I make the model walk through a Confidentiality Analysis before each action,
maybe it'll be more focused and finish in fewer iterations.

I started with one task and one model comparison, then expanded into a full
sweep across 5 tasks and both Opus 4.7 modes (thinking + non-thinking) so I
could see whether the CIA prompt's effect held up beyond a single test.

## Tasks tested

I picked one task from each of 5 categories so the result wouldn't depend on
the type of cipher:

- `data/CTF/01-Classic/01-greek-cipher`
- `data/CTF/02-Block/01-integral-communication`
- `data/CTF/03-Stream-PRNG-Hash/01-babycharge`
- `data/CTF/04-RSA/01-blue-hens-2023` (original target task, "RSA School 3rd Grade")
- `data/CTF/05-DLP/01-prove-it`

## The prompt I added

The Analysis I added has 4 questions taken from the CIA triad lecture:
1. What needs to be protected?
2. How much protection is needed?
3. For how long is protection needed?
4. Which threat applies (Exposure / Interception / Inference / Intrusion)?

The model has to answer all 4 in a "Step 0" section before picking any
Action. Everything else in the prompt is identical to the original.

I also wanted to see if it mattered whether the model was using extended
thinking or not, so I tested both `claude-opus-4-7` and the thinking version.

## Files I added

- `config/members/ryan.yaml`: non-thinking model config
- `config/members/ryan-thinking.yaml`: thinking model config
- `config/custom_prompts/ryan_instructional.txt`: my CIA prompt (used by
  both yamls, same prompt for both model modes)
- `run_ryan_sweep.sh`: sequential driver for my 5 tasks × 2 models sweep
- `parallel_sweep.sh`: parallel driver I wrote to speed up the longer
  thinking-model rows once I realized the sequential version would take
  hours
- `parse_runs.py`: small aggregator that walks `outputs/` and prints
  status / duration / iter counts for every (task × prompt × model) cell

## How to run it

From `~/aicrypto-agent` with conda env `crypto`:

Single run (the comparison from the original 1-task version of this doc):

```bash
# baseline
python run_member.py --member ryan --task data/CTF/04-RSA/01-blue-hens-2023 --prompt-mode original
# my CIA prompt
python run_member.py --member ryan --task data/CTF/04-RSA/01-blue-hens-2023 --prompt-mode instructional
```

Full sweep across all 5 tasks (sequential, slow):

```bash
bash run_ryan_sweep.sh
```

Faster parallel version (launches multiple prompt modes concurrently; be
mindful of API rate limits):

```bash
bash parallel_sweep.sh
```

After it finishes, summarize all completions:

```bash
python parse_runs.py
```

Logs end up at `outputs/CTF-ryan/.../run/run.log` (non-thinking) and
`outputs/CTF-ryan-thinking/.../run/run.log` (thinking).

## What I got

Comparing my CIA prompt (`prompt-ryan`) against the unmodified `original`
across all 5 tasks. Format is `iters / duration`. **Bold** = the bigger
gap, in either direction.

### Non-thinking model (`claude-opus-4-7`)

| task | original | ryan (CIA) |
|---|---|---|
| greek-cipher | Failure | Failure |
| integral-communication | 6 / 0:09:03 | **6 / 0:03:26** |
| babycharge | 8 / 0:01:17 | 9 / 0:01:42 |
| blue-hens-2023 | 7 / 0:01:28 | **4 / 0:00:53** |
| prove-it | 10 / 0:10:14 | **Failure** |

### Thinking model (`claude-opus-4-7-thinking`)

| task | original | ryan (CIA) |
|---|---|---|
| greek-cipher | Failure | Failure |
| integral-communication | 10 / 0:15:50 | **6 / 0:11:38** |
| babycharge | 7 / 0:00:52 | 7 / 0:02:17 |
| blue-hens-2023 | 5 / 0:00:35 | 7 / 0:00:24 |
| prove-it | 23 / 0:15:23 | **12 / 0:04:09** |

## What I think this means

My original 1-task hypothesis ("CIA scaffolding only helps if the model is
already doing internal reasoning") was right in *direction* but too clean.
The 5-task sweep shows a more nuanced picture:

- **Thinking model**: CIA prompt is a clear win on the harder tasks. On
  `prove-it` it cut iterations almost in half (23 → 12) and was 4× faster
  (15:23 → 4:09). On `integral-communication` it went 10 → 6 iters and
  shaved 4 minutes off.
- **Non-thinking model**: genuinely mixed. CIA helped a lot on
  `integral-communication` (3× faster) and `blue-hens-2023` (4 iters vs
  7), was a wash on `babycharge`, and *broke* `prove-it` entirely
  (`original` solved it; CIA failed). So the scaffolding can actively
  hurt when the model isn't reasoning internally.
- **Both modes fail on `greek-cipher`** regardless of prompt. That's a
  separate finding: none of the 7 prompt variants the team tested
  cracked the Greek cipher, and the thinking model burned through 100
  iterations on every attempt without converging. The bottleneck there
  is the model's ability to recognize/break the cipher, not the prompt
  scaffold.

Net takeaway: the CIA-triad prompt is a reasonable add-on for the thinking
model, but I'd not enable it by default for non-thinking mode without
checking the specific task as it can regress something that was working.
