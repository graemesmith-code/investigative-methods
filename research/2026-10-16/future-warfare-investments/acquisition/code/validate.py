#!/usr/bin/env python3
"""Check downloaded hashes, archive integrity, canonical lineage/counts and overlap. No network."""
import collections,csv,gzip,hashlib,json,pathlib,shutil,zipfile,re
import pandas as pd,pyarrow.parquet as pq
from acquire import DATA,ROOT,save_json
checks=[]
def check(name,passed,detail,severity='error'):checks.append({'check':name,'passed':bool(passed),'severity':severity,'detail':detail})
manifest=[json.loads(x) for x in (ROOT/'validation/http_manifest.jsonl').read_text().splitlines()];downloaded=[m for m in manifest if m['outcome']=='downloaded'];rawbytes=0
for m in downloaded:
 p=DATA/m['relative_path'];h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 rawbytes+=p.stat().st_size;check('sha256:'+m['relative_path'],h.hexdigest()==m['sha256'],{'bytes':p.stat().st_size,'sha256':h.hexdigest()})
 if p.suffix=='.zip':
  z=zipfile.ZipFile(p);bad=z.testzip();check('zip_crc:'+m['relative_path'],bad is None,{'members':len(z.namelist()),'bad_member':bad})
check('raw_download_budget',rawbytes<=15_000_000_000,{'downloaded_bytes':rawbytes,'budget_bytes':15_000_000_000});check('disk_headroom',shutil.disk_usage(DATA).free>=6_000_000_000,{'free_bytes':shutil.disk_usage(DATA).free})
canonical_profiles=[]
for p in sorted((DATA/'normalized').glob('*.parquet')):
 schema=pq.read_schema(p)
 if 'document_id' not in schema.names or 'raw_locator' not in schema.names:continue
 df=pd.read_parquet(p,columns=[k for k in ['document_id','source_url','raw_locator','source_snapshot_sha256','text','action_date','fiscal_year','transaction_key','award_key','record_sha256'] if k in schema.names]);n=len(df);missing={k:int(df[k].isna().sum()+(df[k]=='').sum()) for k in df.columns};duplicates=int(df.document_id.duplicated().sum());bad_dates=int((df.action_date.notna()&~df.action_date.map(lambda x:x.isoformat() if hasattr(x,'isoformat') else x).fillna('').str.match(r'^\d{4}-\d{2}-\d{2}$')).sum()) if 'action_date' in df else 0
 canonical_profiles.append({'file':p.name,'rows':n,'missing':missing,'duplicate_document_ids':duplicates,'malformed_nonempty_dates':bad_dates})
 for k in ['document_id','source_url','raw_locator','source_snapshot_sha256']:check('canonical_lineage:'+p.name+':'+k,missing.get(k,0)==0,{'missing':missing.get(k),'rows':n})
 check('date_format:'+p.name,bad_dates==0,{'malformed_nonempty':bad_dates})
 if (ROOT/'validation'/(p.stem+'_profile.json')).exists():
  prof=json.loads((ROOT/'validation'/(p.stem+'_profile.json')).read_text());expected=prof.get('retained_rows');check('canonical_count:'+p.name,n==expected,{'parquet_rows':n,'profile_retained_rows':expected})
for p in (ROOT/'validation').glob('usaspending_*_source_table_profiles.json'):
 source=p.name.removesuffix('_source_table_profiles.json');j=json.loads(p.read_text());prime=sum(r['rows'] for r in j if r['kind']=='transactions');allrows=sum(r['rows'] for r in j);status=json.loads((ROOT/'evidence'/f'{source}_status.json').read_text());check('download_status_total:'+source,allrows==status['total_rows'],{'parsed_all_csv_rows':allrows,'generator_reported_rows':status['total_rows']});check('download_cap:'+source,max(r['rows'] for r in j)<500000,{'all_csv_rows':allrows,'individual_csv_rows':{r['kind']:r['rows'] for r in j},'requested_limit':500000,'rule':'No individual CSV reaches the requested row ceiling; prime completeness additionally compared with independent count.'},severity='coverage_warning');cp=ROOT/'evidence'/f'{source}_count.json'
 if cp.exists():
  counts=json.loads(cp.read_text())['results'];expected=sum(counts.values());dp=ROOT/'evidence'/f'{source}_download_count.json';dc=json.loads(dp.read_text())['calculated_count'] if dp.exists() else None;check('api_count_vs_download:'+source,prime==expected,{'search_api_transaction_count':expected,'download_route_count':dc,'parsed_prime_transactions':prime,'note':'Search and download-route counts can differ; inspect route-specific comparison.'},severity='coverage_warning')
  if dc is not None:check('download_route_count_vs_download:'+source,prime==dc,{'download_route_count':dc,'parsed_prime_transactions':prime})
 sp=ROOT/'evidence'/f'{source}_subaward_download_count.json'
 if sp.exists():
  expected_sub=json.loads(sp.read_text())['calculated_count'];actual_sub=sum(r['rows'] for r in j if r['kind']=='subawards');check('subaward_count_vs_download:'+source,actual_sub==expected_sub,{'subaward_count_endpoint':expected_sub,'parsed_subaward_rows':actual_sub,'note':'Generator output count matches actual CSV; separate count endpoint differs slightly. Cause unestablished.'},severity='coverage_warning')
 moneyinvalid={r['csv']:{k:v['invalid_nonempty'] for k,v in r['money_value_checks'].items() if v['invalid_nonempty']} for r in j};check('monetary_numeric_parse:'+source,all(not x for x in moneyinvalid.values()),moneyinvalid)
lp=json.loads((ROOT/'validation/doe_ldrd_finance_profile.json').read_text())
for k,v in lp['checks'].items():check('ldrd_finances:'+k,v,{'rows':lp['rows']})
# Exact transaction overlap is measurable. It is not additive spending.
usas={}
for source in sorted(p.stem for p in (DATA/'normalized').glob('usaspending_dod_rd_fy*.parquet') if re.fullmatch(r'usaspending_dod_rd_fy\d{4}',p.stem))+['usaspending_darpa','usaspending_dod_capabilities','usaspending_dod_rd_contracts','usaspending_dod_research_grants']+sorted(p.stem for p in (DATA/'normalized').glob('usaspending_dod_capabilities_fy*.parquet') if re.fullmatch(r'usaspending_dod_capabilities_fy\d{4}',p.stem)):
 p=DATA/'normalized'/f'{source}.parquet'
 if p.exists():usas[source]=pd.read_parquet(p,columns=['transaction_key'])['transaction_key'].dropna()
overlaps=[]
for i,(name,keys) in enumerate(usas.items()):
 for other,okeys in list(usas.items())[i+1:]:overlaps.append({'left':name,'right':other,'shared_transaction_keys':len(set(keys)&set(okeys))})
union=set(x for ks in usas.values() for x in ks);save_json(ROOT/'validation/overlap.json',{'transaction_rows_across_extracts':sum(len(x) for x in usas.values()),'unique_transaction_keys':len(union),'pairwise_overlap':overlaps,'warning':'Do not sum extracts. Same SBIR award, announcement, subaward, budget and project disclosures may represent same investment. Cross-source amounts and grains remain separate.'})
# Normalized storage inventory with exact hashes and physical rows.
normalized=[]
for p in sorted((DATA/'normalized').glob('*')):
 if not p.is_file():continue
 h=hashlib.sha256(p.read_bytes()).hexdigest();item={'path':str(p.relative_to(DATA)),'bytes':p.stat().st_size,'sha256':h}
 if p.suffix=='.parquet':item['rows']=pq.ParquetFile(p).metadata.num_rows
 normalized.append(item)
save_json(ROOT/'validation/normalized_manifest.json',normalized);save_json(ROOT/'validation/canonical_profiles.json',canonical_profiles);save_json(ROOT/'validation/checks.json',{'checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] and c['severity']=='error' for c in checks),'coverage_warnings':sum(not c['passed'] and c['severity']=='coverage_warning' for c in checks),'raw_bytes':rawbytes,'normalized_bytes':sum(x['bytes'] for x in normalized)})
print(json.dumps({'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] and c['severity']=='error' for c in checks),'coverage_warnings':sum(not c['passed'] and c['severity']=='coverage_warning' for c in checks),'raw_bytes':rawbytes,'unique_transaction_keys':len(union),'normalized_bytes':sum(x['bytes'] for x in normalized)}))
if any(not c['passed'] and c['severity']=='error' for c in checks):raise SystemExit(1)
