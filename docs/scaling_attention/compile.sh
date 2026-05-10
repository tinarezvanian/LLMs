#!/usr/bin/env bash
# XeLaTeX (required: tufte-latex, fontspec, Alegreya Sans TTFs in ./fonts/).
# Three passes: first builds .aux + .toc, second resolves them, third stabilises
# the table of contents page numbers.
set -euo pipefail
cd "$(dirname "$0")"
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
echo "==> $(pwd)/main.pdf"
