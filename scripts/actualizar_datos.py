"""Actualiza productos.js con los precios del dia.

Descarga los JSON que publica a diario el proyecto abierto EasyCompra (MIT,
https://github.com/elopositor/easycompra), los convierte al formato de Cestuki
y escribe productos.js. Si una cadena viene vacia o falla, se aborta sin tocar nada.
"""
import json, re, html, sys, urllib.request
from pathlib import Path
BASE='https://raw.githubusercontent.com/elopositor/easycompra/master/backend/data/'
out_dir=str(Path(__file__).resolve().parent.parent)+'/'
def fetch(name):
    req=urllib.request.Request(BASE+name,headers={'User-Agent':'cestuki-actualizador'})
    with urllib.request.urlopen(req,timeout=120) as r: return json.loads(r.read().decode('utf-8'))
idx=fetch('index.json')
CHAINS=[('merc','mercadona'),('dia','dia'),('carr','carrefour'),('lidl','lidl'),('alim','alimerka')]

def clean(s):
    if not s: return ''
    s=html.unescape(s).replace('\xa0',' ')
    return re.sub(r'\s+',' ',s).strip()

def parse_qty(name):
    n=name.lower().replace(',','.')
    m=re.search(r'(\d+)\s*(?:x|uds?\.?\s*de|unidades\s*de)\s*(\d+(?:\.\d+)?)\s*(kg|gr|g|l|cl|ml)\b',n)
    if m:
        cnt=int(m.group(1)); val=float(m.group(2))*cnt; u=m.group(3)
    else:
        ms=re.findall(r'(\d+(?:\.\d+)?)\s*(kg|gr|g|l|cl|ml)\b',n)
        if not ms: return None
        val=float(ms[-1][0]); u=ms[-1][1]
    if u=='kg': return ('kg',val)
    if u in('g','gr'): return ('kg',val/1000)
    if u=='l': return ('l',val)
    if u=='cl': return ('l',val/100)
    if u=='ml': return ('l',val/1000)

def ref_unit(price,ref,fmt,name):
    f=(fmt or '').strip().lower()
    if ref and ref>0:
        if f in('kg','kilo'): return 'kg',ref
        if f in('l','litro'): return 'l',ref
        if f in('100 g','100g'): return 'kg',ref*10
        if f in('100 ml.','100 ml','100ml'): return 'l',ref*10
        if f in('ud','unidad'): return 'ud',ref
        if f in('dz','docena'): return 'ud',ref/12
    q=parse_qty(name)
    if q and q[1]>0:
        r=price/q[1]
        if 0.05<=r<=500: return q[0],r
    nl=name.lower()
    if re.search(r'\bdocena\b',nl) and 'media' not in nl: return 'ud',price/12
    if re.search(r'media docena',nl): return 'ud',price/6
    m=re.search(r'\b(\d{1,2})\s*(?:ud|uds|unidades|huevos|piezas)\b\.?',nl)
    if m and 2<=int(m.group(1))<=60: return 'ud',price/int(m.group(1))
    return None,None

# Precios anteriores (ofertas) de Mercadona; si falla, se sigue sin ellos
OFERTAS={}
try:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import ofertas_mercadona
    OFERTAS=ofertas_mercadona.ofertas()
    print('ofertas mercadona', len(OFERTAS))
except Exception as e:
    print('Mercadona ofertas: no se pudo leer (%s)' % e)
rows=[]; stats={}
for key,fn in CHAINS:
    d=fetch(fn+'.json')
    n=0; withu=0; seen=set()
    for x in d:
        p=x.get('unit_price')
        if not p or p<=0: continue
        eid=x.get('external_id')
        if eid in seen: continue
        seen.add(eid)
        name=clean(x.get('name')); brand=clean(x.get('brand'))
        if brand in('-','None'): brand=''
        photo=(x.get('photo_url') or '').replace('http://','https://')
        photo=photo.replace('fit=crop&h=300&w=300','fit=crop&h=200&w=200')
        url=x.get('share_url') or ''
        if not url.startswith('https://'): url=''
        u,r=ref_unit(p,x.get('reference_price'),x.get('reference_format'),name)
        fila=[key,name,brand,photo,round(p,2),round(r,2) if r is not None else None,u,url]
        was=OFERTAS.get(str(eid)) if key=='merc' else None
        if was and was>p: fila.append(was)
        rows.append(fila)
        n+=1; withu+= 1 if u else 0
    stats[key]=(n,withu)
for k,(n,w) in stats.items():
    if n<50: sys.exit('Cadena %s con solo %d productos: se aborta sin cambiar nada'%(k,n))
# ALDI: solo ofertas de la semana; si falla no se rompe lo demas
try:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import scrape_aldi
    aldi = scrape_aldi.productos(parse_qty)
    print('aldi productos', len(aldi))
    if len(aldi) >= 20: rows.extend(aldi)
    else: print('ALDI: muy pocos productos, se omite')
except Exception as e:
    print('ALDI: no se pudo leer (%s); se omite' % e)
# El Corte Ingles: lo rellena su propio workflow semanal en datos/eci.json
try:
    f = Path(out_dir) / 'datos' / 'eci.json'
    if f.exists():
        eci = json.loads(f.read_text(encoding='utf-8'))['datos']
        print('eci productos', len(eci)); rows.extend(eci)
except Exception as e:
    print('ECI: no se pudo leer eci.json (%s); se omite' % e)
rows.sort(key=lambda r:(r[0],r[1]))
js='window.PRODUCTOS='+json.dumps({'fecha':idx['updated_at'],'datos':rows},ensure_ascii=False,separators=(',',':'))+';\n'
open(out_dir+'productos.js','w',encoding='utf-8').write(js)
print('fecha',idx['updated_at'],'productos',len(rows),'KB',len(js)//1024)
for k,(n,w) in stats.items(): print(k,'productos',n,'con precio por unidad',w)
