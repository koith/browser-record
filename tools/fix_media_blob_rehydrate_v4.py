from pathlib import Path

p=Path('silent-camera-safari.html')
s=p.read_text(encoding='utf-8')

anchor="""function recoverThumb(imgEl, blob){
  try{
    if(!blob){ return; }
    urlCache.delete(blob);
    const u=URL.createObjectURL(blob);
    urlCache.set(blob,u);
    if(!imgEl.dataset.recovered){ imgEl.dataset.recovered='1'; imgEl.src=u; }
  }catch(e){}
}
"""
insert=anchor+"""
// iOS Safari can keep a stale backing-store relationship for IndexedDB Blobs
// after a media element has consumed them. Rehydrate through ArrayBuffer so each
// UI surface gets a physically new Blob and object URL instead of sharing one.
async function isolatedBlobURL(blob){
  if(!blob || typeof blob.arrayBuffer!=='function') throw new Error('invalid blob');
  const buf=await blob.arrayBuffer();
  const fresh=new Blob([buf],{type:blob.type||'application/octet-stream'});
  return URL.createObjectURL(fresh);
}
async function hydrateImgFromBlob(img, blob, fallback){
  if(!img)return;
  try{
    const u=await isolatedBlobURL(blob);
    if(!img.isConnected)return;
    img.src=u;
    img.onerror=()=>{
      const ph=document.createElement('span'); ph.className='ph'; ph.textContent=fallback||'🖼️';
      if(img.isConnected)img.replaceWith(ph);
    };
  }catch(e){
    const ph=document.createElement('span'); ph.className='ph'; ph.textContent=fallback||'🖼️';
    if(img.isConnected)img.replaceWith(ph);
  }
}
function hydrateMediaThumbs(root, mediaItems){
  if(!root)return;
  const imgs=[...root.querySelectorAll('img[data-thumb]')];
  let ii=0;
  for(const m of (mediaItems||[])){
    if(m.kind==='audio' || (m.kind==='video' && !m.poster)) continue;
    const img=imgs[ii++]; if(!img)break;
    const blob=(m.kind==='video' && m.poster)?m.poster:m.blob;
    hydrateImgFromBlob(img,blob,m.kind==='video'?'🎬':'🖼️');
  }
}
"""
if anchor not in s: raise SystemExit('recoverThumb anchor missing')
s=s.replace(anchor,insert,1)

old="""function mediaCell(m){
  if(m.kind==='video') return m.poster
    ? '<div class=\"m\"><img src=\"'+posterURL(m)+'\" loading=\"lazy\" onerror=\"this.replaceWith(Object.assign(document.createElement(\\'span\\'),{textContent:\\'🎬\\',className:\\'ph\\'}))\"><span class=\"play-badge\">▶</span></div>'
    : '<div class=\"m\"><span class=\"ph\">🎬</span><span class=\"play-badge\">▶</span></div>';
  if(m.kind==='audio') return '<div class=\"m audio\">🎙️</div>';
  return '<div class=\"m\"><img src=\"'+mediaURL(m)+'\" loading=\"lazy\" onerror=\"this.replaceWith(Object.assign(document.createElement(\\'span\\'),{textContent:\\'🖼️\\',className:\\'ph\\'}))\"></div>';
}
"""
new="""function mediaCell(m){
  if(m.kind==='video') return m.poster
    ? '<div class=\"m\"><img data-thumb=\"1\" loading=\"lazy\"><span class=\"play-badge\">▶</span></div>'
    : '<div class=\"m\"><span class=\"ph\">🎬</span><span class=\"play-badge\">▶</span></div>';
  if(m.kind==='audio') return '<div class=\"m audio\">🎙️</div>';
  return '<div class=\"m\"><img data-thumb=\"1\" loading=\"lazy\"></div>';
}
"""
if old not in s: raise SystemExit('mediaCell anchor missing')
s=s.replace(old,new,1)

old="""    const content=wrap.querySelector('.swipe-content');
    content.addEventListener('click',e=>{ if(content.style.transform&&content.style.transform!=='translateX(0px)'&&content.style.transform!==''){ closeAllRows(); return; } openEditor(n); });
"""
new="""    const content=wrap.querySelector('.swipe-content');
    hydrateMediaThumbs(wrap.querySelector('.nc-media'),(n.media||[]).slice(0,6));
    content.addEventListener('click',e=>{ if(content.style.transform&&content.style.transform!=='translateX(0px)'&&content.style.transform!==''){ closeAllRows(); return; } openEditor(n); });
"""
if old not in s: raise SystemExit('renderNotes anchor missing')
s=s.replace(old,new,1)

old="""        wrap.querySelector('.swipe-content').addEventListener('click',()=>{ currentFolderId=f.id; showNotes(); setTimeout(()=>openEditor(n),0); });
        grp.appendChild(wrap);
"""
new="""        hydrateMediaThumbs(wrap.querySelector('.nc-media'),(n.media||[]).slice(0,4));
        wrap.querySelector('.swipe-content').addEventListener('click',()=>{ currentFolderId=f.id; showNotes(); setTimeout(()=>openEditor(n),0); });
        grp.appendChild(wrap);
"""
if old not in s: raise SystemExit('folder search anchor missing')
s=s.replace(old,new,1)

old="""      img.src = m.kind==='video' ? (m.poster?posterURL(m):mediaURL(m)) : mediaURL(m);
      const srcBlob = (m.kind==='video' && m.poster) ? m.poster : m.blob;
      img.addEventListener('error',()=>recoverThumb(img, srcBlob));
      el.appendChild(img);
"""
new="""      const srcBlob = (m.kind==='video' && m.poster) ? m.poster : m.blob;
      el.appendChild(img);
      hydrateImgFromBlob(img,srcBlob,m.kind==='video'?'🎬':'🖼️');
"""
if old not in s: raise SystemExit('editor media anchor missing')
s=s.replace(old,new,1)

old="""let viewerIndex=-1; const viewer=$('viewer'), vwMedia=$('vwMedia');
let viewerObjectURL='';
"""
new="""let viewerIndex=-1; const viewer=$('viewer'), vwMedia=$('vwMedia');
let viewerObjectURL='';
let viewerLoadSeq=0;
"""
if old not in s: raise SystemExit('viewer vars anchor missing')
s=s.replace(old,new,1)

old="""function renderViewer(){
  if(!current||!current.media||!current.media[viewerIndex])return;
  releaseViewerObjectURL();
  const m=current.media[viewerIndex];
  const url=(m&&m.blob)?URL.createObjectURL(m.blob):'';
  viewerObjectURL=url;
"""
new="""async function renderViewer(){
  if(!current||!current.media||!current.media[viewerIndex])return;
  const seq=++viewerLoadSeq;
  releaseViewerObjectURL();
  vwMedia.innerHTML='';
  const m=current.media[viewerIndex];
  let url='';
  try{ url=await isolatedBlobURL(m&&m.blob); }
  catch(e){ if(seq===viewerLoadSeq) showToast('첨부파일을 읽지 못했습니다'); return; }
  if(seq!==viewerLoadSeq)return;
  viewerObjectURL=url;
"""
if old not in s: raise SystemExit('renderViewer anchor missing')
s=s.replace(old,new,1)

old="""function closeViewer(){
  cancelAnimationFrame(vwRaf);
"""
new="""function closeViewer(){
  viewerLoadSeq++;
  cancelAnimationFrame(vwRaf);
"""
if old not in s: raise SystemExit('closeViewer anchor missing')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('patched media Blob rehydration v4')
