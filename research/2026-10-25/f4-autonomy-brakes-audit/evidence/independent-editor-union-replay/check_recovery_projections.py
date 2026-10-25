import pathlib,csv,gzip,json,hashlib,collections
R=pathlib.Path(__file__).parent;csv.field_size_limit(2**31-1)
P=pathlib.Path('/workspace/shared/f4-stage1-recovery/evidence/candidate-provenance.jsonl.gz');S=pathlib.Path('/workspace/shared/f4-stage1-recovery/input/FWI-20261016-normalized-research-context/normalized/sbir_current.jsonl.gz');F=pathlib.Path('/workspace/shared/f4-stage1-recovery/audit/recovery-core-review-sbir-uei-conflicts.json')
conflicts=json.load(F.open());conf_by_row={r['source_row']:r for r in conflicts};source_to_keys=collections.defaultdict(set);bad=[];quarantined=collections.defaultdict(set);total=0
with gzip.open(P,'rt') as f:
 for line in f:
  a=json.loads(line);total+=1
  if not a['source_file'].endswith('sbir_current.jsonl.gz'):continue
  source_to_keys[a['source_record_id']].add(a['award_key'])
  if a['source_row'] in conf_by_row:
   c=conf_by_row[a['source_row']]
   if a['award_key']==c['assigned_award_key']:bad.append({'source_row':a['source_row'],'award_key':a['award_key']})
   else:quarantined[a['source_row']].add(a['award_key'])
docs={}
with gzip.open(S,'rt') as f:
 for n,line in enumerate(f,1):
  a=json.loads(line);docs[a['document_id']]={'source_record_id':a['source_record_id'],'source_record_sha256':a['record_sha256'],'source_snapshot_sha256':a['source_snapshot_sha256'],'physical_row':n}
consumer=list(csv.DictReader(open(R/'consumer-brakes-candidate-register.csv')));edges=[];matched=0;rowdiff=[]
for c in consumer:
 for ref in json.loads(c['source_refs'] or '[]'):
  d=docs.get(ref.get('document_id'))
  if not d:continue
  keys=source_to_keys.get(d['source_record_id'],set())
  if not keys:continue
  matched+=1
  if ref.get('row')!=d['physical_row']:rowdiff.append({'consumer_key':c['award_key'],'reported_row':ref.get('row'),'actual_row':d['physical_row']})
  if keys!={c['award_key']}:
   edges.append({'consumer_key':c['award_key'],'recovery_keys':sorted(keys),'source_document_id':ref['document_id'],**d})
edges=list({(a['consumer_key'],tuple(a['recovery_keys']),a['source_record_id']):a for a in edges}.values())
res={'scope':'Same original SBIR source appearance under different key projections. Edges are not automatic financial identity merges.','provenance_rows_scanned':total,'source_provenance_sha256':hashlib.file_digest(P.open('rb'),'sha256').hexdigest(),'matched_consumer_source_references':matched,'different_key_provenance_edges':len(edges),'consumer_keys_in_different_projections':len({a['consumer_key'] for a in edges}),'recovery_keys_in_different_projections':len({k for a in edges for k in a['recovery_keys']}),'physical_row_disagreements':rowdiff,'conflict_provenance_still_attributed_to_financial_key':bad,'conflict_source_rows_represented_under_other_keys':len(quarantined),'quarantine_provenance_keys':{str(k):sorted(v) for k,v in quarantined.items()}}
(R/'recovery-source-projection-check.json').write_text(json.dumps(res,indent=2));(R/'recovery-same-source-different-key-edges.json').write_text(json.dumps(edges,indent=2));print(json.dumps({k:v for k,v in res.items() if k!='quarantine_provenance_keys'},indent=2));assert not bad and not rowdiff
