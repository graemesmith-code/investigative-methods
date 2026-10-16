#!/usr/bin/env python3
"""Verify archive hashes plus complete raw/normalized coverage and member hashes, offline."""
import collections,hashlib,json,tarfile
from acquire import ROOT,save_json
manifest=json.loads((ROOT/'BUNDLE_MANIFEST.json').read_text())
expected={r['relative_path']:r['sha256'] for r in map(json.loads,(ROOT/'validation/http_manifest.jsonl').read_text().splitlines()) if r['outcome']=='downloaded'}
expected.update({r['path']:r['sha256'] for r in json.loads((ROOT/'validation/normalized_manifest.json').read_text())})
seen=collections.Counter();bad=[];archives=[]
for a in manifest['archives']:
 h=hashlib.sha256()
 with open(a['local_path'],'rb') as f:
  for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
 good=h.hexdigest()==a['sha256'];archives.append({'filename':a['filename'],'sha256_matches':good,'bytes':a['bytes']})
 if not good:bad.append(a['filename'])
 with tarfile.open(a['local_path'],'r:gz') as t:
  for m in t:
   if m.name not in expected:continue
   seen[m.name]+=1;h=hashlib.sha256();f=t.extractfile(m)
   for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
   if h.hexdigest()!=expected[m.name]:bad.append(m.name)
missing=sorted(set(expected)-set(seen));duplicates={k:v for k,v in seen.items() if v!=1}
result={'archives':archives,'required_raw_payloads':sum(p.startswith('raw/') for p in expected),'required_normalized_files':sum(p.startswith('normalized/') for p in expected),'represented_paths':len(seen),'missing_paths':missing,'duplicate_representations':duplicates,'hash_mismatches':bad,'passed':not(missing or duplicates or bad),'scope':'Local archive bytes and member hashes; Library retention is independently recorded in library_retention_receipt.json'}
save_json(ROOT/'validation/qa_artifact_verification.json',result);print(json.dumps(result))
if not result['passed']:raise SystemExit(1)
