# Teaser script — "The curve that's killing AI"

> Pure Manim + voiceover. No on-camera. **Short cut:** scenes 01–06 only (~75s, ~155 words) for X / LinkedIn / Discord. **Extended cut:** insert `scene_03b`–`scene_03g` between the KV wall and the break for ~5 minutes of teaching beats (aligned with `docs/scaling_attention/`).
> Pacing target (short cut): 124 wpm — leaves breathing room for the visuals to land.

---

**[0:00 - 0:08]  COLD OPEN**
[ANIM: A clean blue line rising linearly across the frame. Label: "what we wish AI cost".]

VO: "This is what we *wish* AI cost as it gets smarter."

**[0:08 - 0:18]  THE CURVE**
[ANIM: Line bends. Curls upward. Becomes a red parabola. The label morphs to: "what attention actually costs". A small "n^2" floats up.]

VO: "This is what it actually costs. Every transformer ever built lives on this curve. Doubling the context quadruples the compute."

**[0:18 - 0:32]  THE WALL**
[ANIM: A GPU memory bar fills as we step through 100k, 500k, 1M tokens. At 1M, "524 GB" lands hard. An H100 outline: 80 GB. The bar overflows the card.]

VO: "At one million tokens, the cache alone needs five hundred and twenty-four gigabytes. Top-of-the-line GPU: eighty."

**[0:32 - 0:48]  THE BREAK**
[ANIM: The red curve cracks. Falls away. A green linear line slides in to replace it. SubQ logo pulses in.]

VO: "Subquadratic just shipped a model that flips that curve. Linear scaling. One million tokens in production, twelve million in research. Fifty-two times faster than FlashAttention at one million tokens."

**[0:48 - 1:00]  THE PAYOFF**
[ANIM: Three icons cascade — a whole repo, a 500-page PDF, a multi-hour video transcript — all flowing into a single prompt window.]

VO: "Whole codebases. Whole books. Whole video archives. In one prompt."

**[1:00 - 1:15]  CTA**
[ANIM: SubQ wordmark, "Full breakdown ↓", handle/link, end card.]

VO: "I broke down the math, the architecture, and built the starter repo. Link below."

---

## Extended teaser (~5 min) — seven Manim beats after the KV wall

These scenes slot **between** `scene_03_wall` and `scene_04_break` (files `scene_03b` … `scene_03h`). They mirror the LaTeX primer (`docs/scaling_attention/`): tokens, the attention tile, scaling laws, Chinchilla, KV mitigations, the routing×scaling frame, then training vs inference. VO is optional for socials; for YouTube / teaching cuts, record over the longer concat (`make teaser && make concat`).

**[1:15 - 1:55]  TOKENS (`scene_03b_tokens`)**  
[ANIM: V and d callouts; per-token last-layer cost ∝ V·d; footnote that “1M context” is tokens.]  
VO (suggested): "Before attention even runs, tokens set the bill: a huge vocabulary times a wide hidden state hits you on every output step. And when a vendor says one million context, they mean tokens — not pages."

**[1:55 - 2:35]  ATTENTION TILE (`scene_03c_attention_tile`)**  
[ANIM: 10×10 causal grid; n² counter; heads×layers reminder.]  
VO: "Self-attention writes an n-by-n tile every layer. Causal models only need the lower triangle, but it is still order n squared per head — and you stack heads and layers."

**[2:35 - 3:15]  SCALING LAWS (`scene_03d_scaling_loglog`)**  
[ANIM: log–log scatter + line; L(N) ≈ (N_c/N)^α; bridge line that this does not remove the attention quadratic.]  
VO: "Kaplan-style scaling laws are why labs bet on bigger budgets: loss falls along a straight line on log–log axes. That is about parameters and data — not a free pass on attention cost."

**[3:15 - 3:55]  CHINCHILLA (`scene_03e_chinchilla_bite`)**  
[ANIM: D ≈ 20×N; three-line intuition; C ≈ 6·N·D rule-of-thumb.]  
VO: "Chinchilla said: if you fix compute, grow tokens and parameters together — about twenty tokens per parameter at the optimum. Training FLOPs still scale like N times D."

**[3:55 - 4:35]  KV BAND-AIDS (`scene_03f_kv_band_aids`)**  
[ANIM: MHA vs GQA vs MQA bar widths; FlashAttention caveat caption.]  
VO: "Grouped-query and multi-query attention shrink the KV cache by sharing keys and values across heads. FlashAttention is a memory trick for the score matrix — it does not change the big-O of the matmuls."

**[4:35 - 5:10]  QUADRANT (`scene_03g_landscape_quadrant`)**  
[ANIM: 2×2 routing × scaling frame; highlight bottom-right; honest footnote on benchmarks.]  
VO: "New architectures argue about two axes: fixed versus content-dependent routing, and quadratic versus linear work. Sparse attention lives in that map — treat vendor numbers as something to verify, not inherit."

**[5:10 - 5:45]  TWO BUDGETS (`scene_03h_wall_twice`)**  
[ANIM: Training column vs inference column; bridge line on n² at decode.]  
VO: "Training and serving are two different budgets. Chinchilla is about how many tokens to pair with parameters. Inference is about latency and how many gigabytes of key-value state you carry per request. Neither removes the quadratic attention tile when you decode long contexts."

Then pick up the original **THE BREAK** at `scene_04_break` (~5:45 onward in this extended layout).

---

## Production notes
- Music: low cinematic synth, fade out under VO at -22 LUFS
- Color: SubQ palette — deep navy bg, signal-green for "good" curves, signal-red for "bad" curves
- Captions burned in for social cuts (X / LinkedIn / Shorts / Reels / TikTok all autoplay muted); see [DESIGN.md §6](../DESIGN.md) for caption spec
- Three cuts (re-render with `config.frame_size`):
  - **16:9** (1920×1080) — YouTube short, LinkedIn, blog embed
  - **1:1** (1080×1080) — X feed, Instagram
  - **9:16** (1080×1920) — YouTube Shorts, Reels, TikTok. CTA text moves to upper third to survive platform overlays.
- End frame holds 2s for thumbnail grab
- ANIM cue at 0:08-0:18 says "n²" (Unicode); on-screen mobject also uses `Text("O(n²)")`, not `MathTex`, so the teaser renders without LaTeX
