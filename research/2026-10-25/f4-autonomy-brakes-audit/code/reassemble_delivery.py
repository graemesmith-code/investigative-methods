#!/usr/bin/env python3
"""Recover the one complete UTF-8 artifact from its hash-verified public transport.
No network, credentials or paid service. Never overwrite a different existing file.
"""
import argparse,codecs,gzip,hashlib,json,pathlib,shutil,tempfile,os
P=pathlib.Path(__file__).resolve().parents[1]
BUNDLE='F4-COMPLETE-RESEARCH-PACKAGE.txt'
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as inp:
  for b in iter(lambda:inp.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def restore(output):
 m=json.loads((P/(BUNDLE+'.delivery.json')).read_text());output=pathlib.Path(output).resolve();output.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory(dir=output.parent,prefix='f4-delivery-') as work:
  compressed=pathlib.Path(work)/'complete.gz'
  with compressed.open('wb') as out:
   for member in m['ordered_transport_members']:
    src=P/member['path'];assert src.resolve().is_relative_to(P.resolve()) and src.is_file()
    assert src.stat().st_size==member['bytes'] and sha(src)==member['sha256']
    with src.open('rb') as inp:shutil.copyfileobj(inp,out,1024*1024)
  assert compressed.stat().st_size==m['gzip_bytes'] and sha(compressed)==m['gzip_sha256']
  plain=pathlib.Path(work)/BUNDLE;decoder=codecs.getincrementaldecoder('utf-8')();total=0;h=hashlib.sha256()
  with gzip.open(compressed,'rb') as inp,plain.open('wb') as out:
   for b in iter(lambda:inp.read(1024*1024),b''):
    total+=len(b);assert total<=m['payload_bytes'];decoder.decode(b);h.update(b);out.write(b)
   decoder.decode(b'',final=True)
  assert total==m['payload_bytes'] and h.hexdigest()==m['payload_sha256']
  if output.exists():assert sha(output)==m['payload_sha256'],'Existing different output not overwritten'
  else:os.replace(plain,output)
 print(json.dumps({'output':str(output),'bytes':total,'sha256':h.hexdigest(),'UTF8_validated':True,'all_transport_and_payload_hashes_verified':True},indent=2))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--output',required=True);restore(a.parse_args().output)
