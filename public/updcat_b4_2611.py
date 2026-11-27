import re,json,os,sys,datetime as dt
exec(open('/home/claude/cat-logo-local4b/public/updcat_b3b4b5_2211.py').read().split("os.chdir")[0])
os.chdir('/home/claude/cat-logo-local4b/public')
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
SC='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
smax=max(d['s'] for d in D);S=[smax,sum(1 for d in D if d['s']==smax)]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
def mk(n):
    l=n.lower()
    for k,b in(('on cloud','On Cloud'),('skechers','Skechers'),('under armour','Under Armour'),('puma','Puma'),('le coq','Le Coq Sportif'),('new balance','New Balance'),('nike','Nike'),('adidas','Adidas')):
        if k in l:return b
    return 'Otras'
NM={'5167':('On Cloudtilt X Loewe','verde oliva'),'3858':('Puma Wild Rider','negro blanco plata'),'5935':('Skechers Go Run Elevate 2.0','negro blanco'),'5220':('Skechers Max','gris lila'),'5591':('Tommy Hilfiger','beige crema'),'5594':('Tommy Hilfiger','negro'),'5712':('Tommy Hilfiger','negro suela café'),'5271':('Tommy Hilfiger','negro'),'5267':('Under Armour Phantom 4','negro blanco'),'5266':('Under Armour Phantom 4','negro'),'4941':('Valentino Garavani','blanco'),'6071':('Nike Chancla Mind 001','blanco crema'),'6072':('Nike Chancla Mind 001','rojo naranja'),'6378':('Under Armour Storm Proof','verde oliva'),'6183':('Under Armour Storm Proof','crema beige'),'6182':('Under Armour Storm Proof','negro gris'),'5639':('Le Coq Sportif','negro rosado'),'5642':('Le Coq Sportif','negro'),'4415':('New Balance 999','negro suela café'),'5914':('Polo Ralph Lauren 89','negro blanco'),'6085':('Polo Ralph Lauren','gris'),'5913':('Polo Ralph Lauren 89','negro rojo'),'5589':('Tommy Hilfiger','azul oscuro'),'5590':('Tommy Hilfiger','blanco'),'5587':('Tommy Hilfiger','negro'),'5805':('Tommy Hilfiger Tabla','azul oscuro'),'5807':('Tommy Hilfiger Tabla','beige'),'6180':('Under Armour Vibram','beige crema'),'6178':('Under Armour Vibram','café arena')}
new=[];caps=[];os.makedirs(SC+'n26',exist_ok=True)
def addnew(e,src,lab,crop,cap):
    sn,si=slot();e.update(s=sn,i=si,u=u);assert e['f'] not in byf,e['f']
    make(src,lab,'p/'+e['f'],640,800,crop);k=len(caps)+1
    make(src,lab,SC+'n26/%02d_%s'%(k,e['f']),1080,1350,crop)
    caps.append(dict(f=e['f'],fn='%02d_%s'%(k,e['f']),cap=cap));new.append(e);byf[e['f']]=e
def dd(s):return s[:5]
def upd(d,date,z,caja_flag):
    d['d']=date;d.pop('a',None);d.pop('h',None)
    if caja_flag:d['x']=1
    else:d.pop('x',None)
    if z and len(d['r'])==1:
        zz=[n for n in z if n<=39] if d['g']=='D' else ([n for n in z if n>=40] if d['g']=='H' else z)
        if zz and zz!=d['z']:d['z']=zz;d['t']=tstr(zz)
B4=json.load(open('/tmp/w/b4_2611.json'));rep=0;seen=set()
for x in B4:
    if x['ex']:
        for f in x['ex']:upd(byf[f],dd(x['h']),x['z'],x['caja']);rep+=1
for x in B4:
    if x['ex'] or not x['ref']:continue
    ref=x['ref'];
    if ref in seen:continue
    seen.add(ref);z=x['z'];lista=x['price'];cost=lista if lista<=50 else lista-10;P=pub(cost);n,col=NM[ref]
    g='N' if max(z)<=35 else ('D' if max(z)<=39 else 'H');code='4'+ref;f='%s-%s.jpg'%(code,g);t=tstr(z);lab='%s-%s/%s'%(code,g,t.lower())
    e=dict(f=f,b='B4',n=n,r=[code],t=t,c=col,z=z,g=g,m=mk(n),d=dd(x['h']))
    if x['caja']:e['x']=1
    cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~'%(n,code,P,t,col)
    if x['promo']:cap+='\n❌ _No cambio, no garantía_'
    addnew(e,'/tmp/q/m/'+x['f'],lab,0.125,cap)
AG=dt.date(2026,11,23);na=0
for d in D+new:
    if d['b'] in('B3','B4') and d.get('d') and not d.get('a'):
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
json.dump(caps,open('/tmp/w/caps_26.json','w'),ensure_ascii=False)
print('nuevas',len(new),'repostes',rep,'agotado',na)
for c in caps:print(c['fn'],'|',c['cap'].replace('\n',' / '))
