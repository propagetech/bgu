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
