"""One ordinary UI-equivalent public keyword search; no account or download bypass."""
import urllib.request, urllib.parse, http.cookiejar, re, json, time
from pathlib import Path
root=Path(__file__).resolve().parents[1]
host='https://telechargerdemandesaicompletees-downloadcompletedatirequests.bac-lac.gc.ca'
op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
s=op.open(host+'/eng/search',timeout=30).read().decode()
token=re.search(r"'RequestVerificationToken':\s*'([^']+)'",s)[1]
payload=dict(keyword='Afghanistan',sorting='2',language='eng',AdvanceSearch=[],RequestNumber='',SpecificTerm=[],ItemIdNumber='',FileName='',RecorddateFrom='',PastDays='0',IsAdvancedSearch=False,totalHits=0,pageSize='20',startFrom=1,items=[])
(root/'results/lac-query.json').write_text(json.dumps(payload,indent=2))
r={'url':host+'/search/SearchPost','method':'POST public read-only search','time_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'max_results':20}
time.sleep(1.2)
try:
 req=urllib.request.Request(host+'/search/SearchPost',data=urllib.parse.urlencode({'value':json.dumps(payload)}).encode(),headers={'RequestVerificationToken':token,'Content-Type':'application/x-www-form-urlencoded'})
 with op.open(req,timeout=35) as response:
  body=response.read(2000000);r.update(status=response.status,bytes=len(body));(root/'results/lac-search-result.json').write_bytes(body)
except Exception as e:r['error']=str(e)
(root/'results/lac-access.json').write_text(json.dumps(r,indent=2));print(r)
