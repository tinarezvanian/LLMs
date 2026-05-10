# EB Garamond (SIL Open Font License)

Static `.ttf` files expected by `preamble.tex` (paths match **Algorithmic Adventures**):

| File | Source |
|------|--------|
| `EBGaramond-Regular.ttf` | `octaviopardo/EBGaramond12`, `fonts/ttf/` |
| `EBGaramond-Italic.ttf` | same |
| `EBGaramond-Bold.ttf` | same |
| `EBGaramond-BoldItalic.ttf` | same |

`OFL.txt` is copied from the same upstream repository.

Download when vendoring:

```bash
BASE=https://raw.githubusercontent.com/octaviopardo/EBGaramond12/master/fonts/ttf
for f in EBGaramond-Regular.ttf EBGaramond-Italic.ttf EBGaramond-Bold.ttf EBGaramond-BoldItalic.ttf; do
  curl -fsSL -o "$f" "$BASE/$f"
done
curl -fsSL -o OFL.txt https://raw.githubusercontent.com/octaviopardo/EBGaramond12/master/OFL.txt
```
