#!/usr/bin/env python3
"""Bounded public FPDS keyword follow-up for deontic/assurance program IDs."""
import datetime as dt,hashlib,json,pathlib,re,urllib.parse,urllib.request,xml.etree.ElementTree as ET
P=pathlib.Path(__file__).resolve().parents[1];CACHE=pathlib.Path('/workspace/scratch/f4-ota-keywords');CACHE.mkdir(parents=True,exist_ok=True)
A='{http://www.w3.org/2005/Atom}';F='{https://www.fpds.gov/FPDS}'
QUERIES=['CODORD','"HUMAN-AI" "DEONTIC"','DONATELLO','KRADL','DROIDDS','TIAMAT','DESCRIPTION_OF_REQUIREMENT:"CODORD"','DESCRIPTION_OF_REQUIREMENT:"DEONTIC"','"SRI" "DEONTIC"']
MATCH=re.compile(r'CODORD|DEONTIC|DONATELLO|KRADL|DROIDDS|TIAMAT',re.I)
LOG=[]
def fetch(url):
 r={'url':url,'method':'GET','retrieved_utc':dt.datetime.now(dt.timezone.utc).isoformat()}
 with (CACHE/'request-events.jsonl').open('a') as f:f.write(json.dumps({**r,'state':'started'})+'\n')
 try:
  with urllib.request.urlopen(url,timeout=40) as response:b=response.read();r.update(http_status=response.status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  (CACHE/(r['sha256']+'.xml')).write_bytes(b)
 except Exception as e:r.update(http_status=getattr(e,'code',None),error=repr(e));b=None
 LOG.append(r)
 with (CACHE/'request-events.jsonl').open('a') as f:f.write(json.dumps({**r,'state':'finished'})+'\n')
 return b,r
def local(tag):return tag.split('}')[-1]
def find(node,name):
 return next((x for x in node.iter() if local(x.tag)==name),None)
def text(node,name):
 x=find(node,name);return x.text if x is not None and x.text is not None else ''
def scan(query):
 url='https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&VERSION=1.5.3&q='+urllib.parse.quote(query)+'&s=FPDSNG.COM&indexName=awardfull&start=0'
 seen=set();pages=[];entries=[];unknown=[];complete=False
 while url:
  if url in seen:unknown.append({'error':'pagination_cycle','url':url});break
  seen.add(url);b,receipt=fetch(url);pages.append(receipt)
  if b is None:break
  try:root=ET.fromstring(b)
  except ET.ParseError as e:unknown.append({'error':str(e)});break
  for entry in root.findall(A+'entry'):
   content=entry.find(A+'content');payload=list(content)[0] if content is not None and len(content) else None
   if payload is None:unknown.append({'title':entry.findtext(A+'title'),'error':'missing payload'});continue
   schema=local(payload.tag);description=text(payload,'descriptionOfContractRequirement')
   piid=text(payload,'PIID');keyword=bool(MATCH.search(description));program=keyword and piid.startswith('HR0011')
   item={'schema':schema,'title':entry.findtext(A+'title'),'piid':piid,'agency_id':text(payload,'agencyID'),'modification':text(payload,'modNumber'),'transaction_number':text(payload,'transactionNumber'),'recipient':text(payload,'vendorName'),'description':description,'action_obligation_usd':text(payload,'obligatedAmount'),'aggregate_obligation_usd':text(payload,'totalObligatedAmount'),'signed_date':text(payload,'signedDate'),'current_end':text(payload,'currentCompletionDate'),'potential_end':text(payload,'ultimateCompletionDate'),'keyword_match':keyword,'matched_program_content':program,'program_filter_note':'DARPA-prefix identity plus explicit deontic/program term; not a technical effectiveness finding' if program else 'Keyword collision outside DARPA program identities; excluded from program leads','source_url':url,'response_sha256':receipt['sha256'],'retrieved_utc':receipt['retrieved_utc']}
   entries.append(item)
  nxt=next((x.get('href') for x in root.findall(A+'link') if x.get('rel')=='next'),None)
  if not nxt:complete=True;url=None
  else:url=urllib.parse.urljoin(url,nxt)
 return {'query':query,'pages':pages,'pagination_complete':complete,'returned_entry_count':len(entries),'matched_program_entry_count':sum(x['matched_program_content'] for x in entries),'entries':entries,'parse_notes':unknown}
if __name__=='__main__':
 scopes=[scan(q) for q in QUERIES];matches={}
 for s in scopes:
  for r in s['entries']:
   if r['matched_program_content']:matches.setdefault((r['agency_id'],r['piid'],r['modification'],r['transaction_number']),r)
 records=list(matches.values());ids=sorted({(r['agency_id'],r['piid'],r['recipient']) for r in records});sri=[r for r in records if re.search(r'\bSRI\b|STANFORD RESEARCH',r['recipient'],re.I)]
 result={'scopes':scopes,'requests':LOG,'request_count':len(LOG),'failed_request_count':sum('error' in r for r in LOG),'all_successful_scopes_pagination_complete':all(s['pagination_complete'] for s in scopes if not any('error' in p for p in s['pages'])),'unique_matching_actions':len(records),'unique_matching_identities':[{'agency_id':a,'piid':b,'recipient':c} for a,b,c in ids],'sri_matching_actions':sri,'limit':'Keyword-search hits are discovery records, not complete award histories or a census. Program keywords in generic FPDS search may return fewer matching actions than exact-PIID feeds. Source descriptions and primary identities are preserved; no additional award financial totals are reconciled from these keyword subsets.','initial_probe_note':'One preceding read-only CODORD probe returned two USC entries. Formal repeated query is fully logged here; no exact original start timestamp is reconstructed.','paid_calls':0}
 (P/'audit/ota-keyword-followups.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ['scopes','requests','sri_matching_actions']},indent=2));print('SRI matching actions',len(sri))
