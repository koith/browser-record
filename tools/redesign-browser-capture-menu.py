from pathlib import Path
p=Path("silent-camera-safari.html");s=p.read_text()

# CSS: replace old single FAB semantics with radial capture menu + mode toggle.
s=s.replace("body.memo-open .memo-fab{display:none}", """body.memo-open .memo-fab{display:none}
.radial-action{position:fixed;right:20px;bottom:calc(22px + env(safe-area-inset-bottom));z-index:19;width:48px;height:48px;border:0;border-radius:50%;background:rgba(255,255,255,.88);box-shadow:0 5px 18px rgba(0,0,0,.22);font-size:21px;display:flex;align-items:center;justify-content:center;opacity:0;transform:translate(0,0) scale(.65);pointer-events:none;transition:transform .18s ease,opacity .15s ease;-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);touch-action:manipulation}
.radial-menu.open .radial-action{opacity:1;pointer-events:auto}
.radial-menu.open #radialCamera{transform:translate(-66px,-6px) scale(1)}
.radial-menu.open #radialAudio{transform:translate(-48px,-62px) scale(1)}
.radial-menu{position:fixed;right:0;bottom:0;z-index:18}
.mode-toggle{min-width:74px!important;padding:0 8px!important;font-size:12px!important;font-weight:700}
.mode-toggle .mode-web,.mode-toggle.memo .mode-memo{color:#0a84ff}
.mode-toggle.memo .mode-web{color:#8e8e93}
""",1)

# HTML browser bar: replace Go with mode toggle; enter still navigates, add compact go icon if desired through address enter.
s=s.replace('<button id="brGo">이동</button>', '<button id="modeToggle" class="mode-toggle" type="button"><span class="mode-web">웹</span> / <span class="mode-memo">메모</span></button>',1)
s=s.replace('<button class="memo-fab" id="memoFab" aria-label="메모 열기">📝</button>', '''<div class="radial-menu" id="radialMenu">
    <button class="radial-action" id="radialCamera" type="button" aria-label="카메라">📷</button>
    <button class="radial-action" id="radialAudio" type="button" aria-label="녹음">🎙️</button>
    <button class="memo-fab" id="memoFab" type="button" aria-label="촬영 메뉴">＋</button>
  </div>''',1)

# JS browser handlers: remove brGo dependency, add radial/menu mode.
s=s.replace("$('memoFab').addEventListener('click',()=>setMemoOverlay(true));", """function closeRadialMenu(){ $('radialMenu').classList.remove('open'); }
function toggleRadialMenu(){ $('radialMenu').classList.toggle('open'); }
$('memoFab').addEventListener('click',e=>{e.preventDefault();e.stopPropagation();toggleRadialMenu();});
$('radialMenu').addEventListener('click',e=>e.stopPropagation());
document.addEventListener('pointerdown',e=>{if($('radialMenu').classList.contains('open')&&!$('radialMenu').contains(e.target))closeRadialMenu();},{capture:true});
$('radialCamera').addEventListener('click',async e=>{e.preventDefault();e.stopPropagation();closeRadialMenu();if(!cam.classList.contains('open'))await openCamera();});
$('radialAudio').addEventListener('click',e=>{e.preventDefault();e.stopPropagation();closeRadialMenu();if(audioRec&&audioRec.state==='recording')audioRec.stop();else startAudio();});
function syncModeToggle(){
  const memo=document.body.classList.contains('memo-open');
  $('modeToggle').classList.toggle('memo',memo);
  $('modeToggle').setAttribute('aria-label',memo?'웹 모드로 전환':'메모 모드로 전환');
}
$('modeToggle').addEventListener('click',()=>{
  const memo=document.body.classList.contains('memo-open');
  if(memo){if(current&&editor.classList.contains('open'))saveCurrent();setMemoOverlay(false);}
  else setMemoOverlay(true);
  closeRadialMenu();syncModeToggle();
});
syncModeToggle();""",1)
s=s.replace("$('brGo').addEventListener('click',()=>browserNavigate($('brAddress').value));\n","",1)
# old memo close should sync toggle
s=s.replace("setMemoOverlay(false); });","setMemoOverlay(false); syncModeToggle(); });",1)

p.write_text(s)