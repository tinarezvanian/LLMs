# Deep-dive script — "Why every frontier lab is quietly betting against the transformer" (~11 min, ~1700 words)

> Hybrid: Tina on-camera intro + Manim core + on-camera outro + live SubQ Code demo.
> Pacing target: ~150 wpm.
> Markers: `[ON-CAM]`, `[ANIM: ...]`, `[SCREEN]`, `[B-ROLL]`.

---

## Scene 1 — Cold open (0:00 - 0:25)

[SCREEN: Terminal. Tina runs `subq-code load .` on a real ~400k-token codebase. Spinner. Progress bar. Done in seconds. She types a question that spans files.]
[B-ROLL: Cut to a competing tool — same prompt, OOM error, red text.]

VO (over SCREEN): "On the right, a frontier model from a well-known lab. On the left, a model that didn't exist a week ago. Same prompt. Same machine. One of them just read four hundred thousand tokens of code in seconds. The other one ran out of memory before it finished thinking."

---

## Scene 2 — On-camera hook (0:25 - 0:55)

[ON-CAM: Tina, eye-level, neutral background, lower-third with name and "Founding Developer Advocate, Subquadratic."]

"Hi, I'm Tina. Today I want to walk you through why every serious AI lab on Earth is quietly betting against the architecture they're famous for. We're going to start with the scaling laws that built modern AI, hit the wall those laws don't talk about, look at what the post-transformer research has been cooking for the last four years, and end with a live demo of what happens when somebody actually ships it."

---

## Scene 3 — Scaling laws (0:55 - 2:30)

[ANIM: Plot. Loss on y-axis (log), parameters on x-axis (log). Scattered training run dots appear one by one. A straight line slides through them.]

VO: "In 2020, OpenAI published a paper that quietly changed everything. They trained a few hundred language models at different sizes, plotted loss against parameters on a log-log scale, and found this. A straight line."

[ANIM: Highlight the line. Equation appears: L(N) = (N_c / N)^alpha, alpha ~ 0.076.]

VO: "Loss falls as a smooth power law in model size. Same shape for data. Same shape for compute. Architecture details, depth, width, head counts — they barely move this line. What moves it is *scale*."

[ANIM: Three lines side by side — N, D, C — all straight, all pointing down.]

VO: "This is the moment AI stopped being a research problem and became an engineering problem. If you have more money, you get a better model. Period. That's the whole pitch deck for every frontier lab from 2020 to today."

[ANIM: Pivot to Chinchilla. Isoflops surface — a 3D bowl. Camera tilts to show the valley.]

VO: "Two years later, DeepMind ran the experiment again with a wider sweep, and found the original recipe was off. For a fixed compute budget, parameters and tokens should grow together — about twenty tokens for every parameter. They built a 70-billion-parameter model on 1.4 trillion tokens that beat a 280-billion model on 300 billion tokens. Same compute, way better results. Every frontier model since 2022 — Llama, Mistral, every Chinchilla-pilled descendant — sits in this valley."

---

## Scene 4 — The pivot (2:30 - 3:00)

[ANIM: The straight line on log-log plot extends off the right side of the frame, fading into infinity.]

VO: "So the recipe is clear. More params, more tokens, more compute, lower loss. Forever. Right?"

[ANIM: A new axis appears at the bottom. Label: "context length (n)". The smooth scaling line curls up as `n` grows. Color shifts to red.]

VO: "Here's what scaling laws don't tell you. They assume you can actually use the model at the context length you want. And the moment you ask a transformer to read a long document, this happens."

---

## Scene 5 — Attention from scratch (3:00 - 4:15)

[ANIM: Three matrices materialize: Q, K, V — each labeled `[n x d]`. They float, rotate, label themselves.]

VO: "Quick refresher on how attention works. Every token in your input gets turned into three vectors. Query, Key, Value. There are `n` tokens, each vector is dimension `d`."

[ANIM: Q rotates. K transposes. They multiply. A new matrix appears between them, dimension `[n x n]`. Cells light up in a diagonal pattern.]

VO: "Then the queries dot-product with all the keys. That gives you this — an `n by n` matrix telling every token how much attention to pay to every other token. Softmax it, multiply by V, you get your output."

[ANIM: Highlight the `n x n` matrix. A counter spins up: n=10 (100 cells), n=100 (10,000), n=1000 (1,000,000), n=1,000,000 (1,000,000,000,000).]

VO: "Look at that middle matrix. Its size is `n` squared. Double the input length, you quadruple the work. At a million tokens, that matrix has a *trillion* entries. Per head. Per layer."

---

## Scene 6 — The wall (4:15 - 5:15)

[ANIM: A single H100 GPU outline appears, labeled "80 GB". A KV cache bar starts filling next to it.]

VO: "But the compute isn't even the worst of it. The real killer is memory. To do autoregressive generation, you have to *keep* the keys and values for every token you've already seen. That's the KV cache."

[ANIM: Math floats up: `2 * num_layers * num_heads * head_dim * n * sizeof(fp16)`. Concrete numbers fill in: 2 * 32 * 32 * 128 * n bytes ~ 524 KB per token.]

VO: "For a typical 7-billion-parameter model, the cache eats about half a megabyte per token. At one million tokens, you need five hundred and twenty-four gigabytes. The most expensive GPU you can buy has eighty."

[ANIM: KV cache bar massively overflows the H100 outline, spilling off-screen.]

VO: "This is the wall. Not the math, not the FLOPs — the memory."

---

## Scene 7 — FlashAttention defense (5:15 - 6:00)

[ANIM: A heroic-looking "FlashAttention" badge appears. The cache bar shrinks somewhat.]

VO: "Now, smart people have been chipping at this wall for years. The big one is FlashAttention — Tri Dao's work. The insight: attention isn't compute-bound on a modern GPU. It's I/O-bound. By tiling the computation in fast on-chip memory, you avoid materializing that full `n x n` matrix in main memory."

[ANIM: The original red parabola reappears. FlashAttention shifts it down by a constant factor, but the shape is unchanged. The asymptote stays.]

VO: "FlashAttention is brilliant. It buys you about an order of magnitude. But the asymptotic complexity is *still* `n` squared. Sliding window attention, multi-query attention, paged KV — they're all band-aids on the same wound. The patient survives. The disease is still there."

---

## Scene 8 — Post-transformer landscape (6:00 - 7:30)

[ANIM: A tree diagram grows from the bottom. Root: "subquadratic sequence models". Three branches: "state space models", "long convolutions", "linear attention". A fourth branch grows later: "hybrids".]

VO: "While everyone was chasing transformer scale, a parallel research thread was asking: what if we just don't do the `n x n` matrix at all?"

[ANIM: First branch. "State Space Models" lights up. A small dot slides along a 1D track, accumulating into a state vector that morphs as it goes.]

VO: "State space models — Mamba is the famous one — treat sequence modeling like a continuous-time linear dynamical system. There's a single hidden state that gets updated as each token arrives. No grid, no all-pairs comparison. Linear in `n`."

[ANIM: Second branch. "Long Convolutions" lights up. A long kernel sweeps across a signal.]

VO: "Hyena replaces attention with implicit long convolutions, computed in `n log n` via FFT. Hundred times faster than attention at sixty-four thousand tokens."

[ANIM: Third branch. "Linear attention" lights up with the kernel reformulation: phi(Q) phi(K)^T V.]

VO: "Linear attention rewrites softmax as a kernel feature map and reorders the matrix multiplications. The math goes from `n` squared `d` to `n d` squared. For long sequences, that's a giant win."

[ANIM: Fourth branch grows. "Hybrids — SAMBA, Jamba, Griffin." Two small icons interleave: SSM blocks and attention blocks.]

VO: "And the current frontier consensus, before SubQ, has been hybrids — interleave Mamba layers with a few attention layers, get the best of both. SAMBA, Jamba, Griffin. Real production systems."

---

## Scene 9 — Where SubQ fits (7:30 - 8:30)

[ANIM: A new branch grows on the tree, labeled "Subquadratic Sparse Attention (SubQ)". It sits between "linear attention" and "hybrids".]

VO: "Here is where Subquadratic — the company — fits. They launched five days ago. They call their architecture Subquadratic Sparse Attention. The internals are proprietary, so I can't show you the math. What I can show you is the *shape* of the claim."

[ANIM: Three benchmark callouts appear, sourced and dated.]

VO: "Linear scaling with context length. One million tokens in production, twelve million in research. Fifty-two times faster than FlashAttention at one million tokens. Ninety-five percent on the RULER 128K benchmark."

[ANIM: A small footnote: "Source: subq.ai/introducing-subq, May 5 2026. Independent verification pending."]

VO: "Now, those are SubQ's own numbers. Independent benchmarks are still coming. So instead of taking their word for it, let's just go run it."

---

## Scene 10 — Live demo (8:30 - 10:15)

[SCREEN: Tina opens the `subq-quickstart` repo (the one shipping with this video). She runs `subq-code load .` on a real codebase — let's pick something hairy, like a 300-file Python monorepo.]

VO (over SCREEN): "This is the starter repo I built to go with this video. It's on GitHub — link in the description. We're going to load my entire production codebase into context — about three hundred files, four hundred thousand tokens — and then ask it questions that no chunked retrieval system would get right."

[SCREEN: She asks: "Where do we set the API timeout, and is it consistent across all our HTTP clients?" The model answers correctly, naming files and line numbers across the repo.]

VO: "Cross-file. Cross-module. Without RAG. Without chunking. Without losing the thread."

[SCREEN: Second prompt: "Find every place we silently swallow an exception in this repo, and explain why each one is or isn't a bug." The model produces a structured list.]

VO: "This is the thing transformers couldn't do at this context length without spending a small fortune. SubQ does it on a single GPU."

[SCREEN: Tina runs the benchmark script in the repo — a small needle-in-a-haystack test at 500k tokens. Result prints: 96% accuracy.]

VO: "I also put together a small needle-in-a-haystack benchmark in the repo so you can verify the long-context retention claims yourself. Don't trust me. Don't trust them. Run it."

---

## Scene 11 — On-camera close (10:15 - 11:00)

[ON-CAM: Tina back on camera. Slightly warmer framing.]

"So that's the pitch. Scaling laws got us here. The transformer's `n` squared problem stopped us. The post-transformer research has been ready for a couple of years. Subquadratic is the first team to put a credible 1M-token model in front of developers and say 'go build.' Whether their numbers hold up under independent scrutiny is the most interesting question in AI infrastructure this year. And if they do, every developer building agents has a new tool that costs an order of magnitude less."

"Repo, blog post, and the math derivations are linked below. If you build something with SubQ, send it to me. I'd love to see it."

[ANIM: End card. Subscribe + repo link + Tina's handles. Hold 3s.]

---

## Production notes
- Voiceover separately recorded, synced in post (do not trust on-cam audio for VO)
- Manim renders at 1440p60, downscale at delivery
- On-cam: 4K24, 50mm equivalent, soft key + practical fill
- Aim for one full pass without breaks per shoot day
- 1080p H.264 master for YouTube; 4K H.265 archive
- Captions: Whisper-large transcribe, hand-correct LaTeX terms (alpha, sqrt, etc.)
- Music bed: -22 LUFS under VO, fade fully under demo screencast
