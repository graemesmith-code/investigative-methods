from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True);page=b.new_page(ignore_https_errors=False);page.goto('https://www2.aer.ca/t/Production/views/PRD_1000_Hydraulic_Fracture_Fluid_Search_EXT/HydraulicFractureFluidSearch?:showVizHome=no&:embed=yes',wait_until='domcontentloaded',timeout=25000);page.wait_for_timeout(7000)

 filled=False
 for loc in page.locator('input,textarea,[contenteditable=true],[role=textbox]').all():
  if loc.is_visible():
   loc.fill('0466075');filled=True;loc.press('Enter');page.wait_for_timeout(5000);break
 try:
  page.get_by_text('PCC 103 KAYBOBS 4-8-63-21',exact=True).click(timeout=4000);page.wait_for_timeout(4000)
 except Exception as e:print('record selection:',str(e)[:160])
 print('links',page.locator('a').evaluate_all('(xs)=>xs.filter(x=>x.innerText.includes("PCC")||x.href.includes("Fract")).map(x=>({text:x.innerText,url:x.href}))'))
 d=dict(label='aer-well-record-selection-attempt',licence='0466075',form_entry_completed=filled,method='Searched visible editable controls; only entered licence if present',body_excerpt=page.locator('body').inner_text()[:12000],browser_certificate_validation='required; stop on certificate failure')
 print(json.dumps(d))
 with open('/workspace/investigative-methods/research/2026-10-04/consequential-expansion-08/evidence/browser-probes.jsonl','a') as f:f.write(json.dumps(d)+'\n')
 b.close()
