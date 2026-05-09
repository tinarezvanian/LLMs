# Runbook — Phase 6 (edit + ship)

## DaVinci Resolve (assembly)

1. Create timeline at **24 fps** for on-cam; Manim renders are **30 fps** by default — conform or interpret footage as needed (common: nest Manim clips on a 24p timeline with frame blending off).
2. Build **VO spine first** (scratch or final from `audio/final/`).
3. Lay Manim clips from `edit/renders/{teaser,deepdive}/videos/.../` on upper tracks; slip edits to hit stress words.
4. Drop `SKIP_RENDER` placeholders: camera MP4 for scene 2, screen capture for scene 13.

## Loudness

- Dialog **~-18 LUFS** integrated; music bed **~-22 LUFS** under VO; duck music **12–18 dB** under VO during dense explanation.

## Captions

- Whisper-large (or Resolve transcription) → hand-fix **α**, **√**, **n²**, model names.
- Follow [DESIGN.md §6](../DESIGN.md) for burned-in social cuts; YouTube gets `.srt`.

## Delivery masters

| Output | Spec |
| ------ | ---- |
| Archive | 4K H.265, 16:9, deep-dive long-form |
| YouTube primary | 1080p H.264, 16:9 |
| Teaser social | 1080×1080 (X / IG), 1080×1920 (Shorts / Reels / TikTok) — safe areas in [DESIGN.md §7](../DESIGN.md) |

## Compression for X

- Teaser embed: keep **under ~20 MB** for Twitter/X if uploading directly (re-encode with ffmpeg if needed).
