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

## The shape of the page

The editor is an instrument, not a document, and it holds to two rules at every
size:

1. **The artwork never leaves the screen.** The page itself does not scroll.
   `.editor` is a `100dvh` grid of three rows: the space the site nav floats
   over, the stage, and the tray. Opening a tool takes height *from the stage*
   rather than covering it, so the mark shrinks to make room and you watch the
   edit happen. `layout()` fits the board to `.stage-frame`, and a
   `ResizeObserver` on that frame re-fits it on every frame of the sheet
   animation, so the artwork tracks the controls exactly.
2. **Export is always one tap away.** It is the fifth, primary slot in the dock,
   which is fixed. You never scroll, or hunt, to download.

Nineteen controls were grouped into four tools plus Export, named for what you
are changing rather than for the widget: **Mark** (lockup, crown circles),
**Colour** (colourway, the five pickers), **Canvas** (artboard, background),
**Place** (size, fit, centre), **Export** (PDF, PNG, SVG, PNG size). A
colourway swatch is a miniature of the mark itself, so the choice previews its
own result.

The tray goes where the space is. Tall windows get it along the bottom; wide
ones lay each sheet's fields out in two columns so the tray is shorter and the
artwork bigger; a landscape phone, which has width to spare and almost no
height, moves the whole tray to the right-hand side. It is one object answering
the shape of the window, not three layouts.

Verified at 320x568, 360x640, 375x812, 390x844, 414x896, 768x1024, 844x390,
932x430, 1024x768, 1280x800, 1440x900 and 1920x1080, in both themes and both
languages: the page never scrolls, the dock is always on screen, and the
artwork is never covered by the controls.

## Files

| File | What it is |
|---|---|
| `index.html` | the page |
| `editor.css` | editor shell only; tokens, fonts and the nav come from `../css/main.css` |
| `editor.js` | state, the tool dock, layout fitting, PNG and SVG export |
| `svg2pdf.js` | the PDF writer, standalone and reusable |
| `art/*.svg` | base artwork, generated |
| `scripts/build_editor_art.py` | regenerates `art/` from `../vector/` and the native sun |

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

The `ring` is the exception: it is not traced. It comes from the native
Illustrator original via `../vector-native/scripts/extract_sun.py`, so the
brush is real vector rather than an auto-trace of a JPEG. Two details make
that work, both explained in the build script:

- The brush has the Ganesha knocked out of it, leaving elephant-shaped gaps.
  The 8th-edition file carries that same elephant in register on the same page,
  so painting it back in with the ring's own gradient fills each gap with
  exactly the colour its surroundings already have.
- The native sun is drawn tighter around its own mark than the 10th-edition
  disc is, so `SUN_SCALE` opens it out until the disc no longer escapes past
  the brush on any of 720 sampled rays, for both lockups.

The fit is baked into the coordinates rather than carried on a nested
transform, so the group still looks like every other layer: one transform, one
`url(#ringG)` fill, flat `<path>` children. That keeps the gradient correct and
keeps `svg2pdf.js`, which reads only top-level groups, working unchanged.

## Not there yet

- No caption or extra text. Adding Kannada text to a PDF means embedding and
  subsetting a font, which is a much bigger piece of work than the rest of this
  put together.
- Colourway names stay in English when the UI is in Kannada, because they match
  the downloaded file names.
