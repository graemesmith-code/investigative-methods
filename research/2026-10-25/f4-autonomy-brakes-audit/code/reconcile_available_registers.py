#!/usr/bin/env python3
"""Exact-key membership for available archive/live/OTA instruments and history QA.

Does not modify any source register or add parallel monetary populations. The
separate independent-stage1 comparator remains pending until that input arrives.
"""
from __future__ import annotations
import argparse,csv,datetime,hashlib,json,pathlib,sqlite3,sys
from decimal import Decimal
P=pathlib.Path(__file__).resolve().parents[1]
csv.field_size_limit(sys.maxsize)
GAP_PIIDS={'FD01','N0016422F3007','N0042123F3004'}
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def cents(v):
 d=Decimal(str(v))*100
 if d!=d.to_integral_value():raise ValueError('fractional cents')
 return int(d)
def money(v):return format(Decimal(v)/100,'.2f')
def read_csv(path):
 with path.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def run(args):
 rootpath=P/'evidence/brakes-candidate-register.csv';livepath=P/'evidence/live-award-register.json';actpath=P/'evidence/fpds-verified-actions.csv'
 otpaths=[P/'evidence/ota-resolution-review.json',P/'evidence/ota-keyword-followup-records.json']
 sources=[rootpath,livepath,actpath]+otpaths;before={str(f.relative_to(P)):sha(f) for f in sources}
 rootrows=read_csv(rootpath);root={r['award_key']:r for r in rootrows}
 if len(root)!=len(rootrows):raise ValueError('duplicate exact archive keys')
 live=json.loads(livepath.read_text());live_records=[r for a in live['awards'] for r in a.get('records',[])];std={r['award_key']:r for r in live_records}
 if len(std)!=len(live_records):raise ValueError('duplicate exact standard live identities')
 unresolved=[a['piid'] for a in live['awards'] if not a.get('records')]
 ota={};ota_provenance={}
 for path in otpaths:
  for rownum,t in enumerate(json.loads(path.read_text())['targets'],1):
   identities={a['primary_identity'] for a in t.get('actions',[]) if a.get('primary_identity')}
   if len(identities)!=1:raise ValueError('OTA target lacks a unique complete primary identity')
   key=next(iter(identities))
   if key in ota:raise ValueError('duplicate OTA primary identity')
   ota[key]=t;ota_provenance[key]=(str(path.relative_to(P)),rownum)
 allkeys=sorted(set(root)|set(std)|set(ota));rows=[]
 for key in allkeys:
  a,b,c=root.get(key),std.get(key),ota.get(key)
  source_membership=';'.join(label for label,item in [('canonical_archive_screen',a),('standard_live_record',b),('FPDS_other_transaction_record',c)] if item is not None)
  otref,otnum=ota_provenance.get(key,('',''))
  rows.append({'exact_award_or_source_identity':key,'membership':source_membership,'archive_source_row_present':bool(a),'standard_live_record_present':bool(b),'other_transaction_record_present':bool(c),'archive_key_kind':'complete_financial_award_key' if key.startswith(('CONT_AWD_','ASST_NON_')) else 'parent_or_source_document_key' if a else 'not_archive_key','archive_primary_category_preliminary':a.get('primary_category_preliminary','') if a else '', 'standard_live_piid':b.get('piid','') if b else '', 'ota_piid':c.get('piid','') if c else '', 'standard_live_source_url':b.get('source_url','') if b else '', 'ota_source_register':otref,'ota_target_number':otnum,'money_combination_permitted':False,'scope_note':'Exact-key discovery membership only; source/document keys are not proven distinct awards; no PIID-only cross-schema equivalence inferred'})
 membership_path=P/'evidence/available-register-membership.csv'
 with membership_path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 otpiids={r['piid'] for r in ota.values()};resolved_old=[p for p in unresolved if p in otpiids]
 audit={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'available_sources_compared; independent_stage1_pending','input_sha256':before,'exact_membership_counts':{'archive_screen_keys':len(root),'standard_live_records':len(std),'other_transaction_primary_identities':len(ota),'archive_standard_intersection':len(set(root)&set(std)),'archive_ota_intersection':len(set(root)&set(ota)),'standard_ota_intersection':len(set(std)&set(ota)),'standard_live_only_relative_to_archive':len(set(std)-set(root)),'OTA_only_relative_to_archive':len(set(ota)-set(root)),'union_exact_source_or_instrument_keys':len(allkeys)},'standard_live_candidates':len(live['awards']),'standard_live_targets_without_standard_record':unresolved,'previously_unresolved_piids_with_separately_verified_OTA_identity':resolved_old,'cross_schema_warning':'PIID matches above explain resolution of named target searches, but complete OTA primary identities remain distinct schema-specific keys; no blind financial merge is performed.','interpretation':'This is an exact-key logical membership index, not a count of verified programs, not a new full-description register, and not a monetary sum. The original archive register is not modified. Independent-stage1 is not yet materialized and must not be added as disjoint population.','membership_csv':'evidence/available-register-membership.csv'}
 # Verify the instructed acquisition-history examples directly against canonical
 # transaction identities. This is separate from source-internal reconciliation.
 acts=read_csv(actpath);gaprows=[];gapcases=[];c=sqlite3.connect('file:'+str(args.sqlite)+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;sourcehashes={}
 for piid in sorted(GAP_PIIDS):
  target=[r for r in acts if r['piid']==piid and '2018-10-01'<=r['signed_date'][:10]<='2026-09-30']
  keys={r['award_key'] for r in target}
  if len(keys)!=1:raise ValueError('nonunique scoped live key for history comparison')
  key=next(iter(keys));canonical={r['tx']:dict(r) for r in c.execute('SELECT * FROM financial WHERE award=?',(key,))};matched=[];missing=[];conflicts=[]
  for r in target:
   tx='_'.join([r['agency_id'],r['parent_agency_id'],r['piid'],r['modification'],r['parent_piid'],r['transaction'] or '0']);amount=cents(r['obligation_usd']);day=r['signed_date'][:10]
   if tx in canonical:
    old=canonical[tx];matched.append(tx)
    if old['cents']!=amount or old['action_date']!=day:conflicts.append({'transaction_key':tx,'archive_cents':old['cents'],'live_cents':amount,'archive_date':old['action_date'],'live_date':day})
   else:
    missing.append((tx,amount));gaprows.append({'award_key':key,'piid':piid,'transaction_key':tx,'modification':r['modification'],'transaction_number':r['transaction'] or '0','signed_date':day,'live_obligation_cents':amount,'live_obligation_usd':money(amount),'archive_action_present':False,'scope':'FY2019-FY2026 only, 2018-10-01 through 2026-09-30','source_url':r['source_url'],'response_sha256':r['response_sha256'],'retrieved_utc':r['retrieved_utc'],'source_register':'evidence/fpds-verified-actions.csv'})
  for old in canonical.values():
   sf=pathlib.Path(old['source_file'])
   if sf.name not in sourcehashes:sourcehashes[sf.name]=sha(sf)
  ca=sum((r['cents'] for r in canonical.values() if 2019<=r['fy']<=2026 and r['cents'] is not None),0);la=sum(cents(r['obligation_usd']) for r in target)
  gapcases.append({'award_key':key,'piid':piid,'archive_actions':len(canonical),'live_actions_in_same_fiscal_window':len(target),'shared_exact_transaction_keys':len(matched),'shared_date_or_cent_conflicts':conflicts,'missing_from_acquired_archive_actions':len(missing),'archive_net_obligations_cents':ca,'live_net_obligations_same_window_cents':la,'live_minus_archive_cents':la-ca,'live_minus_archive_usd':money(la-ca),'sum_missing_action_cents':sum(a for tx,a in missing),'first_missing_action':min((r['signed_date'] for r in gaprows if r['award_key']==key),default=''),'last_missing_action':max((r['signed_date'] for r in gaprows if r['award_key']==key),default=''),'finding':'Shared acquired actions agree exactly; missing historical actions demonstrate incomplete acquisition-history coverage, not merely the newest-quarter public-release delay.'})
  if conflicts or la-ca!=sum(a for tx,a in missing):raise ValueError('history comparison conflict or unexplained difference')
 c.close()
 gapfile=P/'evidence/acquisition-history-missing-actions.csv'
 with gapfile.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(gaprows[0]));w.writeheader();w.writerows(gaprows)
 history={'generated_utc':audit['generated_utc'],'status':'verified_selected_examples','fiscal_window':'FY2019-FY2026: 2018-10-01 through 2026-09-30','source_hashes':{'canonical_financial_compressed_inputs':sourcehashes,'fpds_action_register_sha256':before['evidence/fpds-verified-actions.csv'],'archive_screen_register_sha256':before['evidence/brakes-candidate-register.csv']},'cases':gapcases,'scope_limit':'These are three selected positive counterexamples to full acquisition-history coverage. They do not estimate all missing actions in the corpus and do not imply any missing action is safeguard-specific spending. No original ledger is patched, no source-internal monetary error is alleged, and no raw provenance is invented. Exact source acquisition/filtering cause is not independently established.','missing_action_register':'evidence/acquisition-history-missing-actions.csv'}
 (P/'audit/acquisition-history-coverage.json').write_text(json.dumps(history,indent=2)+'\n')
 after={str(f.relative_to(P)):sha(f) for f in sources};audit['input_sha256_after_read']=after;audit['inputs_stable_during_read']=before==after
 if before!=after:audit['status']='inputs_changed_retry_required'
 (P/'audit/available-register-membership.json').write_text(json.dumps(audit,indent=2)+'\n')
 print(json.dumps({'membership':audit['exact_membership_counts'],'stable_inputs':before==after,'history_cases':[{k:r[k] for k in ['piid','archive_actions','live_actions_in_same_fiscal_window','missing_from_acquired_archive_actions','live_minus_archive_usd']} for r in gapcases],'shared_action_conflicts':sum(len(r['shared_date_or_cent_conflicts']) for r in gapcases)},indent=2))
 return 0 if before==after else 3
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--sqlite',type=pathlib.Path,default=pathlib.Path('/workspace/scratch/f4-data-complete/screen.sqlite'));sys.exit(run(a.parse_args()))
