"""Use the published public IAR search form; no login or access changes."""
from html.parser import HTMLParser
import urllib.request,urllib.parse,http.cookiejar,json,hashlib,datetime,pathlib,re
P=pathlib.Path(__file__).resolve().parents[1];URL='https://dds.aer.ca/iar_query/FindApplications.aspx'
class Form(HTMLParser):
 def __init__(self):super().__init__();self.inputs={};self.select=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='input' and a.get('name') and a.get('type') not in ['button','submit']:self.inputs[a['name']]=a.get('value','')
  if tag=='select':self.select=a.get('name');self.inputs[self.select]=''
  if tag=='option' and self.select and 'selected' in a:self.inputs[self.select]=a.get('value','')
 def handle_endtag(self,tag):
  if tag=='select':self.select=None
for licence in ['0515889','0516327','0516328']:
 record={'licence_query':licence,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tls_verification':True}
 try:
  op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()));op.addheaders=[('User-Agent','Public-record-research/1.0')]
  with op.open(URL,timeout=60) as r:s=r.read(2_000_000).decode()
  f=Form();f.feed(s);fields=f.inputs;fields['BoardApprovalNumber']=licence;fields['btnSearch']='Search'
  with op.open(urllib.request.Request(URL,data=urllib.parse.urlencode(fields).encode(),method='POST'),timeout=60) as r:data=r.read(5_000_000);record.update(status=r.status,final_url=r.url)
  path=P/'sources'/f'iar-search-{licence}.html';path.write_bytes(data);record.update(file=path.name,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
  visible=re.sub(r'<[^>]+>',' ',data.decode(errors='replace'));record['text_tail']=' '.join(visible.split())[-2500:]
 except Exception as e:record.update(error_type=type(e).__name__,error=str(e))
 with (P/'results/iar-search-log.jsonl').open('a') as out:out.write(json.dumps(record)+'\n')
 print(json.dumps(record),flush=True)
 if 'error' in record:break
