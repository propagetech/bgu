# Ganesha Utsava logo — font identification and redraw

## 1. Font identification

**Method.** Each letter's outline was extracted from the logo, normalised into a
fixed box, and matched against every glyph of every candidate font — letter by
letter, not word by word, so the designer's tracking cannot distort the result.
The matcher is encoding-independent, which is what made the 172 legacy Nudi
fonts testable without knowing their code pages.

**Calibration.** "BELLANDURU" set in Cinzel Bold was fed through the pipeline as
a control: it returned Cinzel at 1.00 on all ten letters, with the Cormorant
family as runners-up. A true match therefore scores 1.00.

**Pools searched**

| script | files | glyphs | coverage |
|---|---|---|---|
| Kannada | 224 | 86,139 | all 10 Google Kannada families (every weight), macOS Kannada MN + Kannada Sangam MN, Gubbi, Navilu, Cheluvi, Ambarisha, Kittel, Padyakke, 172 Nudi fonts |
| Latin | 1,096 | ~39,000 | ~820 Google families — every Display and Serif family with Latin |

### Kannada — matched

**Baloo Tamma 2 ExtraBold (800)**, tracked about **−0.12 em**.

| letter | best matches (weight-normalised IoU) |
|---|---|
| ಗ | Baloo Tamma 2 ExtraBold **0.857**, Noto Sans Kannada Bold 0.825, Anek Kannada Bold 0.806 |
| ಶ | Noto Sans Kannada Medium 0.824, Noto Serif Kannada SemiBold 0.818, Anek Bold 0.796, Baloo Tamma 2 ExtraBold 0.792 |

Baloo Tamma 2 is the only face that wins or near-wins on both letters. Runner-up:
Noto Sans Kannada Bold. The entire Nudi set was tested and lost, so this was
probably not set in the usual Karnataka print fonts.

### Latin — no match found

The ceiling across all ~820 families is **0.79**, against 1.00 for a known match.
The fonts that reach that ceiling (Big Shoulders, Caacupe One, Koulen) are
condensed *sans* faces winning on proportion alone — they have no serifs. That is
what "no match" looks like in this data.

The logo's Latin is a bold condensed inscriptional roman with small wedge serifs.
GANESHA is the same genre with swash alternates — spiral terminals on the G and
S, a descending swash tail on the N — which points to a specific decorative
family, most likely commercial rather than open source.

Closest open substitutes, none exact: **Cinzel Bold/Black** (right genre and
weight, wider), Marcellus (right serif style, too light), Amarante (right flare
and weight, more Art Nouveau), BIZ UDMincho Bold (right weight, Mincho serifs).

Incidental: the two lockups do not share numerals. The Kannada "10" is a bold
grotesque; the English "10th" is a serif.

## 2. Redraw

Every lettering contour was rebuilt two ways and the more faithful kept:

- **font-guided warp** — the base font glyph (Cinzel / Baloo Tamma 2) affinely
  aligned, then deformed onto the traced letter with a low-pass-filtered
  displacement field, then refitted;
- **direct refit** — de-serration, corner detection, Schneider least-squares
  cubic fitting, then near-linear segments forced to exact straight lines.

**Measured head-to-head** on UTSAVA (max deviation from the traced original):

| letter | warp rms / max / nodes | refit rms / max / nodes |
|---|---|---|
| U | 0.76 / 2.12 px / 18 | **0.25 / 0.98 px / 30** |
| T | 0.75 / 2.42 px / 18 | **0.25 / 0.94 px / 25** |
| S | 1.03 / 3.77 px / 14 | **0.30 / 0.96 px / 28** |
| A | 0.75 / 4.26 px / 21 | **0.28 / 0.88 px / 33** |
| V | 0.86 / 2.20 px / 14 | **0.34 / 0.95 px / 23** |

The direct refit is ~3x more faithful at comparable node counts, so it won every
contour in both lockups. The font base cannot beat the trace on fidelity by
construction — the trace already carries all the shape information — and its
regularisation benefit is delivered instead by the straightening pass.

**Result** (max deviation from the original, per wordmark):

| wordmark | contours | rms | max | beziers |
|---|---|---|---|---|
| EN GANESHA | 11 | 0.31 px | 0.99 px | 324 |
| EN BELLANDURU | 15 | 0.36 px | 0.98 px | 248 |
| EN UTSAVA | 8 | 0.33 px | 0.99 px | 171 |
| EN 10th | 5 | 0.32 px | 0.97 px | 66 |
| EN 2026 | 8 | 0.49 px | 0.98 px | 55 |
| KN ಗಣೇಶ | 5 | 0.34 px | 0.98 px | 191 |
| KN ಬೆಳ್ಳಂದೂರು | 6 | 0.36 px | 0.97 px | 67 |
| KN ಉತ್ಸವ | 3 | 0.35 px | 0.98 px | 134 |
| KN 10ನೇ | 6 | 0.39 px | 1.00 px | 76 |

Verification: both files rendered at 2000px against the raw trace and diffed.
Every differing pixel disappears under a 5px erosion, so no feature moved,
merged or vanished — the differences are edge slivers only.

The GANESHA swashes (G spiral, S spiral, N tail) are preserved exactly; they came
through the refit path, which reads them from the trace rather than from a font.

## 3. Files

- `vector/*.svg` — redrawn, all four variants share identical geometry
- `vector/_raw-trace/` — the original autotraces, untouched
- `fonts/` — Baloo Tamma 2 (700/800), Cinzel (700/900), Noto Sans Kannada 700,
  as woff2 + ttf, for supporting collateral
- `font-match/*.py` — the pipeline, re-runnable: `python3 produce.py english out.svg`
