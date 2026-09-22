from pathlib import Path
p=Path("silent-camera-safari.html");s=p.read_text()
s=s.replace('id="camOpacitySlider" type="range" min="15" max="100" step="5"', 'id="camOpacitySlider" type="range" min="0" max="100" step="5"')
s=s.replace(".cam-opacity input{display:block;width:100%;height:38px;accent-color:#0a84ff;pointer-events:auto;touch-action:pan-x}", ".cam-opacity input{display:block;width:100%;height:44px;accent-color:#0a84ff;pointer-events:auto;touch-action:pan-x;-webkit-appearance:none;appearance:none;background:transparent}\n  .cam-opacity input::-webkit-slider-runnable-track{height:7px;border-radius:999px;background:rgba(28,28,30,.18)}\n  .cam-opacity input::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:30px;height:30px;border-radius:50%;background:#0a84ff;border:3px solid #fff;box-shadow:0 1px 5px rgba(0,0,0,.28);margin-top:-11.5px}")
# Fix zero being coerced back to 40.
s=s.replace("camOpacityValue=parseInt(e.target.value,10)||40;", "camOpacityValue=parseInt(e.target.value,10);if(!Number.isFinite(camOpacityValue))camOpacityValue=40;")
p.write_text(s)