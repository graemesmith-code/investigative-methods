import json,urllib.request,urllib.parse,concurrent.futures,pathlib,time,xml.etree.ElementTree as ET,subprocess,re
D=pathlib.Path('/tmp/deep216');rs=json.load(open(D/'records.json'));(D/'xml').mkdir(exist_ok=True);(D/'text').mkdir(exist_ok=True)
def get(url):
 p=subprocess.run(['curl','-sS','-L','--max-time','45',url],capture_output=True);return p.stdout
urls={}
for p in D.glob('representations_*.json'):
 for x in json.load(open(p))['results']['bindings']:
  if x['url']['value'].endswith('.xml'): urls[x['pub']['value']]=x['url']['value']
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
 for x in ex.map(run,[(i,rs[i]) for i in [102,103,104,190,191,192,214,215]]):
  outs.append(x);print(x['index'],x['normalized_id'],x['status'],flush=True);json.dump(outs,open(D/'priority-acquisition.json','w'),indent=2)
