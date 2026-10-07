import pathlib,json
from acquire import fetch
P=pathlib.Path(__file__).resolve().parents[1];done=set();index=[]
for n in ['0515889','0516327','0516328']:
 data=json.loads((P/'sources'/f'pubdocs-licence-{n}.json').read_text())
 for e in data['data']['events']['Events']:
  groups=[(None,e['Attachments'])]+[(a['ActivityID'],a['Attachments']) for a in e['Activities']]
  for aid,ats in groups:
   for a in ats:
    if a['IsConfidential']!='N':continue
    url='https://www1.aer.ca/wsPubDocs/'+e['EventID']+('/'+aid if aid else '')+'/'+str(a['ID'])
    if url in done:continue
    done.add(url);name='public-documents/'+e['EventID']+('-'+aid if aid else '')+'-'+str(a['ID'])+'-'+a['FileName'].replace('/','_')
    (P/'sources/public-documents').mkdir(exist_ok=True)
    fetch(name,url);index.append({'event':e['EventID'],'activity':aid,'attachment':a,'file':'sources/'+name,'url':url})
(P/'results/public-document-index.json').write_text(json.dumps(index,indent=2)+'\n')
