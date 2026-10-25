#!/usr/bin/env python3
"""Read public FPDS OtherTransactionIDV schemas, not only FAR f:award.

No paid API, credentials, access bypass or outbound contact. All visible actions
are retained; feed aggregate differences remain unresolved rather than patched.
"""
import csv,datetime as dt,hashlib,json,pathlib,urllib.parse,urllib.request,xml.etree.ElementTree as ET
from decimal import Decimal
P=pathlib.Path(__file__).resolve().parents[1]
CACHE=pathlib.Path('/workspace/scratch/f4-ota');CACHE.mkdir(parents=True,exist_ok=True)
A='{http://www.w3.org/2005/Atom}';F='{https://www.fpds.gov/FPDS}'
TARGETS={'HR00112490431':'TIAMAT / University of Texas at Austin','HR00112590088':'CODORD / RTX BBN DONATELLO','HR00112590097':'CODORD / Barnstorm KRADL','HR00112590089':'CODORD / USC DROIDDS'}
LOG=[]
def fetch(url):
 row={'url':url,'method':'GET','retrieved_utc':dt.datetime.now(dt.timezone.utc).isoformat()}
 with (CACHE/'request-events.jsonl').open('a') as f:f.write(json.dumps({**row,'state':'started'})+'\n')
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'public-source-safeguards-audit/1.0'}),timeout=40) as response:
   raw=response.read();row.update(status=response.status,final_url=response.url,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
  (CACHE/(row['sha256']+'.raw')).write_bytes(raw)
 except Exception as e:row.update(status='failed',error=repr(e));raw=None
 LOG.append(row)
 with (CACHE/'request-events.jsonl').open('a') as f:f.write(json.dumps({**row,'state':'finished'})+'\n')
 return raw,row
def fpds(piid):
 url='https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&VERSION=1.5.3&q='+urllib.parse.quote('PIID:"'+piid+'"')+'&s=FPDSNG.COM&indexName=awardfull&start=0'
 pages=[];seen=set();actions={};unknown=[];conflicts=[];complete=False
 while url:
  if url in seen:unknown.append({'error':'pagination_cycle','url':url});break
  seen.add(url);raw,receipt=fetch(url);pages.append(receipt)
  if raw is None:break
  try:root=ET.fromstring(raw)
  except ET.ParseError as e:unknown.append({'parse_error':str(e),'url':url});break
  for entry in root.findall(A+'entry'):
   content=entry.find(A+'content');payload=list(content)[0] if content is not None and len(content) else None
   if payload is None:unknown.append({'entry':'missing content'});continue
   schema=payload.tag.split('}')[-1]
   if schema!='OtherTransactionIDV':unknown.append({'schema':schema,'title':entry.findtext(A+'title')});continue
   ident=payload.find(F+'OtherTransactionIDVID/'+F+'OtherTransactionIDVContractID');detail=payload.find(F+'contractDetail')
   if ident is None or detail is None:unknown.append({'schema':schema,'error':'missing identity/detail'});continue
   def get(node,path):return node.findtext('/'.join(F+x for x in path.split('/')),'')
   def attr(path):
    node=detail.find('/'.join(F+x for x in path.split('/')));return node.get('description','') if node is not None else ''
   row={k:get(ident,v) for k,v in {'piid':'PIID','agency_id':'agencyID','modification':'modNumber','transaction_number':'transactionNumber'}.items()}
   if row['piid']!=piid:unknown.append({'error':'piid mismatch','observed':row['piid']});continue
   row.update({k:get(detail,v) for k,v in {'signed_date':'relevantContractDates/signedDate','effective_date':'relevantContractDates/effectiveDate','current_end':'relevantContractDates/currentCompletionDate','potential_end':'relevantContractDates/ultimateCompletionDate','action_obligation_usd':'dollarValues/obligatedAmount','action_exercised_value_usd':'dollarValues/baseAndExercisedOptionsValue','action_all_options_value_usd':'dollarValues/baseAndAllOptionsValue','aggregate_obligations_usd':'totalDollarValues/totalObligatedAmount','aggregate_exercised_value_usd':'totalDollarValues/totalBaseAndExercisedOptionsValue','aggregate_all_options_value_usd':'totalDollarValues/totalBaseAndAllOptionsValue','recipient':'vendor/vendorHeader/vendorName','description':'contractData/descriptionOfContractRequirement','agreement_type':'contractData/typeOfAgreement','modification_reason_code':'contractData/reasonForModification','solicitation':'contractData/solicitationID'}.items()})
   row.update(schema=schema,modification_reason=attr('contractData/reasonForModification'),feed_record_modified=entry.findtext(A+'modified',''),source_url=url,response_sha256=receipt['sha256'],retrieved_utc=receipt['retrieved_utc'],primary_identity='FPDS_OTHER_TRANSACTION_IDV:'+row['agency_id']+':'+piid)
   key=(row['agency_id'],row['piid'],row['modification'],row['transaction_number'])
   if key in actions and any(actions[key].get(k)!=row.get(k) for k in ['action_obligation_usd','signed_date','description']):conflicts.append({'key':key,'note':'conflicting visible duplicate'})
   actions[key]=row
  links=[x.get('href') for x in root.findall(A+'link') if x.get('rel')=='next']
  if not links:complete=True;url=None
  else:url=urllib.parse.urljoin(url,links[0])
 rows=sorted(actions.values(),key=lambda r:(r['signed_date'],r['modification'],r['transaction_number']))
 total=sum((Decimal(r['action_obligation_usd']) for r in rows),Decimal(0))
 latest=max(rows,key=lambda r:(r['signed_date'],r['feed_record_modified'])) if rows else {}
 aggregate=Decimal(latest['aggregate_obligations_usd']) if latest.get('aggregate_obligations_usd') else None
 return {'piid':piid,'program_lead':TARGETS[piid],'source':'public FPDS Atom OtherTransactionIDV','schema':'https://www.fpds.gov/FPDS OtherTransactionIDV / contractDetail','pages':pages,'pagination_complete':complete,'visible_action_count':len(rows),'action_obligation_sum_usd':str(total),'feed_aggregate_obligations_usd':str(aggregate) if aggregate is not None else None,'aggregate_minus_visible_actions_usd':str(aggregate-total) if aggregate is not None else None,'visible_actions_reconcile_feed_aggregate':bool(rows and aggregate==total and not conflicts and complete),'latest_signed_date':latest.get('signed_date'),'last_positive_obligation_date':max((r['signed_date'] for r in rows if Decimal(r['action_obligation_usd'])>0),default=None),'latest_visible_current_end':latest.get('current_end'),'latest_visible_potential_end':latest.get('potential_end'),'latest_visible_aggregate_exercised_value_usd':latest.get('aggregate_exercised_value_usd'),'latest_visible_aggregate_all_options_value_usd':latest.get('aggregate_all_options_value_usd'),'record_period_overlaps_cutoff':bool(latest.get('current_end','')[:10]>='2026-10-25'),'duplicate_conflicts':conflicts,'unparsed_entry_notes':unknown,'actions':rows,'limit':'Visible action sums and feed aggregates are different evidence fields. A mismatch is not silently reconciled. DoD release delays and omitted/corrected records are possibilities, not demonstrated explanations. No USAspending cross-system match or operational LOAC validation is inferred.'}
if __name__=='__main__':
 output=[fpds(piid) for piid in TARGETS]
 # Only test ordinary documented generated-ID forms; a 404 is not absence.
 for piid in TARGETS:
  for key in ['CONT_IDV_'+piid+'_9700','CONT_AWD_'+piid+'_97AE_-NONE-_-NONE-']:
   raw,receipt=fetch('https://api.usaspending.gov/api/v2/awards/'+key+'/')
   if raw is not None:
    try:receipt['resolved_generated_key']=json.loads(raw).get('generated_unique_award_id')
    except ValueError:receipt['semantic_status']='non-JSON response'
 (P/'evidence/ota-resolution-review.json').write_text(json.dumps({'targets':output,'accounting':'These four primary OT IDV records are a supplemental view. Deduplicate by agency+PIID+modification+transaction; do not add parent totals to child spending or sum unreconciled aggregates. The two IDs previously unresolved by a FAR-only parser are now identified.','raw_cache_public':False},indent=2)+'\n')
 initial=[]
 for piid in TARGETS:
  file=CACHE/(piid+'.xml')
  if file.exists():initial.append({'piid':piid,'source_url':next(r['url'] for r in LOG if 'fpds.gov/' in r['url'] and piid in urllib.parse.unquote(r['url'])),'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'local_file_mtime_utc_not_http_start':dt.datetime.fromtimestamp(file.stat().st_mtime,dt.timezone.utc).isoformat()})
 (P/'audit/ota-retrieval-log.json').write_text(json.dumps({'requests':LOG,'request_count':len(LOG),'failure_count':sum(x['status']=='failed' for x in LOG),'initial_probe_count':4,'initial_probes':initial,'initial_probe_note':'Four initial read-only FPDS probes identified the schema. Their original requests were visible in tool history; exact HTTP-start timestamps were not separately saved. File modification timestamps below are not substituted for HTTP request times. Original piid-named XML files remain private. The formal verification requests below have durable start/finish events and exact retrieval timestamps.','paid_calls':0},indent=2)+'\n')
 rows=[row for target in output for row in target['actions']]
 with (P/'evidence/ota-verified-actions.csv').open('w',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
 print(json.dumps([{k:v for k,v in r.items() if k not in ['actions','pages']} for r in output],indent=2))
