from pathlib import Path
p=Path("silent-camera-safari.html");s=p.read_text()
# Add a dedicated browser-mode floating shrink button beside camera; existing toolbar button is hidden with memo UI.
anchor='<div class="cam-opacity-backdrop" id="camOpacityBackdrop"></div>'
if anchor not in s: raise SystemExit("anchor missing")
s=s.replace(anchor,'<button class="cam-shrink-float" id="camShrinkFloat" type="button" aria-label="프리뷰 크기 전환">↙</button>\n    '+anchor,1)
css='.cam-shrink-float{position:fixed;right:108px;bottom:calc(160px + env(safe-area-inset-bottom));z-index:46;display:none;width:38px;height:38px;border:1px solid rgba(255,255,255,.9);border-radius:50%;background:rgba(255,255,255,.78);color:#1c1c1e;font-size:20px;font-weight:700;box-shadow:0 3px 14px rgba(0,0,0,.16);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);touch-action:manipulation}\nbody.browser-home:not(.memo-open).cam-active .cam-shrink-float{display:block}\n'
s=s.replace('.cam-opacity{position:fixed;',css+'.cam-opacity{position:fixed;',1)
# centralize shrink state so both controls stay synchronized
old="$('btnShrinkCam').addEventListener('click',()=>{ document.body.classList.toggle('shrink-cam'); const on=document.body.classList.contains('shrink-cam'); $('btnShrinkCam').classList.toggle('on',on); localStorage.setItem('shrinkCam',on?'1':'0'); });"
new="""function toggleCameraPreviewSize(){
  document.body.classList.toggle('shrink-cam');
  const on=document.body.classList.contains('shrink-cam');
  $('btnShrinkCam').classList.toggle('on',on);
  const fb=$('camShrinkFloat');if(fb){fb.classList.toggle('on',on);fb.textContent=on?'↗':'↙';}
  localStorage.setItem('shrinkCam',on?'1':'0');
}
$('btnShrinkCam').addEventListener('click',toggleCameraPreviewSize);
$('camShrinkFloat').addEventListener('click',e=>{e.preventDefault();e.stopPropagation();toggleCameraPreviewSize();});"""
if old not in s: raise SystemExit("shrink listener missing")
s=s.replace(old,new,1)
# init floating icon state
s=s.replace("$('btnShrinkCam').classList.toggle('on',sc);","$('btnShrinkCam').classList.toggle('on',sc); if($('camShrinkFloat')){$('camShrinkFloat').classList.toggle('on',sc);$('camShrinkFloat').textContent=sc?'↗':'↙';}",1)
p.write_text(s)