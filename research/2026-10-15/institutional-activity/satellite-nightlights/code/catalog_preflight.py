#!/usr/bin/env python3
"""Public metadata audit only: no credentials, radiance downloads or signal claims."""
import concurrent.futures, datetime as dt, json, pathlib, urllib.request, urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'evidence'; OUT.mkdir(exist_ok=True)
CMR='https://cmr.earthdata.nasa.gov/search/'

def fetch_json(url, name):
    with urllib.request.urlopen(url, timeout=50) as r:
        body=r.read(); status=r.status; hits=r.headers.get('CMR-Hits')
    data=json.loads(body)
    (OUT/(name+'.json')).write_text(json.dumps(data,indent=2))
    return data, {'url':url,'retrieved_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'http_status':status,'cmr_hits':hits}

def query(product, label, start, end):
    params={'short_name':product,'bounding_box':'-77.1,38.8,-77,38.9','temporal':start+'T00:00:00Z,'+end+'T00:00:00Z','page_size':'100','sort_key':'start_date'}
    if not product.endswith('_NRT'):params['version']='2'
    url=CMR+'granules.json?'+urllib.parse.urlencode(params)
    try:
        data,meta=fetch_json(url,product+'_'+label)
        entries=data['feed']['entry']
        meta.update(product=product,window=label,entry_count=len(entries),items=[{k:e.get(k) for k in ['id','producer_granule_id','title','time_start','time_end','updated','granule_size','boxes','links']} for e in entries])
        return meta
    except Exception as e:return {'product':product,'window':label,'url':url,'error':type(e).__name__+': '+str(e)}

def main():
    windows=[('iran_june_2025','2025-06-18','2025-06-21'),('venezuela_jan_2026','2025-12-30','2026-01-02'),('iran_feb_2026','2026-02-25','2026-02-28'),('recent','2026-10-12','2026-10-15')]
    jobs=[(p,*w) for p in ['VNP46A1','VNP46A2','VNP46A1_NRT','VNP46A2_NRT'] for w in windows]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(lambda x:query(*x),jobs))
    (OUT/'catalog_preflight.json').write_text(json.dumps(results,indent=2))
    for r in results:print(r['product'],r['window'],r.get('cmr_hits'),r.get('entry_count'),r.get('error',''))
if __name__=='__main__':main()
