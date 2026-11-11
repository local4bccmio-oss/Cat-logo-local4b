import re,json,math,sys,collections
from PIL import Image
B='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
h=open('index.html').read()
mm=re.search(r'const D=(\[.*?\]);\n',h,re.S)
D=json.loads(mm[1]);have={d['f'] for d in D}
def brand(n):
    l=n.lower()
    for k,v in [('tiger','Onitsuka Tiger'),('onitsuka','Onitsuka Tiger'),('jordan','Jordan'),('retro','Jordan'),('new balance','New Balance'),('nb ','New Balance'),('louis','Louis Vuitton'),('under','Under Armour'),('skechers','Skechers'),('tommy','Tommy'),('timberland','Timberland'),('on cloud','On Cloud'),('puma','Puma'),('vans','Vans'),('boss','Hugo Boss'),('coach','Coach'),('reebok','Reebok'),('le coq','Le Coq Sportif'),('dc ','DC'),('golden','Golden Goose'),('saucony','Saucony'),('globe','Globe'),('lacoste','Lacoste'),('asics','Asics'),('fila','Fila'),('dior','Dior'),('adidas','Adidas'),('samba','Adidas'),('super star','Adidas'),('superstar','Adidas'),('campus','Adidas'),('terrex','Adidas'),('nike','Nike'),('vomero','Nike'),('pegazus','Nike'),('air max','Nike'),('airmax','Nike'),('af1','Nike'),('sb ','Nike'),('tn ','Nike'),('blazer','Nike'),('cortez','Nike')]:
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
        refs=[re.sub(r'-[A-Z]+$','',parts[0])[1:]+'_']
        sz=set()
        for a,c in re.findall(r'(\d+)EUR al (\d+)EUR',tal): sz|=set(range(int(a),int(c)+1))
        for a in re.findall(r'(\d+)EUR',re.sub(r'\d+EUR al \d+EUR','',tal)): sz.add(int(a))
        out.append(dict(f=f,b=b,n=name,r=refs,t=tal,c=col,z=sorted(sz),g=''.join(sorted(set(re.findall(r'-([DHN])',base)))),m=brand(name),j=''))
    return out
SRC={};new=[]
for x in parse(open(B+'b1111out/descripciones_B1_11nov.txt').read(),'B1'):
    x['t']=x['t'].replace(' - ',' / ') if len(x['r'])==2 else x['t']
    SRC[x['f']]=B+'b1111out/'+x['f'];new.append(x)
new=[x for x in new if x['f'] not in have];print(len(new))
s0=max(d['s'] for d in D)+1
for k,x in enumerate(new): x['s']=s0+k//12;x['i']=k%12
TW,TH=420,525
for s in range(math.ceil(len(new)/12) if len(sys.argv)>1 else 0):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for x in new[s*12:s*12+12]:
        src=SRC[x['f']]
        im=Image.open(src).convert('RGB')
        im.resize((640,800),Image.LANCZOS).save('p/'+x['f'],quality=80,optimize=True)
        im.thumbnail((TW,TH),Image.LANCZOS);c,r=x['i']%4,x['i']//4
        sh.paste(im,(c*TW+(TW-im.width)//2,r*TH+(TH-im.height)//2))
    sh.save(f's/{s0+s:03d}.jpg',quality=66,optimize=True)
_u=max(d.get('u',0) for d in D)+1
for x in new: x['u']=_u
D+=new

APPLY=len(sys.argv)>1
rows=json.load(open(B+'b1111g_rows.json'))+json.load(open(B+'b1111f_rows.json'))+json.load(open(B+'b110c_rows.json'))+json.load(open(B+'b110b_rows.json'))+json.load(open(B+'b110_rows.json'))+json.load(open(B+'cn9_rows.json'))+json.load(open(B+'b1111_rows.json'))+json.load(open(B+'b1110_rows.json'))+json.load(open(B+'b119_rows.json'))+json.load(open(B+'b117_rows.json'))+json.load(open(B+'b111_rows.json'))+json.load(open(B+'b1i_rows2.json'))+json.load(open(B+'fz_rows.json'))
last={};byref={}
for r in sorted(rows,key=lambda r:r['ts']):
    if r['let']: last['1'+r['ref']+'-'+r['let']]=r
    else: byref['1'+r['ref']+'-']=r
desc=open(B+'b1111out/descripciones_B1_11nov.txt').read()
for x in new:
    blk=[bl for bl in desc.split('\n\n') if bl.startswith(x['f'])][0]
    if '📦' in blk: x['x']=1
st=collections.Counter()
newf={x['f'] for x in new}
for d in D:
    if d['b']!='B1' or d['f'] in newf: continue
    k=d['f'][:-4]
    r=last.get(k) or byref.get(k.rsplit('-',1)[0]+'-')
    if r is None:
        if not d.get('h'): st['sin_mencion_oculta']+=1
        d['h']=1;d['d']='';d.pop('a',None);continue
    dt=r['date'];dd=dt[8:10]+'/'+dt[5:7];kk=(int(dt[5:7]),int(dt[8:10]))
    d['d']=dd;st['fecha']+=1
    if kk>(11,7):
        if d.pop('a',None): st['des_ago']+=1
    if kk>(11,3):
        if d.pop('h',None): st['des_hid']+=1
    if kk<=(11,6) and kk>(11,3):
        if not d.get('a'): st['agotado']+=1
        d['a']=1
    if kk<=(11,3):
        d['h']=1;d.pop('a',None);st['oculta_7d']+=1
    v=bool(r['caja']) or bool(re.search(r'DOCENA[^$\n]*\$\s*\d+',r['body'],re.I))
    if v!=bool(d.get('x')):
        st['x']+=1
        if v:d['x']=1
        else:d.pop('x',None)
for x in new:
    rr=last.get(x['f'][:-4]);x['d']=rr['date'][8:10]+'/'+rr['date'][5:7] if rr else '11/11'
DEF={'D':list(range(36,40)),'H':list(range(40,45)),'N':list(range(28,36))}
def fmt(z):
    runs=[];
    for v in z:
        if runs and v==runs[-1][-1]+1: runs[-1].append(v)
        else: runs.append([v])
    return '-'.join(f'{r[0]}EUR' if len(r)==1 else f'{r[0]}EUR al {r[-1]}EUR' for r in runs)
DM={d['f'][:-4]:d for d in D if d['b']=='B1'}
for k,r in last.items():
    if r['ts']<=[2026,11,10,11,27] or k not in DM: continue
    let=k.rsplit('-',1)[1];nums=re.findall(r'\n\s*(\d\d)\s*[-.]\s*(\d+)',r['body'])
    z=sorted({int(a) for a,c in nums if int(c)>0}) if nums else DEF[let]
    if not z: continue
    d=DM[k]
    if d['z']!=z: d['z']=z;d['t']=fmt(z);st['tallas']+=1
for d in D:
    if d['b']=='B1' and d.get('z') and len(d['z'])<=3 and not d.get('h') and not d.get('a'): d['a']=1;st['pocas']+=1
print(len(new),dict(st))
if APPLY:
    h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
    open('index.html','w').write(h)
