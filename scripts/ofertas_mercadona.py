"""Precios anteriores (ofertas) de Mercadona, leidos de su API publica de la tienda online.

Devuelve {id_producto: precio_anterior} solo para los productos cuyo precio ha bajado.
"""
import json, time, urllib.request

BASE = 'https://tienda.mercadona.es/api'
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

def _get(ruta):
    req = urllib.request.Request(BASE + ruta, headers={'User-Agent': UA, 'Accept': 'application/json'})
    for i in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            err = e; time.sleep(2 * (i + 1))
    raise err

def ofertas():
    out = {}
    arbol = _get('/categories/').get('results', [])
    ids = [c['id'] for cat in arbol for c in cat.get('categories', [])]
    for cid in ids:
        try: datos = _get('/categories/%s/' % cid)
        except Exception as e:
            print('mercadona oferta: fallo categoria', cid, e); continue
        for sub in datos.get('categories', []):
            for p in sub.get('products', []):
                pi = p.get('price_instructions') or {}
                try:
                    ahora = float(pi.get('unit_price')); antes = float(pi.get('previous_unit_price'))
                except (TypeError, ValueError):
                    continue
                if pi.get('price_decreased') and antes > ahora:
                    out[str(p['id'])] = round(antes, 2)
        time.sleep(0.25)
    return out

if __name__ == '__main__':
    o = ofertas(); print(len(o), 'ofertas de Mercadona'); print(list(o.items())[:5])
