const {chromium}=require('playwright');const path=require('node:path');const appPath=path.resolve(__dirname,'../silent-camera-safari.html');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox']});
 const page=await browser.newPage({acceptDownloads:true});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.route('https://memo.test/**',r=>r.fulfill({path:appPath,contentType:'text/html'}));
 await page.goto('https://memo.test/');
 await page.fill('#loginPw','1128');await page.click('#loginBtn');
 await page.waitForFunction(()=>typeof db!=='undefined'&&db&&folders.length>0);
 await page.evaluate(()=>{
   window.shareCalls=[];
   Object.defineProperty(navigator,'canShare',{configurable:true,value:({files})=>files.length>0});
   Object.defineProperty(navigator,'share',{configurable:true,value:({files})=>{shareCalls.push({names:files.map(f=>f.name),active:navigator.userActivation.isActive});return Promise.resolve();}});
   setMemoOverlay(true);showNotes();openEditor({id:'test',title:'영상테스트',text:'',folderId:currentFolderId,media:[{kind:'video',blob:new Blob(['video-one'],{type:'video/mp4'})},{kind:'video',blob:new Blob(['video-two'],{type:'video/webm'})}]});
 });
 await page.evaluate(()=>openViewer(0));
 await page.click('#vwSave');await page.waitForFunction(()=>!document.getElementById('batchShare').disabled);
 await page.click('#batchShare');
 assert.deepEqual(await page.evaluate(()=>shareCalls[0]),{names:['영상테스트_01_video.mp4'],active:true});
 let download=page.waitForEvent('download');await page.click('#batchZip');let file=await download;assert.equal(file.suggestedFilename(),'영상테스트_01_video.mp4');await file.saveAs('/tmp/memo-single.mp4');
 await page.evaluate(()=>{closeSheet();closeViewer();openBatchExportSheet([current]);});
 await page.waitForFunction(()=>!document.getElementById('batchShare').disabled);
 await page.click('#batchShare');assert.equal((await page.evaluate(()=>shareCalls[1])).names.length,2);
 download=page.waitForEvent('download');await page.click('#batchZip');file=await download;await file.saveAs('/tmp/memo-batch.zip');
 await page.evaluate(()=>{closeSheet();setMemoOverlay(false);openViewer(0);});
 await page.click('#vwClose');assert.equal(await page.evaluate(()=>document.body.classList.contains('memo-open')),true);
 await page.evaluate(()=>setMemoOverlay(false));
 // The editor is normally reached again through the mode switch; exercise the hidden-overlay return directly.
 await page.evaluate(()=>returnToNoteList());
 await page.waitForFunction(()=>current===null&&document.body.classList.contains('memo-open')&&view==='notes');
 assert.equal(await page.locator('#login').isVisible(),false);
 assert.equal(await page.locator('#edBack').isVisible(),false);
 assert.equal(await page.locator('#list').isVisible().catch(()=>true),true);
 // Verify preparation errors stay in the sheet and never become unhandled rejections.
 await page.evaluate(()=>openBatchExportSheet([{media:[{kind:'video',blob:{arrayBuffer:()=>Promise.reject(new Error('read failed'))}}]}]));
 await page.waitForFunction(()=>document.getElementById('exportStatus').textContent.includes('읽지 못했습니다'));
 assert.equal(await page.locator('#batchShare').isDisabled(),true);
 assert.deepEqual(errors,[]);
 await browser.close();console.log('PASS: single export, multiple export, download, active share tap, memo navigation, read failure');
})().catch(e=>{console.error(e);process.exit(1)});
