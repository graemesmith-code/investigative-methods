import json,time,pathlib,collections
from acquire import fetch,P,S
url='https://lda.gov/api/v1/filings/?filing_year=2025&filing_amount_reported_min=1000000&page_size=25';allrows=[];page=0
while url:
 page+=1;b=fetch(f'lda-major-{page:03}.json',url)
 if b is None:break
 x=json.loads(b);allrows+=x['results'];url=x['next']
 (P/'coverage.json').write_text(json.dumps({'server_count':x['count'],'acquired_rows':len(allrows),'unique_uuids':len({r['filing_uuid'] for r in allrows}),'pages':page,'next':url,'complete':url is None},indent=2))
 print(page,len(allrows),flush=True)
 if url:time.sleep(4.3)
(P/'major-cohort.json').write_text(json.dumps(allrows,indent=2))
print('Complete',url is None,'clients',len({r['client']['id'] for r in allrows}),flush=True)
