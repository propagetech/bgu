# Colour and finish treatments

Fourteen treatments per lockup, both rebuilt from the same 10th-edition vector
that `../tenth-edition/` ships, so the artwork is identical across the set:
crown circle at centre top only, bottom ornament kept, `• 2026 •` line kept.

Everything here is generated. Run `python3 scripts/build_variants.py` to rebuild.

| # | Treatment | Notes |
|---|---|---|
| 01 | cherry-gold | the approved primary. Cream disc, cherry ink |
| 02 | gold-cherry | gold-forward: gold ring and disc, cherry ink |
| 03 | cherry-gold-dark | reversed colourway on a near-black ground |
| 04 | gold-dark | gold on a near-black ground |
| 05 | mono-gold | single-hue gold |
| 06 | mono-cherry | single-hue cherry |
| 07 | mono-black | greyscale, for fax-grade and single-colour print |
| 08 | knockout-cherry | ivory art on flat cherry |
| 09 | knockout-gold | cherry art on flat gold |
| 10 | 3d-cherry-gold | 01 with an extruded edge |
| 11 | 3d-gold-dark | 04 with an extruded edge |
| 12 | 3d-rose-gold | rose colourway with an extruded edge |
| 13 | bevel-gold | 02 with a soft emboss |
| 14 | bevel-cherry-gold | 01 with a soft emboss |

03, 04, 08, 09 and 11 are flattened onto their background colour. The rest are
transparent PNGs, ~1150px on the long edge.

`contact-sheet-english.png` and `contact-sheet-kannada.png` show all fourteen.

Colour is applied in the SVG before rasterising; the 3D and bevel finishes are
raster passes applied after render, in `scripts/build_variants.py`.
