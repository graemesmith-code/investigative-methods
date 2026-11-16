exec(open('spine_recovery/kongsberg/download.py').read().split('manifest=[]')[0])
urls={
'US11946710B1_PDF':'https://patentimages.storage.googleapis.com/f9/82/9c/b9ee5253f6e9b9/US11946710.pdf',
'US20230229794A1_PDF':'https://patentimages.storage.googleapis.com/cb/71/81/55f945a58a1fc3/US20230229794A1.pdf',
'SAN_Euronext':'https://live.euronext.com/en/products/equities/company-news/2026-01-30-kongsberg-wins-nok-16-billion-contract-deliver-counter',
'CAVS_Euronext':'https://live.euronext.com/en/products/equities/company-news/2026-02-06-germany-and-sweden-order-kongsberg-remote-weapon-stations',
'CAVS_Patria':'https://www.patriagroup.com/newsroom/news/2026/patria-and-kongsberg-agree-on-weapon-station-deliveries-to-sweden-and-germany-within-cavs-vehicle-programme',
'NDIA_interview_reprint':'https://www.ndia.org/-/media/sites/ndia/e-books/ffc/2024/ffc-2024-ebook-v1.pdf'}
manifest=[]
for id,u in urls.items():
 r={'id':id,'url':u,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(u,timeout=25) as f:b=f.read();r.update(status=f.status,final_url=f.url,mime=f.headers.get('Content-Type'))
  if any(x in b[:20000].lower() for x in [b'just a moment...',b'verify you are human',b'_incapsula_resource',b'access denied']):r['error']='security wrapper; not saved'
  else:
   p=raw/(id+('.pdf' if b.startswith(b'%PDF') else '.html'));p.write_bytes(b);r.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),path=str(p.resolve()))
 except urllib.error.HTTPError as e:r.update(status=e.code,error=str(e))
 except Exception as e:r['error']=str(e)
 manifest.append(r);(base/'extras_manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(r),flush=True)
