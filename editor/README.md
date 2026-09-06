# Browser logo editor

A static page. No server, no build step, no dependencies: three files of plain
JavaScript and CSS plus the two artwork files. Serve the site and open
`/editor/`.

## What a visitor can do

- Pick the English or Kannada lockup
- Show the crown circle as the centre one, all three, or none
- Pick a colourway, or set Sun / Sun edge / Disc / Line art / Accent by hand
- Pick a background: none, paper, cherry, gold, or any colour
- Pick an artboard: square, Instagram post, story, profile picture, Facebook
  cover, A4 portrait or landscape, A3 poster, business card, or a custom size
- Size the mark with the slider and drag it into place
- Download **PDF**, **PNG** or **SVG**

## Files

| File | What it is |
|---|---|
| `index.html` | the page |
| `editor.css` | editor shell only; tokens, fonts and the nav come from `../css/main.css` |
| `editor.js` | state, controls, PNG and SVG export |
| `svg2pdf.js` | the PDF writer, standalone and reusable |
| `art/*.svg` | base artwork, generated |
| `scripts/build_editor_art.py` | regenerates `art/` from `../vector/` |

## The PDF is real vector art

`svg2pdf.js` walks the live SVG and writes a PDF by hand: paths become PDF path
operators, radial gradients become PDF type 3 shadings with a stitching
function over the stops, and the content stream is Flate compressed with
`CompressionStream` (falling back to uncompressed where that is missing). An A4
page comes out around 290KB and stays sharp at any size a printer asks for.

It covers exactly what this artwork uses: filled paths, flat and radial-gradient
fills, no strokes, no text, no images. Arc segments throw rather than being
drawn wrong; the trace has none.

Two things worth knowing:

- **PDF pages have no transparency.** With the background set to none, the mark
  prints straight onto the paper. That is usually what you want for print; for a
  transparent asset use the PNG or SVG.
- **Colour is RGB.** A commercial printer wanting CMYK separations should
  convert, or ask for the source SVG.

## Regenerating the artwork

```bash
python3 editor/scripts/build_editor_art.py
```

Same trace as `../tenth-edition/`, except the three crown circles are lifted
into `crown-side` and `crown-center` groups so the editor can toggle them, and
the layer fills are left on the neutral trace colours for the editor to set.
Layer order is `ring`, `dotpatch`, `head`, `ink`, `text`, `crown-side`,
`crown-center`.

## Not there yet

- No caption or extra text. Adding Kannada text to a PDF means embedding and
  subsetting a font, which is a much bigger piece of work than the rest of this
  put together.
- Colourway names stay in English when the UI is in Kannada, because they match
  the downloaded file names.
