#!/usr/bin/env python3
"""Lossless small-part transport for four already public research registers.
No network, credentials, paid services, new source data or record aggregation.
Create deterministic gzip copies; restore and verify original-byte SHA256.
"""
import argparse,gzip,hashlib,json,pathlib,shutil,tempfile,os
P=pathlib.Path(__file__).resolve().parents[1]
T=P/'audit/recovery-transport'
FILES=('evidence/brakes-candidate-register.csv','evidence/brakes-candidate-register.json','evidence/asimov-performer-continuation-check.csv','evidence/auxiliary-candidates.jsonl')
PART=4*1024*1024
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as inp:
  for b in iter(lambda:inp.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def create():
 T.mkdir(exist_ok=True);records=[]
 with tempfile.TemporaryDirectory(prefix='f4-recovery-gzip-',dir='/workspace/scratch') as work:
  for rel in FILES:
   src=P/rel;original=sha(src);compressed=pathlib.Path(work)/(src.name+'.gz')
   with src.open('rb') as inp,compressed.open('wb') as out:
    with gzip.GzipFile(filename='',mode='wb',fileobj=out,mtime=0,compresslevel=9) as gz:shutil.copyfileobj(inp,gz,1024*1024)
   parts=[]
   with compressed.open('rb') as inp:
    index=0
    while True:
     body=inp.read(PART)
     if not body:break
     f=T/(src.name+f'.gz.part-{index:04d}');f.write_bytes(body);parts.append({'path':f.relative_to(P).as_posix(),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()});index+=1
   records.append({'original_path':rel,'original_bytes':src.stat().st_size,'original_sha256':original,'compressed_bytes':compressed.stat().st_size,'compressed_sha256':sha(compressed),'encoding':'Concatenate listed parts in order, then gzip-decompress once; complete original UTF-8 bytes','parts':parts})
 manifest={'format_version':1,'purpose':'Duplicate lossless transport encodings of four existing public registers; not additional observations, awards or funding','max_part_bytes':PART,'files':records,'reproduce':'python3 code/recovery_transport.py restore --destination /absolute/output-parent; verifies every part, combined gzip and recovered original before installation','source_scope':'Only the four named public authored research registers; no raw third-party article caches, private notes or input archives'}
 (T/'transport-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');restore(None);print(json.dumps({'files':len(records),'parts':sum(len(r['parts']) for r in records),'compressed_bytes':sum(r['compressed_bytes'] for r in records),'original_bytes':sum(r['original_bytes'] for r in records),'validation':'Every part, concatenated gzip and decompressed original hash verified'},indent=2))
def restore(destination):
 manifest=json.loads((T/'transport-manifest.json').read_text())
 with tempfile.TemporaryDirectory(prefix='f4-recovery-verify-',dir='/workspace/scratch') as work:
  for index,r in enumerate(manifest['files']):
   compressed=pathlib.Path(work)/(str(index)+'.gz')
   with compressed.open('wb') as out:
    for part in r['parts']:
     src=P/part['path'];assert src.resolve().is_relative_to(P.resolve())
     assert src.stat().st_size==part['bytes'] and sha(src)==part['sha256']
     with src.open('rb') as inp:shutil.copyfileobj(inp,out,1024*1024)
   assert compressed.stat().st_size==r['compressed_bytes'] and sha(compressed)==r['compressed_sha256']
   plain=pathlib.Path(work)/(str(index)+'.plain')
   with gzip.open(compressed,'rb') as inp,plain.open('wb') as out:shutil.copyfileobj(inp,out,1024*1024)
   assert plain.stat().st_size==r['original_bytes'] and sha(plain)==r['original_sha256']
   if destination:
    base=pathlib.Path(destination).resolve();target=base/r['original_path'];assert target.resolve().is_relative_to(base)
    target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():assert sha(target)==r['original_sha256'],'Existing different output is not overwritten'
    else:
     temporary=target.with_name(target.name+'.recovery-tmp');shutil.copyfile(plain,temporary);os.replace(temporary,target)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('action',choices=['create','restore']);a.add_argument('--destination');args=a.parse_args();create() if args.action=='create' else restore(args.destination)
