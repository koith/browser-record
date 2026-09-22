from pathlib import Path
p=Path("silent-camera-safari.html");s=p.read_text()
s=s.replace(".cam-opacity.open{display:block}", ".cam-opacity.open{display:block}\n.cam-opacity-backdrop{position:fixed;inset:0;z-index:47;display:none;background:transparent;pointer-events:auto;touch-action:manipulation}\n.cam-opacity-backdrop.open{display:block}",1)
s=s.replace('<div class="cam-opacity" id="camOpacity">', '<div class="cam-opacity-backdrop" id="camOpacityBackdrop"></div>\n    <div class="cam-opacity" id="camOpacity">',1)
start=s.index("/* Browser camera preview opacity control.")
end=s.index("\n/* ===== Rear lens detection",start)
block=r'''/* Browser camera preview opacity control. The transparent backdrop sits above
   the cross-origin iframe, so taps on the web page can reliably dismiss the panel. */
const camOpacity=$('camOpacity'),camOpacityBackdrop=$('camOpacityBackdrop'),camOpacitySlider=$('camOpacitySlider'),camOpacityReadout=$('camOpacityReadout');
let camOpacityValue=parseInt(localStorage.getItem('camOpacity')||'40',10);
if(!Number.isFinite(camOpacityValue))camOpacityValue=40;
camOpacitySlider.value=String(camOpacityValue);
function applyCamOpacity(){video.style.opacity=String(camOpacityValue/100);if(camOpacityReadout)camOpacityReadout.textContent=camOpacityValue+'%';}
function openCamOpacity(){
  camOpacity.classList.add('open');camOpacityBackdrop.classList.add('open');
}
function closeCamOpacity(){
  localStorage.setItem('camOpacity',String(camOpacityValue));
  camOpacity.classList.remove('open');camOpacityBackdrop.classList.remove('open');
}
applyCamOpacity();
function toggleCamOpacityFromPreview(e){
  if(e.target.closest('.cam-top'))return;
  if(document.body.classList.contains('browser-home')&&!document.body.classList.contains('memo-open')){
    e.preventDefault();e.stopPropagation();
    if(camOpacity.classList.contains('open'))closeCamOpacity();else openCamOpacity();
  }
}
let camPreviewTapMoved=false,camPreviewTapX=0,camPreviewTapY=0;
cam.addEventListener('touchstart',e=>{if(e.target.closest('.cam-top'))return;const t=e.touches[0];camPreviewTapMoved=false;camPreviewTapX=t.clientX;camPreviewTapY=t.clientY;},{passive:true});
cam.addEventListener('touchmove',e=>{if(!e.touches[0])return;const t=e.touches[0];if(Math.hypot(t.clientX-camPreviewTapX,t.clientY-camPreviewTapY)>10)camPreviewTapMoved=true;},{passive:true});
cam.addEventListener('touchend',e=>{if(camPreviewTapMoved||e.target.closest('.cam-top'))return;toggleCamOpacityFromPreview(e);},{passive:false});
cam.addEventListener('click',e=>{if('ontouchstart' in window)return;toggleCamOpacityFromPreview(e);});
camOpacitySlider.addEventListener('input',e=>{camOpacityValue=parseInt(e.target.value,10);if(!Number.isFinite(camOpacityValue))camOpacityValue=40;localStorage.setItem('camOpacity',String(camOpacityValue));applyCamOpacity();});
camOpacity.addEventListener('touchstart',e=>e.stopPropagation(),{passive:true});
camOpacity.addEventListener('touchmove',e=>e.stopPropagation(),{passive:true});
camOpacity.addEventListener('touchend',e=>e.stopPropagation(),{passive:true});
camOpacity.addEventListener('click',e=>e.stopPropagation());
camOpacityBackdrop.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();closeCamOpacity();},{passive:false});
'''
s=s[:start]+block+s[end:]
# ensure close/background cleanup removes backdrop too
s=s.replace("stream=null; camOpacity.classList.remove('open'); cam.classList.remove('open');", "stream=null; camOpacity.classList.remove('open'); camOpacityBackdrop.classList.remove('open'); cam.classList.remove('open');")
p.write_text(s)