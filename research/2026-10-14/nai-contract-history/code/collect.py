import os
import urllib.request,urllib.parse,urllib.error,json,datetime,hashlib,pathlib,concurrent.futures
ROOT=pathlib.Path(os.environ['NAI_AUDIT_DIR']);BASE='https://api.usaspending.gov'
def fetch(label,url,body=None):
 if url.startswith('/'):url=BASE+url
 data=json.dumps(body).encode() if body is not None else None
 req=urllib.request.Request(url,data=data,headers={'Content-Type':'application/json','User-Agent':'public-records-research/1.0'})
 meta={'url':url,'method':'POST' if data else 'GET','body':body,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(req,timeout=50) as r:b=r.read();meta.update(status=r.status,final_url=r.url)
 except urllib.error.HTTPError as e:b=e.read();meta.update(status=e.code,error=str(e))
 except Exception as e:b=str(e).encode();meta.update(error=str(e))
 meta.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest());(ROOT/'raw'/f'{label}.body').write_bytes(b);(ROOT/'raw'/f'{label}.request.json').write_text(json.dumps(meta,indent=2))
 try:return json.loads(b)
 except:return b.decode(errors='replace')
def paginate(label,url,body):
 rows=[];page=1
 while True:
  payload={**body,'page':page,'limit':100};r=fetch(f'{label}-p{page:03}',url,payload)
  if not isinstance(r,dict) or 'results' not in r:raise ValueError((label,r))
  rows+=r['results'];print(label,page,len(r['results']),r.get('page_metadata'),flush=True)
  if not r.get('page_metadata',{}).get('hasNext'):break
  page+=1
 (ROOT/f'{label}.json').write_text(json.dumps(rows,indent=2));return rows
if __name__=='__main__':
 tasks=[('doc-transactions','https://raw.githubusercontent.com/fedspendingtransparency/usaspending-api/master/usaspending_api/api_contracts/contracts/v2/transactions.md',None),('doc-search','https://raw.githubusercontent.com/fedspendingtransparency/usaspending-api/master/usaspending_api/api_contracts/contracts/v2/search/spending_by_award.md',None),('doc-search-transactions','https://raw.githubusercontent.com/fedspendingtransparency/usaspending-api/master/usaspending_api/api_contracts/contracts/v2/search/spending_by_transaction.md',None),('doc-download-contract','https://raw.githubusercontent.com/fedspendingtransparency/usaspending-api/master/usaspending_api/api_contracts/contracts/v2/download/contract.md',None),('doc-filters','https://raw.githubusercontent.com/fedspendingtransparency/usaspending-api/master/usaspending_api/api_contracts/contracts/v2/search/spending_by_award_count.md',None),('vehicle','/api/v2/awards/CONT_IDV_SPE60523D9402_9700/',None),('count-vehicle','/api/v2/awards/count/transaction/CONT_IDV_SPE60523D9402_9700/',None),('recipient-autocomplete','/api/v2/autocomplete/recipient/',{'search_text':'NAI LOGISTICS','limit':100}),('uei-autocomplete','/api/v2/autocomplete/recipient/',{'search_text':'SLVJF3DR8MN5','limit':100})]
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
  for label,r in ex.map(lambda t:(t[0],fetch(*t)),tasks):print(label,str(r)[:1000],flush=True)
 for typ in ['child_awards','child_idvs','grandchild_awards']:
  paginate('vehicle-'+typ,'/api/v2/idvs/awards/',{'award_id':'CONT_IDV_SPE60523D9402_9700','type':typ,'sort':'piid','order':'asc'})
