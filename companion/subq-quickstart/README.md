# subq-quickstart

> Build a whole-codebase QA agent on [Subquadratic](https://subq.ai/introducing-subq) in 50 lines.
> Companion repo for the video [Why every frontier lab is quietly betting against the transformer](https://youtube.com/...) (link added when published).

SubQ shipped a 1M-token context model on May 5 2026 that scales linearly instead of quadratically. This repo is a few small examples that load a problem you couldn't fit into a transformer (a whole codebase, a 500-page book) and ask interesting questions across all of it. No RAG, no chunking.

## What's in here

- [`examples/codebase-qa/`](examples/codebase-qa) — load an entire repo into context and ask cross-file questions
- [`examples/long-doc-summarizer/`](examples/long-doc-summarizer) — load a 500-page PDF and produce structured summaries
- [`benchmarks/`](benchmarks) — a small needle-in-a-haystack script you can run yourself to verify the long-context retention claims

## Quick start

```bash
git clone https://github.com/tinarezvanian/subq-quickstart
cd subq-quickstart
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Optional: verify repo walking + haystack size without the SDK (no API key)
python examples/codebase-qa/load_repo.py /path/to/git/repo --dry-run
python benchmarks/needle_in_haystack.py --dry-run --tokens 500000

# get a SubQ API key from https://subq.ai
export SUBQ_API_KEY=sk-...

# load this repo into SubQ Code and start asking questions
python examples/codebase-qa/load_repo.py .
```

## Why this repo exists

SubQ's launch numbers are striking — 52x faster than FlashAttention at 1M tokens, 95% on RULER 128K — and they're SubQ-reported. The right response from the developer community isn't "trust them" or "ignore them," it's **run the benchmarks yourself**. This repo does that.

If you find the numbers don't hold up, open an issue. If you build something cooler with SubQ, send me a PR adding it to the examples. I'm tracking what people ship at [@tinarezvanian](https://twitter.com/tinarezvanian).

## Sources

- Subquadratic launch: https://subq.ai/introducing-subq
- SubQ API docs: https://docs.subq.ai
- Background reading: see [research/notes.md](../../research/notes.md) in the parent repo for primary-source notes on scaling laws, attention math, and the post-transformer landscape.

## License

MIT — see [LICENSE](LICENSE).
