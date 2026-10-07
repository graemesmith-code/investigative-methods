import pathlib,json,re,urllib.request,urllib.error,datetime,hashlib
P=pathlib.Path(__file__).resolve().parents[1];s=(P/'sources/pubdocs-main.js').read_text();fields=json.loads(re.search(r'EVENT_GQL=("(?:[^"\\]|\\.)*")',s).group(1));url='https://www1.aer.ca/wsPubDocs/search'
queries=[('licence-'+n,'AuthorizationID: "'+n+'"') for n in ['0515889','0516327','0516328','515889','516327','516328']]+[('pad-location','Location: {SEC:"31",TWP:"37",RGE:"28",M:"4"}')]
for name,flt in queries:
 payload={'query':f'query {{ events(filters: {{{flt}}},first:100,offset:0,sortBy:"EventID",sortDirection:-1) {{ Events {fields} first offset total }} }}'}
 (P/'sources'/f'pubdocs-{name}.request.json').write_text(json.dumps(payload,indent=2)+'\n');rec={'name':name,'url':url,'method':'POST read-only GraphQL query','request_file':f'pubdocs-{name}.request.json','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tls_verified':True}
 try:
  req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','User-Agent':'Public-record-research/1.0'})
  with urllib.request.urlopen(req,timeout=60) as r:b=r.read(10_000_000);rec['status']=r.status
  rec['sha256']=hashlib.sha256(b).hexdigest();(P/'sources'/f'pubdocs-{name}.json').write_bytes(b);x=json.loads(b);rec['summary']=x.get('errors') or {'total':x['data']['events']['total'],'returned':len(x['data']['events']['Events'])}
 except Exception as e:rec['error']=str(e)
 with (P/'results/pubdocs-query-log.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
 print(json.dumps(rec),flush=True)
