import re,json,math,sys,collections,datetime as dt
from PIL import Image
B='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
APPLY=len(sys.argv)>1
h=open('index.html').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1])
new=[]
for o in json.load(open(B+'b210_items_new.json')):
    cod,let=o['cod'],o['let'];f=f'M2{cod}-{let}.jpg'
    if any(d['f']==f for d in D): continue
    new.append(dict(f=f,b='B2',n=o['name'],r=['2'+cod],t='36EUR al 39EUR' if let=='D' else '40EUR al 44EUR',c=o['col'],z=list(range(36,40)) if let=='D' else list(range(40,45)),g=let,m=o['name'].split()[0]))
s0=max(d['s'] for d in D)+1
for k,x in enumerate(new):x['s']=s0+k//12;x['i']=k%12
TW,TH=420,525
if APPLY:
  for s in range(math.ceil(len(new)/12)):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for x in new[s*12:s*12+12]:
        im=Image.open(B+'b210out/'+x['f']).convert('RGB');im.resize((640,800),Image.LANCZOS).save('p/'+x['f'],quality=80,optimize=True)
        im.thumbnail((TW,TH),Image.LANCZOS);c,r=x['i']%4,x['i']//4
        sh.paste(im,(c*TW+(TW-im.width)//2,r*TH+(TH-im.height)//2))
    sh.save(f's/{s0+s:03d}.jpg',quality=66,optimize=True)
_u=max(d.get('u',0) for d in D)+1
for x in new:x['u']=_u
D+=new
rows=json.load(open(B+'b210_rows.json'))
last={}
for r in sorted(rows,key=lambda r:r['ts']):last[r['cod']+r['let']]=r;last.setdefault(r['cod'],r) if r['let']=='?' else None
st=collections.Counter()
AG=dt.date(2026,11,10);HI=dt.date(2026,11,2)
for d in D:
    if d['b']!='B2':continue
    c=re.match(r'M2(\d+)-',d['f'])[1]+d['f'][-5]
    if c not in last: c=c[:-1]
    if c not in last or False:
        st['sin']+=1;d['h']=1;d['d']='';d['a']=1;continue
    r=last[c];L=dt.date.fromisoformat(r['date']);d['d']=L.strftime('%d/%m')
    if L<AG:d['a']=1;st['ago']+=1
    else:
        if d.pop('a',None):st['des_ago']+=1
    if L<=HI:d['h']=1;st['hid']+=1
    else:
        if d.pop('h',None):st['des_hid']+=1
    if L>=dt.date(2026,11,10) and d['f'][-5] in 'DH':
        let=d['f'][-5];z=list(range(36,40)) if let=='D' else list(range(40,45))
        if d['z']!=z:st['talla']+=1
        d['z']=z;d['t']='36EUR al 39EUR' if let=='D' else '40EUR al 44EUR'
print(len(new),dict(st),sum(1 for d in D if d['b']=='B2'))
if APPLY:
    h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
    open('index.html','w').write(h)
