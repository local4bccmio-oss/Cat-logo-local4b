import re,json,datetime as dt
from PIL import Image
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1])
M=json.load(open('/tmp/b6match.json'))
seen={m['m1'] for m in M if m['s1']>=0.93 and not m['f'].endswith('WA6755.jpg')}
N=[('63643-D_3642-H','Louis Vuitton',['63643','63642'],'negro blanco','Louis Vuitton'),
('63641-D_3640-H','Louis Vuitton',['63641','63640'],'crema café','Louis Vuitton'),
('63645-D_3644-H','Louis Vuitton',['63645','63644'],'negro','Louis Vuitton'),
('63685-H','Jordan Cadense',['63685'],'negro rojo blanco','Jordan'),
('63373-H','Puma Easy BMW',['63373'],'negro azul rojo','Puma'),
('63473-H','New Balance 410',['63473'],'negro','New Balance'),
('63597-H_3596-D','Off White',['63597','63596'],'blanco negro','Otras'),
('63807-D_3808-H','Nike For One',['63807','63808'],'blanco','Nike')]
s0=max(d['s'] for d in D)+1;u=max(d.get('u',0) for d in D)+1
new=[];TW,TH=420,525;sh=Image.new('RGB',(4*TW,3*TH),'white')
for k,(fn,n,r,c,m) in enumerate(N):
    pair=len(r)==2
    z=list(range(36,45)) if pair else list(range(40,45))
    e=dict(f=fn+'.jpg',b='B6',n=n,r=r,t='36EUR al 39EUR / 40EUR al 44EUR' if pair else '40EUR al 44EUR',c=c,z=z,g='DH' if pair else 'H',m=m,s=s0,i=k,u=u,d='18/11')
    new.append(e)
    im=Image.open('/tmp/b6out/'+fn+'.jpg').convert('RGB')
    im.resize((640,800),Image.LANCZOS).save('p/'+fn+'.jpg',quality=80,optimize=True)
    im.thumbnail((TW,TH),Image.LANCZOS);sh.paste(im,((k%4)*TW+(TW-im.width)//2,(k//4)*TH+(TH-im.height)//2))
sh.crop((0,0,4*TW,2*TH)).save(f's/{s0:03d}.jpg',quality=66,optimize=True)
have={d['f'] for d in D};assert not any(e['f'] in have for e in new)
AG=dt.date(2026,11,14);HI=dt.date(2026,11,10);c=0
for d in D+new:
    if d['b']!='B6':continue
    if d['f'] in seen: d['d']='18/11';d.pop('a',None);d.pop('h',None);c+=1
    if not d.get('d'):continue
    q=dt.date(2026,int(d['d'][3:5]),int(d['d'][:2]))
    if q<=AG:d['a']=1
    if q<=HI:d['h']=1
D+=new
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
open('index.html','w',encoding='utf-8').write(h)
print('nuevas',len(new),'reposts',c,len(seen))
