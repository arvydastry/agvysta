#!/usr/bin/env python3
"""Statinė patikra: python3 tools/check.py
Tikrina vietines nuorodas (href, src, srcset, data-src, data-gallery, poster), inkarus, h1 skaičių, alt atributus,
ilguosius brūkšnius matomame tekste ir ar failai nėra tušti / iškelti į iCloud (dataless)."""
import glob, os, re, sys, html as H
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
pages = sorted(glob.glob('*.html'))
problems = []
ids = {}
for p in pages:
    s = open(p, encoding='utf-8').read()
    ids[p] = set(re.findall(r'\sid="([^"]+)"', s))
for p in pages:
    s = open(p, encoding='utf-8').read()
    refs = set()
    for attr in ('href', 'src', 'data-src', 'poster'):
        refs |= set(re.findall(rf'\s{attr}="([^"]+)"', s))
    for ss in re.findall(r'srcset="([^"]+)"', s):
        refs |= {x.strip().split(' ')[0] for x in ss.split(',')}
    for g in re.findall(r'data-gallery="([^"]+)"', s):
        refs |= set(g.split('|'))
    for r in refs:
        r = H.unescape(r)
        if re.match(r'^(https?:|mailto:|tel:|#$|data:)', r):
            continue
        path, _, frag = r.partition('#')
        path = path.split('?')[0]
        if path and not os.path.exists(path):
            problems.append(f'{p}: nerastas {r}')
        elif path and os.path.isfile(path) and os.path.getsize(path) == 0:
            problems.append(f'{p}: tuščias {r}')
        if frag and frag not in ids.get(path or p, set()):
            problems.append(f'{p}: nėra inkaro {r}')
    if s.count('<h1') != 1:
        problems.append(f'{p}: h1 skaičius {s.count("<h1")}')
    for tag in re.findall(r'<img\b[^>]*>', s):
        if ' alt=' not in tag:
            problems.append(f'{p}: img be alt {tag[:80]}')
    vis = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', s, flags=re.S)
    vis = re.sub(r'<[^>]+>', ' ', vis)
    if re.search('[–—]', vis):
        problems.append(f'{p}: ilgasis brūkšnys tekste')
# iCloud dataless
try:
    import subprocess
    out = subprocess.run(['find', 'assets', '-type', 'f', '-flags', '+dataless'], capture_output=True, text=True).stdout.split()
    for f in out:
        problems.append(f'iCloud iškėlė failą (paleiskite sh tools/hydrate.sh): {f}')
except Exception:
    pass
print('\n'.join(problems) if problems else f'{len(pages)} puslapiai, problemų nėra')
sys.exit(1 if problems else 0)
