import re,json,os,sys,datetime as dt
exec(open('updcat_b3b4b5_2211.py').read().split("os.chdir")[0])  # make,tstr
os.chdir('/home/claude/cat-logo-local4b/public')
src=open('/tmp/lcmk2.py').read()
N=eval(re.search(r'N=(\{.*?\})\nFP=',src,re.S)[1])
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
SC='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
smax=max(d['s'] for d in D);S=[smax,sum(1 for d in D if d['s']==smax)]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
def brand(n):
    for b in('Under Armour','Adidas','Nike','Puma','Vans','Reebok','Coach','Columbia','New Balance','Skechers','The North Face'):
        if b.lower() in n.lower():return b
    return 'Otras'
def zl(desc):
    d=desc.upper();z=set()
    for m in re.finditer(r'DEL\s+(\d+)\s+AL\s+(\d+)',d):z|=set(range(int(m[1]),int(m[2])+1))
    t=re.sub(r'DEL\s+\d+\s+AL\s+\d+',' ',d)
    for m in re.finditer(r'\b(\d{2})\b',t):z.add(int(m[1]))
    return sorted(x for x in z if 26<=x<=46)
os.makedirs('/tmp/w',exist_ok=True)
new=[];n23=0;added23=0
# --- 23/11: 67 publicadas
lc=json.load(open('/tmp/lc_items.json'))
for i,x in enumerate(lc):
    ref=x['rf'];L='DN' if 'NINO' in x['desc'].upper() else x['L'];f='%s-%s.jpg'%(ref,L)
    ex=[k for k in byf if byf[k]['b']=='B0' and byf[k]['r']==[ref]]
    if ex:
        for k in ex:byf[k]['d']='23/11';byf[k].pop('a',None);byf[k].pop('h',None)
        n23+=1;continue
    name,color=N[i];z=zl(x['desc']);t=tstr(z);sn,si=slot()
    g={'H':'H','D':'D','DH':'D','DN':'N','N':'N'}.get(L,L[0])
    e=dict(f=f,b='B0',n=name,r=[ref],t=t,c=color,z=z,g=g,m=brand(name),s=sn,i=si,u=u,d='23/11')
    im=Image.open('/tmp/lcout2/%s-%s.jpg'%(ref,x['L'] if L!='DN' else 'DN'))
    im.convert('RGB').resize((640,800),Image.LANCZOS).save('p/'+f,quality=80,optimize=True)
    new.append(e);byf[f]=e;added23+=1
# --- 24/11: 15 nuevas
INFO={'02715':('Columbia','gris, negro y blanco'),'02712':('New Balance','gris y naranja'),'02724':('The North Face','negro'),'02710':('Columbia','negro y blanco'),'00251':('New Balance 1000','blanco y negro'),'02720':('New Balance','negro y fucsia'),'02592':('Nike','gris y negro'),'02729':('Nike P-6000','blanco, gris y crema'),'02718':('Columbia','negro'),'02723':('Adidas','gris azulado y blanco'),'02716':('Skechers','negro y blanco'),'02727':('Skechers','blanco'),'00072':('New Balance 1000','negro'),'02725':('Nike','negro y blanco'),'02707':('Adidas','negro')}
rows=json.load(open('/tmp/w/b0_new_2411.json'));seen=set();caps=[];os.makedirs(SC+'b0n',exist_ok=True)
for r in rows:
    ref=r['ref']
    if ref in seen:continue
    seen.add(ref);raw=r['raw'].upper();name,col=INFO[ref]
    L='DH' if 'DAMA Y HOMBRE' in raw else ('D' if 'DAMA' in raw else 'H')
    z=[36,37,38,39,40] if L=='D' else ([40,41,42,43,44,45] if L=='H' else None)
    if L=='H' and ref=='02724':z=[40,41,42,43,44]
    if L=='DH':z=list(range(36,46)) if ref!='00072' else list(range(36,45))
    t=tstr(z);P=r['p']+5;f='%s-%s.jpg'%(ref,L)
    assert f not in byf,f
    sn,si=slot();e=dict(f=f,b='B0',n=name,r=[ref],t=t,c=col,z=z,g='D' if L=='DH' else L,m=brand(name),s=sn,i=si,u=u,d='24/11')
    im=Image.open('/tmp/z_lc24/'+r['f']).convert('RGB');W,H=im.size
    ImageDraw.Draw(im).rectangle((int(.73*W),0,W,int(.08*H)),fill=im.getpixel((int(.6*W),int(.03*H))))
    tmp='/tmp/w/_t.jpg';im.save(tmp,quality=95);lab='%s/%s'%(f[:-4],t.lower())
    make(tmp,lab,'p/'+f,640,800,0);make(tmp,lab,SC+'b0n/%02d_%s'%(len(caps)+1,f),1080,1350,0)
    caps.append(dict(f=f,fn='%02d_%s'%(len(caps)+1,f),cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~'%(name,ref,P,t.replace('-','EUR-') if False else t,col)));new.append(e);byf[f]=e
AG=dt.date(2026,11,14);na=0
for d in D+new:
    if d['b']=='B0' and d.get('d') and not d.get('a'):
        q=dt.date(2026,int(d['d'][3:5]),int(d['d'][:2]))
        if q<=AG or (d['d'] in('18/11','19/11','20/11','21/11','22/11','23/11','24/11') and len(d['z'])<=3):d['a']=1;na+=1
D+=new
TW,TH=420,525
for sn in sorted({e['s'] for e in new}):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for d in D:
        if d['s']==sn:
            im=Image.open('p/'+d['f']).convert('RGB');im.thumbnail((TW,TH),Image.LANCZOS);i=d['i'];sh.paste(im,((i%4)*TW+(TW-im.width)//2,(i//4)*TH+(TH-im.height)//2))
    sh.save('s/%03d.jpg'%sn,quality=66,optimize=True)
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):];open('index.html','w',encoding='utf-8').write(h)
json.dump(caps,open('/tmp/w/caps_b0_2411.json','w'),ensure_ascii=False)
print('23/11 actualizadas',n23,'agregadas',added23,'nuevas 24/11',len(caps),'agotado',na)
for c in caps:print(c['fn'],'|',c['cap'].replace('\n',' / '))
