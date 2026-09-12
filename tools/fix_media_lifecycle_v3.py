from pathlib import Path

p=Path('silent-camera-safari.html')
s=p.read_text(encoding='utf-8')

old="""function cleanForSave(v){
  if(v&&v.media){ v.media.forEach(m=>{ delete m._url; delete m._purl; }); }
  return v;
}"""
new="""function cleanForSave(v){
  if(!v)return v;
  const copy={...v};
  if(v.media){
    copy.media=v.media.map(m=>{
      const mc={...m};
      delete mc._url; delete mc._purl;
      return mc;
    });
  }
  return copy;
}"""
if old not in s: raise SystemExit('cleanForSave anchor not found')
s=s.replace(old,new,1)

old="""let viewerIndex=-1; const viewer=$('viewer'), vwMedia=$('vwMedia');
let viewerObjectURL='';
function releaseViewerObjectURL(){
  if(!viewerObjectURL)return;
  const old=viewerObjectURL; viewerObjectURL='';
  setTimeout(()=>{ try{ URL.revokeObjectURL(old); }catch(e){} },0);
}"""
new="""let viewerIndex=-1; const viewer=$('viewer'), vwMedia=$('vwMedia');
let viewerObjectURL='';
function releaseViewerObjectURL(){
  // Deliberately do NOT revoke blob URLs on iOS Safari.
  // Revoking a viewer URL has repeatedly invalidated thumbnail/playback URLs
  // backed by the same IndexedDB Blob. We only drop our reference here.
  viewerObjectURL='';
}"""
if old not in s: raise SystemExit('viewer release anchor not found')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
