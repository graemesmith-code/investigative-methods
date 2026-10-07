"""All-years histories for verified returned client identities; original-led parents.

Global AI's AIDS-nonprofit search hit is explicitly excluded as a different entity.
BOE and Huawei parent searches follow names written in original Exhibit A pages 2.
"""
import json,time,urllib.parse,concurrent.futures
from reverse_cohort import P,S,fetch
def query(name,params):
    url='https://lda.gov/api/v1/filings/?'+urllib.parse.urlencode({'page_size':25,**params});rows=[];page=0;count=None
    while url and page<100:
        page+=1;t=time.monotonic();b=fetch(f'lda-followup-{name}-{page:03}.json',url)
        if b is None:break
        d=json.loads(b);rows+=d['results'];url=d['next'];count=d['count'];time.sleep(max(0,4.3-(time.monotonic()-t)))
    return rows,{'name':name,'params':params,'count':len(rows),'server_count':count,'complete':url is None}
def run():
    jobs=[('stark-61125',{'client_id':61125}),('stark-69451',{'client_id':69451}),('futurewei-203486',{'client_id':203486}),('qatar-61132',{'client_id':61132}),('boe-parent-2025',{'client_name':'BOE Technology','filing_year':2025}),('huawei-parent-2025',{'client_name':'Huawei Technologies','filing_year':2025})]
    out=[]
    for name,params in jobs:
        rows,summary=query(name,params)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:acquired=list(pool.map(lambda r:fetch('lda-original-'+r['filing_uuid']+'.html',r['filing_document_url']) is not None,rows))
        summary.update(originals_acquired=sum(acquired),client_ids=sorted({r['client']['id'] for r in rows}));out.append(summary)
        (P/'followup-coverage.json').write_text(json.dumps(out,indent=2));print(summary,flush=True)
if __name__=='__main__':run()
