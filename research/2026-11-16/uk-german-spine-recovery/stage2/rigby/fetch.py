import urllib.request,hashlib,json,datetime,pathlib
base=pathlib.Path('stage2_rigby'); m=[]
urls={
'rigby_US9156552.pdf':'https://patentimages.storage.googleapis.com/e6/af/64/531ec203e9aa2e/US9156552.pdf',
'PYRAMID_Technical_Standard.pdf':'https://assets.publishing.service.gov.uk/media/67dbe7ec0f38d929e57ee310/20250224-PYRAMID_Technical_Standard_V1-O.pdf',
'PYRAMID_Guidance.pdf':'https://assets.publishing.service.gov.uk/media/67dbe7ea931ea30d1b7ee313/20250224-PYRAMID_Technical_Standard_Guidance_V1-O.pdf',
'GD_stores.html':'https://generaldynamics.uk.com/businesses/mission-systems/air/airborne-mission-management/stores-management/',
'PYRAMID_landing.html':'https://www.gov.uk/government/publications/pyramid'}
for name,url in urls.items():
 r={'name':name,'url':url,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(url,timeout=60) as f:
   b=f.read();r.update(status=f.status,mime=f.headers.get_content_type(),bytes=len(b))
  if len(b)<200 or b'captcha' in b[:500].lower(): raise Exception('suspect wrapper')
  (base/'raw'/name).write_bytes(b); r['sha256']=hashlib.sha256(b).hexdigest()
 except Exception as e:r['error']=str(e)
 m.append(r);(base/'manifest.json').write_text(json.dumps(m,indent=2))
print(json.dumps(m,indent=2))
