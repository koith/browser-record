from pathlib import Path
p=Path("silent-camera-safari.html");s=p.read_text()
old=".cam { position:absolute; right:12px; bottom:calc(150px + var(--kb,0px) + env(safe-area-inset-bottom)); width:88px; height:118px; background:#000; display:none; flex-direction:column; z-index:30; border-radius:14px; overflow:hidden; box-shadow:0 6px 20px rgba(0,0,0,.35); border:1.5px solid rgba(255,255,255,.85); opacity:.4; touch-action:none; }"
new=".cam { position:absolute; right:12px; bottom:calc(150px + var(--kb,0px) + env(safe-area-inset-bottom)); width:88px; height:118px; background:transparent; display:none; flex-direction:column; z-index:30; border-radius:14px; overflow:hidden; box-shadow:0 6px 20px rgba(0,0,0,.35); border:1.5px solid rgba(255,255,255,.85); opacity:1; touch-action:none; }"
if old not in s: raise SystemExit("cam css not found")
s=s.replace(old,new,1)
# Ensure the preview itself has a transparent backing; low opacity should reveal webpage, not black camera container.
s=s.replace(".cam video { flex:1; width:100%; height:100%; object-fit:cover; }",".cam video { flex:1; width:100%; height:100%; object-fit:cover; background:transparent; }",1)
p.write_text(s)