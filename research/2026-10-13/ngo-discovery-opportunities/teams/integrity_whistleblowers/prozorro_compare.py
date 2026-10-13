#!/usr/bin/env python3
"""Fetch original criteria, bid eligibility and award documents for one data-nominated tender."""
import pathlib,json,urllib.request,hashlib,subprocess
P=pathlib.Path(__file__).parent;C=pathlib.Path('/tmp/ngo-integrity-cache');j=json.loads((P/'prozorro-pilot.json').read_text());tender=j['sample'][0];x=next(x for x in j['access_checks'] if x['url'].endswith(tender['id']));t=json.loads(urllib.request.urlopen('https://public.api.openprocurement.org/api/2.5/tenders/'+tender['id'],timeout=35).read())['data'];out=[]
for b in t.get('bids',[]):
 for d in b.get('eligibilityDocuments',[])+b.get('qualificationDocuments',[]):
  if any(q in d.get('title','').lower() for q in ['працівник','сертифікат']):out.append(dict(side='bid_eligibility',bid_id=b['id'],document=d))
for a in t.get('awards',[]):
 for d in a.get('documents',[]):
  if d.get('format')=='application/pdf':out.append(dict(side='award_decision',award_id=a['id'],bid_id=a.get('bid_id'),document=d))
for x in out:
 d=x['document'];u=d['url']
 try:
  b=urllib.request.urlopen(u,timeout=35).read();h=hashlib.sha256(b).hexdigest();(C/(h+'.pdf')).write_bytes(b);x.update(status='acquired',bytes=len(b),sha256=h)
  proc=subprocess.run(['pdftotext','-layout',str(C/(h+'.pdf')),str(C/(h+'.txt'))],capture_output=True);x['text_chars']=len((C/(h+'.txt')).read_text(errors='replace')) if proc.returncode==0 else 0
 except Exception as e:x.update(status='failed',error=str(e))
(P/'prozorro-comparison.json').write_text(json.dumps(dict(tender_id=t['id'],tenderID=t['tenderID'],bidder_identifier=t['bids'][0]['tenderers'][0]['identifier'],award_status=t['awards'][0]['status'],qualification_document_id='f03a844a3daa45d1ae090cf8fb584d76',qualification_sha256='41267eba14cc05e6672f589def65d38c9188fd58a325d7d49db39cf309fcafc2',checks=out),ensure_ascii=False,indent=2));print([(x['side'],x['document']['title'],x['status'],x.get('text_chars')) for x in out])

import subprocess
subprocess.run(["python", str(P/"scrub_urls.py")], check=True)
