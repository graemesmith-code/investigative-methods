#!/usr/bin/env python3
"""Archive-only name-matched ASIMOV performer continuation universe.

All named recipients are included regardless of PSC/NAICS. Name aliases are retrieval
candidates, not verified legal-entity or corporate-family assertions. Period selection
is union(CY2025-2026, FY2025-2026) to preserve Oct-Dec2024 fiscal-year records. All
monetary totals derive ONLY from exact, deduplicated financial_actions transaction keys;
subaward and SBIR stated amounts are kept separate and never added to those totals.
"""
from __future__ import annotations
import pathlib,re,json,gzip,csv,collections,hashlib,decimal,datetime
from lexicon_additional_narratives_snapshot import hits,classify
ROOT=pathlib.Path(__file__).resolve().parents[1]
ALIASES={
 'Kitware':r'\bKITWARE\b',
 'RTX / Raytheon / BBN':r'\bRTX\b|\bRAYTHEON\b|\bBBN\b|\bUNITED TECHNOLOGIES\b|\bPRATT\s*(?:&|AND)?\s*WHITNEY\b|\bCOLLINS AEROSPACE\b',
 'STR':r'\bSYSTEMS\s*(?:&|AND)\s*TECHNOLOGY\s*RESEARCH\b|\bS\.?T\.?R\.?\s*,?\s*LLC\b',
 'CoVar':r'\bCOVAR\b',
 'UNSW':r'\bUNIVERSITY OF NEW SOUTH WALES\b|\bNEW SOUTH WALES UNIVERSITY\b|\bUNSW\b',
 'Saab':r'\bSAAB\b',
 'Lockheed Martin':r'\bLOCKHEED\b|\bSIKORSKY AIRCRAFT\b',
 'MIT':r'\bMASSACHUSETTS INSTITUTE OF TECHNOLOGY\b|\bMIT LINCOLN\b',
 'Georgia Tech / Arkin':r'\bGEORGIA TECH\b|\bGEORGIA INSTITUTE OF TECHNOLOGY\b|\bRONALD\s+ARKIN\b',
 'Penn State':r'\bPENNSYLVANIA STATE UNIVERSITY\b|\bPENN STATE\b',
 'Virginia Tech':r'\bVIRGINIA POLYTECHNIC\b|\bVIRGINIA TECH\b',
 'SIFT':r'\bSMART INFORMATION FLOW\b|\bSIFT\b',
 'Duality AI':r'\bDUALITY\b',
 'Charles River Analytics':r'\bCHARLES RIVER ANALYTICS\b',
 'ASU':r'\bARIZONA STATE UNIVERSIT(?:Y|IES)\b|\bARIZONA STATE UNIV\b'}
RX={k:re.compile(v,re.I) for k,v in ALIASES.items()}
C={};F={};fstats=collections.Counter();inputcounts=collections.Counter();alias_names=collections.defaultdict(set);namecache={};hitcache={}
def norm(v):return '' if v is None else str(v)
def match(name):
 if name not in namecache:namecache[name]=[k for k,p in RX.items() if p.search(name or '')]
 return namecache[name]
def cents(v):return int(decimal.Decimal(norm(v) or '0')*100)
def usd(v):return format(decimal.Decimal(v)/100,'.2f')
def periods(date,fy):
 try:fy=int(fy)
 except (ValueError,TypeError):fy=0
 return {'CY2025_2026':bool(date and '2025-01-01'<=date<='2026-12-31'),'FY2025_2026':2025<=fy<=2026}
def eligible(date,fy):return any(periods(date,fy).values())
def obj(v):return json.loads(v) if isinstance(v,str) and v else v or {}
def ensure(key,role,award=None):
 return C.setdefault(key,{'register_key':key,'record_role':role,'award_key':award,'recipient_groups':set(),'matched_names':set(),'recipient_identifiers':set(),'period_evidence':set(),'sources':set(),'urls':set(),'locators':set(),'descriptions':{},'identifiers':{},'observed_action_dates':set(),'subaward_records':{},'sbir_records':{},'term_hits':collections.defaultdict(set),'match_note':'Name/alias matched retrieval candidate. Legal identity, corporate relationship and ASIMOV continuation are NOT verified.'})
def keep_description(c,r,p):
 title=norm(r.get('title'));text=norm(r.get('text'));goal=norm(r.get('funding_opportunity_goals_text'))
 dkey=(title,text,goal)
 if any(dkey):c['descriptions'].setdefault(dkey,{'title':title,'text':text,'funding_opportunity_goals_text':goal,'source_files':set()})['source_files'].add(p)
 c['sources'].add(p)
 for field,output in [('source_url','urls'),('raw_locator','locators')]:
  if r.get(field):c[output].add(r[field])
 if r.get('action_date'):c['observed_action_dates'].add(r['action_date'])
 ids=obj(r.get('identifiers_json'))
 if ids:c['identifiers'][json.dumps(ids,sort_keys=True)]=ids
 full='\n'.join(dkey)
 if full not in hitcache:hitcache[full]=hits(full)
 for g,ts in hitcache[full].items():c['term_hits'][g].update(ts)
def evidence(c,r,groups):
 c['recipient_groups'].update(groups);c['matched_names'].add(norm(r.get('entity_name')))
 if r.get('entity_key'):c['recipient_identifiers'].add(r['entity_key'])
 for p,yes in periods(r.get('action_date'),r.get('fiscal_year')).items():
  if yes:c['period_evidence'].add(p)
 for g in groups:alias_names[g].add(norm(r.get('entity_name')))

financial=next((ROOT/'input').rglob('financial_actions.jsonl.gz'))
for line in gzip.open(financial,'rt'):
 r=json.loads(line);inputcounts[financial.name]+=1;key=r['transaction_key'];entry=(r['award_key'],cents(r['action_obligation_usd']),int(r['fiscal_year']),r['action_date'],r['entity_name'],r.get('entity_key'))
 if key in F:
  fstats['duplicate_financial_keys']+=1
  if F[key]!=entry:raise ValueError('Conflicting financial transaction '+key)
  continue
 F[key]=entry;groups=match(r['entity_name'])
 if groups and eligible(r.get('action_date'),r.get('fiscal_year')):
  c=ensure(r['award_key'],'prime_or_assistance_financial_award',r['award_key']);evidence(c,r,groups)
print('Selected financial recipient awards',len(C),flush=True)
# Recover one-to-one normalized PIID mapping from all date-enriched source metadata.
piids=collections.defaultdict(set);date_records={}
for line in (ROOT/'evidence/award-date-fields.jsonl').open():
 r=json.loads(line);key=r['award_key']
 for piid in r['institutional_and_award_metadata'].get('award_id_piid',[]):piids[re.sub(r'[^A-Z0-9]','',piid.upper())].add(key)
 if key in C:date_records[key]=r

paths=sorted((ROOT/'input').rglob('*.jsonl.gz'))
for p in paths:
 if not p.name.startswith('usaspending') and p.name not in ['sbir.jsonl.gz','sbir_current.jsonl.gz']:continue
 sub='subawards' in p.name;sbir=p.name.startswith('sbir')
 for line in gzip.open(p,'rt'):
  r=json.loads(line);inputcounts[p.name]+=1;award=r.get('award_key');groups=match(r.get('entity_name'))
  if sub:
   if not groups or not eligible(r.get('action_date'),r.get('fiscal_year')):continue
   entity=r.get('entity_key') or norm(r.get('entity_name'));key='SUBRECIPIENT::'+norm(award)+'::'+entity
   c=ensure(key,'reported_first_tier_subrecipient',award);evidence(c,r,groups);keep_description(c,r,p.name)
   srkey=r.get('source_record_id') or r.get('document_id');skey=norm(srkey)+'|'+norm(r.get('source_snapshot_sha256'))+'|'+norm(r.get('record_sha256'));c['subaward_records'][skey]={'source_record_id':srkey,'source_file':p.name,'source_snapshot_sha256':r.get('source_snapshot_sha256'),'record_sha256':r.get('record_sha256'),'entity_name':r.get('entity_name'),'entity_key':r.get('entity_key'),'action_date':r.get('action_date'),'fiscal_year':r.get('fiscal_year'),'amounts':obj(r.get('money_json')),'identifiers':obj(r.get('identifiers_json')),'money_warning':'Reported first-tier subaward amount, not prime transaction obligation; not added to financial totals.'}
  elif sbir:
   if not groups or not eligible(r.get('action_date'),r.get('fiscal_year')):continue
   normalized=re.sub(r'[^A-Z0-9]','',norm(award).upper());matches=piids.get(normalized,set())
   # Join only unambiguous PIID whose selected financial record is also name-matched.
   canonical=next(iter(matches)) if len(matches)==1 else None
   if canonical not in C:canonical=None
   key=canonical or 'SBIR::'+norm(r.get('source_record_id') or r.get('document_id'))
   c=ensure(key,'prime_or_assistance_financial_award' if canonical else 'sbir_report_not_joined',canonical);evidence(c,r,groups);keep_description(c,r,p.name)
   srkey=r.get('source_record_id') or r.get('document_id');skey=norm(srkey)+'|'+norm(r.get('source_snapshot_sha256'))+'|'+norm(r.get('record_sha256'));c['sbir_records'][skey]={'source_record_id':srkey,'source_file':p.name,'source_snapshot_sha256':r.get('source_snapshot_sha256'),'record_sha256':r.get('record_sha256'),'raw_award_key':award,'action_date':r.get('action_date'),'fiscal_year':r.get('fiscal_year'),'amounts':obj(r.get('money_json')),'identifiers':obj(r.get('identifiers_json')),'join_method':'unique_normalized_piid_and_name_matched_financial_award' if canonical else 'not_joined_no_unique_name_matched_financial_award','money_warning':'SBIR reported amount is not additive to award financial obligations.'}
  elif award in C:
   c=C[award];keep_description(c,r,p.name)
 print('Descriptions scanned',p.name,inputcounts[p.name],flush=True)
# Preserve additional assistance narratives for selected financial awards.
extra=ROOT/'evidence/source-extra-narratives.jsonl.gz'
if extra.exists():
 for line in gzip.open(extra,'rt'):
  r=json.loads(line);inputcounts[extra.name]+=1
  if r['award_key'] in C:keep_description(C[r['award_key']],r,extra.name)
# Collect complete exact-key financial history only once per transaction, including negatives.
aggregate={};target_awards={c['award_key'] for c in C.values() if c['award_key']}
for tx,(award,amount,fy,date,name,uei) in F.items():
 if award not in target_awards:continue
 a=aggregate.setdefault(award,{'transaction_count':0,'negative_transaction_count':0,'fy2019_2026':0,'fy2024_2026':0,'fy2025_2026':0,'cy2025_2026':0,'first_action':date,'last_action':date,'period_action_dates':set(),'financial_entity_names':set(),'financial_entity_keys':set(),'period_transactions':[]})
 a['transaction_count']+=1;a['negative_transaction_count']+=amount<0;a['financial_entity_names'].add(name)
 if uei:a['financial_entity_keys'].add(uei)
 a['first_action']=min(a['first_action'],date);a['last_action']=max(a['last_action'],date)
 if 2019<=fy<=2026:a['fy2019_2026']+=amount
 if 2024<=fy<=2026:a['fy2024_2026']+=amount
 if 2025<=fy<=2026:a['fy2025_2026']+=amount
 if '2025-01-01'<=date<='2026-12-31':a['cy2025_2026']+=amount
 if eligible(date,fy):a['period_action_dates'].add(date);a['period_transactions'].append({'transaction_key':tx,'action_date':date,'fiscal_year':fy,'obligation_usd':usd(amount),'entity_name':name,'entity_key':uei})
# Date/identity metadata for all linked parent/prime awards, exact key; separate prime/subrecipient roles.
for line in (ROOT/'evidence/award-date-fields.jsonl').open():
 r=json.loads(line)
 if r['award_key'] in target_awards:date_records[r['award_key']]=r
output=[];roles=collections.Counter();group_counts=collections.Counter();relevant=collections.Counter()
for key,c in sorted(C.items()):
 award=c['award_key'];a=aggregate.get(award);d=date_records.get(award,{});meta=d.get('institutional_and_award_metadata',{});prime=c['record_role']=='prime_or_assistance_financial_award'
 psc=meta.get('product_or_service_code',[]);naics=meta.get('naics_code',[])
 code_flags=[]
 if any(x.startswith(('A','D','R4','R5','R6','R7')) for x in psc):code_flags.append('broad_research_it_professional_psc')
 if any(x.startswith(('5413','5415','5416','5417','334','3364')) for x in naics):code_flags.append('broad_research_it_engineering_aerospace_naics')
 if award and award.startswith('ASST_'):code_flags.append('assistance_no_psc_naics_exclusion')
 h={k:sorted(v) for k,v in c['term_hits'].items()};tags,reasons=classify(h)
 descriptions=[]
 for value in c['descriptions'].values():value['source_files']=sorted(value['source_files']);descriptions.append(value)
 descriptions.sort(key=lambda x:(x['title'],x['text'],x['funding_opportunity_goals_text']))
 row={'register_key':key,'record_role':c['record_role'],'award_key':award,'recipient_groups':sorted(c['recipient_groups']),'matched_entity_names':sorted(c['matched_names']),'matched_entity_identifiers':sorted(c['recipient_identifiers']),'recipient_match_status':c['match_note'],'continuation_status':'unverified_archive_name_matched_candidate_not_proof_of_ASIMOV_follow_on','period_selection':'union of CY2025-2026 action dates and FY2025-2026; FY2025 includes2024-10-01 onward','matching_period_bases':sorted(c['period_evidence']),'product_or_service_codes':psc,'naics_codes':naics,'relevant_code_flags_not_exclusions':code_flags,'preliminary_safeguard_categories':tags,'preliminary_safeguard_reasons':reasons,'safeguard_term_hits':h,'description_count':len(descriptions),'full_descriptions':descriptions,'source_files':sorted(c['sources']),'source_urls':sorted(c['urls']),'source_locators':sorted(c['locators']),'source_identifiers':list(c['identifiers'].values()),'observed_description_action_dates':sorted(c['observed_action_dates']),'financial_match':a is not None,'financial_attribution':'whole_prime_or_assistance_award_not_safeguard_allocated' if prime else 'no_recipient_obligation_attribution; linked_parent_totals_separate' if a else 'no_exact_financial_join; missing_not_zero','obligations_fy2019_2026_usd':usd(a['fy2019_2026']) if a and prime else None,'obligations_fy2024_2026_usd':usd(a['fy2024_2026']) if a and prime else None,'obligations_fy2025_2026_usd':usd(a['fy2025_2026']) if a and prime else None,'obligations_cy2025_2026_usd':usd(a['cy2025_2026']) if a and prime else None,'parent_award_obligations_fy2025_2026_usd':usd(a['fy2025_2026']) if a and not prime else None,'parent_award_obligations_cy2025_2026_usd':usd(a['cy2025_2026']) if a and not prime else None,'financial_transaction_count':a['transaction_count'] if a else None,'negative_financial_transaction_count':a['negative_transaction_count'] if a else None,'first_financial_action':a['first_action'] if a else None,'last_financial_action':a['last_action'] if a else None,'financial_entity_names':sorted(a['financial_entity_names']) if a else [],'financial_entity_keys':sorted(a['financial_entity_keys']) if a else [],'financial_period_action_dates':sorted(a['period_action_dates']) if a else [],'financial_period_transactions':sorted(a['period_transactions'],key=lambda x:(x['action_date'],x['transaction_key'])) if a else [],'archived_current_end_date':d.get('period_of_performance_current_end_date'),'archived_potential_end_date':d.get('period_of_performance_potential_end_date'),'date_selection_conflicts':d.get('date_or_money_selection_conflicts',{}),'sbir_reported_records':list(c['sbir_records'].values()),'reported_subaward_records':list(c['subaward_records'].values()),'verification_status':'LOCAL ARCHIVE ONLY; NOT LIVE VERIFIED'}
 output.append(row);roles[row['record_role']]+=1
 for g in row['recipient_groups']:group_counts[g]+=1
 relevant[bool(code_flags)]+=1
stem=ROOT/'evidence/asimov-performer-continuation-local-2025-2026'
with stem.with_suffix('.json').open('w') as f:json.dump(output,f,indent=2);f.write('\n')
with stem.with_suffix('.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(output[0]) if output else ['register_key']);w.writeheader()
 for r in output:w.writerow({k:json.dumps(v,sort_keys=True,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()})
audit={'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_rows':dict(inputcounts),'financial_unique_transaction_keys':len(F),'financial_duplicate_transaction_keys':fstats['duplicate_financial_keys'],'output_rows':len(output),'role_counts':dict(roles),'recipient_group_counts_overlapping':dict(group_counts),'matched_entity_names_by_group':{k:sorted(v) for k,v in alias_names.items()},'alias_regexes':ALIASES,'relevant_codes_flagged_no_exclusions':{str(k):v for k,v in relevant.items()},'missing_target_groups':[g for g in ALIASES if not group_counts[g]],'financial_window':'Financial archive action-date coverage2018-10-01 through2026-09-30; FY2019-2026. Output period filter unionCY2025-2026/FY2025-2026. Calendar2026 is incomplete and does not include October2026.','identity_cautions':['All name matching is preliminary; exact UEI/name legal identity must be checked live.','RTX retrieval aliases include legacy/corporate-family candidates Raytheon, BBN, United Technologies, Pratt & Whitney and Collins Aerospace; affiliation not independently verified.','Lockheed retrieval also includes Sikorsky as a corporate-family candidate, not verified current affiliation.','Duality and SIFT alias matches can have unrelated entities; matched names retained.','Do not sum primary and subrecipient rows: parent financial amounts are separate fields, not attributed to subrecipient.','No PSC/NAICS exclusion; relevance flags are broad retrieval hints, not safeguards classifications.','Historical award-level descriptions included even if underlying action predates selected period; exact period transactions are separately listed.','No evidence that recipient overlap establishes ASIMOV continuation.'], 'outputs':[{ 'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest()} for p in [stem.with_suffix('.csv'),stem.with_suffix('.json')]]}
(ROOT/'audit/asimov-performer-continuation-local-accounting.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps({k:v for k,v in audit.items() if k not in ['matched_entity_names_by_group','alias_regexes','input_rows']},indent=2))
