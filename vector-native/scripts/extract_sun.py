"""Lift the brush-stroke sun out of the native Illustrator originals.

The sun is 100% vector in `../original-files/`: 742 filled paths in three
tonal layers, drawn once and reused in both the 6th and the 8th edition files.
Nothing here is traced.

    python3 vector-native/scripts/extract_sun.py

writes, into `../svg/`:

  sun-brush.svg       the whole sun, three layers, colours as authored
  sun-ring.svg        the brush ring only, with the solid centre dropped
  sun-ring-<scheme>.svg   the ring in each house scheme

  sun-face.svg        the gap-free background: sun + elephant face
  sun-face-plain.svg  the same without the edition vignette
  sun-face-plain-<scheme>.svg   that, in each house scheme

Layer ids are `sun-outer`, `sun-mid`, `sun-disc`, outermost first, plus
`face-ink` and `face-accent`, so a consumer can recolour or drop a layer
without touching path data.

## Why there is a sun-face at all

The brush is cut around the Ganesha: the mark's line art is knocked OUT of the
sun paths, so the ring on its own has elephant-shaped gaps in it. The 8th
edition file carries the sun and that same mark on one page, already in
register, so dropping the Kannada wordmark and keeping everything else fills
every gap exactly, by construction rather than by fitting.

Three things are cleaned up on the way through:

- Extraction artefacts. Three lone `re` rectangles come through the parser that
  do not render in the original. Real artwork here is only lines and cubics, so
  any path that is a single rectangle is dropped.
- A vestigial "GANESH". The solid disc still carries a knock-out of a Latin
  wordmark from some earlier version, showing as hairline seams. Splitting that
  one path into its subpaths fills the holes and leaves the brushed edge alone.
- The wordmark. The Kannada lettering sits in a known central box and the face
  never does, so a box test separates them.

Note on editions: this is the 6th/8th-edition brush and the 8th-edition face. The 10th-edition mark in
`../../vector/` and `../../editor/art/` uses a LATER redraw of the sun, a
different drawing (best-case overlap with this one is about a third). Treat
this as its own asset, not as a sharper copy of the current one.
"""
import math
import os

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "svg")
ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(ROOT, "original-files", "BELLANDUR GANESHA UTSAVA.pdf")
PAGE = 0
# The 8th-edition file: the same sun, with the elephant face in register on it.
SRC_FACE = os.path.join(ROOT, "original-files", "Bellandur Ganesh Festival 2024.pdf")
PAGE_FACE = 0
SIDE = 1000.0                      # the square viewBox we normalise into

# The three sun colours as authored, outermost first. Anything else on the
# page is the Ganesha mark or the wordmark and is left behind.
LAYERS = [
    ("outer", (0.951, 0.417, 0.154), "#F26A27"),
    ("mid",   (0.978, 0.645, 0.117), "#F9A51E"),
    ("disc",  (0.991, 0.850, 0.227), "#FDD93A"),
]

# For `sun-ring.svg`: in the innermost layer only, drop anything nearer the
# centre than this fraction of the radius. That is the solid disc plus the
# knock-out of the 6th-edition lettering, neither of which belongs behind a
# different mark. The two brush layers are always kept whole.
RING_INNER = 0.45
RING_TRIMS = "disc"

# Same roles and hexes as scripts/recolor.py, so the two agree.
SCHEMES = {
    "cherry-gold":     {"disc": "#F2DFA8", "mid": "#D4AF37", "outer": "#C41E3A",
                        "ink": "#7E0B21", "accent": "#A31530"},
    "gold-dominant":   {"disc": "#F5E3B0", "mid": "#D4AF37", "outer": "#A67C1A",
                        "ink": "#7E0B21", "accent": "#C41E3A"},
    "cherry-reversed": {"disc": "#8E1024", "mid": "#6B0F1E", "outer": "#C41E3A",
                        "ink": "#E8C25A", "accent": "#F2DFA8"},
}

# On the 8th-edition page: the Kannada wordmark lives in this box and the face
# never does; the skydiver holding an "8th" balloon lives in this one.
WORDMARK = (320, 240, 510, 390)
VIGNETTE = (368, 180, 468, 232)
FACE_INK, FACE_ACCENT = "#102448", "#D82427"


def fmt(v, places=3):
    s = f"{v:.{places}f}".rstrip("0").rstrip(".") if places else f"{v:.0f}"
    return "0" if s in ("-0", "", "-0.0") else s


def path_d(items, close, matrix=None, places=3):
    """Serialise one PDF path. The originals use only lines and cubics.

    `matrix` is an optional (a, b, c, d, e, f) affine baked into the
    coordinates, for callers that cannot wrap the result in a transform.
    `places` is the decimals kept; a caller working in a large coordinate
    space wants fewer, and the file gets a lot smaller for it.
    """
    if matrix is None:
        def at(p):
            return fmt(p.x, places) + " " + fmt(p.y, places)
        def pt(p):
            return (p.x, p.y)
    else:
        a, b, c, d, e, f = matrix
        def at(p):
            return (fmt(a * p.x + c * p.y + e, places) + " "
                    + fmt(b * p.x + d * p.y + f, places))
        def pt(p):
            return (a * p.x + c * p.y + e, b * p.x + d * p.y + f)

    out, cur = [], None

    def move(p):
        q = pt(p)
        if cur is None or abs(q[0] - cur[0]) > 1e-6 or abs(q[1] - cur[1]) > 1e-6:
            out.append("M" + at(p))

    for it in items:
        kind = it[0]
        if kind == "l":
            move(it[1])
            out.append("L" + at(it[2]))
            cur = pt(it[2])
        elif kind == "c":
            move(it[1])
            out.append("C" + at(it[2]) + " " + at(it[3]) + " " + at(it[4]))
            cur = pt(it[4])
        elif kind == "re":
            r = it[1]
            corners = [fitz.Point(r.x0, r.y0), fitz.Point(r.x1, r.y0),
                       fitz.Point(r.x1, r.y1), fitz.Point(r.x0, r.y1)]
            out.append("M" + at(corners[0]) + "".join("L" + at(c) for c in corners[1:]) + "Z")
            cur = None
        elif kind == "qu":
            q = it[1]
            out.append("M" + at(q.ul) + "L" + at(q.ur) + "L" + at(q.lr) + "L" + at(q.ll) + "Z")
            cur = None
        else:                                    # nothing else occurs in these files
            raise ValueError("unhandled path item: " + kind)
    if close:
        out.append("Z")
    return "".join(out)


def extract(src=SRC, page_no=PAGE):
    """Return the sun's paths per layer, in a centred 0..SIDE square."""
    want = {tuple(round(c, 3) for c in rgb): name for name, rgb, _ in LAYERS}
    page = fitz.open(src)[page_no]

    raw, box = [], fitz.Rect()
    for p in page.get_drawings():
        if p["type"] not in ("f", "fs"):
            continue
        name = want.get(tuple(round(x, 3) for x in (p["fill"] or ())))
        if name:
            raw.append((name, p))
            box |= p["rect"]

    scale = SIDE / max(box.width, box.height)
    dx = SIDE / 2 - (box.x0 + box.x1) / 2 * scale
    dy = SIDE / 2 - (box.y0 + box.y1) / 2 * scale
    cx, cy = (box.x0 + box.x1) / 2, (box.y0 + box.y1) / 2
    radius = max(box.width, box.height) / 2

    out = {name: [] for name, _, _ in LAYERS}
    for name, p in raw:
        r = p["rect"]
        near = min(max(cx, r.x0), r.x1), min(max(cy, r.y0), r.y1)
        inner = math.hypot(near[0] - cx, near[1] - cy) / radius
        out[name].append({
            "d": path_d(p["items"], p["closePath"]),
            "even_odd": p["even_odd"],
            "inner": inner,
        })
    return out, (scale, dx, dy)


def render(groups, fit, fills, ring_only):
    scale, dx, dy = fit
    body = []
    for name, _, native in LAYERS:
        trim = ring_only and name == RING_TRIMS
        items = [it for it in groups[name]
                 if not (trim and it["inner"] < RING_INNER)]
        if not items:
            continue
        nz = [it["d"] for it in items if not it["even_odd"]]
        eo = [it["d"] for it in items if it["even_odd"]]
        inner = "".join(f'<path d="{d}"/>' for d in nz)
        if eo:
            inner += '<g fill-rule="evenodd">' + "".join(f'<path d="{d}"/>' for d in eo) + "</g>"
        body.append(f'<g id="sun-{name}" fill="{fills.get(name, native)}">{inner}</g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(SIDE)} {fmt(SIDE)}" '
            f'width="{fmt(SIDE)}" height="{fmt(SIDE)}">'
            f'<g transform="translate({fmt(dx)} {fmt(dy)}) scale({scale:.6f})" stroke="none">'
            + "".join(body) + "</g></svg>")


def background(src=SRC_FACE, page_no=PAGE_FACE, matrix=None, places=3):
    """Sun and elephant face from one page, so the gaps are filled by register.

    Returns the sun layers, the face paths tagged ink/accent and whether each
    belongs to the edition vignette, and the sun's bounding box.
    """
    sun_of = {tuple(round(c, 3) for c in rgb): name for name, rgb, _ in LAYERS}
    page = fitz.open(src)[page_no]
    page_box = fitz.Rect(page.rect)
    word, vig = fitz.Rect(*WORDMARK), fitz.Rect(*VIGNETTE)

    sun = {name: [] for name, _, _ in LAYERS}
    face, box = [], fitz.Rect()
    for p in page.get_drawings():
        if p["type"] not in ("f", "fs"):
            continue
        r = p["rect"]
        # the originals are lines and cubics only; a lone rectangle is a parser
        # artefact and does not render in the source
        if not page_box.contains(r) or (len(p["items"]) == 1 and p["items"][0][0] == "re"):
            continue
        d, eo = path_d(p["items"], p["closePath"], matrix, places), p["even_odd"]
        layer = sun_of.get(tuple(round(x, 3) for x in (p["fill"] or ())))
        if layer:
            if layer == "disc" and d.count("M") > 200:
                # the solid disc: split its subpaths to fill the vestigial
                # wordmark knock-out without touching the brushed edge
                sun[layer] += [("M" + part, False) for part in d.split("M")[1:]]
            else:
                sun[layer].append((d, eo))
            box |= r
        elif not word.contains(r):
            role = "accent" if p["fill"][0] > 0.7 else "ink"
            face.append((d, eo, role, vig.contains(r)))
    return sun, face, box


def render_background(sun, face, box, fills, drop_vignette):
    parts = []
    for name, _, native in LAYERS:
        parts.append(layer_svg(f"sun-{name}", fills.get(name, native), sun[name]))
    for role, native in (("ink", FACE_INK), ("accent", FACE_ACCENT)):
        items = [(d, eo) for d, eo, r, v in face
                 if r == role and not (drop_vignette and v)]
        if items:
            parts.append(layer_svg(f"face-{role}", fills.get(role, native), items))
    pad = 6
    vb = (f"{fmt(box.x0 - pad)} {fmt(box.y0 - pad)} "
          f"{fmt(box.width + 2 * pad)} {fmt(box.height + 2 * pad)}")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" '
            f'stroke="none">' + "".join(parts) + "</svg>")


def layer_svg(gid, fill, items):
    """One tonal layer. `fill` of None leaves the colour to the parent group."""
    nz = [d for d, e in items if not e]
    eo = [d for d, e in items if e]
    inner = "".join(f'<path d="{d}"/>' for d in nz)
    if eo:
        inner += '<g fill-rule="evenodd">' + "".join(f'<path d="{d}"/>' for d in eo) + "</g>"
    paint = "" if fill is None else f' fill="{fill}"'
    return f'<g id="{gid}"{paint}>{inner}</g>'


def main():
    os.makedirs(OUT, exist_ok=True)
    groups, fit = extract()
    counts = {k: len(v) for k, v in groups.items()}
    kept = {k: sum(1 for it in v if k != RING_TRIMS or it["inner"] >= RING_INNER)
            for k, v in groups.items()}
    print("extracted", counts, "-> ring keeps", kept)

    jobs = [("sun-brush.svg", {}, False), ("sun-ring.svg", {}, True)]
    jobs += [(f"sun-ring-{name}.svg", fills, True) for name, fills in SCHEMES.items()]
    for name, fills, ring_only in jobs:
        write(name, render(groups, fit, fills, ring_only))

    sun, face, box = background()
    print("background: sun", {k: len(v) for k, v in sun.items()},
          "face", len(face), "of which vignette", sum(1 for f in face if f[3]))
    write("sun-face.svg", render_background(sun, face, box, {}, False))
    write("sun-face-plain.svg", render_background(sun, face, box, {}, True))
    for name, fills in SCHEMES.items():
        write(f"sun-face-plain-{name}.svg", render_background(sun, face, box, fills, True))


def write(name, svg):
    open(os.path.join(OUT, name), "w").write(svg)
    print(f"  {name:30s} {len(svg):7d} bytes")


if __name__ == "__main__":
    main()
