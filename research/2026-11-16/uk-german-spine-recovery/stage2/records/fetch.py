import urllib.request,urllib.error,json,hashlib,datetime,pathlib
p=pathlib.Path(__file__).parent
urls=[('T1_Bundestag_2105159.pdf','https://dserver.bundestag.de/btd/21/051/2105159.pdf'),('T1_BMVg_KI.pdf','https://www.bmvg.de/resource/blob/6143700/9954e2b6b993b17cd3d09ca31c506774/dl-ki-konzeption-data.pdf'),('T1_Ghostplay_mirror.pdf','https://files.auftrag-select.com/file/auftrag-select-public/pdfs/6656021/bekanntmachung.pdf'),('T1_EP4229352A1.xml','https://data.epo.org/linked-data/representation/publication/EP/4229352/NWA1.xml'),('T1_RENK.pdf','https://ir.renk.com/static-files/1223e64d-1b82-4b79-97a3-1fec64780557'),('T1_Wu2022.pdf','https://savage.nps.edu/EthicalControl/documentation/papers/SSS-22_paper_117_TieredApproachEthicalAIEvaluationMetrics.pdf'),('T1_ACTS.html','https://www.sell2wales.gov.wales/search/show/search_view.aspx?ID=AUG648236&catID=')]+[(f'T1_INPI_{n}.html',f'https://data.inpi.fr/brevets/{n}') for n in ['FR3102239','EP3812690','EP3882560','EP3882561']]
logs=[]
for name,url in urls:
 r={'name':name,'url':url,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(url,timeout=25) as x:
   b=x.read();r.update(status=x.status,mime=x.headers.get('Content-Type'),final_url=x.url,bytes=len(b))
  if not b or b'captcha' in b[:10000].lower() or b'incapsula' in b.lower() or (name.endswith('.pdf') and not b.startswith(b'%PDF')):
   r['result']='wrapper_or_non_document_not_saved'
  else:
   (p/'raw'/name).write_bytes(b);r.update(result='saved',sha256=hashlib.sha256(b).hexdigest(),path=str((p/'raw'/name).resolve()))
 except Exception as e:r.update(result='failed',error=str(e),status=getattr(e,'code',None))
 logs.append(r);(p/'fetch-log.json').write_text(json.dumps(logs,indent=2));print(r,flush=True)
