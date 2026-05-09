# DESIGN.md

Visual identity, narrative principles, and editorial rules for the SubQ video package. Read before changing anything that affects what the audience sees or hears.

## 1. Visual identity

### Palette (defined in [vid/theme.py](vid/theme.py))

| token       | hex       | use                                          |
| ----------- | --------- | -------------------------------------------- |
| SUBQ_BG     | `#0B1020` | scene background (deep navy)                 |
| SUBQ_FG     | `#E8ECF7` | primary text                                 |
| SUBQ_MUTED  | `#7A8299` | captions, axis labels, footnotes             |
| SUBQ_GREEN  | `#3DDC97` | "good" — linear scaling, SubQ, what works    |
| SUBQ_RED    | `#FF5A5F` | "bad" — quadratic curves, walls, OOM         |
| SUBQ_BLUE   | `#5C9EFF` | neutral structures (matrices, axes)          |
| SUBQ_YELLOW | `#F5C451` | accents, highlighted equations               |
| SUBQ_PURPLE | `#A77BFF` | secondary accent (rare)                      |

The semantic meaning matters: green = the thing we're rooting for, red = the wall. Don't break that contract by using green for "old transformers".

### Typography

Two families, both shipped in-repo at [`assets/branding/fonts/`](assets/branding/fonts) (SIL OFL). Registered with Pango on import via `vid/theme.py::_activate_repo_fonts()` so renders work on a fresh checkout with no system font install.

| family             | use                                                       | source             |
| ------------------ | --------------------------------------------------------- | ------------------ |
| **Inter**          | body, captions, footnotes, branch labels                  | rsms/inter v4      |
| **Inter Display**  | titles, headings, SubQ wordmark                            | rsms/inter v4      |
| **JetBrains Mono** | equations (`text_equation()`), code, KV / GPU labels, n²   | jb/JetBrainsMono v2.304 |

Sizes pinned in `theme.py`:

- Title: 56pt (Inter Display Bold)
- Heading: 40pt (Inter Display Bold)
- Body: 32pt (Inter Regular)
- Caption: 24pt (Inter Regular muted)
- Equation: 44pt (JetBrains Mono Bold via `text_equation`; or `MathTex` if LaTeX is installed)
- Mono / code: 32pt (JetBrains Mono Regular via `mono()` helper)
- Footnote: 18pt italic muted (Inter Italic)

**Why these two:** Inter has tabular numerals and excellent screen rendering at every weight (used by Vercel, Notion, Linear); JetBrains Mono ligatures + slashed zero make `O(n²)`, `1M`, `H100  80 GB` read unambiguously on a phone. Both ship as SIL OFL so we can redistribute the TTFs without per-machine installs.

**Don't** call `Text("foo")` without specifying `font=` — you'll get system sans and the type will pop visibly inconsistent against scenes that use the helpers. Use `body()` / `caption()` / `mono()` / `text_equation()` / `title()` / `heading()` from `vid/theme.py`.

### Pacing constants

- `PACE_FAST = 0.4s` — a punctuation beat
- `PACE_NORMAL = 0.8s` — most transitions
- `PACE_SLOW = 1.5s` — let an idea land
- `PACE_BEAT = 0.6s` — between sentences

Use these instead of inline `run_time=0.5` magic numbers. Adjust globally in `theme.py`.

## 2. Narrative principles (3Blue1Brown-derived)

These are non-negotiable. They're the difference between an explainer that feels educational and one that feels like a sales pitch.

1. **One idea per scene.** If you can't summarize the scene in one sentence, split it.
2. **Animation carries the logic.** If you read an equation aloud without the visual already on screen, the audience tunes out. The visual leads, the voiceover supports.
3. **Earn every claim.** "52x faster" requires the next frame to show the source. No exceptions.
4. **Concrete before abstract.** "524 GB on an 80 GB card" beats "memory-constrained at long context."
5. **Show the math; don't intimidate with it.** Equations are characters. Build them up symbol by symbol when introduced. Color the variable you're talking about.
6. **Honest framing.** Every benchmark we cite is sourced. Every SubQ-internal number is footnoted as "SubQ-reported, independent verification pending."

## 3. The two-part structure

The teaser and the deep-dive serve different jobs. Don't blur them.

### Teaser (~75s)
- **Job:** social-feed magnet. Stops the scroll, communicates the core idea, links to depth.
- **Format:** pure Manim + voiceover. No on-camera.
- **Cuts:** **16:9** (1920×1080) for YouTube/LinkedIn/blog embed, **1:1** (1080×1080) for X feed and Instagram, **9:16** (1080×1920) for YouTube Shorts / Reels / TikTok. All three are mastered from the same scene source by re-rendering with `config.frame_size`; see "Safe areas" below.
- **Content:** the wall (n²) → the break (linear). Everything else is cut.
- **Distribution:** X tweet 1 (1:1), LinkedIn (16:9), Discord (16:9), blog embed (16:9), Shorts/Reels/TikTok (9:16).

### Deep-dive (~10-12 min)
- **Job:** trust + depth. Convinces engineers Tina knows what she's talking about and SubQ is worth their time.
- **Format:** hybrid. On-camera intro/outro + Manim core (~7 min) + live SubQ Code demo screen capture (~2 min).
- **Content:** scaling laws → quadratic wall → post-transformer landscape → where SubQ fits → live demo → what this unlocks for builders.
- **Distribution:** YouTube primary, LinkedIn embed, blog embed, last tweet of the X thread.

## 4. Why a hybrid format for the deep-dive

The job description leans heavily on **on-camera presence**. A pure-Manim deep-dive doesn't show whether Tina can hold a frame. A pure on-camera deep-dive doesn't show technical animation chops. The hybrid demonstrates both in one piece, which is the actual job.

Camera segments stay short (intro ~30s, outro ~45s, plus brief whiteboard cut-aways). Manim carries the explanatory weight. The live demo at the end is the "I built with this" proof point that the JD's nice-to-haves explicitly call out.

## 5. Why the companion repo

The JD says: "build reference applications, demos, and GitHub starter repositories that show developers how to build real-world applications using SubQ's LLM platform." A video alone doesn't prove that capability. `companion/subq-quickstart/` is a working artifact:

- A whole-codebase QA agent (~50 lines)
- A long-doc summarizer
- A reproducible needle-in-a-haystack benchmark you can run yourself

The `BENCHMARKS.md` template ships with intentionally empty result tables — the act of filling them in honestly is itself a content moment ("here are SubQ's claims, here are the numbers I measured, here's the gap").

## 6. Captions

Burned-in captions are required on every social cut (X, LinkedIn, Shorts, Reels, TikTok all autoplay muted). YouTube uses uploaded `.srt` instead of burn-in.

- **Source:** Whisper-large transcribe → hand-correct technical terms (alpha, sqrt, n², FlashAttention, RULER, SSA).
- **Font:** SF Pro / Inter / system sans, weight 600.
- **Size:** 36pt for 1080p; 1:1 and 9:16 cuts use the same font size on a smaller canvas, so lines stay short.
- **Color:** `#FFFFFF` on a 75%-opacity `#0B1020` rounded pill. Never on raw video — readability over aesthetics.
- **Position:** lower third for 16:9; vertical center-low for 1:1; upper third for 9:16 (so it survives the platform-overlaid like/comment buttons at the bottom).
- **Line length:** ≤ 32 chars per line, ≤ 2 lines on screen at once.
- **Timing:** appear 80ms before the matching word; hold 200ms after the phrase ends.

## 7. Safe areas (per aspect ratio)

Critical text and the SubQ wordmark must sit inside the safe area for every cut, otherwise platform overlays or center-cropping will eat them.

| ratio | canvas        | safe area (centered)         | platform overlay risk |
| ----- | ------------- | ---------------------------- | --------------------- |
| 16:9  | 1920 × 1080   | 1728 × 972  (90% × 90%)      | YouTube progress bar bottom 6% |
| 1:1   | 1080 × 1080   | 972 × 972   (90% × 90%)      | Instagram username top, like button right |
| 9:16  | 1080 × 1920   | 864 × 1536  (80% × 80%)      | TikTok/Shorts: bottom 25% (caption + buttons), right 12% (action rail) |

In Manim, set `config.frame_size = (W, H)` per render pass and keep all CTA mobjects within the safe rectangle. Test by exporting a frame and overlaying the platform's UI screenshot before publishing.

## 8. Editorial rules for any text we ship

- **Engineers, not marketing.** Active voice, concrete nouns, numbers with units.
- **No buzzwords.** Forbidden in **Tina's own copy**: "leverage", "unlock", "supercharge", "revolutionary", "AI-powered", "next-generation", "game-changing", "groundbreaking". Verbatim quotes from SubQ's launch material or the JD are exempt — but flag them as quotes when used.
- **Cite or don't claim.** Numbers without sources don't ship.
- **Hedge appropriately.** SubQ's claims are SubQ-reported until verified. Say so when stating them. The audience trusts you more for hedging than for amplifying.
- **Short paragraphs.** Three sentences max in any blog or script paragraph.

## 9. Distribution rhythm

Day 4: teaser ships to X first (catch SubQ team and their followers in the launch wave). Embed in LinkedIn same day.

Day 10: deep-dive ships to YouTube. Same day, blog post goes live linking both videos. Same day, X thread goes out (teaser embedded in tweet 1, deep-dive embedded in tweet 8). Cover letter to SubQ goes out within 24 hours.

The teaser and deep-dive are deliberately spaced ~6 days apart. The teaser builds anticipation; the deep-dive resolves it. Posting both at once flattens the engagement curve.
