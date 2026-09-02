#!/usr/bin/env python3
"""ChronicleBench position-window cutter — uniform 10K windows at fixed offsets.

Cuts windows starting at absolute word offsets 0/25K/50K/75K plus a tail-kept ending window,
on paragraph boundaries. Uniform window size at every position so position is the only
variable (F7 caveat). All five windows are scored in v1.1.

  usage: cut-positions.py <manuscript.txt> <outdir> [targetWords=10000]
"""
import sys, json, os

src, outdir = sys.argv[1], sys.argv[2]
target = int(sys.argv[3]) if len(sys.argv) > 3 else 10000
text = open(src).read()
paras = [p for p in text.split('\n\n') if p.strip()]
sizes = [len(p.split()) for p in paras]
total = sum(sizes)
stem = os.path.splitext(os.path.basename(src))[0]
os.makedirs(outdir, exist_ok=True)

def window_at(offset):
    acc, start = 0, len(paras) - 1
    for i, s in enumerate(sizes):
        if acc + s > offset:
            start = i
            break
        acc += s
    out, n = [], 0
    for p, s in zip(paras[start:], sizes[start:]):
        if n + s > target and out:
            break
        out.append(p)
        n += s
    return '\n\n'.join(out), n

def window_end():
    out, n = [], 0
    for p, s in zip(reversed(paras), reversed(sizes)):
        if n + s > target and out:
            break
        out.append(p)
        n += s
    return '\n\n'.join(reversed(out)), n

man = {'source': src, 'total_words': total, 'target_words': target, 'windows': {}}
for name, off in [('opening', 0), ('25k', 25000), ('50k', 50000), ('75k', 75000)]:
    if off >= total:  # censored: manuscript never reached this position
        continue
    body, n = window_at(off)
    f = os.path.join(outdir, f'{stem}--{name}.txt')
    open(f, 'w').write(body)
    man['windows'][name] = {'file': f, 'words': n, 'offset': off}
body, n = window_end()
f = os.path.join(outdir, f'{stem}--ending.txt')
open(f, 'w').write(body)
man['windows']['ending'] = {'file': f, 'words': n}
open(os.path.join(outdir, f'{stem}--windows.json'), 'w').write(json.dumps(man, indent=1))
print(stem, total, {k: v['words'] for k, v in man['windows'].items()})
