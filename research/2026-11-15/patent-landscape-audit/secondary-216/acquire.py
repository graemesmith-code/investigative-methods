import json,urllib.request,urllib.parse,concurrent.futures,pathlib,time,xml.etree.ElementTree as ET,subprocess,re
D=pathlib.Path('/tmp/deep216');rs=json.load(open(D/'records.json'));(D/'xml').mkdir(exist_ok=True);(D/'text').mkdir(exist_ok=True)
def get(url):
 p=subprocess.run(['curl','-sS','-L','--max-time','45',url],capture_output=True);return p.stdout
urls={}
for k in range(0,len(rs),30):
 q='SELECT ?pub ?url WHERE { VALUES ?pub { '+' '.join('<'+r['publication']+'>' for r in rs[k:k+30])+' } ?pub <http://data.epo.org/linked-data/def/patent/representation> ?url. }'
 (D/f'query_{k}.sparql').write_text(q)
 b=get('https://data.epo.org/linked-data/query?'+urllib.parse.urlencode({'query':q,'format':'application/sparql-results+json'}));(D/f'representations_{k}.json').write_bytes(b)
 data=json.loads(b)
 for x in data['results']['bindings']:
  if x['url']['value'].endswith('.xml'): urls[x['pub']['value']]=x['url']['value']
 print('mapping',k,len(urls),flush=True)
def run(ir):
 i,r=ir;u=urls.get(r['publication']);parts=r['publication'].split('/');pid='EP'+parts[-3]+parts[-2];out=dict(r,index=i,normalized_id=pid,url=u)
 if not u:out['status']='no_xml_representation';return out
 try:
  b=get(u);(D/'xml'/f'{i:03d}_{pid}.xml').write_bytes(b);root=ET.fromstring(b);sects=[]
  for el in root.iter():
   tag=el.tag.split('}')[-1]
   if tag in ['abstract','claims','description']:
    txt=' '.join(' '.join(el.itertext()).split());sects.append({'section':tag,'lang':el.attrib.get('lang',''),'text':txt})
  out['sections']=[{'section':s['section'],'lang':s['lang'],'characters':len(s['text'])} for s in sects];out['status']='claims_acquired' if any(s['section']=='claims' for s in sects) else 'metadata_only';out['text_path']=str(D/'text'/f'{i:03d}_{pid}.txt');open(out['text_path'],'w').write('\n\n'.join(s['section']+' ['+s['lang']+']\n'+s['text'] for s in sects));out['xml_bytes']=len(b)
 except Exception as e:out['status']='error';out['error']=str(e)
 return out
outs=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 for x in ex.map(run,enumerate(rs)):
  outs.append(x);print(x['index'],x['normalized_id'],x['status'],flush=True);json.dump(outs,open(D/'acquisition.json','w'),indent=2)
