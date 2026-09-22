from pathlib import Path
p=Path("silent-camera-safari.html");s=p.read_text()
old="""  // Native photo path first when WebKit exposes ImageCapture and no software crop is required.
  if(typeof ImageCapture!=='undefined' && (zoomHardware||zoomLevel<=1.001)){
    try{"""
new="""  // Do not invoke ImageCapture.takePhoto() while MediaRecorder is consuming the
  // same iOS camera track. WebKit can reconfigure/stall the live track and leave
  // the preview white. During recording, grab the already-live video frame instead.
  const recordingNow=!!(mediaRecorder&&mediaRecorder.state==='recording');
  if(!recordingNow && typeof ImageCapture!=='undefined' && (zoomHardware||zoomLevel<=1.001)){
    try{"""
if old not in s: raise SystemExit("photo block missing")
s=s.replace(old,new,1)
p.write_text(s)