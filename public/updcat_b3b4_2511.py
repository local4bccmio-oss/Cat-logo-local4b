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
def brand(n):
    for b in('Under Armour','Lacoste','Hoka','Puma','Timberland','Off White','Adidas','Nike'):
        if b.lower() in n.lower():return b
    return 'Otras'
def mk(n):
    if 'on cloud' in n.lower():return 'On Cloud'
    return brand(n)
NM={'5838':'Adidas Alpha Bounce','5890':'Adidas SL 72','5748':'Asics Gel 1130','3640':'Diesel Tyche','6161':'Hugo Boss Runner','5706':'Hugo Boss','5273':'Le Coq Runner','6096':'Louis Vuitton Trainer','5216':'New Balance 530','3116':'Nike AF1','5378':'Nike SB Dunk','4998':'Nike SB Dunk Jarrito','4607':'Nike SB Dunk','6039':'Nike SB Dunk Supreme','6054':'Nike SB Dunk','5173':'Nike Shox','5179':'Nike Shox Ride 2','5193':'Nike Skate','5688':'Nike V2K Kids','5858':'Nike Vomero 18','5847':'Nike Vomero 18','5849':'Nike Vomero 18','5428':'Nike Vomero 5','5959':'Nike Vomero Plus','5563':'Nike Zoom','4264':'Nike Zoom X','5301':'On Cloud Eclipse'}
COL={'5838':'negro azul turquesa','5890':'negro blanco verde','5748':'gris crema','3640':'verde azul gris','6161':'café','5706':'negro','5273':'negro rojo azul','6096':'blanco negro','5216':'negro blanco','3116':'crema rosado','5378':'negro blanco gris','4998':'crema verde','4607':'blanco crema','6039':'gris claro','6054':'negro gris','5173':'plata gris','5179':'negro azul oscuro','5193':'blanco crema negro','5688':'blanco gris rosado','5858':'lila azul amarillo','5847':'turquesa blanco','5849':'blanco verde','5428':'gris rosado','5959':'rosado crema','5563':'gris plata azul','4264':'negro blanco','5301':'negro gris azul'}
new=[];caps=[];os.makedirs(SC+'n25',exist_ok=True)
def addnew(e,src,lab,crop,cap):
    sn,si=slot();e.update(s=sn,i=si,u=u,d=e['d']);assert e['f'] not in byf,e['f']
    make(src,lab,'p/'+e['f'],640,800,crop);k=len(caps)+1
    make(src,lab,SC+'n25/%02d_%s'%(k,e['f']),1080,1350,crop)
    caps.append(dict(f=e['f'],fn='%02d_%s'%(k,e['f']),cap=cap));new.append(e);byf[e['f']]=e
# ---------- B4 reposts
def dd(s):return s[:5]
rep4=0;B4=json.load(open('/tmp/w/b4_2511.json'))
def upd(d,date,z,caja_flag):
    d['d']=date;d.pop('a',None);d.pop('h',None)
    if caja_flag:d['x']=1
    else:d.pop('x',None)
    if z and len(d['r'])==1:
        zz=[n for n in z if n<=39] if d['g']=='D' else ([n for n in z if n>=40] if d['g']=='H' else z)
        if zz and zz!=d['z']:d['z']=zz;d['t']=tstr(zz)
for x in B4:
    if x['ex']:
        for f in x['ex']:upd(byf[f],dd(x['h']),x['z'] if len(x['ex'])==1 else x['z'],x['caja']);rep4+=1
# ---------- B4 nuevas
seen=set()
for x in json.load(open('/tmp/w/b4_new_2511.json')):
    ref=x['ref'];z=x['z'];lista=x['price'] if x['price'] else 20;cost=lista if lista<=50 else lista-10;P=pub(cost);n=NM[ref];col=COL[ref]
    promo=bool(re.search(r'NO\s+CAMBI|GARANT',x['raw'].upper()));src='/tmp/w/mym/'+x['f'];date=dd(x['h'])
    if ref=='4998':
        f='44998-D_4022-H.jpg';refs=['44998','44022'];g='DH';t='36EUR / 42EUR-43EUR';lab='44998-D/36eur  4022-H/42eur-43eur';zz=[36,42,43];refl='44998 / 44022'
    else:
        g='N' if max(z)<=35 else ('D' if max(z)<=39 else 'H');code='4'+ref;f='%s-%s.jpg'%(code,g);refs=[code];t=tstr(z);lab='%s-%s/%s'%(code,g,t.lower());zz=z;refl=code
    e=dict(f=f,b='B4',n=n,r=refs,t=t,c=col,z=zz,g=g,m=mk(n),d=date)
    cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~'%(n,refl,P,t,col)
    if promo:cap+='\n❌ _No cambio, no garantía_'
    addnew(e,src,lab,0.125,cap)
# ---------- B3 reposts y nuevas
B3=json.load(open('/tmp/w/b3_2511.json'));rep3=0
for x in B3:
    for f in x['ex']:upd(byf[f],'24/11',x['tal'],bool(x['caja']));rep3+=1
B3N={'1923':('Reebok Club C','blanco verde'),'1801':('Adidas Super Star Core','blanco gris'),'1802':('Adidas Super Star Core','negro gris'),'2215':('Polo','gris'),'2010':('Puma Suede XL','azul oscuro blanco'),'1988':('Puma Suede XL','negro rojo'),'1986':('Puma Suede XL','negro blanco')}
for x in B3:
    if x['codes'] and not x['ex']:
        cd=x['codes'][0];n,col=B3N[cd];g='D' if cd=='1923' else 'H';z=x['tal'] if cd=='1923' else [40,41,42,43,44];cost=x['price']-10;P=pub(cost);code='3'+cd;f='%s-%s.jpg'%(code,g);t=tstr(z)
        e=dict(f=f,b='B3',n=n,r=[code],t=t,c=col,z=z,g=g,m=mk(n),d='24/11')
        if x['caja']:e['x']=1
        cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~'%(n,code,P,t,col)
        if x['caja']:cap+='\n📦 _$%d.000 por caja_'%x['caja']
        addnew(e,'/tmp/w/myl/'+x['f'],'%s-%s/%s'%(code,g,t.lower()),0.0,cap)
# ---------- aviso agotado (d <= hoy-3 = 22/11)
AG=dt.date(2026,11,22);na=0
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
json.dump(caps,open('/tmp/w/caps_25.json','w'),ensure_ascii=False)
print('nuevas',len(new),'rep4',rep4,'rep3',rep3,'agotado',na)
for c in caps:print(c['fn'],'|',c['cap'].replace('\n',' / '))
