import re,json,os,datetime as dt
from PIL import Image,ImageDraw,ImageFont
os.chdir('/home/claude/cat-logo-local4b/public')
Z='/tmp/w/b6/'
SC='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
os.makedirs(SC+'b6s',exist_ok=True)
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
smax=max(d['s'] for d in D);S=[smax,sum(1 for d in D if d['s']==smax)]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
# (imagen, [(cod,letra)], marca/nombre, color, lista, marca-filtro)
Hh,Dd='H','D'
N=[
('IMG-20261119-WA1456.jpg',[('3537','H')],'Bota Under Armour','negro',90,'Under Armour','20261123'),
('IMG-20261119-WA1457.jpg',[('3535','H')],'Bota Under Armour','negro',90,'Under Armour',''),
('IMG-20261119-WA1458.jpg',[('3536','H')],'Bota Under Armour','negro',90,'Under Armour',''),
('IMG-20261119-WA1462.jpg',[('3346','H')],'Bota Timberland','celeste claro y crema',90,'Otras',''),
('IMG-20261119-WA1463.jpg',[('3344','H')],'Bota Timberland','negro',90,'Otras',''),
('IMG-20261119-WA1464.jpg',[('3293','H')],'Reebok','gris, azul y crema',95,'Reebok',''),
('IMG-20261119-WA1465.jpg',[('3605','D')],'On Cloud','blanco y rosado',95,'Otras',''),
('IMG-20261119-WA1511.jpg',[('3722','D')],'Adidas Response','blanco, azul oscuro y morado',90,'Adidas',''),
('IMG-20261122-WA0810.jpg',[('3733','H')],'Tommy Jeans','negro y blanco',100,'Tommy Hilfiger',''),
('IMG-20261122-WA0811.jpg',[('3732','H')],'Tommy Jeans','azul oscuro y blanco',100,'Tommy Hilfiger',''),
('IMG-20261122-WA0813.jpg',[('3653','H')],'Reebok Anuel','blanco y negro',100,'Reebok',''),
('IMG-20261122-WA0818.jpg',[('3746','D'),('3747','H')],'New Balance 574','crema, azul oscuro y beige',90,'New Balance',''),
('IMG-20261122-WA0817.jpg',[('3748','H')],'New Balance 574','gris y verde',90,'New Balance',''),
('IMG-20261122-WA0819.jpg',[('3744','D')],'New Balance 574','crema y naranja',90,'New Balance',''),
('IMG-20261122-WA0821.jpg',[('3745','D')],'New Balance 574','crema y rosado',90,'New Balance',''),
('IMG-20261122-WA0824.jpg',[('3670','H')],'Jordan Retro 13 Low','blanco, negro y rojo',100,'Jordan',''),
('IMG-20261122-WA0826.jpg',[('3669','H')],'Jordan Retro 13 Low','beige y crema',100,'Jordan',''),
('IMG-20261122-WA0825.jpg',[('3671','H')],'Jordan Retro 13 Low','negro y rojo',100,'Jordan',''),
('IMG-20261122-WA0828.jpg',[('3668','H')],'Jordan Retro 13 Low','blanco y negro',100,'Jordan',''),
('IMG-20261122-WA0830.jpg',[('3512','D')],'Nike For One','rosado',95,'Nike',''),
('IMG-20261122-WA0833.jpg',[('3514','D')],'Nike For One','negro',95,'Nike',''),
('IMG-20261122-WA0835.jpg',[('3513','D')],'Nike For One','blanco',95,'Nike',''),
('IMG-20261122-WA0839.jpg',[('3462','H')],'Nike For One Charol','negro',75,'Nike',''),
('IMG-20261122-WA0838.jpg',[('3461','H')],'Nike For One Charol','rojo',75,'Nike',''),
('IMG-20261122-WA0842.jpg',[('3460','H')],'Nike For One Charol','azul rey',75,'Nike',''),
('IMG-20261123-WA1166.jpg',[('3701','H')],'New Balance V1','negro y plateado',90,'New Balance',''),
('IMG-20261123-WA1167.jpg',[('3700','D')],'New Balance V1','blanco y morado',90,'New Balance',''),
('IMG-20261123-WA1168.jpg',[('3699','H')],'New Balance V1','gris y verde azulado',90,'New Balance',''),
('IMG-20261123-WA1169.jpg',[('3698','D')],'New Balance V1','negro y rosado',90,'New Balance',''),
('IMG-20261123-WA1170.jpg',[('3528','D')],'Nike Shox','crema y morado',85,'Nike',''),
('IMG-20261123-WA1171.jpg',[('3529','D')],'Nike Shox','negro, plateado y rosado',85,'Nike',''),
('IMG-20261123-WA1172.jpg',[('3527','D')],'Nike Shox','plateado y rosado',85,'Nike',''),
('IMG-20261123-WA1173.jpg',[('3753','D'),('3752','H')],'New Balance 2000','fucsia',110,'New Balance',''),
('IMG-20261123-WA1174.jpg',[('3750','D'),('3749','H')],'New Balance 2000','azul',110,'New Balance',''),
('IMG-20261123-WA1175.jpg',[('3751','H')],'New Balance 2000','gris y negro',110,'New Balance',''),
('IMG-20261123-WA1176.jpg',[('3318','H'),('3319','D')],'Nike Retro 1','negro charol',70,'Nike',''),
('IMG-20261123-WA1184.jpg',[('3526','D')],'Nike V2K','marrón oscuro y negro',95,'Nike',''),
# repostes de refs que no estaban en el catalogo (publicadas 22-25/11)
('IMG-20261004-WA0228.jpg',[('3555','D'),('3554','H')],'Adidas Super Star','blanco y negro',75,'Adidas',''),
('IMG-20261013-WA1066.jpg',[('3556','D')],'Adidas Super Star','blanco y crema',75,'Adidas',''),
('IMG-20261109-WA1097.jpg',[('3789','H')],'On Cloud Running','verde menta y blanco',105,'Otras',''),
('IMG-20261109-WA1099.jpg',[('3788','H')],'On Cloud Running','crema y vinotinto',105,'Otras',''),
('IMG-20261109-WA1098.jpg',[('3787','H')],'On Cloud Running','naranja y verde',105,'Otras',''),
]
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def mk(src,l1,l2,W,H,out):
    im=Image.open(src).convert('RGB');w,hh=im.size
    im=im.crop((0,int(.12*hh),w,hh))
    hb=round(H*0.12);ph=H-hb
    im=im.resize((W,ph),Image.LANCZOS)
    c=Image.new('RGB',(W,H),'white');c.paste(im,(0,hb));d=ImageDraw.Draw(c)
    f1=ImageFont.truetype(FB,round(W*0.043));f2=ImageFont.truetype(FB,round(W*0.027))
    while d.textlength(l1,font=f1)>W*0.95:f1=ImageFont.truetype(FB,f1.size-1)
    while d.textlength(l2,font=f2)>W*0.95:f2=ImageFont.truetype(FB,f2.size-1)
    d.text((W/2,hb*0.34),l1,font=f1,fill='black',anchor='mm');d.text((W/2,hb*0.74),l2,font=f2,fill='black',anchor='mm')
    c.save(out,quality=90)
def tstr(z):
    return '%dEUR al %dEUR'%(z[0],z[-1])
new=[];caps=[];seen=set()
for k,(img,cods,name,col,lista,mrc,_) in enumerate(N):
    refs=['6'+c for c,l in cods]
    f='-'.join([])  # placeholder
    parts=[]
    for i,(c,l) in enumerate(cods):parts.append(('6'+c if i==0 else c)+'-'+l)
    fn='_'.join(parts)+'.jpg'
    assert fn not in byf,fn
    pair=len(cods)==2 and {cods[0][1],cods[1][1]}=={'D','H'}
    zs=[]
    for c,l in cods:zs.append(list(range(36,40)) if l=='D' else list(range(40,45)))
    z=sorted(set(sum(zs,[])))
    t=' / '.join(tstr(x) for x in sorted(zs,key=lambda x:x[0]))
    g='DH' if pair else cods[0][1]
    l1=' / '.join('6%s-%s'%(c,l) for c,l in cods)
    mk(Z+img,l1,t,640,800,'p/'+fn)
    nn=len(caps)+1
    sendfn='%02d_%s'%(nn,fn)
    mk(Z+img,l1,t,1080,1350,SC+'b6s/'+sendfn)
    sn,si=slot()
    e=dict(f=fn,b='B6',n=name,r=refs,t=t,c=col,z=z,g=g,m=mrc,s=sn,i=si,u=u,d='25/11' if img.startswith('IMG-20261109') or img.startswith('IMG-2026100') or img.startswith('IMG-2026101') else {'20261119':'22/11','20261122':'22/11','20261123':'23/11'}[img[4:12]])
    new.append(e);byf[fn]=e
    code=' / '.join(refs) if pair else refs[0]
    caps.append(dict(f=fn,fn=sendfn,cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~'%(name,code,lista+5,t,col)))
# repostes: fechas
posts=json.load(open(Z+'posts.json'));res=json.load(open(Z+'match.json'))
lastd={}
for p in posts:
    lastd[p['f']]=p['d']   # ultimo gana
nrep=0
def dkey(s):return (int(s[3:5]),int(s[:2]))
for f,(k,s) in res.items():
    if s<0.7 or k not in byf or f not in lastd:continue
    e=byf[k];dd=lastd[f]
    if e.get('d') is None or dkey(dd)>dkey(e['d']):
        e['d']=dd
    e.pop('a',None);nrep+=1
for e in new:
    # nuevas con fecha mas reciente si se reposteo
    pass
AG=dt.date(2026,11,23);na=0
for d in D+new:
    if d['b']!='B6' or not d.get('d'):continue
    q=dt.date(2026,int(d['d'][3:5]),int(d['d'][:2]))
    if q<=AG or len(d['z'])<=3:d['a']=1;na+=1
D+=new
TW,TH=420,525
for sn in sorted({e['s'] for e in new}):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for d in D:
        if d['s']==sn:
            im=Image.open('p/'+d['f']).convert('RGB');im.thumbnail((TW,TH),Image.LANCZOS);i=d['i'];sh.paste(im,((i%4)*TW+(TW-im.width)//2,(i//4)*TH+(TH-im.height)//2))
    sh.save('s/%03d.jpg'%sn,quality=66,optimize=True)
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):];open('index.html','w',encoding='utf-8').write(h)
json.dump(caps,open('/tmp/w/b6/caps.json','w'),ensure_ascii=False)
print('nuevas',len(new),'reposts',nrep,'agotado',na)
for c in caps:print(c['fn'],'|',c['cap'].replace('\n',' / '))
