#!/usr/bin/env python3
"""Genera dist-detal/ (tienda al detal) a partir de public/ (catálogo de bodega).
Uso (desde la raíz del repo): python3 detal/build.py
- Copia public/ a dist-detal/ (hardlinks si se puede) y reemplaza index.html.
- Precio al cliente = precio de difusión (detal/precios_base.json, en miles) + incremento (config.json).
- Sin precio en la tabla => 'Consultar precio'.
"""
import json,os,re,shutil,sys
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg=json.load(open(R+'/detal/config.json'))
base=json.load(open(R+'/detal/precios_base.json'))
src=R+'/public';dst=R+'/dist-detal'
if os.path.exists(dst):shutil.rmtree(dst)
try:shutil.copytree(src,dst,copy_function=os.link)
except OSError:
    shutil.rmtree(dst,ignore_errors=True);shutil.copytree(src,dst)
h=open(src+'/index.html').read()
def rep(a,b,n=1):
    global h
    if a not in h:sys.exit('NO ENCONTRADO: '+a[:80])
    h=h.replace(a,b,n)
# precios en D
i=h.index('const D=');j=h.index('];',i);D=json.loads(h[i+8:j+1])
for d in D:
    p=base.get(d['f'])
    if p:d['v']=(p+cfg['incremento'])*1000
    d.pop('x',None);d.pop('d',None)
h=h[:i]+'const D='+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[j+1:]
marca=cfg['marca']
rep('<title>Catálogo zapatillas</title>','<title>%s</title>'%marca)
rep('<header><h1>Catálogo zapatillas</h1><p>Calzado · <span id="tot"></span> modelos disponibles</p></header>',
 '<header><h1>%s</h1><p>Envíos a todo Colombia · <span id="tot"></span> modelos</p></header><div class="ciud">🚚 Enviamos a %s y todo el país. Confirmamos disponibilidad de tallas por WhatsApp.</div>'%(marca,', '.join(cfg['ciudades'])))
rep('</style>','.ciud{font-size:12.5px;color:var(--mute);margin:-4px 0 8px}.pr{font:700 15px var(--body);color:var(--ink);margin-top:2px}.pr.c{font-weight:500;font-size:12px;color:var(--mute)}</style>')
rep('<div class="row" id="fb"></div>\n','')
rep(' chips($("#fb"),[["","Todos",D.length],...Object.keys(BN).filter(k=>cb[k]).map(k=>[k,BN[k],cb[k]])],"b","Stand");','')
rep('+" "+BN[d.b]+" "+BN[d.b].replace("R.","Ref")','')
rep('q[1].textContent=BN[d.b]+" · "+code(d);','q[1].textContent="Ref "+code(d);')
rep('q[4].textContent=d.d||"";if(d.x){const c=document.createElement("div");c.className="cj";c.textContent="📦 También por caja";q[3].after(c)}',
    'q[4].textContent="";{const pr=document.createElement("div");pr.className="pr"+(d.v?"":" c");pr.textContent=d.v?"$"+d.v.toLocaleString("es-CO"):"Consultar precio";q[1].after(pr)}')
rep('"Mi pedido · Catálogo zapatillas"','"Mi pedido · '+marca+'"')
rep('Nosotros confirmamos por WhatsApp la disponibilidad de lo que pidas.','Confirmamos por WhatsApp la disponibilidad y el envío de lo que pidas.')
rep('placeholder="Ej: Necesito 2 de la 40, 2 de la 41, 1 de la 42 (2.40 / 2.41 / 1.42)"','placeholder="Tu nombre y ciudad de envío. Ej: Ana, Medellín"')
rep('Nota general del pedido (opcional)','Tu nombre y ciudad de envío')
# envío del pedido por WhatsApp
wa=re.sub(r'\D','',cfg.get('whatsapp',''))
js='''
(function(){const WA="%s";const s0=sheet;
 function pedido(){let tot=0,sin=0;const L=[...order.entries()].map(([f,s])=>[find(f),s]).filter(([d])=>d).map(([d,s])=>{const n=Object.values(s).reduce((a,b)=>a+b,0)||1;const ts=Object.keys(s).sort((a,b)=>a-b).map(z=>z+" x"+s[z]).join(", ");if(d.v)tot+=d.v*n;else sin++;const nn=(window.__nn[d.f]||"").trim();
  return "• Ref "+code(d)+" "+nom(d)+(d.c?" "+d.c:"")+(d.v?" — $"+d.v.toLocaleString("es-CO"):"")+"\\n  Tallas: "+(ts||"por definir")+(nn?"\\n  Nota: "+nn:"")+"\\n  Foto: "+new URL("p/"+encodeURIComponent(d.f),location.href).href});
  const nt=(window.__nota||"").trim();
  return "Hola, quiero hacer este pedido:\\n\\n"+L.join("\\n\\n")+(tot?"\\n\\nTotal aproximado: $"+tot.toLocaleString("es-CO")+(sin?" (más "+sin+" por cotizar)":"")+" + envío":"")+(nt?"\\n\\nNombre y ciudad: "+nt:"")}
 sheet=function(){s0.apply(this,arguments);const b=document.getElementById("im");if(!b)return;b.textContent="Pedir por WhatsApp";
  b.onclick=()=>{if(!order.size){b.textContent="Agrega un modelo";return}
   const u="https://wa.me/"+WA+"?text="+encodeURIComponent(pedido());window.open(u,"_blank");b.textContent="Pedido enviado";finish(1200)}}})();
'''%wa
k=h.rindex('</script>')
h=h[:k]+js+h[k:]
os.path.exists(dst+'/index.html') and os.remove(dst+'/index.html')  # romper el hardlink: no tocar public/
open(dst+'/index.html','w').write(h)
print('dist-detal listo:',len(D),'modelos;',sum(1 for d in D if d.get('v')),'con precio')
