#!/usr/bin/env python3
"""Inventory/hash every authored file and concatenate it without truncation.

The bundle cannot contain its own bytes or hash recursively. SHA256SUMS excludes
itself and the bundle; the bundle contains SHA256SUMS and manifest.json in full.
The bundle's independent SHA256 is printed for publication/delivery verification.
No raw source caches, private transfer data, or credentials are input to this code.
"""
import argparse,base64,codecs,gzip,hashlib,json,pathlib,datetime,shutil
P=pathlib.Path(__file__).resolve().parents[1]
BUNDLE='F4-COMPLETE-RESEARCH-PACKAGE.txt'
def digest(b):return hashlib.sha256(b).hexdigest()
def file_digest(path):
 h=hashlib.sha256()
 with path.open('rb') as inp:
  for b in iter(lambda:inp.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def build(reuse_manifest=False,output=None):
 excluded={BUNDLE,BUNDLE+'.gz','manifest.json','SHA256SUMS'}
 files=sorted(p for p in P.rglob('*') if p.is_file() and p.relative_to(P).as_posix() not in excluded and '__pycache__' not in p.parts and p.suffix!='.pyc')
 inventory=[]
 for f in files:
  b=f.read_bytes()
  try:b.decode('utf-8');representation='UTF-8 original bytes'
  except UnicodeDecodeError:representation='Base64 of complete original binary bytes; no data omitted'
  inventory.append({'path':f.relative_to(P).as_posix(),'bytes':len(b),'sha256':digest(b),'text_bundle_representation':representation})
 manifest={'format_version':1,'research_cutoff':'2026-10-25','generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'All authored deliverables, registers, audit records and scripts in this directory; private raw third-party caches and transferred input archives excluded intentionally.','inventory':inventory,'recursive_container_exclusions':{'manifest.json':'Does not inventory itself or SHA256SUMS or delivery containers','SHA256SUMS':'Hashes all other authored files including manifest; excludes itself and delivery containers to avoid recursion',BUNDLE:'Contains complete inventory and every other public package member, including manifest and SHA256SUMS; cannot contain itself or its gzip transport copy',BUNDLE+'.gz':'Exact deterministic gzip transport of the complete UTF-8 bundle; excluded from its own payload to avoid recursion; transport/plain hashes printed separately at delivery'},'authored_file_count_excluding_containers':len(files),'authored_bytes_excluding_containers':sum(x['bytes'] for x in inventory)}
 if not reuse_manifest:(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 else:
  old=json.loads((P/'manifest.json').read_text());assert old['inventory']==inventory,'Files differ from supplied manifest; cannot recreate identical bundle'
 sumfiles=files+[P/'manifest.json']
 sums=''.join(f'{digest(f.read_bytes())}  {f.relative_to(P).as_posix()}\n' for f in sorted(sumfiles))
 if not reuse_manifest:(P/'SHA256SUMS').write_text(sums,encoding='utf-8')
 else:assert (P/'SHA256SUMS').read_text()==sums,'SHA256SUMS differs'
 priority={'report.md':0,'README.md':1,'READING_PACK.md':2}
 members=sorted(files+[P/'manifest.json',P/'SHA256SUMS'],key=lambda f:(priority.get(f.relative_to(P).as_posix(),3),f.relative_to(P).as_posix()))
 target=pathlib.Path(output) if output else P/BUNDLE
 def representation(f):
  b=f.read_bytes()
  try:b.decode('utf-8');return b,'UTF-8'
  except UnicodeDecodeError:return base64.encodebytes(b),'BASE64-COMPLETE-ORIGINAL-BINARY'
 embedded=[]
 with target.open('wb') as out:
  out.write(b'F4 COMPLETE RESEARCH PACKAGE\nUTF-8. Conclusions and reader guides come first; complete inventory and technical annexes follow. Every listed file is included in full. No silent truncation.\nText files retain their original bytes. Binary/gzip sidecars are fully Base64 encoded, explicitly labeled, and can be recovered with Python base64.decodebytes; original-byte hashes remain authoritative.\nThe bundle excludes only itself and its gzip transport representation. Raw third-party narrative caches and supplied source archives remain private; selected public government API evidence is included.\n')
  for index,f in enumerate(members):
   if index==3:
    out.write(b'\n\nCOMPLETE INVENTORY\n')
    for member in members:
     content=member.read_bytes();out.write(f'{member.relative_to(P).as_posix()}\t{len(content)} bytes\tSHA256 {digest(content)}\n'.encode())
    out.write(b'\nTECHNICAL ANNEXES — COMPLETE ORIGINAL FILES\n')
   b=f.read_bytes();body,encoding=representation(f);out.write(f'\n\n===== BEGIN FILE: {f.relative_to(P).as_posix()} | {len(b)} bytes | SHA256 {digest(b)} | {encoding} =====\n'.encode());embedded.append((f,out.tell(),len(body),encoding));out.write(body);out.write(f'\n===== END FILE: {f.relative_to(P).as_posix()} =====\n'.encode())
  out.write(f'\nEND OF COMPLETE PACKAGE. {len(members)} files included in full.\n'.encode())
 # Validate exact bytes of every embedded member, not merely a trailing marker.
 decoder=codecs.getincrementaldecoder('utf-8')()
 with target.open('rb') as inp:
  for chunk in iter(lambda:inp.read(1024*1024),b''):decoder.decode(chunk)
  decoder.decode(b'',final=True)
 with target.open('rb') as inp:
  for f,start,length,encoding in embedded:
   b=f.read_bytes();body,_=representation(f);inp.seek(start);assert inp.read(length)==body
   if encoding.startswith('BASE64'):assert base64.decodebytes(body)==b
 transport=target.with_suffix(target.suffix+'.gz')
 with target.open('rb') as inp,transport.open('wb') as out:
  with gzip.GzipFile(filename='',mode='wb',fileobj=out,compresslevel=9,mtime=0) as compressed:shutil.copyfileobj(inp,compressed,1024*1024)
 expanded_hash=hashlib.sha256();expanded_bytes=0
 with gzip.open(transport,'rb') as inp:
  for chunk in iter(lambda:inp.read(1024*1024),b''):expanded_hash.update(chunk);expanded_bytes+=len(chunk)
 plain_hash=file_digest(target);assert expanded_hash.hexdigest()==plain_hash and expanded_bytes==target.stat().st_size
 print(json.dumps({'bundle':str(target),'files_embedded':len(members),'bytes':target.stat().st_size,'sha256':plain_hash,'gzip_transport':str(transport),'gzip_bytes':transport.stat().st_size,'gzip_sha256':file_digest(transport),'validation':'every embedded original member byte-compared; binary encodings and gzip round-trip verified; UTF-8 incrementally decoded'},indent=2))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--reuse-manifest',action='store_true');a.add_argument('--output');args=a.parse_args();build(args.reuse_manifest,args.output)
