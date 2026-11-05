#!/usr/bin/env python3
"""Summarize preserved responses; validates miniSEED v2 headers, not amplitudes."""
import argparse,csv,datetime,io,json,pathlib,struct,xml.etree.ElementTree as ET
p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();root=pathlib.Path(a.out);NS={'s':'http://www.fdsn.org/xml/station/1'}
rows=[]
for f in sorted((root/'raw').glob('mustang_*.body')):
 if f.name=='mustang_documentation.body':continue
 data=list(csv.DictReader(io.StringIO('\n'.join(f.read_text().splitlines()[1:]))))
 for target in sorted({d['target'] for d in data}):
  x=[d for d in data if d['target']==target]
  rows.append({'target':target,'days':len(x),'start':min(d['start'] for d in x),'end':max(d['end'] for d in x),'minimum_daily_percent':min(float(d['value']) for d in x),'maximum_daily_percent':max(float(d['value']) for d in x),'raw_file':str(f.relative_to(root))})
with (root/'mustang_summary.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
rows=[]
for f in sorted((root/'raw').glob('waveform*.body')):
 b=f.read_bytes();m=json.loads(f.with_suffix('.json').read_text())
 if m['status']!=200:continue
 o=0;records=[]
 while o<len(b):
  h=b[o:o+48];assert len(h)==48 and h[:6].isdigit() and h[6:7] in (b'D',b'R',b'Q',b'M'),f
  nsamp,factor,mult=struct.unpack('>Hhh',h[30:36]);rate=(factor if factor>0 else -1/factor)*(mult if mult>0 else -1/mult)
  y,j=struct.unpack('>HH',h[20:24]);frac=struct.unpack('>H',h[28:30])[0]
  st=datetime.datetime(y,1,1,tzinfo=datetime.timezone.utc)+datetime.timedelta(days=j-1,hours=h[24],minutes=h[25],seconds=h[26],microseconds=frac*100)
  k=struct.unpack('>H',h[46:48])[0];reclen=None
  while k:
   typ,nxt=struct.unpack('>HH',b[o+k:o+k+4])
   if typ==1000:reclen=2**b[o+k+6];break
   k=nxt
  assert reclen and o+reclen<=len(b),(f,o,reclen)
  records.append((st,st+datetime.timedelta(seconds=(nsamp-1)/rate),nsamp,rate,h[18:20].decode().strip(),h[8:13].decode().strip(),h[15:18].decode().strip()))
  o+=reclen
 rows.append({'file':f.name,'network':records[0][4],'station':records[0][5],'channel':records[0][6],'records':len(records),'samples':sum(r[2] for r in records),'sample_rates':','.join(map(str,sorted({r[3] for r in records}))),'first_sample_utc':min(r[0] for r in records).isoformat(),'last_sample_utc':max(r[1] for r in records).isoformat(),'http_status':m['status'],'bytes':len(b)})
with (root/'waveform_validation.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
def identifiers(body):
 x=ET.fromstring(body)
 return {(n.attrib['code'],s.attrib['code'],c.attrib.get('locationCode',''),c.attrib['code'],c.attrib.get('startDate',''),c.attrib.get('endDate','')) for n in x.findall('s:Network',NS) for s in n.findall('s:Station',NS) for c in s.findall('s:Channel',NS)}
t=identifiers((root/'raw/station_service.earthscope.org_true.body').read_bytes());f=identifiers((root/'raw/station_service.earthscope.org_false.body').read_bytes())
(root/'restriction_filter_difference.json').write_text(json.dumps({'note':'Omission when includerestricted=false is a discovery flag, not proof that every historical sample is inaccessible. Four I0 February2 samples downloaded anonymously.','included_only_when_true':sorted(t-f)},indent=2))
print('Saved MUSTANG summaries, validated miniSEED v2 headers, and restriction-filter difference. Successful samples:',len(rows))
