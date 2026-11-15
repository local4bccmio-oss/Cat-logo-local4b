#!/usr/bin/env python3
"""Actualiza las huellas de 'Buscar por foto' (solo calcula las referencias nuevas).
Uso (desde la raíz del repo, después de actualizar public/index.html y los sprites):  python3 tools/huellas.py
Necesita onnxruntime, numpy, pillow. Usa el modelo public/m/mc2.part0+part1 (MobileCLIP2-S0).
Genera public/huellas.json, huellas.bin, mean.bin, color.bin, colormean.bin. Caché: tools/cache.npz"""
import numpy as np,json,re,os,io,onnxruntime as ort
from PIL import Image
D=json.loads(re.search(r'const D=(\[.*?\]);\n',open('public/index.html',encoding='utf-8').read(),re.S).group(1))
mp='/tmp/mc2.onnx'
if not os.path.exists(mp):open(mp,'wb').write(open('public/m/mc2.part0','rb').read()+open('public/m/mc2.part1','rb').read())
s=ort.InferenceSession(mp,providers=['CPUExecutionProvider'])
cache={}
if os.path.exists('tools/cache.npz'):
    z=np.load('tools/cache.npz',allow_pickle=True);cache={f:(e,h) for f,e,h in zip(z['f'],z['E'],z['H'])}
def emb(im):
    W,H=im.size;c=im.crop((int(.1*W),int(.3*H),int(.9*W),int(.92*H)));w,h=c.size;m=max(w,h)
    sq=Image.new('RGB',(m,m),'white');sq.paste(c,((m-w)//2,(m-h)//2));sq=sq.resize((256,256),Image.BICUBIC)
    e=s.run(None,{'x':(np.asarray(sq,np.float32)/255).transpose(2,0,1)[None]})[0][0];return e/np.linalg.norm(e)
def hist(im):
    W,H=im.size;c=im.crop((int(.2*W),int(.4*H),int(.8*W),int(.85*H))).resize((48,48),Image.BILINEAR)
    a=np.asarray(c,np.int32)//64;b=np.bincount((a[...,0]*16+a[...,1]*4+a[...,2]).ravel(),minlength=64).astype(np.float32)
    b=np.sqrt(b/b.sum());return b/np.linalg.norm(b)
new=0;sp={}
for d in D:
    if d['f'] in cache:continue
    k=d['s']
    if k not in sp:sp={k:Image.open(f'public/s/{k:03d}.jpg').convert('RGB')}
    i=d['i'];x=(i%4)*420;y=(i//4)*525;t=sp[k].crop((x,y,x+420,y+525))
    cache[d['f']]=(emb(t).astype(np.float16),hist(t).astype(np.float16));new+=1
fs=[d['f'] for d in D];E=np.array([cache[f][0] for f in fs],np.float32);H=np.array([cache[f][1] for f in fs],np.float32)
np.savez('tools/cache.npz',f=np.array(list(cache.keys())),E=np.array([v[0] for v in cache.values()]),H=np.array([v[1] for v in cache.values()]))
def norm(X):
    mu=X.mean(0);Y=X-mu;Y/=np.linalg.norm(Y,axis=1,keepdims=True);return mu,np.round(Y*127).astype(np.int8)
mu,V=norm(E);V.tofile('public/huellas.bin');mu.astype('<f4').tofile('public/mean.bin')
mu,V=norm(H);V.tofile('public/color.bin');mu.astype('<f4').tofile('public/colormean.bin')
json.dump({'k':512,'n':len(D),'v':3,'f':fs},open('public/huellas.json','w'))
print('nuevas:',new,'total:',len(D))
