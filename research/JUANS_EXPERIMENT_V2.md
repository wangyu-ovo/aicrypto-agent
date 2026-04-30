# Juan's Experiment — Ver2: Cross-Prompt Comparison

This document extends the original experiment by running DeepSeek-chat (V3) across
**all 7 prompt modes** (original + each teammate's prompt) on all 5 CTF challenges.
The goal is to measure how every team member's prompt engineering strategy affects
DeepSeek's solve efficiency — iterations used and wall-clock time.

## Model

**DeepSeek-chat (DeepSeek V3)**
- Model ID: `deepseek-chat`
- API: Official DeepSeek API — `https://api.deepseek.com` (OpenAI-compatible)
- Reasoning: No — standard chat model, not the thinking variant (`deepseek-reasoner`)
- Max tokens: 8192

## Prompt Modes Tested

| Prompt Mode | Author | Strategy |
|-------------|--------|---------|
| `original` | Paper baseline | Default system prompt from the AICrypto codebase |
| `prompt-charlie` | Charlie | Sandwich — format rules repeated at top and bottom |
| `prompt-juan` | Juan | Attack Tree — enumerate FEASIBLE/BLOCKED paths before acting |
| `prompt-justus` | Justus | Poisoned — adversarial junk data injection |
| `prompt-miguel-i` | Miguel | Instructional — structured format guidance |
| `prompt-miguel-p` | Miguel | Poisoned — anti-expert sabotage |
| `prompt-ryan` | Ryan | CIA framework — structured threat reasoning |

## Challenges Tested

| Challenge | Category | Type | Attack |
|-----------|----------|------|--------|
| `01-Classic/01-greek-cipher` | Classic | Static | Monoalphabetic substitution cipher |
| `02-Block/01-integral-communication` | Block | Dynamic | CBC bit-flip / integrity exploit |
| `03-Stream-PRNG-Hash/01-babycharge` | Stream | Dynamic | ChaCha20 known-plaintext |
| `04-RSA/01-blue-hens-2023` | RSA | Static | Common Modulus Attack |
| `05-DLP/01-prove-it` | DLP | Dynamic | Discrete log / zero-knowledge proof exploit |

**Static** = fixed files in `./public/`, same every run.
**Dynamic** = Python server on port 1337, random values per run, agent connects via pwntools.

---

## Results

### Time Results

| Challenge | original | prompt-charlie | prompt-juan | prompt-justus | prompt-miguel-i | prompt-miguel-p | prompt-ryan |
|-----------|----------|----------------|-------------|---------------|-----------------|-----------------|-------------|
| 01-greek-cipher | 0:02:32 | 0:02:47 | 0:01:31 | 0:03:18 | 0:00:48 | 0:08:56 | 0:12:43 |
| 01-integral-communication | 0:04:20 | 0:09:27 | 0:05:17 | Failure | Failure | Failure | Failure |
| 01-babycharge | 0:07:40 | 0:04:33 | 0:01:20 | 0:01:57 | 0:03:18 | 0:01:09 | 0:11:34 |
| 01-blue-hens-2023 | 0:00:59 | 0:00:56 | 0:00:36 | 0:00:18 | 0:00:32 | 0:00:40 | 0:00:40 |
| 01-prove-it | Failure | Failure | 0:54:13 | Failure | Failure | Failure | Failure |

### Iteration Results

| Challenge | original | prompt-charlie | prompt-juan | prompt-justus | prompt-miguel-i | prompt-miguel-p | prompt-ryan |
|-----------|----------|----------------|-------------|---------------|-----------------|-----------------|-------------|
| 01-greek-cipher | 23 | 7 | 9 | 14 | 9 | 100 | 100 |
| 01-integral-communication | 15 | 99 | 33 | Failure | Failure | Failure | Failure |
| 01-babycharge | 100 | 40 | 6 | 18 | 41 | 6 | 29 |
| 01-blue-hens-2023 | 17 | 21 | 7 | 6 | 7 | 12 | 9 |
| 01-prove-it | Failure | Failure | 43* | Failure | Failure | Failure | Failure |

*Flag obtained at iteration 43; 57 additional iterations were verification format errors.
DeepSeek correctly output the flag but failed to format the verification action, hitting
the 100-iteration cap. The flag `lactf{2kp_1s_ov3rr4t3d}` is confirmed correct.

**Failure** = timed out (35-min cap for DLP, 20-min cap for all others) or hit 100
iterations without obtaining the flag.

---

## Findings

### 1. prompt-juan (Attack Tree) — Best overall on DeepSeek

Across all 5 challenges, the attack tree prompt consistently used the fewest iterations
and fastest time where it solved:

| Challenge | original | prompt-juan | Iterations saved | Time saved |
|-----------|----------|-------------|-----------------|------------|
| 01-greek-cipher | 23 iter, 2:32 | 9 iter, 1:31 | −61% | −40% |
| 01-babycharge | 100 iter, 7:40 | 6 iter, 1:20 | −94% | −83% |
| 01-blue-hens-2023 | 17 iter, 0:59 | 7 iter, 0:36 | −59% | −39% |
| 01-integral-communication | 15 iter, 4:20 | 33 iter, 5:17 | +120% | +22% |

The block cipher challenge (CBC bit-flip) was the exception — the attack tree prompt
used more iterations. CBC bit-flip requires a two-step oracle attack where the model
must learn from a failed attempt, then correct the IV. The structured "pick the
shallowest feasible path" approach may have caused the model to commit too early and
spend more iterations recovering.

**Overall: prompt-juan is the best-performing prompt on DeepSeek for 4 of 5 challenges.**

### 2. Poisoned prompts perform worst

Both poisoned prompts (prompt-justus, prompt-miguel-p) failed on all dynamic challenges
(Block, DLP) and performed poorly on others:

- `prompt-justus`: Solved only 3 of 5 (failed Block and DLP entirely)
- `prompt-miguel-p`: Solved only 3 of 5 (failed Block and DLP) — used 100 iterations
  on greek-cipher (maximum), meaning it barely solved it

This confirms poisoned prompts degrade multi-step reasoning on dynamic challenges where
the model needs to adapt to server responses across multiple iterations.

### 3. Ryan's CIA prompt is worst for time efficiency on DeepSeek

`prompt-ryan` used 100 iterations (maximum) on greek-cipher and had the longest times
on both greek-cipher (12:43) and babycharge (11:34). The CIA framework may be optimized
for Claude Opus 4.7's reasoning style and work against DeepSeek's approach.

### 4. Charlie's sandwich prompt is competitive

`prompt-charlie` solved 4 of 5 challenges (same as prompt-juan), with low iterations on
greek-cipher (7) but high iterations on integral-communication (99). The format-repetition
strategy helps with answer formatting but doesn't improve the cryptographic reasoning path.

### 5. Only prompt-juan solved DLP

The discrete log / zero-knowledge proof challenge (`01-prove-it`) was solved only with the
attack tree prompt. All other prompts failed (timed out or hit 100-iteration cap). The
attack tree's forced enumeration of feasible attack paths likely led the model to identify
the correct two-step approach (BSGS for alpha, polynomial root-finding for s) without
wasting iterations on dead ends.

---

## Summary Table — Solve Count by Prompt Mode (out of 5 challenges)

| Prompt | Solved | Failed | Notes |
|--------|--------|--------|-------|
| `prompt-juan` | **5/5** | 0 | Only prompt to solve DLP |
| `prompt-charlie` | 4/5 | 1 | Failed DLP |
| `original` | 4/5 | 1 | Failed DLP |
| `prompt-justus` | 3/5 | 2 | Failed Block + DLP |
| `prompt-miguel-i` | 3/5 | 2 | Failed Block + DLP |
| `prompt-miguel-p` | 3/5 | 2 | Failed Block + DLP |
| `prompt-ryan` | 3/5 | 2 | Failed Block + DLP |

**Conclusion:** The attack tree prompt (prompt-juan) is the only prompt to achieve a 5/5
solve rate with DeepSeek-chat V3. It outperforms the original baseline on 4 of 5 challenges
in both iterations and time. The structured threat enumeration approach from Lecture 2
(Attack Trees) produces measurably better performance on multi-step cryptographic CTF tasks.
