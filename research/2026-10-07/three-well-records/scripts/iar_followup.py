from html.parser import HTMLParser
import urllib.request,urllib.parse,http.cookiejar,pathlib,datetime,json,hashlib,re
P=pathlib.Path(__file__).resolve().parents[1];URL='https://dds.aer.ca/iar_query/FindApplications.aspx'
class Form(HTMLParser):
 def __init__(self):super().__init__();self.inputs={};self.select=None
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='input' and a.get('name') and a.get('type') not in ['button','submit']:self.inputs[a['name']]=a.get('value','')
  if t=='select':self.select=a.get('name');self.inputs[self.select]=''
  if t=='option' and self.select and 'selected' in a:self.inputs[self.select]=a.get('value','')
 def handle_endtag(self,t):
  if t=='select':self.select=None
queries=[('original-app-33151710',{'Application_Number':'33151710'}),('original-app-33174496',{'Application_Number':'33174496'}),('BA-A97L-pad',{'ApplicantBAID':'A97L','LSD':'5','Section':'31','Township':'37','Range':'28','Meridian':'4','SELSD':'5','SESection':'31','SETownship':'37','SERange':'28','SEMeridian':'4'}),('BA-A97L-Feb-Mar2025',{'ApplicantBAID':'A97L','txtSqlValueDatePicker_RegistrationFromDate':'2025-02-01','txtSqlValueDatePicker_RegistrationToDate':'2025-03-31'})]
for name,filters in queries:
 rec={'name':name,'filters':filters,'url':URL,'method':'POST public read-only search','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tls_verified':True}
 try:
  op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()));op.addheaders=[('User-Agent','Public-record-research/1.0')]
  with op.open(URL,timeout=60) as r:b=r.read()
  f=Form();f.feed(b.decode());data={**f.inputs,**filters,'btnSearch':'Search'}
  (P/'sources'/f'iar-{name}.request.json').write_text(json.dumps({'method':'POST','url':URL,'fields':data},indent=2))
  with op.open(urllib.request.Request(URL,data=urllib.parse.urlencode(data).encode()),timeout=60) as r:b=r.read(10_000_000);rec['status']=r.status;rec['final_url']=r.url
  (P/'sources'/f'iar-{name}-initial.html').write_bytes(b)
  if b'action="ListApplications.aspx"' in b:
   with op.open('https://dds.aer.ca/iar_query/ListApplications.aspx',timeout=60) as r:b=r.read(10_000_000);rec['final_url']=r.url
  (P/'sources'/f'iar-{name}.html').write_bytes(b);rec['sha256']=hashlib.sha256(b).hexdigest();rec['visible_tail']=' '.join(re.sub('<[^>]+>',' ',b.decode(errors='replace')).split())[-3500:]
 except Exception as e:rec['error']=str(e)
 with (P/'results/iar-followup-log.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
 print(json.dumps(rec),flush=True)
