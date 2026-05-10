# LLMs / SubQ Video Demo

Video portfolio piece for a Founding Developer Advocate application to [Subquadratic (SubQ)](https://subq.ai/introducing-subq) — a two-part Manim video package explaining LLM scaling laws, the quadratic-attention wall, and the post-transformer landscape SubQ ships into.

**Status (2026-05-09):** `make setup` + `make check` pass. Teaser + deep-dive both render at `-qh` (1080p60). Stitched preview MP4s + 1:1 / 9:16 social cuts available via `make concat` and `make socials`. Deep-dive scenes use `text_equation()` so renders are LaTeX-free.

## What's in here

- **Teaser** (~75s, pure Manim + voiceover) — `vid/scenes/teaser/`
- **Deep-dive** (~11min, hybrid: Manim + on-camera + live SubQ Code demo) — `vid/scenes/deepdive/`
- **Scripts** — [scripts/teaser.md](scripts/teaser.md), [scripts/deepdive.md](scripts/deepdive.md)
- **Research** — [research/notes.md](research/notes.md) — sourced primer on Kaplan/Chinchilla scaling laws, attention math, the subquadratic landscape (Mamba, Hyena, RWKV, hybrids), and SubQ's launch facts
- **LaTeX science companion** — [docs/scaling_attention/](docs/scaling_attention/) — *From n-grams to Subquadratic Attention*, a ~100-page deep-dive primer (six parts: background, transformer, scaling laws, living with O(n²), subquadratic alternatives, SubQ + what comes next). Tufte-book layout (same as `Algorithmic_Adventures`) set in **Alegreya Sans**; build with **XeLaTeX** (`./compile.sh`). See [docs/scaling_attention/README.md](docs/scaling_attention/README.md).
- **Companion deliverables** — `companion/` (GitHub starter repo + blog post + X thread + cover letter)
 - **Plan** — [.cursor/plans/subq_manim_demo_video_a7a5729c.plan.md](.cursor/plans/subq_manim_demo_video_a7a5729c.plan.md) for the full sprint plan
- **Handoff for new agents/humans** — [AGENTS.md](AGENTS.md), [DESIGN.md](DESIGN.md), [TASKS.md](TASKS.md)

## Directory layout

```
vid/                    Manim source (Python package)
  theme.py              palette, fonts, pacing constants
  lib/mobjects.py       reusable mobjects (AttentionGrid, GPUOutline, etc.)
  scenes/teaser/        6 teaser scenes
  scenes/deepdive/      14 deep-dive scenes
scripts/                shooting + voiceover scripts (markdown)
research/               primary-source notes that back every on-screen claim
audio/                  voiceover recordings
video/                  on-camera footage
demo/                   screen-capture footage (SubQ Code session)
edit/                   DaVinci Resolve project + final renders
companion/              GitHub starter repo + blog post + X thread draft
docs/scaling_attention/ LaTeX deep-dive primer (XeLaTeX + tufte-book + Alegreya Sans)
assets/branding/        logos, fonts, color swatches
bin/                    project-local binaries (ffmpeg, micromamba)
```

## Setup

The project uses micromamba + conda-forge for the C-library dependencies (cairo, pango, ffmpeg) that pip can't supply on macOS without a working Homebrew. Everything stays project-local.

```bash
curl -Ls https://micro.mamba.pm/api/micromamba/osx-64/latest | tar -xvj bin/micromamba
mkdir -p bin && curl -L -o bin/ffmpeg.zip "https://evermeet.cx/ffmpeg/getrelease/zip" \
  && (cd bin && unzip -o ffmpeg.zip && rm ffmpeg.zip)

make setup    # creates .micromamba/envs/subq with conda-forge manim + ffmpeg (lean solve)
make check

# Optional: voiceover automation (heavy deps — install only if needed)
# micromamba run -n subq -r .micromamba pip install manim-voiceover
```

`make check` should print the installed Manim version and ffmpeg version.

## Render

```bash
make teaser              # all 6 teaser scenes at default QUALITY=-qm (720p30)
make deepdive            # all deep-dive Manim scenes (shipped scenes use text_equation — no LaTeX)
make all                 # both
make stills              # PNG last frames for X thread (uses QUALITY; default -qm)
make concat              # stitch each track into one preview MP4 (RES=1080p60 by default)
make socials             # 1:1 (1080x1080) + 9:16 (1080x1920) cuts of the teaser concat
make help                # list every target
make clean               # remove edit/renders and __pycache__
QUALITY=-ql make teaser  # 480p15  — fast smoke render
QUALITY=-qh make all     # 1080p60 — production picture lock
QUALITY=-qk make all     # 2160p60 — archive master
QUALITY=-qh make stills  # HD stills matching production (`assets/x_thread_stills/` via scripts/export_x_thread_stills.sh)
RES=720p30 make concat   # concat from a different render resolution (must match prior `make all` QUALITY)
```

Rendered MP4s land in `edit/renders/{teaser,deepdive}/videos/<scene_name>/<resolution>/<SceneName>.mp4` where `<resolution>` is `480p15` / `720p30` / `1080p60` / `2160p60` depending on `QUALITY`. The `make concat` step writes per-track previews to `edit/renders/<track>/_concat/<track>-<res>.mp4`, and `make socials` writes `teaser-1x1-1080.mp4` (square, center-crop) and `teaser-9x16-1080.mp4` (portrait, letterboxed on the SubQ background) next to them. All of it gets assembled in DaVinci Resolve against the voiceover and on-camera tracks; the social cuts are intentionally muxed without audio so the editor's VO is the single source of truth.

## Pipeline

```
research/notes.md
    -> scripts/{teaser,deepdive}.md
        -> vid/scenes/**/*.py     (Manim animations)
        -> audio/                  (recorded voiceover)
        -> video/                  (on-camera footage)
        -> demo/                   (SubQ Code screen capture)
            -> edit/               (DaVinci Resolve assembly)
                -> final masters (4K H.265 + 1080p H.264 + 1:1 social cut)
```

## Troubleshooting — LaTeX / `preview.sty` (optional)

Shipped deep-dive scenes use **`text_equation()`** or plain `Text` for formulas so **`make deepdive` runs without a LaTeX install.** If you add new scenes and call `equation()` / `MathTex`, Manim needs system `latex` plus the **`preview`** package:

- **MiKTeX:** MiKTeX Console → Packages → install `preview`.
- **TeX Live / MacTeX:** `sudo tlmgr install preview`
- **`make setup-latex`** prints these commands.

The teaser hot path still uses `Text("O(n²)")` in scene 2. Prefer `text_equation(...)` from `vid/theme.py` for portable renders.

## License

MIT — see [LICENSE](LICENSE). The companion starter repo also ships under MIT (see [companion/subq-quickstart/LICENSE](companion/subq-quickstart/LICENSE)).

---

## Distribution

- YouTube (deep-dive primary, teaser as Short)
- X thread (teaser embedded in tweet 1, Manim stills as standalones, deep-dive linked at the end)
- LinkedIn (deep-dive embed)
- Personal blog (companion post mirroring the deep-dive, with all source links)
- GitHub (`companion/subq-quickstart` repo referenced from the demo)
- **Operational docs:** [research/PAPER_CHECKLIST.md](research/PAPER_CHECKLIST.md), [scripts/runbook_shoot_day.md](scripts/runbook_shoot_day.md), [scripts/runbook_edit_and_ship.md](scripts/runbook_edit_and_ship.md); X-thread PNGs via `make stills` + [`scripts/export_x_thread_stills.sh`](scripts/export_x_thread_stills.sh)
