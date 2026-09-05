"""Font-guided redraw.

Takes a clean font glyph as the skeleton and deforms it onto the traced logo
letter.  The deformation field is low-pass filtered along the contour, so the
result keeps the font's curve quality (true straights, symmetric bowls,
consistent serifs) while landing on the logo's own silhouette.

    affine ICP  ->  coarse-to-fine normal-displacement warp  ->  Bezier refit
"""
import math, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, '/private/tmp/claude-501/-Users-chetan-Downloads-jeevitha-ganesha-logo/5c5921ea-3fd5-4a2a-b362-49c546b53336/scratchpad')
import smooth, glyphindex
from fontTools.ttLib import TTFont

# ---------- basics ----------
def perim(P):
    P = np.asarray(P)
    return float(np.hypot(*(np.roll(P, -1, 0) - P).T).sum())

def resample(P, step):
    """Uniform arc-length resample of a closed polyline."""
    P = np.asarray(P, float)
    d = np.hypot(*(np.roll(P, -1, 0) - P).T)
    cum = np.concatenate([[0], np.cumsum(d)])
    L = cum[-1]
    n = max(12, int(round(L/step)))
    t = np.linspace(0, L, n, endpoint=False)
    idx = np.searchsorted(cum, t, 'right') - 1
    idx = np.clip(idx, 0, len(P)-1)
    seg = np.where(d[idx] > 0, (t - cum[idx]) / np.where(d[idx] > 0, d[idx], 1), 0)
    A = P[idx]; B = P[(idx+1) % len(P)]
    return A + (B-A)*seg[:, None]

def circ_smooth(V, sigma_pts):
    """Circular Gaussian low-pass on a per-vertex vector field."""
    if sigma_pts < 0.4: return V
    r = max(1, int(3*sigma_pts))
    k = np.exp(-0.5*(np.arange(-r, r+1)/sigma_pts)**2); k /= k.sum()
    n = len(V)
    idx = (np.arange(n)[:, None] + np.arange(-r, r+1)[None, :]) % n
    return (V[idx] * k[None, :, None]).sum(1)

def glyph_contours(fontfile, ch, upem_norm=True):
    tt = TTFont(fontfile, lazy=True)
    gs = tt.getGlyphSet(); cm = tt.getBestCmap()
    pen = glyphindex.PolyPen(gs); gs[cm[ord(ch)]].draw(pen)
    return [np.asarray(c, float) for c in pen.cs]

def bbox(cs):
    P = np.vstack(cs)
    return P[:,0].min(), P[:,1].min(), P[:,0].max(), P[:,1].max()

def apply_aff(cs, M):
    return [c @ M[:2, :2].T + M[:2, 2] for c in cs]

def box_affine(src, dst):
    sx0,sy0,sx1,sy1 = bbox(src); dx0,dy0,dx1,dy1 = bbox(dst)
    a = (dx1-dx0)/max(sx1-sx0,1e-9); d = (dy1-dy0)/max(sy1-sy0,1e-9)
    M = np.array([[a,0,dx0-a*sx0],[0,d,dy0-d*sy0],[0,0,1]])
    return M

def icp_affine(src, dst, iters=30, step=None):
    """Refine an affine (scale/shear/translate) fit of src onto dst."""
    D = np.vstack(dst)
    tree = cKDTree(D)
    M = box_affine(src, dst)
    for _ in range(iters):
        S = np.vstack(apply_aff(src, M))
        _, ii = tree.query(S)
        T = D[ii]
        A = np.hstack([S, np.ones((len(S),1))])
        sol, *_ = np.linalg.lstsq(A, T, rcond=None)     # 3x2
        step_M = np.eye(3); step_M[:2,:2] = sol[:2].T; step_M[:2,2] = sol[2]
        M = step_M @ M
    return M

def pair_contours(src, dst):
    """Match source contours to target contours by area, largest first."""
    def area(c):
        x,y = c[:,0], c[:,1]
        return abs(np.dot(x, np.roll(y,-1)) - np.dot(y, np.roll(x,-1)))/2
    si = sorted(range(len(src)), key=lambda i:-area(src[i]))
    di = sorted(range(len(dst)), key=lambda i:-area(dst[i]))
    n = min(len(si), len(di))
    return [(src[si[i]], dst[di[i]]) for i in range(n)], len(src), len(dst)

def warp(srcC, dstC, step, schedule, max_pull=None):
    """Deform srcC onto dstC. `schedule` is a list of smoothing sigmas in
    contour-length units, coarse to fine."""
    S = resample(srcC, step)
    D = resample(dstC, step*0.6)
    tree = cKDTree(D)
    for sigma_units in schedule:
        _, ii = tree.query(S)
        disp = D[ii] - S
        if max_pull is not None:
            m = np.hypot(*disp.T)
            over = m > max_pull
            if over.any(): disp[over] *= (max_pull/m[over])[:, None]
        disp = circ_smooth(disp, sigma_units/step)
        S = S + disp
    return S

def residual(S, dstC, step):
    D = resample(dstC, step*0.6)
    d, _ = cKDTree(D).query(S)
    return float(np.sqrt((d**2).mean())), float(d.max())

def to_beziers(S, err, corner_scale, corner_angle):
    P = [tuple(p) for p in S]
    h = perim(P)/len(P)
    cs = smooth.detect_corners(P, h, corner_scale, corner_angle)
    return smooth.fit_closed(P, cs, err)

# ---------- two-phase warp ----------
import structwarp as _sw

def warp2(srcC, dstC, step, coarse_sigmas=(0.25,0.12,0.06), fine_fracs=(0.04,0.025,0.015,0.008,0.004,0.002)):
    """Phase 1 seeds the correspondence by arc-length index (cannot fold, gets
    the gross shape right). Phase 2 refines with nearest-point matching, which
    is accurate but only safe once we are already close."""
    S = _sw.resample_closed(np.asarray(srcC, float), max(64, int(perim(srcC)/step)))
    N = len(S)
    D = _sw.resample_closed(np.asarray(dstC, float), N)
    if _sw.signed_area(S)*_sw.signed_area(D) < 0: D = D[::-1]
    D = np.roll(D, -_sw.best_shift(S, D), axis=0)
    for f in coarse_sigmas:
        S = S + circ_smooth(D - S, N*f)
    Dd = _sw.resample_closed(np.asarray(dstC, float), N*4)
    tree = cKDTree(Dd)
    for f in fine_fracs:
        _, ii = tree.query(S)
        S = S + circ_smooth(Dd[ii] - S, max(0.8, N*f))
    return S
