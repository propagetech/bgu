"""One sheet with every 10th-edition colourway, for quick reference."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PNG = os.path.join(ROOT, "png")
COLS = [("cherry-gold", "cherry red + gold", "#FFFFFF"),
        ("cherry-reversed", "for dark grounds", "#140407"),
        ("original", "original colourway", "#FFFFFF")]
ROWS = ["english", "kannada"]
CELL, PAD, TOP = 470, 18, 82


def font(size):
    for p in ("/System/Library/Fonts/Helvetica.ttc",
              "/System/Library/Fonts/Supplemental/Arial.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def main():
    w = len(COLS) * (CELL + PAD) + PAD
    h = TOP + len(ROWS) * (CELL + PAD + 22) + PAD
    sheet = Image.new("RGB", (w, h), "#F7F7F7")
    d = ImageDraw.Draw(sheet)
    d.text((PAD, 14), "Bellandur Ganesha Utsava - 10th edition, centre crown circle",
           fill="#111111", font=font(19))
    d.text((PAD, 38), "vector redraw, cherry red + gold", fill="#666666", font=font(14))
    for r, lang in enumerate(ROWS):
        for c, (scheme, label, bg) in enumerate(COLS):
            x = PAD + c * (CELL + PAD)
            y = TOP + r * (CELL + PAD + 22)
            tile = Image.new("RGBA", (CELL, CELL), bg)
            im = Image.open(os.path.join(PNG, f"{lang}-{scheme}.png")).convert("RGBA")
            im.thumbnail((CELL - 34, CELL - 34))
            tile.alpha_composite(im, ((CELL - im.width) // 2, (CELL - im.height) // 2))
            sheet.paste(tile.convert("RGB"), (x, y))
            if r == 0:
                d.text((x, y - 16), label, fill="#666666", font=font(13))
        d.text((PAD, TOP + r * (CELL + PAD + 22) + CELL + 4), lang,
               fill="#666666", font=font(13))
    out = os.path.join(ROOT, "contact-sheet.png")
    sheet.save(out)
    print(out, sheet.size)


if __name__ == "__main__":
    main()
