from pathlib import Path
p=Path('silent-camera-safari.html')
s=p.read_text(encoding='utf-8')

old="let viewerIndex=-1; const viewer=$('viewer'), vwMedia=$('vwMedia');"
new="let viewerIndex=-1; const viewer=$('viewer'), vwMedia=$('vwMedia');\nlet viewerObjectURL='';\nfunction releaseViewerObjectURL(){\n  if(!viewerObjectURL)return;\n  const old=viewerObjectURL; viewerObjectURL='';\n  setTimeout(()=>{ try{ URL.revokeObjectURL(old); }catch(e){} },0);\n}"
if old not in s: raise SystemExit('viewer declaration anchor not found')
s=s.replace(old,new,1)

old="  const m=current.media[viewerIndex]; const url=mediaURL(m);"
new="  releaseViewerObjectURL();\n  const m=current.media[viewerIndex];\n  const url=(m&&m.blob)?URL.createObjectURL(m.blob):'';\n  viewerObjectURL=url;"
if old not in s: raise SystemExit('renderViewer url anchor not found')
s=s.replace(old,new,1)

old="""function closeViewer(){
  cancelAnimationFrame(vwRaf);
  // pause only — do NOT removeAttribute('src')/load(), that can invalidate the
  // blob URL shared with the list/editor thumbnails and break them.
  const vid=document.getElementById('vwVideo');
  if(vid){ try{ vid.pause(); }catch(e){} }
  viewer.classList.remove('open');
  vwMedia.innerHTML='';
  $('vwCtrl').style.display='none';
  viewerIndex=-1;
  try{ sheetBg.classList.remove('open'); sheetHost.innerHTML=''; }catch(e){}
}"""
new="""function closeViewer(){
  cancelAnimationFrame(vwRaf);
  const vid=document.getElementById('vwVideo');
  if(vid){ try{ vid.pause(); }catch(e){} }
  viewer.classList.remove('open');
  vwMedia.innerHTML='';
  releaseViewerObjectURL();
  $('vwCtrl').style.display='none';
  viewerIndex=-1;
  try{ sheetBg.classList.remove('open'); sheetHost.innerHTML=''; }catch(e){}
}"""
if old not in s: raise SystemExit('closeViewer anchor not found')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
