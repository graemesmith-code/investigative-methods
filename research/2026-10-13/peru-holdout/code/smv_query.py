import sys,json,time,hashlib,datetime,urllib.request,urllib.parse
from pathlib import Path
from lxml import html
sys.path.insert(0,'research/2026-10-13/peru-holdout/code');from acquire import ROOT,CACHE,fetch
r=html.fromstring((CACHE/'smv-memorias-index.html').read_bytes())
data={e.get('name'):e.get('value','') for e in r.xpath('//input[@type="hidden"]') if e.get('name')}
data.update({'ctl00$MainContent$cboDenominacionSocial':'59','ctl00$MainContent$cboAnioInicio':'2025','ctl00$MainContent$cboAnioFin':'2025','ctl00$MainContent$TextBox1':'NEXA RESOURCES PERU S.A.A.','ctl00$MainContent$cbBuscar':'Buscar'})
url='https://www.smv.gob.pe/SIMV/Frm_Memorias?data=A70181B60967D74090DCD93C4920AA1D769614EC12'; start=time.perf_counter()
row={'id':'smv-2025-search.html','method':'POST','url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'query':{'company_id':'59','year':2025},'request_note':'Ordinary public search form hidden state replayed; no authentication'}
try:
 req=urllib.request.Request(url,urllib.parse.urlencode(data).encode(),headers={'User-Agent':'investigative-methods research https://github.com/graemesmith-code/investigative-methods','Content-Type':'application/x-www-form-urlencoded'})
 with urllib.request.urlopen(req,timeout=35) as res:b=res.read();row['status']=res.status
 (CACHE/row['id']).write_bytes(b);row.update(sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
 tree=html.fromstring(b)
 print(' '.join(tree.text_content().split())[-4500:]);print(tree.xpath('//a[contains(@href,"vidDoc")]/@href'))
except Exception as e:row['error']=type(e).__name__
finally:
 row['elapsed_seconds']=time.perf_counter()-start
 with (ROOT/'provenance/acquisition.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
