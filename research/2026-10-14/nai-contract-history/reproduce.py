#!/usr/bin/env python3
"""Retrieve a later public NAI snapshot. Python 3.11+; no API key or packages.
This writes only to --output. It never commits, publishes, emails or bypasses TLS.
"""
import argparse,os,pathlib,sys,runpy,json,time,zipfile,urllib.request,urllib.parse,http.cookiejar,html.parser,hashlib,datetime,shutil,subprocess
p=argparse.ArgumentParser();p.add_argument('--output',type=pathlib.Path,required=True);p.add_argument('--skip-documents',action='store_true');a=p.parse_args()
root=a.output.resolve();root.mkdir(parents=True,exist_ok=True);(root/'raw').mkdir(exist_ok=True);(root/'exports').mkdir(exist_ok=True);(root/'documents').mkdir(exist_ok=True)
os.environ['NAI_AUDIT_DIR']=str(root);code=pathlib.Path(__file__).resolve().parent/'code';sys.path.insert(0,str(code))
def script(name):runpy.run_path(str(code/name),run_name='__main__')
script('collect.py');script('expand.py')
from collect import fetch
jobs=[('download-recipient','/api/v2/download/search/',{'filters':{'recipient_search_text':['SLVJF3DR8MN5'],'award_type_codes':['A','B','C','D','IDV_A','IDV_B','IDV_B_A','IDV_B_B','IDV_B_C','IDV_C','IDV_D','IDV_E']},'spending_level':['awards','transactions'],'file_format':'csv'}),('download-vehicle','/api/v2/download/idv/',{'award_id':'CONT_IDV_SPE60523D9402_9700'}),('download-example','/api/v2/download/contract/',{'award_id':'CONT_AWD_SPE60524FWF6Y_9700_SPE60523D9402_9700'})]
for label,endpoint,body in jobs:
 job=fetch(label,endpoint,body)
 for attempt in range(60):
  status=fetch(label+'-status',job['status_url'])
  if status.get('status')=='finished':break
  if status.get('status')=='failed':raise RuntimeError(status)
  time.sleep(1)
 else:raise RuntimeError('Export not ready; retry its saved status URL later.')
 fetch(label+'-zip',job['file_url'])
 with zipfile.ZipFile(root/'raw'/f'{label}-zip.body') as z:
  # Official exports are flat CSV/readme/dictionary members; reject traversal.
  if any(pathlib.PurePosixPath(n).is_absolute() or '..' in pathlib.PurePosixPath(n).parts for n in z.namelist()):raise ValueError('Unsafe ZIP member')
  z.extractall(root/'exports'/label)
script('coverage.py');script('funding-all.py');script('analyze.py')
if not a.skip_documents:
 class Form(html.parser.HTMLParser):
  def __init__(self):super().__init__();self.action=None;self.fields={}
  def handle_starttag(self,t,attrs):
   d=dict(attrs)
   if t=='form':self.action=d.get('action')
   if t=='input' and d.get('name') and d.get('type') in ['hidden','submit']:self.fields[d['name']]=d.get('value','')
 client=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
 def document(name,url):
  with client.open(url,timeout=50) as r:b=r.read()
  if not b.startswith(b'%PDF'):
   f=Form();f.feed(b.decode(errors='replace'))
   if not f.action or 'butAgree' not in f.fields:raise RuntimeError('Document blocked or unavailable: '+url)
   target=urllib.parse.urljoin(url,f.action)
   if urllib.parse.urlparse(target).hostname!=urllib.parse.urlparse(url).hostname:raise RuntimeError('Unexpected consent destination')
   # Submit the ordinary displayed public notice-and-consent form.
   with client.open(urllib.request.Request(target,data=urllib.parse.urlencode(f.fields).encode()),timeout=50) as r:b=r.read()
  if not b.startswith(b'%PDF'):raise RuntimeError('No PDF returned: '+url)
  dest=root/'documents'/name;dest.write_bytes(b)
  (root/'documents'/(name+'.source.json')).write_text(json.dumps({'url':url,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)},indent=2))
 for suffix in ['', '_P00001','_P00002']:document('SPE60523D9402'+suffix+'.pdf','https://dibbs2.bsm.dla.mil/Downloads/Awards/22NOV22/SPE60523D9402'+suffix+'.PDF')
 for name,url in [('designation-federal-register.pdf','https://www.govinfo.gov/content/pkg/FR-2023-12-18/pdf/2023-27725.pdf'),('legal-2022.pdf','https://ofac.treasury.gov/media/930146/download'),('legal-2023-cfr.pdf','https://www.govinfo.gov/content/pkg/CFR-2023-title31-vol3/pdf/CFR-2023-title31-vol3-part583.pdf'),('legal-2024.pdf','https://ofac.treasury.gov/system/files/2024-03/20240311_global_magnitsky_sanctions_regulations.pdf')]:document(name,url)
 if shutil.which('pdfdetach'):
  for suffix in ['_P00001','_P00002']:subprocess.run(['pdfdetach','-saveall','-o',str(root/'documents'),str(root/'documents'/('SPE60523D9402'+suffix+'.pdf'))],check=True)
print('Saved later snapshot to',root)
