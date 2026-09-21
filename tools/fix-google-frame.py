from pathlib import Path
p=Path("silent-camera-safari.html");s=p.read_text()
old="""$('browserFrame').addEventListener('load',()=>{
  persistBrowserURL();
  clearInterval(browserPersistTimer);
  browserPersistTimer=setInterval(()=>persistBrowserURL(),1200);
});
window.addEventListener('pagehide',()=>persistBrowserURL());
document.addEventListener('visibilitychange',()=>{if(document.hidden)persistBrowserURL();});"""
new="""// Cross-origin iframe locations (Google and most external sites) are intentionally
// unreadable from the parent page. Do not poll contentWindow.location: on iOS Safari
// this can destabilize otherwise frameable pages. We persist only URLs the shell knows.
$('browserFrame').addEventListener('load',()=>{ localStorage.setItem('browserLastURL',browserURL); });
window.addEventListener('pagehide',()=>localStorage.setItem('browserLastURL',browserURL));
document.addEventListener('visibilitychange',()=>{if(document.hidden)localStorage.setItem('browserLastURL',browserURL);});"""
if old not in s: raise SystemExit("persistence block not found")
s=s.replace(old,new)
p.write_text(s)
