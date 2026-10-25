#!/usr/bin/env python3
"""Public USAspending/FPDS snapshot. No paid calls; raw bodies stay private.

Selection includes mandatory named awards and transparent inherited-register
keyword candidates; this is not an exhaustive universe or an ethics-dollar sum.
FPDS follows every next link until absent. Award keys include agency/parent.
"""
import concurrent.futures,csv,datetime,decimal,hashlib,json,os,pathlib,re,sys,threading,urllib.error,urllib.parse,urllib.request,xml.etree.ElementTree as ET
P=pathlib.Path(__file__).resolve().parents[1]
CACHE=pathlib.Path('/workspace/scratch/f4-live');CACHE.mkdir(parents=True,exist_ok=True)
LOG=[];LOCK=threading.Lock();NS={'a':'http://www.w3.org/2005/Atom','f':'https://www.fpds.gov/FPDS'}
def fetch(url,method='GET',body=None):
 ts=datetime.datetime.now(datetime.timezone.utc).isoformat();row={'url':url,'method':method,'retrieved_utc':ts}
 if body is not None:row['request_body']=body
 def persist(event):
  with LOCK:
   with (CACHE/'request-events.jsonl').open('a') as out:
    out.write(json.dumps(event,ensure_ascii=False)+'\n');out.flush();os.fsync(out.fileno())
 persist({**row,'request_state':'attempt_started'})
 try:
  req=urllib.request.Request(url,data=json.dumps(body).encode() if body is not None else None,headers={'User-Agent':'public-source-safeguards-research/1.0','Content-Type':'application/json'},method=method)
  with urllib.request.urlopen(req,timeout=45) as r:
   raw=r.read();row.update(http_status=r.status,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),final_url=r.url)
  (CACHE/(row['sha256']+'.raw')).write_bytes(raw)
 except Exception as e:
  row.update(error=type(e).__name__+': '+str(e),http_status=getattr(e,'code',None));raw=None
  if isinstance(e,urllib.error.HTTPError):
   eraw=e.read();row['error_body_sha256']=hashlib.sha256(eraw).hexdigest();row['error_body']=eraw.decode('utf-8',errors='replace')[:4000];(CACHE/(row['error_body_sha256']+'.raw')).write_bytes(eraw)
 with LOCK:LOG.append(row)
 persist({**row,'request_state':'attempt_finished'})
 return raw,row
def fpds(piid,award_key=None):
 query='PIID:"'+piid+'"'
 # Short delivery-order PIIDs collide across parent vehicles. Scope the feed
 # to the known parent as well as filtering returned award keys below.
 if award_key and award_key.startswith('CONT_AWD_'):
  parts=award_key.split('_')
  if len(parts)>=6 and parts[4]!='-NONE-':query+=' REF_IDV_PIID:"'+parts[4]+'"'
 url='https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&VERSION=1.5.3&q='+urllib.parse.quote(query)+'&s=FPDSNG.COM&indexName=awardfull&start=0'
 seen=set();actions={};pages=[];complete=False
 while url:
  if url in seen:pages.append({'url':url,'error':'pagination_cycle'});break
  seen.add(url);raw,meta=fetch(url);pages.append(meta)
  if raw is None:break
  try:root=ET.fromstring(raw)
  except ET.ParseError as e:meta['parse_error']=str(e);break
  for entry in root.findall('a:entry',NS):
   award=entry.find('a:content/f:award',NS)
   if award is None:continue
   def get(path):return award.findtext('f:'+path.replace('/','/f:'),'',NS)
   def attr(path):
    x=award.find('f:'+path.replace('/','/f:'),NS);return x.get('description','') if x is not None else ''
   row={k:get(v) for k,v in {'piid':'awardID/awardContractID/PIID','agency_id':'awardID/awardContractID/agencyID','parent_piid':'awardID/referencedIDVID/PIID','parent_agency_id':'awardID/referencedIDVID/agencyID','modification':'awardID/awardContractID/modNumber','transaction':'awardID/awardContractID/transactionNumber','signed_date':'relevantContractDates/signedDate','effective_date':'relevantContractDates/effectiveDate','current_completion':'relevantContractDates/currentCompletionDate','ultimate_completion':'relevantContractDates/ultimateCompletionDate','obligation_usd':'dollarValues/obligatedAmount','base_exercised_change_usd':'dollarValues/baseAndExercisedOptionsValue','all_options_change_usd':'dollarValues/baseAndAllOptionsValue','reason_code':'contractData/reasonForModification','description':'contractData/descriptionOfContractRequirement','recipient':'vendor/vendorHeader/vendorName','solicitation':'contractData/solicitationID','total_obligation_usd':'totalDollarValues/totalObligatedAmount','total_base_exercised_usd':'totalDollarValues/totalBaseAndExercisedOptionsValue','total_all_options_usd':'totalDollarValues/totalBaseAndAllOptionsValue'}.items()}
   row.update(reason=attr('contractData/reasonForModification'),record_last_modified=entry.findtext('a:modified','',NS),source_url=url,response_sha256=meta['sha256'],retrieved_utc=meta['retrieved_utc'])
   row['award_key']='CONT_AWD_'+row['piid']+'_'+row['agency_id']+'_'+(row['parent_piid'] or '-NONE-')+'_'+(row['parent_agency_id'] or '-NONE-')
   key=tuple(row[k] for k in ['agency_id','piid','parent_piid','parent_agency_id','modification','transaction'])
   if key in actions and actions[key]['obligation_usd']!=row['obligation_usd']:meta['duplicate_conflict']=True
   actions[key]=row
  nxt=next((x.get('href') for x in root.findall('a:link',NS) if x.get('rel')=='next'),None)
  if not nxt:complete=True
  url=urllib.parse.urljoin(url,nxt) if nxt else None
 return list(actions.values()),pages,complete
def search_id(piid):
 ids=[]
 for group in [['A','B','C','D'],['02','03','04','05','F001','F002'],['IDV_A','IDV_B','IDV_B_A','IDV_B_B','IDV_B_C','IDV_C','IDV_D','IDV_E']]:
  page=1;seen=set()
  while True:
   body={'filters':{'keywords':[piid],'award_type_codes':group},'fields':['Award ID','generated_internal_id','Recipient Name','Description'],'page':page,'limit':100,'sort':'Award ID','order':'asc','subawards':False}
   raw,meta=fetch('https://api.usaspending.gov/api/v2/search/spending_by_award/','POST',body)
   if raw is None:break
   try:
    obj=json.loads(raw);rows=obj.get('results',[]);signature=tuple(x.get('generated_internal_id') for x in rows)
    if signature in seen and rows:meta['pagination_error']='repeated_page';break
    seen.add(signature);ids.extend(x['generated_internal_id'] for x in rows if x.get('Award ID','').upper()==piid.upper() and x.get('generated_internal_id'))
    if not obj.get('page_metadata',{}).get('hasNext'):break
    page+=1
   except Exception:break
 return sorted(set(ids))
def assistance_transactions(record):
 """Reconcile public assistance action obligations, following every page.

 Never substitute FPDS's contract-only denominator for grants. Null money is
 counted and prevents a claim of full reconciliation; exact IDs deduplicate
 repeated transaction observations while conflicting duplicates are surfaced.
 """
 url='https://api.usaspending.gov/api/v2/transactions/';page=1;rows={};pages=[];seen=set();complete=False;duplicates=0;conflicts=[]
 while True:
  body={'award_id':record['award_key'],'page':page,'limit':100}
  raw,meta=fetch(url,'POST',body);pages.append(meta)
  if raw is None:break
  try:obj=json.loads(raw)
  except Exception as e:meta['parse_error']=str(e);break
  results=obj.get('results',[]);signature=tuple(x.get('id') for x in results)
  if results and signature in seen:meta['pagination_error']='repeated_page';break
  seen.add(signature)
  for index,transaction in enumerate(results):
   key=transaction.get('id')
   if not key:key='missing-id-page-'+str(page)+'-row-'+str(index)
   if key in rows:
    duplicates+=1
    if rows[key].get('federal_action_obligation')!=transaction.get('federal_action_obligation'):conflicts.append(key)
   rows[key]={**transaction,'source_url':url,'request_page':page,'response_sha256':meta['sha256'],'retrieved_utc':meta['retrieved_utc']}
  if not obj.get('page_metadata',{}).get('hasNext'):complete=True;break
  page+=1
 nulls=sum(x.get('federal_action_obligation') is None for x in rows.values());missing_ids=sum(str(k).startswith('missing-id-page-') for k in rows)
 total=sum((decimal.Decimal(str(x['federal_action_obligation'])) for x in rows.values() if x.get('federal_action_obligation') is not None),decimal.Decimal(0))
 result={'endpoint':url,'pages':len(pages),'pagination_complete':complete,'unique_transaction_count':len(rows),'duplicate_transaction_observations':duplicates,'conflicting_duplicate_ids':conflicts,'null_obligation_rows':nulls,'missing_transaction_id_rows':missing_ids,'transaction_obligation_sum_usd':str(total),'minus_award_total_obligation_usd':str(total-decimal.Decimal(record['total_obligation_usd'])),'reconciled':complete and bool(rows) and not nulls and not missing_ids and not conflicts and total==decimal.Decimal(record['total_obligation_usd']),'transactions':list(rows.values()),'accounting_note':'Net action obligations by exact assistance transaction ID, not award ceilings. USAspending award and transaction endpoints are two presentations of reported agency data, not independent evidence of performance.'}
 for label,start,end in [('fy2019_2026','2018-10-01','2026-10-01'),('fy2024_2026','2023-10-01','2026-10-01'),('cy2019_2026_to_cutoff','2019-01-01','2026-10-26'),('cy2024_2026_to_cutoff','2024-01-01','2026-10-26')]:
  result[label+'_obligations_usd']=str(sum((decimal.Decimal(str(x['federal_action_obligation'])) for x in rows.values() if x.get('federal_action_obligation') is not None and start<=str(x.get('action_date',''))[:10]<end),decimal.Decimal(0)))
 record['usaspending_transaction_reconciliation']=result
 record['fpds_note']='Assistance award: FPDS contract history is not an applicable denominator. Award total is separately checked against the complete paginated public USAspending assistance transaction history; see usaspending_transaction_reconciliation.'
 return result
def one(candidate):
 piid=candidate['piid'];acts,pages,complete=fpds(piid,candidate.get('award_key'));keys=sorted(set(x['award_key'] for x in acts))
 if candidate.get('award_key'):
  keys=[candidate['award_key']]
  acts=[x for x in acts if x['award_key']==candidate['award_key']]
 if candidate.get('award_key'):keys=sorted(set(keys+[candidate['award_key']]))
 if not keys:keys=['CONT_AWD_'+piid+'_9700_-NONE-_-NONE-']
 records=[]
 for key in keys:
  url='https://api.usaspending.gov/api/v2/awards/'+key+'/'
  raw,meta=fetch(url)
  if raw is None:continue
  try:obj=json.loads(raw)
  except Exception:continue
  if not obj.get('generated_unique_award_id'):continue
  related=[r for r in acts if r['award_key']==obj['generated_unique_award_id']]
  fpds_applicable=obj.get('category')=='contract'
  fpds_sum=sum((decimal.Decimal(r['obligation_usd'] or '0') for r in related),decimal.Decimal(0))
  objsum=decimal.Decimal(str(obj.get('total_obligation',0)))
  record={'piid':piid,'award_key':obj['generated_unique_award_id'],'selection_basis':candidate['selection_basis'],'recipient':obj.get('recipient',{}).get('recipient_name'),'description':obj.get('description'),'date_signed':obj.get('date_signed'),'total_obligation_usd':str(objsum),'base_exercised_options_usd':str(obj.get('base_exercised_options')),'base_and_all_options_usd':str(obj.get('base_and_all_options')),'period_of_performance':obj.get('period_of_performance'),'psc':obj.get('latest_transaction_contract_data',{}).get('product_or_service_code'),'naics':obj.get('latest_transaction_contract_data',{}).get('naics'),'source_url':url,'response_sha256':meta['sha256'],'retrieved_utc':meta['retrieved_utc'],'fpds_applicable':fpds_applicable,'fpds_action_count':len(related),'fpds_complete':complete if fpds_applicable else None,'fpds_pages':len(pages),'fpds_obligation_sum_usd':str(fpds_sum) if fpds_applicable else None,'fpds_minus_usaspending_usd':str(fpds_sum-objsum) if fpds_applicable else None,'subaward_count_reported':obj.get('subaward_count'),'subawards_retrieved':[]}
  record['api_award_category']=obj.get('category')
  record['award_category']='assistance' if record['award_key'].startswith('ASST_') else obj.get('category')
  if fpds_applicable:record['fpds_note']='Contract action history; feed next links exhausted. Public FPDS data may be delayed, including the DoD 90-day public-release restriction; absence of recent actions does not establish no funding.'
  elif obj.get('category')=='idv':record['fpds_note']='IDV parent, not an individual task-order contract. This parser does not reconcile IDV modifications; parent zero obligations do not establish no task-order funding or no ethical architecture funding.'
  else:record['fpds_note']='Assistance award: FPDS contract history is not an applicable denominator. USAspending award-lifetime total retrieved, not reconciled to assistance transaction history.'
  for label,start,end in [('fy2019_2026','2018-10-01','2026-10-01'),('fy2024_2026','2023-10-01','2026-10-01'),('cy2019_2026_to_cutoff','2019-01-01','2026-10-26'),('cy2024_2026_to_cutoff','2024-01-01','2026-10-26')]:
   record[label+'_fpds_obligations_usd']=str(sum((decimal.Decimal(x['obligation_usd'] or '0') for x in related if start<=x['signed_date'][:10]<end),decimal.Decimal(0))) if fpds_applicable else None
  # The endpoint is award-scoped and explicitly paginated when subawards exist.
  if obj.get('subaward_count',0):
   page=1
   while True:
    surl='https://api.usaspending.gov/api/v2/subawards/'
    sraw,smeta=fetch(surl,'POST',{'award_id':obj['id'],'page':page,'limit':100})
    if sraw is None:record['subaward_status']='retrieval_failed';break
    try:sobj=json.loads(sraw)
    except Exception:record['subaward_status']='parse_failed';break
    record['subawards_retrieved']+=sobj.get('results',[])
    if not sobj.get('page_metadata',{}).get('hasNext'):record['subaward_status']='complete';break
    page+=1
  records.append(record)
 if not records:
  ids=search_id(piid)
  # Search retrieval is recorded even if no result is returned; never assert no award.
  if ids and set(ids)-set(keys):
   for key in sorted(set(ids)-set(keys)):
    result,newacts=one({**candidate,'award_key':key});records+=result['records']
    known={(x['award_key'],x['modification'],x['transaction']) for x in acts}
    acts += [x for x in newacts if (x['award_key'],x['modification'],x['transaction']) not in known]
 for record in records:
  subrows=record.get('subawards_retrieved',[]);subids=[x.get('subaward_number') for x in subrows]
  record['subaward_report_rows_retrieved']=len(subrows)
  record['subaward_distinct_numbers']=len(set(subids))
  record['subaward_distinct_recipients']=len(set(x.get('recipient_name') for x in subrows))
  record['subaward_repeated_number_rows']=len(subids)-len(set(subids))
  record['subaward_count_matches_report_rows']=record.get('subaward_count_reported')==len(subrows)
  record['subaward_accounting_note']='Counts are reported rows, not necessarily distinct subcontracts, recipients or funding increments. Repeated numbers may be revisions; no subaward dollars are added to prime obligations.'
 applicable=any(x.get('fpds_applicable') for x in records)
 return {'piid':piid,'selection_basis':candidate['selection_basis'],'status':'retrieved' if any(x.get('award_key') for x in records) else 'award_detail_unresolved','fpds_complete':complete if applicable and acts else None,'fpds_feed_pagination_complete':complete,'fpds_verification_status':'contract_actions_retrieved' if applicable and acts else ('not_applicable_to_assistance_or_IDV_parser' if records else 'no_entries_award_unresolved_not_evidence_of_absence'),'fpds_pages':len(pages),'fpds_action_count':len(acts),'records':records},acts
def select():
 named=['FA865125CB001','FA865125CB002','FA865125CB003','FA865125CB004','FA865125CB006','FA865125CB007','FA865125CB018','FA248722FA002','W5170125C0052','FA864922P1015','N6833521C0510','N6833521C0549','FA945326CX013','W5170124C0174','FA864926P0169','FA864926P0093']
 candidates={x:{'piid':x,'selection_basis':'directive_named_or_independent_editor_counterexample'} for x in named}
 candidates['FA248722FA002']['award_key']='CONT_AWD_FA248722FA002_9700_FA248718D4700_9700'
 prior=P.parents[1]/'2026-10-24/f2-tactical-ai/audit'
 pattern=re.compile(r'ETHIC|MORAL|RULES OF ENGAGEMENT|LAWS OF WAR|LOAC|CIVILIAN HARM|ASSUR|TRUST|SAFETY|SAFE AUTONOM|RUNTIME|RUN.TIME|FORMAL|VERIF|EXPLAINAB|CALIBRAT|UNCERTAINT|HUMAN.IN.THE.LOOP|HUMAN CONTROL|ROBUST|TEST AND EVAL|RED TEAM|GUARDRAIL',re.I)
 additions=[]
 for fname,delim in [('lane1-tactical-candidates-384.csv',','),('lane2-candidate_register.tsv','\t'),('lane2-high-scoring-nonexact-followons-92.csv',',')]:
  for row in csv.DictReader((prior/fname).open(),delimiter=delim):
   text=' '.join(str(row.get(k,'')) for k in ['title','evidence_descriptions_json','description_text','all_descriptions'])
   hits=sorted(set(x.group().upper() for x in pattern.finditer(text)))
   piid=row.get('award_id',row.get('piid',''))
   if hits and piid:additions.append((len(hits),piid,row.get('award_key',''),hits))
 for score,piid,key,hits in sorted(additions,reverse=True):
  if piid not in candidates:candidates[piid]={'piid':piid,'award_key':key,'selection_basis':'inherited_F2_keyword_candidate:'+','.join(hits)}
  if len(candidates)>=90:break
 return list(candidates.values())
def main():
 cs=select();records=[];actions=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
  for record,acts in pool.map(one,cs):records.append(record);actions+=acts;print(record['piid'],record['status'],record['fpds_action_count'],flush=True)
 (P/'evidence/live-award-register.json').write_text(json.dumps({'retrieval_started_utc':min((x['retrieved_utc'] for x in LOG),default=None),'candidate_count':len(cs),'selection_note':'Named candidates plus inherited F2 assurance keywords; screening relevance requires substantive review, not all are brakes. No category-dollar total inferred.','amount_note':'Award API total_obligation is award-lifetime net obligations, not the ceiling/current value. Fiscal window sums use FPDS signed action dates. Subaward reports are not added to prime dollars or summed as incremental funding: repeated subaward numbers can be revisions.','awards':records},indent=2)+'\n')
 (P/'audit/live-retrieval-log.json').write_text(json.dumps({'requests':LOG,'request_count':len(LOG),'failed_request_count':sum(bool(x.get('error')) for x in LOG),'raw_cache_public':False,'source_bodies':'Private local cache only; hashes/URLs published.'},indent=2)+'\n')
 if actions:
  with (P/'evidence/fpds-verified-actions.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(actions[0]));w.writeheader();w.writerows(actions)
def performer_trace(names_override=None):
 """Targeted lead trace, NOT all federal awards to these legal entities.

 Recipient text matching and description keywords have false positives and
 negatives. Transaction-date filter finds awards with matching period activity,
 not necessarily new awards, new 2026 dollars or program continuation.
 """
 names=['KITWARE','RTX','RAYTHEON','SYSTEMS & TECHNOLOGY RESEARCH','COVAR','UNIVERSITY OF NEW SOUTH WALES','SAAB','LOCKHEED MARTIN','MASSACHUSETTS INSTITUTE OF TECHNOLOGY','GEORGIA INSTITUTE OF TECHNOLOGY','PENNSYLVANIA STATE UNIVERSITY','VIRGINIA POLYTECHNIC','SMART INFORMATION FLOW','DUALITY','CHARLES RIVER ANALYTICS','ARIZONA STATE UNIVERSITY','UNIVERSITY OF PENNSYLVANIA','UNIVERSITY OF VIRGINIA','GEORGIA TECH','SYSTEMS AND TECHNOLOGY RESEARCH','MIT LINCOLN LABORATORY']
 if names_override is not None:names=names_override
 keywords=['ASIMOV','AUTONOMOUS','AUTONOMY','ARTIFICIAL INTELLIGENCE','ETHICAL','ASSURANCE','RULES OF ENGAGEMENT','LOAC']
 traces=[]
 for name,group in [(n,g) for n in names for g in [['A','B','C','D'],['02','03','04','05','F001','F002']]]:
  results={};pages=[];page=1;seen=set();complete=False
  while True:
   body={'filters':{'recipient_search_text':[name],'award_type_codes':group,'time_period':[{'start_date':'2025-01-01','end_date':'2026-10-25'}],'keywords':keywords},'fields':['Award ID','generated_internal_id','Recipient Name','Description','Award Amount','Start Date','End Date','Last Modified Date'],'page':page,'limit':100,'sort':'Award ID','order':'asc','subawards':False}
   raw,meta=fetch('https://api.usaspending.gov/api/v2/search/spending_by_award/','POST',body);pages.append(meta)
   if raw is None:break
   try:obj=json.loads(raw)
   except Exception as e:meta['parse_error']=str(e);break
   rows=obj.get('results',[]);signature=tuple(x.get('generated_internal_id') for x in rows)
   if signature in seen and rows:meta['pagination_error']='repeated_page';break
   seen.add(signature)
   for x in rows:
    key=x.get('generated_internal_id')
    if key:
     x['search_response_sha256']=meta['sha256'];x['search_page']=page;x['retrieved_utc']=meta['retrieved_utc'];x['continuation_finding']='unreviewed_candidate_not_proof_of_ASIMOV_continuation';results[key]=x
   if not obj.get('page_metadata',{}).get('hasNext'):complete=True;break
   page+=1
  traces.append({'recipient_search_text':name,'keywords_OR':keywords,'period_filter':'2025-01-01 through 2026-10-25 matching transaction activity','award_type_codes':group,'agency_filter':'none; all federal','pages':len(pages),'pagination_complete':complete,'unique_award_count':len(results),'results':list(results.values())})
  print('performer_trace',name,len(results),'complete',complete,flush=True)
 return {'scope_note':'Targeted recipient-text plus keyword OR search of contract and assistance awards with matching 2025–2026 transaction activity, all federal agencies. Not every award to every legal entity, and not every description is indexed. Does not cover all subcontract/OTA consortium activities. Results include name/medical/engineering false positives. A matching award is a lead, not an ASIMOV continuation. No universal negative follows. Award Amount is lifetime net obligations, not 2025–2026 action obligations.','traces':traces}
def supplement():
 a=json.loads((P/'evidence/live-award-register.json').read_text());oldlog=json.loads((P/'audit/live-retrieval-log.json').read_text());actions=list(csv.DictReader((P/'evidence/fpds-verified-actions.csv').open()))
 extras=['FA870225DB003','FA87502321015','HR00112490431','FA865124CB024','N6833525C0110','N0002425CS104','HR001125F0028','HR00112590089','FA864925P0010','FA9550261B207','FA86552417047']
 for piid in extras:
  existing=next((x for x in a['awards'] if x['piid']==piid),None)
  if existing and existing['status']=='retrieved':continue
  if existing:a['awards'].remove(existing)
  candidate={'piid':piid,'selection_basis':'independent_editor_additional_FFRDC_ANSR_TIAMAT_TALON_CODORD_or_Latent'}
  if piid=='HR001125F0028':candidate['award_key']='CONT_AWD_HR001125F0028_9700_HR001122D0001_9700'
  if piid in ['FA9550261B207','FA86552417047']:candidate['award_key']='ASST_NON_'+piid+'_097'
  r,acts=one(candidate);a['awards'].append(r);actions+=acts;print('supplement',piid,r['status'],r['fpds_action_count'],flush=True)
 a['candidate_count']=len(a['awards']);a['performer_trace']=performer_trace()
 for award in a['awards']:
  for record in award['records']:
   if record.get('award_category')=='assistance' or record['award_key'].startswith('ASST_'):assistance_transactions(record)
 (P/'evidence/live-award-register.json').write_text(json.dumps(a,indent=2)+'\n')
 if oldlog.get('supplemental_requests'):oldlog.setdefault('earlier_supplement_passes',[]).append({'requests':oldlog['supplemental_requests'],'note':'Earlier supplement pass retained, including rejected mixed award-type group performer searches. Fixed by querying contract and assistance groups separately.'})
 oldlog['supplemental_requests']=LOG;oldlog['supplemental_request_count']=len(LOG);oldlog['supplemental_failed_request_count']=sum(bool(x.get('error')) for x in LOG);oldlog['all_passes_request_count']=oldlog.get('all_passes_request_count',oldlog['request_count'])+len(LOG)
 (P/'audit/live-retrieval-log.json').write_text(json.dumps(oldlog,indent=2)+'\n')
 with (P/'evidence/fpds-verified-actions.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(actions[0]));w.writeheader();w.writerows(actions)
def reconcile_assistance():
 a=json.loads((P/'evidence/live-award-register.json').read_text());logpath=P/'audit/live-retrieval-log.json';l=json.loads(logpath.read_text())
 for piid in ['FA9550261B207','FA86552417047']:
  if any(x['piid']==piid for x in a['awards']):continue
  award,actions=one({'piid':piid,'award_key':'ASST_NON_'+piid+'_097','selection_basis':'independent_editor_fresh_HAMLET_or_CASPER_ethical_reasoning'});a['awards'].append(award)
  if actions:raise RuntimeError('Unexpected FPDS contract actions for assistance candidate')
 for award in a['awards']:
  for record in award['records']:
   if record.get('award_category')=='assistance' or record['award_key'].startswith('ASST_'):
    result=assistance_transactions(record);print('assistance',record['piid'],result['unique_transaction_count'],result['transaction_obligation_sum_usd'],result['minus_award_total_obligation_usd'],result['reconciled'],flush=True)
 a['candidate_count']=len(a['awards']);(P/'evidence/live-award-register.json').write_text(json.dumps(a,indent=2)+'\n')
 l.setdefault('assistance_reconciliation_passes',[]).append({'requests':LOG,'request_count':len(LOG),'failed_request_count':sum(bool(x.get('error')) for x in LOG)})
 l['all_logged_request_count']+=len(LOG);l['all_passes_request_count']+=len(LOG);l['all_logged_failed_request_count']+=sum(bool(x.get('error')) for x in LOG);logpath.write_text(json.dumps(l,indent=2)+'\n')
def late_additions():
 a=json.loads((P/'evidence/live-award-register.json').read_text());logpath=P/'audit/live-retrieval-log.json';l=json.loads(logpath.read_text());actions=list(csv.DictReader((P/'evidence/fpds-verified-actions.csv').open()))
 targets=[('W31P4Q26F0015','CONT_AWD_W31P4Q26F0015_9700_W31P4Q22D0025_9700')]+[(piid,'ASST_NON_'+piid+'_097') for piid in ['W911NF261A113','W911NF2510079','FA95502310036','FA95502010342','FA95502010130','N629092212005']]
 for piid,key in targets:
  if any(x['piid']==piid for x in a['awards']):continue
  award,acts=one({'piid':piid,'award_key':key,'selection_basis':'late_independent_editor_CAMP_or_normative_research_lead_not_automatic_weapons_safeguard'})
  for record in award['records']:
   if key.startswith('ASST_'):assistance_transactions(record)
  a['awards'].append(award);actions+=acts;print('late_addition',piid,award['status'],len(acts),[(r.get('total_obligation_usd'),r.get('fpds_minus_usaspending_usd'),r.get('usaspending_transaction_reconciliation',{}).get('reconciled')) for r in award['records']],flush=True)
 a['candidate_count']=len(a['awards']);(P/'evidence/live-award-register.json').write_text(json.dumps(a,indent=2)+'\n')
 with (P/'evidence/fpds-verified-actions.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(actions[0]));w.writeheader();w.writerows(actions)
 l.setdefault('late_editor_addition_passes',[]).append({'requests':LOG,'request_count':len(LOG),'failed_request_count':sum(bool(x.get('error')) for x in LOG)});l['all_logged_request_count']+=len(LOG);l['all_passes_request_count']+=len(LOG);l['all_logged_failed_request_count']+=sum(bool(x.get('error')) for x in LOG);logpath.write_text(json.dumps(l,indent=2)+'\n')
if __name__=='__main__':
 if '--late-additions' in sys.argv:late_additions()
 elif '--assistance-transactions' in sys.argv:reconcile_assistance()
 elif '--supplement' in sys.argv:supplement()
 else:main()
