from pathlib import Path
p=Path("silent-camera-safari.html");s=p.read_text()
needle="body.browser-home:not(.memo-open)>.main>.cam,\n"
if needle not in s: raise SystemExit("allowlist missing")
s=s.replace(needle,"body.browser-home:not(.memo-open)>.main>.cam,\n  body.browser-home:not(.memo-open)>.main>.cam-shrink-float,\n  body.browser-home:not(.memo-open)>.main>.cam-opacity-backdrop,\n",1)
# iOS reliable tap binding, consistent with the rest of the app.
old="$('camShrinkFloat').addEventListener('click',e=>{e.preventDefault();e.stopPropagation();toggleCameraPreviewSize();});"
new="bindTap($('camShrinkFloat'),e=>{if(e){e.preventDefault();e.stopPropagation();}toggleCameraPreviewSize();});"
if old not in s: raise SystemExit("listener missing")
s=s.replace(old,new,1)
p.write_text(s)