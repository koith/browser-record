from pathlib import Path
import re
p=Path("silent-camera-safari.html");s=p.read_text()
old='<div class="rec-badge" id="recBadge"><span class="rec-dot"></span><span id="recTime">0:00</span></div><div class="cam-opacity" id="camOpacity"><span>투명도</span><input id="camOpacitySlider" type="range" min="15" max="100" step="5" value="40"></div>'
if old not in s: raise SystemExit("inline opacity html not found")
s=s.replace(old,'<div class="rec-badge" id="recBadge"><span class="rec-dot"></span><span id="recTime">0:00</span></div>')
s=s.replace('<div class="zoom-menu" id="zoomMenu">','<div class="cam-opacity" id="camOpacity"><div class="cam-opacity-head"><span>프리뷰 투명도</span><strong id="camOpacityReadout">40%</strong></div><input id="camOpacitySlider" type="range" min="15" max="100" step="5" value="40"></div>\n    <div class="zoom-menu" id="zoomMenu">',1)
s=re.sub(r'  \.cam-opacity\{[^\n]*\}\n  \.cam-opacity\.open\{[^\n]*\}\n  \.cam-opacity span\{[^\n]*\}\n  \.cam-opacity input\{[^\n]*\}', '  .cam-opacity{position:fixed;left:14px;right:14px;bottom:calc(92px + env(safe-area-inset-bottom));z-index:48;display:none;padding:12px 14px 14px;border-radius:16px;background:rgba(255,255,255,.86);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);box-shadow:0 5px 22px rgba(0,0,0,.18);border:1px solid rgba(255,255,255,.9)}\n  .cam-opacity.open{display:block}\n  .cam-opacity-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}\n  .cam-opacity-head span,.cam-opacity-head strong{font-size:13px;color:#1c1c1e}\n  .cam-opacity input{display:block;width:100%;height:32px;accent-color:#0a84ff}',s,count=1)
s=s.replace("const camOpacity=$('camOpacity'),camOpacitySlider=$('camOpacitySlider');","const camOpacity=$('camOpacity'),camOpacitySlider=$('camOpacitySlider'),camOpacityReadout=$('camOpacityReadout');")
s=s.replace("function applyCamOpacity(){cam.style.opacity=String(camOpacityValue/100);}","function applyCamOpacity(){cam.style.opacity=String(camOpacityValue/100);if(camOpacityReadout)camOpacityReadout.textContent=camOpacityValue+'%';}")
s=s.replace("if(e.target.closest('.cam-top,.cam-opacity'))return;","if(e.target.closest('.cam-top'))return;")
s=s.replace("if(e.target.closest('.cam-top,.cam-opacity'))return;const t=e.touches[0];","if(e.target.closest('.cam-top'))return;const t=e.touches[0];")
s=s.replace("if(camPreviewTapMoved||e.target.closest('.cam-top,.cam-opacity'))return;","if(camPreviewTapMoved||e.target.closest('.cam-top'))return;")
p.write_text(s)