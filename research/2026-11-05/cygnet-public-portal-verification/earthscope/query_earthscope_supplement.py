#!/usr/bin/env python3
import argparse,json,pathlib
from concurrent.futures import ThreadPoolExecutor
import query_earthscope as q
p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();q.ROOT=pathlib.Path(a.out)
jobs=[]
for n,s in [('I0','RD161'),('I0','RD162'),('I0','RD165'),('I0','RD166'),('RV','REDDA')]:
 jobs.append((f'mustang_{n}_{s}','https://service.earthscope.org/mustang/measurements/1/query',{'metric':'percent_availability','net':n,'sta':s,'cha':'HH?','start':'2025-02-01','end':'2025-04-01','format':'csv','nodata':404}))
for n in ['I0','2K']:
 jobs.append((f'station_alltime_{n}','https://service.earthscope.org/fdsnws/station/1/query',{'latitude':q.LAT,'longitude':q.LON,'maxradius':25/111.195,'net':n,'level':'channel','format':'xml','includerestricted':'true','nodata':404}))
 jobs.append((f'station_operational_{n}','https://service.earthscope.org/fdsnws/station/1/query',{**q.BASE,'starttime':'2025-02-15','endtime':'2025-03-13','net':n,'level':'channel','format':'xml','includerestricted':'true'}))
jobs += [('availability_service_notice','https://www.earthscope.org/news/fdsnws-availability-web-service-outage-and-changes/',{}),('mustang_documentation','https://service.earthscope.org/mustang/measurements/1/',{}),('SO7','https://static.aer.ca/prd/documents/orders/subsurface-orders/SO7.pdf',{}),('ph5_station','https://service.iris.edu/ph5ws/station/1/query',{**q.BASE,'level':'channel','format':'xml','includerestricted':'true'})]
r=list(ThreadPoolExecutor(max_workers=4).map(q.fetch,jobs))
(q.ROOT/'supplement_query_log.json').write_text(json.dumps([x for x,b in r],indent=2))
