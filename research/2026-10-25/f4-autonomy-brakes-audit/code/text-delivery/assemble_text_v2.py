#!/usr/bin/env python3
"""F4 text assembler v2, rebuilt after workspace reset. No network or uploads.
Immutable Git inventory, explicit scope rules, exact body hashes, no truncation.
Any final artifact requires parent-approved final_verified=true.
"""
import argparse,codecs,collections,csv,gzip,hashlib,json,pathlib,re,shutil
from urllib.parse import quote
REPO='graemesmith-code/investigative-methods'
BAD=re.compile(rb'(?<![A-Za-z0-9_])(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{30,}|AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----)')
def digest(p,git=False):
 h=hashlib.sha1() if git else hashlib.sha256()
 if git:h.update(b'blob '+str(p.stat().st_size).encode()+b'\0')
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def content(p):return gzip.open(p,'rb') if p.suffix=='.gz' else p.open('rb')
def body_metadata(p):
 h=hashlib.sha256();n=0;dec=codecs.getincrementaldecoder('utf-8')();carry=b''
 with content(p) as f:
  for b in iter(lambda:f.read(1048576),b''):
   dec.decode(b);assert b'\0' not in b,'NUL: '+str(p);assert not BAD.search(carry+b),'Credential-like text: '+str(p);carry=b[-256:];h.update(b);n+=len(b)
  dec.decode(b'',final=True)
 return n,h.hexdigest()
def csv_proof(cp,jp):
 try:
  with content(jp) as f:rs=json.load(f)
  if not isinstance(rs,list) or not all(isinstance(r,dict) for r in rs):return None
  with cp.open(encoding='utf-8-sig',newline='') as f:
   rd=csv.DictReader(f);cols=rd.fieldnames;n=0
   for n,c in enumerate(rd,1):
    if n>len(rs) or None in c:return None
    for k,s in c.items():
     if k not in rs[n-1]:
      if s=='':continue
      return None
     v=rs[n-1][k]
     if isinstance(v,(dict,list)):
      if json.loads(s)!=v:return None
     elif v is None:
      if s not in ('','null'):return None
     elif isinstance(v,bool):
      if s.lower()!=str(v).lower():return None
     elif str(v)!=s:return None
   if n!=len(rs):return None
  return {'rows':n,'columns':cols,'mismatches':0,'rule':'Every CSV cell matches the same-position JSON value; missing JSON fields map only to empty CSV cells. Additional JSON fields retained.'}
 except (ValueError,TypeError,UnicodeError):return None
def rank(p):
 if p=='report.md':return (0,p)
 if p=='README.md':return (1,p)
 if p=='READING_PACK.md':return (2,p)
 if p.endswith('.md'):return (3,p)
 if 'independent-stage1/evidence/' in p:return (8,p)
 if '/primary-awards/' in p:return (7,p)
 if p.endswith('.py') or '/code/' in '/'+p:return (6,p)
 if p.startswith('audit/') or '/audit/' in p:return (5,p)
 return (4,p)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--inventory',required=True);ap.add_argument('--snapshot',required=True);ap.add_argument('--rules',required=True);ap.add_argument('--output',required=True);ap.add_argument('--audit',required=True);ap.add_argument('--allow-draft',action='store_true');a=ap.parse_args()
 inv=json.loads(pathlib.Path(a.inventory).read_text());rules=json.loads(pathlib.Path(a.rules).read_text());snap=pathlib.Path(a.snapshot);outpath=pathlib.Path(a.output);audit=pathlib.Path(a.audit);audit.mkdir(parents=True,exist_ok=True)
 assert re.fullmatch('[a-f0-9]{40}',inv['commit'])
 if not a.allow_draft:assert inv.get('final_verified') is True,'Final editorial/publication gate remains open'
 rows={};total=0;csv.field_size_limit(2**31-1)
 for item in inv['files']:
  assert item['path'].startswith(inv['root']);rel=item['path'][len(inv['root']):];p=snap/rel
  assert p.is_file() and p.stat().st_size==item['size'] and digest(p,True)==item['sha'],'Git mismatch/missing: '+rel
  rows[rel]={'path':rel,'source_bytes':item['size'],'source_sha256':digest(p),'git_blob_sha':item['sha'],'github_url':f"https://github.com/{REPO}/blob/{inv['commit']}/{quote(item['path'],safe='/')}",'representation':'full_decompressed_utf8' if rel.endswith('.gz') else 'full_utf8'};total+=item['size']
 hashes={}
 for rel in sorted(rows,key=rank):
  h=rows[rel]['source_sha256']
  if h in hashes:rows[rel].update(representation='exact_duplicate',represented_by=hashes[h],proof={'sha256_equal':True})
  else:hashes[h]=rel
 for rel,row in rows.items():
  if rel.endswith('.csv') and row['representation']=='full_utf8' and rel[:-4]+'.json' in rows:
   twin=rel[:-4]+'.json';proof=csv_proof(snap/rel,snap/twin)
   if proof:row.update(representation='json_projection_equivalent',represented_by=twin,proof=proof)
 for rel,row in rows.items():
  if not rel.endswith('.gz'):continue
  h=hashlib.sha256();n=0
  with gzip.open(snap/rel,'rb') as f:
   for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
  row.update(decompressed_bytes=n,decompressed_sha256=h.hexdigest())
  if h.hexdigest() in hashes:row.update(representation='gzip_exact_mirror',represented_by=hashes[h.hexdigest()],proof={'decompressed_sha256_equal':True})
 for r in rules.get('files',[]):
  assert r['path'] in rows,'Rule not in authoritative tree: '+r['path'];assert rows[r['path']]['source_sha256']==r['expected_sha256'],'Stale rule: '+r['path']
  assert r.get('reason')
  if r['representation'] not in ('source_holding_catalogued','transport_catalogued'):assert r.get('proof'),'Missing equivalence proof'
  rows[r['path']].update({k:v for k,v in r.items() if k not in ('path','expected_sha256')})
  if r['representation']=='json_whitespace_compacted':
   assert pathlib.Path(r['rendered_local_path']).is_file() and digest(pathlib.Path(r['rendered_local_path']))==r['proof']['rendered_sha256']
   assert r['proof']['all_lexical_tokens_identical'] is True and r['proof']['source_sha256']==rows[r['path']].get('decompressed_sha256',r['expected_sha256'])
 supplements=rules.get('supplements',[])
 for s in supplements:
  p=pathlib.Path(s['local_path']);assert p.is_file() and digest(p)==s['sha256'];assert all(x in rows for x in s['sources'])
 names={s['name'] for s in supplements}
 def check_refs(rel,seen):
  assert rel not in seen,'Circular representation: '+rel
  ts=rows[rel].get('represented_by',[]);ts=[ts] if isinstance(ts,str) else ts
  for t in ts:
   if t in rows:check_refs(t,seen|{rel})
   else:assert t in names,'Missing referenced representation: '+t
 for rel in rows:check_refs(rel,set())
 full=sorted([r for r in rows if rows[r]['representation'] in ('full_utf8','full_decompressed_utf8','json_whitespace_compacted')],key=rank)
 for i,rel in enumerate(full,1):
  bodypath=pathlib.Path(rows[rel].get('rendered_local_path',str(snap/rel)));n,h=body_metadata(bodypath);rows[rel].update(section_id=f'F{i:04d}',content_bytes=n,content_sha256=h)
 for i,s in enumerate(supplements,1):
  n,h=body_metadata(pathlib.Path(s['local_path']));assert h==s['sha256'];s.update(section_id=f'S{i:04d}',content_bytes=n,content_sha256=h)
 summary={'schema':'f4-comprehensive-text-coverage-v2','commit':inv['commit'],'repo':REPO,'root':inv['root'],'final_verified':inv.get('final_verified',False),'source_file_count':len(rows),'source_encoded_bytes':total,'representation_counts':dict(collections.Counter(r['representation'] for r in rows.values())),'source_files':[{k:v for k,v in rows[r].items() if k!='rendered_local_path'} for r in sorted(rows)],'supplements':[{k:v for k,v in s.items() if k!='local_path'} for s in supplements],'input_exclusions':rules.get('input_exclusions',[]),'coverage_proofs':rules.get('coverage_proofs',[])}
 (audit/'coverage-before-output.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');sections=[];outpath.parent.mkdir(parents=True,exist_ok=True)
 with outpath.open('wb') as o:
  def w(s):o.write(s.encode('utf-8'))
  if a.allow_draft:w('ASSEMBLY REHEARSAL — NOT FOR DELIVERY\nFinal publication gate remains open.\n\n')
  w(f"F4 Autonomous Weapons Safeguards Audit\nComplete Research Results in One Text File\n\nResearch cutoff: 25 October 2026\nCanonical GitHub commit: {inv['commit']}\nPackage: https://github.com/{REPO}/tree/{inv['commit']}/{inv['root'].rstrip('/')}\n\n")
  w('How to read this file\n=====================\nThe master report and findings come first, followed by the guide, ranked reading pack, authored research and adversarial reviews, evidence, accounting, methodology, scripts and complete lead appendices. Search a section ID or filename. Prior drafts and critiques are retained as an audit trail; the final master report controls interpretation. Preliminary matches are not verified safeguards, active programs or allocated spending.\n\n')
  w('Representation and scope\n========================\nEvery published file in the pinned package is inventoried with exact size, SHA-256, Git blob SHA and canonical link. All authored findings and unique substantive results are represented. Proven equivalent CSV/JSON, byte and gzip copies are not repeated. Compressed text included here is decompressed without truncation. Unrelated original input corpora and input-derived caches, third-party article bodies, and private working caches are not reproduced; every such source holding is explicitly catalogued. Relative links inside preserved source documents refer to corresponding sections or their pinned repository links, not required local workspaces.\n\n')
  for note in rules.get('front_matter_notes',[]):w(note+'\n\n')
  w(f"Coverage: {len(rows):,} published files, {total:,} encoded source bytes, {len(full):,} full source sections and {len(supplements):,} explicit derived supplements.\n\nThe master report follows immediately. Detailed contents appear after it.\n")
  def emit(meta,p,derived=False):
   name=meta.get('path',meta.get('name'));sid=meta['section_id'];w('\n'+'='*80+'\n'+sid+'  '+name+'\n'+'='*80+'\n')
   if derived:w(meta['description']+'\n'+('Sources: '+', '.join(meta['sources']) if meta['sources'] else 'Source scope: newly authored assembly code; applies to the pinned inventory.')+'\n')
   else:w('Canonical source: '+meta['github_url']+'\nSource SHA-256: '+meta['source_sha256']+'\nRepresentation: '+meta['representation']+'\n')
   w('Content bytes: '+str(meta['content_bytes'])+'\nContent SHA-256: '+meta['content_sha256']+'\nBEGIN '+('DERIVED' if derived else 'SOURCE')+' CONTENT\n');start=o.tell()
   with (p.open('rb') if derived else content(p)) as f:shutil.copyfileobj(f,o)
   sections.append({'id':sid,'source':name,'byte_start':start,'byte_length':meta['content_bytes'],'rendered_sha256':meta['content_sha256']});w('\nEND '+('DERIVED' if derived else 'SOURCE')+' CONTENT\n')
  if 'report.md' in full:emit(rows['report.md'],pathlib.Path(rows['report.md'].get('rendered_local_path',str(snap/'report.md'))))
  w('\nContents\n========\n')
  for rel in full:w(rows[rel]['section_id']+'  '+rel+(' (above)' if rel=='report.md' else '')+'\n')
  for s in supplements:w(s['section_id']+'  '+s['name']+'\n')
  w('I0001  Complete file inventory and representation audit\n')
  # Put all authored prose, including archive-only research memos, before data.
  for rel in full:
   if rel!='report.md' and rel.endswith('.md'):emit(rows[rel],pathlib.Path(rows[rel].get('rendered_local_path',str(snap/rel))))
  for s in supplements:
   if s['name'].endswith('.md'):emit(s,pathlib.Path(s['local_path']),True)
  for rel in full:
   if rel!='report.md' and not rel.endswith('.md'):emit(rows[rel],pathlib.Path(rows[rel].get('rendered_local_path',str(snap/rel))))
  for s in supplements:
   if not s['name'].endswith('.md'):emit(s,pathlib.Path(s['local_path']),True)
  w('\n'+'='*80+'\nI0001  Complete file inventory and representation audit\n'+'='*80+'\n'+json.dumps(summary,ensure_ascii=False,indent=2)+'\n\nEND OF COMPLETE F4 RESEARCH COMPENDIUM\nNo output section was truncated.\n')
 with outpath.open('rb') as f:
  for s in sections:
   f.seek(s['byte_start']);remain=s['byte_length'];h=hashlib.sha256()
   while remain:
    b=f.read(min(remain,1048576));assert b,'Unexpected EOF';h.update(b);remain-=len(b)
   assert h.hexdigest()==s['rendered_sha256'],'Output corruption: '+s['id']
 summary.update(output_filename=outpath.name,output_bytes=outpath.stat().st_size,output_sha256=digest(outpath),utf8_verified=True,section_readback_verified=True,sections=sections)
 (audit/'coverage-final.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in summary.items() if k not in ('source_files','supplements','sections','input_exclusions','coverage_proofs')},indent=2))
if __name__=='__main__':main()
