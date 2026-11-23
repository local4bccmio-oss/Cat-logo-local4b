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
new=[];caps={'b0':[],'b1':[]}
def addnew(f,b,n,r,t,c,z,g,m,src,lab,cap,crop=0,cover=None,x=0):
    sn,si=slot();e=dict(f=f,b=b,n=n,r=r,t=t,c=c,z=z,g=g,m=m,s=sn,i=si,u=u,d='22/11')
    if x:e['x']=1
    im=Image.open(src).convert('RGB')
    if cover:
        W,H=im.size;ImageDraw.Draw(im).rectangle((int(cover[0]*W),int(cover[1]*H),int(cover[2]*W),int(cover[3]*H)),fill='white')
    tmp='/tmp/w/_t.jpg';im.save(tmp,quality=95)
    make(tmp,lab,'p/'+f,640,800,crop);k='b0' if b=='B0' else 'b1';os.makedirs(SC+k,exist_ok=True)
    make(tmp,lab,SC+k+'/%02d_%s'%(len(caps[k])+1,f),1080,1350,crop)
    caps[k].append(dict(f=f,fn='%02d_%s'%(len(caps[k])+1,f),cap=cap));new.append(e);byf[f]=e
# ---------- B0
B0=json.load(open('/tmp/w/b0_items.json'));zc=0;rb0=0
for it in B0:
    if it['ex']:
        d=byf[it['ex'][0][0]];d['d']='22/11';d.pop('a',None);d.pop('h',None);rb0+=1
        z=it['z']
        if d['g']=='D' and not it['hom']:zz=z
        elif d['g']=='H' and not it['dam']:zz=z
        else:zz=None
        if zz and zz!=d['z']:d['z']=zz;d['t']=tstr(zz);zc+=1
        elif zz is None and it['z'] and d['f'].endswith('-DH.jpg') and it['z']!=d['z']:d['z']=it['z'];d['t']=tstr(it['z']);zc+=1
    else:
        t=tstr(it['z']);f='%s-H.jpg'%it['ref'];P=it['p']+5
        addnew(f,'B0','Under Armour Bota',[it['ref']],t,'negro',it['z'],'H','Under Armour','/tmp/z_b0/'+it['f'],'%s-H/%s'%(it['ref'],t.lower()),
               '*Under Armour Bota* Ref _%s_\n*$%d.000*\n*%s*\n~negro~'%(it['ref'],P,t),cover=(0.77,0.0,1.0,0.065))
# ---------- B1 informativo
B1=json.load(open('/tmp/w/b1i_items.json'))
NEW1={('4402','H'):('Jordan Retro 1 Off White','blanco','Jordan'),('4293','D'):('Adidas Superstar','negro plata','Adidas'),('3938','H'):('New Balance 9060','gris','New Balance')}
rb1=0;seen=set();newb1=[]
for it in B1:
    ref=it['ref']
    if not ref:
        mm2=re.search(r'REF\.?\s*(\d+)\s*([DH])',it['raw']);ref=mm2[1];it['g']=mm2[2]
    key=(ref,it['g'])
    if key in NEW1:
        if key not in [k for k,_ in newb1]:newb1.append((key,it))
        continue
    code='1'+ref
    fs=[f for f in byf if byf[f]['b']=='B1' and re.fullmatch(re.escape(code)+r'-[A-Z]+\.jpg',f) and (not it['g'] or f.endswith('-'+it['g']+'.jpg') or it['g'] not in 'DH')]
    if not fs:fs=[f for f in byf if byf[f]['b']=='B1' and re.fullmatch(re.escape(code)+r'-[A-Z]+\.jpg',f)]
    if ref=='1616':fs=['11616-D.jpg']
    assert fs,(ref,it['g'])
    for f in fs:
        if f in seen:continue
        seen.add(f);d=byf[f];d['d']='22/11';d.pop('a',None);d.pop('h',None)
        if it['c']:d['x']=1
        else:d.pop('x',None)
        rb1+=1
for (ref,g),it in newb1:
    n,c,m=NEW1[(ref,g)];L=it['p'];cb=it['c'];code='1'+ref;z=[36,37,38,39] if g=='D' else [40,41,42,43,44];t=tstr(z);par=L+(20 if L<=65 else 15)
    cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~'%(n,code,par,t,c)
    if cb:cap+='\n📦 _$%d.000 por caja_'%(cb+5)
    addnew('%s-%s.jpg'%(code,g),'B1',n,[code],t,c,z,g,m,'/tmp/z_b1i/'+it['f'],'%s-%s/%s'%(code,g,t.lower()),cap,x=1 if cb else 0)
    caps['b1'][-1].update(caja=(cb+5) if cb else None,L=L,g=g)
# banderas
AG=dt.date(2026,11,14);na=0
for d in D+new:
    if d['b']=='B0' and d.get('d') and not d.get('a'):
        q=dt.date(2026,int(d['d'][3:5]),int(d['d'][:2]))
        if q<=AG or (d['d'] in('18/11','19/11','20/11','21/11','22/11') and len(d['z'])<=3):d['a']=1;na+=1
D+=new
TW,TH=420,525
for sn in sorted({e['s'] for e in new}):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for d in D:
        if d['s']==sn:
            im=Image.open('p/'+d['f']).convert('RGB');im.thumbnail((TW,TH),Image.LANCZOS);i=d['i'];sh.paste(im,((i%4)*TW+(TW-im.width)//2,(i//4)*TH+(TH-im.height)//2))
    sh.save('s/%03d.jpg'%sn,quality=66,optimize=True)
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):];open('index.html','w',encoding='utf-8').write(h)
json.dump(caps,open('/tmp/w/caps_b0b1.json','w'),ensure_ascii=False)
print('B0 reposts',rb0,'tallas',zc,'B1 reposts',rb1,'nuevas',[e['f'] for e in new],'sprites',sorted({e['s'] for e in new}),'agotado b0',na)
for k in caps:
    for c in caps[k]:print(c['fn']);print(c['cap'])
