"""
Outline de-serration for autotraced logo art.

Pipeline per closed subpath:
  1. flatten cubics -> dense polyline
  2. uniform arc-length resample (step h)
  3. corner detection at a scale ABOVE the trace-noise band
  4. circular Gaussian low-pass, applied per corner-to-corner segment
     (corners are pinned, so ear points / trunk tips stay sharp)
  5. Schneider least-squares cubic Bezier refit with Newton reparameterisation
"""
import re, math, sys

# ---------- path parsing ----------
NUM = re.compile(r'[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?')
CMD = re.compile(r'[MmZzLlHhVvCcSsQqTtAa]')

def tokenize(d):
    out, i, n = [], 0, len(d)
    while i < n:
        c = d[i]
        if CMD.match(c):
            out.append(c); i += 1
        elif c in ' ,\t\r\n':
            i += 1
        else:
            m = NUM.match(d, i)
            if not m: i += 1; continue
            out.append(float(m.group())); i = m.end()
    return out

def flatten(d, tol=0.6):
    """Return list of closed subpaths, each a list of (x,y)."""
    toks = tokenize(d)
    subs, cur = [], []
    i = 0; cx = cy = 0.0; sx = sy = 0.0; cmd = None
    prev_c2 = None
    def push():
        nonlocal cur
        if len(cur) > 2: subs.append(cur)
        cur = []
    def bez(p0, p1, p2, p3):
        # adaptive-ish: sample by control-polygon length
        L = (math.dist(p0,p1) + math.dist(p1,p2) + math.dist(p2,p3))
        n = max(2, min(160, int(L / tol) + 2))
        for k in range(1, n+1):
            t = k / n; u = 1-t
            x = u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0]
            y = u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1]
            cur.append((x, y))
    while i < len(toks):
        t = toks[i]
        if isinstance(t, str): cmd = t; i += 1
        elif cmd in ('M','m'): cmd = 'L' if cmd == 'M' else 'l'
        if cmd in ('M','m'):
            x, y = toks[i], toks[i+1]; i += 2
            if cmd == 'm': x += cx; y += cy
            push(); cx, cy = x, y; sx, sy = x, y; cur = [(cx, cy)]
            cmd = 'L' if cmd == 'M' else 'l'
        elif cmd in ('L','l'):
            x, y = toks[i], toks[i+1]; i += 2
            if cmd == 'l': x += cx; y += cy
            cx, cy = x, y; cur.append((cx, cy)); prev_c2 = None
        elif cmd in ('H','h'):
            x = toks[i]; i += 1
            if cmd == 'h': x += cx
            cx = x; cur.append((cx, cy)); prev_c2 = None
        elif cmd in ('V','v'):
            y = toks[i]; i += 1
            if cmd == 'v': y += cy
            cy = y; cur.append((cx, cy)); prev_c2 = None
        elif cmd in ('C','c'):
            x1,y1,x2,y2,x,y = toks[i:i+6]; i += 6
            if cmd == 'c': x1+=cx; y1+=cy; x2+=cx; y2+=cy; x+=cx; y+=cy
            bez((cx,cy),(x1,y1),(x2,y2),(x,y)); prev_c2 = (x2,y2); cx,cy = x,y
        elif cmd in ('S','s'):
            x2,y2,x,y = toks[i:i+4]; i += 4
            if cmd == 's': x2+=cx; y2+=cy; x+=cx; y+=cy
            if prev_c2: x1,y1 = 2*cx-prev_c2[0], 2*cy-prev_c2[1]
            else: x1,y1 = cx,cy
            bez((cx,cy),(x1,y1),(x2,y2),(x,y)); prev_c2 = (x2,y2); cx,cy = x,y
        elif cmd in ('Z','z'):
            push(); cx, cy = sx, sy; cur = [(cx,cy)]; i += 0
            if i < len(toks) and isinstance(toks[i], str): pass
            cmd = None
            # consume nothing; loop continues
            if not (i < len(toks)): break
            continue
        else:
            i += 1
    push()
    # drop duplicated closing vertex
    cleaned = []
    for s in subs:
        while len(s) > 1 and math.dist(s[0], s[-1]) < 1e-9: s.pop()
        if len(s) > 3: cleaned.append(s)
    return cleaned

# ---------- geometry helpers ----------
def area(P):
    a = 0.0
    for i in range(len(P)):
        x1,y1 = P[i]; x2,y2 = P[(i+1) % len(P)]
        a += x1*y2 - x2*y1
    return a/2

def perimeter(P):
    return sum(math.dist(P[i], P[(i+1) % len(P)]) for i in range(len(P)))

def resample(P, h):
    """Uniform arc-length resample of a CLOSED polyline."""
    L = perimeter(P)
    n = max(8, int(round(L/h)))
    step = L/n
    out = []; i = 0; acc = 0.0; cur = P[0]
    out.append(cur)
    seg = 0; N = len(P)
    pos = P[0]; idx = 0; rem = math.dist(P[0], P[1 % N])
    target = step
    # walk
    dist_along = 0.0
    j = 0
    a = P[0]; b = P[1 % N]; d = math.dist(a,b); t0 = 0.0
    k = 0
    while len(out) < n:
        need = step
        while d - t0 < need:
            need -= (d - t0)
            k += 1
            a = P[k % N]; b = P[(k+1) % N]; d = math.dist(a,b); t0 = 0.0
            if k > 4*N: break
        t0 += need
        u = t0/d if d else 0
        out.append((a[0] + (b[0]-a[0])*u, a[1] + (b[1]-a[1])*u))
    return out

def gaussian_kernel(sigma_pts):
    r = max(1, int(math.ceil(3*sigma_pts)))
    k = [math.exp(-0.5*(i/sigma_pts)**2) for i in range(-r, r+1)]
    s = sum(k)
    return [v/s for v in k], r

def detect_corners(P, h, scale_units, angle_deg):
    """Turning angle measured across +/- scale_units of arc length."""
    n = len(P)
    k = max(2, int(round(scale_units/h)))
    if n < 4*k: return []
    thr = math.radians(angle_deg)
    ang = [0.0]*n
    for i in range(n):
        ax = P[i][0]-P[(i-k) % n][0]; ay = P[i][1]-P[(i-k) % n][1]
        bx = P[(i+k) % n][0]-P[i][0]; by = P[(i+k) % n][1]-P[i][1]
        na = math.hypot(ax,ay); nb = math.hypot(bx,by)
        if na < 1e-9 or nb < 1e-9: continue
        c = max(-1.0, min(1.0, (ax*bx+ay*by)/(na*nb)))
        ang[i] = math.acos(c)
    corners = []
    win = max(1, k//2)
    for i in range(n):
        if ang[i] < thr: continue
        if all(ang[i] >= ang[(i+j) % n] for j in range(-win, win+1)):
            corners.append(i)
    # de-dup near-neighbours
    out = []
    for c in corners:
        if not out or min((c-out[-1]) % n, (out[-1]-c) % n) > win:
            out.append(c)
    if len(out) > 1 and min((out[0]-out[-1]) % n, (out[-1]-out[0]) % n) <= win:
        out.pop()
    return out

def smooth_closed(P, sigma_pts, corners):
    n = len(P)
    kern, r = gaussian_kernel(sigma_pts)
    if not corners:
        out = []
        for i in range(n):
            x = y = 0.0
            for j, w in enumerate(kern):
                p = P[(i + j - r) % n]; x += w*p[0]; y += w*p[1]
            out.append((x, y))
        return out
    out = list(P)
    cs = sorted(corners)
    for a_i in range(len(cs)):
        a = cs[a_i]; b = cs[(a_i+1) % len(cs)]
        length = (b - a) % n
        if length == 0: length = n      # single corner: one full loop back to it
        if length < 2: continue
        seg = [P[(a+t) % n] for t in range(length+1)]      # inclusive of both corners
        m = len(seg)
        for t in range(1, m-1):
            # taper sigma near the pinned corners so the joint stays clean
            edge = min(t, m-1-t)
            s = min(sigma_pts, edge/1.5)
            if s < 0.35:
                continue
            kk, rr = gaussian_kernel(s)
            x = y = 0.0
            for j, w in enumerate(kk):
                idx = t + j - rr
                idx = max(0, min(m-1, idx))               # clamp inside segment
                x += w*seg[idx][0]; y += w*seg[idx][1]
            out[(a+t) % n] = (x, y)
    return out

# ---------- Schneider cubic fitting ----------
def _q(bez, t):
    u = 1-t
    return (u*u*u*bez[0][0] + 3*u*u*t*bez[1][0] + 3*u*t*t*bez[2][0] + t*t*t*bez[3][0],
            u*u*u*bez[0][1] + 3*u*u*t*bez[1][1] + 3*u*t*t*bez[2][1] + t*t*t*bez[3][1])

def _qp(bez, t):
    u = 1-t
    d = [(3*(bez[i+1][0]-bez[i][0]), 3*(bez[i+1][1]-bez[i][1])) for i in range(3)]
    return (u*u*d[0][0] + 2*u*t*d[1][0] + t*t*d[2][0],
            u*u*d[0][1] + 2*u*t*d[1][1] + t*t*d[2][1])

def _qpp(bez, t):
    d = [(3*(bez[i+1][0]-bez[i][0]), 3*(bez[i+1][1]-bez[i][1])) for i in range(3)]
    dd = [(2*(d[i+1][0]-d[i][0]), 2*(d[i+1][1]-d[i][1])) for i in range(2)]
    return ((1-t)*dd[0][0] + t*dd[1][0], (1-t)*dd[0][1] + t*dd[1][1])

def chord_param(P):
    u = [0.0]
    for i in range(1, len(P)):
        u.append(u[-1] + math.dist(P[i], P[i-1]))
    if u[-1] == 0: return [i/(len(P)-1) for i in range(len(P))]
    return [v/u[-1] for v in u]

def generate_bezier(P, u, t1, t2):
    n = len(P)
    A = []
    for i in range(n):
        t = u[i]; om = 1-t
        A.append(((3*t*om*om*t1[0], 3*t*om*om*t1[1]),
                  (3*t*t*om*t2[0],  3*t*t*om*t2[1])))
    C = [[0.0,0.0],[0.0,0.0]]; X = [0.0,0.0]
    for i in range(n):
        C[0][0] += A[i][0][0]*A[i][0][0] + A[i][0][1]*A[i][0][1]
        C[0][1] += A[i][0][0]*A[i][1][0] + A[i][0][1]*A[i][1][1]
        C[1][0] = C[0][1]
        C[1][1] += A[i][1][0]*A[i][1][0] + A[i][1][1]*A[i][1][1]
        t = u[i]; om = 1-t
        bx = P[i][0] - (om**3*P[0][0] + 3*om*om*t*P[0][0] + 3*om*t*t*P[-1][0] + t**3*P[-1][0])
        by = P[i][1] - (om**3*P[0][1] + 3*om*om*t*P[0][1] + 3*om*t*t*P[-1][1] + t**3*P[-1][1])
        X[0] += A[i][0][0]*bx + A[i][0][1]*by
        X[1] += A[i][1][0]*bx + A[i][1][1]*by
    det = C[0][0]*C[1][1] - C[1][0]*C[0][1]
    seglen = math.dist(P[0], P[-1])
    eps = 1e-12*seglen
    if abs(det) < 1e-12:
        a1 = a2 = seglen/3
    else:
        a1 = (X[0]*C[1][1] - X[1]*C[0][1])/det
        a2 = (C[0][0]*X[1] - C[1][0]*X[0])/det
    if a1 < eps or a2 < eps:
        a1 = a2 = seglen/3
    return [P[0],
            (P[0][0]+t1[0]*a1, P[0][1]+t1[1]*a1),
            (P[-1][0]+t2[0]*a2, P[-1][1]+t2[1]*a2),
            P[-1]]

def reparam(P, u, bez):
    out = []
    for i, p in enumerate(P):
        t = u[i]
        q = _q(bez,t); qp = _qp(bez,t); qpp = _qpp(bez,t)
        num = (q[0]-p[0])*qp[0] + (q[1]-p[1])*qp[1]
        den = qp[0]**2 + qp[1]**2 + (q[0]-p[0])*qpp[0] + (q[1]-p[1])*qpp[1]
        out.append(t if abs(den) < 1e-12 else t - num/den)
    return out

def max_error(P, u, bez):
    mx = 0.0; idx = len(P)//2
    for i in range(1, len(P)-1):
        d = math.dist(_q(bez, u[i]), P[i])
        if d*d > mx: mx = d*d; idx = i
    return mx, idx

def norm(v):
    n = math.hypot(*v)
    return (v[0]/n, v[1]/n) if n > 1e-12 else (0.0, 0.0)

def _try_fit(P, t1, t2, err):
    """Fit one cubic to P; return (bezier, max_err_sq, split_idx)."""
    if len(P) == 2:
        d = math.dist(P[0], P[1])/3
        return ([P[0], (P[0][0]+t1[0]*d, P[0][1]+t1[1]*d),
                 (P[1][0]+t2[0]*d, P[1][1]+t2[1]*d), P[1]], 0.0, 1)
    u = chord_param(P)
    bez = generate_bezier(P, u, t1, t2)
    mx, idx = max_error(P, u, bez)
    if mx >= err*err:
        for _ in range(4):                      # Newton reparameterisation
            u2 = reparam(P, u, bez)
            bez2 = generate_bezier(P, u2, t1, t2)
            mx2, idx2 = max_error(P, u2, bez2)
            if mx2 >= mx: break
            u, bez, mx, idx = u2, bez2, mx2, idx2
            if mx < err*err: break
    return bez, mx, idx

def fit_cubic(P, t1, t2, err):
    """Iterative Schneider fit. No recursion cap: a long noisy segment keeps
    subdividing until it is within `err`, so deep concavities cannot be
    swallowed by a bail-out single curve."""
    n = len(P)
    if n < 2: return []
    out = []
    stack = [(0, n-1, t1, t2)]
    guard = 0
    while stack:
        lo, hi, T1, T2 = stack.pop()
        guard += 1
        if guard > 40000: 
            seg = P[lo:hi+1]
            out.append(_try_fit(seg, T1, T2, err)[0]); continue
        seg = P[lo:hi+1]
        bez, mx, idx = _try_fit(seg, T1, T2, err)
        if mx < err*err or hi - lo < 3:
            out.append(bez); continue
        gi = lo + idx
        if gi <= lo: gi = lo + 1
        if gi >= hi: gi = hi - 1
        c = norm((P[gi-1][0]-P[gi+1][0], P[gi-1][1]-P[gi+1][1]))
        if c == (0.0, 0.0):
            out.append(bez); continue
        stack.append((gi, hi, (-c[0], -c[1]), T2))   # right, popped second
        stack.append((lo, gi, T1, c))                # left,  popped first
    return out

def fit_closed(P, corners, err):
    n = len(P)
    def tan_at(i, fwd):
        k = 2
        if fwd: return norm((P[(i+k) % n][0]-P[i][0], P[(i+k) % n][1]-P[i][1]))
        return norm((P[(i-k) % n][0]-P[i][0], P[(i-k) % n][1]-P[i][1]))
    if corners:
        knots = sorted(corners)
    else:
        knots = [0, n//3, 2*n//3]
    beziers = []
    for a_i in range(len(knots)):
        a = knots[a_i]; b = knots[(a_i+1) % len(knots)]
        length = (b - a) % n
        if length == 0: length = n      # single corner: one full loop back to it
        if length < 1: continue
        seg = [P[(a+t) % n] for t in range(length+1)]
        t1 = norm((seg[1][0]-seg[0][0], seg[1][1]-seg[0][1]))
        t2 = norm((seg[-2][0]-seg[-1][0], seg[-2][1]-seg[-1][1]))
        if a not in corners:   # smooth knot -> use central-difference tangent
            t1 = tan_at(a, True)
        if b not in corners:
            t2 = norm((P[(b-2) % n][0]-P[b][0], P[(b-2) % n][1]-P[b][1]))
        beziers += fit_cubic(seg, t1, t2, err)
    return beziers

corners_set_cache = set()

def fmt(v):
    s = f'{v:.1f}'
    if s.endswith('.0'): s = s[:-2]
    if s == '-0': s = '0'
    return s

def to_d(all_beziers):
    parts = []
    for beziers in all_beziers:
        if not beziers: continue
        p0 = beziers[0][0]
        parts.append(f'M{fmt(p0[0])} {fmt(p0[1])}')
        for b in beziers:
            parts.append(f'C{fmt(b[1][0])} {fmt(b[1][1])} {fmt(b[2][0])} {fmt(b[2][1])} {fmt(b[3][0])} {fmt(b[3][1])}')
        parts.append('Z')
    return ''.join(parts)

def process(d, h=5.0, sigma=40.0, corner_scale=100.0, corner_angle=42.0,
            fit_err=3.0, min_area=900.0, min_perim=120.0):
    subs = flatten(d)
    out = []
    kept = dropped = 0
    for P in subs:
        A = abs(area(P)); L = perimeter(P)
        if A < min_area or L < min_perim:
            dropped += 1
            continue
        kept += 1
        R = resample(P, h)
        if len(R) < 8:
            out.append(fit_closed(R, [], fit_err)); continue
        # scale sigma down for small shapes so detail survives
        s_units = min(sigma, L/28.0)
        cs = detect_corners(R, h, min(corner_scale, L/14.0), corner_angle)
        S = smooth_closed(R, max(0.6, s_units/h), cs)
        bz = fit_closed(S, cs, fit_err)
        if not bz:                      # never silently lose a contour
            bz = fit_closed(S, [], fit_err)
        assert bz, 'contour lost'
        out.append(bz)
    return to_d(out), kept, dropped
