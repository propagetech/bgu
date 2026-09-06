"""Render the tenth-edition SVGs to trimmed transparent PNGs with headless Chrome."""
import os, subprocess, sys, shutil
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "png")
TMP = "/private/tmp/claude-501/-Users-chetan-Downloads-jeevitha-ganesha-logo/183c1038-eccc-4dce-97cc-93f8c946349d/scratchpad/render"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SIZE = 2000

def render(svg, png):
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
    html = os.path.join(TMP, "p.html")
    with open(html, "w") as f:
        f.write('<style>html,body{margin:0;background:transparent}'
                f'img{{display:block;width:{SIZE}px;height:{SIZE}px}}</style>'
                f'<img src="file://{svg}">')
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--default-background-color=00000000", "--allow-file-access-from-files",
                    f"--window-size={SIZE},{SIZE}", f"--screenshot={png}",
                    f"--user-data-dir={TMP}/prof", f"file://{html}"],
                   check=True, capture_output=True)
    im = Image.open(png).convert("RGBA")
    bb = im.getbbox()
    if bb: im = im.crop(bb)
    im.save(png)
    return im.size

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name in sorted(os.listdir(ROOT)):
        if not name.endswith(".svg"): continue
        png = os.path.join(OUT, name[:-4] + ".png")
        print(name, render(os.path.join(ROOT, name), png))
