import pathlib,json,concurrent.futures,subprocess
from html.parser import HTMLParser
from acquire import P,S,fetch
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,d):
  if d.strip():self.parts.append(d.strip())
def one(r):
 uid=r['filing_uuid'];p=S/f'original-{uid}.html';b=fetch(p.name,r['filing_document_url'])
 if not b:return uid,'unavailable'
 t=p.with_suffix('.txt')
 if b.startswith(b'%PDF'):subprocess.run(['pdftotext','-layout',str(p),str(t)],check=True)
 else:
  h=Text();h.feed(b.decode());t.write_text('\n'.join(h.parts))
 return uid,'readable'
rows={r['filing_uuid']:r for name in ['Stark','ELTA_North_America','IAI_North_America','Israel_Aerospace'] for f in S.glob('lda-'+name+'-history-[0-9]*.json') for r in json.loads(f.read_text())['results']}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:out=list(ex.map(one,rows.values()))
(P/'history-original-access.json').write_text(json.dumps(out,indent=2));print('unique',len(rows),'readable',sum(x[1]=='readable' for x in out))
