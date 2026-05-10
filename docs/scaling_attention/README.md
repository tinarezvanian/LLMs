# From n-grams to Subquadratic Attention (LaTeX, XeLaTeX + tufte-book)

A book-length companion to the SubQ Manim demo. Builds from first principles
(what an LM is, tokens, n-grams, RNN/LSTM) through the transformer, scaling
laws, FlashAttention and the KV-cache mitigations, the subquadratic
alternatives (Mamba, Hyena, linear attention, hybrids), and finally the 2x2
quadrant frame for SSA / SubQ and what could come next (diffusion LMs, JEPA).

## Template

This directory uses the **Algorithmic Adventures** layout
(`Algorithmic_Adventures/main.tex` + `preamble.tex`) but switches the body
face to **Alegreya Sans** per the project brief.

- **`preamble.tex`** — `tufte-book` shell with:
  - `\PassOptionsToPackage{numbers,sort&compress}{natbib}` (before `\documentclass`)
  - `\setmainfont[Path=./fonts/]{Alegreya Sans}` (Regular / Bold / Italic /
    BoldItalic), with `\AlegreyaLight` and `\AlegreyaDisplay` newfontfamily
    aliases for body running text and chapter titles.
  - Math macros (`\bigO`, `\softmax`, `\Attn`, etc.).
- **`main.tex`** — six-part book shell: Background → Transformer → Scaling
  laws → Living with O(n²) → Subquadratic alternatives → 2x2 frame + SSA +
  what's next.
- **`fonts/`** — Alegreya Sans TTFs (vendored from `LLMs/docs/Alegreya_Sans/`,
  SIL Open Font License) and the EB Garamond TTFs left in place as a
  fallback if you want to flip the preamble back.

## Build (XeLaTeX)

Requires a TeX distribution with **tufte-latex** and **fontspec**
(TeX Live, MacTeX, or full MiKTeX).

On a minimal MiKTeX install you may need to fetch:

```text
tufte-latex sauerj (optparams.sty) xifthen ifmtarg xltxtra changepage \
paralist textcase natbib placeins multirow siunitx mdwtools
```

Use `mpm --install=<packagename>` when the log reports a missing `.sty`.

```bash
cd docs/scaling_attention
./compile.sh    # runs xelatex twice
```

Or manually: `xelatex main.tex` twice (three times the very first build, to
fully resolve TOC + cross-references).

## Files

| File | Role |
|------|------|
| `main.tex` | Document shell (six parts) |
| `preamble.tex` | Tufte-book + Alegreya Sans + macros |
| `sections/preface.tex` | How to read this book |
| `sections/copyright.tex` | Copyright / attribution page |
| `sections/ch01_what_lm_does.tex` … `ch20_post_attention.tex` | Chapters |
| `sections/references.tex` | Numeric `\bibitem` bibliography |
| `aux/science.bib` | Optional BibTeX mirror |
| `fonts/AlegreyaSans-*.ttf` | Body face |
| `fonts/EBGaramond-*.ttf` | Optional fallback |
| `compile.sh` | Two-pass XeLaTeX |

## To-fill stubs (for future LLM passes)

The book is a draft. Roughly 60 places where a worked example, code listing,
sidebar, comparison table, or case study would help are marked with a
`\fillme{ID}{TITLE}{BRIEF}{SOURCES}{TARGET}` macro. They render as visible
amber boxes in the PDF so they don't get forgotten, and they are
machine-greppable from the command line.

### List every open stub

```bash
# Plain checklist, all 60 stubs with file:line
bash scripts/list_fill_stubs.sh

# Markdown task list, paste-able into an issue
bash scripts/list_fill_stubs.sh --markdown

# Just the totals
bash scripts/list_fill_stubs.sh --count
```

### Recipe for a future LLM picking off a stub

1. Run `bash scripts/list_fill_stubs.sh`. Pick one ID.
2. Open the file at the reported line. Read the surrounding chapter so you
   understand what was already said and what *not* to repeat.
3. Read the sources named in the stub's `Sources.` field — usually a
   primary paper plus the relevant section of `research/notes.md`.
4. Replace the entire `\fillme{...}{...}{...}{...}{...}` invocation with
   the finished prose / table / listing / figure.
5. Hit the target length to within ±30%. Much shorter usually means you
   skipped something the brief asked for.
6. Cite using `\citep{key}` / `\citet{key}` keys already in
   `sections/references.tex`. Add a `\bibitem[Author(Year)]{key}` entry
   if the source isn't there.
7. Recompile (`./compile.sh`) and confirm there are no `Citation undefined`
   or `Reference undefined` warnings in `main.log`.

### Stub categories

- **Worked examples** (numerical) — most chapters have one or two.
- **Code listings** — Python or PyTorch; `language=Python` in `lstlisting`.
- **Sidebars** — half-page deeper dives on topics the body waves at.
- **Case studies** — one full page each on Jamba (and similar).
- **Comparison tables** — `tabular`, usually 3--5 rows.
- **Appendices** (A: shape cheat sheet, B: glossary, C: reading list) — these
  are entirely composed of stubs that should each be filled before the book
  is considered done.

## Provenance

- Layout / class macros: **Algorithmic Adventures** (Ehsan Shah-Hosseini).
- Scientific content: **`LLMs/research/notes.md`** plus the primary sources
  cited in `sections/references.tex` (Vaswani 2017, Kaplan 2020,
  Hoffmann 2022, Dao 2022, Gu & Dao 2023, Subquadratic 2026 SSA technical
  post, etc.).
- Body face: **Alegreya Sans** by Juan Pablo del Peral, SIL OFL.
