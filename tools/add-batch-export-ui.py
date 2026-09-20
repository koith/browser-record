from pathlib import Path
p=Path("silent-camera-safari.html")
s=p.read_text(encoding="utf-8")
s=s.replace(".sort-btn { flex:0 0 auto; border:none; background:var(--chip); color:var(--accent); font-size:14px; font-weight:600; padding:8px 12px; border-radius:10px; white-space:nowrap; }", """.sort-btn { flex:0 0 auto; border:none; background:var(--chip); color:var(--accent); font-size:14px; font-weight:600; padding:8px 12px; border-radius:10px; white-space:nowrap; }
  .select-btn { flex:0 0 auto; border:none; background:var(--chip); color:var(--blue); font-size:14px; font-weight:600; padding:8px 12px; border-radius:10px; white-space:nowrap; }
  .note-select { display:none; width:24px; height:24px; border:2px solid var(--sub); border-radius:50%; flex:0 0 auto; align-items:center; justify-content:center; color:#fff; font-size:14px; font-weight:800; }
  body.note-select-mode .note-select { display:flex; }
  body.note-select-mode .note-card { display:flex; gap:12px; align-items:flex-start; }
  body.note-select-mode .note-select.checked { background:var(--blue); border-color:var(--blue); }
  .note-main { min-width:0; flex:1; }
  .selection-bar { position:absolute; left:10px; right:10px; bottom:calc(8px + env(safe-area-inset-bottom)); z-index:45; display:none; align-items:center; gap:8px; padding:10px; border-radius:16px; background:var(--panel); box-shadow:0 6px 24px rgba(0,0,0,.22); border:.5px solid var(--border); }
  .selection-bar.open { display:flex; }
  .selection-bar .sel-count { flex:1; font-size:14px; font-weight:600; padding-left:6px; }
  .selection-bar button { border:none; border-radius:10px; padding:10px 12px; font-size:14px; font-weight:600; background:var(--chip); color:var(--blue); }
  .selection-bar button:disabled { opacity:.4; }""")
s=s.replace(".ed-attach-label { font-size:12px; font-weight:600; color:var(--sub); letter-spacing:.03em; text-transform:uppercase; margin-bottom:8px; }", ".ed-attach-label { font-size:12px; font-weight:600; color:var(--sub); letter-spacing:.03em; text-transform:uppercase; margin-bottom:8px; display:flex; align-items:center; justify-content:space-between; gap:10px; }\n  .attach-export { border:none; background:var(--chip); color:var(--blue); border-radius:8px; padding:6px 9px; font-size:12px; font-weight:700; text-transform:none; touch-action:manipulation; }")
s=s.replace('<button class="sort-btn" id="sortBtn">정렬 ▾</button>', '<button class="sort-btn" id="sortBtn">정렬 ▾</button>\n    <button class="select-btn" id="selectBtn">선택</button>')
s=s.replace('<div class="ed-attach-label" id="edAttachLabel">첨부</div>', '<div class="ed-attach-label" id="edAttachLabel"><span>첨부</span><button class="attach-export" id="edExport" type="button">내보내기 ↗</button></div>')
s=s.replace('<div class="toast" id="toast"></div>', '<div class="selection-bar" id="selectionBar"><div class="sel-count" id="selectionCount">0개 선택</div><button id="selectionAll" type="button">전체 선택</button><button id="selectionExport" type="button" disabled>첨부 내보내기</button><button id="selectionCancel" type="button">취소</button></div>\n    <div class="toast" id="toast"></div>')
s=s.replace("let searchQuery='';", "let searchQuery='';\nlet noteSelectMode=false; const selectedNoteIds=new Set();")
s=s.replace("view='notes'; closeEditor(true);", "view='notes'; closeEditor(true);\n  exitNoteSelection(false);",1)
s=s.replace("$('subbar').classList.remove('hidden'); $('sortBtn').style.display='block';", "$('subbar').classList.remove('hidden'); $('sortBtn').style.display='block'; $('selectBtn').style.display='block';",1)
s=s.replace("$('subbar').classList.remove('hidden'); $('sortBtn').style.display='none';", "$('subbar').classList.remove('hidden'); $('sortBtn').style.display='none'; $('selectBtn').style.display='none';",1)
old="""'<div class="swipe-content"><div class="note-card">'+
        '<div class="nc-title">'+(n.title||'(제목 없음)')+'</div>'+"""
new="""'<div class="swipe-content"><div class="note-card">'+
        '<span class="note-select'+(selectedNoteIds.has(n.id)?' checked':'')+'" data-id="'+n.id+'">'+(selectedNoteIds.has(n.id)?'✓':'')+'</span>'+
        '<div class="note-main"><div class="nc-title">'+(n.title||'(제목 없음)')+'</div>'+"""
s=s.replace(old,new,1)
s=s.replace("""((n.media&&n.media.length)?'<span>📎 '+n.media.length+'</span>':'')+'</div>'+
      '</div></div>';""","""((n.media&&n.media.length)?'<span>📎 '+n.media.length+'</span>':'')+'</div></div>'+
      '</div></div>';""",1)
s=s.replace("content.addEventListener('click',e=>{ if(content.style.transform&&content.style.transform!=='translateX(0px)'&&content.style.transform!==''){ closeAllRows(); return; } openEditor(n); });", """content.addEventListener('click',e=>{ if(noteSelectMode){e.preventDefault();toggleNoteSelection(n.id);return;} if(content.style.transform&&content.style.transform!=='translateX(0px)'&&content.style.transform!==''){ closeAllRows(); return; } openEditor(n); });""",1)
sel=r'''
function visibleNotesForSelection(){ let a=notes.filter(n=>n.folderId===currentFolderId); if(searchQuery){const q=searchQuery.toLowerCase();a=a.filter(n=>((n.title||'')+' '+(n.text||'')).toLowerCase().includes(q));} return sortNotes(a); }
function updateSelectionBar(){ const c=selectedNoteIds.size; $('selectionCount').textContent=c+'개 선택'; $('selectionExport').disabled=c===0||!notes.some(n=>selectedNoteIds.has(n.id)&&(n.media||[]).length); const v=visibleNotesForSelection(); $('selectionAll').textContent=v.length&&v.every(n=>selectedNoteIds.has(n.id))?'전체 해제':'전체 선택'; }
function enterNoteSelection(){ if(view!=='notes')return; noteSelectMode=true;selectedNoteIds.clear();document.body.classList.add('note-select-mode');$('selectionBar').classList.add('open');$('selectBtn').textContent='선택 중';closeAllRows();renderNotes();updateSelectionBar(); }
function exitNoteSelection(rerender=true){ noteSelectMode=false;selectedNoteIds.clear();document.body.classList.remove('note-select-mode');const b=$('selectionBar');if(b)b.classList.remove('open');const s=$('selectBtn');if(s)s.textContent='선택';if(rerender&&view==='notes')renderNotes(); }
function toggleNoteSelection(id){ selectedNoteIds.has(id)?selectedNoteIds.delete(id):selectedNoteIds.add(id);renderNotes();updateSelectionBar(); }
$('selectBtn').addEventListener('click',()=>noteSelectMode?exitNoteSelection():enterNoteSelection());
$('selectionCancel').addEventListener('click',()=>exitNoteSelection());
$('selectionAll').addEventListener('click',()=>{const v=visibleNotesForSelection(),all=v.length&&v.every(n=>selectedNoteIds.has(n.id));v.forEach(n=>all?selectedNoteIds.delete(n.id):selectedNoteIds.add(n.id));renderNotes();updateSelectionBar();});
'''
s=s.replace("/* ===== FOLDER LIST ===== */",sel+"\n/* ===== FOLDER LIST ===== */",1)
s=s.replace("$('edAttachLabel').style.display=any?'block':'none';", "$('edAttachLabel').style.display=any?'flex':'none';\n  $('edExport').style.display=hasMedia?'block':'none';",1)
p.write_text(s,encoding="utf-8")
print("patched ui")
