import re,json,datetime as dt,math
from PIL import Image
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1])
I=json.load(open('/tmp/nnitems.json'))
MA={'Numeris':'Otras','Hugo Boss':'Hugo Boss','Monastery':'Monastery','Gucci':'Gucci','Prada':'Prada'}
s0=max(d['s'] for d in D)+1;u=max(d.get('u',0) for d in D)+1;TW,TH=420,525
shs=[Image.new('RGB',(4*TW,3*TH),'white') for _ in range(math.ceil(len(I)/12))];new=[]
for k,x in enumerate(I):
    t={'D':'36EUR al 39EUR','H':'40EUR al 44EUR','DH':'36EUR al 44EUR'}[x['g']]
    e=dict(f=x['fn'],b='NN',n=x['name'],r=['Fr01-'+x['g']],t=t,c=x['col'],z=x['z'],g=x['g'],m=MA[x['name']],d='18/11',s=s0+k//12,i=k%12,u=u)
    new.append(e)
    im=Image.open('/tmp/nnout/'+x['fn']).convert('RGB');w,hh=im.size
    cv=Image.new('RGB',(640,800),'white');r=min(640/w,800/hh);im2=im.resize((int(w*r),int(hh*r)),Image.LANCZOS);cv.paste(im2,((640-im2.width)//2,(800-im2.height)//2));cv.save('p/'+x['fn'],quality=80,optimize=True)
    th=im.copy();th.thumbnail((TW,TH),Image.LANCZOS);c,rr=e['i']%4,e['i']//4;shs[k//12].paste(th,(c*TW+(TW-th.width)//2,rr*TH+(TH-th.height)//2))
for j,s in enumerate(shs):s.save(f's/{s0+j:03d}.jpg',quality=66,optimize=True)
have={d['f'] for d in D};assert not any(e['f'] in have for e in new)
AG=dt.date(2026,11,14);HI=dt.date(2026,11,10);st=dict(a=0,h=0)
for d in D+new:
    if d['b']!='NN' or not d.get('d'):continue
    q=dt.date(2026,int(d['d'][3:5]),int(d['d'][:2]))
    if q<=AG:d['a']=1;st['a']+=1
    if q<=HI:d['h']=1;st['h']+=1
D+=new
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
open('index.html','w',encoding='utf-8').write(h)
print('nuevas',len(new),st)
