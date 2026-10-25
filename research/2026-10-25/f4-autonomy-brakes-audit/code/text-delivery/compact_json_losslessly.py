#!/usr/bin/env python3
"""Remove only insignificant JSON whitespace; preserve every lexical token exactly.
Uses a streaming quote-aware scanner, not parse/reserialize. Numbers, escapes, keys,
description strings and array order therefore stay byte-identical. Inserts a line
break between top-level array elements for plain-text readability.
Usage: python3 compact_json_losslessly.py input.json output.json proof.json
"""
import argparse,hashlib,json,pathlib
WS={9,10,13,32}
def scan(source,destination=None):
 quoted=False;escaped=False;depth=0;n=0;tokens=hashlib.sha256();rawhash=hashlib.sha256();written=0
 out=destination.open('xb') if destination else None
 try:
  with source.open('rb') as inp:
   for block in iter(lambda:inp.read(1048576),b''):
    rawhash.update(block);n+=len(block);clean=bytearray();tokenbuf=bytearray()
    for c in block:
     if quoted:
      clean.append(c);tokenbuf.append(c)
      if escaped:escaped=False
      elif c==92:escaped=True
      elif c==34:quoted=False
     elif c not in WS:
      clean.append(c);tokenbuf.append(c)
      if c==34:quoted=True
      elif c in (91,123):
       depth+=1
       if c==91 and depth==1:clean.append(10)
      elif c in (93,125):depth-=1;assert depth>=0
      elif c==44 and depth==1:clean.append(10)
    tokens.update(tokenbuf)
    if out:out.write(clean);written+=len(clean)
  assert not quoted and not escaped and depth==0,'Unbalanced JSON'
  if out:out.write(b'\n');written+=1
 finally:
  if out:out.close()
 return {'source_bytes':n,'source_sha256':rawhash.hexdigest(),'non_whitespace_lexical_sha256':tokens.hexdigest(),'written_bytes':written}
def compact(source,destination):
 # Validate input syntax; do not retain parsed values or convert numeric tokens.
 with source.open('rb') as f:json.load(f)
 a=scan(source,destination);b=scan(destination);assert a['non_whitespace_lexical_sha256']==b['non_whitespace_lexical_sha256']
 with destination.open('rb') as f:json.load(f)
 return {**a,'rendered_bytes':b['source_bytes'],'rendered_sha256':b['source_sha256'],'all_lexical_tokens_identical':True,'arrays_ordered_identically':True,'numeric_lexemes_unchanged':True,'only_insignificant_whitespace_changed':True}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('output');ap.add_argument('proof');a=ap.parse_args();result=compact(pathlib.Path(a.source),pathlib.Path(a.output));pathlib.Path(a.proof).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
