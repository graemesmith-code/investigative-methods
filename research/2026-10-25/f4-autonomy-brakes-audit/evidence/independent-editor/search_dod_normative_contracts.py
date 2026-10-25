import urllib.request,json,pathlib,concurrent.futures,datetime,hashlib
root=pathlib.Path('/tmp/f4-editor/normative-contract-search');root.mkdir(exist_ok=True);LOG=[]
def search(q):
 rows=[];page=1
 while True:
  body={'filters':{'keywords':[q],'award_type_codes':['A','B','C','D'],'agencies':[{'type':'awarding','tier':'toptier','name':'Department of Defense'}],'time_period':[{'start_date':'2019-01-01','end_date':'2026-10-25'}]},'fields':['Award ID','Recipient Name','Award Amount','Description','generated_internal_id','Start Date','End Date'],'limit':100,'page':page}
  url='https://api.usaspending.gov/api/v2/search/spending_by_award/'
  req=urllib.request.Request(url,data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
  with urllib.request.urlopen(req,timeout=40) as r:raw=r.read()
  LOG.append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':url,'method':'POST','body':body,'sha256':hashlib.sha256(raw).hexdigest()});data=json.loads(raw);(root/(q.replace(' ','-')+f'-{page}.json')).write_text(json.dumps(data,indent=2));rows+=data['results']
  if not data['page_metadata']['hasNext']:break
  page+=1
  if page>20:raise RuntimeError('Investigative scope too broad; narrow '+q)
 return {'query':q,'count':len(rows),'pages':page,'active_record_candidates':[r for r in rows if (r.get('End Date') or '')>='2026-10-25']}
if __name__=='__main__':
 out=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
  for r in ex.map(search,['ethical','rules of engagement','noncombatant','non-combatant','civilian harm','collateral damage']):out.append(r);print(json.dumps(r),flush=True)
 (root/'summary.json').write_text(json.dumps(out,indent=2));(root/'request-log.json').write_text(json.dumps(LOG,indent=2))
