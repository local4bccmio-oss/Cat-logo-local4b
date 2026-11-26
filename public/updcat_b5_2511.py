import re,json,os,sys,datetime as dt
exec(open('updcat_b3b4b5_2211.py').read().split("os.chdir")[0])
os.chdir('/home/claude/cat-logo-local4b/public')
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
SC='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
smax=max(d['s'] for d in D);S=[smax,sum(1 for d in D if d['s']==smax)]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
N=json.load(open('/tmp/w/fym_new.json'))
INFO={'4886':('AF1 1.1 Kids','Nike','blanco',list(range(28,36))),'4887':('AF1 1.1 Kids','Nike','negro',list(range(28,36))),
'3136':('Armani Exchange','Otras','negro y blanco',[40,41]),'6792':('Carolina Herrera','Otras','negro y rojo',[40,41]),
'3080':('Nike Comfort','Nike','blanco y gris',[36]),'6856':('Nike Gusano','Nike','dorado y crema',[37]),
'3096':('Bape Bathing','Otras','negro, azul y rojo',[40]),'3138':('Adidas Lightblaze','Adidas','rojo y negro',[40]),
'2995':('Lacoste Spin','Otras','negro',[40]),'3100':('Nike Streakfly','Nike','blanco y negro',[40,41]),
'3094':('Bape Bathing','Otras','negro, camuflado y rojo',[40]),'2026':('Armani Exchange','Otras','blanco, rojo y negro',[40]),
'6799':('Carolina Herrera','Otras','mostaza, morado y azul oscuro',[40,41]),'2935':('Nike Pegasus 41','Nike','celeste y verde',[36])}
os.makedirs(SC+'fymm',exist_ok=True);caps=[];new=[]
for p in N:
    ref=p['ref'];name,mar,col,z=INFO[ref];L='D' if max(z)<=39 else 'H';code='5'+ref
    lista=int(p['precio'].replace('.',''))//1000;P=lista-10+(20 if lista-10<=65 else 15)
    f='%s-%s.jpg'%(code,L);assert f not in byf
    t=tstr(z);src='/tmp/w/fym/'+p['img'];lab='%s/%s'%(f[:-4],t.lower())
    fn='%02d_%s'%(len(caps)+1,f)
    make(src,lab,SC+'fymm/'+fn,1080,1350,0)
    sn,si=slot();e=dict(f=f,b='B5',n=name,r=[code],t=t,c=col,z=z,g=L,m=mar,s=sn,i=si,u=u,d='25/11')
    if p['caja']:e['x']=1
    make(src,lab,'p/'+f,640,800,0);new.append(e);byf[f]=e
    cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~'%(name,code,P,t,col)
    if p['promo']:cap+='\n❌ _No cambio, no garantía_'
    caps.append(dict(f=f,fn=fn,cap=cap))
D+=new
TW,TH=420,525
for sn in sorted({e['s'] for e in new}):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for d in D:
        if d['s']==sn:
            im=Image.open('p/'+d['f']).convert('RGB');im.thumbnail((TW,TH),Image.LANCZOS);i=d['i'];sh.paste(im,((i%4)*TW+(TW-im.width)//2,(i//4)*TH+(TH-im.height)//2))
    sh.save('s/%03d.jpg'%sn,quality=66,optimize=True)
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):];open('index.html','w',encoding='utf-8').write(h)
json.dump(caps,open('/tmp/w/caps_b5_2511.json','w'),ensure_ascii=False)
print('nuevas',len(new))
for c in caps:print(c['fn'],'|',c['cap'].replace('\n',' / '))
