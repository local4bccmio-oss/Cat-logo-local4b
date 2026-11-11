import re,json,math,sys
from PIL import Image
B='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
h=open('index.html').read()
mm=re.search(r'const D=(\[.*?\]);\n',h,re.S)
D=json.loads(mm[1]);have={d['f'] for d in D}
def brand(n):
    l=n.lower()
    for k,v in [('tiger','Onitsuka Tiger'),('onitsuka','Onitsuka Tiger'),('jordan','Jordan'),('retro','Jordan'),('new balance','New Balance'),('nb ','New Balance'),('louis','Louis Vuitton'),('under','Under Armour'),('skechers','Skechers'),('tommy','Tommy'),('timberland','Timberland'),('on cloud','On Cloud'),('puma','Puma'),('vans','Vans'),('boss','Hugo Boss'),('coach','Coach'),('reebok','Reebok'),('le coq','Le Coq Sportif'),('dc ','DC'),('golden','Golden Goose'),('saucony','Saucony'),('globe','Globe'),('lacoste','Lacoste'),('asics','Asics'),('fila','Fila'),('dior','Dior'),('bape','Bape'),('calvin','Calvin Klein'),('amiri','Amiri'),('mcqueen','Alexander McQueen'),('guayos','Nike'),('adidas','Adidas'),('samba','Adidas'),('super star','Adidas'),('superstar','Adidas'),('campus','Adidas'),('terrex','Adidas'),('nike','Nike'),('vomero','Nike'),('pegazus','Nike'),('air max','Nike'),('airmax','Nike'),('af1','Nike'),('sb ','Nike'),('tn ','Nike'),('blazer','Nike'),('cortez','Nike')]:
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
        out.append(dict(f=f,b=b,n=name,r=refs,t=tal,c=col,z=sorted(sz),g=''.join(sorted(set(re.findall(r'-([DHN])',base)))),m=brand(name)))
    return out
SRC={};new=[]
for x in parse(open(B+'b011out/descripciones_B0_11nov.txt').read(),'B0'):
    x['t']=x['t'].replace(' - ',' / ') if len(x['r'])==2 else x['t']
    SRC[x['f']]=B+'b011out/'+x['f'];new.append(x)
new=[x for x in new if x['f'] not in have];print(len(new))
s0=max(d['s'] for d in D)+1
for k,x in enumerate(new): x['s']=s0+k//12;x['i']=k%12
TW,TH=420,525
APPLY=len(sys.argv)>1
for s in range(math.ceil(len(new)/12) if APPLY else 0):
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
import collections,datetime
def fmt(sz):
    sz=sorted(sz);runs=[];cur=[sz[0]]
    for x in sz[1:]:
        if x==cur[-1]+1:cur.append(x)
        else:runs.append(cur);cur=[x]
    runs.append(cur);out=[]
    for r in runs: out.append(f'{r[0]}EUR al {r[-1]}EUR' if len(r)>=3 else '-'.join(f'{x}EUR' for x in r))
    return '-'.join(out)
exec(open(B+'p0n_parse.py').read())
rows=json.load(open(B+'b0n11_rows.json'))
last={}
for r in sorted(rows,key=lambda r:r['ts']): last[r['ref']]=r
st=collections.Counter();newf={x['f'] for x in new}
for d in D:
    if d['b']!='B0':continue
    if d['f'] in newf: dd0=last.get(d['f'][:5]);d['d']=dd0['date'][8:10]+'/'+dd0['date'][5:7] if dd0 else '11/11';continue
    r=last.get(d['f'][:5])
    if r is None:
        if not d.get('h'):st['sin_mencion']+=1
        d['h']=1;d['d']='';d.pop('a',None);continue
    dt=r['date'];d['d']=dt[8:10]+'/'+dt[5:7];kk=(int(dt[5:7]),int(dt[8:10]));st['fecha']+=1
    try:
        pr,o=parse(r['body']);sz=sorted(set().union(*o.values())) if o else []
        if sz and sz!=d['z'] and kk>=(11,9):
            d['z']=sz;d['t']=fmt(sz);st['tallas']+=1
    except Exception as e: st['err_parse']+=1
    if kk>(11,7):
        if d.pop('a',None):st['des_ago']+=1
    if kk>(11,3):
        if d.pop('h',None):st['des_hid']+=1
    if (11,3)<kk<=(11,7):
        if not d.get('a'):st['agotado']+=1
        d['a']=1
    if kk<=(11,3): d['h']=1;d.pop('a',None);st['oculta_7d']+=1
for d in D:
    if d['b']=='B0' and d.get('z') and len(d['z'])<=3 and not d.get('h') and not d.get('a'): d['a']=1;st['pocas']+=1
print(len(new),dict(st))
if APPLY:
    h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
    open('index.html','w').write(h);print(len(D))
