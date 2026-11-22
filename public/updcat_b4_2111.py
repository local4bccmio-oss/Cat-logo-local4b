import re,json,math
from PIL import Image,ImageDraw,ImageFont
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1])
S=[i for i in json.load(open('/tmp/mym22.json')) if i['d']=='21/11' and i['refs']]
byr={}
for d in D:
    if d['b']=='B4':
        for r in d['r']:byr.setdefault(r,[]).append(d)
N=[('0314','46413-D.jpg','Nike Jordan Retro 1','36EUR','rosado blanco',[36],'D','Nike',0),
('0337','44746-D.jpg','Nike SB','36EUR','blanco azul gris',[36],'D','Nike',0),
('0343','45324-H.jpg','Reebok Classic','40EUR','gris',[40],'H','Reebok',0),
('0354','45210-D.jpg','Nike Air Force 1 Billie Eilish','36EUR-38EUR-39EUR','beige',[36,38,39],'D','Nike',0),
('0397','45182-H.jpg','Nike Shox Ride 2','44EUR','blanco negro rojo',[44],'H','Nike',1)]
newrefs={'46413','44746','45324','45210','45182'}
seen=set();rep=0
for s in S:
    for r in s['refs']:
        r='4'+r
        if r in newrefs:continue
        for d in byr.get(r,[]):
            if d['f'] in seen:continue
            seen.add(d['f']);d['d']='21/11';d.pop('a',None);d.pop('h',None);d['x']=1;rep+=1
s0=max(d['s'] for d in D)+1;u=int(max(d.get('u',0) for d in D))+1
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',32)
new=[];ims=[]
for k,(wa,f,n,t,c,z,g,m,x) in enumerate(N):
    src=[i for i in S if i['f'].endswith('WA'+wa+'.jpg')][0]['f']
    im=Image.open('/tmp/z22_mym/'+src).convert('RGB');W,H=im.size
    dr=ImageDraw.Draw(im);dr.rounded_rectangle((int(.004*W),int(.003*H),int(.46*W),int(.083*H)),8,fill='white')
    dr.text((int(.016*W),int(.02*H)),'%s-%s/%s'%(f[:5],g,t.replace('-','/') if len(z)>1 and t.count('-') else t),fill='black',font=font)
    e=dict(f=f,b='B4',n=n,r=[f[:5]],t=t,c=c,z=z,g=g,s=s0,i=k,m=m,u=u,d='21/11')
    if x:e['x']=1
    new.append(e);ims.append(im)
TW,TH=420,525
sh=Image.new('RGB',(4*TW,3*TH),'white')
for j,(e,im) in enumerate(zip(new,ims)):
    im.resize((640,800),Image.LANCZOS).save('p/'+e['f'],quality=80,optimize=True)
    t=im.copy();t.thumbnail((TW,TH),Image.LANCZOS);sh.paste(t,((j%4)*TW+(TW-t.width)//2,(j//4)*TH+(TH-t.height)//2))
sh.save('s/%03d.jpg'%s0,quality=66,optimize=True)
D+=new
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
open('index.html','w',encoding='utf-8').write(h)
print('nuevas',len(new),'repost',rep,'sprite',s0)
