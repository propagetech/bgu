import re
TOK=re.compile(r'([MmLlCcZzHhVv])|(-?\d*\.?\d+(?:[eE][-+]?\d+)?)')
def tokens(d):
    for m in TOK.finditer(d):
        yield ('c',m.group(1)) if m.group(1) else ('n',float(m.group(2)))

def to_abs_subpaths(d):
    """Normalise a path to a list of absolute subpath strings."""
    toks=list(tokens(d)); i=0; cmd=None
    cx=cy=0.0; sx=sy=0.0
    subs=[]; cur=[]
    def flush():
        if cur: subs.append(" ".join(cur))
    while i<len(toks):
        k,v=toks[i]
        if k=='c': cmd=v; i+=1
        # gather numbers for this command
        need={'M':2,'m':2,'L':2,'l':2,'C':6,'c':6,'H':1,'h':1,'V':1,'v':1,'Z':0,'z':0}[cmd]
        args=[]
        while len(args)<need and i<len(toks) and toks[i][0]=='n':
            args.append(toks[i][1]); i+=1
        if cmd in 'Zz':
            if cur: cur.append("Z"); flush(); cur=[]
            cx,cy=sx,sy
            continue
        if cmd in 'Mm':
            if cur: flush(); cur=[]
            if cmd=='M': cx,cy=args
            else: cx,cy=cx+args[0],cy+args[1]
            sx,sy=cx,cy
            cur=[f"M{cx:.3f} {cy:.3f}"]
            cmd='L' if cmd=='M' else 'l'
        elif cmd in 'Cc':
            if cmd=='C': x1,y1,x2,y2,x,y=args
            else: x1,y1,x2,y2,x,y=cx+args[0],cy+args[1],cx+args[2],cy+args[3],cx+args[4],cy+args[5]
            cur.append(f"C{x1:.3f} {y1:.3f} {x2:.3f} {y2:.3f} {x:.3f} {y:.3f}")
            cx,cy=x,y
        elif cmd in 'Ll':
            x,y=(args if cmd=='L' else [cx+args[0],cy+args[1]])
            cur.append(f"L{x:.3f} {y:.3f}"); cx,cy=x,y
        elif cmd in 'Hh':
            x=args[0] if cmd=='H' else cx+args[0]
            cur.append(f"L{x:.3f} {cy:.3f}"); cx=x
        elif cmd in 'Vv':
            y=args[0] if cmd=='V' else cy+args[0]
            cur.append(f"L{cx:.3f} {y:.3f}"); cy=y
    flush()
    return subs

NUM=re.compile(r'-?\d*\.?\d+(?:[eE][-+]?\d+)?')
def bbox(sp):
    v=[float(x) for x in NUM.findall(sp)]
    xs=v[0::2]; ys=v[1::2]
    if not xs or not ys: return None
    return min(xs),min(ys),max(xs),max(ys)
