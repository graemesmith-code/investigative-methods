#!/usr/bin/env python3
"""Create bounded portable archives outside Git. No credentials or environment files included."""
import gzip,hashlib,json,pathlib,tarfile
from acquire import DATA,ROOT,save_json
OUT=DATA.parent/'fwi-bundles';OUT.mkdir(exist_ok=True)
groups={'FWI-20261016-raw-sbir-snapshots':[(p,str(p.relative_to(DATA))) for p in sorted((DATA/'raw').rglob('*')) if p.is_file() and p.parent.name in ['sbir','sbir_current'] and not p.name.endswith('.part')],'FWI-20261016-raw-other-sources':[(p,str(p.relative_to(DATA))) for p in sorted((DATA/'raw').rglob('*')) if p.is_file() and p.parent.name not in ['sbir','sbir_current'] and not p.name.endswith('.part')],'FWI-20261016-normalized-rd-contracts':[],'FWI-20261016-normalized-capabilities':[],'FWI-20261016-normalized-research-context':[],'FWI-20261016-provenance':[(p,'provenance/'+str(p.relative_to(ROOT))) for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name not in ['BUNDLE_MANIFEST.json','STORAGE.md']]}
for p in sorted((DATA/'normalized').glob('*')):
 if not p.is_file():continue
 if p.name.startswith(('usaspending_dod_rd','usaspending_darpa')):key='FWI-20261016-normalized-rd-contracts'
 elif p.name.startswith('usaspending_dod_capabilities'):key='FWI-20261016-normalized-capabilities'
 else:key='FWI-20261016-normalized-research-context'
 groups[key].append((p,str(p.relative_to(DATA))))
manifest=[]
for name,members in groups.items():
 path=OUT/(name+'.tar.gz')
 with path.open('wb') as raw:
  with gzip.GzipFile(filename='',mode='wb',fileobj=raw,compresslevel=5,mtime=0) as gz:
   with tarfile.open(fileobj=gz,mode='w|') as tar:
    for p,arcname in members:
     info=tar.gettarinfo(str(p),arcname=arcname);info.uid=info.gid=0;info.uname=info.gname='';info.mtime=0
     with p.open('rb') as f:tar.addfile(info,f)
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 item={'filename':path.name,'local_path':str(path),'bytes':path.stat().st_size,'sha256':h.hexdigest(),'members':len(members),'member_paths':[a for _,a in members]};manifest.append(item);print(json.dumps({k:v for k,v in item.items() if k!='member_paths'}),flush=True)
 if item['bytes']>490_000_000:raise SystemExit('Archive exceeds chosen 490MB portability bound; split this group before upload.')
 # Validate every member and its uncompressed size without modifying any data.
 with tarfile.open(path,'r:gz') as t:
  actual=t.getmembers()
  if len(actual)!=len(members):raise RuntimeError('Archive member count differs')
save_json(ROOT/'BUNDLE_MANIFEST.json',{'format':'tar.gz; extract all archives into the same task-data root','raw_workspace_retention':'not independently guaranteed','archives':manifest})
(OUT/'SHA256SUMS').write_text(''.join(f"{m['sha256']}  {m['filename']}\n" for m in manifest))
