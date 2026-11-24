import re,json,os,sys,datetime as dt
from PIL import Image,ImageDraw,ImageFont,ImageFilter
exec(open('updcat_b3b4b5_2211.py').read().split("os.chdir")[0].split("def pub")[0])  # make, tstr
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
SC='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
smax=max(d['s'] for d in D);S=[smax,sum(1 for d in D if d['s']==smax)]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
B1=json.load(open('/tmp/w/b1i_2411.json'))
NEW1={('4282','D'):('New Balance 9060','blanco','New Balance')}
rb1=0;newb1=[];last={}
for it in B1:
    ref=it['ref'];g=it['g'];key=(ref,g)
    if key in NEW1:
        if key not in [k for k,_ in newb1]:newb1.append((key,it))
        continue
    code='1'+ref
    fs=[f for f in byf if byf[f]['b']=='B1' and re.fullmatch(re.escape(code)+r'-[A-Z]+\.jpg',f) and (not g or f.endswith('-'+g+'.jpg') or g not in 'DH')]
    if not fs:fs=[f for f in byf if byf[f]['b']=='B1' and re.fullmatch(re.escape(code)+r'-[A-Z]+\.jpg',f)]
    if ref=='1616':fs=['11616-D.jpg']
    assert fs,(ref,g)
    for f in fs:last[f]=it
for f,it in last.items():
    d=byf[f];d['d']='%02d/%02d'%(it['d'][2],it['d'][1]);d.pop('a',None);d.pop('h',None)
    if it['c']:d['x']=1
    else:d.pop('x',None)
    rb1+=1
new=[];caps=[]
os.makedirs(SC+'b1n',exist_ok=True)
for (ref,g),it in newb1:
    n,c,m=NEW1[(ref,g)];L=it['p'];cb=it['c'];code='1'+ref;z=[36,37,38,39] if g=='D' else [40,41,42,43,44];t=tstr(z);par=L+(20 if L<=65 else 15)
    cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~'%(n,code,par,t,c)
    if cb:cap+='\n📦 _$%d.000 por caja_'%(cb+5)
    f='%s-%s.jpg'%(code,g);sn,si=slot()
    e=dict(f=f,b='B1',n=n,r=[code],t=t,c=c,z=z,g=g,m=m,s=sn,i=si,u=u,d='23/11')
    if cb:e['x']=1
    src='/tmp/z_loc24/'+it['f'];lab='%s-%s/%s'%(code,g,t.lower())
    make(src,lab,'p/'+f,640,800,0);make(src,lab,SC+'b1n/'+f,1080,1350,0)
    new.append(e);byf[f]=e;caps.append(dict(f=f,cap=cap,caja=(cb+5) if cb else None))
# banderas B1: >14 días sin post => agotado (igual que antes: ≤14/11)
AG=dt.date(2026,11,14);na=0
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
json.dump(caps,open('/tmp/w/caps_b1_2411.json','w'),ensure_ascii=False)
print('B1 reposts',rb1,'nuevas',[e['f'] for e in new],'agotado nuevos',na)
for c in caps:print(c['f']);print(c['cap'])
