import re,json,os
exec(open('updcat_b3b4b5_2211.py').read().split("os.chdir")[0])
os.chdir('/home/claude/cat-logo-local4b/public')
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
SC='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
smax=max(d['s'] for d in D);S=[smax,sum(1 for d in D if d['s']==smax)]
if S[1]>=12:S=[S[0]+1,0]
u=int(max(d.get('u',0) for d in D))+1
R=json.load(open('/tmp/w/b3_2611.json'));n=0
for r in R:
    for c in r['cod']:
        for d in D:
            if d['b']=='B3' and d['r']==['3'+c] and d.get('d')!='26/11':d['d']='26/11';d.pop('a',None);n+=1
f='31580-H.jpg';assert f not in byf
z=[40,41,42,43,44];t=tstr(z);lab='31580-H/'+t.lower()
os.makedirs(SC+'b3m',exist_ok=True)
make('/tmp/w/y1/IMG-20261126-WA5680.jpg',lab,SC+'b3m/01_'+f,1080,1350,0);make('/tmp/w/y1/IMG-20261126-WA5680.jpg',lab,'p/'+f,640,800,0)
e=dict(f=f,b='B3',n='Vans X Blends',r=['31580'],t=t,c='crema y azul claro',z=z,g='H',m='Vans',s=S[0],i=S[1],u=u,d='26/11',x=1);D.append(e)
TW,TH=420,525;sh=Image.new('RGB',(4*TW,3*TH),'white')
for d in D:
    if d['s']==S[0]:
        im=Image.open('p/'+d['f']).convert('RGB');im.thumbnail((TW,TH),Image.LANCZOS);i=d['i'];sh.paste(im,((i%4)*TW+(TW-im.width)//2,(i//4)*TH+(TH-im.height)//2))
sh.save('s/%03d.jpg'%S[0],quality=66,optimize=True)
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):];open('index.html','w',encoding='utf-8').write(h)
print('fechas',n)
