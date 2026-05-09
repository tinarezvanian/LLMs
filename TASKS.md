# TASKS.md

> Live actionable backlog. The plan in `.cursor/plans/` is the strategy; this file is the next physical step. Update statuses as you finish things.

Conventions:
- `[x]` complete  ·  `[~]` in progress  ·  `[ ]` pending  ·  `[!]` blocked
- Each task lists **acceptance criteria** so you know when you're done

---

## Phase 1 — Research

- [x] **Research notes drafted** → [research/notes.md](research/notes.md)
  - Acceptance: Kaplan + Chinchilla + Vaswani + FlashAttention + Mamba + Hyena + linear attention + hybrids + SubQ launch facts, all with numbered citations.

- [ ] **Read the actual papers, not just summaries**
  - Files: Kaplan 2020, Chinchilla 2022, Vaswani 2017, FlashAttention 1/2/3, Mamba (Gu & Dao), Hyena (Poli)
  - Acceptance: Tina can reproduce the key equations on a whiteboard from memory. Used in the on-cam segments and in any Q&A on the application call.

## Phase 2 — Scripts

- [x] **Teaser script** → [scripts/teaser.md](scripts/teaser.md)
  - Acceptance: ~155 words, every line has an `[ANIM:]` cue, total VO time at 124 wpm fits 60-90s.

- [x] **Deep-dive script** → [scripts/deepdive.md](scripts/deepdive.md)
  - Acceptance: ~1700 words, `[ON-CAM]` / `[ANIM:]` / `[SCREEN]` markers throughout, total time at 150 wpm fits 10-12 min.

- [ ] **Scratch VO recording**
  - Record both scripts on phone or AirPods. Listen at 1x and 1.5x. Cut anything that drags. Update scripts.
  - Acceptance: scratch tracks land in `audio/scratch/{teaser,deepdive}.m4a`. Scripts reflect the cut.

## Phase 3 — Production tooling

- [x] **Repo scaffolded** → vid/, scripts/, research/, companion/, audio/, video/, demo/, edit/
- [x] **Theme + reusable mobjects** → [vid/theme.py](vid/theme.py), [vid/lib/mobjects.py](vid/lib/mobjects.py)
- [x] **Makefile + environment.yml**
- [x] **ffmpeg (static binary)** → bin/ffmpeg
- [x] **micromamba (static binary)** → bin/micromamba

- [x] **Manim env install** → lean solve: `micromamba create -y -n subq -c conda-forge python=3.12 manim ffmpeg` (see [Makefile](Makefile) `setup` target). **Do not** put `manim-voiceover` in the same conda solve (hangs 20+ min).
  - Acceptance: `make check` prints a manim version string and an ffmpeg version string with no errors.

- [x] **Teaser smoke render**
  - Ran: `QUALITY=-ql make teaser` — all 6 scenes produce final MP4s under `edit/renders/teaser/videos/*/480p15/*.mp4` (gitignored).
  - Scene 02 uses `Text("O(n²)")` instead of `MathTex` so teaser does not require a full LaTeX `preview` package. Deep-dive scenes still need LaTeX for `equation()` — see [README.md](README.md#troubleshooting).

## Phase 4 — Animation

### Teaser (6 scenes)
First-pass animations rendered (`QUALITY=-ql`). Polish pass still needed for production (`-qh` / `-qk`).

- [~] [scene_01_open](vid/scenes/teaser/scene_01_open.py) — linear curve fade-in. Polish: micro-easing on the curve creation.
- [~] [scene_02_curve](vid/scenes/teaser/scene_02_curve.py) — linear morphs to quadratic; `O(n²)` label is `Text` (no LaTeX). Polish: stronger anticipation before the bend.
- [~] [scene_03_wall](vid/scenes/teaser/scene_03_wall.py) — KV bar fills 100k → 500k → 1M, overflows H100. Polish: numbers count up rather than snap.
- [~] [scene_04_break](vid/scenes/teaser/scene_04_break.py) — red curve cracks, green linear replaces. Polish: literal "crack" particle effect on the break frame.
- [~] [scene_05_payoff](vid/scenes/teaser/scene_05_payoff.py) — repo + PDF + video flow into single prompt. Polish: better icon glyphs.
- [~] [scene_06_cta](vid/scenes/teaser/scene_06_cta.py) — wordmark, "Full breakdown ↓", handle. Polish: subscribe shimmer.

### Deep-dive (14 scenes)
12 Manim scenes + 2 placeholders for camera/screen footage.

- [~] [scene_01_cold_open](vid/scenes/deepdive/scene_01_cold_open.py) — title card after the screen-capture intro
- [ ] scene_02 — on-camera footage (no Manim, marked `SKIP_RENDER`)
- [~] [scene_03_scaling_laws](vid/scenes/deepdive/scene_03_scaling_laws.py) — Kaplan power-law plot + Chinchilla mention
- [~] [scene_04_pivot](vid/scenes/deepdive/scene_04_pivot.py) — good vs bad axes, the pivot to context length
- [~] [scene_05_attention](vid/scenes/deepdive/scene_05_attention.py) — Q/K/V → n×n grid → O(n²d)
- [~] [scene_06_kv_wall](vid/scenes/deepdive/scene_06_kv_wall.py) — KV cache equation + 524 GB > 80 GB
- [~] [scene_07_flashattention](vid/scenes/deepdive/scene_07_flashattention.py) — FlashAttention helps but asymptote stays
- [~] [scene_08_landscape](vid/scenes/deepdive/scene_08_landscape.py) — post-transformer tree
- [~] [scene_09_mamba](vid/scenes/deepdive/scene_09_mamba.py) — rolling state intuition
- [~] [scene_10_subq_position](vid/scenes/deepdive/scene_10_subq_position.py) — SubQ branch on the tree
- [~] [scene_11_benchmarks](vid/scenes/deepdive/scene_11_benchmarks.py) — sourced benchmark callouts
- [~] [scene_12_demo_intro](vid/scenes/deepdive/scene_12_demo_intro.py) — title card before the screen demo
- [ ] scene_13 — SubQ Code screen capture (no Manim, marked `SKIP_RENDER`)
- [~] [scene_14_close](vid/scenes/deepdive/scene_14_close.py) — end card

For each `[~]` scene:
- Acceptance: scene renders at `-qh` in under 30s, looks readable on a 1080p phone screen, animation feels intentional (no jank), color contract from [DESIGN.md](DESIGN.md) is respected.

## Phase 5 — Shoot day

- [ ] **Apply for SubQ beta access** (do this immediately — gating factor for the demo)
- [ ] **Camera setup**: 4K24, 50mm equiv, single key + window fill, lavalier mic. Soft eye-level frame, neutral background.
- [ ] **On-camera takes**: intro (~30s), outro (~45s), 2-3 whiteboard cut-aways. Multiple takes per setup.
- [ ] **VO recording**: full deep-dive script in a closet with blankets. Match scratch pacing.
- [ ] **SubQ Code demo capture**: OBS, 1440p, repo loaded, 3 takes minimum, hide secrets.
  - Acceptance: usable footage lands in `video/`, `audio/final/deepdive_vo.wav`, and `demo/subq_code_session.mov`.

## Phase 6 — Edit + ship

- [ ] **DaVinci assembly**: VO timeline first, drop Manim renders to picture, sync on-camera segments
- [ ] **Color**: subtle warm grade on on-cam, leave Manim untouched
- [ ] **Sound mix**: -18 LUFS dialog, -22 LUFS music bed, duck under VO
- [ ] **Captions**: Whisper-large auto-transcribe, hand-correct LaTeX terms (alpha, sqrt, n^2 etc.)
- [ ] **Render formats** (final masters; see [DESIGN.md §3, §7](DESIGN.md) for full spec):
  - 4K H.265 archive master (16:9, deep-dive only)
  - 1080p H.264 distribution copy (16:9, YouTube primary)
  - 1080×1080 square cut of the teaser (X / Instagram)
  - 1080×1920 vertical cut of the teaser (Shorts / Reels / TikTok) — CTA text in upper third, see safe-area table

## Phase 7 — Companion deliverables

- [x] [companion/subq-quickstart/README.md](companion/subq-quickstart/README.md)
- [x] [companion/subq-quickstart/examples/codebase-qa/load_repo.py](companion/subq-quickstart/examples/codebase-qa/load_repo.py)
- [x] [companion/subq-quickstart/examples/long-doc-summarizer/summarize_pdf.py](companion/subq-quickstart/examples/long-doc-summarizer/summarize_pdf.py)
- [x] [companion/subq-quickstart/benchmarks/needle_in_haystack.py](companion/subq-quickstart/benchmarks/needle_in_haystack.py)
- [x] [companion/subq-quickstart/BENCHMARKS.md](companion/subq-quickstart/BENCHMARKS.md) (template)
- [x] [companion/blog/post.md](companion/blog/post.md)
- [x] [companion/social/x_thread.md](companion/social/x_thread.md)
- [x] [companion/cover_letter.md](companion/cover_letter.md)

- [ ] **Run the actual benchmarks** once SubQ access is granted; fill in BENCHMARKS.md
- [ ] **Push subq-quickstart to its own GitHub repo** under tinarezvanian/subq-quickstart
- [ ] **Render Manim still frames** for the X thread (one per tweet 2-7)
- [ ] **Schedule X thread** for ~9am PT with both videos linked

## Phase 8 — Submit

- [ ] **Personal branding double-check**: handles in scripts/social are still the placeholder `tinarezvanian` — confirm or update before publishing
- [ ] **Submit application** with cover letter + links

---

## Reconcile duplicate scene files — DONE 2026-05-09

Three deep-dive scenes had two implementations on disk. Reconciled as follows:

- `scene_04_chinchilla.py` → **deleted.** Chinchilla content stays as a verbal beat inside [scene_03_scaling_laws](vid/scenes/deepdive/scene_03_scaling_laws.py). Plan also lists Chinchilla as the first cut candidate.
- `scene_05_attention_grid.py` → **deleted.** Its `softmax(QK^T/sqrt(d))V` equation was folded into the canonical [scene_05_attention.py](vid/scenes/deepdive/scene_05_attention.py).
- `scene_07_flash_attention.py` → **deleted.** Its three-curve comparison (attn / FlashAttn / linear) replaced the simpler version in [scene_07_flashattention.py](vid/scenes/deepdive/scene_07_flashattention.py).

## Things that are nice-to-have but cuttable if time runs out

These are flagged in the plan as candidates to drop first if the sprint slips:

- Deep-dive scene 9 (Mamba intuition) — the post-transformer tree in scene 8 already conveys the landscape; the rolling-state animation is icing
- Deep-dive scene 4 (Chinchilla isoflops) — scene 3 already lands the scaling-laws beat; Chinchilla can be a verbal mention
- Whiteboard B-roll on shoot day — Manim covers the math, on-cam already has intro/outro
- Vertical 9:16 cut of the teaser — 1:1 covers most platforms; vertical can ship as a follow-up

## Done definition (for the whole sprint)

The sprint is done when **all of the following** are public:
- [ ] Teaser uploaded to YouTube and embedded in tweet 1 of the X thread
- [ ] Deep-dive uploaded to YouTube
- [ ] Companion blog post live on tinarezvanian.com (or Substack)
- [ ] X thread posted
- [ ] subq-quickstart repo public on GitHub with at least one filled-in BENCHMARKS row
- [ ] Application submitted to SubQ with cover letter linking everything above
