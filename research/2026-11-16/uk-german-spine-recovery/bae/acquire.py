import urllib.request,hashlib,json,datetime,pathlib
p=pathlib.Path(__file__).parent
urls={
'S23_MBDA_DragonFire':'https://www.mbda-systems.com/uk-defence-minister-visits-mbda-dragonfire-laser-weapon-contract-announcement',
'S24_Dstl_laser':'https://www.gov.uk/government/news/advanced-future-military-laser-achieves-uk-first',
'S25_FCAS_708m':'https://www.gov.uk/government/news/708-million-to-accelerate-uk-next-generation-air-combat-technology',
'S26_RAF_ACP_strategy':'https://assets.publishing.service.gov.uk/media/66019fa8f1d3a0666832acfc/RAF_Autonomous_Collaborative_Platform_Strategy.pdf',
'S27_Rigby_2022':'https://www.aerosociety.com/media/19656/weapons-for-generation-after-next-platform-17-november-2022-v3.pdf',
'S28_Rigby_2025':'https://www.aerosociety.com/media/26488/fcas25-speaker-library.pdf',
'BAE_US11473880B2':'https://patents.google.com/patent/US11473880B2/en',
'BAE_US11422549B2':'https://patents.google.com/patent/US11422549B2/en'}
manifest=[]
for k,u in urls.items():
 d={'id':k,'url':u,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(u,timeout=35) as r:
   b=r.read();d.update(status=r.status,mime=r.headers.get_content_type(),final_url=r.url)
  if b'captcha' in b[:10000].lower() or b'Just a moment' in b[:10000]:d['blocked']='possible security wrapper';raise ValueError('security wrapper')
  ext='.pdf' if d['mime']=='application/pdf' else '.html';f=p/(k+ext);f.write_bytes(b);d.update(path=str(f.resolve()),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 except Exception as e:d['error']=str(e)
 manifest.append(d);(p/'manifest.json').write_text(json.dumps(manifest,indent=2));print(k,d.get('status'),d.get('bytes'),d.get('error'),flush=True)
