from pathlib import Path
p=Path("silent-camera-safari.html");s=p.read_text()
old='<div class="login-sub">간편 비밀번호를 입력해 주세요</div>'
new='<div class="login-sub" id="loginVersion">v0.1</div>'
if old not in s: raise SystemExit("login sub missing")
s=s.replace(old,new,1)
# Keep a single explicit app version constant so future revisions can bump one place.
marker="/* ===== IndexedDB (v2: notes + folders) ===== */"
s=s.replace(marker,"const APP_VERSION='v0.1';\nconst loginVersionEl=document.getElementById('loginVersion');if(loginVersionEl)loginVersionEl.textContent=APP_VERSION;\n\n"+marker,1)
p.write_text(s)