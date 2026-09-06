"""Base artwork for the browser editor.

Same trace as ../../tenth-edition, but the three crown circles are lifted into
their own groups so the editor can toggle them, and the layer fills are left on
the neutral trace colours so the editor can set them by group id.

Layer order: ring, dotpatch, head, ink, text, crown-side, crown-center.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tenth-edition", "scripts"))
from build10 import REG, HALO, RING, TRANSFORM, circle  # noqa: E402
from pathlib2 import to_abs_subpaths, bbox              # noqa: E402

SRC = os.path.join(ROOT, "vector")
OUT = os.path.join(os.path.dirname(HERE), "art")
INK, ACCENT = "#141414", "#8E1420"


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
    svg = svg[:j] + patch + svg[j:]

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
