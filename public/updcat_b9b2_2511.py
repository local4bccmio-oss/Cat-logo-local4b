import re,json,os,sys,datetime as dt
from PIL import Image,ImageDraw,ImageFont,ImageFilter
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
def tstr(z):
    return '36EUR al 39EUR' if z[0]<40 else '40EUR al 44EUR'
os.chdir('/home/claude/cat-logo-local4b/public')
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
SC='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
OUT=SC+'n25b';os.makedirs(OUT,exist_ok=True)
smax=max(d['s'] for d in D);S=[smax,sum(1 for d in D if d['s']==smax)]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
N9={'184':('Le Coq','negro rojo'),'844':('Nike Zoom','azul petróleo verde neón'),'607':('Hugo Boss','café'),'608':('Hugo Boss','blanco café crema'),'886':('Vans','negro gris'),'888':('Vans','negro blanco'),'887':('Vans','negro blanco azul claro'),'1064':('Adidas Response 2','azul marino blanco'),'573':('Adidas','negro gris'),'1093':('Adidas','blanco crema negro'),'906':('New Balance 9060','crema beige'),'611':('New Balance 9060','gris blanco'),'1075':('Adidas Supernova','gris claro crema'),'173':('Adidas Samba','blanco negro gris'),'1097':('On Cloud','gris negro'),'1068':('Nike Presto','gris oscuro negro'),'1110':('Nike V2K','blanco gris'),'1112':('Adidas Superstar','blanco negro'),'1113':('Adidas Superstar','blanco negro'),'981':('Adidas','blanco azul'),'910':('Adidas','negro blanco'),'1030':('Adidas','negro blanco')}
N2={'1132':('Nike','plata blanco crema'),'1138':('Nike Metcon','gris negro'),'983':('Adidas','blanco lila'),'553':('Adidas','negro blanco'),'804':('Le Coq','negro'),'1103':('Le Coq','negro'),'1104':('Le Coq','negro rojo'),'708':('Le Coq','negro rojo'),'786':('Le Coq','negro'),'607':('Vans','blanco'),'805':('Vans','blanco café rojo'),'1022':('Nike Metcon','azul claro azul'),'307':('Adidas Samba','blanco negro'),'393':('Adidas Campus','negro blanco'),'925':('Adidas Campus','negro blanco'),'1221':('Adidas Campus','gris blanco'),'1222':('Adidas Campus','negro blanco'),'1220':('Adidas Campus','negro blanco')}
new=[];caps=[];lastd={}
def price(L):return L+10 if L-10<=65 else L+5
def process(bod,pre,f,c,g,L,date,src,mark,table,send):
    fn='%s%s-%s.jpg'%(mark,c,g);z=[36,37,38,39] if g=='D' else [40,41,42,43,44];t=tstr(z);P=price(L)
    if fn in byf:
        d=byf[fn];d['d']=date if date>d.get('d','00/00')[::-1] or True else d['d'];n,col=d['n'],d['c']
        d['d']=date;d.pop('a',None);d.pop('h',None);isnew=False
    else:
        n,col=table[c];sn,si=slot();d=dict(f=fn,b=bod,n=n,r=[pre+c],t=t,c=col,z=z,g=g,m=n.split()[0] if n.split()[0]!='New' else 'New Balance',s=sn,i=si,u=u,d=date)
        if n.startswith('Le Coq'):d['m']='Le Coq Sportif'
        make(src,'%s%s-%s/%s'%(mark,c,g,t.lower()),'p/'+fn,640,800);new.append(d);byf[fn]=d;isnew=True
    if send:
        k=len(caps)+1;make(src,'%s%s-%s/%s'%(mark,c,g,t.lower()),OUT+'/%02d_%s'%(k,fn),1080,1350)
        caps.append(dict(f=fn,fn='%02d_%s'%(k,fn),cap='*%s* Ref _%s%s_\n*$%d.000*\n*%s*\n~%s~'%(n,pre,c,P,t,col),new=isnew,bod=bod))
    return isnew
# ---------- B9
R=json.load(open('/tmp/w/b9_rows.json'));last={}
for r in R:last[r['file']]=r  # última aparición
sent=set();st=dict(n9=0,r9=0)
for r in R:
    if r['d']=='24/11':continue
for fn,r in last.items():
    send=(r['d']=='24/11');isnew=process('B9','9',r['f'],r['c'],r['g'],r['L'],r['d'],'/tmp/w/b9/'+r['f'],'A9',N9,False)
# reconstruir envío: solo fotos del 24/11, sin repetidas
caps.clear();seen=set()
for r in R:
    if r['d']!='24/11' or r['file'] in seen:continue
    seen.add(r['file']);fn=r['file'];d=byf[fn];c=r['c'];g=r['g'];z=d['z'];t=d['t'];P=price(r['L']);k=len(caps)+1
    make('/tmp/w/b9/'+r['f'],'A9%s-%s/%s'%(c,g,t.lower()),OUT+'/%02d_%s'%(k,fn),1080,1350)
    caps.append(dict(f=fn,fn='%02d_%s'%(k,fn),cap='*%s* Ref _9%s_\n*$%d.000*\n*%s*\n~%s~'%(d['n'],c,P,t,d['c']),bod='B9'))
n9=len(new)
# ---------- B2
from_b2=[]
import sys
sys.path.insert(0,'/tmp/w')
from parse import ents
for e in ents('/tmp/w/b2'):
    f=re.search(r'(IMG-\S+?\.jpg)',e['x'])
    if not f:continue
    cap=e['x'].split('\n',1)[1]
    m=re.search(r'COD\s*(\d+)\s*(.*?)\s*(DAMA|HOMBRE)',cap.replace('\n',' '))
    pr=re.search(r'💲([\d.]+)',cap)
    from_b2.append(dict(f=f[1],c=m[1],g='D' if m[3]=='DAMA' else 'H',L=int(pr[1].replace('.',''))//1000,d=e['d'][:5]))
for r in from_b2:
    fn='M2%s-%s.jpg'%(r['c'],r['g']);process('B2','2',r['f'],r['c'],r['g'],r['L'],r['d'],'/tmp/w/b2/'+r['f'],'M2',N2,True)
n2=len(new)-n9
# ---------- agotado B2/B9 (d <= 22/11)
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
json.dump(caps,open('/tmp/w/caps_25b.json','w'),ensure_ascii=False)
print('nuevas B9',n9,'B2',n2,'agotado',na,'envío',len(caps))
for c in caps:print(c['fn'],'|',c['cap'].replace('\n',' / '))
