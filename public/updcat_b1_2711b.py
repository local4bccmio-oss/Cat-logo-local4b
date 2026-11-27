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
INFO={'1803':('Nike Zoom Vomero 5','plateado y celeste','Nike'),'348':('On Cloud','negro y blanco','On Cloud'),'1830':('New Balance 1000','rosado y crema','New Balance'),'126':('Adidas Samba','blanco y beige','Adidas'),'5006':('Nike SB Dunk Low','gris oscuro y blanco','Nike'),'1470':('New Balance','verde y crema','New Balance'),'5001':('Nike P-6000','blanco y turquesa','Nike')}
rows=json.load(open('/tmp/w/rows_b1_2711b.json'))[6:]
OA='/mnt/user-data/uploads/n27d';os.makedirs(OA,exist_ok=True);new=[];caps=[]
for k,r in enumerate(rows,1):
    ref=r['ref'];g=r['g'];code='1'+ref;L=r['p'];cb=45 if ref=='5006' else r['cb'];par=L+(20 if L<=65 else 15);f='%s-%s.jpg'%(code,g);src='/tmp/w/c4/'+r['f']
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
json.dump(caps,open('/tmp/w/caps_b1_2711b.json','w'),ensure_ascii=False)
print('nuevas',len(new))
for c in caps:print(c['fn'],'|',c['cap'].replace('\n',' / '))
