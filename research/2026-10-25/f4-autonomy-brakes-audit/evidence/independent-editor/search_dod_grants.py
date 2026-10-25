import urllib.request,json,pathlib,concurrent.futures,datetime,hashlib
root=pathlib.Path('/tmp/f4-editor/grant-search');root.mkdir(exist_ok=True)
LOG=[]
def search(q):
 body={'filters':{'keywords':[q],'award_type_codes':['02','03','04','05'],'agencies':[{'type':'awarding','tier':'toptier','name':'Department of Defense'}]},'fields':['Award ID','Recipient Name','Award Amount','Description','generated_internal_id','Start Date','End Date'],'limit':100,'page':1}
 url='https://api.usaspending.gov/api/v2/search/spending_by_award/'
 req=urllib.request.Request(url,data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=30) as r: raw=r.read()
 LOG.append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':url,'method':'POST','body':body,'sha256':hashlib.sha256(raw).hexdigest()})
 data=json.loads(raw);(root/(q+'-search.json')).write_text(json.dumps(data,indent=2))
 if data['page_metadata']['hasNext']: raise RuntimeError('Additional pages required: '+q)
 return {'query':q,'count':len(data['results']),'hasNext':False}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
  for r in ex.map(search,['ethical','deontic','moral','civilian harm']):print(json.dumps(r))
 (root/'request-log.json').write_text(json.dumps(LOG,indent=2))
