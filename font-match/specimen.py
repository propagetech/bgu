import sys, io, math; sys.path.insert(0,'.')
import smooth, glyphindex, numpy as np
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from PIL import Image, ImageDraw, ImageChops
H=150

def word_cs(path, text, sc=None, track=0.0):
    data=open(path,'rb').read()
    if data[:4] in (b'wOFF',b'wOF2'):
        t=TTFont(io.BytesIO(data)); t.flavor=None; b=io.BytesIO(); t.save(b); data=b.getvalue()
    face=hb.Face(data); f=hb.Font(face); f.scale=(face.upem,face.upem); hb.ot_font_set_funcs(f)
    buf=hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(f,buf)
    tt=TTFont(io.BytesIO(data)); gs=tt.getGlyphSet(); order=tt.getGlyphOrder()
    pen=SVGPathPen(gs); x=0
    for n,(i,p) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        k=1.0 if (sc is None or n==0) else sc
        gs[order[i.codepoint]].draw(TransformPen(pen,(k,0,0,k,x+p.x_offset*k,p.y_offset*k)))
        x+=p.x_advance*k + track*face.upem
    return smooth.flatten(pen.getCommands(), tol=1.0)

def rast(cs, h=H, flip=True):
    xs=[p[0] for c in cs for p in c]; ys=[p[1] for c in cs for p in c]
    x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
    s=h/(y1-y0); w=int((x1-x0)*s)+8
    img=Image.new('1',(w,h+8),0)
    for c in cs:
        m=Image.new('1',(w,h+8),0)
        pts=[((p[0]-x0)*s+4, (h+4-((p[1]-y0)*s)) if flip else ((p[1]-y0)*s+4)) for p in c]
        ImageDraw.Draw(m).polygon(pts, fill=1); img=ImageChops.logical_xor(img,m)
    return img

def fit_track(path, text, target_asp, sc=None):
    lo,hi=-0.45,0.35
    for _ in range(22):
        mid=(lo+hi)/2
        cs=word_cs(path,text,sc,mid)
        xs=[p[0] for c in cs for p in c]; ys=[p[1] for c in cs for p in c]
        a=(max(xs)-min(xs))/(max(ys)-min(ys))
        if a<target_asp: lo=mid
        else: hi=mid
    return (lo+hi)/2

def target(svgf, gid, box):
    s=open(svgf).read(); i=s.index('id="%s"'%gid); j=s.index('<path d="',i)+9; k=s.index('"',j)
    subs=smooth.flatten(s[j:k], tol=1.0); out=[]
    for P in subs:
        xs=[p[0]/10 for p in P]; ys=[3762-p[1]/10 for p in P]
        if box[0]<=min(xs) and max(xs)<=box[2] and box[1]<=min(ys) and max(ys)<=box[3]: out.append(P)
    return out

KN='/Users/chetan/Downloads/jeevitha/ganesha-logo/vector/kannada-original.svg'
EN='/Users/chetan/Downloads/jeevitha/ganesha-logo/vector/english-original.svg'
rows=[]
def add(label, img): rows.append((label, img))

# --- Kannada ---
tk=target(KN,'ink',(930,1540,2870,2230))
tkr=rast(tk); xs=[p[0] for c in tk for p in c]; ys=[p[1] for c in tk for p in c]
kasp=(max(xs)-min(xs))/(max(ys)-min(ys))
add('LOGO  GANESHA (Kannada)', tkr)
for f,lab in [('ttf/BalooTamma2-800.ttf','Baloo Tamma 2 ExtraBold'),
              ('ttf/NotoSansKannada-700.ttf','Noto Sans Kannada Bold'),
              ('ttf/AnekKannada-700.ttf','Anek Kannada Bold'),
              ('ttf/NotoSerifKannada-800.ttf','Noto Serif Kannada ExtraBold')]:
    tr=fit_track(f,'ಗಣೇಶ',kasp)
    add(f'{lab}  (tracking {tr*1000:+.0f}/1000em)', rast(word_cs(f,'ಗಣೇಶ',None,tr)))

# --- English ---
tu=target(EN,'text',(1280,2270,2615,2640))
tur=rast(tu); xs=[p[0] for c in tu for p in c]; ys=[p[1] for c in tu for p in c]
uasp=(max(xs)-min(xs))/(max(ys)-min(ys))
add('LOGO  UTSAVA', tur)
for f,lab in [('enfonts/Oranienbaum-400.woff','Oranienbaum'),
              ('enfonts/Marcellus-400.woff','Marcellus'),
              ('enfonts/Amarante-400.woff','Amarante'),
              ('enfonts/Cinzel-700.woff','Cinzel Bold'),
              ('enfonts/BIZUDMincho-700.woff','BIZ UDMincho Bold')]:
    try:
        tr=fit_track(f,'UTSAVA',uasp,0.847)
        add(f'{lab}  (tracking {tr*1000:+.0f}/1000em)', rast(word_cs(f,'UTSAVA',0.847,tr)))
    except Exception as e: print('skip',lab,e)

W=max(i.width for _,i in rows)+16; Ht=sum(i.height+24 for _,i in rows)+10
c=Image.new('RGB',(W,Ht),'white'); dr=ImageDraw.Draw(c); y=4
for lab,img in rows:
    dr.text((6,y+3), lab, fill='#000' if lab.startswith('LOGO') else '#555')
    c.paste(img.convert('L').point(lambda v:255-v).convert('RGB'),(8,y+16)); y+=img.height+24
c.save('specimen.png'); print('saved', c.size)
