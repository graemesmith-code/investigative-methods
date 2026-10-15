#!/usr/bin/env python3
"""Filter CMR interval overlaps by observation date and derive production delays."""
import datetime as dt,json,pathlib,statistics
ROOT=pathlib.Path(__file__).resolve().parents[1]
WINDOWS={'iran_june_2025':('2025-06-18','2025-06-21'),'venezuela_jan_2026':('2025-12-30','2026-01-02'),'iran_feb_2026':('2026-02-25','2026-02-28')}
def main():
    results=json.loads((ROOT/'evidence/catalog_preflight.json').read_text())
    manifest=[];summary=[]
    for result in results:
        if result['window'] not in WINDOWS:continue
        if 'error' in result:raise ValueError(result['error'])
        start,end=WINDOWS[result['window']];rows=[]
        for e in result['items']:
            date=e['time_start'][:10]
            if not start<=date<end:continue
            name=e['producer_granule_id']
            if '.h10v05.002.' not in name:raise ValueError('Unexpected tile/version: '+name)
            production=dt.datetime.strptime(name.split('.')[-2],'%Y%j%H%M%S').replace(tzinfo=dt.timezone.utc)
            daystart=dt.datetime.fromisoformat(e['time_start'].replace('Z','+00:00'))
            row={'event':result['window'],'product':result['product'],'observation_date_utc':date,'filename':name,'granule_id':e['id'],'size_mib':float(e['granule_size']),'production_time_utc':production.isoformat(),'production_days_since_utc_day_start':(production-daystart).total_seconds()/86400,'catalog_updated_utc':e['updated'],'download_url':next(l['href'] for l in e['links'] if l.get('type')=='application/x-hdf5' and l['href'].startswith('https://')),'cmr_query_url':result['url']}
            rows.append(row)
            if not result['product'].endswith('_NRT'):manifest.append(row)
        if len({r['observation_date_utc'] for r in rows})!=len(rows):raise ValueError('Duplicate date; resolve versions before analysis.')
        summary.append({'event':result['window'],'product':result['product'],'query_url':result['url'],'retrieved_at_utc':result['retrieved_at_utc'],'raw_cmr_hits':int(result['cmr_hits']),'selected_date_count':len(rows),'expected_date_count':3,'dates':[x['observation_date_utc'] for x in rows]})
    (ROOT/'download_manifest.json').write_text(json.dumps(manifest,indent=2))
    (ROOT/'evidence/coverage_summary.json').write_text(json.dumps(summary,indent=2))
    recent=[{k:r.get(k) for k in ['product','window','url','retrieved_at_utc','cmr_hits','entry_count','error']} for r in results if r['window']=='recent']
    (ROOT/'evidence/recent_catalog_check.json').write_text(json.dumps(recent,indent=2))
    for product in ['VNP46A1','VNP46A2']:
        values=[r['production_days_since_utc_day_start'] for r in manifest if r['product']==product]
        print(product,'files',len(values),'production delay days:',min(values),statistics.median(values),max(values))
if __name__=='__main__':main()
