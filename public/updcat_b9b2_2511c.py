import re,json,os,datetime as dt
src=open('updcat_b9b2_2511.py').read()
exec(src.split("os.chdir")[0])  # make,tstr,imports
os.chdir('/home/claude/cat-logo-local4b/public')
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
SC='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/';OUT=SC+'n25c';os.makedirs(OUT,exist_ok=True)
smax=max(d['s'] for d in D);S=[smax,sum(1 for d in D if d['s']==smax)]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
def price(L):return L+10 if L-10<=65 else L+5
INFO={('B2','936'):('On Cloud','blanco y gris'),('B2','1226'):('Adidas','azul marino y azul'),('B2','1227'):('Adidas','negro y gris'),('B2','1033'):('Adidas','negro y gris oscuro'),('B2','618'):('Lacoste','negro'),('B2','1229'):('Adidas','fucsia, morado y blanco'),('B2','1223'):('Adidas','blanco y negro'),('B2','907'):('Jordan Retro 3','blanco, azul claro y rosado'),('B2','1228'):('On Cloud','blanco y rojo'),('B2','341'):('Vans','negro, gris y blanco'),('B2','1160'):('On Cloud','negro'),('B2','1225'):('Nike ZoomX','blanco y rojo'),
('B9','880'):('Adidas Campus','negro y crema'),('B9','270'):('Nike','plata, blanco y celeste'),('B9','370'):('Adidas','negro, blanco y gris'),('B9','883'):('On Cloud','negro, gris y blanco'),('B9','617'):('On Cloud','blanco y gris'),('B9','205'):('On Cloud','crema, vino y amarillo'),('B9','769'):('On Cloud','crema y rosado'),('B9','577'):('On Cloud','celeste y blanco'),('B9','917'):('On Cloud','blanco y crema')}
R=json.load(open('/tmp/w/rows2511b.json'));new=[];caps=[];nrep=0
for r in R:
    bod=r['bod'];pre='2' if bod=='B2' else '9';mark='M2' if bod=='B2' else 'A9';c=r['c'];g=r['g'];fn='%s%s-%s.jpg'%(mark,c,g)
    if fn in byf:
        d=byf[fn]
        if d.get('d')!='25/11':nrep+=1
        d['d']='25/11';d.pop('a',None);d.pop('h',None);continue
    n,col=INFO[(bod,c)];z=[36,37,38,39] if g=='D' else [40,41,42,43,44];t=tstr(z);P=price(r['L'])
    sn,si=slot();m=n.split()[0]
    d=dict(f=fn,b=bod,n=n,r=[pre+c],t=t,c=col,z=z,g=g,m='On Cloud' if m=='On' else m,s=sn,i=si,u=u,d='25/11')
    src_='/tmp/w/%s/%s'%(r['dir'],r['f']);lab='%s%s-%s/%s'%(mark,c,g,t.lower())
    make(src_,lab,'p/'+fn,640,800);new.append(d);byf[fn]=d
    k=len(caps)+1;make(src_,lab,OUT+'/%02d_%s'%(k,fn),1080,1350)
    caps.append(dict(f=fn,fn='%02d_%s'%(k,fn),cap='*%s* Ref _%s%s_\n*$%d.000*\n*%s*\n~%s~'%(n,pre,c,P,t,col),bod=bod))
AG=dt.date(2026,11,22);na=0
for d in D+new:
    if d['b'] in('B9','B2') and d.get('d') and not d.get('a'):
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
json.dump(caps,open('/tmp/w/caps_25c.json','w'),ensure_ascii=False)
print('nuevas',len(new),'reposts fecha',nrep,'agotado',na)
for c in caps:print(c['fn'],'|',c['cap'].replace('\n',' / '))
