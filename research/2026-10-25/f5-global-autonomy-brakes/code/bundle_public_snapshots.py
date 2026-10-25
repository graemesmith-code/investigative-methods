#!/usr/bin/env python3
"""Bundle explicitly selected public-cleared files with complete payload hashes.

This tool does not determine redistribution rights, upload or share files. Supply
only approved files/directories. It refuses credential-like file extensions and PDFs; callers must separately
review contents for secrets and redistribution rights. Original source
archives are not F5 outputs. The outer Drive receipt records the inventory's own
hash, avoiding self-referential hash claims. No filesystem extraction is needed.
"""
import argparse,csv,hashlib,io,json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile
def row_count(name,b):
 try:
  if name.endswith('.csv'):return sum(1 for _ in csv.DictReader(io.StringIO(b.decode())))
  if name.endswith('.jsonl'):return sum(bool(x.strip()) for x in b.splitlines())
  o=json.loads(b)
  if isinstance(o,list):return len(o)
  for key in ['records','results','members','objects','sources']:
   if isinstance(o.get(key),list):return len(o[key])
  return 1
 except Exception:
  try:return len(ET.fromstring(b).findall('{http://www.w3.org/2005/Atom}entry'))
  except Exception:return None
def bundle(paths,output):
 files={}
 for path in map(Path,paths):
  for p in sorted(path.rglob('*')) if path.is_dir() else [path]:
   if not p.is_file():continue
   if p.suffix.lower() in ['.pdf','.pem','.key'] or p.name.startswith('.env'):raise ValueError('Disallowed file '+p.name)
   name=path.name+'/'+str(p.relative_to(path)) if path.is_dir() else p.name
   if name in files:raise ValueError('Duplicate bundle path '+name)
   files[name]=p.read_bytes()
 inventory={'schema':'F5-public-payload-members-v1','self_inventory_note':'Every payload file is listed below. MEMBER_MANIFEST.json is the additional archive member; its exact hash and total member count are recorded in the outer Drive receipt.','member_count_excluding_inventory':len(files),'members':[{'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'row_count':row_count(n,b),'row_count_note':'Table rows/list entries/API page results; null for non-tabular or uninterpreted body. Counts across snapshots are not additive distinct actions.'} for n,b in sorted(files.items())]}
 payload=(json.dumps(inventory,indent=2,ensure_ascii=False)+'\n').encode()
 with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
  for n,b in sorted(files.items()):z.writestr(n,b)
  z.writestr('MEMBER_MANIFEST.json',payload)
 return {'filename':str(output),'bytes':Path(output).stat().st_size,'sha256':hashlib.sha256(Path(output).read_bytes()).hexdigest(),'members':len(files)+1,'member_manifest_sha256':hashlib.sha256(payload).hexdigest()}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('paths',nargs='+');p.add_argument('--output',required=True);a=p.parse_args();print(json.dumps(bundle(a.paths,a.output)))
