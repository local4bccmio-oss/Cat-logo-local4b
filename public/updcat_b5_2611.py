import re,json,os,sys
exec(open('updcat_b3b4b5_2211.py').read().split("os.chdir")[0])
os.chdir('/home/claude/cat-logo-local4b/public')
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
SC='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
smax=max(d['s'] for d in D);S=[smax,sum(1 for d in D if d['s']==smax)]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
N=json.load(open('/tmp/w/b5_split.json'))['new']
INFO={'4282':('Jordan Sixty','Jordan','negro'),'4200':('Jordan Retro 4 RM','Jordan','negro, gris y crema'),'4201':('Jordan Retro 4 RM','Jordan','negro, gris y rojo'),
'4033':('Jordan Luka 5','Jordan','café y rosado'),'4032':('Jordan Luka 5','Jordan','negro y amarillo'),'4286':('Adidas Campus Brillos','Adidas Campus','negro y brillos'),
'4287':('Adidas Campus Brillos','Adidas Campus','negro y blanco'),'3146':('Adidas Campus','Adidas Campus','negro y blanco'),'4543':('Adidas Campus','Adidas Campus','verde menta y beige'),
'4646':('Coach','Coach','café y beige'),'4647':('Coach','Coach','negro y beige'),'4648':('Coach','Coach','negro y gris'),'4304':('Coach','Coach','blanco y plateado'),'4306':('Coach','Coach','negro y gris'),
'4326':('Puma Indoor','Puma','blanco y negro'),'4328':('Puma Indoor','Puma','blanco y lila'),'4329':('Puma Indoor','Puma','blanco y gris'),
'4339':('Lacoste Sport','Lacoste','negro y blanco'),'4341':('Lacoste Sport','Lacoste','negro'),'4016':('Lacoste Spinor','Lacoste','blanco'),'4150':('Lacoste Spinor','Lacoste','gris'),'4151':('Lacoste Spinor','Lacoste','blanco'),'4152':('Lacoste Spinor','Lacoste','beige'),
'4342':('Vans Bold','Vans','blanco y negro'),'4343':('Vans Bold','Vans','blanco y azul claro'),'4403':('Puma Park','Puma','rosado'),
'357':('Adidas Spezial','Adidas','café y beige'),'4629':('Adidas Spezial','Adidas','azul oscuro y rosado'),'4628':('Adidas Spezial','Adidas','vinotinto y blanco'),'4565':('Adidas Spezial','Adidas','gris y negro'),'4563':('Adidas Spezial','Adidas','rosado palo y blanco'),
'4422':('Le Coq Sportif','Le Coq Sportif','negro y dorado'),'4423':('Le Coq Sportif','Le Coq Sportif','blanco y café'),'4424':('Le Coq Sportif','Le Coq Sportif','blanco y rojo'),'4425':('Le Coq Sportif','Le Coq Sportif','café y verde'),'4426':('Le Coq Sportif','Le Coq Sportif','negro'),'4427':('Le Coq Sportif','Le Coq Sportif','negro y blanco'),'4428':('Le Coq Sportif','Le Coq Sportif','negro y coral'),
'4436':('Nike SB Pro ISO','Nike','café y blanco'),'4438':('Nike SB The North Face','Nike','negro, blanco y gris'),'4440':('Nike SB','Nike','blanco y gris'),'4441':('Nike SB','Nike','blanco y negro'),'4442':('Nike SB','Nike','gris y blanco'),
'4468':('AF1 Foamposite','Nike','naranja'),'4472':('AF1 Foamposite','Nike','plateado y negro')}
def psz(s):
    s=s.replace('43144','43-44').replace('Euro','').strip();z=[]
    for tk in s.split('-'):
        m=re.match(r'\s*(\d+)\s*al\s*(\d+)',tk)
        if m:z+=list(range(int(m[1]),int(m[2])+1))
        else:z.append(int(tk))
    return sorted(set(z))
os.makedirs(SC+'b5m',exist_ok=True);caps=[];cajas=[];new=[]
for r in N:
    refs5=r['refs'];name,mar,col=INFO[refs5[0]];z=psz(r['tl'].split('\n')[0].split('👱')[0]);lista=r['p'];cost=lista-10;P=cost+(20 if cost<=65 else 15)
    if len(refs5)==2:
        g='DH';f='5%s-D_%s-H.jpg'%tuple(refs5);refs=['5'+x for x in refs5]
        zD=[n for n in z if n<=39];zH=[n for n in z if n>=40];t=' / '.join(x for x in(tstr(zD),tstr(zH)) if x)
        lab='5%s-D/%s  %s-H/%s'%(refs5[0],tstr(zD).lower(),refs5[1],tstr(zH).lower());refl='%s / %s'%tuple(refs)
    else:
        g='D' if max(z)<=39 else 'H';code='5'+refs5[0];f='%s-%s.jpg'%(code,g);refs=[code];t=tstr(z);lab='%s-%s/%s'%(code,g,t.lower());refl=code
    assert f not in byf,f
    src='/tmp/w/y2/'+r['f'];fn='%02d_%s'%(len(caps)+1,f)
    make(src,lab,SC+'b5m/'+fn,1080,1350,0)
    sn,si=slot();e=dict(f=f,b='B5',n=name,r=refs,t=t,c=col,z=z,g=g,m=mar,s=sn,i=si,u=u,d='26/11')
    if r['cj']:e['x']=1
    make(src,lab,'p/'+f,640,800,0);new.append(e);byf[f]=e
    cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~'%(name,refl,P,t,col)
    if r['cj']:cap+='\n📦 _$%d.000 por caja_'%r['cj']
    if r['promo']:cap+='\n❌ _No cambio, no garantía_'
    caps.append(dict(f=f,fn=fn,cap=cap,cj=r['cj'],g=g,n=len(refs)))
# reposts: update date
for rr in json.load(open('/tmp/w/b5_split.json'))['rep']:
    for fx in rr['ex']:
        if fx in byf and byf[fx].get('d')!='26/11':byf[fx]['d']='26/11';byf[fx]['a']=0 if 'a' in byf[fx] else byf[fx].get('a',0);byf[fx].pop('a',None)
D+=new
TW,TH=420,525
for sn in sorted({e['s'] for e in new}):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for d in D:
        if d['s']==sn:
            im=Image.open('p/'+d['f']).convert('RGB');im.thumbnail((TW,TH),Image.LANCZOS);i=d['i'];sh.paste(im,((i%4)*TW+(TW-im.width)//2,(i//4)*TH+(TH-im.height)//2))
    sh.save('s/%03d.jpg'%sn,quality=66,optimize=True)
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):];open('index.html','w',encoding='utf-8').write(h)
json.dump(caps,open('/tmp/w/caps_b5_2611.json','w'),ensure_ascii=False)
print('nuevas',len(new),'cajas',sum(1 for c in caps if c['cj']))
for c in caps:print(c['fn'],'|',c['cap'].replace('\n',' / '))
