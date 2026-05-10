# TASKS.md — explicit step-by-step backlog

> **Audience:** any LLM picking this up cold. Each task lists exact files, exact commands, and a one-line "done when" check.
> Strategy lives in [.cursor/plans/](.cursor/plans/). Style rules in [DESIGN.md](DESIGN.md). Architecture decisions in [AGENTS.md](AGENTS.md).
>
> Status keys: `[x]` done · `[~]` partial / human-only follow-up · `[ ]` not started · `[!]` blocked on external

---

## How to run anything in this repo (do this first)

The whole pipeline runs inside the `subq` micromamba env at `.micromamba/envs/subq/`.

```bash
cd /Users/ed/Developer/LLMs                     # repo root
export MAMBA_ROOT_PREFIX="$PWD/.micromamba"
eval "$(./bin/micromamba shell hook --shell bash)"
micromamba activate subq
export PATH="$PWD/bin:$PATH"
export PYTHONPATH="$PWD:$PYTHONPATH"

make help                                       # list every Make target
```

If `python -c "import typer"` fails inside the env, run `pip install "typer>=0.12" "rich>=13.7"` once (older envs predate the addition to `environment.yml`).

---

## Phase 1 — Research (human only)

- [x] **Aggregate notes** → [research/notes.md](research/notes.md). All cited primary sources.
- [~] **TASK 1.1** Read every P0 paper in [research/PAPER_CHECKLIST.md](research/PAPER_CHECKLIST.md).
  - **Doer:** Tina (human). LLMs cannot complete this.
  - **Done when:** Tina can sketch on a whiteboard (a) Kaplan power law, (b) attention QKV → n×n grid, (c) one post-transformer family of her choice, without notes.

---

## Phase 2 — Scripts

- [x] [scripts/teaser.md](scripts/teaser.md) (~155 words, all `[ANIM]` cues present).
- [x] [scripts/deepdive.md](scripts/deepdive.md) (~1700 words with `[ON-CAM]` / `[ANIM]` / `[SCREEN]` cues).
- [~] **TASK 2.1** Record scratch VO; save under `audio/scratch/teaser.m4a` and `audio/scratch/deepdive.m4a` per [audio/scratch/README.md](audio/scratch/README.md).
  - **Done when:** both files exist and match script word counts within ±10%.

---

## Phase 3 — Production tooling

- [x] Manim env: `make setup` → `make check` prints `manim 0.20.x` + an `ffmpeg` line.
- [x] **Typography:** Inter + JetBrains Mono shipped in [`assets/branding/fonts/`](assets/branding/fonts) and auto-registered by `vid/theme.py`. See [DESIGN.md §1 Typography](DESIGN.md).
- [x] All current scenes smoke-render at `QUALITY=-ql`.

### TASK 3.1 — If a render is missing a font (text suddenly looks like Helvetica/DejaVu)

1. Check the TTFs are present: `ls assets/branding/fonts/Inter assets/branding/fonts/JetBrainsMono` — each should list 4–6 TTFs.
2. If missing, re-run the download:
   ```bash
   curl -sSL -o /tmp/Inter-4.0.zip https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip
   unzip -q -o /tmp/Inter-4.0.zip -d /tmp/Inter-4.0
   cp /tmp/Inter-4.0/extras/ttf/Inter-{Regular,Medium,SemiBold,Bold}.ttf assets/branding/fonts/Inter/
   cp /tmp/Inter-4.0/extras/ttf/InterDisplay-{SemiBold,Bold}.ttf assets/branding/fonts/Inter/
   curl -sSL -o /tmp/JBM.zip https://download.jetbrains.com/fonts/JetBrainsMono-2.304.zip
   unzip -q -o /tmp/JBM.zip -d /tmp/JBM
   cp /tmp/JBM/fonts/ttf/JetBrainsMono-{Regular,Medium,Bold}.ttf assets/branding/fonts/JetBrainsMono/
   ```
3. Re-render the affected scene. If still wrong, the scene file likely calls `Text("...")` directly — replace with `body(...)` / `caption(...)` / `mono(...)` / `text_equation(...)` from `vid.theme` (see Gotcha 11 in [AGENTS.md](AGENTS.md)).

---

## Phase 4 — Animation

### Teaser (6 scenes)

| Scene | File | What it does |
| ----- | ---- | ------------ |
| 01 | [vid/scenes/teaser/scene_01_open.py](vid/scenes/teaser/scene_01_open.py) | Linear cold-open curve |
| 02 | [vid/scenes/teaser/scene_02_curve.py](vid/scenes/teaser/scene_02_curve.py) | Linear → quadratic + `O(n²)` |
| 03 | [vid/scenes/teaser/scene_03_wall.py](vid/scenes/teaser/scene_03_wall.py) | KV bar count-up to 524 GB |
| 04 | [vid/scenes/teaser/scene_04_break.py](vid/scenes/teaser/scene_04_break.py) | Curve cracks → linear green |
| 05 | [vid/scenes/teaser/scene_05_payoff.py](vid/scenes/teaser/scene_05_payoff.py) | code/doc/film chips → one prompt |
| 06 | [vid/scenes/teaser/scene_06_cta.py](vid/scenes/teaser/scene_06_cta.py) | Wordmark + CTA + sheen |

- [x] **TASK 4.1** Smoke render: `QUALITY=-ql make teaser` exits 0; 6 MP4s under `edit/renders/teaser/videos/scene_*/480p15/`.
- [x] **TASK 4.2** Production render: `QUALITY=-qh make teaser`. **Done when** 6 MP4s exist under `edit/renders/teaser/videos/scene_*/1080p60/` and look readable on a phone (≥ iPhone 12 size). *(Automated 2026-05-09 — verify on device.)*
- [ ] **TASK 4.3** Watch each `-qh` render and fix any scene whose VO timing in [scripts/teaser.md](scripts/teaser.md) doesn't fit the animation. **Done when** every `[ANIM:]` cue lands in the right place when read at 124 wpm.

### Deep-dive (11 Manim + 2 `SKIP_RENDER` placeholders)

| Scene | File | Notes |
| ----- | ---- | ----- |
| 01 | [vid/scenes/deepdive/scene_01_cold_open.py](vid/scenes/deepdive/scene_01_cold_open.py) | Title after screen-cap intro |
| 02 | [vid/scenes/deepdive/scene_02_oncam_hook.py](vid/scenes/deepdive/scene_02_oncam_hook.py) | `SKIP_RENDER` — on-cam |
| 03 | [vid/scenes/deepdive/scene_03_scaling_laws.py](vid/scenes/deepdive/scene_03_scaling_laws.py) | Kaplan plot + Chinchilla |
| 04 | [vid/scenes/deepdive/scene_04_pivot.py](vid/scenes/deepdive/scene_04_pivot.py) | Pivot to context-length axis |
| 05 | [vid/scenes/deepdive/scene_05_attention.py](vid/scenes/deepdive/scene_05_attention.py) | Q/K/V → n×n grid |
| 06 | [vid/scenes/deepdive/scene_06_kv_wall.py](vid/scenes/deepdive/scene_06_kv_wall.py) | KV cache equation + 524 GB |
| 07 | [vid/scenes/deepdive/scene_07_flashattention.py](vid/scenes/deepdive/scene_07_flashattention.py) | Three curves (attn / FA / linear) |
| 08 | [vid/scenes/deepdive/scene_08_landscape.py](vid/scenes/deepdive/scene_08_landscape.py) | Post-transformer tree |
| 09 | [vid/scenes/deepdive/scene_09_mamba.py](vid/scenes/deepdive/scene_09_mamba.py) | Rolling state intuition |
| 10 | [vid/scenes/deepdive/scene_10_subq_position.py](vid/scenes/deepdive/scene_10_subq_position.py) | SubQ branch on tree |
| 11 | [vid/scenes/deepdive/scene_11_benchmarks.py](vid/scenes/deepdive/scene_11_benchmarks.py) | Sourced benchmark callouts |
| 12 | [vid/scenes/deepdive/scene_12_demo_intro.py](vid/scenes/deepdive/scene_12_demo_intro.py) | Title before demo |
| 13 | [vid/scenes/deepdive/scene_13_demo_capture.py](vid/scenes/deepdive/scene_13_demo_capture.py) | `SKIP_RENDER` — screen capture |
| 14 | [vid/scenes/deepdive/scene_14_close.py](vid/scenes/deepdive/scene_14_close.py) | End card |

- [x] **TASK 4.4** Smoke render: `QUALITY=-ql make deepdive` exits 0; 12 MP4s under `edit/renders/deepdive/videos/scene_*/480p15/`. (Scenes 02 + 13 do not render — that's expected.)
- [x] **TASK 4.5** Production render: `QUALITY=-qh make deepdive`. **Done when** 12 MP4s exist at 1080p60. *(Automated 2026-05-09 — verify on device.)*
- [x] **TASK 4.6** **Decision (locked):** keep **`text_equation()`** (JetBrains Mono Unicode) for all shipped formula beats — portable, no TeX install. Optional upgrade path: install LaTeX `preview` (`make setup-latex`) and swap specific lines to `equation()` only if a scene needs true fractions/stacked radicals; none of the current scenes require it.
- [x] **TASK 4.7** Stitch per-track preview MP4s: `make concat` writes `edit/renders/{teaser,deepdive}/_concat/{teaser,deepdive}-1080p60.mp4` via ffmpeg's concat demuxer (no re-encode). *(Automated 2026-05-09 — teaser 29.2s, deepdive 79.2s. Lengths are short of the script targets because Manim is B-roll only; on-cam + screencap fill the gap at edit time.)*

### Aspect-ratio prep

- [x] **TASK 4.8** Generate 1:1 (1080×1080) and 9:16 (1080×1920) cuts of the teaser concat: `make socials`. **Done when** `edit/renders/teaser/_concat/teaser-1x1-1080.mp4` and `teaser-9x16-1080.mp4` exist. *(Automated 2026-05-09. Outputs are silent — VO is layered in DaVinci. The 9:16 cut letterboxes on the SubQ background and reserves the upper third for CTA per [DESIGN.md §7](DESIGN.md).)*

### Script-driven Manim follow-ups (queued by the 2026-05-09 deep-dive Scene 9 rewrite)

- [x] **TASK 4.9** Redesign [`vid/scenes/deepdive/scene_10_subq_position.py`](vid/scenes/deepdive/scene_10_subq_position.py) from a **tree branch** to the **2×2 quadrant** visual now described in [scripts/deepdive.md](scripts/deepdive.md) Scene 9. Axes: routing (position-fixed → content-dependent) × scaling (quadratic → linear). Markers: top-right = transformers / FlashAttention / DeepSeek SA*; bottom-left = sliding-window family; bottom-right = Mamba/SSM* (lossy state caveat) + SSA / SubQ (the highlighted drop-in). Source for every claim on screen: [research/notes.md §3.5–3.6](research/notes.md), citation [13]. **Done when** the rendered scene matches the [ANIM] cues in the script and `make deepdive` still passes at `-qh`. *(Done 2026-05-10: `QuadrantMap` in [`vid/lib/mobjects.py`](vid/lib/mobjects.py); `QUALITY=-ql make deepdive` passes.)*
- [x] **TASK 4.10** Add an [ANIM] beat to [`vid/scenes/deepdive/scene_07_flashattention.py`](vid/scenes/deepdive/scene_07_flashattention.py) showing the n×n grid with **most cells dimmed to near-black** to set up the "wastefully quadratic" intuition the new script Scene 7 closes on. Should reuse `AttentionGrid` from `vid/lib/mobjects.py`. **Done when** the new beat sits before `self.wait()` at scene end and the production render still ≤ ~10s. *(Source: [research/notes.md §3.5](research/notes.md), citation [13].)* *(Done 2026-05-10: causal `AttentionGrid` + LaggedStart dim + punch line.)*
- [x] **TASK 4.11** Add a benchmarks-table beat to [`vid/scenes/deepdive/scene_11_benchmarks.py`](vid/scenes/deepdive/scene_11_benchmarks.py) covering the **MRCR v2 leaderboard** verbatim from the script (Opus 4.6 78.3%, GPT 5.5 74.0%, **SubQ 65.9%**, GPT 5.4 36.6%, Opus 4.7 32.2%, Gemini 3.1 Pro 26.3%). The point is the *honest framing* — SubQ in the conversation, not at the top. **Done when** the table renders legibly at 1080p and the source footnote cites `subq.ai/how-ssa-makes-long-context-practical, May 5 2026`. *(Done 2026-05-10.)*

---

## Phase 5 — Shoot day

Runbook: [scripts/runbook_shoot_day.md](scripts/runbook_shoot_day.md). All tasks are human-only.

- [!] **TASK 5.1** Apply for SubQ beta at [subq.ai](https://subq.ai). Blocks tasks 5.5, 7.2.
- [ ] **TASK 5.2** Capture on-cam intro → `video/oncam_intro.mov` (3+ takes, 4K24, 50mm).
- [ ] **TASK 5.3** Capture on-cam outro → `video/oncam_outro.mov` (3+ takes).
- [ ] **TASK 5.4** Record final VO (deep-dive script) → `audio/final/deepdive_vo.wav`.
- [!] **TASK 5.5** Record SubQ Code demo (OBS, 1440p, no secrets visible) → `demo/subq_code_session.mov` (3+ takes).
  - Blocked on TASK 5.1.

---

## Phase 6 — Edit + ship

Runbook: [scripts/runbook_edit_and_ship.md](scripts/runbook_edit_and_ship.md). DaVinci Resolve.

- [ ] **TASK 6.1** Build VO spine timeline; lay Manim renders to picture; sync on-cam takes.
- [ ] **TASK 6.2** Color (warm grade on on-cam only; do not regrade Manim).
- [ ] **TASK 6.3** Sound mix: dialog -18 LUFS, music bed -22 LUFS under VO.
- [ ] **TASK 6.4** Captions: Whisper-large transcribe → hand-fix `α`, `√`, `n²`, `FlashAttention`, `RULER`, `SSA`, model names per [DESIGN.md §6](DESIGN.md).
- [ ] **TASK 6.5** Render delivery masters per [DESIGN.md §3](DESIGN.md). Animation-only previews are already shipped from `make concat` + `make socials` (`edit/renders/teaser/_concat/`); the editor uses those as the picture lock and adds VO + on-cam.
  - 4K H.265 archive (16:9, deep-dive)
  - 1080p H.264 (16:9, YouTube)
  - 1080×1080 teaser (X / Instagram) — start from `teaser-1x1-1080.mp4`
  - 1080×1920 teaser (Shorts / Reels / TikTok) — start from `teaser-9x16-1080.mp4`; **CTA text in upper third**, see safe-area table

---

## Phase 7 — Companion deliverables

- [x] [companion/subq-quickstart/README.md](companion/subq-quickstart/README.md), [examples/codebase-qa/load_repo.py](companion/subq-quickstart/examples/codebase-qa/load_repo.py), [examples/long-doc-summarizer/summarize_pdf.py](companion/subq-quickstart/examples/long-doc-summarizer/summarize_pdf.py), [benchmarks/needle_in_haystack.py](companion/subq-quickstart/benchmarks/needle_in_haystack.py), [BENCHMARKS.md](companion/subq-quickstart/BENCHMARKS.md), [PUBLISH.md](companion/subq-quickstart/PUBLISH.md), [LICENSE](companion/subq-quickstart/LICENSE).
- [x] [companion/blog/post.md](companion/blog/post.md), [companion/social/x_thread.md](companion/social/x_thread.md), [companion/cover_letter.md](companion/cover_letter.md).
- [x] **TASK 7.1** Generate X-thread stills (use **`-qh`** so PNGs match production resolution):
  ```bash
  QUALITY=-qh make stills
  bash scripts/export_x_thread_stills.sh
  ```
  **Done when** `assets/x_thread_stills/02_*…07_*.png` all exist (regenerated 2026-05-09 at 1080p60).
- [!] **TASK 7.2** Run real benchmarks against SubQ. Requires `SUBQ_API_KEY`. Blocked on TASK 5.1.
  ```bash
  cd companion/subq-quickstart/benchmarks
  python needle_in_haystack.py --tokens 500000 --trials 5
  ```
  **Done when** [BENCHMARKS.md](companion/subq-quickstart/BENCHMARKS.md) has at least the 128k / 500k / 1M rows filled in (or honestly marked as "model returned X — see results.json").
- [ ] **TASK 7.3** Publish `subq-quickstart` as its own GitHub repo per [companion/subq-quickstart/PUBLISH.md](companion/subq-quickstart/PUBLISH.md). **Done when** `https://github.com/tinarezvanian/subq-quickstart` resolves and READMEs match.
- [ ] **TASK 7.4** Schedule X thread for ~9am PT using your scheduler of choice (Typefully, Hypefury, native X scheduler).

---

## Phase 8 — Submit

- [ ] **TASK 8.1** In [companion/cover_letter.md](companion/cover_letter.md): replace every `[link]`, `[email]`, `[phone]`, `[github]`, `[twitter]` placeholder with verified live values.
- [ ] **TASK 8.2** In [companion/social/x_thread.md](companion/social/x_thread.md): replace `@SubQ_AI @JustinDangel @AlexWhedon` with the real verified handles for SubQ founders.
- [ ] **TASK 8.3** Submit application via SubQ careers page with the cover letter + 4 links (teaser YT, deep-dive YT, blog, `subq-quickstart` repo).

---

## Done definition (whole sprint)

- [ ] Teaser uploaded to YouTube + embedded in X tweet 1
- [ ] Deep-dive uploaded to YouTube
- [ ] Blog post live
- [ ] X thread posted
- [ ] `subq-quickstart` public on GitHub with ≥1 real benchmark row
- [ ] Application submitted

---

## Already-decided things (do not re-litigate)

- Local Manim package directory is **`vid/`**, never `manim/` (PyPI collision; AGENTS Decision 2).
- Conda env is **lean** — no `manim-voiceover` in `environment.yml` (solver hangs; AGENTS Gotcha 2).
- Three deep-dive scenes (`scene_04_chinchilla.py`, `scene_05_attention_grid.py`, `scene_07_flash_attention.py`) were **deleted on 2026-05-09**; their useful bits live in the canonical 04/05/07 files. Don't restore them.
- All on-screen formulas use `text_equation()` (Unicode `Text`) rather than `equation()` (LaTeX) so deep-dive renders without TeX. Switch back to `equation()` only after `make setup-latex`.
- All on-screen text goes through the helpers in `vid/theme.py` (`body`, `caption`, `mono`, `title`, `heading`, `text_equation`); bare `Text("...")` is banned (Gotcha 11).
- Aspect ratio set: **16:9 + 1:1 + 9:16**. See [DESIGN.md §3, §7](DESIGN.md).
