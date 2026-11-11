"""Supermercado El Corte Ingles: recorre las categorias de https://www.elcorteingles.es/supermercado/
y guarda los productos con precio en datos/eci.json (formato Cestuki).

Es un recorrido largo (miles de paginas), asi que corre en su propio workflow semanal.
Uso:  python3 scripts/scrape_eci.py          # completo
      python3 scripts/scrape_eci.py --probe  # solo prueba: 1 categoria, 2 paginas
"""
import gzip, html, json, re, sys, time, urllib.request
from pathlib import Path
from bs4 import BeautifulSoup

BASE = 'https://www.elcorteingles.es'
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
OUT = Path(__file__).resolve().parent.parent / 'datos' / 'eci.json'
PAUSA = 0.8
LIMITE_S = 4 * 3600   # corta a las 4 horas y guarda lo que lleve

def get(path):
    req = urllib.request.Request(BASE + path, headers={'User-Agent': UA, 'Accept-Language': 'es-ES,es;q=0.9',
                                                       'Accept': 'text/html', 'Accept-Encoding': 'gzip'})
    for intento in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                b = r.read()
                if r.headers.get('Content-Encoding') == 'gzip': b = gzip.decompress(b)
                return b.decode('utf-8', 'replace')
        except Exception as e:
            err = e; time.sleep(3 * (intento + 1))
    raise err

def enlaces(t, patron):
    s = BeautifulSoup(t, 'lxml')
    return sorted({a['href'] for a in s.find_all('a', href=True) if re.match(patron, a['href'])})

def num(x):
    return float(x.replace('.', '').replace(',', '.'))

def tarjetas(t):
    s = BeautifulSoup(t, 'lxml'); out = []
    for e in s.select('.food-product-preview-responsive'):
        pr = e.select_one('.food-prices__price'); a = e.select_one('a.food-product-preview-responsive__link')
        if not pr or not a: continue
        m = re.search(r'([\d.]+,\d{2})', pr.get_text())
        if not m: continue
        price = num(m.group(1)); img = e.select_one('img')
        alt = html.unescape((img.get('alt') if img else '') or '').strip()
        name, brand = alt, ''
        if ' - ' in alt: name, brand = alt.rsplit(' - ', 1)
        name = re.sub(r'\s+', ' ', name).strip()
        if name: name = name[0].upper() + name[1:]
        ref = unit = None
        u = e.select_one('.food-prices__measurement-unit')
        if u:
            mu = re.search(r'([\d.]+,\d{2})\s*€\s*/\s*(kg|l|ud|litro|unidad)', u.get_text(' '), re.I)
            if mu:
                unit = {'litro': 'l', 'unidad': 'ud'}.get(mu.group(2).lower(), mu.group(2).lower()); ref = num(mu.group(1))
        out.append(['eci', name, brand.strip(), (img.get('src') if img else '') or '', round(price, 2),
                    round(ref, 2) if ref is not None else None, unit, BASE + a['href']])
    return out

def main():
    sonda = '--probe' in sys.argv; t0 = time.time()
    home = get('/supermercado/')
    cats = [c for c in enlaces(home, r'^/supermercado/[a-z][a-z0-9-]+/$') if 'exclusivo' not in c]
    print('categorias:', len(cats))
    subs = []
    for c in cats[:1] if sonda else cats:
        try: ss = enlaces(get(c), r'^' + re.escape(c) + r'[a-z][a-z0-9-]+/$')
        except Exception as e: print('fallo', c, e); ss = []
        subs += ss or [c]; time.sleep(PAUSA)
    print('subcategorias:', len(subs))
    vistos = {}; 
    for i, sc in enumerate(subs[:1] if sonda else subs):
        if time.time() - t0 > LIMITE_S: print('limite de tiempo'); break
        for pag in range(1, 3 if sonda else 80):
            try: t = get(sc + ('?page=%d' % pag if pag > 1 else ''))
            except Exception as e: print('fallo', sc, pag, e); break
            nuevas = 0
            for f in tarjetas(t):
                if f[7] not in vistos: vistos[f[7]] = f; nuevas += 1
            time.sleep(PAUSA)
            if nuevas == 0: break
        if i % 10 == 0: print(i, '/', len(subs), 'productos', len(vistos), flush=True)
    filas = list(vistos.values())
    print('TOTAL', len(filas)); print(filas[:3])
    if sonda: return
    if len(filas) < 500: sys.exit('Muy pocos productos de El Corte Ingles: no se guarda nada')
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({'fecha': time.strftime('%Y-%m-%d'), 'datos': filas}, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')

if __name__ == '__main__':
    main()
