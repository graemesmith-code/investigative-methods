import asyncio,json,pathlib,datetime
from playwright.async_api import async_playwright
R=pathlib.Path(__file__).resolve().parents[1]/'sources'
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(headless=True,executable_path="/usr/bin/chromium")
  context=await b.new_context(ignore_https_errors=False)
  page=await context.new_page()
  try:
   await page.goto('https://www2.aer.ca/t/Production/views/PRD_1000_Hydraulic_Fracture_Fluid_Search_EXT/HydraulicFractureFluidSearch?:showVizHome=no&:embed=yes',wait_until='domcontentloaded',timeout=60000)
   await page.wait_for_timeout(10000)
   text=await page.locator('body').inner_text();(R/'tableau-browser.txt').write_text(text)
   await page.screenshot(path=str(R/'tableau-browser.png'),full_page=True)
   print(text[:6000])
  except Exception as e:
   (R/'tableau-browser-error.json').write_text(json.dumps({'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'error':str(e),'tls_verification':True}));print(type(e).__name__,str(e)[:700])
  await b.close()
asyncio.run(main())
