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
# Optional: CHECK_OVERFULL=1 ./compile.sh  (lists Overfull \\hbox from main.log)
# Strict gate: CHECK_OVERFULL=1 FAIL_MAX_PT=30 ./compile.sh
if [[ -n "${CHECK_OVERFULL:-}" ]]; then
  ./check_overfull.sh
fi
