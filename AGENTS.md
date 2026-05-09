# AGENTS.md

> Handoff doc for any LLM agent (or human) picking up this repo cold. Read this **before** writing code or running commands.

## Mission

Ship a two-part video portfolio for Tina Rezvanian's application to **Subquadratic (SubQ)** — a Founding Developer Advocate role they posted shortly after launching publicly on **May 5 2026** with $29M in seed funding and a 1M-token-context post-transformer model called SubQ 1M-Preview.

The deliverables are:

1. **Teaser** — ~75 second pure-Manim explainer of the quadratic-attention wall and why SubQ matters. Optimized for X / LinkedIn / Discord. Renders from `vid/scenes/teaser/`.
2. **Deep-dive** — ~10-12 minute hybrid (Manim + on-camera + live SubQ Code demo) walking through scaling laws, the post-transformer landscape, and where SubQ fits. Renders from `vid/scenes/deepdive/`.
3. **Companion package** — GitHub starter repo, blog post, X thread, cover letter. Lives under `companion/`.

The full sprint plan is at [`.cursor/plans/subq_manim_demo_video_a7a5729c.plan.md`](.cursor/plans/subq_manim_demo_video_a7a5729c.plan.md). The live backlog is at [`TASKS.md`](TASKS.md). Visual + narrative principles are in [`DESIGN.md`](DESIGN.md).

## File map (what lives where)

```
.cursor/plans/                 sprint plan (markdown, frontmatter has todos[])
research/notes.md              primary-source notes; every claim in the videos traces back here
scripts/teaser.md              ~155-word teaser script with [ANIM] cues
scripts/deepdive.md            ~1700-word deep-dive script with [ANIM]/[ON-CAM]/[SCREEN] cues
vid/                           Manim Python package (NOTE: directory is `vid/` to avoid clashing with the `manim` PyPI package)
  theme.py                     palette, type sizes, pacing constants
  lib/mobjects.py              reusable mobjects (AttentionGrid, GPUOutline, KVCacheBar, ScalingCurve, PostTransformerTree, SubQWordmark)
  scenes/teaser/scene_0N_*.py  6 teaser scenes, one Manim Scene class per file
  scenes/deepdive/scene_0N_*.py 14 deep-dive scenes (some are placeholders with SKIP_RENDER = True for camera/screen segments)
companion/
  subq-quickstart/             standalone GitHub starter repo to publish separately
    README.md                  "Build a whole-codebase QA agent on SubQ in 50 lines"
    examples/codebase-qa/      load entire repo into context, ask cross-file questions
    examples/long-doc-summarizer/  load 500-page PDF into context
    benchmarks/needle_in_haystack.py   reproducible long-context test
    BENCHMARKS.md              methodology + results template
  blog/post.md                 written companion to the deep-dive (MDX-ready)
  social/x_thread.md           9-tweet launch thread
  cover_letter.md              cover note for the SubQ application
audio/  video/  demo/  edit/   gitignored: VO recordings, on-cam footage, screen capture, DaVinci project
bin/                           project-local binaries (ffmpeg, micromamba); large files gitignored
.venv/  .micromamba/           gitignored Python toolchains
Makefile                       `make setup` / `make teaser` / `make deepdive` / `make all`
environment.yml                conda-forge env spec (canonical install path)
```

## Setup (clean machine, macOS)

```bash
# 1) ffmpeg (static binary, no Homebrew dependency)
mkdir -p bin && curl -L -o bin/ffmpeg.zip "https://evermeet.cx/ffmpeg/getrelease/zip" \
  && (cd bin && unzip -o ffmpeg.zip && rm ffmpeg.zip)

# 2) micromamba (static binary, no system install)
curl -Ls https://micro.mamba.pm/api/micromamba/osx-64/latest | tar -xvj bin/micromamba

# 3) conda env (NOTE: see "Gotchas" below — install just `manim` first, then `pip install manim-voiceover`)
make setup
make check
```

`make check` should print a manim version and an ffmpeg version. If it does, `make teaser` will render all 6 teaser scenes to `edit/renders/teaser/`.

## Decisions and rationale

These were deliberate calls, not coincidences. Reverse them only if you have a strong reason.

### 1. Manim Community (`manim` on PyPI / conda-forge), not 3b1b/manim
Pinned to ManimCE because it's the maintained community fork. 3b1b/manim is Grant Sanderson's personal codebase, harder to install, fewer maintainers.

### 2. Local Python package named `vid/`, not `manim/`
The directory was originally `manim/` but that collides with the actual `manim` PyPI package, breaking `from manim import *` inside scene files. Renamed to `vid/`. Don't rename it back. The `vid/lib/` directory is also re-included via `!vid/lib/` in `.gitignore` because the generic `lib/` rule (Python wheel exclude) would otherwise hide it.

### 3. micromamba + conda-forge for the C-library deps
On macOS, `pycairo` and `manimpango` need system `cairo` and `pango`. Homebrew was misconfigured on the build machine (HOMEBREW_CELLAR mis-set, no bottles available). conda-forge ships prebuilt cairo/pango/ffmpeg as conda packages; micromamba is a single 5MB static binary that doesn't need root. This is the standard Manim-on-macOS recipe.

### 4. Scripts and scenes are 1:1 (numbered)
`scripts/teaser.md` describes 6 sections, and `vid/scenes/teaser/scene_01_*.py` through `scene_06_*.py` implement them. Same convention for the deep-dive (14 scenes, 12 of them rendered + 2 placeholders for camera/screen footage). Keep this numbering aligned when editing.

### 5. Two scenes in the deep-dive intentionally don't render
`scene_02_oncam_hook.py` and `scene_13_demo_capture.py` set `SKIP_RENDER = True`. They exist to keep numbering consistent with the script and the DaVinci edit list. The actual content is camera footage (scene 2) and screen capture (scene 13).

### 6. Honesty over hype
SubQ's launch numbers (52x faster than FlashAttention, 95% RULER 128K, 12M context) are SubQ-reported and not yet independently verified [VentureBeat, May 5 2026]. The video script and blog post are written to **teach the math so viewers can evaluate the claims themselves**, not to amplify hype. The companion `subq-quickstart` repo includes a reproducible needle-in-haystack benchmark so anyone can verify long-context retention claims locally.

This is a strategic asset, not a constraint. If you find yourself adding "amazing" / "groundbreaking" / "revolutionary" copy, stop and re-read this section.

### 7. The teaser ships before the deep-dive
Day 4 of the 10-day sprint. Reasoning: launches plant flags. Even a 75-second pure-Manim teaser shipped within a week of SubQ's launch beats a polished 12-minute video shipped three weeks after.

## Gotchas (in priority order)

1. **`pip install manim` fails on macOS without system cairo.** This is the #1 trap. Use the conda-forge env as documented; do not try to fix pip-manim by installing system cairo unless you really know what you're doing.
2. **The conda solve for `manim + manim-voiceover` together hangs (~18+ min).** The `manim-voiceover` package pulls in heavy TTS deps that explode the dependency graph. Install just `manim` from conda-forge, then `pip install manim-voiceover` inside the env.
3. **Don't rename `vid/` back to `manim/`.** See decision 2 above.
4. **`.gitignore` line 17 (`lib/`) would hide `vid/lib/`.** The negation `!vid/lib/` keeps it visible. Don't remove the negation.
5. **`make` targets use micromamba via `MAMBA_ROOT_PREFIX="$ROOT/.micromamba"`.** Never run `micromamba activate subq` outside that env var or you'll target the user's global micromamba (if any).
6. **Manim CE versions move fast.** As of writing the env targets `manim` (latest from conda-forge, ~0.18+). If a future scene file uses an API that shifts, pin in `environment.yml`.
7. **The SubQ Python SDK (`subq` package) is a placeholder.** As of writing, the production package surface isn't documented yet. The starter-repo example scripts assume `from subq import SubQ` with a `client.responses.create(...)` shape, which mirrors the OpenAI SDK convention. Update once docs exist at https://docs.subq.ai.
8. **Tina doesn't yet have SubQ beta access.** The live demo at the end of the deep-dive depends on it. If access is denied by Day 8 of the sprint, the demo becomes a "what I'd build the day I get access" mock-up — still valuable but weaker. Apply for the waitlist immediately.

## How to continue the work

The current state is "scripts + scaffolding done, env install pending." The most likely next session picks up here:

1. Run `make setup` (with the lean install fix described above).
2. Run `make check` to confirm Manim and ffmpeg both work.
3. Run `make teaser QUALITY=-ql` for a quick low-quality smoke test that all 6 scenes render without errors.
4. Polish each teaser scene against [`scripts/teaser.md`](scripts/teaser.md). Each scene file has a docstring linking back to the script section it implements.
5. Render the teaser at `QUALITY=-qh` (1080p), assemble in DaVinci against the VO recording.
6. Move on to the deep-dive scenes one at a time.

See [`TASKS.md`](TASKS.md) for the live backlog with acceptance criteria.

## Voice + tone for any text content

Engineers, not marketing. Concrete numbers with sources. No "leverage", "unlock", "supercharge", "revolutionary", "AI-powered", or "next generation". When in doubt, fewer adjectives, more equations.

## Citations

All sources for facts that appear in any video, blog post, or README live in [`research/notes.md`](research/notes.md). Every numeric claim should map to a footnote there. If you're adding a new claim, add the source to `research/notes.md` first.
