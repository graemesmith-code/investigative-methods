#!/usr/bin/env python3
"""Recreate the full SBIR-abstract input for the hand-adjudicated live scope crosswalk.
Reads the authorized canonical archive extraction; no network or paid service.
"""
import argparse,gzip,json,pathlib,re
P=pathlib.Path(__file__).resolve().parents[1]
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--extracted',type=pathlib.Path,default=pathlib.Path('/workspace/scratch/f4-data-complete/extracted'));a.add_argument('--output',type=pathlib.Path,default=pathlib.Path('/workspace/scratch/f4-live-technical-matches.json'));args=a.parse_args()
 live=json.loads((P/'evidence/live-award-register.json').read_text());targets={x['piid'] for x in live['awards']};found={};counts={}
 files=sorted(args.extracted.rglob('sbir*.jsonl.gz'),key=lambda x:x.name,reverse=True)
 for f in files:
  with gzip.open(f,'rt') as inp:
   for num,line in enumerate(inp,1):
    r=json.loads(line);piid=re.sub('[^A-Z0-9]','',str(r.get('award_key','')).upper())
    if piid in targets:
     text=r.get('text','') or r.get('evidence_excerpt','');item={'piid':piid,'source_file':f.name,'source_row':num,'title':r.get('title'),'full_description':text,'source_url':r.get('source_url'),'row_sha256':r.get('record_sha256'),'input_snapshot_sha256':r.get('source_snapshot_sha256')}
     if piid not in found or len(text)>len(found[piid]['full_description']):found[piid]=item
   counts[f.name]=num
 args.output.write_text(json.dumps(found,indent=2));print(json.dumps({'rows_read':counts,'matched_live_awards':len(found),'output':str(args.output)}))
