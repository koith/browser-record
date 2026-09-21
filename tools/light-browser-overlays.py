from pathlib import Path
p=Path("silent-camera-safari.html"); s=p.read_text()
css=r'''
  /* Browser mode overlay chrome: light/translucent so it doesn't dominate pages. */
  body.browser-home:not(.memo-open) .memo-fab,
  body.browser-home:not(.memo-open) .cap-dock .big,
  body.browser-home:not(.memo-open) .zoom-btn{
    background:rgba(255,255,255,.72)!important;color:#1c1c1e!important;
    border:1px solid rgba(255,255,255,.82)!important;
    -webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);
    box-shadow:0 3px 14px rgba(0,0,0,.16)!important;
  }
  body.browser-home:not(.memo-open) .cam{border-color:rgba(255,255,255,.85);box-shadow:0 4px 16px rgba(0,0,0,.16)}
  body.browser-home:not(.memo-open) .cam .cam-top button{background:rgba(255,255,255,.72);color:#1c1c1e;-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
  body.browser-home:not(.memo-open) .zoom-menu{background:rgba(255,255,255,.76);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
  body.browser-home:not(.memo-open) .zoom-readout,body.browser-home:not(.memo-open) .opt-badge{color:#1c1c1e}
  .cam-opacity{position:absolute;left:5px;right:5px;top:25px;z-index:6;display:none;align-items:center;gap:4px;padding:4px 6px;border-radius:8px;background:rgba(255,255,255,.78);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
  .cam-opacity.open{display:flex}
  .cam-opacity span{font-size:9px;color:#1c1c1e;font-weight:700}
  .cam-opacity input{width:100%;min-width:0;height:18px;accent-color:#0a84ff}
'''
s=s.replace('</style>',css+'\n</style>')
s=s.replace('<div class="rec-badge" id="recBadge"><span class="rec-dot"></span><span id="recTime">0:00</span></div>', '<div class="rec-badge" id="recBadge"><span class="rec-dot"></span><span id="recTime">0:00</span></div><div class="cam-opacity" id="camOpacity"><span>투명도</span><input id="camOpacitySlider" type="range" min="15" max="100" step="5" value="40"></div>')
js=r'''
/* Browser camera preview opacity control. Tap preview to show/hide slider. */
const camOpacity=$('camOpacity'),camOpacitySlider=$('camOpacitySlider');
let camOpacityValue=parseInt(localStorage.getItem('camOpacity')||'40',10);
if(!Number.isFinite(camOpacityValue))camOpacityValue=40;
camOpacitySlider.value=String(camOpacityValue);
function applyCamOpacity(){cam.style.opacity=String(camOpacityValue/100);}
applyCamOpacity();
$('preview').addEventListener('click',e=>{e.stopPropagation();if(document.body.classList.contains('browser-home')&&!document.body.classList.contains('memo-open'))camOpacity.classList.toggle('open');});
camOpacitySlider.addEventListener('input',e=>{camOpacityValue=parseInt(e.target.value,10)||40;localStorage.setItem('camOpacity',String(camOpacityValue));applyCamOpacity();});
camOpacity.addEventListener('click',e=>e.stopPropagation());
'''
s=s.replace("/* ===== Rear lens detection",js+"\n/* ===== Rear lens detection")
s=s.replace("stream=null; cam.classList.remove('open');", "stream=null; camOpacity.classList.remove('open'); cam.classList.remove('open');")
p.write_text(s)
