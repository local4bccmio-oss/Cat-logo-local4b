import re,json,os,sys,datetime as dt
from PIL import Image,ImageDraw,ImageFont,ImageFilter
exec(open('updcat_b3b4b5_2211.py').read().split("os.chdir")[0].split("def pub")[0])
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
OUT='/mnt/user-data/uploads/n26c';os.makedirs(OUT,exist_ok=True)
smax=max(d['s'] for d in D);S=[smax,sum(1 for d in D if d['s']==smax)]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
INFO={'4568':('Nike Dunk Low','lila y blanco','Nike'),'3661':('Nike Dunk Low','azul y blanco','Nike'),'4713':('Nike Dunk Low','beige y blanco','Nike'),'4980':('Puma','blanco y rosado','Puma'),'4964':('Converse Chuck 70','beige','Converse'),'4977':('Jordan 1 Mid','lila y blanco','Jordan'),'4974':('Jordan 1 Low','rosado','Jordan'),'1507':('Nike Air Max2 Light','negro multicolor','Nike'),'2120':('New Balance 9060','morado multicolor','New Balance'),'971':('Adidas Superstar','blanco y negro','Adidas'),'892':('New Balance','verde y blanco','New Balance'),'838':('Bota Nike','negro','Nike'),'1741':('New Balance 574','azul claro y rosado','New Balance'),'3638':('Puma Suede XL','blanco','Puma'),'3524':('On Cloudtilt','blanco y café','On Cloud'),'4969':('Jordan 1 Low','crema y azul','Jordan'),'3177':('On Cloud','crema','On Cloud'),'4978':('Puma','blanco y crema','Puma'),'206':('Puma','blanco y azul','Puma'),'2935':('Nike','blanco','Nike'),'4244':('Adidas Samba','crema y café','Adidas'),'4967':('Jordan 1 Low','blanco y dorado','Jordan'),'5004':('Guayos Nike Mercurial','azul y blanco','Nike'),'4979':('Puma','negro y blanco','Puma'),'1864':('Nike Kyrie','gris y rosado','Nike'),'4983':('Bota Under Armour','beige','Under Armour'),'4968':('Jordan 4','azul jean','Jordan')}
R=json.load(open('/tmp/w/b1n_2611.json'));new=[];caps=[];nrep=0
for it in R:
    ref=it['ref'];g=it['g'];code='1'+ref;L=it['p'];cb=it['cb'];par=L+(20 if L<=65 else 15);f='%s-%s.jpg'%(code,g);src='/tmp/w/g1n/'+it['f']
    if it['ex']:
        f=it['ex'][0];d=byf[f];n,c,t=d['n'],d['c'],d['t'];g=f[-5]
        if d.get('d')!='26/11':nrep+=1
        d['d']='26/11';d.pop('a',None);d.pop('h',None)
        if cb:d['x']=1
    else:
        n,c,m=INFO[ref];z=[36,37,38,39] if g=='D' else [40,41,42,43,44];t=tstr(z);sn,si=slot()
        d=dict(f=f,b='B1',n=n,r=[code],t=t,c=c,z=z,g=g,m=m,s=sn,i=si,u=u,d='26/11')
        if cb:d['x']=1
        make(src,'%s-%s/%s'%(code,g,t.lower()),'p/'+f,640,800,0);new.append(d);byf[f]=d
    k=len(caps)+1;make(src,'%s-%s/%s'%(code,g,t.lower()),OUT+'/%02d_%s'%(k,f),1080,1350,0)
    cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~'%(n,code,par,t,c)
    if cb:cap+='\n📦 _$%d.000 por caja_'%(cb+5)
    caps.append(dict(f=f,fn='%02d_%s'%(k,f),cap=cap,caja=(cb+5) if cb else None))
AG=dt.date(2026,11,12);na=0
for d in D+new:
    if d['b']=='B1' and d.get('d') and not d.get('a'):
        q=dt.date(2026,int(d['d'][3:5]),int(d['d'][:2]))
        if q<=AG:d['a']=1;na+=1
D+=new
TW,TH=420,525
for sn in sorted({e['s'] for e in new}):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for d in D:
        if d['s']==sn:
            im=Image.open('p/'+d['f']).convert('RGB');im.thumbnail((TW,TH),Image.LANCZOS);i=d['i'];sh.paste(im,((i%4)*TW+(TW-im.width)//2,(i//4)*TH+(TH-im.height)//2))
    sh.save('s/%03d.jpg'%sn,quality=66,optimize=True)
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):];open('index.html','w',encoding='utf-8').write(h)
json.dump(caps,open('/tmp/w/caps_b1_2611.json','w'),ensure_ascii=False)
print('nuevas',len(new),'reposts',nrep,'agotado',na,len(caps))
for c in caps:print(c['fn'],'|',c['cap'].replace('\n',' / '))
