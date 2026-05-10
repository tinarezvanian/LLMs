# Research notes: scaling laws, the quadratic wall, and Subquadratic

> Source-of-truth for both videos. Every claim that ends up on screen must be traceable to a citation here. Numbers in `[brackets]` map to the citation list at the bottom.

---

## 1. Scaling laws — the empirical foundation

### 1.1 Kaplan et al. 2020 — "Scaling Laws for Neural Language Models" [1]

Headline finding: cross-entropy loss `L` of an autoregressive transformer follows smooth power laws in three resources, when each is the bottleneck:

- Model parameters `N` (non-embedding):  L(N) ~ (N_c / N)^alpha_N,  alpha_N ~ 0.076
- Dataset size `D` (tokens):              L(D) ~ (D_c / D)^alpha_D,  alpha_D ~ 0.095
- Compute `C` (PF-days):                  L(C) ~ (C_c / C)^alpha_C,  alpha_C ~ 0.050

Killer intuitions to animate:
- The loss curve is straight on a log-log plot. That straightness is the whole reason "scale up" is a strategy.
- Architecture details (depth, width, heads) matter ~10x less than total parameter count, within reasonable bounds.
- Kaplan recommended `N` should grow much faster than `D` for compute-optimal training. **This was wrong.** See Chinchilla.

### 1.2 Hoffmann et al. 2022 — "Training Compute-Optimal LLMs" (Chinchilla) [2]

DeepMind re-ran the analysis with broader sweeps and a different fit. Verdict: **for a fixed compute budget, parameters and tokens should scale ~equally**. The compute-optimal token-to-parameter ratio is roughly 20:1.

- Chinchilla 70B trained on 1.4T tokens beats Gopher 280B trained on 300B tokens, on the same compute.
- This rewrote the recipe for every frontier lab in 2022-2023 (Llama, Mistral, etc. are all "Chinchilla-pilled").

Killer animation: an isoflops surface — fix `C`, sweep `N` and `D`, find the valley. The valley sits along `D ~ 20 * N`.

### 1.3 What scaling laws assume that breaks at long context

Scaling laws say: more params + more data + more compute = lower loss. They are silent on **how much compute it costs to use a long context at inference time**. That cost is what makes "just train a 10M-context transformer" infeasible. Pivot point of the deep-dive video.

---

## 2. The quadratic wall

### 2.1 Vaswani et al. 2017 — "Attention Is All You Need" [3]

For a sequence of length `n` and head dim `d`:

- Q, K, V are each `[n, d]`
- Attention matrix `A = softmax(Q K^T / sqrt(d))` is `[n, n]`
- Compute: O(n^2 * d) per head, per layer
- Memory: O(n^2) for the attention matrix; O(n * d) for the KV cache per layer

For `n = 1,000,000`:
- Attention matrix has 10^12 entries per head per layer. At fp16, that's 2 TB per layer per head. Untenable.
- KV cache (assume 32 layers, 32 heads, head_dim 128, fp16) = 2 * 32 * 32 * 128 * n bytes = 524 KB per token = **524 GB at 1M tokens**. Single H100 has 80 GB.

Killer animation:
- Build the attention grid cell-by-cell, watch it grow as `n` doubles. Cell count quadruples each time.
- Translate compute to wall-clock dollars: at `n = 1M`, even one forward pass costs more than a small model's entire training run.

### 2.2 FlashAttention 1/2/3 [4]

Tri Dao's work: attention is **IO-bound**, not compute-bound, on modern GPUs. By tiling and recomputing in SRAM you avoid materializing the full `[n,n]` matrix in HBM.

- Compute cost is **still O(n^2)** — FlashAttention does not change asymptotics.
- It changes the constant by ~2-4x and dramatically reduces memory traffic.
- This is the strongest counterargument to "transformers are doomed at long context." The honest framing in the video: FlashAttention buys ~one order of magnitude of context. SubQ claims to buy ~three.

### 2.3 KV cache economics

At inference, the KV cache dominates memory at long context. Engineering responses:

- **Multi-query attention** (MQA), **Grouped-query attention** (GQA): share K/V across heads. Llama 2/3, Mistral.
- **Paged KV** (vLLM): treat KV as virtual memory, page in/out.
- **Sliding window attention**: only attend to last `w` tokens. Mistral.
- **YaRN, RoPE scaling**: positional encoding tricks for extrapolation.

All of these are **band-aids on an O(n^2) wound**. They keep the patient alive; they don't cure the disease.

---

## 3. The subquadratic landscape

### 3.1 State Space Models — Mamba [5]

Gu & Dao 2023. SSMs model sequences as continuous-time linear dynamical systems, discretized:

- h_t = A h_{t-1} + B x_t
- y_t = C h_t

Linear in `n`. The breakthrough in Mamba: **selective** SSMs — A, B, C become functions of the input, giving content-based reasoning that earlier SSMs (S4) lacked.

- Mamba-3B matches Transformers 2x its size on language modeling
- 5x throughput at long context
- Linear scaling to ~1M tokens demonstrated

Animation idea: a tiny rolling "memory state" carried through tokens, vs. attention's all-pairs grid. The state remembers what matters, forgets what doesn't.

### 3.2 Long convolutions — Hyena [6]

Poli et al. 2023. Replace attention with implicit long convolutions + data-controlled gating.

- O(n log n) via FFT
- Matches transformer quality on WikiText-103 and The Pile with 20% less compute at n=2k
- 100x faster than attention at n=64k

### 3.3 Linear attention family [7]

Katharopoulos et al. 2020 reformulated softmax attention as a kernel feature map and showed you can swap softmax for a feature map phi(.) and reorder the computation:

- Standard: softmax(QK^T) V  --> O(n^2 d)
- Linear: phi(Q) (phi(K)^T V) --> O(n d^2)

Trade-off: phi(.) is an approximation; quality typically lags softmax attention. Recent work (RetNet, GLA) closes the gap via gating.

### 3.4 Hybrids — SAMBA, Jamba, Griffin [8]

The frontier consensus circa 2024-2025: pure SSMs lose on in-context retrieval, pure transformers lose on context length. Hybrids interleave Mamba/SSM layers with a few attention layers (often sliding-window).

- SAMBA: Mamba + SWA, 3.8B params, extrapolates to 256K context
- Jamba (AI21): Mamba + MoE + attention
- Griffin (DeepMind): RG-LRU + local attention

### 3.5 Where SubQ fits on this map — Subquadratic Sparse Attention (SSA)

SubQ's launch-day technical post [13] is more specific than the marketing copy and gives us enough to teach the mechanism *family* honestly without claiming to know SubQ's secret sauce.

**The core mechanism, in SubQ's own words:**

> "Instead of computing every pairwise interaction, SSA uses content-dependent selection to route attention toward the positions that matter, regardless of where those positions appear in the sequence." [13]

**Three properties they claim hold together:**

1. **Linear scaling.** Compute and memory grow with the *number of selected positions* per query, not with `n`. (No big-O is stated explicitly; "linear" suggests the selected count is bounded or grows much slower than `n`.)
2. **Content-dependent routing.** The selection happens *after* seeing the query — meaning, not position. Contrast: sliding window decides where to look before knowing what it's looking for.
3. **Sparse retrieval from arbitrary positions.** Unlike recurrent / SSM approaches that compress the past into a fixed-capacity state, SSA preserves the ability to recover a specific token from arbitrarily far back.

**Crucially, it is not an approximation.** Per SubQ: "It does not approximate attention. It restricts attention to the positions that actually carry signal, and skips the rest." [13] The claim is "exact attention on a chosen subset of positions" — the proprietary part is *how* the subset is chosen.

**What's still unknown / unverified:**
- The selection algorithm (no learned-router architecture, no top-k vs threshold, no per-query / per-head / per-layer detail)
- Whether selection cost itself is included in the linear claim, or amortized away
- Independent reproduction of the wall-clock + benchmark numbers — the post says "third-party verified benchmarks" with a model card "coming soon" [13]; VentureBeat headline still flags the "researchers demand independent proof" angle [11]

### 3.6 Why this is hard — what every prior attempt at efficient attention gave up

This is the cleanest "why now / why nobody got here yet" beat in the deep-dive. SubQ's own technical post articulates the tradeoff space better than most published papers, and it tracks the literature [13]:

| Approach | Won | Gave up |
| -------- | --- | ------- |
| **Fixed-pattern sparse** (sliding window, strided, dilated — Longformer, BigBird, Mistral SWA) | Subquadratic compute by limiting *which* positions a token can attend to. | **Content-dependent routing.** The mask is decided in advance, by position. When the relevant token sits outside the pattern, the model literally cannot see it. |
| **State space / recurrent** (Mamba, RWKV, Hyena) | Linear scaling by construction; replaces all-pairs comparison with a state that evolves across the sequence. | **Exact retrieval from arbitrary positions.** The state has fixed capacity. As the sequence grows, information must be summarized, blurred, or discarded. Strong on gist, weak on "find the one fact 800K tokens ago." |
| **Hybrids** (SAMBA, Jamba, Griffin) | Real production systems by interleaving efficient layers with a few dense-attention layers. | **The scaling fix.** Dense layers remain load-bearing; quadratic cost still dominates as `n` grows. The benefit is a constant factor, not a complexity change. |
| **DeepSeek Sparse Attention** (2025) | Looks sparse from the outside — each query attends to a small subset of keys. | **The indexer is itself O(n²)** — it scores every query against every key (small constants, same scaling). The cost has been moved, not removed. [13] |

The pattern: **efficient + content-dependent + arbitrary-position retrieval has been the open problem.** Pick any two and a known architecture covers it; SubQ's claim is to be the first to credibly hit all three at production scale.

Animation idea (replaces the current "tree of post-transformer architectures" Manim scene): a **2×2 matrix** with axes *routing* (position-fixed → content-dependent) and *scaling* (quadratic → linear). Place each family in its quadrant. SSA is the bottom-right (content-dependent + linear) — empty quadrant before the SubQ launch, with a small Mamba/SSM marker also in the bottom-right but annotated with the lossy-state caveat. This gives the audience a single image to leave with.

---

## 4. SubQ — the company and the launch

### 4.1 Facts (May 5, 2026 launch)

- **Founders:** Justin Dangel (CEO), Alexander Whedon (CTO, formerly Head of Generative AI at Meta) [9, 10]
- **Funding:** $29M seed round, ~$500M valuation [10, 11]
- **Investors include:** Tinder co-founder Justin Mateen, ex-SoftBank Vision Fund partner Javier Villamizar, early backers of Anthropic, OpenAI, Stripe, Brex [11]
- **Headquarters:** Miami
- **Architecture:** Subquadratic Sparse Attention (SSA), proprietary
- **Model:** SubQ 1M-Preview
- **Context window:** 12M tokens (research), 1M tokens (production API)
- **Performance claims (with the more specific numbers from the SSA technical post [13]):**
  - **Wall-clock prefill speedup vs. FlashAttention-2 on B200 GPUs** [13]:

    | Context length | Speedup |
    | -------------- | ------- |
    | 128K | 7.2× |
    | 256K | 13.2× |
    | 512K | 23.0× |
    | 1M   | 52.2× |

    (Note SubQ's own footnote: "FlashAttention-3 did not produce a speedup on B200s over FlashAttention-2." So the comparison baseline is the fastest available standard attention on this hardware.)
  - **Attention FLOP reduction vs. standard attention** [13]: 8× at 128K → 62.5× at 1M.
  - 1000× reduction in attention compute at 12M tokens vs frontier models [9].
  - **RULER @ 128K: 95.0% (SubQ) vs 94.8% (Opus 4.6)** [13]. Multi-hop retrieval, aggregation, variable tracking, selective filtering. Genuinely competitive.
  - **MRCR v2 (multi-hop reasoning over fragmented evidence)** [13]:

    | Model | MRCR v2 |
    | ----- | ------- |
    | Opus 4.6 | 78.3% |
    | GPT 5.5 | 74.0% |
    | **SSA / SubQ** | **65.9%** |
    | GPT 5.4 | 36.6% |
    | Opus 4.7 | 32.2% |
    | Gemini 3.1 Pro | 26.3% |

    SubQ is **not the leader** here — they're behind two frontier models and ahead of three. **This is the honest framing for the deep-dive video**: SubQ is in the conversation with frontier dense-attention models on multi-hop reasoning, while running 52× faster at 1M tokens. The Opus 4.7 / Gemini 3.1 Pro scores show how brittle MRCR v2 is — strong models can fall over.
  - **SWE-Bench Verified: 81.8% (SSA / SubQ)** vs 80.6% (Gemini 3.1 Pro), 80.8% (Opus 4.6), 87.6% (Opus 4.7) [13].
- **Products in private beta:**
  - SubQ API — full-context access for developers
  - SubQ Code — CLI coding agent that loads entire codebases into context
  - SubQ Search — long-context research tool
- **Launch traction:** 12M+ views on X, 30,000+ waitlist signups in 24 hours [12]

### 4.2 The honest caveat

VentureBeat's headline (May 5, 2026) framed it as "Miami startup Subquadratic claims 1,000x AI efficiency gain... researchers demand independent proof" [11]. The architecture details are proprietary, and although the SSA post [13] says the published benchmarks are "third-party verified" with a comprehensive model card "coming soon," the field hasn't seen the full methodology yet. Trust calibration is still a work in progress.

**This is an asset for the video, not a liability.** A DevRel-quality video that:
1. Teaches the math so viewers can evaluate the claims themselves
2. Acknowledges what is and isn't independently verified — including beats where SubQ is *behind* a frontier model (MRCR v2, where Opus 4.6 and GPT 5.5 both score higher)
3. Runs Tina's own benchmarks in the GitHub starter repo

...is exactly the kind of trust-building content SubQ desperately needs right now. The major-lab playbook for this is hype + paper. SubQ's playbook (and Tina's) should be hype + math + reproducible code.

### 4.3 The "why now" pitch

Three things converged:
- Agents need 100k+ token contexts to be useful (whole codebases, long PDFs, video transcripts)
- Transformer KV cache makes that prohibitively expensive at scale
- Post-transformer research (Mamba, Hyena, RWKV) has matured enough that production systems are viable

SubQ is making the bet that the next wave of LLM applications will be context-bound, not parameter-bound. If they're right, every developer building agents is their customer.

---

## 5. Killer intuitions list (these become Manim scenes)

1. **The straight line on a log-log plot** — scaling laws made AI an engineering problem instead of a research problem
2. **The 20:1 valley** — Chinchilla isoflops surface
3. **The square that ate compute** — attention matrix growing as n^2
4. **524 GB on an 80 GB card** — the KV cache wall, made visceral
5. **FlashAttention is a band-aid** — the asymptote stays
6. **The rolling state vs. the all-pairs grid** — Mamba intuition in one image
7. **The post-transformer tree** — SSMs / convolutions / linear-attention / hybrids as branches
8. **Sparse + subquadratic = SubQ's bet** — positioned on the tree
9. **A whole codebase in context, in one prompt** — the developer payoff
10. **Loading subq-quickstart into SubQ Code, live** — the "I built with this" moment

---

## 6. Citations

1. Kaplan, J. et al. "Scaling Laws for Neural Language Models." arXiv:2001.08361 (2020).
2. Hoffmann, J. et al. "Training Compute-Optimal Large Language Models." arXiv:2203.15556 (2022). (Chinchilla)
3. Vaswani, A. et al. "Attention Is All You Need." NeurIPS 2017.
4. Dao, T. et al. "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness." NeurIPS 2022. FlashAttention-2 (2023), FlashAttention-3 (2024).
5. Gu, A. & Dao, T. "Mamba: Linear-Time Sequence Modeling with Selective State Spaces." arXiv:2312.00752 (2023). Mamba-2 (2024).
6. Poli, M. et al. "Hyena Hierarchy: Towards Larger Convolutional Language Models." ICML 2023.
7. Katharopoulos, A. et al. "Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention." ICML 2020.
8. SAMBA (Ren et al. 2024), Jamba (AI21 2024), Griffin (De et al. 2024).
9. Subquadratic. "Introducing SubQ — Efficiency is Intelligence." subq.ai/introducing-subq, May 5, 2026.
10. SiliconANGLE. "Subquadratic launches with $29M to bring 12M-token context windows to AI." May 5, 2026.
11. VentureBeat. "Miami startup Subquadratic claims 1,000x AI efficiency gain with SubQ model; researchers demand independent proof." May 5, 2026.
12. Refresh Miami. "Subquadratic raised $29M on the idea that it has cracked AI's biggest math problem." May 2026.
13. Subquadratic. "How SSA Makes Long Context Practical." subq.ai/how-ssa-makes-long-context-practical, May 5, 2026. Source for the SSA mechanism description, the prior-art tradeoff taxonomy (incl. the DeepSeek Sparse Attention indexer point), wall-clock B200 numbers (7.2× / 13.2× / 23.0× / 52.2× at 128K / 256K / 512K / 1M), the 8× → 62.5× attention-FLOP table, the RULER + MRCR v2 + SWE-Bench numbers, and the three-stage training pipeline (pretraining → SFT → RL targeting long-context retrieval and aggressive context use).
14. Independent third-party context: FelloAI, "SubQ Review: The First Subquadratic LLM with a 12 Million Token Context" (2026); LLMReference, "Using SubQ 1M-Preview on SubQ API — Setup, API, Pricing." Useful for sanity-checking that the SubQ claims are being reported consistently outside the company's own materials. Neither is an independent reproduction of the benchmarks.
