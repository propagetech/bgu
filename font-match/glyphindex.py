"""Encoding-independent glyph shape matching.

Rasterises every glyph of every font into a fixed box (aspect preserved, centred)
so a legacy ASCII-encoded font can be matched without knowing its code page.
"""
import os, glob, math, pickle, sys
import numpy as np
from PIL import Image, ImageDraw, ImageChops
from fontTools.ttLib import TTFont, TTCollection
from fontTools.pens.basePen import BasePen

N = 96          # raster box
INK = 0.02      # min ink fraction to keep a glyph

class PolyPen(BasePen):
    def __init__(self, gs):
        super().__init__(gs); self.cs=[]; self.c=None
    def _moveTo(self, p): self.c=[p]
    def _lineTo(self, p): self.c.append(p)
    def _curveToOne(self, a,b,c):
        p0=self.c[-1]; L=(math.dist(p0,a)+math.dist(a,b)+math.dist(b,c))
        n=max(3,min(40,int(L/12)+3))
        for i in range(1,n+1):
            t=i/n; u=1-t
            self.c.append((u**3*p0[0]+3*u*u*t*a[0]+3*u*t*t*b[0]+t**3*c[0],
                           u**3*p0[1]+3*u*u*t*a[1]+3*u*t*t*b[1]+t**3*c[1]))
    def _qCurveToOne(self, a, b):
        p0=self.c[-1]; L=math.dist(p0,a)+math.dist(a,b)
        n=max(3,min(30,int(L/12)+3))
        for i in range(1,n+1):
            t=i/n; u=1-t
            self.c.append((u*u*p0[0]+2*u*t*a[0]+t*t*b[0], u*u*p0[1]+2*u*t*a[1]+t*t*b[1]))
    def _closePath(self):
        if self.c and len(self.c)>2: self.cs.append(self.c)
        self.c=None
    def _endPath(self): self._closePath()

def rasterise(cs, n=N):
    xs=[p[0] for c in cs for p in c]; ys=[p[1] for c in cs for p in c]
    if not xs: return None
    x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
    w,h=x1-x0,y1-y0
    if w<=0 or h<=0: return None
    s=(n-4)/max(w,h)
    ox=(n-w*s)/2; oy=(n-h*s)/2
    img=Image.new('1',(n,n),0)
    for c in cs:
        m=Image.new('1',(n,n),0)
        ImageDraw.Draw(m).polygon([((p[0]-x0)*s+ox, n-((p[1]-y0)*s+oy)) for p in c], fill=1)
        img=ImageChops.logical_xor(img,m)
    a=np.array(img,dtype=bool)
    return a, w/h

def font_glyphs(path):
    try:
        tt=TTFont(path, fontNumber=0, lazy=True)
        gs=tt.getGlyphSet()
    except Exception:
        return
    for name in tt.getGlyphOrder():
        if name=='.notdef': continue
        try:
            pen=PolyPen(gs); gs[name].draw(pen)
            if not pen.cs: continue
            r=rasterise(pen.cs)
            if r is None: continue
            a,asp=r
            if a.mean()<INK: continue
            yield name, a, asp
        except Exception:
            continue

def build(dirs, out):
    idx=[]
    files=[]
    for d in dirs: files += sorted(glob.glob(os.path.join(d,'*')))
    for i,f in enumerate(files):
        if not f.lower().endswith(('.ttf','.otf','.woff')): continue
        n=0
        for name,a,asp in font_glyphs(f):
            idx.append((os.path.basename(f), name, np.packbits(a), asp)); n+=1
        if i%25==0: print(f'  [{i}/{len(files)}] {os.path.basename(f)} {n} glyphs', flush=True)
    print('indexed', len(idx), 'glyphs from', len(files), 'files')
    with open(out,'wb') as fh: pickle.dump(idx, fh)
    return idx

def load(p):
    return pickle.load(open(p,'rb'))

def score(target, idx, topn=25, aspect_tol=0.35):
    ta, tasp = target
    tf=ta.astype(np.uint8)
    out=[]
    for fname, gname, packed, asp in idx:
        if abs(math.log(asp/tasp)) > aspect_tol: continue
        a=np.unpackbits(packed)[:N*N].reshape(N,N).astype(bool)
        inter=np.logical_and(a,ta).sum(); uni=np.logical_or(a,ta).sum()
        if uni: out.append((inter/uni, fname, gname, asp))
    out.sort(reverse=True)
    return out[:topn]
