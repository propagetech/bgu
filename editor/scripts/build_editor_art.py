"""Base artwork for the browser editor.

Same trace as ../../tenth-edition, but the three crown circles are lifted into
their own groups so the editor can toggle them, and the layer fills are left on
the neutral trace colours so the editor can set them by group id.

Layer order: ring, dotpatch, head, ink, text, crown-side, crown-center.

The ring is the one layer NOT taken from the trace. It comes from the native
Illustrator original instead, via ../../vector-native/scripts/extract_sun.py:
real brush strokes rather than a lumpy auto-trace of a JPEG.

Two things make that possible:

- The brush has the Ganesha knocked OUT of it, so on its own it has
  elephant-shaped gaps. The 8th-edition file carries that same elephant in
  register on the same page, so painting it back in with the ring's own
  gradient fills every gap with exactly the colour its surroundings already
  have. The holes vanish rather than being covered.
- The native sun is drawn tighter around its own mark than the 10th-edition
  disc is, so at 1:1 the pale disc escapes past the brush on the left and
  right flanks. SUN_SCALE opens the sun out until it contains the disc on all
  720 sampled rays, for both lockups; 1.14 is the first value that does
  (English is clean from 1.10, Kannada needs the extra).
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tenth-edition", "scripts"))
from build10 import REG, HALO, RING, TRANSFORM, circle  # noqa: E402
from pathlib2 import to_abs_subpaths, bbox              # noqa: E402

sys.path.insert(0, os.path.join(ROOT, "vector-native", "scripts"))
from extract_sun import background, layer_svg  # noqa: E402

SRC = os.path.join(ROOT, "vector")
OUT = os.path.join(os.path.dirname(HERE), "art")
INK, ACCENT = "#141414", "#8E1420"
VB = 3762                      # the artwork viewBox, and the trace's 10x space
SUN_SCALE = 1.14               # see the module docstring


def ring_box(svg):
    """The traced ring's footprint, in viewBox units.

    The trace lives in a 10x space with y flipped, so undo that as we go.
    """
    d = re.search(r'<g[^>]*id="ring"[^>]*>\s*<path d="([^"]+)"', svg).group(1)
    xs, ys = [], []
    for sp in to_abs_subpaths(d):
        bb = bbox(sp)
        if bb:
            xs += [bb[0] / 10.0, bb[2] / 10.0]
            ys += [VB - bb[1] / 10.0, VB - bb[3] / 10.0]
    return min(xs), min(ys), max(xs), max(ys)


def native_ring(svg):
    """The native brush sun, gaps filled, fitted where the traced ring sat.

    The fit is baked into the coordinates rather than carried on a nested
    transform, so the group looks exactly like every other layer: one
    TRANSFORM, one `url(#ringG)` fill, flat <path> children. That keeps the
    gradient (userSpaceOnUse, defined in this same 10x space) correct and
    keeps svg2pdf.js, which reads only top-level groups, working unchanged.
    """
    x0, y0, x1, y1 = ring_box(svg)
    scale = SUN_SCALE * min((x1 - x0) / box_of().width, (y1 - y0) / box_of().height)
    box = box_of()
    dx = (x0 + x1) / 2 - (box.x0 + box.x1) / 2 * scale
    dy = (y0 + y1) / 2 - (box.y0 + box.y1) / 2 * scale
    # page space -> the trace's 10x space, y flipped
    matrix = (10 * scale, 0, 0, -10 * scale, 10 * dx, 10 * (VB - dy))

    # one decimal in a 37620-unit space is a ten-thousandth of the artwork
    sun, face, _ = background(matrix=matrix, places=1)
    parts = [layer_svg(f"sun-{n}", None, sun[n]) for n in ("outer", "mid", "disc")]
    # the elephant, painted in the ring's own gradient, so the gaps close
    parts.append(layer_svg("sun-fill", None,
                           [(d, eo) for d, eo, _role, vignette in face if not vignette]))
    return (f'<g {TRANSFORM} fill="url(#ringG)" stroke="none" id="ring">'
            + "".join(parts) + "</g>")


_BOX = []


def box_of():
    """The native sun's bounding box in page space, read once."""
    if not _BOX:
        _BOX.append(background()[2])
    return _BOX[0]


def split_crown(svg, name):
    """Move the crown subpaths out of the ink and text layers."""
    x0, x1, ytop, ybot = REG[name]
    px0, px1 = x0 * 30, x1 * 30
    py0, py1 = 37620 - ybot * 30, 37620 - ytop * 30
    taken = {"ink": [], "text": []}

    def fix(m):
        gid, d = m.group(1), m.group(2)
        if gid not in taken:
            return m.group(0)
        keep = []
        for sp in to_abs_subpaths(d):
            bb = bbox(sp)
            if bb:
                a, b, c, e = bb
                w, h = c - a, e - b
                if (a >= px0 and c <= px1 and b >= py0 and e <= py1
                        and 700 < w < 2000 and 700 < h < 2000 and 0.8 < w / h < 1.25):
                    taken[gid].append(sp)
                    continue
            keep.append(sp)
        return m.group(0).replace(d, " ".join(keep))

    svg = re.sub(r'<g[^>]*id="(\w+)"[^>]*>\s*<path d="([^"]+)"', fix, svg)
    return svg, taken


def group(gid, fill, paths):
    inner = "".join(f'<path d="{p}"/>' for p in paths)
    return (f'<g {TRANSFORM} fill="{fill}" stroke="none" fill-rule="evenodd" '
            f'id="{gid}">{inner}</g>')


def build(name):
    svg = open(f"{SRC}/{name}-original.svg").read()
    svg, taken = split_crown(svg, name)

    patch = group("dotpatch", "url(#ringG)", [circle(*c) for c in HALO[name]])
    i = svg.find('id="ring"')
    j = svg.find("</g>", i) + 4
    svg = svg[:svg.rfind("<g", 0, i)] + native_ring(svg) + patch + svg[j:]

    crown = (group("crown-side", INK, taken["ink"])
             + group("crown-center", ACCENT, taken["text"]))
    svg = svg.replace("</svg>", crown + "</svg>")

    cx, cy, r = RING[name]
    ring = (f'<radialGradient id="ringG" gradientUnits="userSpaceOnUse" '
            f'cx="{cx}" cy="{cy}" r="{r}">'
            f'<stop offset="0%" stop-color="#F9C742"/>'
            f'<stop offset="46%" stop-color="#F7B01E"/>'
            f'<stop offset="78%" stop-color="#F5910E"/>'
            f'<stop offset="100%" stop-color="#EE7A05"/></radialGradient>')
    svg = re.sub(r'<radialGradient id="ringG".*?</radialGradient>', ring, svg, flags=re.S)
    svg = re.sub(r'<radialGradient id="ringGU".*?</radialGradient>', '', svg, flags=re.S)
    return svg, {k: len(v) for k, v in taken.items()}


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name in ("english", "kannada"):
        svg, counts = build(name)
        open(f"{OUT}/{name}.svg", "w").write(svg)
        print(name, counts, len(svg))
