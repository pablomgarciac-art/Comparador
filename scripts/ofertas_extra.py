"""Precios anteriores (ofertas) de Lidl y Alimerka.  Devuelven {id_producto: precio_anterior}."""
import html, json, re, time, urllib.request, urllib.parse, http.cookiejar

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36'

def _abrir():
    cj = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj)), cj

def _get(op, url, accept='*/*', extra=None):
    h = {'User-Agent': UA, 'Accept': accept, 'Accept-Language': 'es-ES,es;q=0.9'}
    h.update(extra or {})
    for i in range(3):
        try:
            with op.open(urllib.request.Request(url, headers=h), timeout=60) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception as e:
            err = e; time.sleep(2 * (i + 1))
    raise err

def lidl():
    op, _ = _abrir(); out = {}; leidos = 0; muestra = None
    for _p in range(200):
        q = urllib.parse.urlencode({'q': '*', 'offset': leidos, 'fetchsize': 100, 'locale': 'es_ES', 'assortment': 'ES', 'version': '2.1.0'})
        d = json.loads(_get(op, 'https://www.lidl.es/q/api/search?' + q))
        items = d.get('items') or []
        if not items: break
        leidos += len(items)
        for it in items:
            data = ((it.get('gridbox') or {}).get('data')) or {}
            pr = data.get('price') or {}
            ant = pr.get('oldPrice')
            if muestra is None and ant: muestra = pr
            try:
                if ant and float(ant) > float(pr.get('price')):
                    out[str(data.get('productId') or data.get('erpNumber') or data.get('itemId') or data.get('id'))] = round(float(ant), 2)
            except (TypeError, ValueError):
                pass
        if leidos >= (d.get('numFound') or 0): break
        time.sleep(0.3)
    print('lidl: %d articulos, %d con precio anterior; muestra precio: %s' % (leidos, len(out), json.dumps(muestra)[:300] if muestra else '-'))
    return out

def alimerka():
    BASE = 'https://www.alimerkaonline.es'; SITIO = BASE + '/on/demandware.store/Sites-Alimerka-Site/default'
    op, cj = _abrir(); out = {}
    _get(op, BASE + '/')
    _get(op, SITIO + '/Stores-FindByZipcode?consent=true&zipCode=33001', 'application/json', {'X-Requested-With': 'XMLHttpRequest'})
    cj.set_cookie(http.cookiejar.Cookie(0, 'logged', 'true', None, False, 'www.alimerkaonline.es', True, False, '/', True, False, None, False, None, None, {}))
    tarjeta = re.compile(r'<div class="product" data-pid="([^"]+)">(.*?)(?=<div class="product" data-pid=|\Z)', re.S)
    total = 0; muestra = None
    for sec in ['101', '103', '104', '201', '202', '203', '204', '206', '10201', '10205', '10299']:
        ini = 0
        while True:
            try: t = _get(op, SITIO + '/Search-UpdateGrid?' + urllib.parse.urlencode({'cgid': sec, 'start': ini, 'sz': 500}))
            except Exception as e:
                print('alimerka oferta: fallo', sec, e); break
            tarj = tarjeta.findall(t); total += len(tarj)
            for pid, bloque in tarj:
                m = re.search(r'class="strike-through[^"]*">\s*<span class="value"[^>]*content="([\d.]+)"', bloque)
                a = re.search(r'class="sales">\s*<span class="value" content="([\d.]+)"', bloque)
                if m and a and float(m.group(1)) > float(a.group(1)):
                    out[pid] = round(float(m.group(1)), 2)
                    if muestra is None: muestra = bloque[:0]
            if len(tarj) < 500: break
            ini += 500
            time.sleep(0.3)
        time.sleep(0.3)
    print('alimerka: %d tarjetas, %d con precio anterior' % (total, len(out)))
    return out
