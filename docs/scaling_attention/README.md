# Scaling laws and attention (LaTeX, XeLaTeX + tufte-book)

Companion write-up to the SubQ Manim demo; science content from `LLMs/research/notes.md`.

## Template

This directory mirrors **Algorithmic Adventures** (`Algorithmic_Adventures/main.tex` + `preamble.tex`):

- **`preamble.tex`** — same as `Algorithmic_Adventures/preamble.tex`, plus these lines at the top/bottom:
  `\PassOptionsToPackage{numbers,sort&compress}{natbib}` (before `\documentclass`),
  `\usepackage{amssymb}`, and `\newcommand{\bigO}{\mathcal{O}}`.
- **`main.tex`** — same shell as the source book: `\maketitle` → `sections/copyright` → `\frontmatter` →
  abstract + `\tableofcontents` → `\mainmatter` → `\part` / `\input{sections/...}` → `\backmatter` / references.
- **`fonts/`** — EB Garamond TTFs (see `fonts/README.md`) matching the `\setmainfont[Path=./fonts/]{EB Garamond}` block.

## Build (XeLaTeX)

Requires a TeX distribution with **tufte-latex** and **fontspec** (TeX Live / MacTeX / full MiKTeX).

On a minimal MiKTeX install you may need extra packages (dependencies pulled in by tufte), for example:
`tufte-latex`, `sauerj` (provides `optparams.sty`), `xifthen`, `ifmtarg`, `xltxtra`, `changepage`, `paralist`, `textcase`, `natbib`, `placeins`, `multirow`, `siunitx`, `mdwtools`, etc.
Use `mpm --install=<packagename>` when the log reports a missing `.sty` file.

```bash
cd docs/scaling_attention
./compile.sh
```

Or manually: `xelatex main.tex` twice.

## Files

| File | Role |
|------|------|
| `main.tex` | Document shell (Algorithmic Adventures structure) |
| `preamble.tex` | Same as `Algorithmic_Adventures/preamble.tex` + minor math package lines |
| `sections/copyright.tex` | Copyright / attribution page |
| `sections/*.tex` | Chapters |
| `sections/references.tex` | `\bibitem` bibliography |
| `aux/science.bib` | Optional BibTeX mirror |
| `compile.sh` | Two-pass XeLaTeX |

## Provenance

- Layout, class, fonts, and list-of-problems macros: **Algorithmic Adventures** (Ehsan Shah-Hosseini).
- Scientific content: **`LLMs/research/notes.md`**.
