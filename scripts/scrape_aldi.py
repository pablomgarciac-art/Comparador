"""Ofertas de ALDI (alimentacion y bazar) leidas de https://www.aldi.es/ofertas.html

ALDI no publica un catalogo con precios fijos en su web: solo las ofertas de la semana.
Los datos viajan dentro de la propia pagina (bloque __NEXT_DATA__), asi que basta una peticion HTTP.
Devuelve filas en el formato de Cestuki: [cadena, nombre, marca, foto, precio, ref, unidad, url]
"""
import json, re, time, html, urllib.request

PAGINAS = ['https://www.aldi.es/ofertas.html']
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

def _get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'es-ES,es;q=0.9'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode('utf-8', 'replace')

def _walk(o, out, seen):
    if isinstance(o, str):
        if len(o) > 50 and o[0] in '[{':
            try: _walk(json.loads(o), out, seen)
            except Exception: pass
        return
    if isinstance(o, list):
        for x in o: _walk(x, out, seen)
        return
    if isinstance(o, dict):
        if o.get('productSlug') and o.get('currentPrice') and o['productSlug'] not in seen:
            seen.add(o['productSlug']); out.append(o)
        for v in o.values(): _walk(v, out, seen)

def _precio(p, ahora):
    """Precio vigente hoy: el mas bajo entre el normal y las promociones activas.
    Se ignoran promos del tipo '2a unidad al -50%' o '2x1': ahi el precio suelto no baja."""
    cands = [p.get('currentPrice') or {}] + list(p.get('promotionPrices') or [])
    validos = []
    for c in cands:
        a, b = c.get('validFrom'), c.get('validUntil')
        if not c.get('priceValue') or not a or not b or not (a <= ahora <= b): continue
        promo = ((c.get('priceTagLabels') or {}).get('promoText1') or '').lower()
        if re.search(r'unidad|\bud\b|\dx\d|ª|º|\+', promo): continue
        validos.append(c)
    if validos: return min(validos, key=lambda c: c['priceValue'])
    c = p.get('currentPrice') or {}
    if c.get('priceValue') and (not c.get('validFrom') or c['validFrom'] <= ahora):
        return c
    return None

def productos(parse_qty=None):
    ahora = int(time.time()); filas = []; vistos = set()
    for url in PAGINAS:
        t = _get(url)
        m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', t, re.S)
        if not m: raise RuntimeError('ALDI: la pagina no trae __NEXT_DATA__ (cambio de web o bloqueo)')
        items = []; _walk(json.loads(m.group(1)), items, set())
        for p in items:
            slug = p['productSlug']
            if slug in vistos or p.get('isAvailable') is False or p.get('isComingSoon'): continue
            c = _precio(p, ahora)
            if not c: continue
            price = float(c['priceValue'])
            name = html.unescape(re.sub(r'\s+', ' ', p.get('name') or '')).strip()
            brand = html.unescape(re.sub(r'[®™]', '', p.get('brandName') or '')).strip()
            if not name or price <= 0: continue
            foto = ''
            for a in p.get('assets') or []:
                if a.get('type') == 'primary' and a.get('url'):
                    foto = a['url'].replace('http://', 'https://') + '?wid=200&fmt=jpeg&qlt=80'; break
            ref = unit = None
            for b in c.get('basePrice') or []:
                s = (b.get('basePriceScale') or '').lower()
                if b.get('basePriceValue') and s in ('kg', 'l'):
                    ref, unit = float(b['basePriceValue']), s; break
            if ref is None and parse_qty:
                q = parse_qty((name + ' ' + (p.get('salesUnit') or '')).strip())
                if q and q[1] > 0:
                    r = price / q[1]
                    if 0.05 <= r <= 500: unit, ref = q[0], r
            vistos.add(slug)
            filas.append(['aldi', name, brand, foto, round(price, 2), round(ref, 2) if ref is not None else None, unit,
                          'https://www.aldi.es/producto/' + slug + '.html'])
    return filas

if __name__ == '__main__':
    f = productos()
    print(len(f), 'productos de ALDI'); print(f[:3])
