const {chromium}=require('playwright');const path=require('node:path');const appPath=path.resolve(__dirname,'../silent-camera-safari.html');const fs=require('fs');const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream']});
 const context=await browser.newContext({permissions:['camera','microphone']});const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.route('https://memo.test/**',r=>r.fulfill({path:appPath,contentType:'text/html'}));
 await page.route(/https:\/\/(?!memo.test)/,r=>r.abort());
 await page.goto('https://memo.test/');
 await page.evaluate(()=>new Promise((resolve,reject)=>{
  const request=indexedDB.open('memoDB',2);
  request.onupgradeneeded=()=>{request.result.createObjectStore('notes',{keyPath:'id'});request.result.createObjectStore('folders',{keyPath:'id'});};
  request.onsuccess=()=>{const old=request.result,tx=old.transaction(['notes','folders'],'readwrite');tx.objectStore('folders').put({id:'legacy-folder',name:'기존 폴더',order:0});tx.objectStore('notes').put({id:'legacy-note',title:'기존 메모',text:'보존 확인',folderId:'legacy-folder',media:[]});tx.oncomplete=()=>{old.close();resolve();};tx.onerror=()=>reject(tx.error);};request.onerror=()=>reject(request.error);
 }));
 await page.fill('#loginPw','1128');await page.click('#loginBtn');await page.waitForFunction(()=>db&&folders.length>0&&!document.body.classList.contains('locked'));
 assert.equal(await page.evaluate(()=>db.version===3&&notes.some(n=>n.id==='legacy-note'&&n.text==='보존 확인')),true);
 // A transaction error must reject a write, not falsely report success.
 assert.equal(await page.evaluate(async()=>{
   const tx=db.transaction(NOTES,'readwrite'),done=new Promise(r=>{tx.onabort=()=>r(true)});tx.objectStore(NOTES).put({id:'aborted'});tx.abort();await done;
   return !(await getAll(NOTES)).some(n=>n.id==='aborted');
 }),true);
 await page.evaluate(()=>{setMemoOverlay(true);showNotes();openEditor(null)});
 await page.fill('#edTitle','자동 저장 검증');await page.fill('#edText','입력한 내용 보존');
 for(let i=0;i<30;i++){if(await page.evaluate(async()=> (await getAll(NOTES)).some(n=>n.title==='자동 저장 검증'&&n.text==='입력한 내용 보존')))break;await page.waitForTimeout(100);}
 assert.equal(await page.evaluate(async()=> (await getAll(NOTES)).some(n=>n.text==='입력한 내용 보존')),true);
 const noteId=await page.evaluate(()=>current.id);
 // Real fake-device recording: leaving the editor must await final data and disk writes.
 await page.evaluate(()=>openCamera());await page.waitForFunction(()=>stream&&document.getElementById('preview').videoWidth>0);
 await page.evaluate(()=>toggleRec());for(let i=0;i<150;i++){if(await page.evaluate(async()=> (await getAll(CAPTURE_CHUNKS)).length>0))break;await page.waitForTimeout(100);}
 assert.equal(await page.evaluate(async()=> (await getAll(CAPTURE_CHUNKS)).length>0),true);
 await page.evaluate(()=>returnToNoteList());
 await page.waitForFunction(()=>current===null);
 assert.equal(await page.evaluate(async id=>{const n=(await getAll(NOTES)).find(n=>n.id===id);return n.media.length===1&&n.media[0].blob.size>0&&n.text==='입력한 내용 보존'},noteId),true);
 assert.equal(await page.evaluate(async()=> (await getAll(CAPTURE_CHUNKS)).length),0);
 // Audio finalization belongs to the original note even if another editor opens.
 await page.evaluate(id=>{openEditor(notes.find(n=>n.id===id));return startAudio()},noteId);
 await page.waitForTimeout(1100);
 await page.evaluate(()=>{audioRec.stop();openEditor({id:'other',title:'다른 메모',text:'',media:[],folderId:currentFolderId});return audioFinish});
 assert.equal(await page.evaluate(id=>notes.find(n=>n.id===id).media.filter(m=>m.kind==='audio').length,noteId),1);
 assert.equal(await page.evaluate(()=>current.media.length),0);
 // A late camera permission result cannot revive a closed camera or leak tracks.
 assert.equal(await page.evaluate(async()=>{
   const original=navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices);let resolve;
   const track={stopped:false,stop(){this.stopped=true}},pending=new Promise(r=>resolve=r);
   navigator.mediaDevices.getUserMedia=()=>pending;
   cam.classList.add('open');const request=startStream(true);closeCamera();resolve({getTracks:()=>[track]});await request;
   navigator.mediaDevices.getUserMedia=original;return track.stopped&&stream===null;
 }),true);
 // Thumbnail URLs must return to a fixed count after many redraws.
 assert.equal(await page.evaluate(async()=>{
  let created=0,revoked=0;const create=URL.createObjectURL.bind(URL),revoke=URL.revokeObjectURL.bind(URL);
  URL.createObjectURL=b=>{created++;return create(b)};URL.revokeObjectURL=u=>{revoked++;revoke(u)};
  const photo=new Blob([new Uint8Array([1,2,3])],{type:'image/jpeg'});current.media=[{kind:'photo',blob:photo}];
  for(let i=0;i<50;i++)renderEditorMedia();await new Promise(r=>setTimeout(r,20));
  $('edMedia').innerHTML='';await new Promise(r=>setTimeout(r,20));
  URL.createObjectURL=create;URL.revokeObjectURL=revoke;return created===revoked;
 }),true);
 // Legacy backup stays parseable, exact binary bytes survive chunk boundaries.
 assert.equal(await page.evaluate(async()=>{
  const bytes=new Uint8Array(500003);for(let i=0;i<bytes.length;i++)bytes[i]=i%251;
  const blob=new Blob([bytes],{type:'video/mp4'});const n={id:'backup-test',title:'따옴표 "와 한글',text:'본문',folderId:currentFolderId,media:[{kind:'video',blob,duration:12.5}]};
  notes=[n];const result=JSON.parse(await (await buildBackupBlob()).text());
  const restored=new Uint8Array(await dataURLToBlob(result.notes[0].media[0].blob).arrayBuffer());
  return restored.every((b,i)=>b===bytes[i])&&restored.length===bytes.length&&result.notes[0].media[0].duration===12.5;
 }),true);
 // Persisted interrupted recording recovers once, then removes temporary data.
 await page.evaluate(async()=>{
  const n={id:'recovery',title:'복구',text:'',media:[],folderId:currentFolderId};await put(NOTES,n);
  await put(CAPTURE_SESSIONS,{id:'recover-session',noteId:n.id,kind:'video',type:'video/mp4',started:Date.now()});
  await put(CAPTURE_CHUNKS,{id:'recover-session:0000000000',blob:new Blob(['recover-bytes']),capturedAt:Date.now()});
 });
 await page.reload();await page.fill('#loginPw','1128');await page.click('#loginBtn');await page.waitForFunction(()=>db&&notes.some(n=>n.id==='recovery'&&n.media.length===1));
 assert.equal(await page.evaluate(async()=> (await getAll(CAPTURE_SESSIONS)).length),0);
 assert.equal(await page.evaluate(async()=> (await getAll(CAPTURE_CHUNKS)).length),0);
 assert.equal(await page.evaluate(async()=>{await recoverCaptures();return notes.find(n=>n.id==='recovery').media.length}),1);
 assert.deepEqual(errors,[]);await browser.close();console.log('PASS: autosave, real video/audio capture, chunk persistence/recovery, navigation races, late permissions, 50 thumbnail redraws, chunked backup round-trip');
})().catch(e=>{console.error(e);process.exit(1)});
