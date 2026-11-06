#!/usr/bin/env python3
"""Agvysta demo: projektų duomenų paruošimas.
python3 tools/prepare.py  ->  content/projektai.json (iš content/projektai-raw.json, nuskaityto iš agvysta.lt).

Kas daroma:
- pavadinimų rašybos klaidos ir sulipę žodžiai pataisomi (žr. TITLE_FIX);
- užsakovų pavadinimai suvienodinami (kabutės „“, didžiosios raidės, žr. CLIENTS);
- privataus asmens vardas keičiamas į „Privatus užsakovas“;
- iš laikotarpio išskiriami metai (rūšiavimui ir grupavimui);
- iš darbų aprašymo išskiriami ilgiai (L=… m) ir skersmenys (D …);
- projektams priskiriamos paslaugų kategorijos (filtrui ir paslaugų puslapiams);
- ilgieji brūkšniai keičiami trumpais (tipografinė demo taisyklė).
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'content', 'projektai-raw.json')
OUT = os.path.join(ROOT, 'content', 'projektai.json')
IMG = os.path.join(ROOT, 'assets', 'img', 'agvysta', 'projektai')

CLIENTS = {
    'UAB "LAKAJA"': 'UAB „Lakaja“',
    'AB Panevėžio statybos trestas': 'AB „Panevėžio statybos trestas“',
    'AB "PANEVĖŽIO STATYBOS TRESTAS" FILIALAS "GERBŪSTA"': 'AB „Panevėžio statybos trestas“, filialas „Gerbūsta“',
    'AB "PST" filialas "GERBUSTA"': 'AB „Panevėžio statybos trestas“, filialas „Gerbūsta“',
    'UAB "Sintervalas"': 'UAB „Sintervalas“',
    'UAB "Conresta"': 'UAB „Conresta“',
    'UAB "Litcon"': 'UAB „Litcon“', 'UAB "LITCON"': 'UAB „Litcon“',
    'UAB "EIKA"': 'UAB „EIKA“', 'UAB „EIKA“': 'UAB „EIKA“',
    'UAB „SIV STATYBA“': 'UAB „SIV statyba“', 'UAB "SIV Statyba"': 'UAB „SIV statyba“',
    'AB „PANEVĖŽIO KELIAI“': 'AB „Panevėžio keliai“', 'AB "PANEVĖŽIO KELIAI"': 'AB „Panevėžio keliai“',
    'AB "Panevėžio keliai"': 'AB „Panevėžio keliai“', 'AB Panevėžio keliai': 'AB „Panevėžio keliai“',
    'UAB „FEGDA“': 'UAB „Fegda“', 'UAB „Fegda“': 'UAB „Fegda“',
    'UAB "Citus construction"': 'UAB „Citus construction“',
    'Povilas Milašauskas': 'Privatus užsakovas',
    'UAB „Omberg“': 'UAB „Omberg“',
    'UAB „DTC Internacional“': 'UAB „DTC Internacional“',
    'UAB "Vavista"': 'UAB „Vavista“',
    'AB Ogmios centras': 'AB „Ogmios centras“',
    'UAB "Baltijos gildija"': 'UAB „Baltijos gildija“',
    'UAB "Vilbra"': 'UAB „Vilbra“', 'UAB "VILBRA"': 'UAB „Vilbra“',
    'UAB "Geležinkelių projektavimas"': 'UAB „Geležinkelių projektavimas“',
    'UAB "BM būstas"': 'UAB „BM būstas“',
    'UAB "VERSINA"': 'UAB „Versina“',
    'UAB „SANTARIŠKIŲ NAMAI“': 'UAB „Santariškių namai“',
    'IBERDROLA': 'Iberdrola',
    'NESTE LIETUVA, HES-PRO VILNIUS': 'UAB „Neste Lietuva“, UAB „HES-PRO Vilnius“',
    'UAB "KAMINTA': 'UAB „Kaminta“', 'UAB „KAMINTA“': 'UAB „Kaminta“',
    'Mažesniųjų brolių konventualų (pranciškonų) ordino vienuolynas': 'Mažesniųjų brolių konventualų (pranciškonų) ordino vienuolynas',
    'UAB „ORSTA“': 'UAB „Orsta“',
    'UAB „LONSTA“': 'UAB „Lonsta“',
    'UAB „CONSTRUCTUS“': 'UAB „Constructus“',
    'UAB „ASTANA“': 'UAB „Astana“',
    'UAB „VILMESTOS PROJEKTAI“': 'UAB „Vilmestos projektai“',
    'UAB „RANGA IV”': 'UAB „Ranga IV“',
    'UAB „HERMIS CAPITAL“': 'UAB „Hermis Capital“',
    'VĮ „VISAGINO STATYBININKAI“': 'VĮ „Visagino statybininkai“',
    'UAB „TRAKŲ VANDENYS“': 'UAB „Trakų vandenys“',
    'UAB "Romantalis"': 'UAB „Romantalis“',
    'UAB "Sivysta"': 'UAB „Sivysta“',
}

TITLE_FIX = [
    ('VilniujeLauko', 'Vilniuje. Lauko'),
    ('Daugiabutis gyvenamasis namas Linksmoji g., Daugiabutis gyvenamasis namas Linksmoji g.,', 'Daugiabutis gyvenamasis namas Linksmoji g.,'),
    ('mokslninių', 'mokslinių'),
    ('Daugiafukcinis', 'Daugiafunkcinis'),
    ('sandėlys', 'sandėlis'),
    ('inžineriniai tinklais', 'inžineriniai tinklai'),
    ('pastato – siurblinės', 'pastato-siurblinės'),
    ('Ąžuolyno g.5', 'Ąžuolyno g. 5'),
    ('Liepkalnio g.180', 'Liepkalnio g. 180'),
    ('Santariškių g.45', 'Santariškių g. 45'),
    ('Kęstučio Žemaitės g.,Trakuose.', 'Kęstučio ir Žemaitės g., Trakuose'),
    ('“G 1“,“G 3“, “G 4“, “G 5“', '„G 1“, „G 3“, „G 4“, „G 5“'),
    ('"LTD gamybinio pastato 20P1g rekonstrukcijos darbai"', '„LTD gamybinio pastato 20P1g rekonstrukcijos darbai“'),
    ('VŠĮ "Fizikos instituto mokslo ir technologijų parko"', 'VšĮ „Fizikos instituto mokslo ir technologijų parko“'),
    ('Sporto paskirties pastatas priestatas prie "Pramogų arenos"', 'Sporto paskirties pastato priestatas prie „Pramogų arenos“'),
    ('UAB „Autoverslas“ sandėlys', 'UAB „Autoverslas“ sandėlis'),
    ('kad. Nr. 0101/022:267', 'kad. Nr. 0101/0022:267'),
]

CATS = {
    'tinklai': 'Lauko tinklai',
    'siurblines': 'Siurblinės, rezervuarai',
    'zemes': 'Žemės, gerbūvis',
    'spec': 'Specialieji darbai',
}

def clean(s):
    s = s.replace(' – ', ' - ').replace(' — ', ' - ').replace('–', '-').replace('—', '-')
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def fix_title(t):
    for a, b in TITLE_FIX:
        t = t.replace(a, b)
    t = clean(t)
    return t.rstrip('.')

def period_norm(p):
    p = clean(p or '')
    p = re.sub(r'(\d{4})m\.', r'\1 m.', p)
    p = re.sub(r'mėn$', 'mėn.', p)
    return p

def years(p):
    ys = [int(y) for y in re.findall(r'(20\d\d)', p)]
    return (min(ys), max(ys)) if ys else (None, None)

def metrics(text):
    out = []
    for m in re.finditer(r'L\s*=\s*([\d ]+?)\s*m\b', text):
        out.append(int(m.group(1).replace(' ', '')))
    return out

def categorize(title, works):
    t = (title + ' ' + ' '.join(works)).lower()
    cats = []
    if re.search(r'tinkl|vandentiek|nuotek|lietaus|kanaliz|vamzd', t): cats.append('tinklai')
    if re.search(r'siurblin|rezervuar|infiltrac|valymo įreng|gaudykl|drenaž', t): cats.append('siurblines')
    if re.search(r'gerbūv|privažiavimo kel|aikštel|bendrastatyb|griovim', t): cats.append('zemes')
    if re.search(r'atramin|špunt|perėjim|gruntinio|įšal|šiluminės trasos', t): cats.append('spec')
    return cats or ['tinklai']

def image_entry(url):
    base = os.path.splitext(url.split('/')[-1])[0]
    if not os.path.exists(os.path.join(IMG, base + '.webp')):
        return None
    return {'src': f'assets/img/agvysta/projektai/{base}.webp', 'thumb': f'assets/img/agvysta/projektai/{base}-800.webp'}

def build():
    raw = json.load(open(RAW, encoding='utf-8'))
    out = {'kategorijos': CATS, 'vykdomi': [], 'atlikti': []}
    for status in ('vykdomi', 'atlikti'):
        for i, it in enumerate(raw[status]):
            title = fix_title(it['title'])
            client_raw = (it.get('client') or '').strip()
            client = CLIENTS.get(client_raw, clean(client_raw))
            works = [clean(w).rstrip('.') for w in (it.get('works') or []) if clean(w)]
            period = period_norm(it.get('period'))
            y0, y1 = years(period)
            text = title + ' ' + ' '.join(works)
            imgs = [x for x in (image_entry(u) for u in it['images']) if x]
            out[status].append({
                'id': f'{status[0]}{i+1:02d}',
                'pavadinimas': title,
                'laikotarpis': period,
                'metai_nuo': y0, 'metai_iki': y1,
                'vykdomas': period.startswith('nuo') or status == 'vykdomi',
                'uzsakovas': client,
                'darbai': works,
                'ilgiai_m': metrics(text),
                'kategorijos': categorize(title, works),
                'nuotraukos': imgs,
            })
        out[status].sort(key=lambda x: (-(x['metai_nuo'] or 0), x['pavadinimas']))
    # užsakovų rodyklė (visi projektai)
    counts = {}
    for st in ('vykdomi', 'atlikti'):
        for p in out[st]:
            for c in p['uzsakovas'].split(', UAB '):
                c = c if c.startswith(('UAB', 'AB', 'VĮ', 'Iberdrola', 'Mažesniųjų', 'Privatus')) else 'UAB ' + c
                c = c.split(', filialas')[0]
                counts[c] = counts.get(c, 0) + 1
    out['uzsakovai'] = sorted(({'vardas': k, 'projektai': v} for k, v in counts.items() if k != 'Privatus užsakovas'), key=lambda x: (-x['projektai'], x['vardas']))
    tot_len = sum(sum(p['ilgiai_m']) for st in ('vykdomi', 'atlikti') for p in out[st])
    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    n_img = sum(len(p['nuotraukos']) for st in ('vykdomi', 'atlikti') for p in out[st])
    print(f"vykdomi {len(out['vykdomi'])}, atlikti {len(out['atlikti'])}, nuotraukų {n_img}, užsakovų {len(out['uzsakovai'])}, nurodytų ilgių suma {tot_len} m")

if __name__ == '__main__':
    build()
