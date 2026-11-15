// Buscar por foto: se carga solo cuando el cliente sube una foto.
const S=256,CW=0.3;let P=null;
async function load(st){
  st('Cargando el buscador de imágenes (la primera vez tarda, ~46 MB)…');
  const meta=await (await fetch('huellas.json?_='+Date.now())).json();
  const V=new Int8Array(await (await fetch('huellas.bin?_='+Date.now())).arrayBuffer());
  const mean=new Float32Array(await (await fetch('mean.bin?_='+Date.now())).arrayBuffer());
  const CV=new Int8Array(await (await fetch('color.bin?_='+Date.now())).arrayBuffer());
  const cmean=new Float32Array(await (await fetch('colormean.bin?_='+Date.now())).arrayBuffer());
  const pos=new Map(meta.f.map((f,i)=>[f,i]));
  const ort=await import('https://cdn.jsdelivr.net/npm/onnxruntime-web@1.20.1/dist/ort.min.mjs');
  ort.env.wasm.wasmPaths='https://cdn.jsdelivr.net/npm/onnxruntime-web@1.20.1/dist/';
  const p0=new Uint8Array(await (await fetch('m/mc2.part0')).arrayBuffer()),p1=new Uint8Array(await (await fetch('m/mc2.part1')).arrayBuffer());
  const m=new Uint8Array(p0.length+p1.length);m.set(p0);m.set(p1,p0.length);
  const sess=await ort.InferenceSession.create(m.buffer,{executionProviders:['wasm']});
  return {K:meta.k,V,mean,CV,cmean,pos,ort,sess};
}
function crop(im){
  const W=im.naturalWidth,H=im.naturalHeight,sx=.1*W,sy=.3*H,sw=.8*W,sh=.62*H,m=Math.max(sw,sh);
  const c=document.createElement('canvas');c.width=c.height=S;const g=c.getContext('2d');
  g.fillStyle='#fff';g.fillRect(0,0,S,S);const k=S/m;g.drawImage(im,sx,sy,sw,sh,(S-sw*k)/2,(S-sh*k)/2,sw*k,sh*k);return c}
function chist(im,cmean){
  const W=im.naturalWidth,H=im.naturalHeight,c=document.createElement('canvas');c.width=c.height=48;const g=c.getContext('2d');
  g.drawImage(im,.2*W,.4*H,.6*W,.45*H,0,0,48,48);const d=g.getImageData(0,0,48,48).data,h=new Float32Array(64);
  for(let i=0;i<2304;i++)h[(d[i*4]>>6)*16+(d[i*4+1]>>6)*4+(d[i*4+2]>>6)]++;
  let n=0;for(let j=0;j<64;j++){h[j]=Math.sqrt(h[j]/2304);n+=h[j]*h[j]}n=Math.sqrt(n)||1;
  let m=0;for(let j=0;j<64;j++){h[j]=h[j]/n-cmean[j];m+=h[j]*h[j]}m=Math.sqrt(m)||1;for(let j=0;j<64;j++)h[j]/=m;return h}
async function embed(c,p){
  const d=c.getContext('2d').getImageData(0,0,S,S).data,a=new Float32Array(3*S*S),n=S*S;
  for(let i=0;i<n;i++){a[i]=d[i*4]/255;a[n+i]=d[i*4+1]/255;a[2*n+i]=d[i*4+2]/255}
  const r=await p.sess.run({x:new p.ort.Tensor('float32',a,[1,3,S,S])});
  const v=Float32Array.from(r[p.sess.outputNames[0]].data);let s=0;for(let j=0;j<p.K;j++)s+=v[j]*v[j];s=Math.sqrt(s)||1;
  let nq=0;for(let j=0;j<p.K;j++){v[j]=v[j]/s-p.mean[j];nq+=v[j]*v[j]}nq=Math.sqrt(nq)||1;for(let j=0;j<p.K;j++)v[j]/=nq;return v}
// D: lista de modelos del catálogo (con .f). Devuelve los códigos (f) de los 30 más parecidos, en orden.
export async function buscar(file,D,st){
  if(!P)P=load(st).catch(e=>{P=null;throw e});
  const p=await P;st('Buscando…');
  const url=URL.createObjectURL(file);const im=new Image();im.src=url;await im.decode();
  const q=await embed(crop(im),p),qc=chist(im,p.cmean),K=p.K,sims=[];
  D.forEach((d,i)=>{const r=p.pos.get(d.f);if(r===undefined)return;let s=0,o=r*K;for(let j=0;j<K;j++)s+=p.V[o+j]*q[j];let c=0;o=r*64;for(let j=0;j<64;j++)c+=p.CV[o+j]*qc[j];sims.push([s/127+CW*c/127,d.f])});
  sims.sort((a,b)=>b[0]-a[0]);return {f:sims.slice(0,30).map(x=>x[1]),url};
}
