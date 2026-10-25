import pathlib,csv,gzip,json,hashlib,re
R=pathlib.Path(__file__).parent
S=pathlib.Path('/workspace/shared/f4-stage1-recovery/input/FWI-20261016-normalized-research-context/normalized/sbir_current.jsonl.gz')
C=pathlib.Path('/workspace/shared/f4-editor-recovery/sources/evidence/live-technical-scope-review.csv')
rows=list(csv.DictReader(C.open()));want={int(r['source_row']):r for r in rows};source={};count=0
with gzip.open(S,'rt') as f:
 for n,line in enumerate(f,1):
  count=n
  if n in want:source[n]=json.loads(line)
norm=lambda s:re.sub('[^A-Z0-9]','',s.upper())
checks=[]
for r in rows:
 n=int(r['source_row']);s=source[n];z={'physical_row':n,'piid':r['piid'],'source_document_id':s['document_id'],'source_record_sha256':s['record_sha256'],'source_snapshot_sha256':s['source_snapshot_sha256'],'piid_matches':norm(r['piid'])==norm(s['award_key']),'title_matches':r['title']==s['title'],'stored_record_hash_matches':r['source_row_sha256']==s['record_sha256'],'stored_snapshot_hash_matches':r['input_snapshot_sha256']==s['source_snapshot_sha256']};checks.append(z)
out={'status':'new post-loss replay against re-materialized original normalized SBIR input; identifiers/hashes only, no source bodies exported','source_gzip_sha256':hashlib.file_digest(S.open('rb'),'sha256').hexdigest(),'source_normalized_records':count,'crosswalk_sha256':hashlib.file_digest(C.open('rb'),'sha256').hexdigest(),'crosswalk_rows':len(rows),'all_match':all(all(r[k] for k in ['piid_matches','title_matches','stored_record_hash_matches','stored_snapshot_hash_matches']) for r in checks),'caveat':'Stored record and snapshot hashes verify the supplied source linkage, not independently reconstructed hashes of pre-normalization source serialization. This checks source linkage, not achieved technical effectiveness.','checks':checks}
(R/'sbir-crosswalk-recheck.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k!='checks'});assert out['all_match']
