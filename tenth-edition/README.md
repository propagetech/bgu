# Bellandur Ganesha Utsava - 10th edition, cherry red + gold

Vector redraw of the 10th-edition lockups (`../kannada.jpeg`, `../english.jpeg`),
with the requested edits applied and recoloured to cherry red + gold.

## Edits applied

1. **Crown circle: centre only.** The original had a black / red / black cluster
   above the headdress arcs. The two flanking black dots are gone (they came out
   of the `ink` layer); the red centre circle stays, at the middle top.
2. **White keyline patched.** Each circle sat in a white keyline that is a notch
   in the traced disc outline, not a subpath of its own. Left alone the two
   removed dots would have shown as white blobs. A `dotpatch` layer sits above
   the sun ring and below the disc, painted with the same sun gradient. The sun
   gradient is `userSpaceOnUse`, so the patch resolves it identically to the ring
   path and leaves no seam.
3. **Bottom ornament kept** in both. See the note below.
4. **Recoloured** to cherry red + gold.

## Ornament note - please confirm

You asked to use the ornament symbol in the bottom middle from `kannada.jpeg`.
That ornament is **already present, and identical in design, in both lockups** -
the same scroll flourish with tapered rules and dots. The Kannada one is drawn
slightly narrower; the English one sits above `• 2026 •`. Nothing was changed
there. If you meant something else - move it to where the dots were, resize the
English one to match the Kannada proportion, or drop the `2026` line - say which
and it is a small change.

## Palette

| Role | cherry-gold | cherry-reversed (dark grounds) |
|---|---|---|
| sun ring, inner | `#E8C86B` | `#A81528` |
| sun ring, mid | `#D4AF37` | `#C41E3A` |
| sun ring, outer | `#C2922E` | `#9E1229` |
| sun ring, rim | `#C41E3A` -> `#A31530` | `#6B0F1E` |
| disc | `#FDF7E4` -> `#F1DC9E` | `#8E1024` -> `#6B0F1E` |
| ink - line art, GANESHA / ಗಣೇಶ | `#6B0F1E` | `#E8C25A` |
| accent - BELLANDURU / UTSAVA | `#C41E3A` | `#F2DFA8` |

## Files

- `*.svg` - the deliverable. Layers: `ring`, `dotpatch`, `head`, `ink`, `text`.
  Verified rendering in-browser.
- `png/` - transparent, trimmed, ~1660px.
- `contact-sheet.png` - all six side by side.
- `scripts/build10.py` - regenerates the SVGs from `../vector/*-original.svg`.
  `CROWN` selects `"all"`, `"center"` (shipped) or `"none"` for the crown circles.
  `render.py` rasterises them, `contact_sheet.py` builds the sheet.
  `pathlib2.py` is the path normaliser `build10.py` uses.

`*-original` is the original orange / yellow colourway, same edit, kept so you can
compare the edit independently of the recolour.

The same three colourways plus eleven more finishes are in `../variants/`.

## Provenance

The 10th-edition base trace came from the earlier session (`../vector/`). It is a
four-colour-layer trace of the JPEGs, which is why edits are done by selecting
subpaths geometrically rather than by editing named objects. The genuinely native
vector artwork we have (`../vector-native/`) is the 6th and 8th editions, a
different design - see that folder's README.
