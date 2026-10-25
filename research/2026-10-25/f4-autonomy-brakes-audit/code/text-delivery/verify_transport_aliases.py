#!/usr/bin/env python3
"""Verify concatenated public transport parts against the immutable source.
No network, uploads, or mutation of original files. Emits assembler rules/proofs.
"""
import argparse,gzip,hashlib,json,pathlib,tempfile

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def main():
 a=argparse.ArgumentParser();a.add_argument('--snapshot',required=True);a.add_argument('--output',required=True);v=a.parse_args();r=pathlib.Path(v.snapshot)
 manifests=list(r.rglob('transport-manifest.json'));rules=[];proofs=[]
 for mp in manifests:
  j=json.loads(mp.read_text());mr=str(mp.relative_to(r))
  for entry in j['files']:
   original=r/entry['original_path'];assert original.is_file(),entry['original_path']
   assert original.stat().st_size==entry['original_bytes'] and sha(original)==entry['original_sha256'],'Original source changed: '+entry['original_path']
   ch=hashlib.sha256();cn=0
   with tempfile.TemporaryFile() as tmp:
    for part in entry['parts']:
     p=r/part['path'];assert p.stat().st_size==part['bytes'] and sha(p)==part['sha256']
     with p.open('rb') as f:
      for b in iter(lambda:f.read(1048576),b''):tmp.write(b);ch.update(b);cn+=len(b)
    assert cn==entry['compressed_bytes'] and ch.hexdigest()==entry['compressed_sha256'];tmp.seek(0);dh=hashlib.sha256();dn=0
    with gzip.GzipFile(fileobj=tmp) as f:
     for b in iter(lambda:f.read(1048576),b''):dh.update(b);dn+=len(b)
    assert dn==entry['original_bytes'] and dh.hexdigest()==entry['original_sha256']
   proof={'manifest':mr,'original':entry['original_path'],'combined_compressed_bytes':cn,'combined_compressed_sha256':ch.hexdigest(),'reconstructed_bytes':dn,'reconstructed_sha256':dh.hexdigest(),'all_parts_verified':True,'exact_original_reconstructed':True}
   proofs.append(proof)
   for part in entry['parts']:rules.append({'path':part['path'],'expected_sha256':part['sha256'],'representation':'transport_catalogued','reason':'Lossless binary transport alias, not additional research. Ordered parts reconstruct the exact source bytes already represented.','represented_by':entry['original_path'],'proof':proof})
 pathlib.Path(v.output).write_text(json.dumps({'files':rules,'coverage_proofs':proofs},indent=2)+'\n');print(json.dumps({'manifests':len(manifests),'originals':len(proofs),'parts':len(rules),'all_verified':True}))
if __name__=='__main__':main()
