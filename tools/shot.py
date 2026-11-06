#!/usr/bin/env python3
"""Ekrano nuotrauka su headless Chrome. Naudojimas: python3 shot.py <failas.html arba URL> <plotis> <aukštis> <out.png> [sekcijos_aukštis]
Pridedamas ?static=1 (visos animacijos baigtos). Pločiui < 500 naudojamas iframe laikiklis (Chrome lango minimumas 500px).
Jei nurodytas sekcijos aukštis, nuotrauka supjaustoma į dalis out-1.png, out-2.png ..."""
import os, sys, subprocess, tempfile, urllib.parse
from PIL import Image
CH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SCR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_tmp')
os.makedirs(SCR, exist_ok=True)
src, w, h, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
part = int(sys.argv[5]) if len(sys.argv) > 5 else 0
url = src if src.startswith('http') else 'file://' + urllib.parse.quote(os.path.abspath(src))
url += ('&' if '?' in url else '?') + 'static=1'
profile = os.path.join(SCR, 'chrome-profile-' + str(os.getpid()))
if w < 500:
    host = os.path.join(SCR, f'host-{os.getpid()}.html')
    open(host, 'w').write(f'<!doctype html><html><body style="margin:0"><iframe src="{url}" style="width:{w}px;height:{h}px;border:0;display:block"></iframe></body></html>')
    target = 'file://' + host; ww = 520
else:
    target = url; ww = w
subprocess.run([CH, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', f'--user-data-dir={profile}', f'--window-size={ww},{h}', '--virtual-time-budget=12000', f'--screenshot={out}', target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
im = Image.open(out)
if w < 500: im = im.crop((0, 0, w, h)); im.save(out)
print('saved', out, im.size)
if part:
    base = os.path.splitext(out)[0]
    for i, a in enumerate(range(0, im.height, part)):
        im.crop((0, a, im.width, min(a + part, im.height))).save(f'{base}-{i+1}.png')
    print('parts:', (im.height + part - 1) // part)
