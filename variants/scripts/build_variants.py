"""Rebuild the 14 colour / finish treatments per lockup from the final vector.

Every treatment is a recolour of the same edited trace that tenth-edition ships,
so the artwork (crown circle at centre top, bottom ornament, 2026 line) is
identical across the set. 3D and bevel are raster finishes applied after render.
"""
import os, sys
from PIL import Image, ImageChops, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tenth-edition", "scripts"))
from build10 import base_svg, recolor  # noqa: E402
from render import render_many         # noqa: E402

OUT = os.path.dirname(HERE)
SCRATCH = ("/private/tmp/claude-501/-Users-chetan-Downloads-jeevitha-ganesha-logo/"
           "183c1038-eccc-4dce-97cc-93f8c946349d/scratchpad/variants")

CHERRY_RING = [("0%", "#E8C86B"), ("45%", "#D4AF37"), ("75%", "#C2922E"),
               ("92%", "#C41E3A"), ("100%", "#A31530")]
CREAM_DISC = [("0%", "#FDF7E4"), ("60%", "#F8EAC0"), ("100%", "#F1DC9E")]
GOLD_RING = [("0%", "#FBE9A8"), ("45%", "#F2D06A"), ("75%", "#DFAE33"),
             ("100%", "#B07A18")]
GOLD_DISC = [("0%", "#FFF9E6"), ("60%", "#FCEFC4"), ("100%", "#F6E09A")]

# name -> (ring stops, disc stops, ink, accent, background or None, finish)
TREATMENTS = [
    ("01-cherry-gold",       CHERRY_RING, CREAM_DISC, "#6B0F1E", "#C41E3A", None,      None),
    ("02-gold-cherry",       GOLD_RING,   GOLD_DISC,  "#6B0F1E", "#C41E3A", None,      None),
    ("03-cherry-gold-dark",  [("0%", "#A81528"), ("46%", "#C41E3A"), ("78%", "#9E1229"), ("100%", "#6B0F1E")],
                             [("0%", "#8E1024"), ("62%", "#7E0B21"), ("100%", "#6B0F1E")],
                             "#E8C25A", "#F2DFA8", "#140407", None),
    ("04-gold-dark",         GOLD_RING,   [("0%", "#FBE9A8"), ("60%", "#F2D06A"), ("100%", "#DFAE33")],
                             "#2A1206", "#6B0F1E", "#140407", None),
    ("05-mono-gold",         [("0%", "#EBD9A4"), ("45%", "#DCC077"), ("75%", "#C9A44E"), ("100%", "#B88C33")],
                             [("0%", "#FBF3DC"), ("60%", "#F5E9C4"), ("100%", "#EEDDA8")],
                             "#A9822B", "#C39A3A", None, None),
    ("06-mono-cherry",       [("0%", "#E9A7B2"), ("45%", "#D9808F"), ("75%", "#C4566A"), ("100%", "#A83549")],
                             [("0%", "#FBEAED"), ("60%", "#F6D7DD"), ("100%", "#EFC0C9")],
                             "#A81528", "#C41E3A", None, None),
    ("07-mono-black",        [("0%", "#D8D8D8"), ("45%", "#B8B8B8"), ("75%", "#8E8E8E"), ("100%", "#6E6E6E")],
                             [("0%", "#F4F4F4"), ("60%", "#E6E6E6"), ("100%", "#D6D6D6")],
                             "#141414", "#3A3A3A", None, None),
    ("08-knockout-cherry",   [("0%", "#D8546A"), ("45%", "#CE3F58"), ("75%", "#C22A44"), ("100%", "#A81E37")],
                             [("0%", "#CF4459"), ("62%", "#C6364B"), ("100%", "#B92B40")],
                             "#FDF7E4", "#F8EAC0", "#C41E3A", None),
    ("09-knockout-gold",     [("0%", "#C9A02B"), ("45%", "#BE9224"), ("75%", "#B0851E"), ("100%", "#9E7618")],
                             [("0%", "#C79D28"), ("62%", "#BC9222"), ("100%", "#AE861C")],
                             "#6B0F1E", "#8E1024", "#D4AF37", None),
    ("10-3d-cherry-gold",    CHERRY_RING, CREAM_DISC, "#6B0F1E", "#C41E3A", None,      ("3d", "#5A0C18")),
    ("11-3d-gold-dark",      GOLD_RING,   [("0%", "#FBE9A8"), ("60%", "#F2D06A"), ("100%", "#DFAE33")],
                             "#2A1206", "#6B0F1E", "#140407", ("3d", "#6E5210")),
    ("12-3d-rose-gold",      [("0%", "#F2A6A6"), ("45%", "#E77B7B"), ("75%", "#D9534F"), ("100%", "#C0392B")],
                             [("0%", "#FADBD8"), ("60%", "#F5B7B1"), ("100%", "#F1948A")],
                             "#7B241C", "#C0392B", None,      ("3d", "#7B241C")),
    ("13-bevel-gold",        GOLD_RING,   GOLD_DISC,  "#6B0F1E", "#C41E3A", None,      ("bevel", None)),
    ("14-bevel-cherry-gold", CHERRY_RING, CREAM_DISC, "#6B0F1E", "#C41E3A", None,      ("bevel", None)),
]


def extrude(im, colour, depth=14, step=1.6):
    """Stack darkened silhouettes down-right behind the artwork."""
    pad = int(depth * step) + 2
    canvas = Image.new("RGBA", (im.width + pad, im.height + pad), (0, 0, 0, 0))
    sil = Image.new("RGBA", im.size, colour)
    sil.putalpha(im.getchannel("A"))
    for i in range(depth, 0, -1):
        o = int(i * step)
        canvas.alpha_composite(sil, (o, o))
    canvas.alpha_composite(im, (0, 0))
    return canvas


def bevel(im, strength=100, blur=10, offset=8):
    """Light from the top left, on the large forms only.

    The alpha is blurred hard first so the brush ring's fine flecks are ignored
    and the lift lands on the disc, the trunk lines and the lettering.
    """
    alpha = im.getchannel("A")
    a = alpha.filter(ImageFilter.GaussianBlur(blur))
    # clip both masks back to the artwork so the lift stays inside the marks
    # instead of hazing over the gaps between the brush strokes
    lit = ImageChops.multiply(ImageChops.subtract(a, ImageChops.offset(a, offset, offset)), alpha)
    shade = ImageChops.multiply(ImageChops.subtract(a, ImageChops.offset(a, -offset, -offset)), alpha)
    rgb = im.convert("RGB")
    white = Image.new("RGB", im.size, (255, 255, 255))
    black = Image.new("RGB", im.size, (0, 0, 0))
    rgb = Image.composite(Image.blend(rgb, white, strength / 100), rgb, lit)
    rgb = Image.composite(Image.blend(rgb, black, strength / 160), rgb, shade)
    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    return out


def flatten(im, colour, margin=0.06):
    pad = int(max(im.size) * margin)
    bg = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), colour)
    bg.alpha_composite(im, (pad, pad))
    return bg


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    for lang in ("english", "kannada"):
        base, _ = base_svg(lang)
        paths = []
        for name, ring, disc, ink, accent, _bg, _fx in TREATMENTS:
            sch = dict(ring=ring, head=disc, ink=ink, text=accent)
            p = os.path.join(SCRATCH, f"{lang}-{name}.svg")
            open(p, "w").write(recolor(base, sch, lang))
            paths.append(p)
        images = render_many(paths, cell=1260, cols=4)
        for (name, _r, _d, _i, _a, bg, fx), im in zip(TREATMENTS, images):
            if fx and fx[0] == "3d":
                im = extrude(im, fx[1])
            elif fx and fx[0] == "bevel":
                im = bevel(im)
            if bg:
                im = flatten(im, bg)
            dst = os.path.join(OUT, f"{lang}-{name}.png")
            im.save(dst)
            print(os.path.basename(dst), im.size)




def contact_sheet(lang="english"):
    """A review sheet of all 14 treatments for one lockup."""
    from PIL import ImageDraw, ImageFont
    cell, pad, cols = 330, 12, 5
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 13)
    except OSError:
        font = ImageFont.load_default()
    rows = (len(TREATMENTS) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (cell + pad) + pad,
                              rows * (cell + pad + 20) + pad + 26), "#F7F7F7")
    d = ImageDraw.Draw(sheet)
    d.text((pad, 8), f"{lang} - 14 treatments, 10th edition vector", fill="#111111", font=font)
    for i, (name, *_rest) in enumerate(TREATMENTS):
        im = Image.open(os.path.join(OUT, f"{lang}-{name}.png")).convert("RGBA")
        im.thumbnail((cell - 16, cell - 16))
        tile = Image.new("RGBA", (cell, cell), "#FFFFFF")
        tile.alpha_composite(im, ((cell - im.width) // 2, (cell - im.height) // 2))
        x = pad + (i % cols) * (cell + pad)
        y = 26 + pad + (i // cols) * (cell + pad + 20)
        sheet.paste(tile.convert("RGB"), (x, y))
        d.text((x, y + cell + 3), name, fill="#666666", font=font)
    out = os.path.join(OUT, f"contact-sheet-{lang}.png")
    sheet.save(out)
    print(out, sheet.size)


if __name__ == "__main__":
    main()
    for lang in ("english", "kannada"):
        contact_sheet(lang)
