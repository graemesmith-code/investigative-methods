#!/usr/bin/env python3
"""Read-only requested-deliverable and published-checksum diagnostics."""
import argparse,csv,gzip,hashlib,json,pathlib,re
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('snapshot');ap.add_argument('output');a=ap.parse_args();root=pathlib.Path(a.snapshot)
 required=['README.md','report.md','READING_PACK.md','SHA256SUMS','manifest.json','audit/EDITOR_REPORTER_LOOP_LOG.md','audit/methodology-accounting.json','evidence/brakes-candidate-register.csv','evidence/brakes-candidate-register.json','evidence/asimov-performer-continuation-check.csv','evidence/fpds-verified-actions.csv','audit/exa-query-cost-log.csv']
 req={n:{'at_requested_path':(root/n).is_file(),'other_matches':[str(p.relative_to(root)) for p in root.rglob(pathlib.Path(n).name) if p.is_file() and p!=root/n]} for n in required};checks=[]
 for sums in sorted(root.rglob('SHA256SUMS')):
  checked=0;missing=[];bad=[];unparsed=[];gzip_represented=[]
  for line in sums.read_text().splitlines():
   if not line.strip() or line.lstrip().startswith('#'):continue
   m=re.fullmatch(r'([a-fA-F0-9]{64}) [ *](.+)',line)
   if not m:unparsed.append(line);continue
   rel=pathlib.PurePosixPath(m[2]);assert not rel.is_absolute() and '..' not in rel.parts;p=sums.parent/rel
   if not p.is_file():
    gz=pathlib.Path(str(p)+'.gz')
    if not gz.is_file():missing.append(str(rel));continue
    digest=hashlib.sha256()
    with gzip.open(gz,'rb') as f:
     for b in iter(lambda:f.read(1048576),b''):digest.update(b)
    h=digest.hexdigest();gzip_represented.append({'logical_path':str(rel),'physical_path':str(gz.relative_to(sums.parent)),'decompressed_sha256':h})
   else:h=sha(p)
   checked+=1
   if h.lower()!=m[1].lower():bad.append({'path':str(rel),'expected':m[1],'actual':h})
  checks.append({'file':str(sums.relative_to(root)),'checked':checked,'missing':missing,'mismatches':bad,'unparsed':unparsed,'verified_gzip_representations':gzip_represented})
 exa=[]
 for p in root.rglob('*exa*cost*.csv'):
  with p.open(newline='') as f:
   rd=csv.DictReader(f);rows=list(rd);exa.append({'path':str(p.relative_to(root)),'rows':len(rows),'columns':rd.fieldnames})
 result={'requested_paths':req,'checksums':checks,'exa_ledgers':exa,'potential_full_source_holdings':[str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and (p.suffix.lower() in ('.pdf','.html','.htm') or any(x in ('raw','sources','cache') for x in p.relative_to(root).parts))]}
 pathlib.Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'missing_requested_paths':[k for k,v in req.items() if not v['at_requested_path']],'checksum_files':len(checks),'checksum_mismatches':sum(len(x['mismatches']) for x in checks),'checksum_missing':sum(len(x['missing']) for x in checks),'exa_ledgers':exa,'potential_source_holdings':len(result['potential_full_source_holdings'])},indent=2))
if __name__=='__main__':main()
