import re,json,os,datetime as dt
src=open('updcat_b9b2_2511.py').read()
exec(src.split("os.chdir")[0])
os.chdir('/home/claude/cat-logo-local4b/public')
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
OUT='/mnt/user-data/uploads/n26b';os.makedirs(OUT,exist_ok=True)
smax=max(d['s'] for d in D);S=[smax,sum(1 for d in D if d['s']==smax)]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
def price(L):return L+10 if L-10<=65 else L+5
def ts(z):
    if z==list(range(z[0],z[-1]+1)):return '%dEUR al %dEUR'%(z[0],z[-1])
    return ' '.join('%dEUR'%x for x in z)
INFO={('B2','1230'):('Adidas','fucsia, morado y blanco'),('B2','1185'):('On Cloud','gris y azul'),('B2','1186'):('On Cloud','gris'),('B2','1112'):('On Cloud','blanco'),('B2','1113'):('On Cloud','crema'),('B2','1114'):('On Cloud','blanco'),('B2','1066'):('Adidas','blanco y azul'),('B2','957'):('Adidas','negro'),('B2','1141'):('Adidas','blanco y morado'),('B2','1154'):('Adidas','negro y blanco'),('B2','960'):('Adidas','blanco y morado'),('B2','1111'):('Nike','azul marino y rosado'),('B2','1109'):('Nike','blanco, fucsia y menta'),
('B9','1142'):('On Cloud','gris y azul'),('B9','1143'):('On Cloud','gris'),('B9','1141'):('Adidas Campus','gris'),('B9','1144'):('Adidas Campus','negro y blanco'),('B9','708'):('Adidas','negro y blanco'),('B9','968'):('Adidas Samba','crema y rosado'),('B9','889'):('Vans','café y crema'),('B9','791'):('Nike TN','gris y verde neón')}
SZ={('B2','1113'):[40,41],('B2','1114'):[36,38,39],('B2','1066'):[42,43],('B2','957'):[40,41,42,43],('B2','1154'):[37,38,39],('B2','1111'):[36,38,39],('B9','1144'):list(range(36,45))}
R=json.load(open('/tmp/w/rows2611.json'));R.sort(key=lambda r:(r['bod']!='B9',));new=[];caps=[];nrep=0
for r in R:
    bod=r['bod'];pre='2' if bod=='B2' else '9';mark='M2' if bod=='B2' else 'A9';c=r['c'];g=r['g'];fn=r['fn'];P=price(r['L'])
    src_='/tmp/w/%s/%s'%(r['dir'],r['f'])
    if fn in byf:
        d=byf[fn]
        if d.get('d')!='26/11':nrep+=1
        d['d']='26/11';d.pop('a',None);d.pop('h',None);n,col,t=d['n'],d['c'],d['t']
    else:
        n,col=INFO[(bod,c)];z=SZ.get((bod,c)) or ([36,37,38,39] if g=='D' else [40,41,42,43,44]);t=ts(z)
        sn,si=slot();m=n.split()[0]
        d=dict(f=fn,b=bod,n=n,r=[pre+c],t=t,c=col,z=z,g=g,m='On Cloud' if m=='On' else m,s=sn,i=si,u=u,d='26/11')
        make(src_,'%s%s-%s/%s'%(mark,c,g,t.lower()),'p/'+fn,640,800);new.append(d);byf[fn]=d
    k=len(caps)+1;make(src_,'%s%s-%s/%s'%(mark,c,g,t.lower()),OUT+'/%02d_%s'%(k,fn),1080,1350)
    caps.append(dict(f=fn,fn='%02d_%s'%(k,fn),cap='*%s* Ref _%s%s_\n*$%d.000*\n*%s*\n~%s~'%(n,pre,c,P,t,col),bod=bod))
AG=dt.date(2026,11,23);na=0
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
json.dump(caps,open('/tmp/w/caps_26b.json','w'),ensure_ascii=False)
print('nuevas',len(new),'reposts fecha',nrep,'agotado',na,len(caps))
for c in caps:print(c['fn'],'|',c['cap'].replace('\n',' / '))
