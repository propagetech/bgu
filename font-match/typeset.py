"""Shape text with HarfBuzz, return an SVG path in a 1000-upem-normalised box."""
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen

_cache = {}
def _load(path):
    if path not in _cache:
        data = open(path, 'rb').read()
        face = hb.Face(data); font = hb.Font(face)
        font.scale = (face.upem, face.upem)
        hb.ot_font_set_funcs(font)
        tt = TTFont(path)
        _cache[path] = (font, face.upem, tt, tt.getGlyphSet(), tt.getGlyphOrder())
    return _cache[path]

def shape(path, text, features=None):
    font, upem, tt, gs, order = _load(path)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, features)
    return buf.glyph_infos, buf.glyph_positions, upem, gs, order

def word_path(path, text, features=None):
    """SVG path data in font units (y up). Also returns tight bbox."""
    infos, poss, upem, gs, order = shape(path, text, features)
    pen = SVGPathPen(gs)
    bp = BoundsPen(gs)
    x = 0; y = 0
    ok = 0
    for i, p in zip(infos, poss):
        gname = order[i.codepoint]
        if gname == '.notdef': continue
        ok += 1
        for target in (pen, bp):
            tp = TransformPen(target, (1, 0, 0, 1, x + p.x_offset, y + p.y_offset))
            gs[gname].draw(tp)
        x += p.x_advance; y += p.y_advance
    return pen.getCommands(), bp.bounds, upem, x, ok, len(infos)

def has_all(path, text):
    _, _, _, _, order = shape(path, text)
    infos, poss, upem, gs, order2 = shape(path, text)
    return all(order2[i.codepoint] != '.notdef' for i in infos)
