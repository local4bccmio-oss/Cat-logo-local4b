import re,json,os,sys,datetime as dt
exec(open('updcat_b3b4b5_2211.py').read().split("os.chdir")[0])  # make,tstr,Image
os.chdir('/home/claude/cat-logo-local4b/public')
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
SC='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
smax=max(d['s'] for d in D);S=[smax,sum(1 for d in D if d['s']==smax)]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
rows=json.load(open('/tmp/w/juka_rows.json'))
def szs(t):
    m=re.search(r'(?:TALLAS DISPONIBLES|ᴛᴀʟʟᴀs ᴅɪsᴘᴏɴɪʙʟᴇs|SOLO)[^\d]*([\d/ ]+)',t) or re.search(r'DAMA🌺 SOLO (\d+)',t)
    if 'SOLO 39' in t:return [39]
    if 'SOLO 40' in t:return [40]
    return [int(x) for x in re.findall(r'\d{2}',m[1])] if m else []
def pdate(d):
    if '/' not in (d or ''):return dt.date(2026,1,1)
    a,b=d.split('/');return dt.date(2026,int(b),int(a))
# último post por código
last={}
for k,(c,t) in rows.items():
    d,f=k.split('|')
    if c:last[c]=(d,f,t)
# 1) existentes: fecha/tallas
upd=0
for d_ in D:
    if d_['b']!='B8':continue
    cs=['%03d'%int(r) for r in d_['r']]
    cand=[last[c] for c in last if c in cs or any(x in cs for x in c.split('-'))]
    if not cand:continue
    d0,f0,t0=max(cand,key=lambda x:pdate(x[0]))
    if pdate(d0)>pdate(d_['d']):
        d_['d']=d0;upd+=1
        if len(d_['r'])==1:
            z=szs(t0)
            if z:d_['z']=z;d_['t']=tstr(z)
        if pdate(d0)>=dt.date(2026,11,23):d_.pop('a',None);d_.pop('h',None)
# 2) nuevos
N=[ # code,nombre,color,letras(D/H/M/pair),precio lista
('065','Asics Gel','fucsia y plateado','D'),('072','Nike Air Force 1','blanco','D'),('097','Nike Trail','azul claro, verde neón y naranja','D'),('099','Nike Trail','negro y blanco','H'),('147','Nike Zoom X','negro, blanco y amarillo neón','H'),('190','Nike P-6000','crema y rosado','D'),('068','On Cloud','negro y blanco','D'),('021-022','Adidas EQ21','negro, gris y blanco','P'),('167','On Cloud Cloudtec','negro','H'),('248-249','Nike Air Force 1','blanco y verde','P'),
('340','Nike Asuna','negro','M'),('262','On Cloud Cloudrunner','gris azulado, azul y blanco','D'),('334','On Cloud Horizon','blanco, gris y naranja','H'),('339','On Cloud Jamaica','beige, rosado y verde lima','D'),('330','On Cloud Horizon','gris, azul oscuro y verde lima','H'),('336','On Cloud Horizon','azul grisáceo y amarillo lima','H'),('333','On Cloud Cloudrunner','blanco, rosado y verde lima','D'),('332','On Cloud Surfer','blanco, malva y negro','D'),('259','On Cloud Cloudrunner','gris claro y blanco','H'),('329','On Cloud Cloudrunner','blanco y verde lima','D'),('331','On Cloud Cloudrunner','blanco y rosado','D'),('235','On Cloud Flow 5','celeste y blanco','D'),('227','On Cloud Flow 5','negro','H'),('231','On Cloud Running','blanco y negro','H'),('233','On Cloud Flow 5','gris','D')]
def brand(n):
    for b in('Adidas','Nike','On Cloud','Asics'):
        if n.startswith(b):return b
    return 'Otras'
os.makedirs(SC+'b8m',exist_ok=True);caps=[];new=[]
for code,name,col,L in N:
    d0,f0,t0=last[code];z=szs(t0);P0=int(re.search(r'(\d\d)\.000',t0)[1]);promo=(P0==60)
    pub=P0+5
    cs=code.split('-')
    if L=='P':
        c1,c2=cs;f='8%s-D_%s-H.jpg'%(c1,c2);g='DH';r=[c1,c2];fl='8%s-D_%s-H'%(c1,c2)
        z=[36] if code=='021-022' else [36,40]
        ref='%s/%s'%('8'+c1,'8'+c2)
    else:
        f='8%s-%s.jpg'%(code,L);g='DH' if L=='M' else L;r=[code];fl='8%s-%s'%(code,L);ref='8'+code
    t=tstr(z)
    assert f not in byf,f
    sn,si=slot();e=dict(f=f,b='B8',n=name,r=r,t=t,c=col,j='',z=z,g=g,m=brand(name),s=sn,i=si,u=u,d=d0)
    src='/tmp/w/juka/'+f0;fn='%02d_%s'%(len(caps)+1,f)
    lab='%s/%s'%(fl,t.lower())
    make(src,lab,'p/'+f,640,800,0);make(src,lab,SC+'b8m/'+fn,1080,1350,0)
    cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~'%(name,ref,pub,t,col)
    if promo:cap+='\n❌ _No cambio, no garantía_'
    caps.append(dict(f=f,fn=fn,cap=cap));new.append(e);byf[f]=e
AG=dt.date(2026,11,22);na=0
for d in D+new:
    if d['b']=='B8' and d.get('d') and not d.get('a') and pdate(d['d'])<=AG:d['a']=1;na+=1
D+=new
TW,TH=420,525
for sn in sorted({e['s'] for e in new}):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for d in D:
        if d['s']==sn:
            im=Image.open('p/'+d['f']).convert('RGB');im.thumbnail((TW,TH),Image.LANCZOS);i=d['i'];sh.paste(im,((i%4)*TW+(TW-im.width)//2,(i//4)*TH+(TH-im.height)//2))
    sh.save('s/%03d.jpg'%sn,quality=66,optimize=True)
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):];open('index.html','w',encoding='utf-8').write(h)
json.dump(caps,open('/tmp/w/caps_b8_2511.json','w'),ensure_ascii=False)
print('upd',upd,'nuevas',len(new),'agotado',na)
for c in caps:print(c['fn'],'|',c['cap'].replace('\n',' / '))
