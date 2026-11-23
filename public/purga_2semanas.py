"""Regla 23/11: ficha cuyo último post en los zips fue hace más de 14 días se borra (foto, sprite y ficha). Uso: python3 public/purga_2semanas.py [hoy dd/mm]"""
import re,json,os,sys,datetime as dt
from PIL import Image
hoy=dt.date(2026,int(sys.argv[1][3:5]),int(sys.argv[1][:2])) if len(sys.argv)>1 else dt.date.today()
cut=hoy-dt.timedelta(days=14)
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1])
q=lambda d:dt.date(2026,int(d['d'][3:5]),int(d['d'][:2]))
keep=[d for d in D if not d.get('d') or q(d)>cut];gone=[d for d in D if d.get('d') and q(d)<=cut]
for d in gone:
    try:os.remove('p/'+d['f'])
    except FileNotFoundError:pass
order=sorted(range(len(keep)),key=lambda k:(keep[k]['s'],keep[k]['i']));TW,TH=420,525;n=0
for a in range(0,len(order),12):
    sh=Image.new('RGB',(4*TW,3*TH),'white')
    for j,k in enumerate(order[a:a+12]):
        d=keep[k];d['_s'],d['_i']=d['s'],d['i'];d['s']=a//12;d['i']=j
        if os.path.exists('p/'+d['f']):
            im=Image.open('p/'+d['f']).convert('RGB');im.thumbnail((TW,TH),Image.LANCZOS);sh.paste(im,((j%4)*TW+(TW-im.width)//2,(j//4)*TH+(TH-im.height)//2))
        else:
            o=Image.open('/tmp/s_old/%03d.jpg'%d['_s']).convert('RGB');x=(d['_i']%4)*TW;y=(d['_i']//4)*TH;sh.paste(o.crop((x,y,x+TW,y+TH)),(j%4*TW,j//4*TH))
    sh.save('s/%03d.jpg'%(a//12),quality=66,optimize=True);n=a//12+1
for f in os.listdir('s'):
    if f.endswith('.jpg') and int(f[:3])>=n:os.remove('s/'+f)
h=h[:mm.start(1)]+json.dumps(keep,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):];[(d.pop('_s',None),d.pop('_i',None)) for d in keep];open('index.html','w',encoding='utf-8').write(h)
print('borradas',len(gone),'quedan',len(keep),'sprites',n)
