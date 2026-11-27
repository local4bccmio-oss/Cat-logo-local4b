import re,json,os,sys,datetime as dt
exec(open('updcat_b3b4b5_2211.py').read().split("os.chdir")[0])
os.chdir('/home/claude/cat-logo-local4b/public')
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
smax=max(d['s'] for d in D);S=[smax,sum(1 for d in D if d['s']==smax)]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
def brand(n):
    for b in('Skechers','Burberry','The North Face','On Cloud','Jordan','Adidas','Nike','Puma','New Balance'):
        if b.lower() in n.lower():return b
    return 'Otras'
CS='Chancla Skechers';CN='Chancla Nike';CB='Chancla Burberry'
INFO={'02675':(CS,'rojo y negro'),'02678':(CS,'gris oscuro y verde'),'02653':(CS,'blanco y negro'),'02652':(CS,'rojo y negro'),'02677':(CS,'negro y rojo'),'02650':(CS,'negro y beige'),'02676':(CS,'gris oscuro y beige'),'02679':(CS,'azul oscuro y celeste'),'02654':(CS,'gris y negro'),'02651':(CS,'negro'),
'02628':(CN,'verde militar y verde lima'),'02629':(CN,'blanco y negro'),'02659':(CN,'camuflado y negro'),'01449':(CN,'negro'),'02755':(CN,'verde menta'),'02754':(CN,'rosado'),
'02752':(CB,'gris oscuro'),'02753':(CB,'rojo y negro'),'02751':(CB,'café y beige'),
'02788':('Adidas Samba','blanco y beige'),'02708':('Nike Zoom Vomero 5','negro'),'02600':('On Cloudsurfer','gris y blanco'),'01062':('Adidas Samba','negro y crema'),'02156':('Nike Dunk Low','café y blanco'),'02792':('Nike Dunk Low Supreme','arena')}
rows=json.load(open('/tmp/w/rows_b0_2711.json'))
OUT='/mnt/user-data/uploads/n27c';os.makedirs(OUT,exist_ok=True);caps=[];new=[];nrep=0
import cv2,numpy as np
for r in rows:
    ref=r['ref'];raw=r['raw'].upper()
    ex=[k for k in byf if byf[k]['b']=='B0' and byf[k]['r']==[ref]]
    if 'DAMA' in raw and 'HOMBRE' not in raw:
        L='D';m=re.search(r'DEL (\d+) AL (\d+)',raw);z=list(range(int(m[1]),int(m[2])+1))
    elif 'DAMA' in raw:L='DH';z=None
    else:
        L='H';m=re.search(r'DEL (\d+) AL (\d+)',raw);z=list(range(int(m[1]),int(m[2])+1))
    P=r['p']+5
    im=Image.open('/tmp/w/c3/'+r['f']).convert('RGB');W,H=im.size
    a=cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR);mk=np.zeros(a.shape[:2],np.uint8);mk[0:int(.13*H),int(.66*W):W]=255
    im=Image.fromarray(cv2.cvtColor(cv2.inpaint(a,mk,7,cv2.INPAINT_TELEA),cv2.COLOR_BGR2RGB))
    tmp='/tmp/w/_t.jpg';im.save(tmp,quality=95)
    if ex:
        f=ex[0];e=byf[f];name,col,t=e['n'],e['c'],e['t'];e['d']=r['d'];e.pop('a',None);e.pop('h',None);nrep+=1
        lab='%s/%s'%(f[:-4],t.lower());make(tmp,lab,'p/'+f,640,800,0)
    else:
        name,col=INFO[ref];t=tstr(z);f='%s-%s.jpg'%(ref,L);lab='%s/%s'%(f[:-4],t.lower())
        sn,si=slot();e=dict(f=f,b='B0',n=name,r=[ref],t=t,c=col,z=z,g=L,m=brand(name),s=sn,i=si,u=u,d=r['d'])
        make(tmp,lab,'p/'+f,640,800,0);new.append(e);byf[f]=e
    fn='%02d_%s'%(len(caps)+1,f);make(tmp,lab,OUT+'/'+fn,1080,1350,0)
    caps.append(dict(f=f,fn=fn,cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~'%(name,ref,P,t,col)))
AG=dt.date(2026,11,23);na=0
for d in D+new:
    if d['b']=='B0' and d.get('d') and not d.get('a'):
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
json.dump(caps,open('/tmp/w/caps_b0_2711.json','w'),ensure_ascii=False)
print('nuevas',len(new),'reposts',nrep,'caps',len(caps),'agotado',na)
for c in caps:print(c['fn'],'|',c['cap'].replace('\n',' / '))
