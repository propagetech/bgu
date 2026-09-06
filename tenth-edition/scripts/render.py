"""Render SVGs to trimmed transparent PNGs.

One headless-Chrome pass lays every SVG out on a single grid page and screenshots
it, then the cells are sliced and trimmed. Chrome start-up dominates the cost, so
batching is roughly an order of magnitude faster than one run per file.
"""
import os, shutil, subprocess, time
from PIL import Image

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TMP = ("/private/tmp/claude-501/-Users-chetan-Downloads-jeevitha-ganesha-logo/"
       "183c1038-eccc-4dce-97cc-93f8c946349d/scratchpad/render")


def render_many(svgs, cell=1200, cols=4):
    """svgs: list of absolute paths. Returns a list of trimmed RGBA images."""
    shutil.rmtree(TMP, ignore_errors=True)
    os.makedirs(TMP)
    rows = (len(svgs) + cols - 1) // cols
    tiles = "".join(f'<img src="file://{s}">' for s in svgs)
    html = os.path.join(TMP, "grid.html")
    with open(html, "w") as f:
        f.write("<style>html,body{margin:0;background:transparent}"
                f"body{{display:grid;grid-template-columns:repeat({cols},{cell}px)}}"
                f"img{{display:block;width:{cell}px;height:{cell}px}}</style>{tiles}")
    shot = os.path.join(TMP, "grid.png")
    # Chrome writes the screenshot and then sometimes fails to exit on a large
    # page, so wait on the file rather than on the process.
    proc = subprocess.Popen([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                             "--default-background-color=00000000",
                             "--allow-file-access-from-files",
                             "--virtual-time-budget=20000",
                             f"--window-size={cols * cell},{rows * cell}",
                             f"--screenshot={shot}", f"--user-data-dir={TMP}/prof",
                             f"file://{html}"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline, size = time.time() + 300, -1
    while time.time() < deadline:
        if os.path.exists(shot):
            cur = os.path.getsize(shot)
            if cur and cur == size:      # file has stopped growing
                break
            size = cur
        if proc.poll() is not None and os.path.exists(shot):
            break
        time.sleep(1.5)
    proc.terminate()
    try:
        proc.wait(10)
    except subprocess.TimeoutExpired:
        proc.kill()
    if not os.path.exists(shot):
        raise RuntimeError("chrome produced no screenshot")
    sheet = Image.open(shot).convert("RGBA")
    out = []
    for i in range(len(svgs)):
        x, y = (i % cols) * cell, (i // cols) * cell
        im = sheet.crop((x, y, x + cell, y + cell))
        bb = im.getbbox()
        out.append(im.crop(bb) if bb else im)
    return out


if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "png")
    os.makedirs(out, exist_ok=True)
    names = sorted(n for n in os.listdir(root) if n.endswith(".svg"))
    for name, im in zip(names, render_many([os.path.join(root, n) for n in names],
                                           cell=1820, cols=3)):
        im.save(os.path.join(out, name[:-4] + ".png"))
        print(name, im.size)
