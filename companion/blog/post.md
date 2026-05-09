---
title: "Why every frontier lab is quietly betting against the transformer"
subtitle: "A primer on scaling laws, the quadratic-attention wall, and what Subquadratic just shipped."
author: Tina Rezvanian
date: 2026-05-10
tags: [llm, transformers, scaling-laws, mamba, subquadratic, post-transformer]
---

> Companion to the video [Why every frontier lab is quietly betting against the transformer](https://youtube.com/...). Code that goes with it: [github.com/tinarezvanian/subq-quickstart](https://github.com/tinarezvanian/subq-quickstart).

Five days ago, a startup nobody had heard of came out of stealth with $29M, a $500M valuation, and a claim that they'd built a language model with 12 million tokens of context that runs 52x faster than FlashAttention at 1M tokens.[^1] Twitter went bananas. Researchers asked, reasonably, for independent proof.[^2]

This post is the math you need to evaluate the claim. We'll walk through:

1. What scaling laws actually say (and what they don't)
2. Why context length is the part scaling laws can't help you with
3. The quadratic-attention bottleneck, derived from scratch
4. What the post-transformer research has been quietly cooking
5. Where Subquadratic fits — and how to verify their numbers yourself

By the end you'll be able to read SubQ's launch post and know exactly what to believe and what to test.

## 1. Scaling laws

In January 2020, OpenAI published a paper that quietly changed every AI roadmap in the industry.[^3] They trained a few hundred language models at different sizes, plotted cross-entropy loss against parameter count on a log-log scale, and found this:

```
log(loss) = -alpha * log(params) + const
```

A straight line. Loss falls as a smooth power law in model size. The same shape held for dataset size and for compute. Model architecture details — depth, width, head count — barely move the curve. **Scale moves the curve.**

This was the moment AI became an engineering problem. If you had more money, you got a better model. The next four years of frontier-lab roadmaps fall out of that single insight.

Two years later, DeepMind ran the experiment again with a wider sweep and found the original recipe was off.[^4] For a fixed compute budget, parameters and tokens should scale **together** — about twenty tokens for every parameter. Their 70B-parameter Chinchilla model trained on 1.4T tokens beat Gopher 280B trained on 300B tokens, on the same compute. Every Llama, Mistral, and frontier descendant since 2022 sits in this Chinchilla-pilled valley.

Notice what's missing from the recipe: any mention of context length. Scaling laws assume you can train and run the model at the context length you want. That assumption breaks the moment you ask a transformer to read a long document.

## 2. The quadratic-attention bottleneck

Quick refresher. In a transformer, every token gets projected into three vectors — query Q, key K, value V — each of dimension `d`. With `n` tokens, those are `n x d` matrices. Self-attention computes:

```
A = softmax(Q K^T / sqrt(d))    # shape (n, n)
output = A V                     # shape (n, d)
```

The middle matrix `A` has `n^2` entries. Per head. Per layer. Compute is `O(n^2 * d)`. Memory is `O(n^2)`.

For `n = 1,000,000`, the attention matrix has 10^12 entries. At fp16, that's 2 TB **per head per layer**. Untenable.

Compute isn't even the worst of it. To do autoregressive generation you have to keep the keys and values for every token you've already seen — the **KV cache**. For a typical 7B model with 32 layers, 32 heads, and head dimension 128:

```
KV bytes per token = 2 layers * 32 heads * 128 d_head * 2 bytes
                   = 524,288 bytes ~= 524 KB
```

At one million tokens that's **524 GB**. The most expensive single GPU you can buy has 80.

This is the wall. Not the FLOPs — the memory.

## 3. What we've tried so far

Smart people have been chipping at this wall for years. The headline mitigations are:

- **FlashAttention** [^5] — Tri Dao's IO-aware attention algorithm. By tiling computation in fast on-chip SRAM you avoid materializing the full `n x n` matrix in main memory. **Compute is still O(n^2).** It's a smaller constant, not a different shape. Roughly an order-of-magnitude win.
- **Multi-query / grouped-query attention** — share K/V across heads. Llama 2/3, Mistral.
- **Sliding-window attention** — only attend to the last `w` tokens. Mistral.
- **Paged KV** — treat the cache as virtual memory. vLLM.

Every one of these is a band-aid on an `n^2` wound. The patient lives. The disease is still there.

## 4. The post-transformer research

While most of the field chased transformer scale, a parallel research thread asked the unfashionable question: **what if we just don't do the `n x n` matrix at all?**

### State Space Models

State space models treat sequence modeling as a discrete-time linear dynamical system:

```
h_t = A h_{t-1} + B x_t
y_t = C h_t
```

A single rolling hidden state, updated per token. Linear in `n`. The breakthrough work is **Mamba**, which makes A, B, C functions of the input — giving SSMs the content-based reasoning that earlier S4 variants lacked.[^6] Mamba-3B matches Transformers twice its size on language modeling and runs 5x faster at long context.

### Long convolutions

**Hyena** replaces attention with implicit long convolutions plus data-controlled gating, computed in `O(n log n)` via FFT.[^7] At sequence length 64K, Hyena runs 100x faster than attention.

### Linear attention

**Linear-attention** methods rewrite softmax attention as a kernel feature map:

```
softmax(Q K^T) V              -->  O(n^2 d)
phi(Q) (phi(K)^T V)           -->  O(n d^2)     # reorder the matrix multiplications
```

Trade-off: phi(.) is an approximation; quality lags softmax. Recent work (RetNet, GLA) closes the gap with gating.

### Hybrids

The frontier consensus before this week has been **hybrids**. Pure SSMs lose on in-context retrieval; pure transformers lose on context length. **SAMBA**, **Jamba**, and **Griffin** interleave Mamba layers with a few attention layers and get the best of both.[^8]

## 5. Where Subquadratic fits

SubQ calls their architecture **Subquadratic Sparse Attention** (SSA). The internals are proprietary. From the launch material we know:

- It scales linearly with context length
- 1M tokens in production, 12M in research
- 52x faster than FlashAttention at 1M tokens
- 95% accuracy on RULER 128K
- 1000x reduction in attention compute at 12M tokens vs frontier models

The "sparse" qualifier strongly suggests it sits closer to the attention family than to pure SSMs — likely a learned sparsity pattern that brings compute down to `O(n)` or `O(n log n)` while retaining the precision benefits of attention. But this is inference; SubQ hasn't published a paper.

**That's why I built [subq-quickstart](https://github.com/tinarezvanian/subq-quickstart).** It contains a small needle-in-a-haystack benchmark you can run yourself at any context length you want, plus reference implementations of the two applications I think showcase long-context the best:

- A whole-codebase QA agent (`examples/codebase-qa/`)
- A book-length PDF summarizer (`examples/long-doc-summarizer/`)

If SubQ's numbers hold up under independent scrutiny, every developer building agents has a new tool that costs an order of magnitude less. If they don't, we'll find out together.

Either way, the math is the math. The transformer hit the wall. Whoever ships the first credible post-transformer model into production has a real chance at rewriting how the next wave of LLM applications gets built.

---

[^1]: SiliconANGLE, "Subquadratic launches with $29M to bring 12M-token context windows to AI," May 5 2026.
[^2]: VentureBeat, "Miami startup Subquadratic claims 1,000x AI efficiency gain... researchers demand independent proof," May 5 2026.
[^3]: Kaplan, J. et al. "Scaling Laws for Neural Language Models." arXiv:2001.08361 (2020).
[^4]: Hoffmann, J. et al. "Training Compute-Optimal Large Language Models." arXiv:2203.15556 (2022).
[^5]: Dao, T. et al. "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness." NeurIPS 2022.
[^6]: Gu, A. & Dao, T. "Mamba: Linear-Time Sequence Modeling with Selective State Spaces." arXiv:2312.00752 (2023).
[^7]: Poli, M. et al. "Hyena Hierarchy: Towards Larger Convolutional Language Models." ICML 2023.
[^8]: Ren et al. (SAMBA), AI21 Labs (Jamba), De et al. (Griffin), 2024.
