import re,json,os
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
FT='/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf'
def trim(im,th=14):
    g=im.convert('L').point(lambda v:255 if v>th else 0);b=g.getbbox()
    if b and (b[2]-b[0])>im.width*0.3 and (b[3]-b[1])>im.height*0.3 and (b!=(0,0,im.width,im.height)):return im.crop(b)
    return im
def make(src,label,out,W,H,tr=False):
    im=Image.open(src).convert('RGB')
    if tr:im=trim(im)
    bg=im.copy();s=max(W/bg.width,H/bg.height);bg=bg.resize((int(bg.width*s)+1,int(bg.height*s)+1),Image.LANCZOS)
    bg=bg.crop(((bg.width-W)//2,(bg.height-H)//2,(bg.width-W)//2+W,(bg.height-H)//2+H)).filter(ImageFilter.GaussianBlur(W*0.037))
    s=min(W/im.width,H/im.height);fg=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=(W-fg.width)//2;y=(H-fg.height)//2;bg.paste(fg,(x,y))
    d=ImageDraw.Draw(bg);f=ImageFont.truetype(FT,round(W*0.036));tw=d.textlength(label,font=f);pad=round(W*0.022);bh=round(f.size*1.5)
    x0,y0=x+14*W//1080,y+14*W//1080;d.rounded_rectangle((x0,y0,x0+tw+2*pad,y0+bh),radius=round(bh*.3),fill='white')
    d.text((x0+pad,y0+bh/2),label,font=f,fill='black',anchor='lm');bg.save(out,quality=90);return bg
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
SC='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
s0=max(d['s'] for d in D)+1;u=int(max(d.get('u',0) for d in D))+1;k=0;ims={};new=[]
def ent(f,src,n,r,t,c,z,g,m,tr,lab,price,extra=''):
    global k
    if f in byf:
        d=byf[f];d['d']='22/11';d.pop('a',None);d.pop('h',None)
    else:
        d=dict(f=f,b=r[0][:2].upper() if False else ('AR' if f.startswith('Arg') else 'JH'),n=n,r=r,t=t,c=c,z=z,g=g,m=m,d='22/11',s=s0+k//12,i=k%12,u=u)
        make(src,lab,'p/'+f,640,800,tr);ims.setdefault(d['s'],{})[d['i']]=Image.open('p/'+f);new.append(d);k+=1
    return d
caps={'arg':[],'joh':[]}
def add(kind,idx,f,src,n,ref,t,c,z,g,m,lab,price,tr=False,extra='',old=None):
    ent(f,src,n,[ref],t,c,z,g,m,tr,lab,price)
    out=SC+kind+'/';os.makedirs(out,exist_ok=True)
    fn='%02d_%s'%(idx,f);make(src,lab,out+fn,1080,1350,tr)
    cap='%s*%s* Ref _%s_\n*$%d.000*\n*%s*\n~%s~%s'%(extra[0],n,ref,price,t,c,extra[1])
    caps[kind].append(dict(f=f,fn=fn,cap=cap))
A='/tmp/z_sa/';J='/tmp/z_jo/'
T39='36EUR al 39EUR'
add('arg',1,'Arg89-D.jpg',A+'IMG-20261121-WA3792.jpg','Sandalia Coach','Arg89',T39,'café',[36,37,38,39],'D','Coach','Arg89-D/36eur al 39eur',55,extra=('',''))
add('arg',2,'Arg90-D.jpg',A+'IMG-20261121-WA3793.jpg','Sandalia Coach','Arg90',T39,'gris',[36,37,38,39],'D','Coach','Arg90-D/36eur al 39eur',55,extra=('',''))
add('arg',3,'Arg91-D.jpg',A+'IMG-20261121-WA3794.jpg','Sandalia Chanel','Arg91',T39,'café',[36,37,38,39],'D','Chanel','Arg91-D/36eur al 39eur',55,extra=('',''))
add('arg',4,'Arg38-D.jpg',A+'IMG-20261002-WA0806.jpg','Sandalia Dior','Arg38',T39,'blanco crema',[36,37,38,39],'D','Dior','Arg38-D/36eur al 39eur',90,extra=('',''))
add('arg',5,'Arg37-DH.jpg',A+'IMG-20261121-WA3795.jpg','Nike Ozuna','Arg37','36EUR al 40EUR','negro',[36,37,38,39,40],'D','Nike','Arg37-D/36eur al 40eur',55,extra=('',''))
TU='\n🎒 _Incluye tula_'
D39='36EUR al 39EUR';H44='40EUR al 44EUR'
rows=[
('Joh-H_05_hugo-boss.jpg','IMG-20261119-WA5550.jpg','Hugo Boss','Joh-H',H44,'negro blanco suela blanca',95,0),
('Joh-D_12_gucci.jpg','IMG-20261118-WA6185.jpg','Gucci','Joh-D',D39,'blanco',95,0),
('Joh-D_02_calvin-klein.jpg','IMG-20261106-WA4467.jpg','Calvin Klein','Joh-D',D39,'negro',95,0),
('Joh-DH_01_gucci-bota.jpg','IMG-20261108-WA0164.jpg','Gucci bota','Joh-DH',D39+' / '+H44,'beige monograma verde rojo',100,0),
('Joh-D_08_clemont.jpg','IMG-20261106-WA4470.jpg','Clemont','Joh-D',D39,'beige',95,0),
('Joh-D_09_coach.jpg','IMG-20261106-WA4465.jpg','Coach','Joh-D',D39,'negro charol',95,0),
('Joh-D_10_coach.jpg','IMG-20261112-WA4847.jpg','Coach','Joh-D',D39,'negro blanco',95,0),
('Joh-DH_02_coach.jpg','IMG-20261106-WA4464.jpg','Coach','Joh-DH',D39,'azul oscuro',95,1),
('Joh-D_13_gucci.jpg','IMG-20261120-WA4962.jpg','Gucci','Joh-D',D39,'monograma verde rojo',95,0)]
for i,(f,s,n,ref,t,c,p,tr) in enumerate(rows,1):
    g=ref.split('-')[1]
    z=[36,37,38,39] if g=='D' else ([40,41,42,43,44] if g=='H' else [36,37,38,39,40,41,42,43,44])
    lab='%s/%s'%(ref,t.lower().replace(' / ','  '))
    if g=='DH':lab='Joh-DH/36eur al 39eur  40eur al 44eur'
    # reusa el ref del dato existente
    add('joh',i,f,J+s,n,ref,t,c,z,g,n.split()[0],lab,p,tr,extra=('',TU))
P=[('Joh-D_14_gucci.jpg','IMG-20261120-WA4877.jpg','Gucci','Joh-D','36EUR y 44EUR','monograma verde rojo',[36,44],'D',0),
('Joh-D_15_coach.jpg','IMG-20261120-WA4876.jpg','Coach','Joh-D','36EUR','negro',[36],'D',1),
('Joh-H_06_clemont.jpg','IMG-20261120-WA4874.jpg','Clemont','Joh-H','40EUR y 42EUR','negro rojo',[40,42],'H',1),
('Joh-H_07_clemont.jpg','IMG-20261120-WA4872.jpg','Clemont','Joh-H','40EUR','negro suela roja',[40],'H',0),
('Joh-D_16_karl-lagerfeld.jpg','IMG-20261120-WA4869.jpg','Karl Lagerfeld','Joh-D','36EUR','blanco negro',[36],'D',0)]
for i,(f,s,n,ref,t,c,z,g,tr) in enumerate(P,10):
    add('joh',i,f,J+s,n,ref,t,c,z,g,n.split()[0],'%s/%s'%(ref,t.lower()),80,tr,extra=('‼️PROMO‼️\n',TU))
TW,TH=420,525
for sn,mp in ims.items():
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for i,im in mp.items():
        t=im.copy();t.thumbnail((TW,TH),Image.LANCZOS);sh.paste(t,((i%4)*TW+(TW-t.width)//2,(i//4)*TH+(TH-t.height)//2))
    sh.save('s/%03d.jpg'%sn,quality=66,optimize=True)
D+=new
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):];open('index.html','w',encoding='utf-8').write(h)
json.dump(caps,open('/tmp/arjh_caps.json','w'),ensure_ascii=False)
print('nuevas',len(new),'sprite',s0,'u',u)
for kd in caps:
    for c in caps[kd]:print(c['fn']);print(c['cap']);print('--')
