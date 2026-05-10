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
  theme.py                     palette, type sizes, pacing constants, equation()/text_equation() helpers
  lib/mobjects.py              reusable mobjects (AttentionGrid, GPUOutline, KVCacheBar, ScalingCurve, PostTransformerTree, SubQWordmark)
  scenes/teaser/scene_0N_*.py  6 teaser scenes, one Manim Scene class per file
  scenes/deepdive/scene_0N_*.py 11 deep-dive scenes (some are placeholders with SKIP_RENDER = True for camera/screen segments)
companion/
  subq-quickstart/             standalone GitHub starter repo to publish separately (MIT)
    README.md                  "Build a whole-codebase QA agent on SubQ in 50 lines"
    LICENSE                    MIT
    examples/codebase-qa/      load entire repo into context, ask cross-file questions
    examples/long-doc-summarizer/  load 500-page PDF into context
    benchmarks/needle_in_haystack.py   reproducible long-context test
    BENCHMARKS.md              methodology + results template
  blog/post.md                 written companion to the deep-dive (MDX-ready)
  social/x_thread.md           9-tweet launch thread
  cover_letter.md              cover note for the SubQ application
assets/branding/               SubQ wordmark sources, palette swatches (.gitkeep'd)
  fonts/Inter/                 Inter v4 (rsms/inter, SIL OFL) — Regular/Medium/SemiBold/Bold + Inter Display
  fonts/JetBrainsMono/         JetBrains Mono v2.304 (jb/JetBrainsMono, SIL OFL) — Regular/Medium/Bold
audio/  video/  demo/  edit/   pipeline dirs (.gitkeep'd) — large media gitignored: VO recordings, on-cam footage, screen capture, DaVinci project
bin/                           project-local binaries (ffmpeg, micromamba); large files gitignored
.venv/  .micromamba/           gitignored Python toolchains
LICENSE                        MIT (project root)
Makefile                       `make setup` / `make check` / `make teaser` / `make deepdive` / `make stills` / `make concat` / `make socials` / `make all` / `make clean` / `make setup-latex` / `make help`
environment.yml                conda-forge env spec (canonical install path)
```

## Setup (clean machine, macOS)

```bash
# 1) ffmpeg (static binary, no Homebrew dependency)
mkdir -p bin && curl -L -o bin/ffmpeg.zip "https://evermeet.cx/ffmpeg/getrelease/zip" \
  && (cd bin && unzip -o ffmpeg.zip && rm ffmpeg.zip)

# 2) micromamba (static binary, no system install)
curl -Ls https://micro.mamba.pm/api/micromamba/osx-64/latest | tar -xvj bin/micromamba

# 3) conda env (lean: manim + ffmpeg only; pip install manim-voiceover separately if needed — see Gotcha 2)
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
`scripts/teaser.md` describes 6 sections, and `vid/scenes/teaser/scene_01_*.py` through `scene_06_*.py` implement them. Same convention for the deep-dive (11 Manim scenes + 2 SKIP_RENDER placeholders for camera/screen footage = 13 total numbered files; the script's "Scene 4 — pivot" doubles as the Chinchilla beat, which used to have its own scene file but was reconciled away — see TASKS.md). Keep this numbering aligned when editing, and update the Makefile's `DEEPDIVE_SCENES` list whenever a scene is renamed.

### 5. Two scenes in the deep-dive intentionally don't render
`scene_02_oncam_hook.py` and `scene_13_demo_capture.py` set `SKIP_RENDER = True`. They exist to keep numbering consistent with the script and the DaVinci edit list. The actual content is camera footage (scene 2) and screen capture (scene 13).

### 6. Honesty over hype
SubQ's launch numbers (52x faster than FlashAttention, 95% RULER 128K, 12M context) are SubQ-reported and not yet independently verified [VentureBeat, May 5 2026]. The video script and blog post are written to **teach the math so viewers can evaluate the claims themselves**, not to amplify hype. The companion `subq-quickstart` repo includes a reproducible needle-in-haystack benchmark so anyone can verify long-context retention claims locally.

This is a strategic asset, not a constraint. If you find yourself adding "amazing" / "groundbreaking" / "revolutionary" copy, stop and re-read this section.

### 7. The teaser ships before the deep-dive
Day 4 of the 10-day sprint. Reasoning: launches plant flags. Even a 75-second pure-Manim teaser shipped within a week of SubQ's launch beats a polished 12-minute video shipped three weeks after.

## Gotchas (in priority order)

1. **`pip install manim` fails on macOS without system cairo.** This is the #1 trap. Use the conda-forge env as documented; do not try to fix pip-manim by installing system cairo unless you really know what you're doing.
2. **The conda solve for `manim + manim-voiceover` together hangs (~18+ min).** The `manim-voiceover` package pulls in heavy TTS deps that explode the dependency graph. `make setup` installs only `manim` + `ffmpeg` from conda-forge; add `pip install manim-voiceover` afterward if you need voiceover automation.
3. **`MathTex` / `equation()` require system LaTeX with the `preview` package.** Shipped deep-dive scenes avoid this by using **`text_equation()`** for on-screen formulas. If you add new `equation()` calls and hit `preview.sty not found`, install `preview` (MiKTeX / TeX Live) or switch to `text_equation()`. Teaser scene 2 uses `Text("O(n²)")`.
4. **Don't rename `vid/` back to `manim/`.** See decision 2 above.
5. **`.gitignore` line 17 (`lib/`) would hide `vid/lib/`.** The negation `!vid/lib/` keeps it visible. Don't remove the negation.
6. **`make` targets use micromamba via `MAMBA_ROOT_PREFIX="$ROOT/.micromamba"`.** Never run `micromamba activate subq` outside that env var or you'll target the user's global micromamba (if any).
7. **Manim CE versions move fast.** As of writing the env targets `manim` (latest from conda-forge, ~0.20+). If a future scene file uses an API that shifts, pin in `environment.yml`.
8. **The SubQ Python SDK (`subq` package) is a placeholder.** As of writing, the production package surface isn't documented yet. The starter-repo example scripts assume `from subq import SubQ` with a `client.responses.create(...)` shape, which mirrors the OpenAI SDK convention. **`pip install -r requirements.txt` will fail on this line until SubQ ships the package** — that's expected; the failure is the prompt to update the import once docs exist at https://docs.subq.ai.
9. **Tina doesn't yet have SubQ beta access.** The live demo at the end of the deep-dive depends on it. If access is denied by Day 8 of the sprint, the demo becomes a "what I'd build the day I get access" mock-up — still valuable but weaker. Apply for the waitlist immediately.
10. **Three deep-dive scene files were intentionally deleted on 2026-05-09.** `scene_04_chinchilla.py`, `scene_05_attention_grid.py`, `scene_07_flash_attention.py` were duplicates of canonical scenes 04/05/07; their better bits were folded in. Don't restore them from git history without re-reading TASKS.md "Reconcile duplicate scene files".
11. **Don't call bare `Text("foo")` in scene code.** It bypasses Inter / JetBrains Mono and lands as system sans, which reads inconsistent next to helper-rendered text. Always go through `body()` / `caption()` / `mono()` / `title()` / `heading()` / `text_equation()` from `vid/theme.py` (or pass `font=FONT_SANS` / `FONT_SANS_DISPLAY` / `FONT_MONO` explicitly). The fonts are auto-registered with Pango at theme import; ship a missing TTF and that single label silently falls back — diff scene PNGs against a known-good frame to catch this.

## How to continue the work

Current state: **`make setup` + `make check` work; `-ql` smoke and `-qh` production renders for teaser + deep-dive Manim scenes both pass without LaTeX** (formulas use `text_equation` where needed). MP4s land in `edit/renders/` (gitignored). **`QUALITY=-qh make stills`** + [`scripts/export_x_thread_stills.sh`](scripts/export_x_thread_stills.sh) refreshes `assets/x_thread_stills/` at production resolution. **`make concat`** stitches each track into a single preview MP4 under `edit/renders/<track>/_concat/`, and **`make socials`** writes `teaser-1x1-1080.mp4` (square) + `teaser-9x16-1080.mp4` (portrait, letterboxed on the SubQ background) — both silent, since the editor lays VO on top in DaVinci.

Next steps, in order:

1. **TASK 4.3** — Tina watches the teaser concat (`edit/renders/teaser/_concat/teaser-1080p60.mp4`) against [scripts/teaser.md](scripts/teaser.md) pacing (human).
2. Optional **4K archive**: `QUALITY=-qk make teaser` / `make deepdive` once picture is locked, then re-run `make concat RES=2160p60`.
3. Lock VO + edit per [`scripts/runbook_edit_and_ship.md`](scripts/runbook_edit_and_ship.md); export **16:9, 1:1, and 9:16** masters using the concat outputs as the picture lock (see [DESIGN.md §3, §7](DESIGN.md)).
4. Shoot day ([`scripts/runbook_shoot_day.md`](scripts/runbook_shoot_day.md)): camera + SubQ Code capture + final VO — needs SubQ beta for live demo.
5. Primary-source reading for interviews: [`research/PAPER_CHECKLIST.md`](research/PAPER_CHECKLIST.md).

See [`TASKS.md`](TASKS.md) for the live backlog with acceptance criteria.

## Voice + tone for any text content

Engineers, not marketing. Concrete numbers with sources. No "leverage", "unlock", "supercharge", "revolutionary", "AI-powered", or "next generation". When in doubt, fewer adjectives, more equations.

## Citations

All sources for facts that appear in any video, blog post, or README live in [`research/notes.md`](research/notes.md). Every numeric claim should map to a footnote there. If you're adding a new claim, add the source to `research/notes.md` first.
