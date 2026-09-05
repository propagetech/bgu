import sys, re, importlib, time
sys.path.insert(0,'/private/tmp/claude-501/-Users-chetan-Downloads-jeevitha-ganesha-logo/5c5921ea-3fd5-4a2a-b362-49c546b53336/scratchpad')
import smooth; importlib.reload(smooth)

src = sys.argv[1]; dst = sys.argv[2]
groups = sys.argv[3].split(',')
s = open(src).read()

def path_span(s, gid):
    i = s.index('id="%s"' % gid)
    j = s.index('<path d="', i) + 9
    k = s.index('"', j)
    return j, k

out = s
for gid in groups:
    j, k = path_span(out, gid)
    d = out[j:k]
    t0 = time.time()
    nd, kept, dropped = smooth.process(d)
    print(f'{gid}: {len(d)} -> {len(nd)} chars, contours kept {kept} dropped {dropped}, {time.time()-t0:.1f}s')
    out = out[:j] + nd + out[k:]
open(dst,'w').write(out)
print('wrote', dst, len(out))
