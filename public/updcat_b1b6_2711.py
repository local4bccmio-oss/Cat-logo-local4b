import re,json,os,datetime as dt
from PIL import Image,ImageDraw,ImageFont
exec(open('updcat_b3b4b5_2211.py').read().split("os.chdir")[0].split("def pub")[0])
os.chdir('/home/claude/cat-logo-local4b/public')
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
smax=max(d['s'] for d in D);S=[smax,sum(1 for d in D if d['s']==smax)]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
OA='/mnt/user-data/uploads/n27a';OB='/mnt/user-data/uploads/n27b'
os.makedirs(OA,exist_ok=True);os.makedirs(OB,exist_ok=True)
new=[];caps=[];capsB=[]
# B1: (img, ref, letra, lista, caja_bodega, nombre, color, marca)
B1=[('IMG-20261127-WA0011.jpg','4161','H',30,25,'Nike Mind Mule','blanco','Nike'),
('IMG-20261127-WA0012.jpg','2085','D',60,55,'Nike Free Metcon','negro y blanco','Nike'),
('IMG-20261127-WA0013.jpg','3008','D',70,65,'Nike Zoom Vomero 5','blanco y plateado','Nike'),
('IMG-20261007-WA0787.jpg','4762','D',70,65,None,None,None),
('IMG-20261127-WA0014.jpg','866','D',70,65,'Nike V2K','rosado y vinotinto','Nike'),
('IMG-20261127-WA0025.jpg','900','D',65,60,'Nike Pegasus Trail','verde menta','Nike')]
nrep1=0
for k,(img,ref,g,L,cb,n,c,m) in enumerate(B1,1):
    code='1'+ref;par=L+(20 if L<=65 else 15);f='%s-%s.jpg'%(code,g);src='/tmp/w/c1/'+img
    if f in byf:
        d=byf[f];n,c,t=d['n'],d['c'],d['t'];d['d']='27/11';d.pop('a',None);d.pop('h',None);d['x']=1;nrep1+=1
    else:
        z=[36,37,38,39] if g=='D' else [40,41,42,43,44];t=tstr(z);sn,si=slot()
        d=dict(f=f,b='B1',n=n,r=[code],t=t,c=c,z=z,g=g,m=m,s=sn,i=si,u=u,d='27/11',x=1)
        make(src,'%s-%s/%s'%(code,g,t.lower()),'p/'+f,640,800,0);new.append(d);byf[f]=d
    make(src,'%s-%s/%s'%(code,g,t.lower()),OA+'/%02d_%s'%(k,f),1080,1350,0)
    cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~\n📦 _$%d.000 por caja_'%(n,code,par,t,c,cb+5)
    caps.append(dict(f=f,fn='%02d_%s'%(k,f),cap=cap,caja=cb+5,gen='dama' if g=='D' else 'hombre'))
# B6 nuevas
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
B6=[('IMG-20261025-WA0353.jpg','3592','H','Jordan Retro 3','blanco, gris y celeste',95,'Jordan'),
('IMG-20261109-WA1100.jpg','3790','H','Adidas Hyperboost','azul y celeste',95,'Adidas')]
for k,(img,c_,g,n,col,lista,mrc) in enumerate(B6,1):
    fn='6%s-%s.jpg'%(c_,g);assert fn not in byf
    z=list(range(40,45));t=tstr(z);sn,si=slot()
    e=dict(f=fn,b='B6',n=n,r=['6'+c_],t=t,c=col,z=z,g=g,m=mrc,s=sn,i=si,u=u,d='27/11')
    l1='6%s-%s'%(c_,g)
    mk('/tmp/w/c2/'+img,l1,t,640,800,'p/'+fn);mk('/tmp/w/c2/'+img,l1,t,1080,1350,OB+'/%02d_%s'%(k,fn))
    new.append(e);byf[fn]=e
    capsB.append(dict(f=fn,fn='%02d_%s'%(k,fn),cap='*%s* Ref _6%s_\n*$%d.000*\n*%s*\n~%s~'%(n,c_,lista+5,t,col)))
# B6 reposts
codes='3428 3427 3595 3594 3593 3619 3620 3592 3591 3631 3632 3789 3787 3791 3793 3792 3737 3738 3454 3663 3664 3728 3729 3730 3733 3653 3748 3746 3747 3744 3745 3670 3671 3669 3668 3512 3514 3513 3461 3462 3460 3701 3700 3699 3698 3528 3529 3527 3753 3752 3750 3749 3751 3526 3605'.split()
nrep6=0;seen=set()
for d in D:
    if d['b']!='B6' or d['f'] in [e['f'] for e in new]:continue
    parts=re.findall(r'6?(\d+)-[HD]',d['f'][:-4])
    if any(p in codes for p in parts):
        seen.add(d['f']);d['d']='27/11';d.pop('a',None);nrep6+=1
print('b6 repost entries',nrep6,'codes sin entrada:',[c for c in codes if not any(c in f for f in seen)])
D+=new
TW,TH=420,525
for sn in sorted({e['s'] for e in new}):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for d in D:
        if d['s']==sn:
            im=Image.open('p/'+d['f']).convert('RGB');im.thumbnail((TW,TH),Image.LANCZOS);i=d['i'];sh.paste(im,((i%4)*TW+(TW-im.width)//2,(i//4)*TH+(TH-im.height)//2))
    sh.save('s/%03d.jpg'%sn,quality=66,optimize=True)
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):];open('index.html','w',encoding='utf-8').write(h)
json.dump(dict(a=caps,b=capsB),open('/tmp/w/caps_2711.json','w'),ensure_ascii=False)
print('nuevas',len(new),'rep B1',nrep1)
for c in caps+capsB:print(c['fn'],'|',c['cap'].replace('\n',' / '))
