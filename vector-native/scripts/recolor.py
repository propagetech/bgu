import fitz, re, os, shutil
S="/private/tmp/claude-501/-Users-chetan-Downloads-jeevitha-ganesha-logo/039bc002-0c1a-4015-8230-f306e9d56e94/scratchpad"
OUT="/Users/chetan/Downloads/jeevitha/ganesha-logo/vector-native"

# the five source colours in the native Illustrator artwork, as CMYK
SRC = {
 "disc":   (0.011, 0.123, 0.873, 0.0),      # inner sun disc      #FAD823
 "mid":    (0.002, 0.407, 0.9863, 0.0),     # mid sun brush       #F79B11
 "outer":  (0.0,   0.7246, 0.9629, 0.0),    # outer brush wisps   #F25620
 "ink":    (1.0,   0.8809, 0.4099, 0.4409), # Ganesha line art    #182543
 "accent": (0.0911,0.9863, 1.0,    0.017),  # accent word + dots  #D92025
}
SCHEMES = {
 "cherry-gold":     {"disc":"F2DFA8","mid":"D4AF37","outer":"C41E3A","ink":"7E0B21","accent":"A31530"},
 "gold-dominant":   {"disc":"F5E3B0","mid":"D4AF37","outer":"A67C1A","ink":"7E0B21","accent":"C41E3A"},
 "cherry-reversed": {"disc":"8E1024","mid":"6B0F1E","outer":"C41E3A","ink":"E8C25A","accent":"F2DFA8"},
}
PAT = re.compile(rb'([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(k|K)\b')

def role_of(v, tol=0.06):
    best,bd=None,9
    for r,s in SRC.items():
        d=sum((a-b)**2 for a,b in zip(v,s))**0.5
        if d<bd: best,bd=r,d
    return best if bd<=tol else None

def build(src_pdf, scheme, dst):
    doc=fitz.open(src_pdf)
    hits=0
    for page in doc:
        for xref in page.get_contents():
            data=doc.xref_stream(xref)
            def sub(m):
                nonlocal hits
                v=tuple(float(x) for x in m.groups()[:4])
                op=m.group(5)
                r=role_of(v)
                if r is None: return m.group(0)
                h=scheme[r]; hits+=1
                R,G,B=[int(h[i:i+2],16)/255 for i in (0,2,4)]
                tag=b"rg" if op==b"k" else b"RG"
                return b"%.5f %.5f %.5f %s"%(R,G,B,tag)
            doc.update_stream(xref, PAT.sub(sub,data))
    doc.save(dst, garbage=4, deflate=True)
    doc.close()
    return hits

os.makedirs(f"{OUT}/pdf",exist_ok=True)
for label in ["kannada","english","mark"]:
    src=f"{S}/flat/{label}.pdf"
    shutil.copy(src, f"{OUT}/pdf/{label}-original.pdf")
    for sname,sch in SCHEMES.items():
        n=build(src,sch,f"{OUT}/pdf/{label}-{sname}.pdf")
        print(f"{label}-{sname}: recoloured {n} colour ops")
