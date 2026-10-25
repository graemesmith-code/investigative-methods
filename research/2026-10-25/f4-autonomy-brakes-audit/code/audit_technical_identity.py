#!/usr/bin/env python3
"""Reproduce58 SBIR/entity associations from complete source rows and cached primary responses. No network or paid calls. Recreate --matches with extract_live_technical.py; DUNS and UEI namespaces remain separate."""
import json,csv,gzip,re,hashlib,collections,argparse
from pathlib import Path
base=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--normalized',type=Path,default=Path('/workspace/scratch/f4-data-complete/extracted/FWI-20261016-normalized-research-context/normalized'));parser.add_argument('--matches',type=Path,default=Path('/workspace/scratch/f4-live-technical-matches.json'));parser.add_argument('--live-cache',type=Path,default=Path('/workspace/scratch/f4-live'));args=parser.parse_args()
private=args.normalized
matches_path=args.matches
matches=json.loads(matches_path.read_text())
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def norm(s):return re.sub('[^A-Z0-9]','',str(s or '').upper())
def isuei(s):return bool(re.fullmatch('[A-Z0-9]{12}',s or ''))
wantrows={v['source_row']:k for k,v in matches.items()}
sbir={};sbir_count=0
with gzip.open(private/'sbir_current.jsonl.gz','rt',encoding='utf-8') as f:
 for i,l in enumerate(f,1):
  sbir_count=i
  if i not in wantrows:continue
  r=json.loads(l);piid=wantrows[i];ids=json.loads(r.get('identifiers_json') or '{}')
  assert norm(ids.get('Contract') or r['award_key'])==piid
  assert r['record_sha256']==matches[piid]['row_sha256']
  sbir[piid]={'row':i,'uei':str(ids.get('UEI') or '').strip(),'entity_key':r['entity_key'],'duns':str(ids.get('Duns') or ''),'name':r['entity_name'],'agency':ids.get('Agency'),'branch':ids.get('Branch'),'contract':ids.get('Contract'),'record_sha256':r['record_sha256'],'snapshot_sha256':r['source_snapshot_sha256'],'normalized_line_sha256_without_terminator':hashlib.sha256(l.rstrip('\r\n').encode('utf-8')).hexdigest(),'raw_locator':r.get('raw_locator')}
financial=collections.defaultdict(dict);fin_count=0
with gzip.open(private/'financial_actions.jsonl.gz','rt',encoding='utf-8') as f:
 for i,l in enumerate(f,1):
  fin_count=i;r=json.loads(l);key=r['award_key'];parts=key.split('_')
  if len(parts)<3 or parts[:2]!=['CONT','AWD']:continue
  piid=parts[2]
  if piid not in matches:continue
  a=financial[piid].setdefault(key,{'uei_shaped_entity_keys':set(),'nine_digit_duns_entity_keys':set(),'other_entity_keys':set(),'legal_names':set(),'source_rows':[]})
  e=str(r.get('entity_key') or '').strip()
  a['legal_names'].add(r.get('entity_name') or '')
  a['source_rows'].append(i)
  if isuei(e):a['uei_shaped_entity_keys'].add(e)
  elif re.fullmatch(r'\d{9}',e):a['nine_digit_duns_entity_keys'].add(e)
  else:a['other_entity_keys'].add(e)
livepath=base/'evidence/live-award-register.json';live=json.loads(livepath.read_text());cached=collections.defaultdict(list)
for a in live['awards']:
 for rec in a.get('records',[]):
  piid=norm(rec.get('piid') or a.get('piid'))
  if piid not in matches:continue
  digest=rec.get('response_sha256');p=args.live_cache/(str(digest)+'.raw')
  if not p.exists():cached[piid].append({'status':'cache_missing','record_award_key':rec.get('award_key'),'response_sha256':digest});continue
  assert sha(p)==digest
  x=json.loads(p.read_text());rc=x.get('recipient') or {}
  cached[piid].append({'status':'cache_hash_verified','record_award_key':rec.get('award_key'),'cached_award_key':x.get('generated_unique_award_id'),'cached_piid':x.get('piid'),'recipient_uei':rc.get('recipient_uei'),'recipient_name':rc.get('recipient_name'),'parent_recipient_uei':rc.get('parent_recipient_uei'),'parent_award':x.get('parent_award'),'awarding_agency':x.get('awarding_agency'),'response_sha256':digest,'retrieved_utc':rec.get('retrieved_utc'),'source_url':rec.get('source_url')})
rows=[];jsonrows=[]
for piid in matches:
 s=sbir[piid];f=financial[piid];lu=sorted({str(x.get('recipient_uei') or '').strip() for x in cached[piid] if isuei(str(x.get('recipient_uei') or '').strip())})
 fu=sorted(set().union(*(v['uei_shaped_entity_keys'] for v in f.values()))) if f else []
 su=s['uei'];n=len(f)
 if not isuei(su):status='source_explicit_uei_missing_or_invalid'
 elif not f:status='no_archive_financial_award_for_piid'
 elif n!=1:status='multiple_financial_award_keys_require_agency_parent_scope'
 elif not fu:status='archive_financial_uei_missing_duns_not_substitute'
 elif su not in fu:status='explicit_uei_conflict_with_all_archive_financial_recipient_ueis'
 else:status='source_explicit_uei_matches_archive_financial_recipient_set'
 if not isuei(su):ls='source_uei_unavailable'
 elif not lu:ls='cached_live_recipient_uei_unavailable'
 elif su in lu:ls='source_explicit_uei_matches_cached_live_recipient_uei'
 else:ls='source_explicit_uei_conflicts_with_cached_live_recipient_uei'
 fs={k:{kk:sorted(vv) if isinstance(vv,set) else vv for kk,vv in v.items()} for k,v in f.items()}
 scope='content linkage supported by explicit UEI; not independent verification of full SOW/deployment' if status.startswith('source_explicit_uei_matches') and ls.startswith('source_explicit_uei_matches') else 'linkage unresolved or limited; do not transfer SBIR scope to financial award without resolving identity'
 jr={'piid':piid,'source_sbir':s,'archive_financial_awards':fs,'cached_live':cached[piid],'archive_identity_status':status,'cached_live_identity_status':ls,'scope_association_limit':scope};jsonrows.append(jr)
 rows.append({'piid':piid,'sbir_source_row':s['row'],'sbir_legal_name':s['name'],'sbir_explicit_uei':su,'sbir_entity_key':s['entity_key'],'sbir_duns_separate_not_uei':s['duns'],'sbir_agency':s['agency'],'sbir_branch':s['branch'],'sbir_contract_literal':s['contract'],'financial_award_keys':json.dumps(list(f)),'financial_all_recipient_ueis':json.dumps(fu),'financial_all_recipient_legal_names':json.dumps(sorted(set().union(*(v['legal_names'] for v in f.values())))),'financial_nine_digit_duns_separate_not_uei':json.dumps(sorted(set().union(*(v['nine_digit_duns_entity_keys'] for v in f.values())))),'cached_live_recipient_ueis':json.dumps(lu),'cached_live_recipient_legal_names':json.dumps(sorted({x.get('recipient_name') for x in cached[piid] if x.get('recipient_name')})),'cached_live_full_award_keys':json.dumps(sorted({x.get('cached_award_key') for x in cached[piid] if x.get('cached_award_key')})),'archive_identity_status':status,'cached_live_identity_status':ls,'scope_association_limit':scope,'sbir_record_sha256':s['record_sha256'],'sbir_record_sha256_domain':'Stored original source-record hash, not a hash of the normalized JSONL line','normalized_source_line_sha256_without_terminator':s['normalized_line_sha256_without_terminator'],'sbir_snapshot_sha256':s['snapshot_sha256'],'cached_live_response_sha256s':json.dumps([x.get('response_sha256') for x in cached[piid]]),'source_url':matches[piid]['source_url']})
out=base/'audit';csvpath=out/'technical-58-identity-linkage-audit.csv'
with csvpath.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
accounting={'reviewed_records':len(rows),'sbir_physical_rows_scanned':sbir_count,'financial_physical_rows_scanned':fin_count,'source_rows_and_record_hashes_validated':len(sbir),'archive_status_counts':dict(collections.Counter(x['archive_identity_status'] for x in rows)),'cached_live_status_counts':dict(collections.Counter(x['cached_live_identity_status'] for x in rows)),'input_hashes':{'sbir_current.jsonl.gz':sha(private/'sbir_current.jsonl.gz'),'financial_actions.jsonl.gz':sha(private/'financial_actions.jsonl.gz'),'f4-live-technical-matches.json':sha(matches_path),'live-award-register.json':sha(livepath)},'money_mutations':0,'classification_mutations':0,'rows':jsonrows}
(out/'technical-58-identity-linkage-audit.json').write_text(json.dumps(accounting,indent=2))
print(json.dumps({k:v for k,v in accounting.items() if k!='rows'},indent=2))
for r in rows:
 if 'conflict' in r['archive_identity_status'] or 'conflict' in r['cached_live_identity_status']:print('CONFLICT',json.dumps(r,indent=2))
