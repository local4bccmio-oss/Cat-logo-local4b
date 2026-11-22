import re,json
from PIL import Image,ImageDraw,ImageFont
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1])
it=json.load(open('/tmp/b1b.json'));N=json.load(open('/tmp/b1new22.json'))
NM={'4939':('New Balance 9060','blanco crema'),'4934':('New Balance 9060','blanco crema'),'4948':('New Balance 530','gris azul'),'4932':('New Balance 9060','blanco'),'4949':('Nike Shox R4','rosado gris'),'1090':('Nike M2K Tekno','blanco'),'863':('Nike Air Max 97','negro'),'29':('Nike Dunk Low','crema blanco'),'4933':('New Balance 9060','café beige'),'4561':('New Balance 9060','negro'),'4936':('New Balance 9060','crema gris'),'4938':('New Balance 9060','gris beige'),'3938':('New Balance 9060','gris'),'4944':('Adidas Superstar','blanco rojo'),'4931':('New Balance 9060','crema rosado lila'),'4937':('New Balance 9060','beige azul'),'4706':('New Balance 9060','gris beige'),'4935':('New Balance 9060','blanco negro'),'4941':('New Balance 9060','azul gris'),'4942':('New Balance 9060','crema amarillo'),'4943':('Nike Air Max 97','blanco')}
S={}
for d in D:
    if d['b']=='B1':
        for r in d['r']:S.setdefault(r.rstrip('_'),[]).append(d)
newrefs={x['ref'] for x in N}
# repostes: fecha más reciente (20/11..22/11)
last={}
for i in it:
    if i['d'] not in('20/11','21/11','22/11'):continue
    m=re.search(r'REF (\d+) ([DH])',i['cap'])
    if m:last[m[1]]=i['d']
rep=0;seen=set()
for ref,dd in last.items():
    if ref in newrefs:continue
    for d in (S.get(ref) or S.get('1'+ref) or []):
        if d['f'] in seen:continue
        seen.add(d['f']);d['d']=dd;d.pop('a',None);d.pop('h',None);d['x']=1;rep+=1
s0=max(d['s'] for d in D)+1;u=int(max(d.get('u',0) for d in D))+1
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',32)
new=[];ims=[];caps=[]
for k,x in enumerate(N):
    ref=x['ref'];g=x['g'];code='1'+ref;n,c=NM[ref]
    t='36EUR al 39EUR' if g=='D' else '40EUR al 44EUR';z=[36,37,38,39] if g=='D' else [40,41,42,43,44]
    L=x['lista'];par=L+(20 if L<=65 else 15);caja=x['cb']+5;doc=L+5
    f='%s-%s.jpg'%(code,g)
    im=Image.open('/tmp/z22_b1b/'+x['f']).convert('RGB');W,H=im.size
    dr=ImageDraw.Draw(im);dr.rounded_rectangle((int(.004*W),int(.003*H),int(.46*W),int(.083*H)),8,fill='white')
    dr.text((int(.016*W),int(.02*H)),'%s-%s/%s'%(code,g,t),fill='black',font=font)
    e=dict(f=f,b='B1',n=n,r=[code],t=t,c=c,z=z,g=g,m='New Balance' if n.startswith('New') else n.split()[0],j='',x=1,d=x['d'],s=s0+k//12,i=k%12,u=u)
    new.append(e);ims.append(im)
    caps.append(dict(f=f,cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~\n📦 _$%d.000 por caja_'%(n,code,par,t,c,caja),cj='*$%d.000 por caja de %s*\n$%d.000 por docena\nDisponible también por pares'%(caja,'dama' if g=='D' else 'hombre',doc)))
TW,TH=420,525
for k in range(0,len(new),12):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for j,(e,im) in enumerate(zip(new[k:k+12],ims[k:k+12])):
        im.resize((640,800),Image.LANCZOS).save('p/'+e['f'],quality=80,optimize=True)
        t=im.copy();t.thumbnail((TW,TH),Image.LANCZOS);sh.paste(t,((j%4)*TW+(TW-t.width)//2,(j//4)*TH+(TH-t.height)//2))
    sh.save('s/%03d.jpg'%(s0+k//12),quality=66,optimize=True)
D+=new
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
open('index.html','w',encoding='utf-8').write(h)
json.dump(caps,open('/tmp/b1caps22.json','w'),ensure_ascii=False)
print('nuevas',len(new),'repost',rep,'sprites',s0)
for c in caps[:2]:print(c['cap'],'\n',c['cj'])
