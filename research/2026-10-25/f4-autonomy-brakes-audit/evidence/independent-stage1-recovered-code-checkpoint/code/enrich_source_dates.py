#!/usr/bin/env python3
"""Recover performance dates and institutional anchors from original USAspending source tables.

No summed monetary values are produced: award-level snapshot values are not action obligations.
The award key is used exactly, with no parent/child/recipient fuzzy merge. Duplicate source
appearances are counted; date variants collapse only equal normalized values and provenance.
Dates are selected from the latest action date, then latest last_modified_date. If source rows
remain tied and disagree, selected field is null and alternatives remain explicitly recorded.
"""
from __future__ import annotations
import collections,datetime as dt,hashlib,json,pathlib,sys
import pyarrow.parquet as pq
ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE_FIELDS=['period_of_performance_start_date','period_of_performance_current_end_date','period_of_performance_potential_end_date','ordering_period_end_date']
META_FIELDS=['award_id_piid','award_id_fain','award_id_uri','parent_award_agency_id','parent_award_id_piid','award_or_idv_flag','award_type_code','award_type','parent_award_type_code','parent_award_type','awarding_agency_code','awarding_agency_name','awarding_sub_agency_code','awarding_sub_agency_name','awarding_office_code','awarding_office_name','funding_agency_code','funding_agency_name','funding_sub_agency_code','funding_sub_agency_name','funding_office_code','funding_office_name','recipient_name','recipient_uei','product_or_service_code','naics_code']
MONEY_FIELDS=['total_dollars_obligated','total_obligated_amount','current_total_value_of_award','potential_total_value_of_award']
KEY_FIELDS=['contract_transaction_unique_key','contract_award_unique_key','assistance_transaction_unique_key','assistance_award_unique_key']
EXTRA_FIELDS=['action_date','action_date_fiscal_year','last_modified_date','initial_report_date','federal_action_obligation']
DATE_ERRORS=collections.Counter()
def clean(v):
 if v is None:return None
 s=str(v).strip()
 return s or None

def normdate(v):
 s=clean(v)
 if s is None:return None
 try:
  if s[4:5]=='-' and s[7:8]=='-':return dt.date.fromisoformat(s[:10]).isoformat()
  for f in ('%m/%d/%Y','%m/%d/%Y %H:%M:%S','%Y%m%d'):
   try:return dt.datetime.strptime(s,f).date().isoformat()
   except ValueError:pass
 except (ValueError,IndexError):pass
 DATE_ERRORS[s]+=1
 return None

def modified_sort(v):
 s=clean(v)
 if s is None:return ''
 # Source last_modified_date is sortable ISO; normalize known non-ISO formats to full ISO.
 try:
  if s[4:5]=='-' and s[7:8]=='-':return dt.datetime.fromisoformat(s.replace('Z','+00:00')).isoformat()
  for f in ('%m/%d/%Y %H:%M:%S','%m/%d/%Y'):
   try:return dt.datetime.strptime(s,f).isoformat()
   except ValueError:pass
 except ValueError:pass
 return s

awards={};inputs=[];appearances=0;transaction_keys=set();missing_key=0;source_key_sets={}
for path in sorted((ROOT/'input').rglob('*_transactions_source.parquet')):
 pf=pq.ParquetFile(path);schema=pf.schema_arrow.names
 cols=[x for x in KEY_FIELDS+DATE_FIELDS+META_FIELDS+MONEY_FIELDS+EXTRA_FIELDS if x in schema]
 stats={'file':str(path.relative_to(ROOT)),'rows':0,'sha256':hashlib.file_digest(path.open('rb'),'sha256').hexdigest(),'schema':schema,'selected_columns':cols,'missing_date_columns':[x for x in DATE_FIELDS if x not in schema],'missing_award_keys':0,'unique_award_keys':0,'unique_transaction_keys':0,'negative_action_rows':0}
 file_awards=set();file_transactions=set()
 for batch in pf.iter_batches(columns=cols,batch_size=16384):
  for row in batch.to_pylist():
   appearances+=1;stats['rows']+=1
   key=clean(row.get('contract_award_unique_key') or row.get('assistance_award_unique_key'))
   tx=clean(row.get('contract_transaction_unique_key') or row.get('assistance_transaction_unique_key'))
   if tx:transaction_keys.add(tx);file_transactions.add(tx)
   try:
    if float(row.get('federal_action_obligation') or 0)<0:stats['negative_action_rows']+=1
   except (TypeError,ValueError):pass
   if not key:missing_key+=1;stats['missing_award_keys']+=1;continue
   file_awards.add(key)
   a=awards.setdefault(key,{'source_rows':0,'sources':collections.Counter(),'metadata':collections.defaultdict(set),'variants':{},'latest_rank':('',''),'latest_rows':{}})
   a['source_rows']+=1;a['sources'][path.name]+=1
   for f in META_FIELDS:
    v=clean(row.get(f))
    if v:a['metadata'][f].add(v)
   action=normdate(row.get('action_date'));modified=modified_sort(row.get('last_modified_date'))
   rank=(action or '',modified)
   d={f:normdate(row.get(f)) for f in DATE_FIELDS}
   variant=json.dumps(d,sort_keys=True)
   v=a['variants'].setdefault(variant,{'dates':d,'source_row_appearances':0,'sources':set(),'first_action_date':action,'last_action_date':action,'transaction_keys':set()})
   v['source_row_appearances']+=1;v['sources'].add(path.name)
   if tx:v['transaction_keys'].add(tx)
   if action:
    v['first_action_date']=min(v['first_action_date'] or action,action);v['last_action_date']=max(v['last_action_date'] or action,action)
   chosen={**d,**{f:clean(row.get(f)) for f in MONEY_FIELDS},'action_date':action,'last_modified_date':clean(row.get('last_modified_date')),'transaction_key':tx}
   chosenkey=json.dumps(chosen,sort_keys=True)
   if rank>a['latest_rank']:a['latest_rank']=rank;a['latest_rows']={}
   if rank==a['latest_rank']:
    c=a['latest_rows'].setdefault(chosenkey,{**chosen,'sources':set()});c['sources'].add(path.name)
 stats['unique_award_keys']=len(file_awards);stats['unique_transaction_keys']=len(file_transactions);inputs.append(stats)
 print(json.dumps({k:v for k,v in stats.items() if k not in ('schema','selected_columns')}),flush=True)

out=ROOT/'evidence/award-date-fields.jsonl';summary=collections.Counter()
with out.open('w') as f:
 for key,a in sorted(awards.items()):
  latest=list(a['latest_rows'].values());selected={};conflicts={}
  for field in DATE_FIELDS+MONEY_FIELDS:
   values=sorted({r.get(field) for r in latest},key=lambda x:(x is not None,str(x)))
   selected[field]=values[0] if len(values)==1 else None
   if len(values)>1:conflicts[field]=values
  for row in latest:row['sources']=sorted(row['sources'])
  variants=[]
  for v in a['variants'].values():
   v['sources']=sorted(v['sources']);v['unique_transaction_count']=len(v.pop('transaction_keys'));variants.append(v)
  variants.sort(key=lambda x:json.dumps(x['dates'],sort_keys=True))
  record={'award_key':key,'source_row_appearances':a['source_rows'],'source_files':dict(sorted(a['sources'].items())),'date_selection_method':'max action_date, then max last_modified_date; conflicting tied field -> null; no forward-fill','latest_source_action_date':a['latest_rank'][0] or None,'latest_source_last_modified_sort':a['latest_rank'][1] or None,**selected,'date_or_money_selection_conflicts':conflicts,'latest_source_rows':latest,'date_variants':variants,'institutional_and_award_metadata':{k:sorted(v) for k,v in sorted(a['metadata'].items())}}
  f.write(json.dumps(record,sort_keys=True)+'\n')
  summary['awards']+=1
  for field in DATE_FIELDS:
   if selected[field] is not None:summary['selected_nonnull_'+field]+=1
  if conflicts:summary['awards_with_latest_tied_field_conflicts']+=1
  if len(variants)>1:summary['awards_with_multiple_date_variants']+=1
  if any(x.upper()=='IDV' for x in a['metadata'].get('award_or_idv_flag',[])):summary['idv_award_keys']+=1

manifest={'created_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'script':str(pathlib.Path(__file__).relative_to(ROOT)),'pyarrow_version':__import__('pyarrow').__version__,'inputs':inputs,'source_row_appearances':appearances,'unique_transaction_keys':len(transaction_keys),'missing_award_key_rows':missing_key,'summary':dict(summary),'unparsed_date_values':dict(DATE_ERRORS),'output':str(out.relative_to(ROOT)),'output_sha256':hashlib.file_digest(out.open('rb'),'sha256').hexdigest(),'selection':'Exact canonical award key; choose maximum action_date then maximum last_modified_date. Tied field disagreement returns null and alternatives. No missing-date forward fill. All date variants preserved.','monetary_semantics':'Selected total_dollars_obligated/total_obligated_amount and current/potential_total_value_of_award are source award snapshots, NOT transaction obligations or additive values. End dates do not prove activity or exercised options.','blindspots':['Archive snapshot 2026-10-16, not current 2026-10-25. Live follow-up required.','Source-table date fields are reported administrative dates, not proof of work performed, option exercise, funding or unclassified technical scope.','Assistance sources may lack potential end date; null is not zero or no continuation.','Different transaction dates can report different period end dates; latest administrative modification controls selection.','Archive selection is not a complete census of all US national security spending, classified awards, OTAs, second-tier subawards, or all institutional-office aliases.']}
(ROOT/'audit/source-date-enrichment.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({k:v for k,v in manifest.items() if k!='inputs'},indent=2))
