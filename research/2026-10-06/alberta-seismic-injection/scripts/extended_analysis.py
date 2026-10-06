"""Surface/BH sensitivity, second catalogue, formation proxy, and grouped packets."""
import json,pathlib,datetime as dt,csv,collections
from zoneinfo import ZoneInfo
from study_logic import in_period, rule_version, shutdown_magnitude_screen
from shapely.geometry import shape,Point
from pyproj import Geod,Transformer
P=pathlib.Path(__file__).resolve().parents[1];R=P/'results';S=P/'sources'
def load(n):return json.loads((R/n).read_text())
def write(n,v):(R/n).write_text(json.dumps(v,indent=2)+'\n')
g=Geod(ellps='GRS80')
def km(a,b):return g.inv(a[0],a[1],b[0],b[1])[2]/1000
sh={r['Well_Licence_Number'].strip():r for r in load('st37-ST37_Surface_Holes.json')};lic={r['LicenceNumber']:r for r in load('petrinex-licences-period.json')}
ps={f['properties']['Order_Numb']:shape(f['geometry']) for f in load('rule-geometries.geojson')['features']};areas={'FoxCreek':ps['2'],'Brazeau':ps['6.2'],'RedDeer':ps['7.2']};th={'FoxCreek':4,'Brazeau':2.5,'RedDeer':3}
jobs=load('jobs-period.json');scoped=[]
for j in jobs:
 surface=sh.get(j['Well_Licence_Number']);j['surface']=surface
 j['licence_current']=lic.get(j['Well_Licence_Number'])
 j['surface_areas']=[a for a,p in areas.items() if surface and p.covers(Point(surface['SH_Actual_Longitude'],surface['SH_Actual_Latitude']))]
 j['any_reference_areas']=sorted(set(j['areas']+j['surface_areas']))
 if j['any_reference_areas']:scoped.append(j)
write('jobs-surface-or-bottomhole.json',scoped)
ags=[f['attributes'] for f in json.loads((S/'earthquakes.json').read_text())['features'] if in_period(f['attributes']['Datetime_UTC'])]
nrcan_raw=list(csv.DictReader((S/'nrcan-events.txt').open(),delimiter='|'));nrcan=[e for e in nrcan_raw if in_period(e['Time'])]
events=[]
for e in ags:
 for mt in ['ML','MLy']:
  if e[mt] is not None:events.append({'catalogue':'AGS','id':str(e['object_id']),'time':e['Datetime_UTC'].replace(' ','T')+'Z','lat':e['Latitude'],'lon':e['Longitude'],'magnitude':e[mt],'magnitude_type':mt,'raw':e})
for e in nrcan:events.append({'catalogue':'NRCan','id':e['#EventID'],'time':e['Time'],'lat':float(e['Latitude']),'lon':float(e['Longitude']),'magnitude':float(e['Magnitude']),'magnitude_type':e['MagType'],'raw':e})
collisions=[];near_nonoverlap=[];eventcounts=collections.Counter();areaevents=[]
for e in events:
 date=dt.datetime.fromisoformat(e['time'].replace('Z','+00:00')).astimezone(ZoneInfo('America/Edmonton')).date()
 for a,poly in areas.items():
  if not shutdown_magnitude_screen(e['magnitude_type'],e['magnitude'],th[a],allow_mly=True):continue
  # No polygon buffer prefilter: every acquired event is tested against scoped wells.
  eventcounts[(e['catalogue'],e['magnitude_type'],a)]+=1;areaevents.append({'area':a,**e})
  for j in scoped:
   if a not in j['any_reference_areas']:continue
   bh=km((e['lon'],e['lat']),(j['lon'],j['lat']))
   surface=j['surface'];ds=km((e['lon'],e['lat']),(surface['SH_Actual_Longitude'],surface['SH_Actual_Latitude'])) if surface else None
   if min(bh,ds if ds is not None else float('inf'))>5.5:continue
   start=dt.date.fromisoformat(j['start']);end=dt.date.fromisoformat(j['end']);overlap=start<=date<=end
   c={'area':a,'event':e,'job_id':j['job_id'],'uwi':j['UWI'],'licence':j['Well_Licence_Number'],'distance_bh_km':round(bh,6),'distance_surface_km':round(ds,6) if ds is not None else None,'start':j['start'],'end':j['end'],'overlap':overlap,'rule_version':rule_version(a,date.isoformat()),'formal_geological_applicability':None,'pumping_at_event':None,'reporting_window_overlap_only':True,'current_projected_formation':j['licence_current'].get('ProjectedFormation') if j['licence_current'] else None,'current_terminating_formation':j['licence_current'].get('TerminatingFormation') if j['licence_current'] else None,'classification':'indeterminate'}
   if overlap:collisions.append(c)
   else:
    gap=(date-end).days if date>end else (start-date).days
    if gap<=30:c['days_to_window']=gap;near_nonoverlap.append(c)
write('all-catalogue-collisions.json',collisions);write('near-but-nonoverlap.json',near_nonoverlap);write('threshold-area-events.json',areaevents)
# Group source rows into event-well evidence packets; distinct windows retained; no multiplicative discoveries.
group={}
for c in collisions:group.setdefault((c['event']['catalogue'],c['event']['id'],c['uwi']),[]).append(c)
packets=[]
for k,cs in sorted(group.items()):
 j=next(j for j in scoped if j['job_id']==cs[0]['job_id']);e=cs[0]['event'];a=cs[0]['area'];bhpoint=Point(j['lon'],j['lat'])
 packets.append({'packet_id':f"{k[0]}-{k[1]}-{j['Well_Licence_Number']}",'classification':'indeterminate','not_a_violation_finding':True,'rule_version':cs[0]['rule_version'],'formal_geological_applicability':None,'historical_operator_resolved':False,'raw_ingredient_rows':[{'reporting_group_id':c['job_id'],'source':'sources/SummaryChemical-WaterUse.csv.gz','line_numbers':next(x for x in scoped if x['job_id']==c['job_id'])['source_line_numbers']} for c in cs],'event':e,'records':cs,'well':{'uwi':j['UWI'],'licence':j['Well_Licence_Number'],'current_licensee':j['Licensee'],'historic_identity_status':'current labels only; exact operator at event not yet established','bottomhole':{'lat':j['lat'],'lon':j['lon']},'surface':j['surface'],'current_licence':j['licence_current']},'map_membership':{n:poly.covers(bhpoint) for n,poly in ps.items()},'missing':['actual stage interval/formation rather than licence target proxy','time-resolved pumping and stop logs','event magnitude/detection available at time','historical licensee confirmation','restart authorization if operations resumed'],'ordinary_explanations':['job window includes time not pumping','work may have stopped promptly','later activity may have written authorization','reported date window can contain multiple stages with pauses'],'source_refs':['sources/SummaryChemical-WaterUse.csv.gz','sources/earthquakes.json' if e['catalogue']=='AGS' else 'sources/nrcan-events.txt','sources/SO7.pdf' if a=='RedDeer' else 'sources/SO6.pdf' if a=='Brazeau' else 'sources/'+cs[0]['rule_version']+'.pdf','sources/ST37-excel.zip','sources/petrinex-well-license.zip']})
write('evidence-packets.json',packets)
summary={'join_coverage':{label:{'reporting_groups':len(pop),'missing_surface':sum(j['surface'] is None for j in pop),'missing_licence':sum(j['licence_current'] is None for j in pop),'missing_projected_formation':sum(not (j['licence_current'] or {}).get('ProjectedFormation') for j in pop),'missing_terminating_formation':sum(not (j['licence_current'] or {}).get('TerminatingFormation') for j in pop)} for label,pop in [('all_period',jobs),('scoped',scoped)]},'zone_membership_not_applicability':{n:sum(n in j['subareas'] for j in scoped) for n in ['6.1','6.2','7.1','7.2']},'nrcan_padded_records':len(nrcan_raw),'nrcan_outside_local_period_excluded':len(nrcan_raw)-len(nrcan),'screen_exclusions':['yellow-threshold notification/mitigation duties not evaluated','prohibited-zone HF not evaluated; formation/stage intervals unresolved','disposal and production not treated as HF','SO6/SO7 red duties beyond this bounded proximity screen not evaluated'],'surface_or_bottomhole_job_records':len(scoped),'surface_or_bottomhole_unique_uwis':len({j['UWI'] for j in scoped}),'surface_only_extra_job_records':sum(not j['areas'] for j in scoped),'by_area':{a:sum(a in j['any_reference_areas'] for j in scoped) for a in areas},'nrcan_records':len(nrcan),'nrcan_magtypes':dict(collections.Counter(e['MagType'] for e in nrcan)),'threshold_events_catalogue_wide_before_well_distance':[{ 'catalogue':k[0],'magtype':k[1],'area':k[2],'count':v} for k,v in sorted(eventcounts.items())],'overlap_records':len(collisions),'grouped_catalogue_event_well_packets':len(packets),'groups':list(group),'near_nonoverlap_records':len(near_nonoverlap),'caveat':'These are candidates only. Surface/BH alternatives are screens, not a resolved legal distance reference; 5.5 km includes boundary sensitivity. NRCan and AGS events not automatically merged. Rule geology is not inferred from name or depth. SO6/SO7 red clauses do not explicitly repeat 5km; this is a bounded proximity test, not exhaustive legal coverage.'}
write('extended-denominators.json',summary);print(json.dumps(summary,indent=2))
