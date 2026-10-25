import urllib.request,urllib.parse,json,pathlib,concurrent.futures,datetime,csv,hashlib,time
ROOT=pathlib.Path('/tmp/f4-editor/live-codord');ROOT.mkdir(exist_ok=True)
IDS=['HR001125F0028','HR00112590089']
LOG=[]
def fetch(path,body=None):
 url='https://api.usaspending.gov/api/v2/'+path
 req=urllib.request.Request(url,data=None if body is None else json.dumps(body).encode(),headers={'Content-Type':'application/json','User-Agent':'research-audit'})
 with urllib.request.urlopen(req,timeout=50) as r:raw=r.read()
 LOG.append({'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':url,'method':'GET' if body is None else 'POST','request':body,'sha256':hashlib.sha256(raw).hexdigest()})
 return json.loads(raw)
def one(piid):
 try:
  body={'filters':{'keywords':[piid],'award_type_codes':['A','B','C','D']},'fields':['Award ID','Recipient Name','Award Amount','Start Date','End Date','Description','generated_internal_id'],'limit':10,'page':1}
  search=fetch('search/spending_by_award/',body);(ROOT/(piid+'-search.json')).write_text(json.dumps(search,indent=2));rows=[]
  for s in search.get('results',[]):
   if s.get('Award ID')!=piid:continue
   k=s['generated_internal_id'];a=fetch('awards/'+urllib.parse.quote(k)+'/');(ROOT/(piid+'-award.json')).write_text(json.dumps(a,indent=2));tx=[];p=1
   while True:
    t=fetch('transactions/',{'award_id':a['id'],'page':p,'limit':100,'sort':'action_date','order':'desc'});tx.extend(t.get('results',[]));
    if not t.get('page_metadata',{}).get('hasNext'):break
    p+=1
   (ROOT/(piid+'-transactions.json')).write_text(json.dumps({'complete_paginated':True,'pages':p,'results':tx},indent=2));pop=a.get('period_of_performance',{})
   rows.append({'piid':piid,'key':k,'recipient':a.get('recipient',{}).get('recipient_name'),'signed':a.get('date_signed'),'start':pop.get('start_date'),'end':pop.get('end_date'),'potential_end':pop.get('potential_end_date'),'obligation':a.get('total_obligation'),'base_exercised':a.get('base_exercised_options'),'all_options':a.get('base_and_all_options'),'tx_count':len(tx),'tx_sum':sum(float(t.get('federal_action_obligation') or 0) for t in tx),'latest_action':max([t['action_date'] for t in tx],default=''),'description':a.get('description'),'url':'https://api.usaspending.gov/api/v2/awards/'+k+'/'})
  return rows or [{'piid':piid,'error':'no exact contract result (possibly other award category)'}]
 except Exception as e:return [{'piid':piid,'error':repr(e)}]
rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for r in pool.map(one,IDS):rows+=r;print(json.dumps(r))
(ROOT/'verified-summary.json').write_text(json.dumps(rows,indent=2));(ROOT/'request-log.json').write_text(json.dumps(LOG,indent=2))
keys=sorted(set(k for r in rows for k in r))
with (ROOT/'verified-summary.csv').open('w') as f:w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)
