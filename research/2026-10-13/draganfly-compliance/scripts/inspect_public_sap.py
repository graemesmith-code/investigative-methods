"""Read the expressly public anonymous SAP preview with an ordinary browser.

Trust only the CA public keys supplied by this execution environment. No login,
challenge solving, API guessing, cookie import or permission changes.
"""
import base64
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://portal.us.bn.cloud.ariba.com/dashboard/public/appext/comsapsbncdiscoveryui#/RfxEvent/preview/1110019561?anId=ANONYMOUS'

def environment_ca_spkis():
    hashes = []
    for cert in Path('/usr/local/share/ca-certificates').glob('*.crt'):
        pem = subprocess.run(['openssl','x509','-in',str(cert),'-pubkey','-noout'],capture_output=True,check=True).stdout
        der = subprocess.run(['openssl','pkey','-pubin','-outform','der'],input=pem,capture_output=True,check=True).stdout
        hashes.append(base64.b64encode(hashlib.sha256(der).digest()).decode())
    return hashes

def main():
    log = {'url': URL, 'retrieved_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'certificate_trust': 'Only provisioned environment CA public keys; no blanket TLS-ignore setting', 'responses': []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True,args=['--ignore-certificate-errors-spki-list='+','.join(environment_ca_spkis())])
        page = browser.new_page()
        # Record ordinary requests the public page makes, without replaying them.
        page.on('response', lambda r: log['responses'].append({'url':r.url,'status':r.status}))
        try:
            response = page.goto(URL,wait_until='domcontentloaded',timeout=30000)
            log['status'] = response.status if response else None
            if response and response.status == 200:
                try:
                    page.wait_for_function("document.body && document.body.innerText.trim().length > 100",timeout=15000)
                except Exception:
                    pass
            log['title'] = page.title()
            log['visible_text'] = page.locator('body').inner_text()
            log['links'] = page.locator('a').evaluate_all("els => els.map(e=>({text:e.innerText,href:e.href}))")
            print(log['status'],log['title'],log['visible_text'][:10000],flush=True)
            print('links',log['links'][:30],flush=True)
            if log['status'] == 200:
                (ROOT/'snapshots/sap-public-rendered.html').write_text(page.content())
        except Exception as exc:
            log['error'] = str(exc)
            print(str(exc),flush=True)
        browser.close()
    (ROOT/'snapshots/sap-public-inspection.json').write_text(json.dumps(log,indent=2)+'\n')

if __name__ == '__main__':
    main()
