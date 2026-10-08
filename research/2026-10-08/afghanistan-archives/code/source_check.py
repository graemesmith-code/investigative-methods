"""Fetch explicit public reference pages once; no recursion or retries."""
import urllib.request,hashlib,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
URLS={
'lac-2026':'https://www.canada.ca/en/library-archives/corporate/transparency/reports-publications/atip/action-plan/june-2026-update.html',
'oic-2026-53':'https://www.oic-ci.gc.ca/en/decisions/final-reports/global-affairs-canada-re-2026-oic-53',
'cjoc-catalogue':'https://recherche-collection-search.bac-lac.gc.ca/eng/home/record?IdNumber=5877607&app=fonandcol',
'mpcc-2012':'https://www.mpcc-cppm.gc.ca/public-interest-investigations-and-hearings-enquetes-et-audiences-dinteret-public/afghanistan-hearing-audience/pih-aip-afghan-2008-042-fnl-rpt-eng.html',
'lac-terms':'https://www.canada.ca/en/library-archives/terms-conditions.html',
'publications-terms':'https://publications.gc.ca/site/eng/corporate/termsConditions.html',
'lac-package-details':'https://telechargerdemandesaicompletees-downloadcompletedatirequests.bac-lac.gc.ca/eng/search/details/A-2023-07487',
}
log=[]
for name,url in URLS.items():
 p=R/'sources'/(name+'.html');row=dict(id=name,url=url,retrieved_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
 if p.exists():continue
 time.sleep(1.2)
 try:
  with urllib.request.urlopen(url,timeout=30) as r:
   b=r.read(4*1024**2+1);row.update(status=r.status,final_url=r.url,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  if len(b)>4*1024**2:raise ValueError('4MiB limit')
  p.write_bytes(b)
 except Exception as e:row['error']=str(e)
 log.append(row);(R/'results/source-access.json').write_text(json.dumps(log,indent=2));print(name,row.get('status',row.get('error')))
