from pathlib import Path
p=Path('silent-camera-safari.html')
s=p.read_text()
old="""// iOS Safari can keep a stale backing-store relationship for IndexedDB Blobs
// after a media element has consumed them. Rehydrate through ArrayBuffer so each
// UI surface gets a physically new Blob and object URL instead of sharing one.
async function isolatedBlobURL(blob){
  if(!blob || typeof blob.arrayBuffer!=='function') throw new Error('invalid blob');
  const buf=await blob.arrayBuffer();
  const fresh=new Blob([buf],{type:blob.type||'application/octet-stream'});
  return URL.createObjectURL(fresh);
}
"""
new="""// iOS Safari may fail when the same IndexedDB-backed Blob is read more than once.
// Read each source Blob exactly once, cache an in-memory clone, and create independent
// object URLs from that clone for list/editor/viewer surfaces.
const freshBlobCache=new WeakMap();
async function freshBlob(blob){
  if(!blob || typeof blob.arrayBuffer!=='function') throw new Error('invalid blob');
  let pending=freshBlobCache.get(blob);
  if(!pending){
    pending=(async()=>{
      const buf=await blob.arrayBuffer();
      return new Blob([buf],{type:blob.type||'application/octet-stream'});
    })();
    freshBlobCache.set(blob,pending);
  }
  try{ return await pending; }
  catch(e){ freshBlobCache.delete(blob); throw e; }
}
async function isolatedBlobURL(blob){
  const fresh=await freshBlob(blob);
  return URL.createObjectURL(fresh);
}
"""
if old not in s:
    raise SystemExit('target block not found')
s=s.replace(old,new,1)
p.write_text(s)
print('patched')
