from pathlib import Path

p = Path('silent-camera-safari.html')
s = p.read_text()

old = """function recoverThumb(imgEl, blob){
  try{
    if(!blob){ return; }
    urlCache.delete(blob);
    const u=URL.createObjectURL(blob);
    urlCache.set(blob,u);
    if(!imgEl.dataset.recovered){ imgEl.dataset.recovered='1'; imgEl.src=u; }
  }catch(e){}
}"""
new = """function recoverThumb(imgEl, blob, media, usePoster){
  try{
    if(!blob){ return; }
    urlCache.delete(blob);
    if(media){ if(usePoster) media._purl=''; else media._url=''; }
    const u=URL.createObjectURL(blob);
    urlCache.set(blob,u);
    if(media){ if(usePoster) media._purl=u; else media._url=u; }
    if(!imgEl.dataset.recovered){ imgEl.dataset.recovered='1'; imgEl.src=u; }
  }catch(e){}
}
function bindMediaThumbRecovery(root, mediaItems){
  if(!root)return;
  const imgs=[...root.querySelectorAll('img')];
  let ii=0;
  for(const m of (mediaItems||[])){
    if(m.kind==='audio' || (m.kind==='video' && !m.poster)) continue;
    const img=imgs[ii++]; if(!img) break;
    const usePoster=m.kind==='video' && !!m.poster;
    const blob=usePoster?m.poster:m.blob;
    img.onerror=null;
    img.addEventListener('error',()=>recoverThumb(img,blob,m,usePoster));
  }
}"""
if old not in s:
    raise SystemExit('recoverThumb block not found')
s = s.replace(old, new, 1)

old = """function mediaCell(m){
  if(m.kind==='video') return m.poster
    ? '<div class=\"m\"><img src=\"'+posterURL(m)+'\" loading=\"lazy\" onerror=\"this.replaceWith(Object.assign(document.createElement(\\'span\\'),{textContent:\\'🎬\\',className:\\'ph\\'}))\"><span class=\"play-badge\">▶</span></div>'
    : '<div class=\"m\"><span class=\"ph\">🎬</span><span class=\"play-badge\">▶</span></div>';
  if(m.kind==='audio') return '<div class=\"m audio\">🎙️</div>';
  return '<div class=\"m\"><img src=\"'+mediaURL(m)+'\" loading=\"lazy\" onerror=\"this.replaceWith(Object.assign(document.createElement(\\'span\\'),{textContent:\\'🖼️\\',className:\\'ph\\'}))\"></div>';
}"""
new = """function mediaCell(m){
  if(m.kind==='video') return m.poster
    ? '<div class=\"m\"><img src=\"'+posterURL(m)+'\" loading=\"lazy\"><span class=\"play-badge\">▶</span></div>'
    : '<div class=\"m\"><span class=\"ph\">🎬</span><span class=\"play-badge\">▶</span></div>';
  if(m.kind==='audio') return '<div class=\"m audio\">🎙️</div>';
  return '<div class=\"m\"><img src=\"'+mediaURL(m)+'\" loading=\"lazy\"></div>';
}"""
if old not in s:
    raise SystemExit('mediaCell block not found')
s = s.replace(old, new, 1)

old = """    const content=wrap.querySelector('.swipe-content');
    content.addEventListener('click',e=>{ if(content.style.transform&&content.style.transform!=='translateX(0px)'&&content.style.transform!==''){ closeAllRows(); return; } openEditor(n); });"""
new = """    const content=wrap.querySelector('.swipe-content');
    bindMediaThumbRecovery(wrap.querySelector('.nc-media'),(n.media||[]).slice(0,6));
    content.addEventListener('click',e=>{ if(content.style.transform&&content.style.transform!=='translateX(0px)'&&content.style.transform!==''){ closeAllRows(); return; } openEditor(n); });"""
if old not in s:
    raise SystemExit('note list bind point not found')
s = s.replace(old, new, 1)

old = """        wrap.querySelector('.swipe-content').addEventListener('click',()=>{ currentFolderId=f.id; showNotes(); setTimeout(()=>openEditor(n),0); });"""
new = """        bindMediaThumbRecovery(wrap.querySelector('.nc-media'),(n.media||[]).slice(0,4));
        wrap.querySelector('.swipe-content').addEventListener('click',()=>{ currentFolderId=f.id; showNotes(); setTimeout(()=>openEditor(n),0); });"""
if old not in s:
    raise SystemExit('folder search bind point not found')
s = s.replace(old, new, 1)

old = """      const srcBlob = (m.kind==='video' && m.poster) ? m.poster : m.blob;
      img.addEventListener('error',()=>recoverThumb(img, srcBlob));"""
new = """      const usePoster = m.kind==='video' && !!m.poster;
      const srcBlob = usePoster ? m.poster : m.blob;
      img.addEventListener('error',()=>recoverThumb(img, srcBlob, m, usePoster));"""
if old not in s:
    raise SystemExit('editor recovery bind not found')
s = s.replace(old, new, 1)

p.write_text(s)
