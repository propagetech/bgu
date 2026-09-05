"""Word-level font-guided redraw with graceful degradation.

Contours that pair between the font setting and the traced logo get the
font-guided warp.  Contours with no counterpart (the logo merges some counters
the font keeps open, and carries swashes no font has) fall through to a
corner-preserving curve refit of the trace itself, so nothing is invented and
nothing is lost.
"""
import sys, math; sys.path.insert(0,'.')
import numpy as np, smooth, redraw, specimen as sp
from scipy.spatial import cKDTree
from scipy.optimize import linear_sum_assignment

def area(c):
    c=np.asarray(c,float); x,y=c[:,0],c[:,1]
    return abs(np.dot(x,np.roll(y,-1))-np.dot(y,np.roll(x,-1)))/2

def cent(c):
    return np.asarray(c,float).mean(0)

def smooth_trace(P, sigma=40.0, h=5.0):
    R=[tuple(p) for p in redraw.resample(np.asarray(P,float), h)]
    L=redraw.perim(R)
    cor=smooth.detect_corners(R, h, min(100.0, L/14.0), 42.0)
    return np.asarray(smooth.smooth_closed(R, max(0.6, min(sigma,L/28.0)/h), cor), float)

def _chord_dev(b):
    """Max distance of a cubic from its own chord."""
    p0,c1,c2,p3=[np.asarray(v,float) for v in b]
    v=p3-p0; L=np.hypot(*v)
    if L<1e-9: return max(np.hypot(*(c1-p0)), np.hypot(*(c2-p0)))
    n=np.array([-v[1],v[0]])/L
    return max(abs(float(n@(c1-p0))), abs(float(n@(c2-p0))))

def straighten(bz, tol=4.0):
    """Replace near-linear cubics with exact straight segments, then merge
    consecutive collinear ones. Straight stems are the most visible marker of
    a hand-built outline versus a trace."""
    out=[]
    for b in bz:
        if _chord_dev(b) < tol:
            p0=np.asarray(b[0],float); p3=np.asarray(b[3],float); v=p3-p0
            out.append((tuple(p0), tuple(p0+v/3), tuple(p0+2*v/3), tuple(p3)))
        else:
            out.append(b)
    def is_line(b):
        return _chord_dev(b) < 1e-6
    merged=[]; i=0
    while i < len(out):
        b=out[i]
        if is_line(b):
            p0=np.asarray(b[0],float); p3=np.asarray(b[3],float)
            j=i+1
            while j < len(out) and is_line(out[j]):
                q3=np.asarray(out[j][3],float)
                v=q3-p0; L=np.hypot(*v)
                if L<1e-9: break
                n=np.array([-v[1],v[0]])/L
                mids=[np.asarray(out[t][3],float) for t in range(i,j)]
                if max(abs(float(n@(m-p0))) for m in mids) > tol: break
                p3=q3; j+=1
            v=p3-p0
            merged.append((tuple(p0), tuple(p0+v/3), tuple(p0+2*v/3), tuple(p3)))
            i=j
        else:
            merged.append(b); i+=1
    return merged

def refit(P, err=8.0, straight_tol=4.0):
    pts=[tuple(p) for p in P]
    h=redraw.perim(pts)/len(pts)
    L=redraw.perim(pts)
    cor=smooth.detect_corners(pts, h, min(220.0, L/14.0), 45.0)
    bz=smooth.fit_closed(pts, cor, err)
    return straighten(bz, straight_tol) if straight_tol else bz

def pair_up(src, dst):
    """Hungarian assignment on normalised centroid distance + area ratio."""
    if not src or not dst: return []
    def norm(cs):
        A=np.vstack([np.asarray(c,float) for c in cs])
        o=A.min(0); s=(A.max(0)-o).max()
        return [( (cent(c)-o)/s, area(c)/s**2 ) for c in cs]
    ns, nd = norm(src), norm(dst)
    C=np.zeros((len(src), len(dst)))
    for i,(ci,ai) in enumerate(ns):
        for j,(cj,aj) in enumerate(nd):
            C[i,j]=np.hypot(*(ci-cj)) + 0.6*abs(math.log(max(ai,1e-9)/max(aj,1e-9)))
    r,c=linear_sum_assignment(C)
    return [(int(i),int(j),float(C[i,j])) for i,j in zip(r,c)]

def bez_pts(bz, n=15):
    p=[]
    for b in bz:
        p0,c1,c2,p3=[np.asarray(v,float) for v in b]
        p.append(p0)
        for i in range(1,n):
            u=i/n; v=1-u
            p.append(v**3*p0+3*v*v*u*c1+3*v*u*u*c2+u**3*p3)
    return np.asarray(p)

def resid(bz, tgtP):
    d,_=cKDTree(redraw.resample(np.asarray(tgtP,float), 2.0)).query(bez_pts(bz))
    return float(np.sqrt((d**2).mean())), float(d.max())

def redraw_word(fontfile, text, tgt_cs, sc=None, step=9.0, err=25.0, max_cost=0.55,
                gate_rms=15.0, gate_max=110.0):
    tgt=[smooth_trace(P) for P in tgt_cs]
    tasp=(lambda A:(A[:,0].max()-A[:,0].min())/(A[:,1].max()-A[:,1].min()))(np.vstack(tgt))
    track=sp.fit_track(fontfile, text, tasp, sc)
    src=[np.asarray(c,float) for c in sp.word_cs(fontfile, text, sc, track)]
    M=redraw.icp_affine(src, tgt)
    src=[np.asarray(c) for c in redraw.apply_aff(src, M)]
    pairs=pair_up(src, tgt)
    used=set(); out=[]; rep=[]
    for i,j,cost in pairs:
        if cost>max_cost: continue
        try:
            S=redraw.warp2(src[i], tgt[j], step)
            bz=refit(S, err)
        except Exception:
            continue
        rms,mx=resid(bz, tgt[j])
        if rms>gate_rms or mx>gate_max:      # warp is worse than the trace: reject it
            rep.append(('reject', j, rms, len(bz)))
            continue
        out.append(bz); used.add(j)
        rep.append(('warp', j, rms, len(bz)))
    for j,P in enumerate(tgt):
        if j in used: continue
        bz=refit(P, err*0.4)
        rms,mx=resid(bz, P)
        out.append(bz); rep.append(('refit', j, rms, len(bz)))
    return out, rep, len(src), len(tgt), track
