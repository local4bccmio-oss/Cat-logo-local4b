import re,json,datetime as dt
h=open('index.html',encoding='utf-8').read();mm=re.search(r'const D=(\[.*?\]);\n',h,re.S);D=json.loads(mm[1])
byf={d['f']:d for d in D}
I=json.load(open('/tmp/b0items2.json'));seen=nz=0
def tstr(z):
    out=[];run=[]
    for n in z:
        if run and n==run[-1]+1:run.append(n)
        else:
            if run:out.append(run)
            run=[n]
    if run:out.append(run)
    return ' / '.join(('%dEUR'%r[0]) if len(r)==1 else ('%dEUR-%dEUR'%(r[0],r[1]) if len(r)==2 else '%dEUR al %dEUR'%(r[0],r[-1])) for r in out)
for it in I:
    for f in it['ents']:
        d=byf.get(f)
        if not d:continue
        seen+=1;d['d']='20/11';d.pop('a',None);d.pop('h',None)
        if it['z']!=d['z']:d['z']=it['z'];d['t']=tstr(it['z']);nz+=1
AG=dt.date(2026,11,14);HI=dt.date(2026,11,10);st=dict(a=0,h=0,pocas=0)
for d in D:
    if d['b']!='B0' or not d.get('d'):continue
    q=dt.date(2026,int(d['d'][3:5]),int(d['d'][:2]))
    if q<=AG:d['a']=1;st['a']+=1
    if q<=HI:d['h']=1;st['h']+=1
    if d['d'] in('18/11','19/11','20/11') and len(d['z'])<=3:d['a']=1;st['pocas']+=1
h=h[:mm.start(1)]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+h[mm.end(1):]
open('index.html','w',encoding='utf-8').write(h)
print('vistas',seen,'tallas',nz,st)
