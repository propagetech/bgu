# Bellandur Ganesha Utsava - assets rebuilt from the ORIGINAL vector artwork

Source: `../original-files/` (native Adobe Illustrator PDFs, 100% vector, zero
embedded raster). These supersede the auto-traced approximations in `../vector/`.

## What the originals are

| File | Edition | Contents |
|---|---|---|
| `Bellandur Ganesh Festival.pdf` | 8th | Ganesha head mark ALONE - no sun, no text. 5 fills. |
| `Bellandur Ganesh Festival 2024.pdf` | 8th | Full Kannada lockup: mark + brush sun + Kannada wordmark |
| `BELLANDUR GANESHA UTSAVA.pdf` | 6th | Full English lockup: mark + brush sun + Latin wordmark |

Important: the JPEGs we had been rebuilding (`../kannada.jpeg`, `../english.jpeg`)
are the **10th** edition, a later redraw. These PDFs are the 6th and 8th. See
"What still has to be redrawn" below.

## Original brand palette, as authored (CMYK in the artwork)

| Role | CMYK | Hex |
|---|---|---|
| disc - inner sun | 0.011 0.123 0.873 0 | `#FAD823` |
| mid - sun brush | 0.002 0.407 0.986 0 | `#F79B11` |
| outer - brush wisps | 0 0.725 0.963 0 | `#F25620` |
| ink - line art + main word | 1 0.881 0.410 0.441 | `#182543` |
| accent - second word + dots | 0.091 0.986 1 0.017 | `#D92025` |

## Cherry red + gold schemes applied

| Role | cherry-gold | gold-dominant | cherry-reversed (dark grounds) |
|---|---|---|---|
| disc | `#F2DFA8` | `#F5E3B0` | `#8E1024` |
| mid | `#D4AF37` | `#D4AF37` | `#6B0F1E` |
| outer | `#C41E3A` | `#A67C1A` | `#C41E3A` |
| ink | `#7E0B21` | `#7E0B21` | `#E8C25A` |
| accent | `#A31530` | `#C41E3A` | `#F2DFA8` |

Recolour is done at the PDF content-stream level (`k` CMYK operators rewritten as
`rg` RGB), so every original path, curve and outline is preserved exactly.

## Outputs

- `pdf/` - vector masters, text already converted to outlines (no font needed).
  Open these in Illustrator; they are the file to hand a printer or a designer.
- `png/` - 300 dpi transparent PNG, trimmed to the artwork.
- `svg/` - **mark only**. The lockup SVGs are not shipped: poppler's SVG writer
  corrupts the outlined lettering (letters collapse onto each other), while the
  same PDFs rasterise perfectly. To get lockup SVGs, open the PDF in Illustrator
  and Save As SVG. The mark SVGs are clean (5 paths) and verified in-browser.

## The brush-stroke sun, on its own

`scripts/extract_sun.py` lifts the sun out of the original PDF as true vector:
742 filled paths in three tonal layers (`sun-outer`, `sun-mid`, `sun-disc`),
no tracing anywhere. The same drawing appears in both the 6th and the 8th
edition files (742 and 740 paths, same shape, different placement), so there
is only one native brush sun.

| File | What it is |
|---|---|
| `svg/sun-brush.svg` | the whole sun, colours as authored |
| `svg/sun-ring.svg` | the brush ring, solid centre dropped |
| `svg/sun-ring-<scheme>.svg` | the ring in each house scheme |
| `svg/sun-face.svg` | **gap-free background**: the sun with the elephant face in it |
| `svg/sun-face-plain.svg` | the same, without the edition vignette |
| `svg/sun-face-plain-<scheme>.svg` | that, in each house scheme |

Two things to know before reusing it:

- **It is cut around the Ganesha.** The mark's line art is knocked OUT of the
  brush paths, so the ring on its own has elephant-shaped gaps in it. That is
  what `sun-face.svg` is for, below.
- **It is not the 10th-edition sun.** The 10th edition uses a later redraw. We
  checked: rasterise the traced 10th-edition ring against this one and search
  over scale, rotation and offset, and the best overlap is IoU 0.33 (identical
  art would score above 0.85). This brush covers about 30% more area and is
  more open and calligraphic. Swapping it into `editor/art/` changes the mark;
  it does not sharpen the current one.

### Filling the gaps: `sun-face.svg`

The 8th-edition file carries the sun and the elephant face on one page, already
in register. Keep both, drop the Kannada wordmark, and every gap is filled by
construction rather than by fitting: no alignment guesswork, no seams. The
result is a complete circular background with an empty disc in the middle,
ready for whatever mark or lettering goes on top.

Three things are cleaned up on the way through:

- **Extraction artefacts.** Three lone `re` rectangles come through the parser
  that do not render in the source. The artwork is lines and cubics only, so a
  path that is a single rectangle is dropped.
- **A vestigial "GANESH".** The solid disc still carries a knock-out of a Latin
  wordmark from an earlier version, showing as hairline seams. Splitting that
  one path into its 237 subpaths fills the holes and leaves the brushed edge
  untouched.
- **The wordmark.** The Kannada lettering sits in a known central box and the
  face never does, so a box test separates them.

`sun-face.svg` keeps the skydiver holding an "8th" balloon, as authored.
`sun-face-plain.svg` drops that vignette, which is the one to use anywhere the
edition number would be wrong.

These are masters, around 370KB each and not on the publish list in
`build.sh`. Anything that ships to the browser wants a pass through an SVG
optimiser first.

## What still has to be redrawn for the 10th edition

These originals do NOT contain the 10th-edition design. Still outstanding:

- 10th-edition Kannada lettering (heavier, black-and-cherry, different face)
- 10th-edition English lockup (inscriptional serif with swash G / S / N)
- 10th-edition ears, three-dot crown, and the bottom ornament

The font-identification and redraw work in `../font-match/` therefore still stands.
What these originals DO give us for free: the brush-stroke sun (the single hardest
element to trace, now true vector), the exact palette above, and a clean vector
Ganesha mark in the same design lineage.

## Regenerating

`scripts/recolor.py` rebuilds `pdf/` from `../original-files/` for any scheme.
`scripts/extract_sun.py` rebuilds the `svg/sun-*.svg` set from the same source.
Both need only PyMuPDF.
