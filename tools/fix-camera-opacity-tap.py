from pathlib import Path
p=Path("silent-camera-safari.html");s=p.read_text()
old="""$('preview').addEventListener('click',e=>{e.stopPropagation();if(document.body.classList.contains('browser-home')&&!document.body.classList.contains('memo-open'))camOpacity.classList.toggle('open');});"""
new="""function toggleCamOpacityFromPreview(e){
  if(e.target.closest('.cam-top,.cam-opacity'))return;
  if(document.body.classList.contains('browser-home')&&!document.body.classList.contains('memo-open')){
    e.preventDefault();e.stopPropagation();camOpacity.classList.toggle('open');
  }
}
// The entire preview surface is the opacity control trigger. Bind to the camera
// container (not <video>) because iOS Safari may consume video click events.
let camPreviewTapMoved=false,camPreviewTapX=0,camPreviewTapY=0;
cam.addEventListener('touchstart',e=>{if(e.target.closest('.cam-top,.cam-opacity'))return;const t=e.touches[0];camPreviewTapMoved=false;camPreviewTapX=t.clientX;camPreviewTapY=t.clientY;},{passive:true});
cam.addEventListener('touchmove',e=>{if(!e.touches[0])return;const t=e.touches[0];if(Math.hypot(t.clientX-camPreviewTapX,t.clientY-camPreviewTapY)>10)camPreviewTapMoved=true;},{passive:true});
cam.addEventListener('touchend',e=>{if(camPreviewTapMoved||e.target.closest('.cam-top,.cam-opacity'))return;toggleCamOpacityFromPreview(e);},{passive:false});
cam.addEventListener('click',e=>{if('ontouchstart' in window)return;toggleCamOpacityFromPreview(e);});"""
if old not in s: raise SystemExit("old preview click not found")
s=s.replace(old,new)
p.write_text(s)
