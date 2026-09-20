from pathlib import Path
p=Path("silent-camera-safari.html")
s=p.read_text()
s=s.replace(".ed-media .m .rm { position:absolute;", """.ed-media .m .pick { display:none; position:absolute; left:3px; top:3px; width:20px; height:20px; border-radius:50%; border:2px solid #fff; background:rgba(0,0,0,.45); color:#fff; z-index:4; align-items:center; justify-content:center; font-size:12px; font-weight:800; }
  .ed-media.media-select-mode .m .pick { display:flex; }
  .ed-media .m.picked .pick { background:var(--blue); }
  .ed-media.media-select-mode .m .rm { display:none; }
  .media-select-bar { display:none; align-items:center; gap:8px; margin:8px 0 0; }
  .media-select-bar.open { display:flex; }
  .media-select-bar span { flex:1; font-size:12px; color:var(--sub); }
  .media-select-bar button { border:none; background:var(--chip); color:var(--blue); border-radius:8px; padding:7px 9px; font-size:12px; font-weight:700; }
  .ed-media .m .rm { position:absolute;""")
s=s.replace('<div class="ed-media" id="edMedia"></div>', '<div class="ed-media" id="edMedia"></div><div class="media-select-bar" id="mediaSelectBar"><span id="mediaSelectCount">0개 선택</span><button id="mediaSelectAll" type="button">전체 선택</button><button id="mediaSelectExport" type="button">내보내기</button><button id="mediaSelectCancel" type="button">취소</button></div>')
s=s.replace("let noteSelectMode=false; const selectedNoteIds=new Set();", "let noteSelectMode=false; const selectedNoteIds=new Set();\nlet mediaSelectMode=false; const selectedMediaIndexes=new Set();")
s=s.replace("function closeEditor(silent){\n  closeCamera();", "function closeEditor(silent){\n  exitMediaSelection(); closeCamera();")
s=s.replace("function renderEditorMedia(){\n  const wrap=$('edMedia'); wrap.innerHTML='';", "function renderEditorMedia(){\n  const wrap=$('edMedia'); wrap.innerHTML='';")
s=s.replace("const el=document.createElement('div'); el.className='m'+(m.kind==='audio'?' audio':'');", "const el=document.createElement('div'); el.className='m'+(m.kind==='audio'?' audio':'')+(selectedMediaIndexes.has(i)?' picked':'');\n    const pick=document.createElement('span'); pick.className='pick'; pick.textContent=selectedMediaIndexes.has(i)?'✓':''; el.appendChild(pick);")
s=s.replace("el.addEventListener('click',e=>{ if(e.target.classList.contains('rm'))return; openViewer(i); });", "el.addEventListener('click',e=>{ if(e.target.classList.contains('rm'))return; if(mediaSelectMode){e.preventDefault();toggleMediaSelection(i);return;} openViewer(i); });")
s=s.replace("  updateAttachVisibility();\n}\nfunction updateAttachVisibility()", "  wrap.classList.toggle('media-select-mode',mediaSelectMode); updateMediaSelectionBar();\n  updateAttachVisibility();\n}\nfunction updateAttachVisibility()")
s=s.replace("$('edExport').addEventListener('click',e=>{e.preventDefault();e.stopPropagation();if(current)openBatchExportSheet([current]);});", """function updateMediaSelectionBar(){const bar=$('mediaSelectBar');if(!bar)return;bar.classList.toggle('open',mediaSelectMode);$('mediaSelectCount').textContent=selectedMediaIndexes.size+'개 선택';$('mediaSelectExport').disabled=!selectedMediaIndexes.size;$('mediaSelectAll').textContent=current&&current.media&&selectedMediaIndexes.size===current.media.length?'전체 해제':'전체 선택';}
function enterMediaSelection(){if(!current||!current.media||!current.media.length)return;mediaSelectMode=true;selectedMediaIndexes.clear();renderEditorMedia();}
function exitMediaSelection(){mediaSelectMode=false;selectedMediaIndexes.clear();const w=$('edMedia');if(w)w.classList.remove('media-select-mode');const b=$('mediaSelectBar');if(b)b.classList.remove('open');}
function toggleMediaSelection(i){selectedMediaIndexes.has(i)?selectedMediaIndexes.delete(i):selectedMediaIndexes.add(i);renderEditorMedia();}
function selectedMediaPseudoNote(){return {title:current&&current.title||'메모',media:(current&&current.media||[]).filter((m,i)=>selectedMediaIndexes.has(i))};}
$('edExport').addEventListener('click',e=>{e.preventDefault();e.stopPropagation();if(!current)return;if((current.media||[]).length>1){enterMediaSelection();showToast('내보낼 첨부파일을 선택하세요');}else openBatchExportSheet([current]);});
$('mediaSelectCancel').addEventListener('click',()=>{exitMediaSelection();renderEditorMedia();});
$('mediaSelectAll').addEventListener('click',()=>{if(!current)return;if(selectedMediaIndexes.size===current.media.length)selectedMediaIndexes.clear();else current.media.forEach((m,i)=>selectedMediaIndexes.add(i));renderEditorMedia();});
$('mediaSelectExport').addEventListener('click',()=>{if(!selectedMediaIndexes.size)return;openBatchExportSheet([selectedMediaPseudoNote()]);});""")
p.write_text(s)
