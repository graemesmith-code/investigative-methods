import urllib.request,urllib.parse,json,time,pathlib
D=pathlib.Path('/tmp/patent-coverage/expanded')
prefix='PREFIX patent: <http://data.epo.org/linked-data/def/patent/>\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n'
base='''SELECT DISTINCT ?app ?pub ?date ?title ?code WHERE {
 ?app ?cp ?code; patent:publication ?pub.
 VALUES ?cp { patent:classificationCPCInventive patent:classificationCPCAdditional }
 FILTER(%s)
 ?pub patent:publicationDate ?date; patent:titleOfInvention ?title.
 FILTER(lang(?title)="en")
 FILTER(?date >= "2021-11-15"^^xsd:date && ?date <= "2026-11-15"^^xsd:date)
 %s
} ORDER BY ?date ?pub LIMIT 1000'''
jobs=[('f41-safety-titles','STRSTARTS(STR(?code),"http://data.epo.org/linked-data/def/cpc/F41")','FILTER(regex(str(?title),"safe|inhibit|restrict|authoriz|authoris|collateral|control|autonom|identif|friend|target|prevent|abort|interlock|human","i"))'),('g05d-safety-titles','STRSTARTS(STR(?code),"http://data.epo.org/linked-data/def/cpc/G05D1-")','FILTER(regex(str(?title),"safe|inhibit|restrict|authoriz|authoris|collateral|weapon|military|abort|interlock|human|ethic","i"))'),('f41a17-all','STRSTARTS(STR(?code),"http://data.epo.org/linked-data/def/cpc/F41A17-")','')]
for name,c,t in jobs:
 q=prefix+base%(c,t);(D/(name+'.sparql')).write_text(q)
 u='https://data.epo.org/linked-data/query?'+urllib.parse.urlencode({'query':q})
 try:
  req=urllib.request.Request(u,headers={'Accept':'application/sparql-results+json'})
  with urllib.request.urlopen(req,timeout=80) as r:data=r.read()
  (D/(name+'.json')).write_bytes(data)
  j=json.loads(data);print(name,len(j.get('results',{}).get('bindings',[])),flush=True)
 except Exception as e:print(name,str(e),flush=True);(D/(name+'.error')).write_text(str(e))
 time.sleep(4)
