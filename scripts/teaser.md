# Teaser script — "The curve that's killing AI" (~75s, ~155 words)

> Pure Manim + voiceover. No on-camera. Square 1:1 cut for X / LinkedIn / Discord.
> Pacing target: 124 wpm — leaves breathing room for the visuals to land.

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
