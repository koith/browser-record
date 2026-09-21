from pathlib import Path
p=Path("silent-camera-safari.html"); s=p.read_text()
# Login branding + blue/black theme
s=s.replace('<title>기록 메모</title>','<title>메모 브라우저</title>')
s=s.replace('<div class="login-brand">기록 메모</div>','<div class="login-brand">메모 브라우저</div>')
s=s.replace('background:linear-gradient(180deg,#f4f7fb 0%,#e9eef6 100%)','background:linear-gradient(160deg,#05070b 0%,#0a1220 58%,#0b2d5c 100%)')
s=s.replace('background:#ffffff; padding:34px 26px 26px; border-radius:22px; box-shadow:0 18px 50px rgba(30,58,110,.14), 0 2px 8px rgba(30,58,110,.06);','background:#0d1118; padding:34px 26px 26px; border:1px solid #17263d; border-radius:22px; box-shadow:0 18px 50px rgba(0,0,0,.5), 0 0 32px rgba(47,111,237,.12);')
s=s.replace('color:#16233a; text-align:center;','color:#f4f8ff; text-align:center;',1)
s=s.replace('color:#7a8699; text-align:center;','color:#8fa5c4; text-align:center;')
s=s.replace('border:1.5px solid #dbe2ec; background:#f7f9fc; color:#16233a;','border:1.5px solid #243b5e; background:#080c12; color:#f4f8ff;')
s=s.replace('color:#aab4c4; letter-spacing:.02em;','color:#7186a3; letter-spacing:.02em;')
s=s.replace('border-color:#2f6fed; background:#fff;','border-color:#2f80ff; background:#0b1018;')
s=s.replace('background:#2f6fed; color:#fff;','background:linear-gradient(135deg,#1478ff,#0755c9); color:#fff;')
s=s.replace('background:#1e4fc4; transform:scale(.99);','background:#0647aa; transform:scale(.99);')
s=s.replace('color:#9aa5b5; text-align:center;','color:#60738f; text-align:center;')

# Improve persistence: save iframe-observable URLs, hash route changes, and restore last known.
needle="$('browserFrame').src=browserURL;"
replacement="""$('browserFrame').src=browserURL;
let browserPersistTimer=null;
function persistBrowserURL(candidate){
  try{
    const u=candidate||$('browserFrame').contentWindow.location.href;
    if(u&&/^https?:\\/\\//i.test(u)){
      browserURL=u; localStorage.setItem('browserLastURL',u); $('brAddress').value=u;
    }
  }catch(e){}
}
$('browserFrame').addEventListener('load',()=>{
  persistBrowserURL();
  clearInterval(browserPersistTimer);
  browserPersistTimer=setInterval(()=>persistBrowserURL(),1200);
});
window.addEventListener('pagehide',()=>persistBrowserURL());
document.addEventListener('visibilitychange',()=>{if(document.hidden)persistBrowserURL();});"""
# only final initialization occurrence, not browserNavigate assignment
idx=s.rfind(needle)
if idx<0: raise SystemExit('browser init needle not found')
s=s[:idx]+replacement+s[idx+len(needle):]
p.write_text(s)
