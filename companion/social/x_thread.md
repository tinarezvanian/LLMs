# X thread — launch day

> 9 tweets. Tweet 1 has the teaser video embedded. Tweets 2-7 each have one Manim still attached for the algorithm. Tweet 8 has the deep-dive video. Tweet 9 is the CTA.
>
> Posted ~9am Pacific to catch SubQ team online + East Coast lunch.

---

**1/9**  [VIDEO: teaser_75s.mp4]

@subqai just shipped the first credible 1M-token model — and yeah, it's not a transformer.

Spent the last few days breaking down the math behind why this matters. 75-second teaser ↑

Full deep-dive at the end of this thread.

---

**2/9**  [IMG: 02_scaling_laws_kaplan.png]

Quick recap. In 2020 OpenAI showed that LLM loss falls as a smooth power law in scale. A straight line on a log-log plot.

That straight line is the entire pitch deck for every frontier lab from 2020 to today. AI became an engineering problem.

---

**3/9**  [IMG: 03_pivot_context_length.png]

In 2022 DeepMind corrected the recipe: parameters and tokens should scale together, not separately. ~20 tokens per parameter at compute-optimal.

Every Llama, every Mistral lives in this Chinchilla valley.

But notice what scaling laws are silent on: context length.

---

**4/9**  [IMG: 04_attention_grid.png]

Here's why context length is the silent killer.

Self-attention builds an n×n matrix. Double the input length, quadruple the compute. At n=1M, that's 10^12 cells per head per layer.

The compute isn't even the worst part.

---

**5/9**  [IMG: 05_kv_cache_overflow.png]

The KV cache. For a typical 7B model, ~524 KB per token.

At 1M tokens: 524 GB.

Top-of-the-line GPU: 80.

Sliding window, MQA, paged KV, FlashAttention — every "long context transformer" trick is a band-aid on this n² wound.

---

**6/9**  [IMG: 06_post_transformer_tree.png]

Meanwhile, a parallel research thread (Mamba, Hyena, RWKV, SAMBA) has been quietly cooking O(n) and O(n log n) alternatives for years.

The frontier labs know. Anthropic, DeepMind, Meta — they all have post-transformer R&D running. Nobody wanted to be first.

---

**7/9**  [IMG: 07_subq_benchmark_callouts.png]

@subqai is the first to ship.

Subquadratic Sparse Attention. 1M tokens production, 12M research. 52x faster than FlashAttention at 1M. 95% on RULER 128K.

Architecture is proprietary. Benchmarks are SubQ-reported. Independent verification: pending.

---

**8/9**  [VIDEO: deepdive_11min.mp4]

Full ~11 min deep-dive. Math from first principles, complete derivations, the whole post-transformer landscape, and a live demo of SubQ Code loading my entire production codebase into a single prompt.

@SubQ_AI @JustinDangel @AlexWhedon

---

**9/9**

I also built a small repo so you can verify the long-context retention claims yourself: github.com/tinarezvanian/subq-quickstart

If the numbers hold up, every agent builder has a new tool that costs an order of magnitude less.

If they don't — we'll find out together.

---

## Posting checklist
- [ ] From repo root: `make stills` then `bash scripts/export_x_thread_stills.sh` → PNGs in `assets/x_thread_stills/` (crop to **1080×1080** in Resolve or ffmpeg if needed)
- [ ] Compress teaser to <20MB for X video size limit
- [ ] Set deep-dive YouTube link in tweet 8
- [ ] Tag SubQ team handles only after confirming the right ones (placeholders above)
- [ ] Schedule for 9am PT
- [ ] Reply to first 30 quote-tweets within the first 4 hours
