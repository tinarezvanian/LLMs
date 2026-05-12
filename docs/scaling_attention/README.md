# From n-grams to Subquadratic Attention (LaTeX, XeLaTeX + tufte-book)

A book-length companion to the SubQ Manim demo. Builds from first principles
(what an LM is, tokens, n-grams, RNN/LSTM) through the transformer, scaling
laws, FlashAttention and the KV-cache mitigations, the subquadratic
alternatives (Mamba, Hyena, linear attention, hybrids), and finally the 2x2
quadrant frame for SSA / SubQ and what could come next (diffusion LMs, JEPA).

## Template

This directory is a `tufte-book` (XeLaTeX) project with the body face set to
**Alegreya Sans** per the project brief.

- **`preamble.tex`** — `tufte-book` shell with:
  - `\PassOptionsToPackage{numbers,sort&compress}{natbib}` (before `\documentclass`)
  - `\setmainfont[Path=./fonts/]{Alegreya Sans}` (Regular / Bold / Italic /
    BoldItalic), with `\AlegreyaLight` and `\AlegreyaDisplay` newfontfamily
    aliases for body running text and chapter titles.
  - Math macros (`\bigO`, `\softmax`, `\Attn`, `\heads`, `\dmodel`, `\dhead`).
  - Title-page additions: `\subtitle{...}` macro and a custom `\maketitle`
    that renders title → subtitle → author → date.
  - `\keyidea{...}` punch-box used at the close of every chapter.
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

## Current state

- **128 pages**, ~487 KB, builds clean with `xelatex` (two passes).
- **Zero `\fillme` stubs** remaining. Don't reintroduce them.
- **Zero undefined citations or references.**
- Title page credits **Tina Rezvanian**; subtitle uses the `\subtitle{}` macro defined in `preamble.tex`.
- Compiled PDF [`main.pdf`](main.pdf) is tracked in git.

## Hard rules for any LLM editing this book

These exist because past passes broke them. See [`TASKS.md` §Phase 9](../../TASKS.md#phase-9--latex-companion-book-docsscaling_attention) for the full backlog and explanation; the abridged version:

1. **Never append new content after a chapter's `\keyidea{...}` block.** New worked examples / sidebars / tables / figures / listings go into the most natural body section *above* `\keyidea`.
2. **Before adding a paragraph, `grep` the chapter for the same topic.** Past LLMs added duplicate Jamba / PagedAttention / RoPE / Diffusion / JEPA paragraphs because they didn't check. Merge into the existing section, don't create a parallel one.
3. **`\fillme` is gone.** The macro is still defined in `preamble.tex` for back-compat but every call site has been replaced. Don't bring stubs back.
4. **Use the macros already defined in [`preamble.tex`](preamble.tex)**: `\bigO`, `\R`, `\E`, `\T`, `\softmax`, `\Attn`, `\heads`, `\dmodel`, `\dhead`, `\code{}`, `\term{}`, `\subtitle{}`, `\keyidea{}`. Don't roll new ones.
5. **Every new `\citep` / `\citet` needs a matching `\bibitem`** in [`sections/references.tex`](sections/references.tex).
6. **Tables with placeholder cells get deleted, not shipped.** `tab:ruler-third-party` was removed for this reason. Back every cell with a source or drop the table.
7. **Mark vendor-reported / speculative claims explicitly** with `\dag` / `\textsuperscript{*}` and a caption footnote — see `tab:hybrid-compare` for the template.
8. **Always run `xelatex` twice** for cross-references and citations.

## Provenance

- Scientific content: [`research/notes.md`](../../research/notes.md) plus
  the primary sources cited in
  [`sections/references.tex`](sections/references.tex) (Vaswani 2017,
  Kaplan 2020, Hoffmann 2022, Dao 2022, Gu & Dao 2023, Subquadratic 2026
  SSA technical post, etc.).
- Body face: **Alegreya Sans** by Juan Pablo del Peral, SIL OFL.
