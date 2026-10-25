import pathlib,json,csv,hashlib,gzip,re
R=pathlib.Path(__file__).parent
P=pathlib.Path('/workspace/shared/f4-stage1-recovery/audit/recovery-core-review-sbir-uei-conflicts.json')
E=pathlib.Path('/workspace/shared/f4-editor-recovery/sources/evidence')
raw=P.read_bytes();x=json.loads(raw);selected=list(csv.DictReader(open(E/'reviewed-cases.csv')));technical=list(csv.DictReader(open(E/'live-technical-scope-review.csv')));live=list(csv.DictReader(open(E/'combined-live-inventory.csv')))
clean=[{k:v for k,v in r.items() if k not in ['text','hits']} for r in x];(R/'conflict-identifiers-only.json').write_text(json.dumps(clean,indent=2))
s={r['award_key']:r for r in selected};t={int(r['source_row']):r for r in technical};l={r['award_key']:r for r in live};rows=[];norm=lambda a:re.sub('[^A-Z0-9]','',a.upper())
for a in clean:
 if a['assigned_award_key'] in s or a['source_row'] in t or a['assigned_award_key'] in l:
  z=dict(a);z.update(selected_case=s.get(a['assigned_award_key']),technical_crosswalk=t.get(a['source_row']),live_inventory=l.get(a['assigned_award_key']));rows.append(z)
loose={norm(r['piid']) for r in clean}&{norm(r['piid']) for r in selected+technical+live}
assert loose=={r['piid'] for r in rows}
S=pathlib.Path('/workspace/shared/f4-stage1-recovery/input/FWI-20261016-normalized-research-context/normalized/sbir_current.jsonl.gz');F=S.parent/'financial_actions.jsonl.gz';proof=[]
with gzip.open(S,'rt') as f:
 for n,line in enumerate(f,1):
  if n not in {r['source_row'] for r in rows}:continue
  a=json.loads(line);proof.append({'source_row':n,'source_document_id':a['document_id'],'source_record_sha256':a['record_sha256'],'source_snapshot_sha256':a['source_snapshot_sha256'],'entity_key':a['entity_key'],'explicit_identifiers_UEI':json.loads(a['identifiers_json'])['UEI'],'entity_name':a['entity_name'],'award_key_as_stored':a['award_key']})
financial=[];keys={r['assigned_award_key'] for r in rows}
with gzip.open(F,'rt') as f:
 for line in f:
  if not any(k in line for k in keys):continue
  a=json.loads(line)
  if a['award_key'] in keys:financial.append(a)
out={'conflict_source_sha256':hashlib.sha256(raw).hexdigest(),'conflict_rows':len(x),'intersection_count':len(rows),'selected_case_intersections':sum(r['selected_case'] is not None for r in rows),'technical_crosswalk_intersections':sum(r['technical_crosswalk'] is not None for r in rows),'live_inventory_intersections':sum(r['live_inventory'] is not None for r in rows),'normalized_PIID_discovery_intersection':sorted(loose),'rows':rows,'independently_rechecked_original_sbir_identifiers':proof,'independently_rechecked_original_financial_rows':financial,'input_hashes':{'sbir_gzip':hashlib.file_digest(S.open('rb'),'sha256').hexdigest(),'financial_gzip':hashlib.file_digest(F.open('rb'),'sha256').hexdigest()},'interpretation':'An unresolved explicit UEI contradiction blocks confident recipient-attributed technical/financial joining. It does not automatically prove a wrong award, identifier reuse, novation, or wrongdoing. Exact source hash linkage does not validate the join.'}
(R/'identity-conflict-intersections.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k not in ['rows','independently_rechecked_original_financial_rows']})
