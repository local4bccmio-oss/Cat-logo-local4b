import re,json,math,datetime as dt
from PIL import Image
h=open('index.html').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1])
items=json.load(open('/tmp/b4items.json'));S=json.load(open('/tmp/b4send.json'))
# nuevas
new=[]
s0=max(d['s'] for d in D)+1;u=max(d.get('u',0) for d in D)+1
for k,x in enumerate(S['items']):
    f=x['fn']
    if any(d['f']==f for d in D):continue
    parts=f[:-4].split('_');refs=[parts[0][:-2]]+[('4'+p[:-2]) for p in parts[1:]]
    e=dict(f=f,b='B4',n=x['name']+'*',r=[parts[0][:-2]],t=x['tal'],c=x['col'],z=x['z'],g=x['g'],m='Nike',s=s0,i=len(new),u=u,d='18/11')
    if x['caja']:e['x']=1
    new.append(e)
TW,TH=420,525
sh=Image.new('RGB',(4*TW,3*TH),'white')
for e,x in zip(new,[y for y in S['items'] if any(y['fn']==n['f'] for n in new)]):
    im=Image.open('/tmp/b4out/%02d_%s'%(S['items'].index(x)+1,x['fn'])).convert('RGB')
    im.resize((640,800),Image.LANCZOS).save('p/'+e['f'],quality=80,optimize=True)
    im.thumbnail((TW,TH),Image.LANCZOS);c,r=e['i']%4,e['i']//4
    sh.paste(im,(c*TW+(TW-im.width)//2,r*TH+(TH-im.height)//2))
if new: sh.save(f's/{s0:03d}.jpg',quality=66,optimize=True)
# existentes
refmap={}
for d in D+new:
    if d['b']!='B4':continue
    for k,p in enumerate(d['f'][:-4].split('_')):
        m=re.match(r'(\d+)-([DHN])',p)
        if m: refmap.setdefault(m[1][1:] if k==0 else m[1],[]).append(d)
def sizes(eu):
    eu=re.sub(r'[^\d ,y/alEURTallas:-]','',eu or '')
    z=set()
    for a,b in re.findall(r'(\d\d)\s*al\s*(\d\d)',eu):
        z|=set(range(int(a),int(b)+1))
    rest=re.sub(r'(\d\d)\s*al\s*(\d\d)','',eu)
    z|={int(n) for n in re.findall(r'\b(\d\d)\b',rest) if 28<=int(n)<=46}
    return sorted(z)
def tstr(z):
    out=[];run=[]
    for n in z:
        if run and n==run[-1]+1:run.append(n)
        else:
            if run:out.append(run)
            run=[n]
    if run:out.append(run)
    return ' / '.join(('%dEUR'%r[0]) if len(r)==1 else ('%dEUR-%dEUR'%(r[0],r[1]) if len(r)==2 else '%dEUR al %dEUR'%(r[0],r[-1])) for r in out)
nz=0;seen=set()
for x in items:
    z=sizes(x['eu'])
    for r in x['refs']:
        for d in refmap.get(r,[]):
            seen.add(d['f'])
            d['d']='18/11';d.pop('a',None);d.pop('h',None)
            if x['caja']:d['x']=1
            elif 'x' in d and len(x['refs'])==1:d.pop('x')
            if z and d['g'] in 'DH' and '_' not in d['f']:
                zz=[n for n in z if (n<=39 if d['g']=='D' else n>=40)]
                if zz and zz!=d['z']:d['z']=zz;d['t']=tstr(zz);nz+=1
AG=dt.date(2026,11,14);HI=dt.date(2026,11,10);st={'a':0,'h':0,'pocas':0}
for d in D+new:
    if d['b']!='B4':continue
    if not d.get('d'):continue
    dd=dt.date(2026,int(d['d'][3:5]),int(d['d'][:2]))
    if dd<=AG:d['a']=1;st['a']+=1
    if dd<=HI:d['h']=1;st['h']+=1
    if d['d']=='18/11' and len(d['z'])<=3:d['a']=1;st['pocas']+=1
D+=new
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
open('index.html','w').write(h)
print('nuevas',len(new),'vistas',len(seen),'tallas cambiadas',nz,st)
