from pathlib import Path
p=Path("silent-camera-safari.html");s=p.read_text()
s=s.replace('.cam-opacity{position:absolute;left:5px;right:5px;top:25px;z-index:6;display:none;align-items:center;gap:4px;padding:4px 6px;border-radius:8px;background:rgba(255,255,255,.78);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}','.cam-opacity{position:fixed;left:50%;bottom:calc(86px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:44;width:min(310px,calc(100vw - 28px));display:none;align-items:center;gap:8px;padding:10px 12px;border-radius:14px;background:rgba(255,255,255,.82);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);box-shadow:0 4px 18px rgba(0,0,0,.18)}')
s=s.replace('.cam-opacity span{font-size:9px;', '.cam-opacity span{font-size:12px;')
s=s.replace('.cam-opacity input{width:100%;min-width:0;height:18px;', '.cam-opacity input{width:100%;min-width:0;height:28px;')
old='<div class="rec-badge" id="recBadge"><span class="rec-dot"></span><span id="recTime">0:00</span></div><div class="cam-opacity" id="camOpacity"><span>투명도</span><input id="camOpacitySlider" type="range" min="15" max="100" step="5" value="40"></div>\n      <video'
new='<div class="rec-badge" id="recBadge"><span class="rec-dot"></span><span id="recTime">0:00</span></div>\n      <video'
if old not in s: raise SystemExit("inner opacity html not found")
s=s.replace(old,new)
needle='''    <div class="zoom-menu" id="zoomMenu">'''
external='''    <div class="cam-opacity" id="camOpacity"><span>투명도</span><input id="camOpacitySlider" type="range" min="15" max="100" step="5" value="40"></div>
    <div class="zoom-menu" id="zoomMenu">'''
s=s.replace(needle,external,1)
p.write_text(s)
