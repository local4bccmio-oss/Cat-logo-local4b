import re,json,os,math
from PIL import Image
h=open('index.html').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1])
it=json.load(open('/tmp/b9items.json'))
fn={x['c']:'%02d_A9%s-%s.jpg'%(n+1,x['c'],x['g']) for n,x in enumerate(it)}
new={'1121':('Lacoste','negro'),'376':('Lacoste','negro blanco'),'685':('Le Coq Sportif','blanco crema'),'681':('Vans','blanco negro'),'1115':('Adidas Samba','blanco leopardo'),'1114':('Adidas Samba','morado'),'1027':('Puma','gris blanco'),'1050':('Puma Suede','crema'),'1051':('Puma Suede','negro rojo azul')}
G={x['c']:x['g'] for x in it}
added=[]
s0=max(d['s'] for d in D)+1;u=max(d.get('u',0) for d in D)+1
for k,(c,(n,col)) in enumerate(new.items()):
    g=G[c];f=f'A9{c}-{g}.jpg'
    if any(d['f']==f for d in D):continue
    added.append(dict(f=f,b='B9',n=n,r=['9'+c],t='36EUR al 39EUR' if g=='D' else '40EUR al 44EUR',c=col,z=list(range(36,40)) if g=='D' else list(range(40,45)),g=g,m=n.split()[0],s=s0,i=len(added),u=u,d='18/11'))
TW,TH=420,525
sh=Image.new('RGB',(4*TW,3*TH),'white')
for x in added:
    c=x['r'][0][1:];im=Image.open('/tmp/b9out/'+fn[c]).convert('RGB')
    im.resize((640,800),Image.LANCZOS).save('p/'+x['f'],quality=80,optimize=True)
    im.thumbnail((TW,TH),Image.LANCZOS);cc,r=x['i']%4,x['i']//4
    sh.paste(im,(cc*TW+(TW-im.width)//2,r*TH+(TH-im.height)//2))
sh.save(f's/{s0:03d}.jpg',quality=66,optimize=True)
seen={x['c']+x['g'] for x in it}
for d in D:
    if d['b']!='B9':continue
    m=re.match(r'A9(\d+)-([DHN])',d['f'])
    if m and m[1]+m[2] in seen:
        d['d']='18/11';d.pop('a',None);d.pop('h',None)
        if m[1]=='1031': d['n']='Puma Suede';d['m']='Puma';d['c']='negro blanco';d['t']='40EUR al 44EUR';d['z']=[40,41,42,43,44]
D+=added
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
open('index.html','w').write(h)
print(len(added),[x['f'] for x in added])
