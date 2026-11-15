import json,urllib.request,time,pathlib,xml.etree.ElementTree as E
D=pathlib.Path('/tmp/patent-coverage/expanded'); r=json.loads((D/'prioritized.json').read_text())['results']['bindings'];out=[]
for x in r:
 if x['p']['value'].endswith('/representation') and x['o']['value'].endswith('.xml'):
  u=x['o']['value']; n=x['pub']['value'].split('/publication/')[1].replace('/-','').replace('/',''); f=D/(n+'.xml')
  try:
   b=urllib.request.urlopen(u,timeout=45).read();f.write_bytes(b);root=E.fromstring(b);claims=[v for v in root.iter('claims')]; desc=list(root.iter('description')); print(n,len(b),'claims sections',len(claims),'desc',len(desc),flush=True)
   out.append({'pub':x['pub']['value'],'url':u,'file':f.name,'bytes':len(b),'claims_sections':len(claims),'descriptions':len(desc)})
  except Exception as e:out.append({'pub':x['pub']['value'],'url':u,'error':str(e)});print(n,str(e),flush=True)
  time.sleep(2)
(D/'download-log.json').write_text(json.dumps(out,indent=2))
