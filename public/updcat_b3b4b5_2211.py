import re,json,os,sys,datetime as dt
sys.path.insert(0,'/tmp/w')
from PIL import Image,ImageDraw,ImageFont,ImageFilter
FT='/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf'
def make(src,label,out,W,H,crop=0.0):
    im=Image.open(src).convert('RGB')
    if crop:im=im.crop((0,int(im.height*crop),im.width,im.height))
    bg=im.copy();s=max(W/bg.width,H/bg.height);bg=bg.resize((int(bg.width*s)+1,int(bg.height*s)+1),Image.LANCZOS)
    bg=bg.crop(((bg.width-W)//2,(bg.height-H)//2,(bg.width-W)//2+W,(bg.height-H)//2+H)).filter(ImageFilter.GaussianBlur(W*0.037))
    s=min(W/im.width,H/im.height);fg=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=(W-fg.width)//2;y=(H-fg.height)//2;bg.paste(fg,(x,y))
    d=ImageDraw.Draw(bg);f=ImageFont.truetype(FT,round(W*0.036));tw=d.textlength(label,font=f);pad=round(W*0.022);bh=round(f.size*1.5)
    x0,y0=x+14*W//1080,y+14*W//1080;d.rounded_rectangle((x0,y0,x0+tw+2*pad,y0+bh),radius=round(bh*.3),fill='white')
    d.text((x0+pad,y0+bh/2),label,font=f,fill='black',anchor='lm');bg.save(out,quality=90);return bg
def tstr(z):
    out=[];run=[]
    for n in z:
        if run and n==run[-1]+1:run.append(n)
        else:
            if run:out.append(run)
            run=[n]
    if run:out.append(run)
    return ' / '.join(('%dEUR'%r[0]) if len(r)==1 else ('%dEUR-%dEUR'%(r[0],r[1]) if len(r)==2 else '%dEUR al %dEUR'%(r[0],r[-1])) for r in out)
def pub(cost):return cost+20 if cost<=65 else cost+15
os.chdir('/home/claude/cat-logo-local4b/public')
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
byr={}
for d in D:
    for r in d['r']:byr.setdefault((d['b'],r),[]).append(d)
SC='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
smax=max(d['s'] for d in D);cnt=sum(1 for d in D if d['s']==smax);S=[smax,cnt]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
COL=['negro blanco','azul claro gris','negro gris plata','gris azul','rojo plata','negro blanco gris','amarillo mostaza','azul jean claro','negro blanco','negro','negro','blanco','crema negro','blanco','blanco rosado','blanco negro','azul degradado blanco','crema beige','rosado lila blanco','negro blanco rojo','negro blanco','blanco morado negro','negro rojo','beige crema','negro','café gris crema','negro blanco crema','negro blanco','azul claro blanco','rosado blanco','lila blanco','negro','blanco negro café','negro blanco','rosado blanco','negro blanco','gris rosado blanco negro','blanco rosado azul','gris plomo','negro','blanco verde menta','negro blanco','blanco','naranja negro','verde oliva crema','negro blanco rojo','negro blanco','azul claro','crema gris','blanco','negro blanco','negro gris','blanco rosado negro','blanco azul','gris blanco','blanco crema','blanco negro']
NEWI=json.load(open('/tmp/w/new_items.json'));assert len(NEWI)==len(COL)==57
FIX={'Nike Tn':'Nike TN','Nike Af1':'Nike AF1','Nike Metcom 7':'Nike Metcon 7','Nike Vomero 18':'Nike Vomero 18','Nike Sb Dunk 94':'Nike SB Dunk 94'}
def brand(n):
    for b in('Under Armour','Lacoste','Hoka','Puma','Timberland','Off White','Adidas','Nike'):
        if b.lower() in n.lower():return b
    if n.lower().startswith('supernova'):return 'Adidas'
    if n.lower().startswith(('air futura','metcom','metcon','nike')):return 'Nike'
    return 'Otras'
new=[];caps={'b4':[],'b3':[],'b5':[]};newrefs={'b4':set(),'b3':set(),'b5':set()}
for k,(it,col) in enumerate(zip(NEWI,COL)):
    kd=it['k'];src='/tmp/z_%s/%s'%(kd,it['f'])
    if kd=='b4':
        nombre=it['name'].title();nombre=FIX.get(nombre,nombre)
        z=it['z'];g='D' if max(z)<=39 else 'H';lista=it['price'];cost=lista if lista<=50 else lista-10;P=pub(cost);code='4'+it['ref'];f='%s-%s.jpg'%(code,g);caja=None;refs=[code]
        t=tstr(z);lab='%s-%s/%s'%(code,g,t.lower());crop=0.125;prom=it['promo']
    elif kd=='b3':
        nombre=re.sub(r'\s*CABALLERO|\s*DAMA','',it['head'].replace('*','')).strip().title();nombre=FIX.get(nombre,nombre)
        g='H';z=[40,41,42,43,44];lista=it['price'] or int(re.search(r'\*([\d.]+)\*',it['cap'])[1].replace('.',''))//1000
        cost=lista-10;P=pub(cost);code='3'+it['cod'];f='%s-%s.jpg'%(code,g);caja=it['caja'];refs=[code];t=tstr(z);lab='%s-%s/%s'%(code,g,t.lower());crop=0.0;prom=False
    else:
        nombre=it['name'].title();nombre=FIX.get(nombre,nombre)
        refs5=it['refs'];z=it['z'];lista=it['price'];cost=lista-10;P=pub(cost);caja=it['caja'];crop=0.0;prom=it['promo']
        if len(refs5)==2:
            code=None;g='DH';f='5%s-D_%s-H.jpg'%(refs5[0],refs5[1]);refs=['5'+refs5[0],'5'+refs5[1]]
            zD=[n for n in z if n<=39];zH=[n for n in z if n>=40];t=' / '.join(x for x in(tstr(zD),tstr(zH)) if x)
            lab='5%s-D/%s  %s-H/%s'%(refs5[0],tstr(zD).lower(),refs5[1],tstr(zH).lower())
        else:
            g='D' if max(z)<=39 else 'H';code='5'+refs5[0];f='%s-%s.jpg'%(code,g);refs=[code];t=tstr(z);lab='%s-%s/%s'%(code,g,t.lower())
    b={'b4':'B4','b3':'B3','b5':'B5'}[kd]
    assert f not in byf,f
    m=brand(nombre) if kd!='b3' else brand(nombre)
    sn,si=slot();e=dict(f=f,b=b,n=nombre,r=refs,t=t,c=col,z=z,g=g,m=m,s=sn,i=si,u=u,d='22/11')
    if caja:e['x']=1
    make(src,lab,'p/'+f,640,800,crop);new.append(e);byf[f]=e
    os.makedirs(SC+kd,exist_ok=True);make(src,lab,SC+kd+'/%02d_%s'%(len(caps[kd])+1,f),1080,1350,crop)
    refl='%s'%(refs[0] if len(refs)==1 else '%s / %s'%(refs[0],refs[1]))
    cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~'%(nombre,refl,P,t,col)
    if caja:cap+='\n📦 _$%d.000 por caja_'%caja
    if prom:cap+='\n❌ _No cambio, no garantía_'
    caps[kd].append(dict(f=f,fn='%02d_%s'%(len(caps[kd])+1,f),cap=cap,caja=caja,P=P))
# ---- reposts / actualización de fichas existentes
st=dict(b4=0,b3=0,b5=0);zc=0;seenf=set()
def upd(d,z,caja_flag,setx=True):
    global zc
    d['d']='22/11';d.pop('a',None);d.pop('h',None)
    if setx:
        if caja_flag:d['x']=1
        else:d.pop('x',None)
    if z and len(d['r'])==1:
        zz=[n for n in z if n<=39] if d['g']=='D' else ([n for n in z if n>=40] if d['g']=='H' else z)
        if zz and zz!=d['z']:d['z']=zz;d['t']=tstr(zz) if d['g'] in 'DH' else d['t'];zc+=1
for x in json.load(open('/tmp/w/b4_items.json')):
    for f in x['ex']:
        if f in seenf:continue
        seenf.add(f);upd(byf[f],x['z'],x['caja']);st['b4']+=1
for x in json.load(open('/tmp/w/b3_items.json')):
    if x.get('nocode'):continue
    for f in x['ex']:
        if f in seenf:continue
        seenf.add(f);upd(byf[f],x['tal'],bool(x['caja']));st['b3']+=1
for x in json.load(open('/tmp/w/b5_items.json')):
    if not x['refs']:continue
    for f in x['ex']:
        if f in seenf:continue
        seenf.add(f);upd(byf[f],x['z'],bool(x['caja']),setx=len(x['refs'])==1);st['b5']+=1
# agotado: >3 días sin aparecer (d <= 19/11) en B3, B4, B5
AG=dt.date(2026,11,19);na=0
for d in D+new:
    if d['b'] in('B3','B4','B5') and d.get('d') and not d.get('a'):
        q=dt.date(2026,int(d['d'][3:5]),int(d['d'][:2]))
        if q<=AG:d['a']=1;na+=1
        elif d['d']=='22/11' and len(d['z'])<=3 and False:pass
D+=new
TW,TH=420,525
for sn in sorted({e['s'] for e in new}):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for d in D:
        if d['s']==sn:
            im=Image.open('p/'+d['f']).convert('RGB');im.thumbnail((TW,TH),Image.LANCZOS);i=d['i'];sh.paste(im,((i%4)*TW+(TW-im.width)//2,(i//4)*TH+(TH-im.height)//2))
    sh.save('s/%03d.jpg'%sn,quality=66,optimize=True)
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):];open('index.html','w',encoding='utf-8').write(h)
json.dump(caps,open('/tmp/w/caps345.json','w'),ensure_ascii=False)
print('nuevas',len(new),'sprites',sorted({e['s'] for e in new}),'reposts',st,'tallas cambiadas',zc,'marcadas agotado',na)
for kd in caps:
    for c in caps[kd]:print(c['fn']);print(c['cap']);print('--')
