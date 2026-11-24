import re,json,os,sys,datetime as dt
exec(open('updcat_b3b4b5_2211.py').read().split("os.chdir")[0])  # make, tstr, pub (defs only; os.chdir line excluded)
os.chdir('/home/claude/cat-logo-local4b/public')
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
SC='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
smax=max(d['s'] for d in D);S=[smax,sum(1 for d in D if d['s']==smax)]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
COL={'5390':'negro blanco azul','5907':'blanco negro','3890':'blanco','4391':'negro','5189':'rosado vino','5832':'blanco negro','4177':'rosado vino','5856':'verde claro','5658':'crema','5969':'azul claro','5559':'crema','3153':'negro blanco','6204':'negro lila','5905':'negro crema','5156':'gris claro','5161':'negro blanco','5162':'blanco','4468':'negro gris','6108':'negro gris'}
NM={'5390':'Nike SB Travis Scott','3890':'Nike Shox','4391':'Nike Shox','5189':'Nike Shox Ride 2','5907':'Nike Zoom 2','5832':'Nike Utempo','4177':'Nike V2K','5856':'Nike Vomero 18','5658':'Nike Vomero','5969':'Nike Vomero Plus','5559':'Nike Zoom','3153':'Nike Zoom','6204':'Nike Zoom Hyperset','5905':'Nike Zoom Speed S','5156':'On Cloud 5','5161':'On Cloud 5','5162':'On Cloud 5','4468':'On Cloud Monster','6108':'Osiris Peril'}
def brand(n):
    for b in('Osiris','On Cloud','Nike'):
        if b.lower() in n.lower():return 'On Cloud' if b=='On Cloud' else b
    return 'Otras'
B4=json.load(open('/tmp/w/b4_2411.json'));new=[];caps=[];seen=set();rep=0
os.makedirs(SC+'b4n',exist_ok=True)
for x in B4:
    if x['ex']:
        for f in x['ex']:
            if f in seen:continue
            seen.add(f);d=byf[f];d['d']='23/11';d.pop('a',None);d.pop('h',None)
            if x['caja']:d['x']=1
            else:d.pop('x',None)
            z=x['z']
            if z and len(d['r'])==1:
                zz=[n for n in z if n<=39] if d['g']=='D' else ([n for n in z if n>=40] if d['g']=='H' else z)
                if zz and zz!=d['z']:d['z']=zz;d['t']=tstr(zz)
            rep+=1
        continue
    ref=x['ref']
    if ref=='5859':continue
    z=x['z'];g='D' if max(z)<=39 else 'H';lista=x['price'];cost=lista if lista<=50 else lista-10;P=pub(cost)
    code='4'+ref;f='%s-%s.jpg'%(code,g);t=tstr(z);lab='%s-%s/%s'%(code,g,t.lower());n=NM[ref];col=COL[ref]
    assert f not in byf,f
    sn,si=slot();e=dict(f=f,b='B4',n=n,r=[code],t=t,c=col,z=z,g=g,m=brand(n),s=sn,i=si,u=u,d='23/11')
    if x['caja']:e['x']=1
    src='/tmp/z_mym24/'+x['f']
    make(src,lab,'p/'+f,640,800,0.125);make(src,lab,SC+'b4n/%02d_%s'%(len(caps)+1,f),1080,1350,0.125)
    cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~'%(n,code,P,t,col)
    if x['promo']:cap+='\n❌ _No cambio, no garantía_'
    caps.append(dict(f=f,fn='%02d_%s'%(len(caps)+1,f),cap=cap,P=P,lista=lista));new.append(e);byf[f]=e
AG=dt.date(2026,11,19);na=0
for d in D+new:
    if d['b'] in('B3','B4','B5') and d.get('d') and not d.get('a'):
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
json.dump(caps,open('/tmp/w/caps_b4_2411.json','w'),ensure_ascii=False)
print('nuevas',len(new),'reposts',rep,'agotado',na)
for c in caps:print(c['fn'],'|',c['cap'].replace('\n',' / '))
