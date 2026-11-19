import re,json,datetime as dt,math
from PIL import Image
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1])
I=json.load(open('/tmp/b0items.json'));S=json.load(open('/tmp/b0n_sel.json'))
dmap={}
for o in S:
    if 'archivo adjunto' in o['x']:
        t=' '.join(o['ex']);m=re.search(r'(\d{5})\*?\s*$',t.strip())
        if m:dmap.setdefault(m[1],o['d'][2:]+'/'+o['d'][:2])
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
s0=max(d['s'] for d in D)+1;u=max(d.get('u',0) for d in D)+1;TW,TH=420,525
N=[it for it in I if it['st']=='NUEVA']
shs=[Image.new('RGB',(4*TW,3*TH),'white') for _ in range(math.ceil(len(N)/12))];new=[]
for k,it in enumerate(N):
    f=it['stem']+'.jpg';assert f not in byf
    e=dict(f=f,b='B0',n=it['name'],r=[it['cod']],t=it['tal'],c=it['col'],z=it['z'],g=it['g'],m=it['marca'],s=s0+k//12,i=k%12,u=u,d=dmap[it['cod']])
    new.append(e)
    im=Image.open('/tmp/b0out/'+it['fn']).convert('RGB');w,hh=im.size
    cv=Image.new('RGB',(640,800),'white');r=min(640/w,800/hh);im2=im.resize((int(w*r),int(hh*r)),Image.LANCZOS);cv.paste(im2,((640-im2.width)//2,(800-im2.height)//2));cv.save('p/'+f,quality=80,optimize=True)
    th=im.copy();th.thumbnail((TW,TH),Image.LANCZOS);c,rr=e['i']%4,e['i']//4;shs[k//12].paste(th,(c*TW+(TW-th.width)//2,rr*TH+(TH-th.height)//2))
for j,s in enumerate(shs):s.save(f's/{s0+j:03d}.jpg',quality=66,optimize=True)
seen=nz=0
for it in I:
    if it['st']!='REPOST':continue
    for f in it['ents']:
        d=byf.get(f)
        if not d:continue
        seen+=1;d['d']=dmap[it['cod']];d.pop('a',None);d.pop('h',None)
        z=it['z']
        if z!=d['z']:d['z']=z;d['t']=tstr(z);nz+=1
AG=dt.date(2026,11,14);HI=dt.date(2026,11,10);st=dict(a=0,h=0,pocas=0)
for d in D+new:
    if d['b']!='B0' or not d.get('d'):continue
    q=dt.date(2026,int(d['d'][3:5]),int(d['d'][:2]))
    if q<=AG:d['a']=1;st['a']+=1
    if q<=HI:d['h']=1;st['h']+=1
    if d['d'] in('18/11','19/11') and len(d['z'])<=3:d['a']=1;st['pocas']+=1
D+=new
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
open('index.html','w',encoding='utf-8').write(h)
print('nuevas',len(new),'vistas',seen,'tallas',nz,st,s0)
