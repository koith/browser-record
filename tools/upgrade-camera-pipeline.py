from pathlib import Path
p=Path("silent-camera-safari.html");s=p.read_text()

# 1) Add runtime capability state/helpers before openCamera.
needle="async function openCamera(){"
block=r'''let cameraCaps=null, cameraSettings=null, photoCapture=null, cameraWatchdog=null;
function inspectCameraCapabilities(){
  try{
    const track=stream&&stream.getVideoTracks()[0];
    if(!track)return null;
    cameraCaps=track.getCapabilities?track.getCapabilities():{};
    cameraSettings=track.getSettings?track.getSettings():{};
    photoCapture=(typeof ImageCapture!=='undefined')?new ImageCapture(track):null;
    window.__cameraDiagnostics={capabilities:cameraCaps,settings:cameraSettings,constraints:track.getConstraints?track.getConstraints():{},supported:navigator.mediaDevices.getSupportedConstraints?navigator.mediaDevices.getSupportedConstraints():{}};
    return cameraCaps;
  }catch(e){cameraCaps={};cameraSettings={};photoCapture=null;return null;}
}
function startCameraWatchdog(){
  clearInterval(cameraWatchdog);
  let bad=0;
  cameraWatchdog=setInterval(async()=>{
    if(!cam.classList.contains('open')||isRecording()||document.hidden)return;
    const t=stream&&stream.getVideoTracks()[0];
    const healthy=t&&t.readyState==='live'&&video.videoWidth>0&&video.readyState>=2;
    bad=healthy?0:bad+1;
    if(bad>=3){
      bad=0;
      try{await startStream(true);inspectCameraCapabilities();applyZoom();}catch(e){}
    }
  },1500);
}
async function waitForStableFrame(ms=120){
  if(video.readyState<2) await new Promise(r=>{const done=()=>{video.removeEventListener('loadeddata',done);r()};video.addEventListener('loadeddata',done,{once:true});setTimeout(done,700)});
  await new Promise(r=>setTimeout(r,ms));
}
'''
if needle not in s: raise SystemExit("openCamera missing")
s=s.replace(needle,block+needle,1)

# 2) Inspect and watchdog after stream start.
s=s.replace("await startStream(true);\n    try{ await detectLenses(); }catch(le){}", "await startStream(true);\n    inspectCameraCapabilities();\n    startCameraWatchdog();\n    try{ await detectLenses(); }catch(le){}",1)

# 3) Hardware zoom first when capability exists, otherwise existing lens/digital logic.
needle="async function setZoom(v){\n  $('zoomReadout').textContent=v.toFixed(1)+'×';"
repl="""async function setZoom(v){
  $('zoomReadout').textContent=v.toFixed(1)+'×';
  const track=stream&&stream.getVideoTracks()[0];
  try{
    const caps=track&&track.getCapabilities?track.getCapabilities():{};
    if(caps.zoom && Number.isFinite(caps.zoom.min) && Number.isFinite(caps.zoom.max)){
      const hv=Math.max(caps.zoom.min,Math.min(caps.zoom.max,v));
      await track.applyConstraints({advanced:[{zoom:hv}]});
      video.style.transform=''; zoomLevel=1; zoomHardware=true;
      $('zoomBadge').textContent='카메라 줌';
      return;
    }
  }catch(e){ zoomHardware=false; }
"""
if needle not in s: raise SystemExit("setZoom missing")
s=s.replace(needle,repl,1)

# 4) Stop watchdog on close.
s=s.replace("function closeCamera(){\n  if(mediaRecorder", "function closeCamera(){\n  clearInterval(cameraWatchdog);cameraWatchdog=null;\n  if(mediaRecorder",1)

# 5) Replace photo capture with ImageCapture-first, stable-frame, canvas fallback preserving digital crop.
start=s.index("function takePhoto(){")
end=s.index("\nfunction pickMime",start)
photo=r'''async function takePhoto(){
  if(!stream||!video.videoWidth)return;
  await waitForStableFrame(120);
  const track=stream.getVideoTracks()[0];
  // Native photo path first when WebKit exposes ImageCapture and no software crop is required.
  if(typeof ImageCapture!=='undefined' && (zoomHardware||zoomLevel<=1.001)){
    try{
      const ic=new ImageCapture(track);
      let opts={};
      try{
        const pc=await ic.getPhotoCapabilities();
        if(pc&&pc.imageWidth&&Number.isFinite(pc.imageWidth.max))opts.imageWidth=pc.imageWidth.max;
        if(pc&&pc.imageHeight&&Number.isFinite(pc.imageHeight.max))opts.imageHeight=pc.imageHeight.max;
      }catch(e){}
      const blob=await ic.takePhoto(opts);
      if(blob&&blob.size){await attachMedia(blob,'photo');return;}
    }catch(e){}
  }
  // Reliable fallback: capture the current video frame, including software zoom crop.
  const st=track.getSettings?track.getSettings():{};
  const vw=st.width||video.videoWidth, vh=st.height||video.videoHeight;
  const c=document.createElement('canvas');c.width=vw;c.height=vh;const ctx=c.getContext('2d');
  if(!zoomHardware&&zoomLevel>1){
    const sw=vw/zoomLevel,sh=vh/zoomLevel,sx=(vw-sw)/2,sy=(vh-sh)/2;
    ctx.drawImage(video,sx,sy,sw,sh,0,0,vw,vh);
  }else ctx.drawImage(video,0,0,vw,vh);
  c.toBlob(b=>{if(b)attachMedia(b,'photo')},'image/jpeg',.94);
}'''
s=s[:start]+photo+s[end:]

# 6) Orientation recovery: re-read settings/reapply zoom without restarting recording.
marker="/* ===== Screen Wake Lock:"
orient=r'''/* Re-evaluate camera geometry after iPhone rotation without tearing down an active recording. */
function refreshCameraAfterOrientation(){
  setTimeout(()=>{
    if(!stream||!cam.classList.contains('open'))return;
    inspectCameraCapabilities();
    if(!isRecording())applyZoom();
  },250);
}
window.addEventListener('orientationchange',refreshCameraAfterOrientation);
if(screen.orientation&&screen.orientation.addEventListener)screen.orientation.addEventListener('change',refreshCameraAfterOrientation);

'''
if marker not in s: raise SystemExit("wake marker missing")
s=s.replace(marker,orient+marker,1)

p.write_text(s)