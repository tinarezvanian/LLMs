# Optional fonts (EB Garamond)

To match the Algorithmic Adventures book typography, download **EB Garamond** (OFL) and place:

- `EBGaramond-Regular.ttf`
- `EBGaramond-Italic.ttf`
- `EBGaramond-Bold.ttf`
- `EBGaramond-BoldItalic.ttf`

in this directory, then switch `preamble.tex` to `fontspec` + `Path = ./fonts/` as in the upstream
`Algorithmic_Adventures/preamble.tex`.

The default build uses Latin Modern and does not require this folder.
