import re,json,math,sys
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
        refs=[re.sub(r'-[A-Z]+$','',parts[0])]+[pre+re.sub(r'-[A-Z]+$','',p) for p in parts[1:]]
        sz=set()
        for a,c in re.findall(r'(\d+)EUR al (\d+)EUR',tal): sz|=set(range(int(a),int(c)+1))
        for a in re.findall(r'(\d+)EUR',re.sub(r'\d+EUR al \d+EUR','',tal)): sz.add(int(a))
        out.append(dict(f=f,b=b,n=name,r=refs,t=tal,c=col,z=sorted(sz),g=''.join(sorted(set(re.findall(r'-([DHN])',base)))),m=brand(name)))
    return out
APPLY=len(sys.argv)>1
SRC={};new=[]
for x in parse(open(B+'b611out/descripciones.txt').read(),'B6'):
    x['t']=x['t'].replace(' - ',' / ') if len(x['r'])==2 else x['t']
    SRC[x['f']]=B+'b611out/'+x['f'];new.append(x)
new=[x for x in new if x['f'] not in have];print(len(new))
s0=max(d['s'] for d in D)+1
for k,x in enumerate(new): x['s']=s0+k//12;x['i']=k%12
TW,TH=420,525
for s in (range(math.ceil(len(new)/12)) if APPLY else []):
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
E=json.load(open(B+'b6_new11.json'));C=json.load(open(B+'b6_cl.json'))
oldit=json.load(open(B+'b6_items.json'));orow=json.load(open(B+'b6_rows_out.json'))
f_of={it['img']:orow[i][0] for i,it in enumerate(oldit)}
last={it['img']:it['last'] for it in oldit}
for c,m in zip(C['cl'],C['inold']):
    dt=max(E[i]['date'] for i in c)
    for n in m: last[n]=max(last[n],dt)
lastf={f_of[n]:l for n,l in last.items()}
for u in json.load(open(B+'b6_items11.json')):
    pass
nl={x['f']:l for x,l in zip(new,[r[2] for r in json.load(open(B+'b611_rows_out.json')) if r[0] in {y['f'] for y in new}])}
import collections;st=collections.Counter()
for d in D:
    if d['b']!='B6': continue
    L=lastf.get(d['f']) or nl.get(d['f'])
    if not L: st['sin']+=1;continue
    d['d']=L[8:10]+'/'+L[5:7];kk=(int(L[5:7]),int(L[8:10]))
    if kk<=(11,6): d['a']=1;st['ago']+=1
    else:
        if d.pop('a',None): st['des_ago']+=1
    if kk<=(11,2): d['h']=1;st['hid']+=1
    else:
        if d.pop('h',None): st['des_hid']+=1
print(dict(st),sum(1 for d in D if d['b']=='B6'))
if APPLY:
    h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
    open('index.html','w').write(h)
