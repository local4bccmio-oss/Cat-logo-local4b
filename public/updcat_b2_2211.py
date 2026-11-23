import re,json,sys
from PIL import Image,ImageDraw,ImageFont,ImageFilter
sys.path.insert(0,'/tmp/fix')
FT='/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf'
def make(src,label,out,W,H,crop=0.125):
    im=Image.open(src).convert('RGB');im=im.crop((0,int(im.height*crop),im.width,im.height))
    bg=im.copy();s=max(W/bg.width,H/bg.height);bg=bg.resize((int(bg.width*s)+1,int(bg.height*s)+1),Image.LANCZOS)
    bg=bg.crop(((bg.width-W)//2,(bg.height-H)//2,(bg.width-W)//2+W,(bg.height-H)//2+H)).filter(ImageFilter.GaussianBlur(W*0.037))
    s=min(W/im.width,H/im.height);fg=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=(W-fg.width)//2;y=(H-fg.height)//2;bg.paste(fg,(x,y))
    d=ImageDraw.Draw(bg);f=ImageFont.truetype(FT,round(W*0.036));tw=d.textlength(label,font=f);pad=round(W*0.022);bh=round(f.size*1.5)
    x0,y0=x+14*W//1080,y+14*W//1080;d.rounded_rectangle((x0,y0,x0+tw+2*pad,y0+bh),radius=round(bh*.3),fill='white')
    d.text((x0+pad,y0+bh/2),label,font=f,fill='black',anchor='lm');bg.save(out,quality=90);return bg
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1])
S=json.load(open('/tmp/b2s.json'));byf={d['f']:d for d in D}
NEW={'1065':('Adidas','gris azul oscuro'),'388':('Adidas','negro gris'),'1200':('New Balance','gris beige'),'1213':('Nike','blanco'),'1197':('Adidas','negro'),'1214':('Adidas','crema negro'),'1175':('Nike','negro blanco')}
s0=max(d['s'] for d in D)+1;u=int(max(d.get('u',0) for d in D))+1;k=0
ims={};caps=[];new=[];out='/tmp/b2out';import os;os.makedirs(out,exist_ok=True)
for s in S:
    m=re.search(r'COD (\d+) (.*?)\s*(DAMA|HOMBRE).*?💲([\d.]+)',s['cap']);c=m[1];g='D' if m[3]=='DAMA' else 'H';L=int(m[4].replace('.',''))//1000
    if s['f']=='IMG-20261122-WA0450.jpg':c='1131'
    solo=False
    f='M2%s-%s.jpg'%(c,g);cost=L-10;P=L+10 if cost<=65 else L+5
    t='36EUR al 39EUR' if g=='D' else ('40EUR al 41EUR' if solo else '40EUR al 44EUR');z=[36,37,38,39] if g=='D' else ([40,41] if solo else [40,41,42,43,44])
    lab='M2%s-%s/%s'%(c,g,t.lower())
    if f in byf:
        d=byf[f];d['d']='22/11';d.pop('a',None);d.pop('h',None);n,col=d['n'],d['c']
    else:
        n,col=NEW[c];d=dict(f=f,b='B2',n=n,r=['2'+c],t=t,c=col,z=z,g=g,m='New Balance' if n.startswith('New') else n.split()[0],d='22/11',s=s0+k//12,i=k%12,u=u)
        make('/tmp/z_b2/'+s['f'],lab,'p/'+f,640,800);ims.setdefault(d['s'],{})[d['i']]=Image.open('p/'+f);new.append(d);k+=1
    make('/tmp/z_b2/'+s['f'],lab,'%s/%s'%(out,f),1080,1350)
    caps.append(dict(f=f,L=L,P=P,cap='*%s* Ref _2%s_\n*$%d.000*\n*%s*\n~%s~'%(n,c,P,t,col)))
TW,TH=420,525
for sn,mp in ims.items():
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for i,im in mp.items():
        t=im.copy();t.thumbnail((TW,TH),Image.LANCZOS);sh.paste(t,((i%4)*TW+(TW-t.width)//2,(i//4)*TH+(TH-t.height)//2))
    sh.save('s/%03d.jpg'%sn,quality=66,optimize=True)
D+=new
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):];open('index.html','w',encoding='utf-8').write(h)
json.dump(caps,open('/tmp/b2caps.json','w'),ensure_ascii=False)
print('nuevas',len(new),'sprites',s0,'u',u)
for c in caps:print(c['f'],c['L'],'->',c['P'])
