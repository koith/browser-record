from pathlib import Path
p=Path("silent-camera-safari.html");s=p.read_text()
needle="camOpacity.addEventListener('click',e=>e.stopPropagation());"
insert="""camOpacity.addEventListener('click',e=>e.stopPropagation());
// Tap anywhere outside the external opacity panel: persist the current value and close it.
document.addEventListener('pointerdown',e=>{
  if(!camOpacity.classList.contains('open'))return;
  if(camOpacity.contains(e.target))return;
  localStorage.setItem('camOpacity',String(camOpacityValue));
  camOpacity.classList.remove('open');
},{capture:true});"""
if needle not in s: raise SystemExit("opacity click listener not found")
s=s.replace(needle,insert,1)
p.write_text(s)