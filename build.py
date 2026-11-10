#!/usr/bin/env python3
"""Agvysta demo: statinis generatorius.
python3 build.py  ->  sugeneruoja *.html iš templates/ ir content/*.json (reikia jinja2).
Projektų duomenys: python3 tools/prepare.py (content/projektai-raw.json -> content/projektai.json).
"""
import glob, json, os, re, sys
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, 'content')

def load(name):
    with open(os.path.join(CONTENT, name + '.json'), encoding='utf-8') as f:
        return json.load(f)

def gallery(folder):
    """Originalios agvysta.lt galerijos nuotraukos (assets/img/agvysta/galerija/<folder>--*.webp)."""
    files = sorted(glob.glob(os.path.join(ROOT, 'assets/img/agvysta/galerija', f'{folder}--*.webp')))
    files = [f for f in files if not f.endswith('-800.webp')]
    return [os.path.relpath(f, ROOT)[:-5] for f in files]

def img_size(base):
    """Grąžina (plotis, aukštis) WebP failui, kad naršyklė rezervuotų vietą (CLS)."""
    try:
        from PIL import Image
        with Image.open(os.path.join(ROOT, base + '-800.webp')) as im:
            return im.size
    except Exception:
        return (800, 600)

def nbsp_fix(html):
    """Trumpi žodeliai ir skaičius + vienetas nelieka eilutės gale."""
    def rep(m):
        t = m.group(0)
        t = re.sub(r'(?<=\s)(ir|ar|bei|su|be|iš|į|už|po|per|nuo|iki|prie|ant|apie|nr\.|Nr\.|m\.) ', lambda x: x.group(1) + '\u00a0', t)
        t = re.sub(r'(\d) (m|mm|km|metų|m\.)(?=[\s,.<)])', '\\1\u00a0\\2', t)
        t = re.sub(r'(?<=\S) (g\.|pr\.|al\.|k\.|raj\.)(?=[\s,.<)])', '\u00a0\\1', t)
        t = re.sub(r'\b(g\.|pr\.|al\.) (?=\d)', '\\1\u00a0', t)
        t = re.sub(r'\b(ISO|OHSAS|EN|LST|BS) (?=[\dA-Z])', '\\1\u00a0', t)
        return t
    parts = re.split(r'(<(?:script|style|textarea)[^>]*>.*?</(?:script|style|textarea)>)', html, flags=re.S)
    return ''.join(p if p.startswith(('<script', '<style', '<textarea')) else re.sub(r'>[^<]+<', rep, p) for p in parts)

DASH = re.compile('[\u2013\u2014]')

LEGAL = re.compile(r'^(UAB|AB|VĮ|VšĮ)\s+')

def client_wall(pj, logos):
    """Užsakovų sienelė: logotipas, jei turime, kitaip pavadinimas (teisinė forma atskirai)."""
    by_name = {}
    for l in logos:
        by_name[l['vardas']] = l
        by_name[l['vardas'].split(' (')[0]] = l
    alias = {'UAB „Neste Lietuva“': 'UAB „Neste Lietuva“', 'AB „Ogmios centras“': 'Ogmios grupė (AB „Ogmios centras“)'}
    tiles = []
    for c in pj['uzsakovai']:
        name = c['vardas']
        logo = by_name.get(name) or by_name.get(alias.get(name, ''))
        m = LEGAL.match(name)
        forma = m.group(1) if m else ''
        pav = LEGAL.sub('', name).replace('„', '').replace('“', '')
        tiles.append({'vardas': name, 'forma': forma, 'pav': pav, 'n': c['projektai'], 'logo': logo})
    return tiles

def main():
    site = load('site')
    pj = load('projektai')
    allp = {p['id']: p for st in ('vykdomi', 'atlikti') for p in pj[st]}
    for p in allp.values():
        p['statusas'] = 'vykdomi' if p['id'].startswith('v') else 'atlikti'
    featured = []
    for f in site['atrinkti_projektai']:
        p = dict(allp[f['id']])
        p['trumpas'] = f['trumpas']
        p['virselis'] = p['nuotraukos'][f['virselis']] if p['nuotraukos'] else None
        featured.append(p)
    # ilgiausios trasos (realūs ilgiai iš projektų sąrašo)
    trasos = []
    for t in site['trasos']:
        p = dict(allp[t['id']]); p['trumpas'] = t['pavadinimas']; p['ilgis'] = p['ilgiai_m'][0]
        trasos.append(p)
    su_ilgiu = [p for p in allp.values() if p['ilgiai_m']]
    trasu_suvestine = {'projektai': len(su_ilgiu), 'metrai': sum(p['ilgiai_m'][0] for p in su_ilgiu), 'max': max(t['ilgis'] for t in trasos)}
    for s in site['paslaugos']:
        s['nuotraukos'] = gallery(s['galerija']) if s.get('galerija') else s.get('galerija_rinkinys', [])
        s['projektai'] = [p for p in sorted(allp.values(), key=lambda x: (not x['nuotraukos'], -(x['metai_nuo'] or 0))) if s['kategorija'] in p['kategorijos']]
        s['projektai_su_foto'] = [p for p in s['projektai'] if p['nuotraukos']]
        s['nuo_metu'] = min((p['metai_nuo'] for p in s['projektai'] if p['metai_nuo']), default=None)
    # projektų grupavimas pagal metus (projektų puslapiui)
    def by_year(items):
        groups = {}
        for p in items:
            groups.setdefault(p['metai_nuo'] or 0, []).append(p)
        return sorted(groups.items(), key=lambda x: -x[0])

    env = Environment(loader=FileSystemLoader(os.path.join(ROOT, 'templates')), autoescape=select_autoescape(['html']), trim_blocks=True, lstrip_blocks=True)
    env.globals.update(site=site, imone=site['imone'], paslaugos=site['paslaugos'], img_size=img_size)
    env.filters['thousands'] = lambda n: f'{n:,}'.replace(',', '\u00a0')

    pages = {
        'index.html': ('index.html', dict(page='index', featured=featured, pj=pj, allp=allp, trasos=trasos, trasu=trasu_suvestine, logotipai=load('logotipai'), uzsakovu_sienele=client_wall(pj, load('logotipai')))),
        'projektai.html': ('projektai.html', dict(page='projektai', pj=pj, by_year=by_year)),
        'apie-mus.html': ('apie-mus.html', dict(page='apie', allp=allp)),
        'karjera.html': ('karjera.html', dict(page='karjera')),
        'kontaktai.html': ('kontaktai.html', dict(page='kontaktai')),
        'duomenu-apsauga.html': ('duomenu-apsauga.html', dict(page='privatumas')),
    }
    for s in site['paslaugos']:
        others = [o for o in site['paslaugos'] if o['slug'] != s['slug']]
        pages[s['slug'] + '.html'] = ('paslauga.html', dict(page='paslaugos', s=s, others=others))

    problems = 0
    for out, (tpl, ctx) in pages.items():
        html = env.get_template(tpl).render(**ctx)
        html = nbsp_fix(html)
        visible = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.S)
        if DASH.search(re.sub(r'<[^>]+>', '', visible)):
            print(f'  ! {out}: rastas ilgasis brūkšnys', file=sys.stderr); problems += 1
        with open(os.path.join(ROOT, out), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  {out}')
    print(f'Sugeneruota {len(pages)} puslapių' + (f', problemų: {problems}' if problems else ''))

if __name__ == '__main__':
    main()
