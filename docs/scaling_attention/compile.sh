#!/usr/bin/env bash
# XeLaTeX (required: tufte-latex, fontspec, EB Garamond in ./fonts/)
set -euo pipefail
cd "$(dirname "$0")"
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
echo "==> $(pwd)/main.pdf"
