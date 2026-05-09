# Benchmarks

Reproducible long-context tests against [SubQ 1M-Preview](https://subq.ai). Run them yourself; results below are placeholders to fill in once API access is granted.

## Methodology

- **needle-in-a-haystack** — `python benchmarks/needle_in_haystack.py --tokens 500000 --trials 5`  
  Use `--dry-run` to verify haystack size without the `subq` package or `SUBQ_API_KEY`.
  - Synthetic English filler text padded to N tokens
  - Single-sentence "needle" (a unique passcode) inserted at depths {0.0, 0.25, 0.5, 0.75, 1.0}
  - Model is asked to retrieve the passcode
  - Accuracy reported per depth, averaged over 5 trials

- **codebase QA** — `python examples/codebase-qa/load_repo.py <repo>`
  - Manually graded against a held-out set of 20 questions per repo
  - Repos tested: this one, [django/django](https://github.com/django/django), [vllm-project/vllm](https://github.com/vllm-project/vllm)

## Results — needle-in-a-haystack

Pending API access. Results template:

| context tokens | depth 0.0 | depth 0.25 | depth 0.50 | depth 0.75 | depth 1.0 |
| -------------: | --------: | ---------: | ---------: | ---------: | --------: |
| 128,000        |        ?? |         ?? |         ?? |         ?? |        ?? |
| 500,000        |        ?? |         ?? |         ?? |         ?? |        ?? |
| 1,000,000      |        ?? |         ?? |         ?? |         ?? |        ?? |

SubQ's published number on RULER 128K is 95% [1]. The above table is intentionally not comparing to RULER directly — it's a simpler retrieval test you can verify locally without RULER's full dataset.

## Results — codebase QA

Pending API access. Will report:
- response correctness (graded 0/0.5/1 per question)
- response latency (p50, p95)
- cost per question (USD)

## Honest disclosures

- All numbers below ship as plain JSON in `results.json`. Independent verification welcome.
- Grading on the codebase QA benchmark is human-judged and therefore subjective. Where I'm uncertain I'll mark the answer 0.5 and explain.
- I do not work for SubQ at the time of writing. I'm a candidate for a developer advocacy role there. This benchmark exists because I think the right way to evaluate a launch is to run the code, not retweet the announcement.

## Sources

[1] Subquadratic, "Introducing SubQ — Efficiency is Intelligence," subq.ai/introducing-subq, May 5 2026.
