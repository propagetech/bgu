"""Build the 10th-edition lockups from the traced originals in ../../vector.

The trace is four flat colour layers (ring, head, ink, text) with no named
objects, so the crown circles are selected geometrically by bounding box inside
a small search region rather than by name.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pathlib2 import to_abs_subpaths, bbox

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "vector")
OUT = os.path.join(ROOT, "tenth-edition")

# "all" keeps the original black-red-black cluster, "center" keeps only the red
# centre circle (the two flanking black dots live in the ink layer), "none"
# removes all three.
CROWN = "center"

# crown search region, in source-jpeg pixels
REG = {"english": (555, 700, 120, 196), "kannada": (555, 700, 112, 188)}
# (cx, cy, r) jpeg px - one per circle, each covering the white keyline it sat in
HALO = {"english": [(582, 173, 24), (628, 159, 33), (674, 173, 24)],
        "kannada": [(584, 166, 24), (629, 151, 33), (672, 166, 24)]}
# ring-layer bbox centre and 52% radius, in path units
RING = {"english": (18934, 19632, 17896), "kannada": (18915, 19618, 17911)}
TRANSFORM = 'transform="translate(0.000000,3762.000000) scale(0.100000,-0.100000)"'
K = 0.552284749831


def circle(cx, cy, r):
    """A jpeg-pixel circle as a path in the trace's flipped path space."""
    x, y, r = cx * 30.0, 37620 - cy * 30.0, r * 30.0
    k = K * r
    return (f"M{x + r:.2f} {y:.2f}"
            f"C{x + r:.2f} {y + k:.2f} {x + k:.2f} {y + r:.2f} {x:.2f} {y + r:.2f}"
            f"C{x - k:.2f} {y + r:.2f} {x - r:.2f} {y + k:.2f} {x - r:.2f} {y:.2f}"
            f"C{x - r:.2f} {y - k:.2f} {x - k:.2f} {y - r:.2f} {x:.2f} {y - r:.2f}"
            f"C{x + k:.2f} {y - r:.2f} {x + r:.2f} {y - k:.2f} {x + r:.2f} {y:.2f}Z")


SCHEMES = {
    "cherry-gold": dict(
        ring=[("0%", "#E8C86B"), ("45%", "#D4AF37"), ("75%", "#C2922E"),
              ("92%", "#C41E3A"), ("100%", "#A31530")],
        head=[("0%", "#FDF7E4"), ("60%", "#F8EAC0"), ("100%", "#F1DC9E")],
        ink="#6B0F1E", text="#C41E3A"),
    "cherry-reversed": dict(
        ring=[("0%", "#A81528"), ("46%", "#C41E3A"), ("78%", "#9E1229"), ("100%", "#6B0F1E")],
        head=[("0%", "#8E1024"), ("62%", "#7E0B21"), ("100%", "#6B0F1E")],
        ink="#E8C25A", text="#F2DFA8"),
    "original": dict(
        ring=[("0%", "#F9C742"), ("46%", "#F7B01E"), ("78%", "#F5910E"), ("100%", "#EE7A05")],
        head=[("0%", "#FCE58A"), ("62%", "#F8D452"), ("100%", "#F3C233")],
        ink="#141414", text="#8E1420"),
}


def edit(svg, name, crown=CROWN):
    """Drop the unwanted crown circles and fill the white keyline they sat in.

    The keyline is a notch in the traced disc outline rather than its own
    subpath, so it is covered by a patch layer painted with the same sun
    gradient, sitting above the ring and below the disc.
    """
    x0, x1, ytop, ybot = REG[name]
    px0, px1 = x0 * 30, x1 * 30
    py0, py1 = 37620 - ybot * 30, 37620 - ytop * 30
    drop = {"all": (), "center": ("ink",), "none": ("ink", "text")}[crown]
    rep = {}

    def fix(m):
        gid, d = m.group(1), m.group(2)
        if gid not in drop:
            return m.group(0)
        keep, n = [], 0
        for sp in to_abs_subpaths(d):
            bb = bbox(sp)
            if bb:
                a, b, c, e = bb
                w, h = c - a, e - b
                if (a >= px0 and c <= px1 and b >= py0 and e <= py1
                        and 700 < w < 2000 and 700 < h < 2000 and 0.8 < w / h < 1.25):
                    n += 1
                    continue
            keep.append(sp)
        rep[gid] = n
        return m.group(0).replace(d, " ".join(keep))

    svg = re.sub(r'<g[^>]*id="(\w+)"[^>]*>\s*<path d="([^"]+)"', fix, svg)
    paths = "".join(f'<path d="{circle(*c)}"/>' for c in HALO[name])
    patch = (f'<g {TRANSFORM} fill="url(#ringG)" stroke="none" id="dotpatch">'
             f'{paths}</g>')
    i = svg.find('id="ring"')
    j = svg.find("</g>", i) + 4
    svg = svg[:j] + patch + svg[j:]
    rep["patch"] = len(HALO[name])
    return svg, rep


def recolor(svg, sch, name):
    """Repaint the four layers. The sun gradient is userSpaceOnUse so the patch
    layer resolves it identically to the ring path and leaves no seam."""
    cx, cy, r = RING[name]
    stops = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in sch["ring"])
    ring = (f'<radialGradient id="ringG" gradientUnits="userSpaceOnUse" '
            f'cx="{cx}" cy="{cy}" r="{r}">{stops}</radialGradient>')
    svg = re.sub(r'<radialGradient id="ringG".*?</radialGradient>', ring, svg, flags=re.S)
    svg = re.sub(r'<radialGradient id="ringGU".*?</radialGradient>', '', svg, flags=re.S)
    head = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in sch["head"])
    svg = re.sub(r'(<radialGradient id="headG"[^>]*>).*?(</radialGradient>)',
                 lambda m: m.group(1) + head + m.group(2), svg, flags=re.S)
    svg = svg.replace('fill="#141414"', f'fill="{sch["ink"]}"')
    svg = svg.replace('fill="#8E1420"', f'fill="{sch["text"]}"')
    return svg


def base_svg(name, crown=CROWN):
    """The edited trace for one lockup, before recolouring."""
    return edit(open(f"{SRC}/{name}-original.svg").read(), name, crown=crown)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name in ("kannada", "english"):
        base, rep = base_svg(name)
        print(f"{name}: {rep}")
        for sname, sch in SCHEMES.items():
            open(f"{OUT}/{name}-{sname}.svg", "w").write(recolor(base, sch, name))
    print("done")
