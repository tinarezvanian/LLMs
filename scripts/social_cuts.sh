#!/usr/bin/env bash
# Re-encode the 16:9 teaser concat into 1:1 (1080x1080) and 9:16 (1080x1920)
# crops for X / IG / Reels / Shorts / TikTok. The source must already exist —
# run `make concat` first.
#
# 1:1  : center-crop the 16:9 to a 1080-wide square.
# 9:16 : pad the 16:9 horizontally with the dark theme bg into a portrait
#        canvas, then add letterbox bars top + bottom (none, but visually
#        clean). This preserves the full Manim composition without cropping
#        type or animations off-frame.
#
# All outputs land in edit/renders/teaser/_concat/.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/edit/renders/teaser/_concat/teaser-1080p60.mp4"
OUT_DIR="$ROOT/edit/renders/teaser/_concat"
FFMPEG="$ROOT/bin/ffmpeg"
BG="0x0B1020"   # SUBQ_BG hex sans '#', as ffmpeg expects.

if [[ ! -f "$SRC" ]]; then
  echo "missing $SRC — run 'bash scripts/concat_scenes.sh teaser 1080p60' first" >&2
  exit 1
fi

OUT_1x1="$OUT_DIR/teaser-1x1-1080.mp4"
OUT_9x16="$OUT_DIR/teaser-9x16-1080.mp4"

echo "==> 1:1 1080x1080 -> $OUT_1x1"
"$FFMPEG" -hide_banner -loglevel warning -y -i "$SRC" \
  -vf "crop=1080:1080:(in_w-1080)/2:0,setsar=1" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart \
  -an "$OUT_1x1"

echo "==> 9:16 1080x1920 -> $OUT_9x16  (letterboxed on $BG, CTA-safe top third)"
"$FFMPEG" -hide_banner -loglevel warning -y -i "$SRC" \
  -vf "scale=1080:608:flags=lanczos,pad=1080:1920:0:656:color=$BG,setsar=1" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart \
  -an "$OUT_9x16"

for f in "$OUT_1x1" "$OUT_9x16"; do
  # ffmpeg -i with no output exits 1 — that's expected during probing.
  DUR=$("$FFMPEG" -hide_banner -i "$f" 2>&1 | grep -oE "Duration: [0-9:.]+" | head -1 || true)
  SIZE=$(du -h "$f" | awk '{print $1}')
  echo "    ${DUR#Duration: }  $SIZE  $f"
done
