"""Offline metadata/format/coverage inspection only; no filters, picks or magnitude estimates."""
import pathlib,json,csv,xml.etree.ElementTree as ET
from pyproj import Geod
from obspy import read,read_inventory,UTCDateTime,__version__
P=pathlib.Path(__file__).resolve().parents[1];S=P/'sources/waveforms';R=P/'results/waveforms';g=Geod(ellps='GRS80')
def dist(lat,lon):return g.inv(-113.957,52.215,float(lon),float(lat))[2]/1000
networks={}
for net in ['2K','I0']:
 rows=[]
 for s in ET.parse(S/(net+'-all-stations.xml')).findall('.//{*}Station'):
  lat=s.find('{*}Latitude').text;lon=s.find('{*}Longitude').text
  rows.append({'station':s.attrib['code'],'lat':float(lat),'lon':float(lon),'distance_to_cluster_centre_km':dist(lat,lon),'metadata_restricted_status':s.attrib.get('restrictedStatus'),'epoch_start':s.attrib.get('startDate'),'epoch_end':s.attrib.get('endDate')})
 networks[net]={'stations_returned':len(rows),'within_111km':sum(r['distance_to_cluster_centre_km']<=111 for r in rows),'stations':sorted(rows,key=lambda r:r['distance_to_cluster_centre_km'])}
rows=list(csv.DictReader((S/'RV-channels.txt').open(),delimiter='|'));rv={}
for r in rows:
 if r[' Channel '].strip().startswith('HH'):
  sta=r[' Station '].strip();rv[sta]={'station':sta,'lat':float(r[' Latitude ']),'lon':float(r[' Longitude ']),'distance_to_cluster_centre_km':dist(r[' Latitude '],r[' Longitude '])}
rv=sorted(rv.values(),key=lambda r:(r['distance_to_cluster_centre_km'],r['station']));assert rv[0]['station']=='REDDA'
outputs=[]
for eid,event in [('ca2025dscb','2025-02-22T14:05:18Z'),('ca2025dwzq','2025-02-25T06:32:36Z')]:
 st=read(str(S/(eid+'-RV-REDDA.mseed')),format='MSEED');inv=read_inventory(str(S/(eid+'-RV-REDDA-response.xml')));traces=[]
 for tr in st:
  response=inv.get_response(tr.id,UTCDateTime(event));traces.append({'id':tr.id,'start_utc':str(tr.stats.starttime),'end_utc':str(tr.stats.endtime),'samples':tr.stats.npts,'sample_rate_hz':tr.stats.sampling_rate,'data_encoding':tr.stats.mseed.encoding,'event_timestamp_covered':tr.stats.starttime<=UTCDateTime(event)<=tr.stats.endtime,'instrument_response_found':bool(response.response_stages),'instrument_input_units':response.instrument_sensitivity.input_units,'raw_sample_dtype':str(tr.data.dtype)})
 assert len(traces)==3 and all(t['event_timestamp_covered'] and t['instrument_response_found'] for t in traces)
 outputs.append({'event_id':eid,'event_utc':event,'traces':traces,'gap_records':[list(x) for x in st.get_gaps()],'interpretation':'Data availability and parse validation only; earthquake signal attribution, timing accuracy, magnitude and operator receipt were not assessed.'})
result={'scope':{'cluster_centre':[52.215,-113.957],'metadata_radius_degrees':1,'window_seconds_before_event':60,'window_seconds_after_event':120,'networks_checked':['2K','I0','RV'],'waveform_station_selection':'nearest returned RV HH-channel station to cluster centre; no company seed'},'software':{'obspy':__version__},'industry_network_metadata':networks,'regional_nearby_stations':rv,'waveform_checks':outputs,'compliance_conclusion':None,'new_magnitude_estimates':None}
(R/'availability-summary.json').write_text(json.dumps(result,indent=2,default=str)+'\n');print(json.dumps({'industry_station_counts':{k:v['stations_returned'] for k,v in networks.items()},'RV_HH_stations':rv,'waveform_checks':outputs},indent=2))
