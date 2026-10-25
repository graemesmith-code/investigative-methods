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
GIT_FILE_LIMIT=100*1024*1024
DELIVERY_PART_BYTES=4*1024*1024
def digest(b):return hashlib.sha256(b).hexdigest()
def file_digest(path):
 h=hashlib.sha256()
 with path.open('rb') as inp:
  for b in iter(lambda:inp.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def build(reuse_manifest=False,output=None,publish_transport=False):
 excluded={BUNDLE,BUNDLE+'.gz',BUNDLE+'.delivery.json','manifest.json','SHA256SUMS'}
 def excluded_container(f):
  rel=f.relative_to(P).as_posix()
  return rel in excluded or ('/' not in rel and rel.startswith(BUNDLE+'.gz.part-'))
 files=sorted(p for p in P.rglob('*') if p.is_file() and not excluded_container(p) and '__pycache__' not in p.parts and p.suffix!='.pyc')
 inventory=[]
 for f in files:
  b=f.read_bytes()
  try:b.decode('utf-8');representation='UTF-8 original bytes'
  except UnicodeDecodeError:representation='Base64 of complete original binary bytes; no data omitted'
  inventory.append({'path':f.relative_to(P).as_posix(),'bytes':len(b),'sha256':digest(b),'text_bundle_representation':representation})
 manifest={'format_version':1,'research_cutoff':'2026-10-25','generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'All available authored research deliverables, registers, audit records and scripts in this directory; recursive delivery containers, private raw third-party caches and supplied input archives excluded explicitly. Unavailable independent-original bodies are disclosed in audit/RECOVERY_STATUS.md, not represented as included.','inventory':inventory,'recursive_container_exclusions':{'manifest.json':'Does not inventory itself or SHA256SUMS or delivery containers','SHA256SUMS':'Hashes all other authored files including manifest; excludes itself and delivery containers to avoid recursion',BUNDLE:'Contains complete inventory and every other public package member, including manifest and SHA256SUMS; cannot contain itself or its gzip transport copy',BUNDLE+'.gz':'Exact deterministic gzip transport of the complete UTF-8 bundle; excluded from its own payload to avoid recursion; transport/plain hashes printed separately at delivery'},'authored_file_count_excluding_containers':len(files),'authored_bytes_excluding_containers':sum(x['bytes'] for x in inventory)}
 manifest['recursive_container_exclusions'][BUNDLE+'.delivery.json']='Post-build byte/hash transport map; excluded to avoid embedding a hash of the container in itself. Contains no additional research records.'
 manifest['recursive_container_exclusions'][BUNDLE+'.gz.part-*']='If needed, complete ordered parts of the deterministic gzip delivery container; not additional research records. Reassembled using the post-build delivery map.'
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
  out.write(b'F4 COMPLETE RESEARCH PACKAGE\nUTF-8. Conclusions and reader guides come first; complete inventory and technical annexes follow. Every listed file is included in full. No silent truncation.\nText files retain their original bytes. Binary/gzip sidecars are fully Base64 encoded, explicitly labeled, and can be recovered with Python base64.decodebytes; original-byte hashes remain authoritative.\nThe bundle excludes its recursive delivery containers (itself, gzip/parts and post-build transport map), which contain no additional research records. Unavailable independent-original bodies are documented in RECOVERY_STATUS rather than represented as included. Raw third-party narrative caches and supplied source archives remain private; selected public government API evidence is included.\n')
  for index,f in enumerate(members):
   if index==3:
    out.write(b'\n\nCOMPLETE INVENTORY\n')
    for member in members:
     content=member.read_bytes();out.write(f'{member.relative_to(P).as_posix()}\t{len(content)} bytes\tSHA256 {digest(content)}\n'.encode())
    out.write('\nTECHNICAL ANNEXES — COMPLETE ORIGINAL FILES\n'.encode('utf-8'))
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
 result={'bundle':str(target),'files_embedded':len(members),'bytes':target.stat().st_size,'sha256':plain_hash,'gzip_transport':str(transport),'gzip_bytes':transport.stat().st_size,'gzip_sha256':file_digest(transport),'validation':'every embedded original member byte-compared; binary encodings and gzip round-trip verified; UTF-8 incrementally decoded'}
 if publish_transport:
  # Only owned recursive delivery containers are replaced. Research files stay
  # unchanged; every original is already embedded and byte-compared above.
  for old in P.glob(BUNDLE+'.gz.part-*'):old.unlink()
  public=P/(BUNDLE+'.gz');parts=[]
  if transport.stat().st_size<GIT_FILE_LIMIT:
   if transport.resolve()!=public.resolve():shutil.copyfile(transport,public)
   parts=[{'path':public.name,'bytes':public.stat().st_size,'sha256':file_digest(public)}]
  else:
   with transport.open('rb') as inp:
    index=0
    while True:
     body=inp.read(DELIVERY_PART_BYTES)
     if not body:break
     part=P/(BUNDLE+f'.gz.part-{index:04d}');part.write_bytes(body);parts.append({'path':part.name,'bytes':len(body),'sha256':digest(body)});index+=1
   if public.exists():public.unlink()
  delivery={'format_version':1,'payload_filename':BUNDLE,'payload_bytes':result['bytes'],'payload_sha256':plain_hash,'gzip_bytes':result['gzip_bytes'],'gzip_sha256':result['gzip_sha256'],'ordered_transport_members':parts,'research_members_embedded':len(members),'representation':'Concatenate the complete ordered gzip members, then decompress once to the complete UTF-8 payload','reconstruction':'python3 code/reassemble_delivery.py --output /absolute/F4-COMPLETE-RESEARCH-PACKAGE.txt','recursion_boundary':'This post-build map and gzip delivery containers are excluded from their own research payload. They contain no additional research observations. Every available authored research member is inventoried and embedded in full.'}
  (P/(BUNDLE+'.delivery.json')).write_text(json.dumps(delivery,indent=2)+'\n');result['public_delivery_map']=BUNDLE+'.delivery.json';result['public_transport_members']=len(parts)
 print(json.dumps(result,indent=2));return result
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--reuse-manifest',action='store_true');a.add_argument('--output');a.add_argument('--publish-transport',action='store_true');args=a.parse_args();build(args.reuse_manifest,args.output,args.publish_transport)
