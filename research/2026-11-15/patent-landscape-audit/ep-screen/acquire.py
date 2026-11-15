import pathlib,urllib.request,urllib.parse,json,time,xml.etree.ElementTree as E
D=pathlib.Path('/tmp/patent-coverage/ep-screen'); ids=['EP4647709A1','EP4653796A1','EP4033309A1','EP4111281B1','EP4293311A1','EP3732432B1']
import re
uris=['http://data.epo.org/linked-data/data/publication/EP/'+re.match(r'EP(\d+)([AB]\d)',n).group(1)+'/'+re.match(r'EP(\d+)([AB]\d)',n).group(2)+'/-' for n in ids]
q='SELECT ?pub ?url WHERE { VALUES ?pub { '+' '.join('<'+u+'>' for u in uris)+' } ?pub <http://data.epo.org/linked-data/def/patent/representation> ?url. }'
(D/'query.sparql').write_text(q)
req=urllib.request.Request('https://data.epo.org/linked-data/query?'+urllib.parse.urlencode({'query':q}),headers={'Accept':'application/sparql-results+json'})
b=urllib.request.urlopen(req,timeout=60).read();(D/'representations.json').write_bytes(b);log=[]
for x in json.loads(b)['results']['bindings']:
 u=x['url']['value'];n=x['pub']['value'].split('/publication/')[1].replace('/-','').replace('/','')
 if not u.endswith('.xml'):continue
 try:
  data=urllib.request.urlopen(u,timeout=45).read();(D/(n+'.xml')).write_bytes(data);r=E.fromstring(data)
  out={'id':n,'url':u,'bytes':len(data),'claims_sections':len(r.findall('.//claims'))};log.append(out);print(out,flush=True)
  txt=[]
  for c in r.findall('.//claims'):
   if c.get('lang')=='en':txt.append(' '.join(c.itertext()))
  (D/(n+'-claims.txt')).write_text('\n'.join(txt))
 except Exception as e:log.append({'id':n,'url':u,'error':str(e)});print(n,e,flush=True)
 time.sleep(1)
(D/'download-log.json').write_text(json.dumps(log,indent=2))
