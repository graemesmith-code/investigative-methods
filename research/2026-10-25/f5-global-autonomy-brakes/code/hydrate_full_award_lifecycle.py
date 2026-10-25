#!/usr/bin/env python3
"""Hydrate exact US award identities from public USAspending and FPDS.

Usage: python hydrate_full_award_lifecycle.py --candidates candidates.csv --out data
Required CSV field: award_key (USAspending generated_unique_award_id). Optional
fields: archived_action_count, selection_basis. Raw replies and event journal are
stored below --out/financial-raw, never committed by this program.

No date or keyword filters on transaction histories. Discovery is separate from
hydration. Agency, PIID, parent agency/PIID and schema identity are checked; an
unresolved identity is not replaced with a guessed agency. Decimal action sums
retain negatives. Award/FPDS are agency-derived views, not independent evidence.
"""
import argparse,csv,datetime,decimal,hashlib,json,os,pathlib,urllib.error,urllib.parse,urllib.request,xml.etree.ElementTree as ET
D=decimal.Decimal;A='{http://www.w3.org/2005/Atom}';F='{https://www.fpds.gov/FPDS}'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def money(value):return D(str(value)) if value not in (None,'') else None
def total(rows,field):
 vals=[money(x.get(field)) for x in rows];return sum((x for x in vals if x is not None),D(0)),sum(x is None for x in vals)
def get(node,path):return node.findtext('/'.join(F+x for x in path.split('/')),'') if node is not None else ''
class Client:
 def __init__(self,path):self.path=path;path.mkdir(parents=True,exist_ok=True)
 def fetch(self,url,body=None):
  meta={'url':url,'method':'POST' if body is not None else 'GET','retrieved_utc':utc()}
  if body is not None:meta['request_body']=body
  def log(status):
   with (self.path/'request-events.jsonl').open('a') as f:f.write(json.dumps({**meta,'state':status})+'\n');f.flush();os.fsync(f.fileno())
  log('started');raw=None
  try:
   req=urllib.request.Request(url,data=json.dumps(body).encode() if body is not None else None,headers={'User-Agent':'public-source-governance-research/1.0','Content-Type':'application/json'})
   with urllib.request.urlopen(req,timeout=50) as r:raw=r.read();meta.update(http_status=r.status,final_url=r.url)
   meta.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest());(self.path/(meta['sha256']+'.raw')).write_bytes(raw)
  except Exception as e:
   meta.update(error=type(e).__name__+': '+str(e),http_status=getattr(e,'code',None))
   if isinstance(e,urllib.error.HTTPError):
    err=e.read();meta['error_body_sha256']=hashlib.sha256(err).hexdigest();(self.path/(meta['error_body_sha256']+'.raw')).write_bytes(err)
  log('finished');return raw,meta
def identity(key):
 if key.startswith(('FPDS_OTHER_TRANSACTION_IDV:','FPDS_OTHER_TRANSACTION_AWARD:')):
  p=key.split(':')
  if len(p)!=3:raise ValueError('Malformed native FPDS OT identity')
  return {'schema':'OtherTransactionIDV' if p[0]=='FPDS_OTHER_TRANSACTION_IDV' else 'OtherTransactionAward','piid':p[2],'agency_id':p[1],'parent_piid':'','parent_agency_id':''}
 p=key.split('_')
 if key.startswith('CONT_AWD_') and len(p)==6:return {'schema':'award','piid':p[2],'agency_id':p[3],'parent_piid':'' if p[4]=='-NONE-' else p[4],'parent_agency_id':'' if p[5]=='-NONE-' else p[5]}
 if key.startswith('CONT_IDV_') and len(p)==4:return {'schema':'IDV','piid':p[2],'agency_id':p[3],'parent_piid':'','parent_agency_id':''}
 if key.startswith('ASST_'):return {'schema':'assistance'}
 raise ValueError('Unsupported generated identity; supply verified CONT_AWD/CONT_IDV/ASST key')
def transactions(client,key):
 page=1;seen=set();rows={};pages=[];conflicts=[];missing=[];complete=False
 while True:
  raw,meta=client.fetch('https://api.usaspending.gov/api/v2/transactions/',{'award_id':key,'page':page,'limit':100});pages.append(meta)
  if raw is None:break
  try:o=json.loads(raw)
  except ValueError:meta['error']='non-JSON body';break
  batch=o.get('results');pm=o.get('page_metadata')
  if not isinstance(batch,list) or not isinstance(pm,dict) or 'hasNext' not in pm:meta['error']='missing transaction pagination schema';break
  sig=hashlib.sha256(json.dumps(batch,sort_keys=True).encode()).hexdigest()
  if batch and sig in seen:meta['error']='pagination cycle';break
  seen.add(sig)
  for i,r in enumerate(batch):
   k=r.get('id')
   if k is None:k='missing:'+str(page)+':'+str(i);missing.append(k)
   if k in rows and rows[k]['transaction']!=r:conflicts.append(k)
   rows[k]={'transaction':r,'request_page':page,'response_sha256':meta['sha256'],'retrieved_utc':meta['retrieved_utc']}
  if not pm['hasNext']:complete=True;break
  page+=1
 ordered=sorted(rows.values(),key=lambda x:(x['transaction'].get('action_date') or '',str(x['transaction'].get('id'))));s,n=total([r['transaction'] for r in ordered],'federal_action_obligation')
 return {'pages':pages,'pagination_complete':complete,'action_count':len(ordered),'action_sum_usd':str(s),'null_obligations':n,'missing_ids':missing,'duplicate_conflicts':conflicts,'actions':ordered}
def fpds(client,ident):
 q='PIID:"'+ident['piid']+'"'
 if ident['parent_piid']:q+=' REF_IDV_PIID:"'+ident['parent_piid']+'"'
 # No date, title or keyword selection in lifecycle feed. Returned identities
 # are checked below even when the search index treats a field imprecisely.
 url='https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&VERSION=1.5.3&q='+urllib.parse.quote(q)+'&s=FPDSNG.COM&indexName=awardfull&start=0'
 seen=set();rows={};pages=[];unparsed=[];excluded=[];conflicts=[];complete=False
 while url:
  if url in seen:unparsed.append({'error':'pagination_cycle','url':url});break
  seen.add(url);raw,meta=client.fetch(url);pages.append(meta)
  if raw is None:break
  try:root=ET.fromstring(raw)
  except ET.ParseError as e:unparsed.append({'error':str(e),'url':url});break
  for entry in root.findall(A+'entry'):
   content=entry.find(A+'content');payload=list(content)[0] if content is not None and len(content) else None
   if payload is None:unparsed.append({'error':'missing payload','url':url});continue
   schema=payload.tag.split('}')[-1]
   if schema=='award':identnode=payload.find(F+'awardID/'+F+'awardContractID');parent=payload.find(F+'awardID/'+F+'referencedIDVID');detail=payload
   elif schema=='OtherTransactionIDV':identnode=payload.find(F+'OtherTransactionIDVID/'+F+'OtherTransactionIDVContractID');parent=None;detail=payload.find(F+'contractDetail')
   elif schema=='OtherTransactionAward':identnode=payload.find(F+'OtherTransactionAwardID/'+F+'OtherTransactionAwardContractID');parent=payload.find(F+'OtherTransactionAwardID/'+F+'referencedIDVID');detail=payload.find(F+'contractDetail')
   elif schema=='IDV':identnode=payload.find(F+'IDVID/'+F+'IDVContractID');parent=None;detail=payload
   else:unparsed.append({'schema':schema,'url':url});continue
   r={k:get(identnode,p) for k,p in {'piid':'PIID','agency_id':'agencyID','modification':'modNumber','transaction':'transactionNumber'}.items()};r.update(schema=schema,parent_piid=get(parent,'PIID'),parent_agency_id=get(parent,'agencyID'))
   # An OT IDV is not silently recast as a FAR contract or vice versa.
   match=all(r[k]==ident[k] for k in ['piid','agency_id','parent_piid','parent_agency_id'])
   schema_match=schema==ident['schema']
   if not match or not schema_match:excluded.append({k:r[k] for k in ['schema','piid','agency_id','parent_piid','parent_agency_id']});continue
   if identnode is None or detail is None:unparsed.append({'error':'identity/detail missing','schema':schema});continue
   for k,p in {'signed_date':'relevantContractDates/signedDate','effective_date':'relevantContractDates/effectiveDate','current_end':'relevantContractDates/currentCompletionDate','potential_end':'relevantContractDates/ultimateCompletionDate','obligation_usd':'dollarValues/obligatedAmount','all_options_change_usd':'dollarValues/baseAndAllOptionsValue','aggregate_obligation_usd':'totalDollarValues/totalObligatedAmount','aggregate_all_options_usd':'totalDollarValues/totalBaseAndAllOptionsValue','recipient':'vendor/vendorHeader/vendorName','recipient_uei':'vendor/vendorSiteDetails/entityIdentifiers/vendorUEIInformation/UEI','description':'contractData/descriptionOfContractRequirement','reason_code':'contractData/reasonForModification'}.items():r[k]=get(detail,p)
   r.update(record_modified=entry.findtext(A+'modified',''),source_url=url,response_sha256=meta['sha256'],retrieved_utc=meta['retrieved_utc']);k=tuple(r[x] for x in ['schema','agency_id','piid','parent_piid','parent_agency_id','modification','transaction'])
   if k in rows and any(rows[k][x]!=r[x] for x in ['obligation_usd','signed_date','description']):conflicts.append(k)
   rows[k]=r
  nxt=[x.get('href') for x in root.findall(A+'link') if x.get('rel')=='next']
  if not nxt:complete=True;url=None
  else:url=urllib.parse.urljoin(url,nxt[0])
 ordered=sorted(rows.values(),key=lambda r:(r['signed_date'],r['modification'],r['transaction']));s,n=total(ordered,'obligation_usd')
 return {'pages':pages,'pagination_complete':complete,'action_count':len(ordered),'action_sum_usd':str(s),'null_obligations':n,'duplicate_conflicts':conflicts,'unparsed_entries':unparsed,'excluded_identities':excluded,'actions':ordered}
def hydrate(client,candidate):
 key=candidate['award_key'];ident=identity(key);r={'candidate':candidate,'award_key':key,'identity':ident,'retrieved_utc':utc()}
 if ident['schema'] in ['OtherTransactionIDV','OtherTransactionAward']:
  # Native FPDS identity is sufficient for exact OT action retrieval, but it
  # is not a USAspending generated key. Never guess a cross-system match.
  r.update(identity_verified=False,usaspending_transactions={'status':'unverified_cross_system_mapping','not_applicable':'A generated USAspending key has not been verified for this native FPDS identity; no guessed endpoint key requested. This is a retrieval limitation, not a claim that OT histories never apply.'},fpds=fpds(client,ident))
  fp=r['fpds'];actions=fp['actions'];latest=max(actions,key=lambda x:(x['signed_date'],x['record_modified']),default={});expected=money(latest.get('aggregate_obligation_usd'))
  fp['feed_aggregate_obligation_usd']=str(expected) if expected is not None else None;fp['minus_feed_aggregate_usd']=str(money(fp['action_sum_usd'])-expected) if expected is not None else None
  fp['reconciled']=bool(expected is not None and fp['pagination_complete'] and fp['action_count'] and not fp['null_obligations'] and not fp['duplicate_conflicts'] and not fp['unparsed_entries'] and money(fp['action_sum_usd'])==expected)
  r['identity_verified']=bool(actions and fp['pagination_complete'] and not fp['unparsed_entries']);r['note']='Native FPDS '+ident['schema']+' identity verified separately; USAspending mapping remains unverified and cross-system reconciliation unavailable. FPDS action sum/feed aggregate agreement is one agency-derived source view, not independent corroboration. High-assurance description does not prove an engagement legal governor. Neither parent ceiling nor grants/outlays substituted.'
  return r
 raw,receipt=client.fetch('https://api.usaspending.gov/api/v2/awards/'+urllib.parse.quote(key,safe='')+'/');r['award_receipt']=receipt
 if raw is not None:
  try:r['award']=json.loads(raw)
  except ValueError:r['award_error']='non-JSON body'
 award=r.get('award',{});r['identity_verified']=award.get('generated_unique_award_id')==key
 if award and not r['identity_verified']:r['award_error']='generated unique identity mismatch; money not promoted'
 # Still retrieve exact-key transaction history on an unavailable award detail;
 # retain failures and do not use discovery result as financial denominator.
 r['usaspending_transactions']=transactions(client,key)
 r['fpds']=fpds(client,ident) if ident['schema']!='assistance' else {'not_applicable':'assistance is not a FAR/OT FPDS denominator'}
 expected=money(award.get('total_obligation'));tx=r['usaspending_transactions'];feed=r['fpds']
 for evidence in [tx,feed]:
  if 'action_sum_usd' not in evidence:continue
  evidence['minus_award_total_usd']=str(money(evidence['action_sum_usd'])-expected) if expected is not None and r['identity_verified'] else None
  evidence['reconciled']=bool(r['identity_verified'] and expected is not None and evidence['pagination_complete'] and evidence['action_count'] and not evidence['null_obligations'] and not evidence['duplicate_conflicts'] and not evidence.get('missing_ids') and not evidence.get('unparsed_entries') and money(evidence['action_sum_usd'])==expected)
 r['note']='Net obligations are agency-reported commitments, not outlays, safeguards expenditure, implementation or certification. FPDS and USAspending are related reported data views; DoD public-release lag limits recent absence claims. PoP start is not a signature date. No prime/subaward/IDV ceiling addition.'
 return r
def write_outputs(out,records):
 def atomic(path,body):
  temp=path.with_suffix(path.suffix+'.tmp')
  with temp.open('w') as f:f.write(body);f.flush();os.fsync(f.fileno())
  temp.replace(path)
 atomic(out/'safety-board-contracts-hydrated.json',json.dumps({'schema_version':1,'new_F5_live_run':True,'scope':'Exact machine-hit candidate histories plus primary live leads; promotion tier and description scope remain separate from funding verification','records':records},indent=2)+'\n')
 fields=['award_key','evidence_tier','recipient','recipient_uei','identity_verified','archived_action_count','usaspending_total_obligation_usd','all_options_value_usd','award_date_signed','period_of_performance_start','period_of_performance_current_end','usa_action_count','usa_pages_exhausted','usa_action_sum_usd','usa_minus_award_usd','usa_reconciled','fpds_action_count','fpds_pages_exhausted','fpds_action_sum_usd','fpds_feed_aggregate_usd','fpds_minus_award_usd','fpds_minus_feed_aggregate_usd','fpds_reconciled','fpds_base_mod_present','fpds_earliest_signature','negative_fpds_actions','selection_basis','limitation']
 import io
 stream=io.StringIO(newline='');w=csv.DictWriter(stream,fields);w.writeheader()
 for r in records:
  a=r.get('award',{});tx=r.get('usaspending_transactions',{});fp=r.get('fpds',{});pop=a.get('period_of_performance') or {};actions=fp.get('actions',[]);rec=a.get('recipient') or {};latest=max(actions,key=lambda x:(x['signed_date'],x['record_modified']),default={});native=r['identity']['schema'].startswith('OtherTransaction')
  row={'award_key':r['award_key'],'evidence_tier':r['candidate'].get('evidence_tier','promoted_case_or_regression'),'recipient':rec.get('recipient_name') or latest.get('recipient'),'recipient_uei':rec.get('recipient_uei') or latest.get('recipient_uei'),'identity_verified':r['identity_verified'],'archived_action_count':r['candidate'].get('archived_action_count'),'usaspending_total_obligation_usd':str(a['total_obligation']) if r['identity_verified'] and 'total_obligation' in a else '', 'all_options_value_usd':str(a['base_and_all_options']) if r['identity_verified'] and 'base_and_all_options' in a else latest.get('aggregate_all_options_usd',''), 'award_date_signed':a.get('date_signed'),'period_of_performance_start':pop.get('start_date'),'period_of_performance_current_end':pop.get('end_date') or (latest.get('current_end') if native else ''),'usa_action_count':tx.get('action_count'),'usa_pages_exhausted':tx.get('pagination_complete'),'usa_action_sum_usd':tx.get('action_sum_usd'),'usa_minus_award_usd':tx.get('minus_award_total_usd'),'usa_reconciled':tx.get('reconciled'),'fpds_action_count':fp.get('action_count'),'fpds_pages_exhausted':fp.get('pagination_complete'),'fpds_action_sum_usd':fp.get('action_sum_usd'),'fpds_feed_aggregate_usd':fp.get('feed_aggregate_obligation_usd'),'fpds_minus_award_usd':fp.get('minus_award_total_usd'),'fpds_minus_feed_aggregate_usd':fp.get('minus_feed_aggregate_usd'),'fpds_reconciled':fp.get('reconciled'),'fpds_base_mod_present':any(x['modification']=='0' for x in actions),'fpds_earliest_signature':min((x['signed_date'] for x in actions),default=''),'negative_fpds_actions':sum(money(x['obligation_usd'])<0 for x in actions if money(x['obligation_usd']) is not None),'selection_basis':r['candidate'].get('selection_basis'),'limitation':r['note']}
  w.writerow(row)
 atomic(out/'full-lifecycle-reconciliation-audit.csv',stream.getvalue())
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--candidates',required=True,type=pathlib.Path);p.add_argument('--out',required=True,type=pathlib.Path);p.add_argument('--resume',action='store_true',help='Reuse existing records; incomplete records emit a warning unless --retry-incomplete is set');p.add_argument('--retry-incomplete',action='store_true',help='With --resume, replace failed/incomplete read-only histories with a fresh attempt');args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True);client=Client(args.out/'financial-raw');records=[]
 if args.resume and (args.out/'safety-board-contracts-hydrated.json').exists():records=json.loads((args.out/'safety-board-contracts-hydrated.json').read_text())['records']
 seen={r['award_key'] for r in records}
 for c in csv.DictReader(args.candidates.open()):
  if c['award_key'] in seen:
   previous=next(r for r in records if r['award_key']==c['award_key']);tx=previous.get('usaspending_transactions',{});fp=previous.get('fpds',{});complete=previous.get('identity_verified') and (tx.get('pagination_complete') or tx.get('not_applicable')) and (fp.get('pagination_complete') or fp.get('not_applicable'))
   if complete:continue
   if not args.retry_incomplete:
    print(json.dumps({'award_key':c['award_key'],'warning':'Existing incomplete record retained; use --retry-incomplete to request new read-only histories'}),flush=True);continue
   records=[r for r in records if r['award_key']!=c['award_key']]
  r=hydrate(client,c);records.append(r);seen.add(c['award_key']);write_outputs(args.out,records)
  print(json.dumps({'award_key':r['award_key'],'identity_verified':r['identity_verified'],'usa_count':r['usaspending_transactions'].get('action_count'),'fpds_count':r['fpds'].get('action_count'),'usa_reconciled':r['usaspending_transactions'].get('reconciled'),'fpds_reconciled':r['fpds'].get('reconciled')}),flush=True)
if __name__=='__main__':main()
