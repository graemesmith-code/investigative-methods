"""Bounded availability/schema probes, not investigative screening. Explicit invocation only."""
import json,urllib.request,urllib.parse,datetime,hashlib,pathlib,concurrent.futures
OUT=pathlib.Path(__file__).resolve().parents[1]
LOG=OUT/'evidence/probes.jsonl'
def request(label,url,body=None,cap=256000):
 r={'label':label,'url':url,'request_body':body,'cap_bytes':cap,'requested_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'purpose':'bounded schema/availability probe; no allegation and no actor screening'}
 try:
  data=json.dumps(body).encode() if body is not None else None
  headers={'User-Agent':'InvestigativeMethods-source-feasibility/1.0','Accept':'application/json, application/xml;q=0.9, */*;q=0.1'}
  if data:headers['Content-Type']='application/json'
  with urllib.request.urlopen(urllib.request.Request(url,data=data,headers=headers),timeout=20) as resp:
   raw=resp.read(cap+1);r.update(http_status=resp.status,content_type=resp.headers.get('Content-Type'),bytes_read=len(raw))
  if len(raw)>cap:r['status']='response_exceeds_cap_not_saved';obj=None
  else:
   suffix='.json' if 'json' in r['content_type'] else '.xml' if 'xml' in r['content_type'] else '.txt'
   path=OUT/'evidence'/(label+suffix);path.write_bytes(raw);r.update(status='response_received',sha256=hashlib.sha256(raw).hexdigest(),file=str(path.relative_to(OUT)))
   try:obj=json.loads(raw)
   except ValueError:obj=None
 except Exception as e:r.update(status='failed',error_type=type(e).__name__,error=str(e)[:200]);obj=None
 with LOG.open('a') as f:f.write(json.dumps(r)+'\n')
 return r,obj
PROBES=[
 ('ofac-advanced-schema','https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/ADVANCED_XML.xsd',None),
 ('usa-award-one','https://api.usaspending.gov/api/v2/search/spending_by_award/',{'filters':{'award_type_codes':['A','B','C','D'],'time_period':[{'start_date':'2025-01-01','end_date':'2025-01-31'}]},'fields':['Award ID','Recipient Name','Recipient UEI','Recipient Location','Start Date','End Date','Award Amount','generated_internal_id'],'limit':1,'page':1,'sort':'Award Amount','order':'desc'}),
 ('trial-full-one','https://clinicaltrials.gov/api/v2/studies?pageSize=1&format=json&filter.overallStatus=COMPLETED',None),
 ('worldbank-project-one','https://search.worldbank.org/api/v2/projects?format=json&rows=1&os=0',None),
 ('worldbank-doc-one','https://search.worldbank.org/api/v3/wds?format=json&rows=1&os=0&fl=docdt,docty,projectid,display_title,pdfurl,txturl',None),
 ('ooni-one-metadata','https://api.ooni.org/api/v1/measurements?limit=1&since=2025-01-01&until=2025-01-02&test_name=web_connectivity',None),
 ('crossref-one','https://api.crossref.org/works?rows=1&filter=has-clinical-trial-number:true',None),
]
def main():
 if LOG.exists():raise SystemExit('Existing log preserved; adaptive probes must be called individually.')
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for r,o in pool.map(lambda p:request(*p),PROBES):print(json.dumps({k:v for k,v in r.items() if k not in ['request_body']}))
if __name__=='__main__':main()
