import re,json,math,os,collections,sys
from PIL import Image
B='/tmp/claude-0/-home-claude/ded30c03-3ac4-5560-b95f-09e5d98db5e1/scratchpad/'
h=open('index.html').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1])
APPLY=len(sys.argv)>1
have={d['f'] for d in D}
new=[]
if '8042-D_043-H.jpg' not in have:
    s0=max(d['s'] for d in D)+1
    new=[dict(f='8042-D_043-H.jpg',b='B8',n='Adidas Samba',r=['042','043'],t='36EUR al 37EUR-39EUR / 40EUR al 41EUR',c='negro blanco',j='',z=[36,37,39,40,41],g='DH',m='Adidas',s=s0,i=0,u=max(d.get('u',0) for d in D)+1)]
    if APPLY:
        im=Image.open(B+'b810out/8042-D_043-H.jpg').convert('RGB');im.resize((640,800),Image.LANCZOS).save('p/8042-D_043-H.jpg',quality=80,optimize=True)
        sh=Image.new('RGB',(4*420,3*525),'white');im.thumbnail((420,525),Image.LANCZOS);sh.paste(im,((420-im.width)//2,(525-im.height)//2));sh.save(f's/{s0:03d}.jpg',quality=66,optimize=True)
    D+=new

import re as _r
T=open(B+'b8n10/Chat de WhatsApp con JUKA - MODA BODEGA 510.txt',encoding='utf8').read().replace('\u202f',' ').replace('\u200e','').split('\n')
rows=[];cur=None
for l in T:
    m=_r.match(r'^(\d+)/(\d+)/2026, ',l)
    if m: cur=dict(date=f'{int(m[1])}/{int(m[2])}',body=l);rows.append(cur)
    elif cur: cur['body']+='\n'+l

key=lambda s:(int(s.split('/')[1]),int(s.split('/')[0]))
last={};sz={}
for m in rows:
    b=m['body'];c=re.search(r'C[ÓO]DIGO:?\s*([\d\-]+)',b,re.I)
    if not c: continue
    t=b.split('C')[0] and re.split(r'T[AÁ]LLAS|ᴛᴀʟʟᴀs|💸\s*$',b,flags=re.I|re.M)
    after=b.split('💸')[-1] if '💸' in b else ''
    after=after.replace('436/37','36/37').replace('*RECARGA*','')
    parts=c[1].split('-')
    if re.search(r'HASTA',after,re.I): nums=list(range(36,45))
    else: nums=[int(n) for n in re.findall(r'(?<!\d)(3[4-9]|4[0-5])(?!\d)',after)]
    for p in parts:
        k=p.zfill(3);last[k]=m['date']
        if nums: sz[k]=(m['date'],nums)
st=collections.Counter()
for d in D:
    if d['b']!='B8':continue
    ds=[last[r] for r in d['r'] if r in last]
    if not ds: st['sin']+=1;d['h']=1;d['d']='';continue
    L=max(ds,key=key);d['d']='%02d/%02d'%(int(L.split('/')[0]),int(L.split('/')[1]))
    if key(L)<=(11,6): d['a']=1;st['agotado']+=1
    else:
        if d.pop('a',None):st['des_agotado']+=1
    if key(L)<=(11,2): d['h']=1;st['oculto']+=1
    else:
        if d.pop('h',None):st['des']+=1
    letters=re.findall(r'-([DHM])',d['f'])
    if all(r in sz and key(sz[r][0])>=(11,6) for r in d['r']):
        zz=[]
        for r,l in zip(d['r'],letters):
            n=sz[r][1]
            n=[a for a in n if a<=39] if l=='D' else [a for a in n if a>=40] if l=='H' else n
            zz.append(n)
        U=sorted(set(a for n in zz for a in n))
        if U and U!=d['z']:
            def rng(s):
                out=[];i=0;s=sorted(set(s))
                while i<len(s):
                    j=i
                    while j+1<len(s) and s[j+1]==s[j]+1:j+=1
                    out.append((s[i],s[j]));i=j+1
                return '-'.join(f'{a}EUR al {b}EUR' if b>a else f'{a}EUR' for a,b in out)
            d['z']=U;d['t']=' / '.join(rng(n) for n in zz if n) if len(zz)>1 else rng(zz[0]);st['tallas']+=1
D_=[d for d in D if d['b']=='B8'];print(dict(st),len(D_))
if APPLY: h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
if APPLY: open('index.html','w').write(h)
