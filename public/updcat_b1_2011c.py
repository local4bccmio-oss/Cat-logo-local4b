import re,json,datetime as dt
from PIL import Image
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1])
byf={d['f']:d for d in D}
I=json.load(open('/tmp/g3items.json'))
s0=max(d['s'] for d in D)+1;u=max(d.get('u',0) for d in D)+1
new=[];imgs=[];seen=0;nm=0
def mar(n):
    for k,v in (('Jordan','Jordan'),('Nike','Nike'),('Adidas','Adidas'),('New Balance','New Balance'),('On','On Cloud'),('McQueen','McQueen')):
        if n.startswith(k):return v
    return n.split()[0]
for x in I:
    day='19/11' if x['d']==19 else '20/11'
    for r,g in zip(x['refs'],x['gs']):
        f='1%s-%s.jpg'%(r,g)
        if f in byf:
            d=byf[f];d['d']=day;d.pop('a',None);d.pop('h',None);d['x']=1;seen+=1
            if d['c']=='' and x['col']:d['c']=x['col']
            if d['n'] in('Jordan','Nike','Adidas','New Balance') and len(x['name'])>len(d['n']) and x['name'].startswith(d['n']):d['n']=x['name'];nm+=1
            continue
        if any(e['f']==f for e in new):continue
        g_=g;z=list(range(36,40)) if g=='D' else list(range(40,45))
        tal=x['tal'] if len(x['refs'])==1 else ('36EUR al 39EUR' if g=='D' else '40EUR al 44EUR')
        new.append(dict(f=f,b='B1',n=x['name'],r=['1'+r],t=tal,c=x['col'],z=z,g=g,m=mar(x['name']),j='',x=1,d=day));imgs.append('/tmp/g3out/'+x['fn'])
TW,TH=420,525
for k in range(0,len(new),12):
    sh=Image.new('RGB',(4*TW,3*TH),'white');s=s0+k//12
    for j,(e,p) in enumerate(zip(new[k:k+12],imgs[k:k+12])):
        e.update(s=s,i=j,u=u);im=Image.open(p).convert('RGB')
        im.resize((640,800),Image.LANCZOS).save('p/'+e['f'],quality=80,optimize=True)
        im.thumbnail((TW,TH),Image.LANCZOS);sh.paste(im,((j%4)*TW+(TW-im.width)//2,(j//4)*TH+(TH-im.height)//2))
    sh.save(f's/{s:03d}.jpg',quality=66,optimize=True)
AG=dt.date(2026,11,14);HI=dt.date(2026,11,10)
for d in D+new:
    if d['b']!='B1' or not d.get('d'):continue
    q=dt.date(2026,int(d['d'][3:5]),int(d['d'][:2]))
    if q<=AG:d['a']=1
    if q<=HI:d['h']=1
D+=new
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
open('index.html','w',encoding='utf-8').write(h)
print('nuevas',[e['f'] for e in new],'repost',seen,'nombres',nm)
