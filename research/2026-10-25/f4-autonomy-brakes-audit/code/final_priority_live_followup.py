#!/usr/bin/env python3
"""Six fixed archival leads; public APIs only, separate from the core register.

Uses the package's durable public retrieval helper and FPDS parser. No Exa,
paid API, source outreach, Git ref change, or core register mutation.
"""
import argparse,csv,datetime,decimal,gzip,hashlib,importlib.util,json,pathlib,re
P=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('live_verify',P/'code/live_verify.py');live=importlib.util.module_from_spec(spec);spec.loader.exec_module(live)
TARGETS=['N6426725C7123','W5170125CA287','FA864925P0470','FA864924P0435','FA864923P0469','W911NF24P0033']
DISPOSITIONS={
 'N6426725C7123':'A/B-enabling candidate: NOEMON electronic-warfare tactics include ROE learning/configuration in the archived technical abstract. Public award funding and record-current dates do not prove legal-compliance testing, deployed constraint enforcement, or completed capability.',
 'W5170125CA287':'C primary, B secondary candidate: configurable guardrails, policy enforcement and human workflows for Army AI including joint targeting. No explicit LOAC/proportionality enforcement demonstrated by the award record or archived abstract; general regulatory compliance is not a legal-engagement guarantee.',
 'FA864925P0470':'A-enabling decision-support candidate: legal/ROE guidance retrieval for Security Forces. Distinguish retrieval and advice from enforced engagement authorization or onboard normative testing.',
 'FA864924P0435':'Historical A-enabling JAG/ROE retrieval and workflow support; an ended award record is not evidence of current 2026 deployment or a continuation.',
 'FA864923P0469':'Historical A-enabling legal-review assistant: archived scope explicitly covers targeting-package inconsistencies, civilian/military labels, civilian damage and proportionality. Demonstrates normative research scope, not autonomous enforcement or current 2026 performance.',
 'W911NF24P0033':'Historical B candidate: archived proposed Coalesce swarm interface says humans approve lethal actions. A Phase I proposal or abstract does not prove implemented, non-bypassable authorization or current deployment.'}
def norm(s):return re.sub('[^A-Z0-9]','',str(s).upper())
def transactions(record):
 url='https://api.usaspending.gov/api/v2/transactions/';page=1;results={};seen=set();complete=False;dups=0;conflicts=[];pages=[]
 while True:
  raw,meta=live.fetch(url,'POST',{'award_id':record['award_key'],'page':page,'limit':100});pages.append(meta)
  if raw is None:break
  try:obj=json.loads(raw)
  except Exception as e:meta['parse_error']=str(e);break
  rows=obj.get('results',[]);signature=tuple(x.get('id') for x in rows)
  if rows and signature in seen:meta['pagination_error']='repeated_page';break
  seen.add(signature)
  for i,row in enumerate(rows):
   key=row.get('id') or 'missing-id-page-'+str(page)+'-row-'+str(i)
   if key in results:
    dups+=1
    if results[key].get('federal_action_obligation')!=row.get('federal_action_obligation'):conflicts.append(key)
   results[key]={**row,'source_url':url,'request_page':page,'response_sha256':meta['sha256'],'retrieved_utc':meta['retrieved_utc']}
  if not obj.get('page_metadata',{}).get('hasNext'):complete=True;break
  page+=1
 nulls=sum(x.get('federal_action_obligation') is None for x in results.values());missing=sum(str(k).startswith('missing-id-page-') for k in results)
 total=sum((decimal.Decimal(str(x['federal_action_obligation'])) for x in results.values() if x.get('federal_action_obligation') is not None),decimal.Decimal(0))
 expected=decimal.Decimal(record['total_obligation_usd'])
 return {'pages':len(pages),'pagination_complete':complete,'unique_transaction_count':len(results),'duplicate_observations':dups,'conflicting_duplicate_ids':conflicts,'missing_ids':missing,'null_obligation_rows':nulls,'net_obligations_usd':str(total),'minus_award_total_usd':str(total-expected),'reconciled':complete and bool(results) and not nulls and not missing and not conflicts and total==expected,'transactions':list(results.values())}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--review',type=pathlib.Path,default=pathlib.Path('/workspace/scratch/f4-recovery-v1-canonical/evidence/ab-high-priority-review.csv'));parser.add_argument('--sbir-dir',type=pathlib.Path,default=pathlib.Path('/workspace/scratch/f4-data-complete/extracted/FWI-20261016-normalized-research-context/normalized'));args=parser.parse_args()
 live.CACHE=pathlib.Path('/workspace/scratch/f4-final-priority-live');live.CACHE.mkdir(parents=True,exist_ok=True)
 source_error=None;source_rows={};sourcehash=None
 try:
  sourcehash=hashlib.sha256(args.review.read_bytes()).hexdigest()
  for row in csv.DictReader(args.review.open()):
   for piid in TARGETS:
    if piid in row.get('award_key',''):source_rows[piid]=row
 except Exception as e:source_error=type(e).__name__+': '+str(e)
 sbirs={x:[] for x in TARGETS};sbirfiles=[]
 for name in ['sbir.jsonl.gz','sbir_current.jsonl.gz']:
  f=args.sbir_dir/name
  try:
   info={'name':name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'physical_rows':0}
   with gzip.open(f,'rt') as stream:
    for i,line in enumerate(stream,1):
     r=json.loads(line);info['physical_rows']=i
     matches=[piid for piid in TARGETS if norm(r.get('award_key',''))==norm(piid)]
     for piid in matches:sbirs[piid].append({'source_file':name,'source_row':i,'source_record_id':r.get('source_record_id'),'entity_name':r.get('entity_name'),'entity_identifier_as_source_entity_key':r.get('entity_key'),'title':r.get('title'),'source_url':r.get('source_url'),'record_sha256':r.get('record_sha256'),'source_snapshot_sha256':r.get('source_snapshot_sha256'),'source_row_sha256':hashlib.sha256(line.rstrip('\n').encode()).hexdigest()})
   sbirfiles.append(info)
  except Exception as e:sbirfiles.append({'name':name,'error':type(e).__name__+': '+str(e)})
 union_check=None;fullregister=args.review.parent/'brakes-candidate-register.csv'
 try:
  sourcekeys={r['award_key'] for r in csv.DictReader(fullregister.open())};targetkeys=[source_rows[x]['award_key'] for x in TARGETS if x in source_rows]
  union_check={'full_register_sha256':hashlib.sha256(fullregister.read_bytes()).hexdigest(),'full_register_distinct_keys':len(sourcekeys),'target_key_count':len(targetkeys),'keys_already_present':[k for k in targetkeys if k in sourcekeys],'net_new_keys':[k for k in targetkeys if k not in sourcekeys],'note':'Exact full award-key comparison, not short-PIID addition. This followup creates no extra source-union keys when every target is already present.'}
 except Exception as e:union_check={'error':type(e).__name__+': '+str(e),'note':'No source-union addition or count is inferred.'}
 findings=[];actions=[]
 for piid in TARGETS:
  archived=source_rows.get(piid);key=archived.get('award_key') if archived else 'CONT_AWD_'+piid+'_9700_-NONE-_-NONE-'
  finding,fpds=live.one({'piid':piid,'award_key':key,'selection_basis':'fixed_final_301_register_lead_followup'});actions+=fpds
  finding['priority']='first_three' if piid in TARGETS[:3] else 'historical_followup';finding['archival_source_row_available']=archived is not None
  finding['archival_comparison']={k:archived.get(k) for k in ['award_key','record_kinds','join_methods','financial_entity_names','obligations_fy2019_2026_usd','obligations_fy2024_2026_usd','financial_attribution','quarantined_related_sbir_candidate_keys','potential_conflicted_financial_instruments_not_attributed','source_urls']} if archived else None
  finding['archival_sbir_identity_observations']=sbirs[piid];finding['scope_disposition']=DISPOSITIONS[piid]
  for record in finding['records']:
   detail=json.loads((live.CACHE/(record['response_sha256']+'.raw')).read_bytes());recipient=detail.get('recipient') or {};uei=recipient.get('recipient_uei');record['recipient_uei']=uei
   observations=sbirs[piid];identifiers=sorted(set(norm(x['entity_identifier_as_source_entity_key']) for x in observations if x.get('entity_identifier_as_source_entity_key')));sourceueis=[x for x in identifiers if re.fullmatch('[A-Z0-9]{12}',x)];otherids=[x for x in identifiers if x not in sourceueis]
   record['sbir_recipient_identity_check']={'live_recipient_uei':uei,'source_sbir_uei_format_identifiers':sourceueis,'non_uei_format_source_identifiers':otherids,'all_source_uei_format_identifiers_match_live':all(u==norm(uei) for u in sourceueis) if sourceueis and uei else None,'legacy_identifier_note':'Nine-digit source entity keys are legacy identifiers, not 12-character UEIs; they are not compared as UEIs or silently treated as conflicts. Their mapping is not independently verified.','status':'verified_exact_PIID_and_UEI' if sourceueis and uei and all(u==norm(uei) for u in sourceueis) else 'unresolved_or_conflicted_do_not_attribute_technical_scope_without_review'}
   record['usaspending_transaction_reconciliation']=transactions(record)
  findings.append(finding)
  print(piid,finding['status'],[(r.get('recipient'),r.get('total_obligation_usd'),r.get('period_of_performance'),r.get('fpds_minus_usaspending_usd'),r['usaspending_transaction_reconciliation']['reconciled'],r['sbir_recipient_identity_check']['status']) for r in finding['records']],flush=True)
 result={'scope':'Six fixed public-source followups, separate from stable core register. Do not add these keys to the source union without an exact set comparison. No paid APIs used.','retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'review_source_sha256':sourcehash,'review_source_error':source_error,'source_union_set_check':union_check,'sbir_source_file_accounting':sbirfiles,'currentness_note':'Period-of-performance dates are record dates, not evidence of deployment or capability completion. DoD publication delay and incomplete descriptions limit negative conclusions.','findings':findings,'fpds_actions':actions}
 (P/'evidence/final-priority-live-followup.json').write_text(json.dumps(result,indent=2)+'\n')
 fields=['piid','award_key','recipient','recipient_uei','priority','status','net_obligations_usd','current_end','potential_end','fpds_action_count','fpds_reconciled','usaspending_transaction_count','usaspending_transactions_complete','usaspending_reconciled','sbir_identity_status','archival_fy2019_2026_acquired_net_usd','scope_disposition']
 with (P/'evidence/final-priority-live-followup.csv').open('w',newline='') as stream:
  writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
  for finding in findings:
   for r in finding['records'] or [{}]:
    tx=r.get('usaspending_transaction_reconciliation',{});writer.writerow({'piid':finding['piid'],'award_key':r.get('award_key'),'recipient':r.get('recipient'),'recipient_uei':r.get('recipient_uei'),'priority':finding['priority'],'status':finding['status'],'net_obligations_usd':r.get('total_obligation_usd'),'current_end':(r.get('period_of_performance') or {}).get('end_date'),'potential_end':(r.get('period_of_performance') or {}).get('potential_end_date'),'fpds_action_count':r.get('fpds_action_count'),'fpds_reconciled':r.get('fpds_complete') and decimal.Decimal(r.get('fpds_minus_usaspending_usd') or '1')==0,'usaspending_transaction_count':tx.get('unique_transaction_count'),'usaspending_transactions_complete':tx.get('pagination_complete'),'usaspending_reconciled':tx.get('reconciled'),'sbir_identity_status':r.get('sbir_recipient_identity_check',{}).get('status'),'archival_fy2019_2026_acquired_net_usd':(finding.get('archival_comparison') or {}).get('obligations_fy2019_2026_usd'),'scope_disposition':finding['scope_disposition']})
 (P/'audit/final-priority-live-retrievals.json').write_text(json.dumps({'scope':'Separate six-lead fixed followup; core request logs and award register unchanged. All requests durably logged before and after network execution.','requests':live.LOG,'request_count':len(live.LOG),'failed_request_count':sum(bool(x.get('error')) for x in live.LOG),'source_body_cache_public':False},indent=2)+'\n')
if __name__=='__main__':main()
