# Fonts (SIL Open Font License)

The book is set in **Alegreya Sans** (Juan Pablo del Peral). The TTFs were
copied from `LLMs/docs/Alegreya_Sans/`, where the upstream OFL.txt also lives.
**Manim** (`vid/theme.py`) loads the same `AlegreyaSans-*.ttf` files from
`docs/Alegreya_Sans/`, this directory, or `assets/branding/fonts/Alegreya_Sans/`
when present, so on-screen type can match the PDF.
EB Garamond TTFs are kept as a fallback for anyone wanting to flip the
preamble back to the original Algorithmic Adventures look.

## Active font (Alegreya Sans)

| File | Used as |
|------|---------|
| `AlegreyaSans-Regular.ttf` | `\setmainfont` upright (body) |
| `AlegreyaSans-Italic.ttf` | italic |
| `AlegreyaSans-Bold.ttf` | bold |
| `AlegreyaSans-BoldItalic.ttf` | bold italic |
| `AlegreyaSans-Light.ttf` / `LightItalic.ttf` | `\AlegreyaLight` running text |
| `AlegreyaSans-Medium.ttf` / `MediumItalic.ttf` | medium weight |
| `AlegreyaSans-Black.ttf` / `BlackItalic.ttf` | `\AlegreyaDisplay` chapter / part titles |

To re-vendor or refresh from the workspace copy:

```bash
cp /Users/ed/Developer/LLMs/docs/Alegreya_Sans/AlegreyaSans-*.ttf .
cp /Users/ed/Developer/LLMs/docs/Alegreya_Sans/OFL.txt .
```

## Fallback (EB Garamond)

Kept around in case the preamble is reverted to the original Algorithmic
Adventures `\setmainfont{EB Garamond}` setup.

| File | Source |
|------|--------|
| `EBGaramond-Regular.ttf` | `octaviopardo/EBGaramond12`, `fonts/ttf/` |
| `EBGaramond-Italic.ttf` | same |
| `EBGaramond-Bold.ttf` | same |
| `EBGaramond-BoldItalic.ttf` | same |

Download:

```bash
BASE=https://raw.githubusercontent.com/octaviopardo/EBGaramond12/master/fonts/ttf
for f in EBGaramond-Regular.ttf EBGaramond-Italic.ttf EBGaramond-Bold.ttf EBGaramond-BoldItalic.ttf; do
  curl -fsSL -o "$f" "$BASE/$f"
done
curl -fsSL -o OFL.txt https://raw.githubusercontent.com/octaviopardo/EBGaramond12/master/OFL.txt
```
