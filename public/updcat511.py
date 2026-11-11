import re,json,math,sys,collections
from PIL import Image
B='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
h=open('index.html').read()
mm=re.search(r'const D=(\[.*?\]);\n',h,re.S)
D=json.loads(mm[1]);have={d['f'] for d in D}
def brand(n):
    l=n.lower()
    for k,v in [('tiger','Onitsuka Tiger'),('onitsuka','Onitsuka Tiger'),('jordan','Jordan'),('retro','Jordan'),('new balance','New Balance'),('nb ','New Balance'),('louis','Louis Vuitton'),('under','Under Armour'),('skechers','Skechers'),('tommy','Tommy'),('timberland','Timberland'),('on cloud','On Cloud'),('puma','Puma'),('vans','Vans'),('boss','Hugo Boss'),('coach','Coach'),('reebok','Reebok'),('le coq','Le Coq Sportif'),('dc ','DC'),('golden','Golden Goose'),('saucony','Saucony'),('globe','Globe'),('lacoste','Lacoste'),('asics','Asics'),('fila','Fila'),('dior','Dior'),('hoka','Hoka'),('zoom','Nike'),('nocta','Nike'),('ava ','Nike'),('duramo','Adidas'),('adidas','Adidas'),('adidas','Adidas'),('samba','Adidas'),('super star','Adidas'),('superstar','Adidas'),('campus','Adidas'),('terrex','Adidas'),('nike','Nike'),('vomero','Nike'),('pegazus','Nike'),('air max','Nike'),('airmax','Nike'),('af1','Nike'),('sb ','Nike'),('tn ','Nike'),('blazer','Nike'),('cortez','Nike')]:
        if k in l+' ': return v
    return 'Otras'
def parse(txt,b):
    out=[]
    for blk in txt.strip().split('\n\n'):
        L=blk.split('\n');f=L[0].strip()
        m=re.match(r'\*(.+?)\*',L[1]);name=m[1]
        tal=next(x.strip('*') for x in L if 'EUR' in x)
        col=next((x.strip('~') for x in L if x.startswith('~')),'').replace(' con ',' ')
        base=f[:-4];parts=base.split('_');pre=parts[0][0]
        refs=[re.sub(r'-[A-Z]+$','',parts[0])]+[pre+re.sub(r'-[A-Z]+$','',p) for p in parts[1:]]
        sz=set()
        for a,c in re.findall(r'(\d+)EUR al (\d+)EUR',tal): sz|=set(range(int(a),int(c)+1))
        for a in re.findall(r'(\d+)EUR',re.sub(r'\d+EUR al \d+EUR','',tal)): sz.add(int(a))
        out.append(dict(f=f,b=b,n=name,r=refs,t=tal,c=col,z=sorted(sz),g=''.join(sorted(set(''.join(re.findall(r'-([DHN]+)',base))))),m=brand(name)))
    return out
APPLY=len(sys.argv)>1
SRC={};new=[]
for x in parse(open(B+'b511out/descripciones.txt').read(),'B5'):
    x['t']=x['t'].replace(' - ',' / ') if len(x['r'])==2 else x['t']
    SRC[x['f']]=B+'b511out/'+x['f'];new.append(x)
new=[x for x in new if x['f'] not in have];print('nuevos',len(new))
s0=max(d['s'] for d in D)+1
for k,x in enumerate(new): x['s']=s0+k//12;x['i']=k%12
TW,TH=420,525
if APPLY:
  for s in range(math.ceil(len(new)/12)):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for x in new[s*12:s*12+12]:
        im=Image.open(SRC[x['f']]).convert('RGB')
        im.resize((640,800),Image.LANCZOS).save('p/'+x['f'],quality=80,optimize=True)
        im.thumbnail((TW,TH),Image.LANCZOS);c,r=x['i']%4,x['i']//4
        sh.paste(im,(c*TW+(TW-im.width)//2,r*TH+(TH-im.height)//2))
    sh.save(f's/{s0+s:03d}.jpg',quality=66,optimize=True)
_u=max(d.get('u',0) for d in D)+1
desc=open(B+'b511out/descripciones.txt').read()
for x in new:
    x['u']=_u
    blk=[bl for bl in desc.split('\n\n') if bl.startswith(x['f'])][0]
    if '📦' in blk: x['x']=1
D+=new
rows=json.load(open(B+'b511_rows.json'))
last={};lastrow={}
for r in sorted(rows,key=lambda r:r['ts']):
    for x in r['refs']: last[x]=r['date'];lastrow[x]=r
def p_(t):
    t=t.replace('M','');out=[]
    for tk in [x.strip() for x in t.split('-')]:
        m=re.match(r'^(\d+) al (\d+)$',tk);out.append(('r',int(m[1]),int(m[2])) if m else ('n',int(tk),int(tk)))
    return out
def fmt(p): return '-'.join((f'{a}EUR al {b}EUR' if k=='r' else f'{a}EUR') for k,a,b in p)
def nums(p):
    z=set()
    for k,a,b in p: z|=set(range(a,b+1))
    return sorted(z)
newf={x['f'] for x in new}
st=collections.Counter()
for d in D:
    if d['b']!='B5': continue
    ks=[int(r[1:]) for r in d['r']]
    ds=[last[k] for k in ks if k in last]
    if d['f'] in newf:
        ds=[last[k] for k in [int(r[1:]) for r in d['r']] if k in last];L=max(ds);d['d']=L[8:10]+'/'+L[5:7];
        if len(d['z'])<=3:d['a']=1
        continue
    if not ds:
        st['sin']+=1;d['h']=1;d['d']='';d['a']=1;continue
    L=max(ds);dd=L[8:10]+'/'+L[5:7];kk=(int(L[5:7]),int(L[8:10]))
    d['d']=dd
    if kk<=(11,6): d['a']=1;st['ago']+=1
    else:
        if d.pop('a',None): st['des_ago']+=1
    if kk<=(11,2): d['h']=1;st['hid']+=1
    else:
        if d.pop('h',None): st['des_hid']+=1
    v=any(bool(lastrow[k]['caja']) for k in ks if k in lastrow)
    if v!=bool(d.get('x')):
        st['x']+=1
        if v:d['x']=1
        else:d.pop('x',None)
    r0=lastrow.get(ks[0])
    if r0 and kk>=(11,7) and r0['tal'] and len(ks)==1 and 'M' not in (r0['tal'] or '').replace('Euro','').replace('EURO','')[:0]:
        try:
            t=re.sub(r'(?i)euro\s*','',r0['tal']).strip();p=p_(t)
            z=nums(p)
            if d['g']=='D': z=[a for a in z if a<=39]
            elif d['g']=='H': z=[a for a in z if a>=40]
            pp=[('n',a,a) for a in z]  # reconstruir rangos
            runs=[];i=0
            while i<len(z):
                j=i
                while j+1<len(z) and z[j+1]==z[j]+1:j+=1
                runs.append(('r',z[i],z[j]) if j-i>=2 else None) if False else None
                i=j+1
            if z and z!=d['z']:
                d['z']=z;d['t']=fmt([x for x in p if (d['g']=='DH' or (d['g']=='D' and x[1]<=39) or (d['g']=='H' and x[2]>=40))]) or d['t'];st['tallas']+=1
        except Exception: st['err']+=1
for d in D:
    if d['b']=='B5' and d.get('z') and len(d['z'])<=3 and not d.get('h') and not d.get('a'): d['a']=1;st['pocas']+=1
print(dict(st),sum(1 for d in D if d['b']=='B5'))
if APPLY:
    h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
    open('index.html','w').write(h)
