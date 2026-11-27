import re,json,os,sys,datetime as dt
exec(open('updcat_b3b4b5_2211.py').read().split("os.chdir")[0])  # make,tstr,Image,ImageDraw
os.chdir('/home/claude/cat-logo-local4b/public')
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
SC='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
smax=max(d['s'] for d in D);S=[smax,sum(1 for d in D if d['s']==smax)]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
def brand(n):
    for b in('The North Face','Louis Vuitton','Gucci','On Cloud','Jordan','Under Armour','Adidas','Nike','Puma','Vans','Reebok','Coach','Columbia','New Balance','Skechers','The North Face','Tommy Hilfiger','Dolce & Gabbana'):
        if b.lower() in n.lower():return b
    return 'Otras'
C='Chancla Nike'; T='Chancla Nike TN'
INFO={'02352':('Jordan 1 Mid','rojo vino y negro'),'02663':('Chancla On Cloud','gris y negro'),'02665':('Chancla On Cloud','café y crema'),'02664':('Chancla On Cloud','rojo y negro'),'02660':('Chancla On Cloud','verde y blanco'),'02662':('Chancla On Cloud','negro y blanco'),'02639':('Chancla On Cloud','rojo y negro'),'02638':('Chancla On Cloud','gris y negro'),'02640':('Chancla On Cloud','blanco y negro'),'02661':('Chancla On Cloud','rojo y blanco'),'02637':('Chancla On Cloud','verde y crema'),'00550':('Nike Air Force 1','verde militar')}
rows=json.load(open('/tmp/w/rows_b0_2611b.json'))
os.makedirs('/mnt/user-data/uploads/n26d',exist_ok=True);caps=[];new=[];seen=set();nrep=0
for r in rows:
    ref=r['ref']
    if ref in seen:continue
    seen.add(ref);raw=r['raw'].upper();name,col=INFO[ref]
    dd=r['d']
    if 'DAMA' in raw:L='D';z=[36,37] if 'DAMA 36, 37' in raw else list(range(36,42)) if '36 AL 41' in raw else [36,37,38,39,40]
    else:
        L='H';m=re.search(r'DEL (\d+) AL (\d+)',raw);m2=re.search(r'SOLO (\d+)',raw)
        z=[int(m2[1])] if m2 else list(range(int(m[1]),int(m[2])+1))
    t=tstr(z);P=r['p']+5
    ex=[k for k in byf if byf[k]['b']=='B0' and byf[k]['r']==[ref]]
    f=ex[0] if ex else '%s-%s.jpg'%(ref,L)
    im=Image.open('/tmp/w/y3/'+r['f']).convert('RGB');W,H=im.size
    import cv2,numpy as np
    a=cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR);mk=np.zeros(a.shape[:2],np.uint8);mk[0:int(.11*H),int(.66*W):W]=255
    im=Image.fromarray(cv2.cvtColor(cv2.inpaint(a,mk,7,cv2.INPAINT_TELEA),cv2.COLOR_BGR2RGB))
    tmp='/tmp/w/_t.jpg';im.save(tmp,quality=95);lab='%s/%s'%(f[:-4],t.lower())
    fn='%02d_%s'%(len(caps)+1,f)
    make(tmp,lab,'/mnt/user-data/uploads/n26d/'+fn,1080,1350,0)
    if ex:
        e=byf[f];e['d']=dd;e.pop('a',None);e.pop('h',None);e['z']=z;e['t']=t;e['g']=L;nrep+=1
        make(tmp,lab,'p/'+f,640,800,0)
    else:
        sn,si=slot();e=dict(f=f,b='B0',n=name,r=[ref],t=t,c=col,z=z,g=L,m=brand(name),s=sn,i=si,u=u,d=dd)
        make(tmp,lab,'p/'+f,640,800,0);new.append(e);byf[f]=e
    caps.append(dict(f=f,fn=fn,cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~'%(name,ref,P,t,col)))
AG=dt.date(2026,11,23);na=0
for d in D+new:
    if d['b']=='B0' and d.get('d') and not d.get('a'):
        q=dt.date(2026,int(d['d'][3:5]),int(d['d'][:2]))
        if q<=AG or (len(d['z'])<=3):d['a']=1;na+=1
D+=new
TW,TH=420,525
for sn in sorted({e['s'] for e in new}):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for d in D:
        if d['s']==sn:
            im=Image.open('p/'+d['f']).convert('RGB');im.thumbnail((TW,TH),Image.LANCZOS);i=d['i'];sh.paste(im,((i%4)*TW+(TW-im.width)//2,(i//4)*TH+(TH-im.height)//2))
    sh.save('s/%03d.jpg'%sn,quality=66,optimize=True)
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):];open('index.html','w',encoding='utf-8').write(h)
json.dump(caps,open('/tmp/w/caps_b0_2611b.json','w'),ensure_ascii=False)
print('nuevas',len(new),'reposts',nrep,'caps',len(caps),'agotado',na)
for c in caps:print(c['fn'],'|',c['cap'].replace('\n',' / '))
