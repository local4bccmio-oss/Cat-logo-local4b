import re,json,math,sys,collections
from PIL import Image
B='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
APPLY=len(sys.argv)>1
h=open('index.html').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);D=[d for d in D if d['f']!='46239-D_6238-H'];have={d['f'] for d in D}
def brand(n):
    l=n.lower()+' '
    for k,v in [('lecoq','Le Coq Sportif'),('le coq','Le Coq Sportif'),('armani','Armani Exchange'),('ea7','Armani Exchange'),('calvin','Calvin Klein'),('dc shoes','DC'),('dior','Dior'),('jordan','Jordan'),('new balance','New Balance'),('louis','Louis Vuitton'),('skechers','Skechers'),('boss','Hugo Boss'),('lacoste','Lacoste'),('asics','Asics'),('fila','Fila'),('adidas','Adidas'),('nike','Nike')]:
        if k in l: return v
    return 'Otras'
def parse(txt):
    out=[]
    for blk in txt.strip().split('\n\n'):
        L=blk.split('\n');f=L[0].strip()
        name=re.match(r'\*(.+?) Ref ',L[1])[1]
        tal=next(x.strip('*') for x in L if 'EUR' in x)
        col=next((x.strip('~') for x in L if x.startswith('~')),'')
        base=f[:-4];parts=base.split('_');pre=parts[0][0]
        refs=[parts[0][:-2]]+[pre+p[:-2] for p in parts[1:]]
        sz=set()
        for a,c in re.findall(r'(\d+)EUR al (\d+)EUR',tal): sz|=set(range(int(a),int(c)+1))
        for a in re.findall(r'(\d+)EUR',re.sub(r'\d+EUR al \d+EUR','',tal)): sz.add(int(a))
        out.append(dict(f=f,b='B4',n=name,r=refs,t=tal.replace(' - ',' / ') if len(refs)==2 else tal,c=col,z=sorted(sz),g=''.join(sorted(set(re.findall(r'-([DHN])',base)))),m=brand(name),_x='📦' in blk))
    return out
new=[x for x in parse(open(B+'b410out/descripciones_B4_10nov.txt').read()) if x['f'] not in have]
for x in new:
    if x.pop('_x'): x['x']=1
print('nuevos',len(new))
s0=max(d['s'] for d in D)+1
for k,x in enumerate(new): x['s']=s0+k//12;x['i']=k%12
TW,TH=420,525
if APPLY:
  for s in range(math.ceil(len(new)/12)):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for x in new[s*12:s*12+12]:
        im=Image.open(B+'b410out/'+x['f']).convert('RGB')
        im.resize((640,800),Image.LANCZOS).save('p/'+x['f'],quality=80,optimize=True)
        im.thumbnail((TW,TH),Image.LANCZOS);c,r=x['i']%4,x['i']//4
        sh.paste(im,(c*TW+(TW-im.width)//2,r*TH+(TH-im.height)//2))
    sh.save(f's/{s0+s:03d}.jpg',quality=66,optimize=True)
_u=max(d.get('u',0) for d in D)+1
for x in new:x['u']=_u
D+=new
rows=json.load(open(B+'b410_rows.json'))
key=lambda s:(int(s.split('/')[1]),int(s.split('/')[0]))
last={};lastrow={}
for r in rows:   # cronológico
    for x in r['refs']: last[x]=r['date'];lastrow[x]=r
if '5014' in last: last['5614']=last['5014'];lastrow['5614']=lastrow['5014']
# tallas helpers (de mkb44)
def p_(t):
    t=re.sub(r'\s+',' ',t.replace(' y ',','));out=[]
    for tk in [x.strip() for x in t.split(',') if x.strip()]:
        m=re.match(r'^(\d+) al (\d+)$',tk);out.append(('r',int(m[1]),int(m[2])) if m else ('n',int(tk),int(tk)))
    return out
def fmt(p): return '-'.join((f'{a}EUR al {b}EUR' if k=='r' else f'{a}EUR') for k,a,b in p)
def split(parts):
    dp,hp=[],[]
    for k,a,b in parts:
        if b<=39: dp.append((k,a,b))
        elif a>=40: hp.append((k,a,b))
        else: dp.append(('r' if a<39 else 'n',a,39)); hp.append(('r' if b>40 else 'n',40,b))
    return dp,hp
def nums(p):
    z=set()
    for k,a,b in p: z|=set(range(a,b+1))
    return sorted(z)
st=collections.Counter()
for d in D:
    if d['b']!='B4': continue
    ks=[r[1:] for r in d['r']]
    ds=[last[k] for k in ks if k in last]
    if not ds:
        st['sin']+=1;d['h']=1;d['d']='';d['a']=1;continue
    L=max(ds,key=key);kk=key(L);d['d']='%02d/%02d'%(int(L.split('/')[0]),int(L.split('/')[1]))
    if kk<=(11,6): d['a']=1;st['ago']+=1
    else:
        if d.pop('a',None): st['des_ago']+=1
    if kk<=(11,2): d['h']=1;st['hid']+=1
    else:
        if d.pop('h',None): st['des_hid']+=1
    # caja
    v=any(bool(lastrow[k]['caja']) for k in ks if k in lastrow)
    if v!=bool(d.get('x')):
        st['x']+=1
        if v:d['x']=1
        else:d.pop('x',None)
    # tallas (solo si el último mensaje es de 2/11 en adelante y trae todas las refs del modelo)
    r0=lastrow.get(ks[0])
    if r0 and key(r0['date'])>=(11,2) and r0['refs']==ks and r0['tal'] and d['f'] not in {x['f'] for x in new}:
        try:
            dp,hp=split(p_(r0['tal']))
            g=d['g']
            if g=='DH': z=nums(dp)+nums(hp);t=fmt(dp)+' / '+fmt(hp)
            elif g=='D': z=nums(dp);t=fmt(dp)
            else: z=nums(hp);t=fmt(hp)
            if z and z!=d['z']: d['z']=z;d['t']=t;st['tallas']+=1
        except Exception as e: st['err']+=1
for d in D:
    if d['b']=='B4' and len(d['z'])<=3 and not d.get('h') and not d.get('a'): d['a']=1;st['pocas']+=1
print(dict(st),sum(1 for d in D if d['b']=='B4'))
if APPLY:
    import os
    if os.path.exists('p/46239-D_6238-H.jpg'): os.remove('p/46239-D_6238-H.jpg')
    h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
    open('index.html','w').write(h)
