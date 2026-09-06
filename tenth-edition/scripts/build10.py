import sys,re,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from pathlib2 import to_abs_subpaths,bbox
SRC="/Users/chetan/Downloads/jeevitha/ganesha-logo/vector"
OUT="/Users/chetan/Downloads/jeevitha/ganesha-logo/tenth-edition"
# crown-dot search region, in source-jpeg pixels
REG={"english":(555,700,120,196),"kannada":(555,700,112,188)}
# (cx,cy,r) jpeg px - covers each removed dot plus its white keyline halo
HALO={"english":[(582,173,24),(628,159,33),(674,173,24)],
      "kannada":[(584,166,24),(629,151,33),(672,166,24)]}
# ring-layer bbox -> user-space equivalent of the objectBoundingBox gradient
RING={"english":(18934,19633,17788),"kannada":(17915,19618,17800)}
K=0.552284749831
def circle(cx,cy,r):
    x,y,r=cx*30.0,37620-cy*30.0,r*30.0; k=K*r
    return (f"M{x+r:.2f} {y:.2f}"
            f"C{x+r:.2f} {y+k:.2f} {x+k:.2f} {y+r:.2f} {x:.2f} {y+r:.2f}"
            f"C{x-k:.2f} {y+r:.2f} {x-r:.2f} {y+k:.2f} {x-r:.2f} {y:.2f}"
            f"C{x-r:.2f} {y-k:.2f} {x-k:.2f} {y-r:.2f} {x:.2f} {y-r:.2f}"
            f"C{x+k:.2f} {y-r:.2f} {x+r:.2f} {y-k:.2f} {x+r:.2f} {y:.2f}Z")

# with drop_dots False the crown circles stay put; the dotpatch layer still runs so
# the traced white keyline around them is filled with the sun gradient
KEEP_DOTS=True
SCHEMES={
 "cherry-gold":dict(
   ring=[("0%","#E8C86B"),("45%","#D4AF37"),("75%","#C2922E"),("92%","#C41E3A"),("100%","#A31530")],
   head=[("0%","#FDF7E4"),("60%","#F8EAC0"),("100%","#F1DC9E")],
   ink="#6B0F1E", text="#C41E3A"),
 "cherry-reversed":dict(
   ring=[("0%","#A81528"),("46%","#C41E3A"),("78%","#9E1229"),("100%","#6B0F1E")],
   head=[("0%","#8E1024"),("62%","#7E0B21"),("100%","#6B0F1E")],
   ink="#E8C25A", text="#F2DFA8"),
 "original":dict(
   ring=[("0%","#F9C742"),("46%","#F7B01E"),("78%","#F5910E"),("100%","#EE7A05")],
   head=[("0%","#FCE58A"),("62%","#F8D452"),("100%","#F3C233")],
   ink="#141414", text="#8E1420"),
}
TRANSFORM='transform="translate(0.000000,3762.000000) scale(0.100000,-0.100000)"'

def edit(svg,name,drop_dots=True):
    x0,x1,ytop,ybot=REG[name]
    px0,px1=x0*30,x1*30; py0,py1=37620-ybot*30,37620-ytop*30
    rep={}
    def fix(m):
        gid,d=m.group(1),m.group(2)
        if gid in ("ink","text") and drop_dots:
            keep=[];n=0
            for s in to_abs_subpaths(d):
                bb=bbox(s)
                if bb:
                    a,b,c,e=bb; w,h=c-a,e-b
                    if (a>=px0 and c<=px1 and b>=py0 and e<=py1
                            and 700<w<2000 and 700<h<2000 and 0.8<w/h<1.25):
                        n+=1; continue
                keep.append(s)
            rep[gid]=n
            return m.group(0).replace(d," ".join(keep))
        return m.group(0)
    svg=re.sub(r'<g[^>]*id="(\w+)"[^>]*>\s*<path d="([^"]+)"', fix, svg)
    # patch the white keyline halos: own group, above ring, below the disc
    paths="".join(f'<path d="{circle(*c)}"/>' for c in HALO[name])
    patch=f'<g {TRANSFORM} fill="url(#ringGU)" stroke="none" id="dotpatch">{paths}</g>'
    i=svg.find('id="ring"'); j=svg.find("</g>",i)+4
    svg=svg[:j]+patch+svg[j:]
    rep["patch"]=len(HALO[name])
    return svg,rep

def recolor(svg,sch,name):
    for gid,key in (("ringG","ring"),("headG","head")):
        s="".join(f'<stop offset="{o}" stop-color="{c}"/>' for o,c in sch[key])
        svg=re.sub(r'(<radialGradient id="%s"[^>]*>).*?(</radialGradient>)'%gid,
                   lambda m:m.group(1)+s+m.group(2), svg, flags=re.S)
    cx,cy,r=RING[name]
    s="".join(f'<stop offset="{o}" stop-color="{c}"/>' for o,c in sch["ring"])
    gu=f'<radialGradient id="ringGU" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>'
    svg=re.sub(r'<radialGradient id="ringGU".*?</radialGradient>','',svg,flags=re.S)
    svg=svg.replace("</defs>",gu+"</defs>")
    svg=svg.replace('fill="#141414"',f'fill="{sch["ink"]}"')
    svg=svg.replace('fill="#8E1420"',f'fill="{sch["text"]}"')
    return svg

os.makedirs(OUT,exist_ok=True)
for name in ["kannada","english"]:
    base,rep=edit(open(f"{SRC}/{name}-original.svg").read(),name,
                  drop_dots=not KEEP_DOTS)
    print(f"{name}: {rep}")
    for sname,sch in SCHEMES.items():
        open(f"{OUT}/{name}-{sname}.svg","w").write(recolor(base,sch,name))
print("done")
