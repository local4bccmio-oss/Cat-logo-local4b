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
INFO={'4182':('Adidas Samba','negro y blanco','Adidas'),'1580':('Nike Zoom Vomero 5','blanco y azul oscuro','Nike'),'4972':('Jordan 1 Low','celeste y blanco','Jordan'),'4959':('Adidas Superstar','rosado claro','Adidas'),'807':('Converse Tom y Jerry','crema multicolor','Converse'),'2205':('Nike Free Metcon','negro y blanco','Nike'),'896':('Guayos Adidas','rosado y lila','Adidas'),'4990':('Nike P-6000','café y beige','Nike'),'4975':('Jordan','rojo y negro','Jordan')}
rows=json.load(open('/tmp/w/rows_b1_2711d.json'))
OA='/mnt/user-data/uploads/n27e';os.makedirs(OA,exist_ok=True);new=[];caps=[]
for k,r in enumerate(rows,1):
    ref=r['ref'];g=r['g'];code='1'+ref;L=r['p'];cb=r['cb'];par=L+(20 if L<=65 else 15);f='%s-%s.jpg'%(code,g);src='/tmp/w/c6/'+r['f']
    if f in byf:
        d=byf[f];n,c,t=d['n'],d['c'],d['t'];d['d']='27/11';d.pop('a',None);d.pop('h',None);d['x']=1
    else:
        n,c,m=INFO[ref];z=[36,37,38,39] if g=='D' else [40,41,42,43,44];t=tstr(z);sn,si=slot()
        d=dict(f=f,b='B1',n=n,r=[code],t=t,c=c,z=z,g=g,m=m,s=sn,i=si,u=u,d='27/11',x=1)
        make(src,'%s-%s/%s'%(code,g,t.lower()),'p/'+f,640,800,0);new.append(d);byf[f]=d
    make(src,'%s-%s/%s'%(code,g,t.lower()),OA+'/%02d_%s'%(k,f),1080,1350,0)
    cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~\n📦 _$%d.000 por caja_'%(n,code,par,t,c,cb+5)
    caps.append(dict(f=f,fn='%02d_%s'%(k,f),cap=cap,caja=cb+5,gen='dama' if g=='D' else 'hombre'))
D+=new
TW,TH=420,525
for sn in sorted({e['s'] for e in new}):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for d in D:
        if d['s']==sn:
            im=Image.open('p/'+d['f']).convert('RGB');im.thumbnail((TW,TH),Image.LANCZOS);i=d['i'];sh.paste(im,((i%4)*TW+(TW-im.width)//2,(i//4)*TH+(TH-im.height)//2))
    sh.save('s/%03d.jpg'%sn,quality=66,optimize=True)
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):];open('index.html','w',encoding='utf-8').write(h)
json.dump(caps,open('/tmp/w/caps_b1_2711d.json','w'),ensure_ascii=False)
print('nuevas',len(new))
for c in caps:print(c['fn'],'|',c['cap'].replace('\n',' / '))
