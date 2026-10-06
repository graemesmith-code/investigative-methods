"""Offline, deterministic candidate generation; never a compliance adjudication."""
import csv,gzip,json,datetime as dt,hashlib,zipfile,io,collections,math,re
from pathlib import Path
from zoneinfo import ZoneInfo
from study_logic import local_date, in_period
import shapefile
from shapely.geometry import shape,Point,mapping
from pyproj import Geod
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'sources'; R=ROOT/'results';R.mkdir(exist_ok=True)
def write(name,x): (R/name).write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def num(s):
 try:v=float(s);return v if math.isfinite(v) else None
 except (TypeError,ValueError):return None
geod=Geod(ellps='GRS80')
def km(lon1,lat1,lon2,lat2):return geod.inv(lon1,lat1,lon2,lat2)[2]/1000
z=zipfile.ZipFile(S/'order-shapes.zip');reader=shapefile.Reader(shp=io.BytesIO(z.read('Subsurface_Orders.shp')),shx=io.BytesIO(z.read('Subsurface_Orders.shx')),dbf=io.BytesIO(z.read('Subsurface_Orders.dbf')))
polys={x.record['Order_Numb']:shape(x.shape.__geo_interface__) for x in reader.iterShapeRecords()}
write('rule-geometries.geojson',{'type':'FeatureCollection','crs_note':'Source NAD83 geographic degrees. SO2 historical label retained; SO2A geometry continuity is a visual appendix comparison, not a new versioned GIS record. Strat_Unit field does not override operative PDF geology.','features':[{'type':'Feature','properties':x.record.as_dict(),'geometry':x.shape.__geo_interface__} for x in reader.iterShapeRecords() if x.record['Order_Numb'] in ['2','6.1','6.2','7.1','7.2']]})
areas={'FoxCreek':polys['2'],'Brazeau':polys['6.2'],'RedDeer':polys['7.2']};threshold={'FoxCreek':4.,'Brazeau':2.5,'RedDeer':3.}
# Repeated component/ingredient rows are not separate operations. Keep every distinct reported job window/submission.
jobs={};rows=0;badrows=0;footers=[]
with gzip.open(S/'SummaryChemical-WaterUse.csv.gz','rt',encoding='utf-8-sig',newline='') as f:
 for source_line,line in enumerate(f,1):
  if line.startswith('Well_Licence_Number|'):header=line.strip().split('|');break
 for source_line,line in enumerate(f,source_line+1):
  if not line.strip():continue
  parts=next(csv.reader([line],delimiter='|'))
  if len(parts)!=len(header):
   if line.startswith('(595923 rows affected)') or line.startswith('Completion time:'):footers.append(line.strip());continue
   badrows+=1;continue
  rows+=1
  r={k:v.strip() for k,v in zip(header,parts)}
  k=tuple(r[x] for x in ['Well_Licence_Number','UWI','Last_Submission_Date','Start_Date','End_Date','Bottom_Hole_Latitude','Bottom_Hole_Longitude'])
  if k not in jobs:
   jobs[k]={x:r[x] for x in header[:14] if x not in ['Total_Water_Volume','Number_Of_Stages']};jobs[k].update(ingredient_rows=0,water_values=set(),stage_values=set(),source_line_numbers=[],retained_field_values={x:set() for x in header[:14] if x not in ['Total_Water_Volume','Number_Of_Stages']})
  jobs[k]['source_line_numbers'].append(source_line)
  for field,values in jobs[k]['retained_field_values'].items():values.add(r[field])
  jobs[k]['ingredient_rows']+=1;jobs[k]['water_values'].add(r['Total_Water_Volume']);jobs[k]['stage_values'].add(r['Number_Of_Stages'])
for i,j in enumerate(jobs.values()):
 j['retained_field_conflicts']={k:sorted(v) for k,v in j.pop('retained_field_values').items() if len(v)>1}
 j['water_values']=sorted(j['water_values']);j['stage_values']=sorted(j['stage_values']);j['job_id']=hashlib.sha256(json.dumps({k:v for k,v in j.items() if k not in ['ingredient_rows','water_values','stage_values','source_line_numbers','retained_field_conflicts']},sort_keys=True).encode()).hexdigest()[:16]
 j['start']=j['Start_Date'][:10];j['end']=j['End_Date'][:10];j['lat']=num(j['Bottom_Hole_Latitude']);j['lon']=num(j['Bottom_Hole_Longitude'])
 j['valid_window']=bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}',j['start']) and re.fullmatch(r'\d{4}-\d{2}-\d{2}',j['end']) and j['start']<=j['end'])
 j['in_period']=j['valid_window'] and j['start']<='2025-12-31' and j['end']>='2020-01-01'
 j['valid_coord']=j['lat'] is not None and j['lon'] is not None and 48<=j['lat']<=61 and -121<=j['lon']<=-109
 j['areas']=[a for a,p in areas.items() if j['valid_coord'] and p.covers(Point(j['lon'],j['lat']))]
 j['subareas']=[a for a in ['6.1','6.2','7.1','7.2'] if j['valid_coord'] and polys[a].covers(Point(j['lon'],j['lat']))]
alljobs=list(jobs.values());scope=[j for j in alljobs if j['in_period'] and j['areas']]
write('jobs-scoped.json',scope);write('jobs-period.json',[j for j in alljobs if j['in_period']])
raw=json.loads((S/'earthquakes.json').read_text());assert 'error' not in raw and not raw.get('exceededTransferLimit')
events=[f['attributes'] for f in raw['features']];assert len({e['object_id'] for e in events})==len(events)
padded_count=len(events)
events=[e for e in events if in_period(e['Datetime_UTC'])]
for e in events:e['local_date']=local_date(e['Datetime_UTC'])
candidates=[];sens=[];spatial_only=[]
for a,poly in areas.items():
 aj=[j for j in scope if a in j['areas']]
 # All province events considered for proximity to scoped wells, including events outside area polygon.
 for e in events:
  ml=num(e['ML']);mly=num(e['MLy'])
  passes=ml is not None and ml>=threshold[a]
  alt=mly is not None and mly>=threshold[a]
  if not (passes or alt):continue
  for j in aj:
   d=km(e['Longitude'],e['Latitude'],j['lon'],j['lat'])
   if d>5.5:continue
   overlap=j['start']<=e['local_date']<=j['end']
   record={'area':a,'threshold_ML':threshold[a],'event':e,'job':j,'distance_bottomhole_km':round(d,6),'screen_distance_within_5km':d<=5,'date_window_overlap':overlap,'rule_version':'SO2A' if a=='FoxCreek' and e['local_date']>='2024-11-19' else {'FoxCreek':'SO2','Brazeau':'SO6','RedDeer':'SO7'}[a],'classification':'indeterminate','missing_evidence':['formation and actual stimulated interval','surface and stage/trajectory distance variants','actual pumping intervals and stop time','magnitude available to licensee and detection time','restart consent and approved modified plan, if resumed','historic operator identity verification','quantified event location uncertainty'],'not_established':['continuous pumping within reported job window','pumping after threshold earthquake','causation','noncompliance']}
   if overlap:
    record['packet_id']=f"{a}-{e['object_id']}-{j['job_id']}"
    if passes:candidates.append(record)
    elif alt:sens.append(record)
   elif passes and d<=5:spatial_only.append({'area':a,'event_id':e['object_id'],'job_id':j['job_id'],'distance_km':round(d,6),'date_window_overlap':False})
write('candidates-ML.json',candidates);write('sensitivity-MLy-only.json',sens);write('spatial-without-temporal-controls.json',spatial_only)
counts={'retained_field_conflict_groups':sum(bool(j['retained_field_conflicts']) for j in alljobs),'catalogue_padded_UTC_records':padded_count,'catalogue_outside_local_period_excluded':padded_count-len(events),'raw_ingredient_rows':rows,'source_footers':footers,'malformed_rows':badrows,'all_distinct_job_window_submissions':len(alljobs),'all_period_jobs':sum(j['in_period'] for j in alljobs),'invalid_windows':sum(not j['valid_window'] for j in alljobs),'period_jobs_invalid_coordinates':sum(j['in_period'] and not j['valid_coord'] for j in alljobs),'scoped_bottomhole_jobs':len(scope),'scoped_unique_uwis':len({j['UWI'] for j in scope}),'catalogue_events_2020_2025':len(events),'events_missing_ML':sum(e['ML'] is None for e in events),'events_missing_MLy':sum(e['MLy'] is None for e in events),'by_area':{a:{'jobs':sum(a in j['areas'] for j in scope),'ML_pairs_5km':sum(c['area']==a and c['screen_distance_within_5km'] for c in candidates),'ML_pairs_5_to_5_5km':sum(c['area']==a and not c['screen_distance_within_5km'] for c in candidates),'MLy_only_pairs_5km':sum(c['area']==a and c['screen_distance_within_5km'] for c in sens)} for a in areas},'ML_pairs':len(candidates),'ML_unique_events':len({c['event']['object_id'] for c in candidates}),'MLy_only_pairs':len(sens),'spatial_nonoverlap_pairs':len(spatial_only),'compliance_testable_packets':0,'date_min':min(e['Datetime_UTC'] for e in events),'date_max':max(e['Datetime_UTC'] for e in events),'coverage_caveat':'Not an exposure denominator: bottomhole-only area selection omits surface-only in-area wells; current reported submissions and mutable catalogue are not historical snapshots; ML missingness and unknown monitoring completeness prevent negative conclusions.'}
write('denominators.json',counts);write('actual-schemas.json',{'fracture_columns':header,'earthquake_fields':raw['fields'],'order_fields':[list(f) for f in reader.fields]})
print(json.dumps(counts,indent=2))
