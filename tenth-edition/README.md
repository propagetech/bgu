# Bellandur Ganesha Utsava - 10th edition, cherry red + gold

Vector redraw of the 10th-edition lockups (`../kannada.jpeg`, `../english.jpeg`),
with the requested edits applied and recoloured to cherry red + gold.

## Edits applied

1. **Crown dots removed.** The black / red / black circle cluster above the
   headdress arcs is gone from both lockups. Two black dots came out of the `ink`
   layer and the red centre dot out of the `text` layer.
2. **White keyline halos patched.** Each dot sat in a white keyline that was a gap
   in the traced sun. Left alone it would have shown as three white blobs. A
   `dotpatch` layer sits above the sun ring and below the disc, filled from a
   user-space copy of the ring gradient so it blends with no seam.
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

- `*.svg` - the deliverable. Four layers: `ring`, `dotpatch`, `head`, `ink`, `text`.
  Verified rendering in-browser.
- `png/` - transparent, trimmed, ~1820px.
- `contact-sheet.png` - all six side by side.
- `scripts/` - `build10.py` regenerates everything from `../vector/*-original.svg`;
  `pathlib2.py` is the path normaliser it uses.

`*-original-nodots` is the original orange/yellow colourway with the dots removed,
kept so you can compare the edit independently of the recolour.

## Provenance

The 10th-edition base trace came from the earlier session (`../vector/`). It is a
four-colour-layer trace of the JPEGs, which is why edits are done by selecting
subpaths geometrically rather than by editing named objects. The genuinely native
vector artwork we have (`../vector-native/`) is the 6th and 8th editions, a
different design - see that folder's README.
