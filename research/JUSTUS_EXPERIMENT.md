# Justus' Experiment

I was inspired by the prompt injection techniques we briefly discussed at the beginning of our class and I wondered if it was possible to utilize those techniques in more subtle ways. My prompt follows the practice of "inserting malicious instructions among seemingly normal text," but these malicious instructions are intentionally easy to ignore and don't rarely contradict statements from the original prompt. The reason for this is because running this prompt helps evaluate how well the LLM models used are able to identify, evaluate, and handle these instructions. If time or iterations increase, the assumption would be that it's a result of failing to identify or getting distracted by these malicious prompts, resulting in expended time or manipulated outputs. If, on the other hand, time or iterations are lower than the original prompt, it may suggest that the model in question responded to the clearly malicious prompts by better evaluating other, legitimate instructions.

## What was tested

Challenges:
`data/CTF/01-Classic/01-greek-cipher`
`data/CTF/02-Block/01-integral-communication`
`data/CTF/03-Stream-PRNG-Hash/01-babycharge`
`data/CTF/04-RSA/01-blue-hens-2023`
`data/CTF/05-DLP/01-prove-it`

These are the first questions from the first five categories of CTF problems, covering classic, block, stream prng hash, rsa, and dlp problems.

Prompts:
`original`
`prompt-charlie`
`prompt-juan`
`prompt-justus`
`prompt-miguel-i`
`prompt-miguel-p`
`prompt-ryan`

We tested the original prompt, an altered prompt from each member, and an additional altered prompt from Miguel. Most prompts are intended to help increase accuracy with the exception of prompt-justus and prompt-miguel-p which are intended to decrease accuracy.

Model:
`o3-mini`

The model related to the justus member file that I used for testing was o3-mini. This was one of the models included in the original paper and has not been added separately. In the sample challenges, its success rate was subpar, as suggested by its 30% accuracy in most categories.

## Files I added

- `config/members/justus.yaml` - my member file
- `config/custom_prompts/justus_poisoned.txt` — my prompt file
- Note: I have made many adjustments to member files, the readme file, and run_member.py in the process of providing full prompt integration. The purpose of these changes were to ensure context, accuracy, and provided information were consistent and sufficient. Further details are outlined in my git commits.

## How to use my prompt/member file

I highly recommend referring to README.md for prompt running instructions! A snippet of README.md has been added to run_member.py for convenince as well.

Here is an example of using member justus and prompt-justus in a single run:

```bash
python run_member.py --member justus --task data/CTF/04-RSA/01-blue-hens-2023 --prompt-mode prompt-justus
```

Here is an example of using member justus for a sequential run:

```bash
python run_all_prompts.py justus data/CTF/04-RSA/01-blue-hens-2023
```

Note that these work for any existing CTF questions.

The model associated with member justus is o3-mini.

## Results Analysis of prompt-justus

Overall, prompt-justus had fairly little effect on program running. Compared to the original prompt run on the same model and device, the runtime when using prompt-justus was often noticeably longer. However, the iterations were mostly consistent with that of the original's, implying that the prompt was not significantly impacting outputs but indeed took up a notable amount of processing time.

Some very interesting exceptions exist, such as regularly using less iterations in successful runs of 01-prove-it and occassionally having shorter runtimes in tests done by deepseek-chat V3 and the claude thinking model. Personally, there are two datapoints I find exceptionally interesting:

When using deepseek-chat V3, the original prompt needed only roughly 4 minutes and 15 iterations to complete 01-integral-communication. However, despite the relatively minor adjustments, prompt-justus resulted in a failure. This means that it either hit the 20 minute limit we used for testing or decided to terminate early as a result of the manipulated inputs, which I think is worth noting.

When using o3-mini, 01-babycharge resulted in a non-failing result for prompt-justus and only prompt-justus. Of the data I collected with o3-mini, this is undoubtedly the most interesting, as this success is also the only successful run that o3-mini had on any non-RSA CTF question. Additionally, the associated iteration count (5) was among the lowest iteration results for the entire test. While this could be the result of random chance, it could also suggest that o3-mini is more adept at solving the problems in 03-Stream-PRNG-Hash when it is faced with hidden, malicious instructions.