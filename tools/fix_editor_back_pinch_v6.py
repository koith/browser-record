from pathlib import Path
p=Path('silent-camera-safari.html')
s=p.read_text()
old="""$('edBack').addEventListener('click',saveCurrent);\n$('btnSave').addEventListener('click',saveCurrent);"""
new="""// iOS Safari can consume the first tap only to dismiss the keyboard.\n// Use the same touch-safe tap binding as the capture controls so Back always fires.\nbindTap($('edBack'), saveCurrent);\n$('btnSave').addEventListener('click',saveCurrent);\n\n// Do not allow page/editor pinch zoom. Attachment image pinch remains available\n// inside the dedicated viewer because these guards are scoped to #editor only.\neditor.addEventListener('touchmove',e=>{ if(e.touches&&e.touches.length>1)e.preventDefault(); },{passive:false});\neditor.addEventListener('gesturestart',e=>e.preventDefault(),{passive:false});\neditor.addEventListener('gesturechange',e=>e.preventDefault(),{passive:false});"""
if old not in s:
    raise SystemExit('target binding block not found')
s=s.replace(old,new,1)
old_css=".editor { position:absolute; inset:0; background:var(--paper); display:none; flex-direction:column; }"
new_css=".editor { position:absolute; inset:0; background:var(--paper); display:none; flex-direction:column; touch-action:pan-y; }"
if old_css not in s:
    raise SystemExit('editor css target not found')
s=s.replace(old_css,new_css,1)
p.write_text(s)
