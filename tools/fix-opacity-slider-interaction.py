from pathlib import Path
p=Path("silent-camera-safari.html");s=p.read_text()
old="""body.browser-home:not(.memo-open)>.main>.cam,
  body.browser-home:not(.memo-open)>.main>.cap-dock,
  body.browser-home:not(.memo-open)>.main>.zoom-menu,"""
new="""body.browser-home:not(.memo-open)>.main>.cam,
  body.browser-home:not(.memo-open)>.main>.cap-dock,
  body.browser-home:not(.memo-open)>.main>.cam-opacity,
  body.browser-home:not(.memo-open)>.main>.zoom-menu,"""
if old not in s: raise SystemExit("pointer allowlist not found")
s=s.replace(old,new,1)
# Explicit touch behavior for reliable iOS range dragging.
s=s.replace('.cam-opacity input{display:block;width:100%;height:32px;accent-color:#0a84ff}', '.cam-opacity input{display:block;width:100%;height:38px;accent-color:#0a84ff;pointer-events:auto;touch-action:pan-x}')
# Keep panel touches isolated from the transparent parent main layer.
s=s.replace("camOpacity.addEventListener('click',e=>e.stopPropagation());", "camOpacity.addEventListener('touchstart',e=>e.stopPropagation(),{passive:true});\ncamOpacity.addEventListener('touchmove',e=>e.stopPropagation(),{passive:true});\ncamOpacity.addEventListener('touchend',e=>e.stopPropagation(),{passive:true});\ncamOpacity.addEventListener('click',e=>e.stopPropagation());")
p.write_text(s)