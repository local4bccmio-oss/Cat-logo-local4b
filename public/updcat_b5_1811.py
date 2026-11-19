import re,json,datetime as dt
from PIL import Image
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1])
I=json.load(open('/tmp/b5items.json'))
byf={d['f']:d for d in D}
def tstr(z):
    out=[];run=[]
    for n in z:
        if run and n==run[-1]+1:run.append(n)
        else:
            if run:out.append(run)
            run=[n]
    if run:out.append(run)
    return ' / '.join(('%dEUR'%r[0]) if len(r)==1 else ('%dEUR-%dEUR'%(r[0],r[1]) if len(r)==2 else '%dEUR al %dEUR'%(r[0],r[-1])) for r in out)
MAR={'Boss':'Hugo Boss','Boss TTNM Evo':'Hugo Boss','Onitsuka Tiger':'Onitsuka Tiger','Adidas Superstar':'Adidas','Nike TN Plus':'Nike','New Balance 9060':'New Balance','Adidas Nova Court':'Adidas','Dolce & Gabbana Sorrento':'Otras'}
s0=max(d['s'] for d in D)+1;u=max(d.get('u',0) for d in D)+1
new=[];TW,TH=420,525;sh=Image.new('RGB',(4*TW,3*TH),'white')
for it in I:
    if it['st']!='NUEVA':continue
    f=it['stem']+'.jpg';assert f not in byf
    pair=len(it['refs'])==2;z=it['z']
    e=dict(f=f,b='B5',n=it['name'],r=['5'+r for r in it['refs']],t=it['tal'].replace(' / ',' - ') if pair else it['tal'],c=it['col'],z=z,g='DH' if pair else ('D' if max(z)<=39 else 'H'),m=MAR[it['name']],s=s0,i=len(new),u=u,d='18/11')
    if it['caja']:e['x']=1
    k=len(new);new.append(e)
    im=Image.open('/tmp/b5out/'+it['fn']).convert('RGB')
    im.resize((640,800),Image.LANCZOS).save('p/'+f,quality=80,optimize=True)
    im.thumbnail((TW,TH),Image.LANCZOS);sh.paste(im,((k%4)*TW+(TW-im.width)//2,(k//4)*TH+(TH-im.height)//2))
sh.save(f's/{s0:03d}.jpg',quality=66,optimize=True)
seen=0;nz=0
for it in I:
    if it['st']!='REPOST':continue
    for f in it['ents']:
        d=byf.get(f)
        if not d:continue
        seen+=1;d['d']='18/11';d.pop('a',None);d.pop('h',None)
        if it['caja']:d['x']=1
        elif 'x' in d and len(it['refs'])==1:d.pop('x')
        z=it['z']
        if d['g']=='D':zz=[n for n in z if n<=39]
        elif d['g']=='H':zz=[n for n in z if n>=40]
        else:zz=z
        if zz and zz!=d['z']:
            d['z']=zz
            d['t']=tstr(zz) if d['g'] in 'DH' else ' - '.join(t for t in (tstr([n for n in zz if n<=39]),tstr([n for n in zz if n>=40])) if t)
            nz+=1
AG=dt.date(2026,11,14);HI=dt.date(2026,11,10);st=dict(a=0,h=0,pocas=0)
for d in D+new:
    if d['b']!='B5' or not d.get('d'):continue
    q=dt.date(2026,int(d['d'][3:5]),int(d['d'][:2]))
    if q<=AG:d['a']=1;st['a']+=1
    if q<=HI:d['h']=1;st['h']+=1
    if d['d']=='18/11' and len(d['z'])<=3:d['a']=1;st['pocas']+=1
D+=new
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
open('index.html','w',encoding='utf-8').write(h)
print('nuevas',len(new),'vistas',seen,'tallas',nz,st)
