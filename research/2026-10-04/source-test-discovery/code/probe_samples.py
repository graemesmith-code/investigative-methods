"""OPTIONAL network step. Three fixed, small free schema/record checks; no screening.
Standard-library requests. Does not run investigative tests or call model/search APIs.
Run once intentionally; use saved results for ordinary reproduction.
"""
import json,urllib.request,urllib.error,datetime,hashlib
from normalize import OUT
PROBES=[
 ('SYS-0001','gleif-one-record','https://api.gleif.org/api/v1/lei-records/5493001KJTIIGC8Y1R12'),
 ('SYS-0248','clinicaltrials-one-record','https://clinicaltrials.gov/api/v2/studies?pageSize=1&format=json&fields=NCTId,BriefTitle,LeadSponsorName'),
 ('SYS-0149','cisa-schema','https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities_schema.json'),
]
def main():
 results=[]
 for sid,label,url in PROBES:
  r=dict(sys_id=sid,label=label,url=url,requested_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),max_bytes=200000,purpose='availability/schema only; not an investigative match')
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'InvestigativeMethods-source-documentation-check/1.0','Accept':'application/json'})
   with urllib.request.urlopen(req,timeout=20) as response:
    body=response.read(200001);r.update(http_status=response.status,content_type=response.headers.get('Content-Type'),bytes_read=len(body))
   if len(body)>200000:r['status']='rejected_response_too_large'
   else:
    obj=json.loads(body);path=OUT/'evidence'/(label+'.json');path.write_bytes(body)
    r.update(status='sample_received',sha256=hashlib.sha256(body).hexdigest(),saved_path=str(path.relative_to(OUT)),top_level_keys=list(obj)[:20],inference_limit='One response proves only this request succeeded; no completeness, history, identity match or execution feasibility established.')
  except Exception as e:r.update(status='failed',error_type=type(e).__name__,error=str(e)[:200])
  results.append(r)
 (OUT/'evidence/sample-access-log.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps([{k:v for k,v in r.items() if k not in ['top_level_keys']} for r in results],indent=2))
if __name__=='__main__':main()
