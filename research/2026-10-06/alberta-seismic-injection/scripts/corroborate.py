import pathlib,json,datetime as dt,csv,io,zipfile,xml.etree.ElementTree as ET,collections,re
from pyproj import Geod
P=pathlib.Path(__file__).resolve().parents[1];R=P/'results';S=P/'sources'
def write(n,x):(R/n).write_text(json.dumps(x,indent=2)+'\n')
def readzip(name):
 z=zipfile.ZipFile(S/name);n=z.namelist()[0]
 if n.endswith('.zip'):z=zipfile.ZipFile(io.BytesIO(z.read(n)));n=z.namelist()[0]
 return csv.DictReader(io.TextIOWrapper(z.open(n),encoding='utf-8-sig'))
def uwi_to_petrinex(uwi):
 assert re.fullmatch(r'[0-9A-Z]{2}/\d{2}-\d{2}-\d{3}-\d{2}W[456]/\d',uwi),uwi
 return 'ABWI1'+re.sub(r'[/\-]','',uwi)+'0'
packets=json.loads((R/'evidence-packets.json').read_text());ids={uwi_to_petrinex(p['well']['uwi']):p['well']['uwi'] for p in packets}
rd=readzip('petrinex-vol-2025-02.zip');found=[];n=0
for r in rd:
 n+=1
 if r['FromToID'] in ids:found.append(r)
fac={r['ReportingFacilityID'] for r in found};hist=[];nh=0
for r in readzip('petrinex-operator-history.zip'):
 nh+=1
 if r['FacilityID'] in fac:hist.append(r)
write('monthly-target-identity.json',{'period':'2025-02','purpose':'post-discovery identity corroboration only; NOT pumping timing','uwi_mapping':ids,'rows_scanned':n,'matched_rows':found,'operator_history_rows_scanned':nh,'facility_operator_history':hist,'caveat':'FromToID match identifies a well event, but facility operator is not automatically HF service provider or historic licensee; monthly load injection and production cannot prove stage timing.'})
# Candidate cross-catalogue matches using predeclared +/-10 sec AND <=10km, retain all matches.
g=Geod(ellps='GRS80');ags=[f['attributes'] for f in json.loads((S/'earthquakes.json').read_text())['features']];out=[]
for eid,e in {p['event']['id']:p['event'] for p in packets if p['event']['catalogue']=='NRCan'}.items():
 t=dt.datetime.fromisoformat(e['time'].replace('Z','+00:00'));matches=[]
 for a in ags:
  at=dt.datetime.fromisoformat(a['Datetime_UTC']).replace(tzinfo=dt.timezone.utc);seconds=abs((at-t).total_seconds())
  if seconds<=10:
   km=g.inv(a['Longitude'],a['Latitude'],e['lon'],e['lat'])[2]/1000
   if km<=10:matches.append({'AGS':a,'seconds_difference':seconds,'horizontal_km_difference':km})
 out.append({'NRCan':e,'candidate_matches':matches,'unique_within_tolerance':len(matches)==1})
write('catalogue-crosschecks.json',out)
x=ET.parse(S/'nrcan-events.xml').getroot();events=x.findall('.//{*}event');selected=[]
for e in events:
 if e.attrib['publicID'].split('/')[-1] in {p['event']['id'] for p in packets}:
  selected.append({'publicID':e.attrib['publicID'],'xml':ET.tostring(e,encoding='unicode')})
write('nrcan-version-uncertainty.json',{'event_count':len(events),'events_with_uncertainty_element':sum(bool(e.findall('.//{*}uncertainty')) for e in events),'events_with_origin_uncertainty':sum(bool(e.findall('.//{*}originUncertainty')) for e in events),'note':'No per-event numerical spatial uncertainty supplied. XML depth values numerically match CSV km values rather than assumed QuakeML metres; use explicit CSV Depth/km, do not silently reinterpret XML depth. Creation times are catalogue metadata, not operator detection/notification times.','candidate_xml':selected})
print('February rows',n,'well matches',len(found),'operator history',len(hist))
print(json.dumps(out,indent=2)[:5000])
