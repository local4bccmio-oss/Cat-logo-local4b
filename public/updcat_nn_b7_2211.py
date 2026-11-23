import re,json,os,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import onnxruntime as ort
FT='/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf'
def make(src,label,out,W,H):
    im=Image.open(src).convert('RGB')
    bg=im.copy();s=max(W/bg.width,H/bg.height);bg=bg.resize((int(bg.width*s)+1,int(bg.height*s)+1),Image.LANCZOS)
    bg=bg.crop(((bg.width-W)//2,(bg.height-H)//2,(bg.width-W)//2+W,(bg.height-H)//2+H)).filter(ImageFilter.GaussianBlur(W*0.037))
    s=min(W/im.width,H/im.height);fg=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=(W-fg.width)//2;y=(H-fg.height)//2;bg.paste(fg,(x,y))
    d=ImageDraw.Draw(bg);f=ImageFont.truetype(FT,round(W*0.036));tw=d.textlength(label,font=f);pad=round(W*0.022);bh=round(f.size*1.5)
    x0,y0=x+14*W//1080,y+14*W//1080;d.rounded_rectangle((x0,y0,x0+tw+2*pad,y0+bh),radius=round(bh*.3),fill='white')
    d.text((x0+pad,y0+bh/2),label,font=f,fill='black',anchor='lm');bg.save(out,quality=90);return bg
os.chdir('/home/claude/cat-logo-local4b/public')
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
SC='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
sess=ort.InferenceSession('/tmp/mc2.onnx',providers=['CPUExecutionProvider'])
def emb(im):
    W,H=im.size;c=im.crop((int(.1*W),int(.3*H),int(.9*W),int(.92*H)));w,h2=c.size;m=max(w,h2)
    sq=Image.new('RGB',(m,m),'white');sq.paste(c,((m-w)//2,(m-h2)//2));sq=sq.resize((256,256),Image.BICUBIC)
    e=sess.run(None,{'x':(np.asarray(sq,np.float32)/255).transpose(2,0,1)[None]})[0][0];return e/np.linalg.norm(e)
z=np.load('../tools/cache.npz',allow_pickle=True);cf=[str(x) for x in z['f']];E=np.array(z['E'],np.float32)
# siguiente hueco de sprite
smax=max(d['s'] for d in D);cnt=sum(1 for d in D if d['s']==smax);S=[smax,cnt]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
touched=set();new=[];caps={'nn':[],'b7':[]}
def addcap(kind,idx,f,cap):
    caps[kind].append(dict(f=f,fn='%02d_%s'%(idx,f),cap=cap))
# ---------- NN
t=open('/tmp/z_nn/'+[x for x in os.listdir('/tmp/z_nn') if x.endswith('.txt')][0],encoding='utf8').read().replace(' ',' ').split('\n')
rows=[]
for i,l in enumerate(t):
    if l.startswith('22/11/2026') and 'archivo adjunto' in l:
        f=re.search(r'(IMG-\S+?\.jpg)',l)[1];j=i+1;txt=''
        while j<len(t) and not re.match(r'\d+/\d+/\d{4}, ',t[j]):txt+=' '+t[j];j+=1
        rows.append((f,txt.strip()))
NEWC={3:'negro suela roja',14:'gris claro blanco',15:'crema blanco',23:'negro suela roja'}
os.makedirs(SC+'nn',exist_ok=True);os.makedirs(SC+'b7',exist_ok=True)
for n,(f,txt) in enumerate(rows,1):
    src='/tmp/z_nn/'+f
    m=re.search(r'\*([A-ZÁÉÍÓÚ ]+?)\s*(DAMA Y HOMBRE|HOMBRE Y DAMA|DAMA|HOMBRE)\*?',txt.replace('*  ','* ')) or re.search(r'([A-Z ]+?)\s+(DAMA Y HOMBRE|HOMBRE Y DAMA|DAMA|HOMBRE)',txt)
    nombre=m[1].strip().title();gt=m[2];g='DH' if ' Y ' in gt else ('D' if gt=='DAMA' else 'H')
    tl=[int(x) for x in re.search(r'TALLAS ([\d ]+?)\*',txt)[1].split()];price=int(re.search(r'\$(\d+)\.000',txt)[1])+10
    tula='INCLUYE TULA' in txt
    t_='36EUR al 39EUR' if g=='D' else ('40EUR al 44EUR' if g=='H' else '36EUR al 44EUR')
    if tl==[36,37,38]:t_='36EUR al 38EUR'
    code='Fr01-'+g;lab='%s/%s'%(code,t_.lower())
    e=emb(Image.open(src).convert('RGB'));sim=E@e;bi=int(np.argmax(sim));mf=cf[bi]
    if n in NEWC or sim[bi]<0.915 and n not in(2,4):
        ff='22nov_%02d_%s.jpg'%(n,code);col=NEWC.get(n,'por confirmar')
        sn,si=slot();d=dict(f=ff,b='NN',n=nombre,r=[code],t=t_,c=col,z=tl,g=g,m=nombre.split()[0],d='22/11',s=sn,i=si,u=u)
        make(src,lab,'p/'+ff,640,800);new.append(d);touched.add(sn);fnm=ff
    elif n==4:
        ff='22nov_%02d_%s.jpg'%(n,code);col=byf[mf]['c']
        sn,si=slot();d=dict(f=ff,b='NN',n=nombre,r=[code],t=t_,c=col,z=tl,g=g,m=nombre.split()[0],d='22/11',s=sn,i=si,u=u)
        make(src,lab,'p/'+ff,640,800);new.append(d);touched.add(sn);fnm=ff
    else:
        d=byf[mf];d['d']='22/11';d.pop('a',None);d.pop('h',None);col=d['c'];fnm=mf
        print(n,'repost',mf,'%.3f'%sim[bi])
    out=SC+'nn/%02d_%s'%(n,fnm);make(src,lab,out,1080,1350)
    cap='*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~%s'%(nombre,code,price,t_,col,'\n🎒 _incluye tula_' if tula else '')
    addcap('nn',n,fnm,cap)
# ---------- B7
HV='/tmp/z_hv/'
B=[('71039-D.jpg','IMG-20261105-WA5339.jpg',None,100,'36EUR al 39EUR',[36,37,38,39],None),
('71041-D.jpg','IMG-20261105-WA5340.jpg',None,95,'36EUR al 38EUR',[36,37,38],None),
('71040-D.jpg','IMG-20261105-WA5341.jpg',None,100,'36EUR al 39EUR',[36,37,38,39],None),
('71042-H.jpg','IMG-20261105-WA5342.jpg',None,100,'40EUR-41EUR-43EUR al 45EUR',[40,41,43,44,45],None),
('71055-D.jpg','IMG-20261122-WA1055.jpg','Nike Internacional',100,'36EUR al 39EUR',[36,37,38,39],'rosado blanco'),
('71057-D.jpg','IMG-20261122-WA1057.jpg','Nike Internacional',100,'36EUR al 39EUR',[36,37,38,39],'negro'),
('71059-D.jpg','IMG-20261122-WA1059.jpg','Nike SB Dunk',90,'36EUR al 39EUR',[36,37,38,39],'crema vino'),
('71060-D.jpg','IMG-20261122-WA1060.jpg','Nike SB Dunk',90,'36EUR al 39EUR',[36,37,38,39],'azul claro')]
for k,(f,src,nombre,price,t_,z_,col) in enumerate(B,1):
    code=f[:5];lab=f[:-4]+'/'+t_.lower()
    if f in byf:
        d=byf[f];d['d']='22/11';d.pop('a',None);d.pop('h',None);d['t']=t_;d['z']=z_;nombre=d['n'];col=d['c']
    else:
        sn,si=slot();d=dict(f=f,b='B7',n=nombre,r=[code],t=t_,c=col,j='',z=z_,g=f[5],m='Nike',d='22/11',s=sn,i=si,u=u)
        make(HV+src,lab,'p/'+f,640,800);new.append(d);touched.add(sn)
    make(HV+src,lab,SC+'b7/%02d_%s'%(k,f),1080,1350)
    addcap('b7',k,f,'*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~'%(nombre,code,price,t_,col))
D+=new
byf={d['f']:d for d in D}
TW,TH=420,525
for sn in sorted(touched):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for d in D:
        if d['s']==sn:
            im=Image.open('p/'+d['f']).convert('RGB');im.thumbnail((TW,TH),Image.LANCZOS);i=d['i'];sh.paste(im,((i%4)*TW+(TW-im.width)//2,(i//4)*TH+(TH-im.height)//2))
    sh.save('s/%03d.jpg'%sn,quality=66,optimize=True)
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):];open('index.html','w',encoding='utf-8').write(h)
json.dump(caps,open('/tmp/nnb7_caps.json','w'),ensure_ascii=False)
print('nuevas',len(new),'sprites',sorted(touched))
for kd in caps:
    for c in caps[kd]:print(c['fn']);print(c['cap']);print('--')
