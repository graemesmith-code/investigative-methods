import urllib.request,json,pathlib,hashlib,datetime,sys
from log import log,P
def fetch(test,url,label,body=None):
 rows=[json.loads(x) for x in (P/'evidence/attempts.jsonl').read_text().splitlines()] if (P/'evidence/attempts.jsonl').exists() else []
 own=[r for r in rows if r['test_id']==test]
 assert sum(r['attempt_charge'] for r in own)<12,'attempt cap'
 if own:assert (datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(own[0]['utc'])).total_seconds()<900,'elapsed block cap'
 started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  req=urllib.request.Request(url,data=json.dumps(body).encode() if body else None,headers={'Content-Type':'application/json','User-Agent':'InvestigativeMethods bounded public research'})
  with urllib.request.urlopen(req,timeout=25) as r:
   data=r.read(1572865);meta=dict(http_status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),read_bytes=len(data),truncated=len(data)>1572864,tls_validation=True)
  if meta['truncated']:status='byte_cap';meta['saved']=False
  else:
   path=P/'evidence'/label;path.write_bytes(data);meta.update(saved=True,file=label,sha256=hashlib.sha256(data).hexdigest());status='retrieved'
 except Exception as e:meta=dict(error=str(e),tls_validation=True);status='failed'
 meta.update(started_utc=started,request_body=body)
 log(test,'http',url,status,meta);print(json.dumps(meta));return meta
if __name__=='__main__':fetch(*sys.argv[1:4],json.loads(sys.argv[4]) if len(sys.argv)>4 else None)
