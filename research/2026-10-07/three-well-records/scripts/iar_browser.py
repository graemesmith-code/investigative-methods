import pathlib,json,datetime
from playwright.sync_api import sync_playwright
P=pathlib.Path(__file__).resolve().parents[1];out=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 c=b.new_context(ignore_https_errors=False)
 page=c.new_page();page.on('dialog',lambda d:d.dismiss())
 for label,field,value in [('app33151710','Application_Number','33151710'),('lic0515889','BoardApprovalNumber','0515889'),('BAA97L','ApplicantBAID','A97L')]:
  rec={'label':label,'field':field,'value':value,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'ignore_https_errors':False}
  try:
   page.goto('https://dds.aer.ca/iar_query/FindApplications.aspx?SEARCH=NEW',wait_until='domcontentloaded',timeout=30000)
   page.locator('#'+field).fill(value,timeout=15000);page.locator('#btnSearch').click();page.wait_for_timeout(1200)
   (P/'sources'/f'iar-browser-{label}.html').write_text(page.content());rec['url']=page.url;rec['text']=page.locator('body').inner_text()[-8000:]
  except Exception as e:rec['error']=str(e);out.append(rec);break
  out.append(rec)
 b.close()
(P/'results/iar-browser-log.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
