import json,pathlib,datetime
from playwright.sync_api import sync_playwright
P=pathlib.Path(__file__).resolve().parents[1]
urls=[('aer-one-well','https://www2.aer.ca/t/Production/views/PRD_1000_Hydraulic_Fracture_Fluid_Search_EXT/HydraulicFractureFluidSearch?:showVizHome=no&:embed=yes&Well%20Licence%20Number=0466075'),('ct-one-history','https://clinicaltrials.gov/study/NCT00000415?a=1&tab=history')]
with sync_playwright() as p:
 try:b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True)
 except Exception as e:
  (P/'evidence/browser-probes.jsonl').write_text(json.dumps(dict(stage='browser_launch',error=str(e),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))+'\n');print(str(e));raise SystemExit(0)
 for label,url in urls:
  d=dict(label=label,url=url,utc=datetime.datetime.now(datetime.timezone.utc).isoformat());page=b.new_page(ignore_https_errors=False);d["browser_certificate_validation"]= "required; stop on certificate failure"
  try:
   page.goto(url,wait_until='domcontentloaded',timeout=25000);page.wait_for_timeout(8000)
   d.update(final_url=page.url,title=page.title(),body_excerpt=page.locator('body').inner_text()[:16000])
  except Exception as e:d['error']=str(e)
  with (P/'evidence/browser-probes.jsonl').open('a') as f:f.write(json.dumps(d)+'\n')
  print(json.dumps(d));page.close()
 b.close()
