"""Produce the redrawn logo SVGs.

Lettering contours are rebuilt two ways - font-guided warp (Cinzel for Latin,
Baloo Tamma 2 for Kannada) and a direct corner-preserving refit of the trace -
and the more faithful of the two is kept per contour.  Artwork contours get the
de-serration pass.  Every choice is measured, not assumed.
"""
import sys, os, math, json; sys.path.insert(0,'.')
import numpy as np, smooth, redraw, word_redraw as wr, structwarp as sw, specimen as sp
from scipy.spatial import cKDTree

RAW_KN='/Users/chetan/Downloads/jeevitha/ganesha-logo/vector/_raw-trace/kannada-original.svg'
RAW_EN='/Users/chetan/Downloads/jeevitha/ganesha-logo/vector/english-original.svg'

# lettering regions, in display coords (x0,y0,x1,y1) -> (label, font, text, smallcap)
LETTERING = {
 'kannada': {
   'ink':  [((930,1540,2875,2235),  'KN ganesha',    'ttf/BalooTamma2-800.ttf', 'ಗಣೇಶ', None),
            ((1660,920,2215,1175),  'KN 10ne',        None, None, None)],
   'text': [((1100,1280,2760,1640), 'KN bellanduru',  'ttf/BalooTamma2-700.ttf', 'ಬೆಳ್ಳಂದೂರು', None),
            ((1240,2240,2660,2700), 'KN utsava',      'ttf/BalooTamma2-700.ttf', 'ಉತ್ಸವ', None)],
 },
 'english': {
   'ink':  [((900,1650,2990,2300),  'EN GANESHA',     None, None, None),
            ((1660,940,2150,1220),  'EN 10th',        None, None, None),
            ((1640,2930,2140,3050), 'EN 2026',        None, None, None)],
   'text': [((1150,1280,2670,1620), 'EN BELLANDURU',  'ttf/Cinzel-700.ttf', 'BELLANDURU', 0.86),
            ((1275,2265,2620,2645), 'EN UTSAVA',      'ttf/Cinzel-700.ttf', 'UTSAVA', 0.847)],
 },
}

def get_d(s, gid):
    i=s.index('id="%s"'%gid); j=s.index('<path d="',i)+9; k=s.index('"',j); return j,k,s[j:k]

def in_box(P, box):
    xs=[p[0]/10 for p in P]; ys=[3762-p[1]/10 for p in P]
    return box[0]<=min(xs) and max(xs)<=box[2] and box[1]<=min(ys) and max(ys)<=box[3]

def deserrate(P):
    return wr.smooth_trace(np.asarray(P,float))

def run_group(s, gid, regions, log):
    j,k,d = get_d(s, gid)
    subs = smooth.flatten(d, tol=1.0)
    # which region each contour belongs to
    owner = {}
    for ri,(box,label,font,text,scv) in enumerate(regions):
        for ci,P in enumerate(subs):
            if ci not in owner and in_box(P, box): owner[ci]=ri
    out=[None]*len(subs)
    # 1. artwork contours: de-serrate + faithful refit
    for ci,P in enumerate(subs):
        if ci in owner: continue
        A=abs(smooth.area(P)); L=smooth.perimeter(P)
        if A<900 or L<120: out[ci]=[]; continue
        S=deserrate(P); out[ci]=wr.refit(S, 3.0)
    # 2. lettering contours
    for ri,(box,label,font,text,scv) in enumerate(regions):
        idx=[ci for ci,r in owner.items() if r==ri]
        if not idx: log.append((label,'MISSING',0,0,0,0)); continue
        tgt={ci: deserrate(subs[ci]) for ci in idx}
        warped={}
        if font and text:
            try:
                tasp=(lambda A:(A[:,0].max()-A[:,0].min())/(A[:,1].max()-A[:,1].min()))(
                     np.vstack([tgt[ci] for ci in idx]))
                track=sp.fit_track(font, text, tasp, scv)
                src=[np.asarray(c,float) for c in sp.word_cs(font, text, scv, track)]
                order=sorted(idx)
                M=redraw.icp_affine(src, [tgt[ci] for ci in order])
                src=[np.asarray(c) for c in redraw.apply_aff(src, M)]
                for i,jj,cost in wr.pair_up(src, [tgt[ci] for ci in order]):
                    if cost>0.55: continue
                    ci=order[jj]
                    try:
                        S=redraw.warp2(src[i], tgt[ci], 9.0)
                        warped[ci]=wr.refit(S, 12.0)
                    except Exception: pass
            except Exception as e:
                log.append((label,'warp-failed:'+str(e)[:40],0,0,0,0))
        nw=nr=0; rms_all=[]; mx_all=[]; nodes=0
        for ci in idx:
            direct=wr.refit(tgt[ci], 10.0)
            dr,dm = wr.resid(direct, tgt[ci])
            pick, kind, r, m = direct, 'refit', dr, dm
            if ci in warped:
                wrms,wmx = wr.resid(warped[ci], tgt[ci])
                if wrms <= dr + 0.5 and len(warped[ci]) <= len(direct):
                    pick, kind, r, m = warped[ci], 'warp', wrms, wmx
            out[ci]=pick; nodes+=len(pick); rms_all.append(r); mx_all.append(m)
            if kind=='warp': nw+=1
            else: nr+=1
        log.append((label, f'{nw} warp / {nr} refit', len(idx),
                    max(rms_all)/10, max(mx_all)/10, nodes))
    newd = smooth.to_d([b for b in out if b])
    return s[:j] + newd + s[k:], len(d), len(newd)

def run(src, dst, which):
    s=open(src).read(); log=[]
    for gid, regions in LETTERING[which].items():
        s, a, b = run_group(s, gid, regions, log)
        print(f'  {gid}: {a} -> {b} chars')
    for row in log:
        print(f'    {row[0]:16s} {str(row[1]):18s} {row[2]:2d} contours  rms {row[3]:.2f}px  max {row[4]:.2f}px  {row[5]} beziers')
    open(dst,'w').write(s); print('  wrote', dst)

if __name__=='__main__':
    which=sys.argv[1]
    run(RAW_KN if which=='kannada' else RAW_EN, sys.argv[2], which)
