# LLMs / SubQ Video Demo

Video portfolio piece for a Founding Developer Advocate application to [Subquadratic (SubQ)](https://subq.ai/introducing-subq) — a two-part Manim video package explaining LLM scaling laws, the quadratic-attention wall, and the post-transformer landscape SubQ ships into.

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
make setup
make check
```

`make check` should print the installed Manim version and ffmpeg version.

## Render

```bash
make teaser              # all 6 teaser scenes at -qm (medium, 720p)
make deepdive            # all deep-dive Manim scenes
make all                 # both
QUALITY=-qh make all     # HD (1080p)
QUALITY=-qk make all     # 4K
```

Rendered MP4s land in `edit/renders/{teaser,deepdive}/videos/.../1080p60/<SceneName>.mp4` and get assembled in DaVinci Resolve against the voiceover and on-camera tracks.

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

## Distribution

- YouTube (deep-dive primary, teaser as Short)
- X thread (teaser embedded in tweet 1, Manim stills as standalones, deep-dive linked at the end)
- LinkedIn (deep-dive embed)
- Personal blog (companion post mirroring the deep-dive, with all source links)
- GitHub (`companion/subq-quickstart` repo referenced from the demo)
