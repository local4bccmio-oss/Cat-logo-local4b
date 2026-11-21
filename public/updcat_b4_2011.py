import re,json,datetime as dt
from PIL import Image
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1])
S=json.load(open('/tmp/g4S.json'));I=json.load(open('/tmp/g4items.json'))
byr={}
for d in D:
    if d['b']=='B4':
        for r in d['r']:byr.setdefault(r,[]).append(d)
newrefs={r for x in I for r in ['4'+q for q in x['refs']]}
seen=set();rep=0
for s in S:
    for r in s['refs']:
        r='4'+r
        if r in newrefs:continue
        for d in byr.get(r,[]):
            if d['f'] in seen:continue
            seen.add(d['f']);d['d']='20/11';d.pop('a',None);d.pop('h',None);d['x']=1;rep+=1
s0=max(d['s'] for d in D)+1;u=max(d.get('u',0) for d in D)+1
new=[];imgs=[]
def mar(n):
    for k in ('Nike','Adidas','Puma','Hoka','Timberland'):
        if n.startswith(k):return k
    return 'On Cloud' if n.startswith('On') else n.split()[0]
for x in I:
    refs=['4'+r for r in x['refs']]
    f=x['stem']
    if len(refs)==2:
        a,b=x['refs'];f='4%s-D_%s-H'%(a,b[1:]) if b.startswith('4') else x['stem']  # nombre corto como el resto del catálogo
        f='4%s-D_%s-H'%(a,b[1:])
    f+='.jpg'
    g='DH' if len(refs)==2 else x['gs'][0]
    new.append(dict(f=f,b='B4',n=x['name'],r=refs,t=x['tal'],c=x['col'],z=x['z'],g=g,m=mar(x['name']),x=1,d='20/11'));imgs.append('/tmp/g4out/'+x['fn'])
TW,TH=420,525
for k in range(0,len(new),12):
    sh=Image.new('RGB',(4*TW,3*TH),'white');s=s0+k//12
    for j,(e,p) in enumerate(zip(new[k:k+12],imgs[k:k+12])):
        e.update(s=s,i=j,u=u);im=Image.open(p).convert('RGB')
        im.resize((640,800),Image.LANCZOS).save('p/'+e['f'],quality=80,optimize=True)
        im.thumbnail((TW,TH),Image.LANCZOS);sh.paste(im,((j%4)*TW+(TW-im.width)//2,(j//4)*TH+(TH-im.height)//2))
    sh.save(f's/{s:03d}.jpg',quality=66,optimize=True)
D+=new
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
open('index.html','w',encoding='utf-8').write(h)
print('nuevas',len(new),'repost',rep)
