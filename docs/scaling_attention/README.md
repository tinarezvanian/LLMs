# Scaling laws and attention (LaTeX)

Companion write-up to the SubQ Manim demo in the parent `LLMs` repository. Content is distilled from
`LLMs/research/notes.md`.

## Build (minimal TeX)

From this directory:

```bash
pdflatex main.tex
pdflatex main.tex
```

Produces `main.pdf` (pdfLaTeX + Latin Modern; no `tufte-book`, `fontspec`, or `biblatex` required).

## Optional: EB Garamond (XeLaTeX, closer to Algorithmic Adventures)

The parent project's `Algorithmic_Adventures/preamble.tex` expects EB Garamond under `./fonts/`.
If you copy the TTF files into `fonts/` here, you can adapt `preamble.tex` to use `fontspec` again
(tufte-book optional).

## Files

| File | Role |
|------|------|
| `main.tex` | Document shell |
| `preamble.tex` | Packages (derived from `Algorithmic_Adventures/preamble.tex`, simplified for portability) |
| `sections/*.tex` | Chapters |
| `sections/references.tex` | Manual `\bibitem` bibliography (no BibTeX pass required) |
| `upstream_preamble_algorithmic_adventures.tex` | Exact copy of `Algorithmic_Adventures/preamble.tex` for typography reference (tufte-book + EB Garamond path). Default build uses portable `preamble.tex` instead. |
| `aux/science.bib` | Optional BibTeX mirror of the same references |
| `compile.sh` | Two-pass `pdflatex` |

## Provenance

- Layout and package choices trace to `Algorithmic_Adventures/main.tex` + `Algorithmic_Adventures/preamble.tex`.
- Science content traces to `LLMs/research/notes.md`.
