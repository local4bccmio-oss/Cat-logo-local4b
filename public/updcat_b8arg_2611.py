import re,json,os
exec(open('updcat_b3b4b5_2211.py').read().split("os.chdir")[0])
os.chdir('/home/claude/cat-logo-local4b/public')
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1]);byf={d['f']:d for d in D}
SC='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
smax=max(d['s'] for d in D);S=[smax,sum(1 for d in D if d['s']==smax)]
def slot():
    if S[1]>=12:S[0]+=1;S[1]=0
    r=(S[0],S[1]);S[1]+=1;return r
u=int(max(d.get('u',0) for d in D))+1
for f in ['8329-D.jpg','8019-D.jpg','8156-D_158-H.jpg','8042-D_043-H.jpg']:
    byf[f]['d']='26/11';byf[f].pop('a',None)
os.makedirs(SC+'jk',exist_ok=True);caps=[];new=[]
J=[('141','Nike'.replace('Nike','New Balance'),'New Balance 9060','gris y negro',[36,37,38],95,'IMG-20261126-WA1318.jpg','D'),
('148','Nike','Nike Zoom X','gris y verde neón',[40,41,42,43],85,'IMG-20261126-WA1327.jpg','H'),
('084','Adidas','Adidas Superstar','blanco y negro',[36,37,38,39],75,'IMG-20261125-WA2417.jpg','D')]
for cod,mar,name,col,z,P,img,L in J:
    f='8%s-%s.jpg'%(cod,L);assert f not in byf
    t=tstr(z);lab='8%s-%s/%s'%(cod,L,t.lower());fn='%02d_%s'%(len(caps)+1,f);src='/tmp/w/y4/'+img
    make(src,lab,SC+'jk/'+fn,1080,1350,0);make(src,lab,'p/'+f,640,800,0)
    sn,si=slot();e=dict(f=f,b='B8',n=name,r=[cod],t=t,c=col,z=z,g=L,m=mar,s=sn,i=si,u=u,d='26/11');new.append(e);byf[f]=e
    caps.append(dict(fn=fn,cap='*%s* Ref _8%s_\n*$%d.000*\n*%s*\n~%s~'%(name,cod,P,t,col)))
D+=new
TW,TH=420,525
for sn in sorted({e['s'] for e in new}):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for d in D:
        if d['s']==sn:
            im=Image.open('p/'+d['f']).convert('RGB');im.thumbnail((TW,TH),Image.LANCZOS);i=d['i'];sh.paste(im,((i%4)*TW+(TW-im.width)//2,(i//4)*TH+(TH-im.height)//2))
    sh.save('s/%03d.jpg'%sn,quality=66,optimize=True)
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):];open('index.html','w',encoding='utf-8').write(h)
# Argot (solo envío)
A=[('102','Sandalia Louis Vuitton','negro',55,'WA5589'),('103','Sandalia Hermes','beige',55,'WA5590'),('104','Sandalia Dior','azul jean',90,'WA5591'),
('105','Sandalia Chanel','negro brillante',90,'WA5592'),('106','Sandalia Karl Lagerfeld','blanco',90,'WA5593'),('107','Sandalia Guess','blanco',90,'WA5595')]
os.makedirs(SC+'arg',exist_ok=True)
for n,name,col,P,w in A:
    z=[36,37,38,39];t=tstr(z);lab='Arg%s-D/%s'%(n,t.lower());fn='%02d_Arg%s-D.jpg'%(len(caps)+1,n)
    make('/tmp/w/y5/IMG-20261126-%s.jpg'%w,lab,SC+'arg/'+fn,1080,1350,0)
    caps.append(dict(fn=fn,cap='*%s* Ref _Arg%s_\n*$%d.000*\n*%s*\n~%s~'%(name,n,P,t,col)))
json.dump(caps,open('/tmp/w/caps_b8arg.json','w'),ensure_ascii=False)
for c in caps:print(c['fn'],'|',c['cap'].replace('\n',' / '))
