#!/usr/bin/env bash
# Rename Manim last-frame PNGs into tweet-sized filenames for the X thread.
# Prerequisites: run `make stills` from repo root (needs micromamba env).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/edit/renders/stills/images"
DST="$ROOT/assets/x_thread_stills"
mkdir -p "$DST"

pick() {
  local dir="$1"
  local out="$2"
  local f
  f="$(find "$SRC/$dir" -maxdepth 1 -name '*.png' -print -quit)"
  if [[ -z "${f:-}" ]]; then
    echo "missing PNG under $SRC/$dir — run: make stills" >&2
    exit 1
  fi
  cp "$f" "$DST/$out"
  echo "OK $out <= $(basename "$f")"
}

[[ -d "$SRC" ]] || { echo "No stills at $SRC — run: make stills" >&2; exit 1; }

pick scene_03_scaling_laws   02_scaling_laws_kaplan.png
pick scene_04_pivot         03_pivot_context_length.png
pick scene_05_attention     04_attention_grid.png
pick scene_06_kv_wall       05_kv_cache_overflow.png
pick scene_08_landscape     06_post_transformer_tree.png
pick scene_11_benchmarks    07_subq_benchmark_callouts.png

echo "Done. Square-crop / resize to 1080×1080 in Resolve or ffmpeg before posting if needed."
