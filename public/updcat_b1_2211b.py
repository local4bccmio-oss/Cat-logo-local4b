import re,json
from PIL import Image,ImageDraw,ImageFont
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1])
Z='/tmp/z_g1/'
N=[
('4945','H','IMG-20261122-WA0211.jpg',65,60,'Jordan Retro 4','blanco negro'),('4951','H','IMG-20261122-WA0346.jpg',60,55,'New Balance 9060','negro gris rojo'),('4952','H','IMG-20261122-WA0352.jpg',75,70,'Jordan Retro 11','blanco'),
('4929','D','IMG-20261122-WA0375.jpg',55,50,'New Balance 9060','rosado vino')]
REP=['14218-D.jpg','14302-D.jpg','14720-D.jpg','11062-H.jpg','14769-D.jpg','14770-H.jpg','11305-D.jpg','14844-H.jpg']
rep=0
for d in D:
    if d['f'] in REP:
        d['d']='22/11';d.pop('a',None);d.pop('h',None);d['x']=1;rep+=1
s0=max(d['s'] for d in D)+1;u=int(max(d.get('u',0) for d in D))+1
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',32)
new=[];ims=[];caps=[]
for k,(ref,g,fi,L,cb,n,c) in enumerate(N):
    code='1'+ref;t='36EUR al 39EUR' if g=='D' else '40EUR al 44EUR';z=[36,37,38,39] if g=='D' else [40,41,42,43,44]
    par=L+(20 if L<=65 else 15);caja=cb+5;doc=L+5;f='%s-%s.jpg'%(code,g)
    assert not any(d['f']==f for d in D)
    im=Image.open(Z+fi).convert('RGB');W,H=im.size
    dr=ImageDraw.Draw(im);dr.rounded_rectangle((int(.004*W),int(.003*H),int(.46*W),int(.083*H)),8,fill='white')
    dr.text((int(.016*W),int(.02*H)),'%s-%s/%s'%(code,g,t),fill='black',font=font)
    new.append(dict(f=f,b='B1',n=n,r=[code],t=t,c=c,z=z,g=g,m='New Balance' if n.startswith('New') else n.split()[0],j='',x=1,d='22/11',s=s0,i=k,u=u));ims.append(im)
    caps.append(dict(f=f,cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~\n📦 _$%d.000 por caja_'%(n,code,par,t,c,caja),cj='*$%d.000 por caja de %s*\n$%d.000 por docena\nDisponible también por pares'%(caja,'dama' if g=='D' else 'hombre',doc)))
TW,TH=420,525;sh=Image.new('RGB',(4*TW,3*TH),'white')
for j,(e,im) in enumerate(zip(new,ims)):
    im.resize((640,800),Image.LANCZOS).save('p/'+e['f'],quality=80,optimize=True)
    t=im.copy();t.thumbnail((TW,TH),Image.LANCZOS);sh.paste(t,((j%4)*TW+(TW-t.width)//2,(j//4)*TH+(TH-t.height)//2))
sh.save('s/%03d.jpg'%s0,quality=66,optimize=True)
D+=new
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
open('index.html','w',encoding='utf-8').write(h)
json.dump(caps,open('/tmp/b1caps22b.json','w'),ensure_ascii=False)
print('nuevas',len(new),'repost',rep,'sprite',s0,'u',u)
for c in caps:print(c['f'],c['cap'].replace('\n',' / '))
