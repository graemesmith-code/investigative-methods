import urllib.request,urllib.error,hashlib,json,datetime,pathlib
base=pathlib.Path(__file__).parent; raw=base/'raw';raw.mkdir(exist_ok=True)
urls={
'US11946710B1':'https://patents.google.com/patent/US11946710B1/en',
'US20230229794A1':'https://patents.google.com/patent/US20230229794A1/en',
'S06_Boxer11897':'https://questions-statements.parliament.uk/written-questions/detail/2026-06-22/11897',
'S07_MCT_Bjorset':'https://www.kongsberg.com/news/stories/2018/9/technology-award-mct/',
'S08_ND_interview':'https://www.nationaldefensemagazine.org/articles/2024/6/18/kongsbergs-counter-drone-secret-sauce-refined-in-ukraine',
'IFU_2023':'https://www.kongsberg.com/news/news-archive/2023/international-fund-for-ukraine-orders-multiple-c-uas-air-defence-systems-from-kongsberg/',
'SAN_2026':'https://www.kongsberg.com/news/news-archive/2026/kongsberg-wins-nok-16-billion-contract-to-deliver-counter-uas-solutions-in-poland/',
'CAVS_2026':'https://www.kongsberg.com/news/news-archive/2026/germany-and-sweden-order-kongsberg-remote-weapon-stations-for-cavs-6x6-programme/',
'Netherlands_2026':'https://www.kongsberg.com/news/news-archive/2026/kongsberg-signs-contract-with-oshkosh-defense-europe-to-deliver-counter-drone-capabilities-to-the-netherlands/',
'Boxer_2020':'https://www.kongsberg.com/news/news-archive/20202/kongsberg-wins-remote-weapon-stations-contract-of-1-030-mnok-with-the-the-british-miv-program/'
}
manifest=[]
for id,u in urls.items():
 r={'id':id,'url':u,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(u,timeout=30) as f:
   b=f.read();r.update(status=f.status,final_url=f.url,mime=f.headers.get('Content-Type'))
  if any(x in b[:20000].lower() for x in [b'just a moment...',b'verify you are human',b'access denied']): r['error']='possible security wrapper; not saved'
  else:
   p=raw/(id+'.html');p.write_bytes(b);r.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),path=str(p.resolve()))
 except urllib.error.HTTPError as e:r.update(status=e.code,error=str(e))
 except Exception as e:r['error']=str(e)
 manifest.append(r);(base/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(r),flush=True)
