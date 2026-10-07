"""Standard public client, default TLS verification; stop on any TLS/access failure."""
import pathlib,json,datetime,hashlib
from tableauscraper import TableauScraper,api
original_set_session=api.setSession
P=pathlib.Path(__file__).resolve().parents[1];log=[]
for name,path in [('licence','COM-WellLicenceMainDashboard/LicenceDetailDashboard'),('general','PRD_0100_General_Well_Identifier_Search/WellIdentifierSearch')]:
 t=TableauScraper();counter=[0]
 def capture(resp,*args,**kw):
  counter[0]+=1;n=f'tableau-{name}-http-{counter[0]}.bin';(P/'sources'/n).write_bytes(resp.content);req=resp.request
  row={'file':n,'method':req.method,'url':req.url,'request_body':str(req.body) if req.body else None,'status':resp.status_code,'sha256':hashlib.sha256(resp.content).hexdigest(),'bytes':len(resp.content),'tls_verification':True,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};log.append(row)
 def logged_session(scraper):
  original_set_session(scraper);scraper.session.hooks['response']=[capture]
 api.setSession=logged_session
 try:
  t.loads('https://www2.aer.ca/t/Production/views/'+path+'?:embed=y&:showVizHome=no');w=t.getWorkbook();result={'parameters':w.getParameters(),'sheets':w.getSheets(),'worksheets':[{'name':s.name,'records':s.data.to_dict(orient='records')} for s in w.worksheets]};(P/'results'/f'tableau-{name}-initial.json').write_text(json.dumps(result,indent=2,default=str));print(name,json.dumps(result,default=str)[:5000])
 except Exception as e:
  log.append({'name':name,'error_type':type(e).__name__,'error':str(e),'tls_verification':True});print(name,type(e).__name__,str(e)[:500]);break
(P/'results/tableau-probe-log.json').write_text(json.dumps(log,indent=2)+'\n')
