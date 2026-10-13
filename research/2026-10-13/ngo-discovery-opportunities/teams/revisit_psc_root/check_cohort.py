#!/usr/bin/env python3
"""Registry-nominated access controls; no allegation, credentials or model calls."""
import csv,datetime,hashlib,io,json,pathlib,re,subprocess,urllib.request,urllib.parse,zipfile
from html.parser import HTMLParser
P=pathlib.Path(__file__).parent;CACHE=pathlib.Path('/tmp/ngo-revisit-psc');CACHE.mkdir(exist_ok=True)
log=[]
def get(url,cap=80000000):
 x={'url':url,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'verified HTTPS GET, no retries'}
 try:
  with urllib.request.urlopen(url,timeout=45) as r:b=r.read(cap+1);x.update(status=r.status,content_type=r.headers.get('Content-Type'),bytes=len(b))
  if len(b)>cap:raise ValueError('bounded download cap exceeded')
  x['sha256']=hashlib.sha256(b).hexdigest();log.append(x);return b
 except Exception as e:x['error']=str(e);log.append(x);return None
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  if tag=='a':
   d=dict(attrs)
   if d.get('href'):self.links.append(d['href'])
def main():
 landing='https://download.companieshouse.gov.uk/en_output.html';b=get(landing,2000000)
 if not b:return
 h=Links();h.feed(b.decode());urls=[urllib.parse.urljoin(landing,u) for u in h.links if re.search(r'BasicCompanyData-.*part7_7\.zip',u)]
 if not urls:return
 url=urls[-1];b=get(url)
 if not b:return
 (CACHE/'cohort.zip').write_bytes(b);z=zipfile.ZipFile(io.BytesIO(b));member=[n for n in z.namelist() if n.lower().endswith('.csv')][0]
 selected=[];fields=[];seen=0;eligible=0
 with z.open(member) as f:
  reader=csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig'));fields=reader.fieldnames
  for original in reader:
   seen+=1;r={k.strip():v.strip() for k,v in original.items()};num=r.get('CompanyNumber','');dt=r.get('IncorporationDate','');category=r.get('CompanyCategory','')
   try:d=datetime.datetime.strptime(dt,'%d/%m/%Y').date()
   except ValueError:continue
   if re.fullmatch(r'\d{8}',num) and category=='Private Limited Company' and datetime.date(2024,1,1)<=d<=datetime.date(2024,12,31) and r.get('CompanyStatus')=='Active':
    eligible+=1;selected.append({'company_number':num,'incorporation_date':d.isoformat(),'company_category':category,'sample_score':hashlib.sha256(('ngo-rights-pilot-2026-10-13|'+num).encode()).hexdigest()})
 selected=sorted(selected,key=lambda r:r['sample_score'])[:3]
 controls=[]
 for r in selected:
  num=r['company_number'];base='https://find-and-update.company-information.service.gov.uk/company/'+num
  body=get(base+'/filing-history',2000000);control=dict(r,filing_history_access=body is not None,documents=[])
  if body:
   html=body.decode(errors='replace');(CACHE/(num+'.html')).write_text(html);links=Links();links.feed(html)
   docs=[]
   for u in links.links:
    if '/document?' in u:
     # Preserve filing-page table-row context for category/date, not guessed doc types.
     m=re.search(r'<tr\b[^>]*>.*?'+re.escape(u.replace('&','&amp;'))+r'.*?</tr>',html,re.S)
     idx=html.find(u);window=html[max(0,idx-1600):idx+400] if idx>=0 else ''
     category=next((x for x in ['NEWINC','CS01','SH01','SH02','SH08','PSC01','PSC02','PSC07','PSC08','PSC09'] if re.search(r'\b'+x+r'\b',window)),None)
     docs.append((u,category))
   # Select first3documents plus any NEWINC/CS01 among first12; page classification reviewed separately.
   chosen=docs[:3]
   for u,typ in docs[:12]:
    if typ in ['NEWINC','CS01'] and (u,typ) not in chosen:chosen.append((u,typ))
   for u,typ in chosen[:5]:
    link=urllib.parse.urljoin(base,u);pdf=get(link,15000000);dr={'url':link,'inferred_category_needs_table_review':typ,'success':bool(pdf and pdf.startswith(b'%PDF'))}
    if dr['success']:
     sha=hashlib.sha256(pdf).hexdigest();fp=CACHE/(sha+'.pdf');fp.write_bytes(pdf);tp=fp.with_suffix('.txt');subprocess.run(['pdftotext','-layout',str(fp),str(tp)],check=True);text=tp.read_text(errors='replace');dr.update(sha256=sha,bytes=len(pdf),pages=text.count('\f'),text_chars=len(text),text_sha256=hashlib.sha256(tp.read_bytes()).hexdigest(),contains_capital_or_rights=bool(re.search(r'statement of capital|prescribed particulars|shareholder|rights attached',text,re.I)))
    control['documents'].append(dr)
  psc=get(base+'/persons-with-significant-control',2000000)
  control['psc_page_access']=psc is not None
  controls.append(control)
 (P/'cohort-check.json').write_text(json.dumps({'selection':'One downloaded basic-company snapshot part7of7; active Private Limited Company numericIDs incorporated2024; deterministic SHA256 seed sorts eligible records; first3 access controls. Partial alphabetic partition, not national randomsample. No suspect selection.','snapshot_url':url,'zip_member':member,'rows_parsed':seen,'eligible_rows_in_partition':eligible,'csv_fields':fields,'controls':controls,'paid_calls':0,'contradiction_test_executed':False,'limitations':'Page labels inferred pending exact table review; current PSC is not historical state; no person details reproduced.'},indent=2)+'\n')
 (P/'request-manifest.json').write_text(json.dumps(log,indent=2)+'\n')
 print(json.dumps({'rows_parsed':seen,'eligible':eligible,'controls':len(controls),'http_successes':sum(r.get('status')==200 for r in log),'errors':[r.get('error') for r in log if r.get('error')]},indent=2))
if __name__=='__main__':main()
