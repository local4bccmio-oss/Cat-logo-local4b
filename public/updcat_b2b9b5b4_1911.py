import re,json,datetime as dt
from PIL import Image
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1])
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
def zt(t):
    z=[]
    for seg in re.split(r'\s*/\s*|\s+-\s+',t):
        m=re.fullmatch(r'(\d\d)EUR(?: al (\d\d)EUR|-(\d\d)EUR)?',seg.strip())
        if not m:continue
        a=int(m[1])
        if m[2]:z+=range(a,int(m[2])+1)
        elif m[3]:z+=[a,int(m[3])]
        else:z.append(a)
    return sorted(set(z))
def mar(n):
    for k,v in (('Boss','Hugo Boss'),('New Balance','New Balance'),('Jordan','Jordan'),('Nike','Nike'),('Adidas','Adidas'),('Puma','Puma'),('Vans','Vans'),('Lacoste','Lacoste'),('Globe','Globe')):
        if n.startswith(k):return v
    return n.split()[0]
s0=[max(d['s'] for d in D)+1];u0=[max(d.get('u',0) for d in D)+1]
new=[]
def addnew(entries,imgs):
    """entries: list de dict sin s/i/u; imgs: rutas. sprites de 12"""
    u=u0[0];u0[0]+=1
    for k in range(0,len(entries),12):
        TW,TH=420,525;sh=Image.new('RGB',(4*TW,3*TH),'white');s=s0[0];s0[0]+=1
        for j,(e,p) in enumerate(zip(entries[k:k+12],imgs[k:k+12])):
            e.update(s=s,i=j,u=u);im=Image.open(p).convert('RGB')
            im.resize((640,800),Image.LANCZOS).save('p/'+e['f'],quality=80,optimize=True)
            im.thumbnail((TW,TH),Image.LANCZOS);sh.paste(im,((j%4)*TW+(TW-im.width)//2,(j//4)*TH+(TH-im.height)//2))
        sh.save(f's/{s:03d}.jpg',quality=66,optimize=True)
    new.extend(entries)
cnt=dict(b2=0,b9=0,b5rep=0,b5nz=0,b4rep=0,b4nz=0)
# B2 / B9
E1=[];I1=[]
for x in json.load(open('/tmp/b2b9.json')):
    pre='M2' if x['b']=='B2' else 'A9';f=f"{pre}{x['cod']}-{x['g']}.jpg"
    if f in byf:
        d=byf[f];d['d']='19/11';d.pop('a',None);d.pop('h',None);cnt['b2' if x['b']=='B2' else 'b9']+=1;continue
    g=x['g'];n={'New Balance 530':'New Balance 530'}.get(x['name'],x['name'])
    E1.append(dict(f=f,b=x['b'],n=n,r=[('2' if x['b']=='B2' else '9')+x['cod']],t='36EUR al 39EUR' if g=='D' else '40EUR al 44EUR',c=x['col'],z=list(range(36,40)) if g=='D' else list(range(40,45)),g=g,m=mar(n),d='19/11'));I1.append('/tmp/b2b9out/'+x['fn'])
addnew(E1,I1)
# B5 / B4 (85 imágenes)
E2=[];I2=[];seen=set()
for it in json.load(open('/tmp/b5b4items.json')):
    f=it['stem']+'.jpg';pair=len(it['refs'])==2
    if it['b']=='B4':
        pre='4'
    else:pre='5'
    if it['st']=='NUEVA':
        if f in byf or f in seen:continue
        seen.add(f)
        if it['b']=='B5':
            z=zt(it['tal'].replace(' / ',' - '));
            e=dict(f=f,b='B5',n=it['name'],r=['5'+r for r in it['refs']],t=it['tal'].replace(' / ',' - ') if pair else it['tal'],c=it['col'],z=z,g='DH' if pair else ('D' if max(z)<=39 else 'H'),m=mar(it['name']),d='19/11')
        else:
            t='36EUR al 39EUR / 40EUR al 42EUR' if pair else it['tal'];z=zt(t)
            e=dict(f=f,b='B4',n=it['name']+'*',r=['4'+r for r in it['refs']],t=t,c=it['col'],z=z,g='DH' if pair else 'H',m='Nike',d='19/11')
        if it['cj']:e['x']=1
        E2.append(e);I2.append('/tmp/b5b4out/'+it['fn']);continue
    # repost B5
    ents=[byf[f]] if f in byf else [d for d in D if d['b']=='B5' and any('5'+r in d['r'] for r in it['refs'])]
    exact=f in byf;z=zt(it['tal'].replace(' / ',' - '))
    for d in ents:
        cnt['b5rep']+=1;d['d']='19/11';d.pop('a',None);d.pop('h',None)
        if it['cj']:d['x']=1
        elif 'x' in d and len(it['refs'])==1:d.pop('x')
        if exact and z:
            zz=[n for n in z if n<=39] if d['g']=='D' else [n for n in z if n>=40] if d['g']=='H' else z
            if zz and zz!=d['z']:
                d['z']=zz;cnt['b5nz']+=1
                d['t']=tstr(zz) if d['g'] in 'DH' else ' - '.join(t for t in (tstr([n for n in zz if n<=39]),tstr([n for n in zz if n>=40])) if t)
addnew(E2,I2)
# B4 reposts (posts del 19/11)
rm={}
for d in D:
    if d['b']=='B4':
        for r in d['r']:rm.setdefault(r,[]).append(d)
for p in json.load(open('/tmp/b4posts.json')):
    refs=['4'+r.strip() for r in p['ref'].split('/')]
    m=re.search(r'Euro([^\n]*)',p['t']);z=[]
    if m:
        ln=re.sub(r'[^\d ,y/al]','',m[1])
        for a,b in re.findall(r'(\d\d)\s*al\s*(\d\d)',ln):z+=range(int(a),int(b)+1)
        z+=[int(n) for n in re.findall(r'\b(\d\d)\b',re.sub(r'(\d\d)\s*al\s*(\d\d)','',ln)) if 28<=int(n)<=46]
        z=sorted(set(z))
    cj='📦' in p['t']
    for r in refs:
        for d in rm.get(r,[]):
            if d['f'] in {e['f'] for e in new}:continue
            cnt['b4rep']+=1;d['d']='19/11';d.pop('a',None);d.pop('h',None)
            if cj:d['x']=1
            elif 'x' in d and len(refs)==1:d.pop('x')
            if z and d['g'] in 'DH' and '_' not in d['f']:
                zz=[n for n in z if (n<=39 if d['g']=='D' else n>=40)]
                if zz and zz!=d['z']:d['z']=zz;d['t']=tstr(zz);cnt['b4nz']+=1
AG=dt.date(2026,11,14);HI=dt.date(2026,11,10);st=dict(a=0,h=0,pocas=0)
for d in D+new:
    if d['b'] not in('B2','B9','B5','B4') or not d.get('d'):continue
    q=dt.date(2026,int(d['d'][3:5]),int(d['d'][:2]))
    if q<=AG:d['a']=1;st['a']+=1
    if q<=HI:d['h']=1;st['h']+=1
    if d['d'] in('18/11','19/11') and len(d['z'])<=3:d['a']=1;st['pocas']+=1
D+=new
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
open('index.html','w',encoding='utf-8').write(h)
print('nuevas',len(new),[e['f'] for e in new]);print(cnt,st)
