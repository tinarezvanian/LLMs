# Runbook — Phase 6 (edit + ship)

## DaVinci Resolve (assembly)

1. Create timeline at **24 fps** for on-cam; Manim renders are **60 fps** at production `-qh` — conform or interpret footage as needed (common: nest Manim clips on a 24p timeline with frame blending off).
2. Build **VO spine first** (scratch or final from `audio/final/`).
3. Lay Manim clips from `edit/renders/{teaser,deepdive}/videos/.../` on upper tracks; slip edits to hit stress words. **Shortcut:** the per-track stitched previews already exist as picture-lock references — `edit/renders/teaser/_concat/teaser-1080p60.mp4` (~29s, all 6 scenes back-to-back) and `edit/renders/deepdive/_concat/deepdive-1080p60.mp4` (~79s, 12 Manim scenes; on-cam + screen-cap fill the gap to ~11min). Regenerate with `make concat` after any re-render.
4. Drop `SKIP_RENDER` placeholders: camera MP4 for scene 2, screen capture for scene 13.

## Loudness

- Dialog **~-18 LUFS** integrated; music bed **~-22 LUFS** under VO; duck music **12–18 dB** under VO during dense explanation.

## Captions

- Whisper-large (or Resolve transcription) → hand-fix **α**, **√**, **n²**, model names.
- Follow [DESIGN.md §6](../DESIGN.md) for burned-in social cuts; YouTube gets `.srt`.

## Delivery masters

| Output | Spec | Source |
| ------ | ---- | ------ |
| Archive | 4K H.265, 16:9, deep-dive long-form | DaVinci timeline |
| YouTube primary | 1080p H.264, 16:9 | DaVinci timeline |
| Teaser 1:1 | 1080×1080 (X / IG) | start from `edit/renders/teaser/_concat/teaser-1x1-1080.mp4` (silent center-crop) and add VO/captions in DaVinci |
| Teaser 9:16 | 1080×1920 (Shorts / Reels / TikTok) — safe areas in [DESIGN.md §7](../DESIGN.md) | start from `edit/renders/teaser/_concat/teaser-9x16-1080.mp4` (silent letterbox on the SubQ background; CTA-safe upper third) and add VO/captions in DaVinci |

`make socials` regenerates the silent 1:1 + 9:16 cuts from the latest `make concat` output. Both intentionally have no audio: the editor's VO mix is the only source of truth.

## Compression for X

- Teaser embed: keep **under ~20 MB** for Twitter/X if uploading directly (re-encode with ffmpeg if needed).
