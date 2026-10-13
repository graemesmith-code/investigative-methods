#!/usr/bin/env python3
"""Public bounded download check; no bulk report committed, no external AI transmission."""
import urllib.request,pathlib,hashlib,json,subprocess,zipfile,io
P=pathlib.Path(__file__).parent;C=pathlib.Path('/tmp/ngo-revisit-integrity');C.mkdir(exist_ok=True)
checks=[]
for u,typ in [('https://cdnweb.ictsi.com/Final%20Draft%20-%20BIPI%20ESIA%20v3.pdf','esia_control'),('https://download.geonames.org/export/dump/PH.zip','gazetteer_control'),('https://rsis.ramsar.org/RISapp/files/RISrep/CD788RIS.pdf','ramsar_supporting_only')]:
 try:
  r=urllib.request.urlopen(u,timeout=45);b=r.read();h=hashlib.sha256(b).hexdigest();(C/h).write_bytes(b);x=dict(url=u,status='acquired',bytes=len(b),sha256=h,type=typ)
  if typ=='esia_control':
   (C/(h+'.pdf')).write_bytes(b);subprocess.run(['pdftotext','-layout',str(C/(h+'.pdf')),str(C/(h+'.txt'))],check=True);t=(C/(h+'.txt')).read_text(errors='replace');x.update(pages=t.count('\f'),text_characters=len(t),notice='Publicly reachable report bears OFFICIAL USE ONLY watermark;no externalAI processing performed.')
  if typ=='gazetteer_control':
   z=zipfile.ZipFile(io.BytesIO(b));t=z.read('PH.txt').decode();x['records']=len(t.splitlines());matches=[]
   for ln in t.splitlines():
    fs=ln.split('\t')
    if fs[1] in ['Bauan','Batangas','Batangas Bay']:matches.append(dict(geonameid=fs[0],name=fs[1],latitude=fs[4],longitude=fs[5],feature_class=fs[6],feature_code=fs[7],country_code=fs[8],admin1=fs[10],modification_date=fs[18]))
   x['bounded_place_matches']=matches
  checks.append(x)
 except Exception as e:checks.append(dict(url=u,status='failed',error=str(e),type=typ))
(P/'environment-access.json').write_text(json.dumps(checks,indent=2));print('bounded_check',[(x['type'],x['status']) for x in checks])
