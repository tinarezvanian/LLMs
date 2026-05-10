#!/usr/bin/env bash
# Concatenate all scene MP4s for a track into one preview file using ffmpeg's
# concat demuxer (no re-encode). Outputs land under edit/renders/<track>/_concat/.
#
# Usage:
#   bash scripts/concat_scenes.sh teaser   [resolution]
#   bash scripts/concat_scenes.sh deepdive [resolution]
#
# resolution defaults to 1080p60. Use 480p15 / 720p30 / 2160p60 for other QUALITY runs.
#
# Why concat demuxer: every scene is rendered with identical Manim settings
# (Pango fonts, 60 fps, H.264, yuv420p), so streams can be glued without
# re-encoding. If a stream mismatch ever shows up, switch to filter_complex
# concat (slower but tolerant).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TRACK="${1:-teaser}"
RES="${2:-1080p60}"

case "$TRACK" in
  teaser|deepdive) ;;
  *) echo "track must be 'teaser' or 'deepdive', got: $TRACK" >&2; exit 1;;
esac

VID_DIR="$ROOT/edit/renders/$TRACK/videos"
OUT_DIR="$ROOT/edit/renders/$TRACK/_concat"
mkdir -p "$OUT_DIR"

# Discover scene MP4s in numerical order (scene_01, scene_02, ...).
# macOS ships bash 3.2, so no `mapfile`; use a portable while-read loop.
LIST="$OUT_DIR/$TRACK-$RES.list"
: > "$LIST"
COUNT=0
while IFS= read -r s; do
  printf "file '%s'\n" "$s" >> "$LIST"
  COUNT=$((COUNT + 1))
done < <(find "$VID_DIR" -mindepth 3 -maxdepth 3 -type f -name "*.mp4" | grep "/$RES/" | sort)

if [[ $COUNT -eq 0 ]]; then
  echo "no MP4s found at $VID_DIR/*/$RES/*.mp4 — run 'QUALITY=-qh make $TRACK' first" >&2
  rm -f "$LIST"
  exit 1
fi

OUT="$OUT_DIR/$TRACK-$RES.mp4"
echo "==> concat $COUNT scenes -> $OUT"
"$ROOT/bin/ffmpeg" -hide_banner -loglevel warning -y -f concat -safe 0 -i "$LIST" -c copy "$OUT"

# ffmpeg -i with no output returns exit 1 — that's expected during probing.
DUR=$("$ROOT/bin/ffmpeg" -hide_banner -i "$OUT" 2>&1 | grep -oE "Duration: [0-9:.]+" | head -1 || true)
SIZE=$(du -h "$OUT" | awk '{print $1}')
echo "    ${DUR#Duration: }  $SIZE  $OUT"
