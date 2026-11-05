#!/usr/bin/env python3
"""Read-only, dependency-free EarthScope audit. Keeps HTTP bodies and provenance.
Station metadata is not waveform availability, and a 404 is not proof of non-filing.
The time window is Feb 1 through March 31 inclusive (end April 1 UTC).
"""
import argparse, csv, datetime, hashlib, json, math, pathlib, urllib.request, urllib.parse, urllib.error, xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
NS={'s':'http://www.fdsn.org/xml/station/1'}
LAT,LON=52.222509,-114.001397
BASE={'latitude':LAT,'longitude':LON,'maxradius':25/111.195,'starttime':'2025-02-01T00:00:00','endtime':'2025-04-01T00:00:00','nodata':404}
ROOT=None

def fetch(job):
 name,url,params=job
 url=url+('?' + urllib.parse.urlencode(params) if params else '')
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 error=None; status=None; headers={}; final_url=url; body=b''
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Cygnet-public-record-verification/1.0'}),timeout=90) as r:
   status=r.status;headers=dict(r.headers);final_url=r.url;body=r.read()
 except urllib.error.HTTPError as e:
  status=e.code;headers=dict(e.headers);final_url=e.url;body=e.read();error=str(e)
 except Exception as e:error=repr(e)
 stem=ROOT/'raw'/name;stem.parent.mkdir(parents=True,exist_ok=True)
 pathlib.Path(str(stem)+'.body').write_bytes(body)
 rec={'name':name,'accessed_at_utc':now,'requested_url':url,'parameters':params,'final_url':final_url,'status':status,'headers':headers,'error':error,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'body_file':str(pathlib.Path(str(stem)+'.body').relative_to(ROOT))}
 pathlib.Path(str(stem)+'.json').write_text(json.dumps(rec,indent=2))
 print(name,status,len(body),error or '',flush=True)
 return rec,body

def dist(lat,lon):
 a,b,p,q=map(math.radians,[LAT,LON,lat,lon]);d=math.sin((p-a)/2)**2+math.cos(a)*math.cos(p)*math.sin((q-b)/2)**2
 return 6371.0088*2*math.asin(math.sqrt(d))

def run(out, windows):
 global ROOT
 ROOT=pathlib.Path(out);ROOT.mkdir(parents=True,exist_ok=True)
 jobs=[]
 for host in ('service.iris.edu','service.earthscope.org'):
  for restricted in ('true','false'):
   jobs.append((f'station_{host}_{restricted}',f'https://{host}/fdsnws/station/1/query',{**BASE,'level':'channel','format':'xml','includerestricted':restricted}))
 for net in ('RV','TD','AB','CN','EO','I0','2K'):
  jobs.append((f'station_network_{net}','https://service.earthscope.org/fdsnws/station/1/query',{**BASE,'network':net,'level':'channel','format':'xml','includerestricted':'true'}))
 jobs += [('fdsn_I0','https://www.fdsn.org/networks/detail/I0/',{}),('fdsn_2K','https://www.fdsn.org/networks/detail/2K_2014/',{}),('fdsn_RV','https://www.fdsn.org/networks/detail/RV/',{}),('station_help','https://service.earthscope.org/fdsnws/station/docs/1/help/',{})]
 results=list(ThreadPoolExecutor(max_workers=4).map(fetch,jobs))
 rows=[]
 rec,body=results[2]
 if rec['status']!=200: rec,body=results[0]
 if rec['status']==200:
  root=ET.fromstring(body)
  for net in root.findall('s:Network',NS):
   for sta in net.findall('s:Station',NS):
    lat=float(sta.findtext('s:Latitude',namespaces=NS));lon=float(sta.findtext('s:Longitude',namespaces=NS))
    for ch in sta.findall('s:Channel',NS):
     rows.append({'network':net.attrib['code'],'station':sta.attrib['code'],'location':ch.attrib.get('locationCode',''),'channel':ch.attrib['code'],'latitude':lat,'longitude':lon,'distance_pad_km':round(dist(lat,lon),4),'network_restricted_status':net.attrib.get('restrictedStatus','unknown'),'station_restricted_status':sta.attrib.get('restrictedStatus','unknown'),'iris_alternate_network_codes':sta.attrib.get('{http://www.fdsn.org/xml/station/1/iris}alternateNetworkCodes',''),'channel_restricted_status':ch.attrib.get('restrictedStatus','unknown'),'start':ch.attrib.get('startDate',''),'end':ch.attrib.get('endDate',''),'sample_rate':ch.findtext('s:SampleRate','',NS),'site':sta.findtext('s:Site/s:Name','',NS)})
 if rows:
  with (ROOT/'channels.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 pairs=sorted({(r['network'],r['station']) for r in rows})
 jobs=[]
 for n,s in pairs:
  jobs.append((f'mda_{n}_{s}',f'https://ds.iris.edu/mda/{n}/{s}/',{}))
  jobs.append((f'availability_{n}_{s}','https://service.earthscope.org/fdsnws/availability/1/query',{'network':n,'station':s,'channel':'HH?','starttime':BASE['starttime'],'endtime':BASE['endtime'],'format':'json','nodata':404}))
 for n in sorted({n for n,s in pairs}|{'I0','2K'}):jobs.append((f'mda_{n}',f'https://ds.iris.edu/mda/{n}/',{}))
# Anonymous spot-check windows are supplied from a separately stored CSV.
 for n,s in pairs:
  for label,start,end in windows:
   jobs.append((f'waveform_{n}_{s}_{label}','https://service.earthscope.org/fdsnws/dataselect/1/query',{'net':n,'sta':s,'loc':'--','cha':'HHZ','start':start,'end':end,'nodata':404}))
 more=list(ThreadPoolExecutor(max_workers=4).map(fetch,jobs));results+=more
 (ROOT/'query_log.json').write_text(json.dumps([r for r,b in results],indent=2))
 print('DONE',len(results),'queries',len(rows),'channel epochs',len(pairs),'stations',flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--windows-csv',required=True,help='Private input CSV: label,start,end, UTC ISO timestamps');a=p.parse_args();windows=[(r['label'],r['start'],r['end']) for r in csv.DictReader(open(a.windows_csv))];run(a.out,windows)
