# LLMs / SubQ Video Demo

Video portfolio piece for a Founding Developer Advocate application to [Subquadratic (SubQ)](https://subq.ai/introducing-subq) — a two-part Manim video package explaining LLM scaling laws, the quadratic-attention wall, and the post-transformer landscape SubQ ships into.

**Status (2026-05-09):** `make setup` + `make check` pass. Teaser smoke-renders at `-ql` (all 6 scenes). Deep-dive renders pending: install LaTeX `preview` package (see [Troubleshooting](#troubleshooting--latex--previewsty-not-found-deep-dive-only)).

## What's in here

- **Teaser** (~75s, pure Manim + voiceover) — `vid/scenes/teaser/`
- **Deep-dive** (~11min, hybrid: Manim + on-camera + live SubQ Code demo) — `vid/scenes/deepdive/`
- **Scripts** — [scripts/teaser.md](scripts/teaser.md), [scripts/deepdive.md](scripts/deepdive.md)
- **Research** — [research/notes.md](research/notes.md) — sourced primer on Kaplan/Chinchilla scaling laws, attention math, the subquadratic landscape (Mamba, Hyena, RWKV, hybrids), and SubQ's launch facts
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
make deepdive            # all deep-dive Manim scenes (needs LaTeX, see Troubleshooting)
make all                 # both
make stills              # export PNG frames for the X thread
make help                # list every target
make clean               # remove edit/renders and __pycache__
QUALITY=-ql make teaser  # 480p15  — fast smoke render
QUALITY=-qh make all     # 1080p60 — production
QUALITY=-qk make all     # 2160p60 — archive master
```

Rendered MP4s land in `edit/renders/{teaser,deepdive}/videos/<scene_name>/<resolution>/<SceneName>.mp4` where `<resolution>` is `480p15` / `720p30` / `1080p60` / `2160p60` depending on `QUALITY`. They get assembled in DaVinci Resolve against the voiceover and on-camera tracks.

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

## Troubleshooting — LaTeX / `preview.sty` not found (deep-dive only)

Scenes that call `equation()` or `MathTex` delegate to your system `latex`. A minimal MiKTeX/TeX Live install often omits the **`preview`** package. If Manim prints `LaTeX Error: File 'preview.sty' not found`:

- **MiKTeX:** open MiKTeX Console → Packages → search `preview` → install.
- **TeX Live / MacTeX:** `sudo tlmgr install preview`
- **Hint:** `make setup-latex` prints these commands in case you forget.

The **teaser** avoids this for the hot path: scene 2 uses `Text("O(n²)")` instead of `MathTex`. **`make deepdive`** still expects LaTeX until those scenes are refactored. As an escape hatch, `vid/theme.py` exposes `text_equation(plain_text)` which renders a plain `Text` instead of `MathTex` — use it in any scene that needs to render on a machine without LaTeX.

## License

MIT — see [LICENSE](LICENSE). The companion starter repo also ships under MIT (see [companion/subq-quickstart/LICENSE](companion/subq-quickstart/LICENSE)).

---

## Distribution

- YouTube (deep-dive primary, teaser as Short)
- X thread (teaser embedded in tweet 1, Manim stills as standalones, deep-dive linked at the end)
- LinkedIn (deep-dive embed)
- Personal blog (companion post mirroring the deep-dive, with all source links)
- GitHub (`companion/subq-quickstart` repo referenced from the demo)
