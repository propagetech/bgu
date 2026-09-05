"""Segment-structured font-guided redraw.

The output keeps the base font's exact segment structure - the same on-curve
nodes, the same line-vs-curve decision for every segment - but every control
point is refitted to the traced logo letter.  Straight stems stay perfectly
straight, serif corners stay corners, and the silhouette is the logo's own.
"""
import math
import numpy as np
from scipy.spatial import cKDTree
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen

# ---------- font glyph as typed segments ----------
class StructPen(BasePen):
    def __init__(self, gs):
        super().__init__(gs); self.contours=[]; self.cur=None; self.start=None; self.pt=None
    def _moveTo(self, p): self.cur=[]; self.start=p; self.pt=p
    def _lineTo(self, p): self.cur.append(('L', self.pt, p)); self.pt=p
    def _curveToOne(self, a,b,c): self.cur.append(('C', self.pt, a, b, c)); self.pt=c
    def _qCurveToOne(self, a, b):
        p0=self.pt
        c1=(p0[0]+2/3*(a[0]-p0[0]), p0[1]+2/3*(a[1]-p0[1]))
        c2=(b[0]+2/3*(a[0]-b[0]),  b[1]+2/3*(a[1]-b[1]))
        self.cur.append(('C', p0, c1, c2, b)); self.pt=b
    def _closePath(self):
        if self.cur is None: return
        if self.pt != self.start: self.cur.append(('L', self.pt, self.start))
        if len(self.cur)>1: self.contours.append(self.cur)
        self.cur=None
    def _endPath(self): self._closePath()

def glyph_segments(fontfile, ch):
    tt=TTFont(fontfile, lazy=True); gs=tt.getGlyphSet(); cm=tt.getBestCmap()
    pen=StructPen(gs); gs[cm[ord(ch)]].draw(pen)
    return pen.contours

# ---------- sampling ----------
def seg_points(seg, n):
    if seg[0]=='L':
        p0,p1=seg[1],seg[2]
        t=np.linspace(0,1,n,endpoint=False)[:,None]
        return np.array(p0)+ (np.array(p1)-np.array(p0))*t
    p0,c1,c2,p3=[np.array(v,float) for v in seg[1:]]
    t=np.linspace(0,1,n,endpoint=False)[:,None]; u=1-t
    return u**3*p0 + 3*u*u*t*c1 + 3*u*t*t*c2 + t**3*p3

def seg_len(seg):
    P=seg_points(seg, 24)
    end=np.array(seg[-1],float)
    P=np.vstack([P,end])
    return float(np.hypot(*(P[1:]-P[:-1]).T).sum())

def sample_contour(segs, step):
    """Uniform arc-length sampling of the whole contour, plus the index of each
    segment's start node. Uniformity matters: index correspondence against the
    target is only meaningful if both are parameterised by arc length."""
    dense=[]; node_s=[]; acc=0.0
    for seg in segs:
        pts=seg_points(seg, 40)
        node_s.append(acc)
        P=np.vstack([pts, np.array(seg[-1],float)])
        acc += float(np.hypot(*(P[1:]-P[:-1]).T).sum())
        dense.append(pts)
    total=max(acc,1e-9)
    Dn=np.vstack(dense)
    N=max(64, int(round(total/step)))
    S=resample_closed(Dn, N)
    nodes=np.round(np.array(node_s)/total*N).astype(int)
    # keep nodes strictly increasing so every segment owns at least one sample
    for j in range(1, len(nodes)):
        if nodes[j] <= nodes[j-1]: nodes[j] = nodes[j-1]+1
    if nodes[-1] >= N:
        N = int(nodes[-1])+2
        S = resample_closed(Dn, N)
    return S, nodes

def resample_closed(P, n):
    P=np.asarray(P,float)
    d=np.hypot(*(np.roll(P,-1,0)-P).T)
    cum=np.concatenate([[0],np.cumsum(d)]); L=cum[-1]
    t=np.linspace(0,L,n,endpoint=False)
    i=np.clip(np.searchsorted(cum,t,'right')-1, 0, len(P)-1)
    f=np.where(d[i]>0,(t-cum[i])/np.where(d[i]>0,d[i],1),0)
    return P[i]+(P[(i+1)%len(P)]-P[i])*f[:,None]

def signed_area(P):
    x,y=P[:,0],P[:,1]
    return 0.5*(np.dot(x,np.roll(y,-1))-np.dot(y,np.roll(x,-1)))

def best_shift(S, D, coarse=4):
    """Circular shift k minimising sum |S_i - D_{i+k}|^2. Brute force on a
    subsampled contour, then refined locally - FFT correlation got the sign
    conventions wrong and rotated letters around their own outline."""
    n=len(S)
    sub=max(1, n//192)
    Ss=S[::sub]; m=len(Ss)
    idx=(np.arange(m)*sub)[None,:]
    best=None; bk=0
    ks=np.arange(0, n, coarse)
    for k in ks:
        d=Ss-D[(idx[0]+k) % n]
        v=float((d*d).sum())
        if best is None or v<best: best, bk = v, int(k)
    for k in range(max(0,bk-coarse), bk+coarse+1):
        d=Ss-D[(idx[0]+k) % n]
        v=float((d*d).sum())
        if v<best: best, bk = v, int(k)
    return bk

def circ_smooth(V, sig):
    if sig<0.4: return V
    r=max(1,int(3*sig)); k=np.exp(-0.5*(np.arange(-r,r+1)/sig)**2); k/=k.sum()
    n=len(V); idx=(np.arange(n)[:,None]+np.arange(-r,r+1)[None,:])%n
    return (V[idx]*k[None,:,None]).sum(1)

# ---------- fitting one segment ----------
def fit_line(pts):
    return ('L', tuple(pts[0]), tuple(pts[-1]))

def fit_curve(pts, t1, t2):
    """Least-squares cubic with fixed endpoints and fixed end tangents."""
    P0=pts[0]; P3=pts[-1]
    d=np.hypot(*(pts[1:]-pts[:-1]).T); cum=np.concatenate([[0],np.cumsum(d)])
    if cum[-1]<=0: return ('C', tuple(P0), tuple(P0), tuple(P3), tuple(P3))
    u=cum/cum[-1]
    b1=3*(1-u)**2*u; b2=3*(1-u)*u**2
    base=((1-u)**3)[:,None]*P0 + (u**3)[:,None]*P3
    R=pts-base
    A=np.stack([b1[:,None]*t1, b2[:,None]*t2], axis=2).reshape(-1,2)
    sol,*_=np.linalg.lstsq(A, R.reshape(-1), rcond=None)
    a1,a2=float(sol[0]),float(sol[1])
    L=float(np.hypot(*(P3-P0)))
    a1=min(max(a1, 0.01*L), 2.0*L); a2=min(max(a2, 0.01*L), 2.0*L)
    return ('C', tuple(P0), tuple(P0+t1*a1), tuple(P3+t2*a2), tuple(P3))

def redraw_contour(segs, target_pts, step, final_sigma_frac=0.010, nsteps=7):
    """Warp the font contour onto target_pts, then refit its own segments."""
    S, nodes = sample_contour(segs, step)
    N=len(S)
    D=resample_closed(target_pts, N)
    if signed_area(S)*signed_area(D) < 0: D=D[::-1]
    D=np.roll(D, -best_shift(S,D), axis=0)
    # coarse-to-fine: low-pass the displacement so the font's local geometry survives
    sig0 = N*0.25
    sig1 = max(0.8, N*final_sigma_frac)
    for i in range(nsteps):
        f=i/(nsteps-1)
        sig=sig0*(sig1/sig0)**f
        S = S + circ_smooth(D-S, sig)
    # windowed nearest-point refinement: search only a local index window, so
    # the correspondence cannot fold back on itself
    W=max(6, N//12)
    off=np.arange(-W, W+1)
    for sig in (N*0.06, N*0.035, N*0.02, N*0.012, sig1*2, sig1, sig1):
        cand=D[(np.arange(N)[:,None]+off[None,:]) % N]
        dd=((cand-S[:,None,:])**2).sum(2)
        tgt=cand[np.arange(N), dd.argmin(1)]
        S = S + circ_smooth(tgt-S, sig)
    # refit each original segment against its warped points
    out=[]
    for j,s in enumerate(segs):
        a=nodes[j]; b=nodes[j+1] if j+1<len(nodes) else N
        pts=np.vstack([S[a:b], S[b % N]])
        if len(pts)<3 or s[0]=='L':
            out.append(fit_line(pts))
        else:
            p0=np.array(s[1]); c1=np.array(s[2]); c2=np.array(s[3]); p3=np.array(s[4])
            def unit(v):
                n=np.hypot(*v); return v/n if n>1e-9 else np.array([0.,0.])
            t1=unit(c1-p0); t2=unit(c2-p3)
            # rotate original tangents into the warped frame
            A0=np.array(s[1]); A1=np.array(s[4])
            B0=pts[0]; B1=pts[-1]
            va=A1-A0; vb=B1-B0
            na,nb=np.hypot(*va),np.hypot(*vb)
            if na>1e-9 and nb>1e-9:
                ca=(va[0]*vb[0]+va[1]*vb[1])/(na*nb); sa=(va[0]*vb[1]-va[1]*vb[0])/(na*nb)
                R=np.array([[ca,-sa],[sa,ca]])
                t1=R@t1; t2=R@t2
            out.append(fit_curve(pts, t1, t2))
    return out, S, D
