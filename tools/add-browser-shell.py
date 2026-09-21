from pathlib import Path
p=Path("silent-camera-safari.html")
s=p.read_text()
css=r'''
  /* Browser-first shell (v1). Existing memo app becomes an on-demand overlay. */
  .browser-shell{position:fixed;inset:0;z-index:0;background:#fff;display:flex;flex-direction:column}
  .browser-bar{flex:0 0 auto;padding:calc(7px + env(safe-area-inset-top)) 8px 7px;display:flex;gap:6px;align-items:center;background:#f5f5f7;border-bottom:.5px solid #d7d7dc}
  .browser-bar button{border:0;background:#e5e5ea;border-radius:9px;min-width:36px;height:36px;font-size:16px;color:#111;padding:0 9px}
  .browser-address{flex:1;min-width:0;height:36px;border:0;border-radius:10px;background:#fff;padding:0 11px;font-size:15px;outline:none;color:#111}
  .browser-stage{position:relative;flex:1;min-height:0;background:#fff}
  #browserFrame{width:100%;height:100%;border:0;background:#fff}
  .browser-help{position:absolute;left:10px;right:10px;bottom:10px;padding:8px 10px;border-radius:10px;background:rgba(20,20,20,.72);color:#fff;font-size:11px;line-height:1.35;pointer-events:none;opacity:0;transition:.2s}
  .browser-help.show{opacity:1}
  .memo-fab{position:fixed;right:14px;bottom:calc(16px + env(safe-area-inset-bottom));z-index:18;width:52px;height:52px;border:0;border-radius:50%;background:#1c1c1e;color:#fff;font-size:23px;box-shadow:0 5px 18px rgba(0,0,0,.28);touch-action:manipulation}
  body.memo-open .memo-fab{display:none}
  body.browser-home:not(.memo-open)>.header,body.browser-home:not(.memo-open)>.subbar,body.browser-home:not(.memo-open)>.toolbar{display:none!important}
  body.browser-home:not(.memo-open)>.main{position:fixed;inset:0;z-index:20;pointer-events:none;background:transparent}
  body.browser-home:not(.memo-open)>.main>.list,
  body.browser-home:not(.memo-open)>.main>.editor,
  body.browser-home:not(.memo-open)>.main>.settings,
  body.browser-home:not(.memo-open)>.main>.selection-bar{display:none!important}
  body.browser-home:not(.memo-open)>.main>.cam,
  body.browser-home:not(.memo-open)>.main>.cap-dock,
  body.browser-home:not(.memo-open)>.main>.zoom-menu,
  body.browser-home:not(.memo-open)>.main>.viewer,
  body.browser-home:not(.memo-open)>.main>.sheet-bg,
  body.browser-home:not(.memo-open)>.main>.toast{pointer-events:auto}
  body.memo-open>.header,body.memo-open>.subbar,body.memo-open>.main,body.memo-open>.toolbar{position:relative;z-index:25}
  body.memo-open>.header,body.memo-open>.subbar,body.memo-open>.toolbar{background:var(--panel)}
  body.memo-open>.main{background:var(--bg)}
  .memo-browser-close{border:none;background:var(--chip);color:var(--blue);font-size:14px;font-weight:700;padding:7px 10px;border-radius:10px}
'''
s=s.replace('</style>',css+'\n</style>')
browser=r'''
  <div class="browser-shell" id="browserShell">
    <div class="browser-bar">
      <button id="brBack" aria-label="뒤로">‹</button>
      <button id="brForward" aria-label="앞으로">›</button>
      <button id="brReload" aria-label="새로고침">↻</button>
      <input class="browser-address" id="brAddress" type="text" inputmode="url" autocapitalize="off" autocomplete="off" spellcheck="false" placeholder="검색 또는 주소 입력">
      <button id="brGo">이동</button>
      <button id="brExternal" aria-label="Safari에서 열기">↗</button>
    </div>
    <div class="browser-stage">
      <iframe id="browserFrame" title="웹 브라우저" referrerpolicy="strict-origin-when-cross-origin"></iframe>
      <div class="browser-help" id="browserHelp">페이지가 표시되지 않으면 우측 ↗ 버튼으로 Safari에서 여세요.</div>
    </div>
  </div>
  <button class="memo-fab" id="memoFab" aria-label="메모 열기">📝</button>
'''
s=s.replace('<body class="locked">','<body class="locked browser-home">\n'+browser)
s=s.replace('<div class="h-right">\n      <div class="count"', '<div class="h-right">\n      <button class="memo-browser-close" id="memoBrowserClose">웹으로</button>\n      <div class="count"')
js=r'''
/* ===== Browser-first shell ===== */
const BR_HOME='https://www.google.com/webhp?igu=1';
let browserURL=localStorage.getItem('browserLastURL')||BR_HOME;
function normalizeBrowserInput(raw){
  const v=(raw||'').trim();
  if(!v)return browserURL||BR_HOME;
  if(/^https?:\/\//i.test(v))return v;
  if(/^([a-z0-9-]+\.)+[a-z]{2,}(\/|$)/i.test(v))return 'https://'+v;
  return 'https://www.google.com/search?igu=1&q='+encodeURIComponent(v);
}
function browserNavigate(raw){
  browserURL=normalizeBrowserInput(raw);
  localStorage.setItem('browserLastURL',browserURL);
  $('brAddress').value=browserURL;
  $('browserFrame').src=browserURL;
  const h=$('browserHelp');h.classList.add('show');clearTimeout(h._t);h._t=setTimeout(()=>h.classList.remove('show'),3500);
}
function setMemoOverlay(open){
  document.body.classList.toggle('memo-open',!!open);
  if(open){ if(typeof renderNotes==='function'&&view==='notes')renderNotes(); }
}
$('memoFab').addEventListener('click',()=>setMemoOverlay(true));
$('memoBrowserClose').addEventListener('click',()=>{ if(current&&editor.classList.contains('open')) saveCurrent(); setMemoOverlay(false); });
$('brGo').addEventListener('click',()=>browserNavigate($('brAddress').value));
$('brAddress').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();browserNavigate(e.target.value);e.target.blur();}});
$('brReload').addEventListener('click',()=>{try{$('browserFrame').src=browserURL;}catch(e){}});
$('brExternal').addEventListener('click',()=>{window.open(browserURL,'_blank');});
$('brBack').addEventListener('click',()=>{try{$('browserFrame').contentWindow.history.back();}catch(e){showToast('이 페이지에서는 뒤로가기를 사용할 수 없습니다');}});
$('brForward').addEventListener('click',()=>{try{$('browserFrame').contentWindow.history.forward();}catch(e){showToast('이 페이지에서는 앞으로가기를 사용할 수 없습니다');}});
$('brAddress').value=browserURL;
$('browserFrame').src=browserURL;
'''
s=s.replace("/* ===== bootstrap ===== */",js+"\n/* ===== bootstrap ===== */")
# Camera should float over browser once started, while keeping its target memo alive.
s=s.replace("async function openCamera(){\n  if(!current)openEditor(null);", "async function openCamera(){\n  if(!current)openEditor(null);\n  setMemoOverlay(false);")
p.write_text(s)
