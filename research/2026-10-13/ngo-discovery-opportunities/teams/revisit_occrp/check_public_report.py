"""One bounded public report request; retain failure and stop, no fallback routes.
The original run returned HTTP403 and acquired no report.
"""
import urllib.request,json,hashlib,pathlib
P=pathlib.Path(__file__).parent
URL='https://www.ferrexpo.com/media/wkphhjkc/ferrexpo-plc-ara-2018-for-website.pdf'
result={'url':URL,'purpose':'public annual-report access feasibility; no payment proof'}
try:
 with urllib.request.urlopen(URL,timeout=30) as r:
  b=r.read();result.update(status=r.status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
except Exception as e:result['status']=str(e)
P.joinpath('public-report-check.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
