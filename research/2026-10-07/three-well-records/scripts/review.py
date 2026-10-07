"""Offline replay of follow-up joins, coordinate audit and provenance inventory."""
import pathlib,json,hashlib,re,math
P=pathlib.Path(__file__).resolve().parents[1]; O=P.parents[1]/'2026-10-06/alberta-seismic-injection'; ids={'0515889','0516327','0516328'}
def read(p):return json.loads(p.read_text())
def save(n,x):(P/'results'/n).write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Recreate current all-leg extracts from frozen prior tables, not a live lookup.
names=['st37-ST_37_Bottom_Hole.json','st37-Production_String.json']
save('current-all-leg-mapping.json',{n:[r for r in read(O/'results'/n) if r['Well_Licence_Number'].strip() in ids] for n in names})
# PDF extraction is reproducible; original PDF bytes remain authoritative.
import fitz
pdfs=[]
for f in sorted((P/'sources/public-documents').glob('*.pdf')):
 d=fitz.open(f);pdfs.append({'file':str(f.relative_to(P)),'pages':len(d),'text':'\n'.join('PAGE '+str(i+1)+'\n'+p.get_text() for i,p in enumerate(d))})
save('public-pdf-extracts.json',pdfs)
sh={r['Well_Licence_Number']:r for r in read(O/'results/st37-ST37_Surface_Holes.json') if r['Well_Licence_Number'] in ids}
coords={}
for p in pdfs:
 if 'Well-Licence-' not in p['file']:continue
 licence=re.search(r'Well-Licence-(\d+)',p['file'])[1]
 m=re.search(r'Surface Latitude\s+Surface Longitude\s+\(NAD83 ATS 4.1\)\s+([\d.]+)\s+(-[\d.]+)',p['text']);assert m
 lat,lon=map(float,m.groups());assert (lat,lon)==(sh[licence]['SH_Actual_Latitude'],sh[licence]['SH_Actual_Longitude'])
 coords[licence]={'lat':lat,'lon':lon,'original_licence_pdf':p['file'],'matches_later_ST37_surface':True,'datum_label':'NAD83 ATS 4.1'}
from pyproj import Geod
g=Geod(ellps='GRS80')
def km(a,b,c,d):return g.inv(b,a,d,c)[2]/1000
audit=[]
for p in read(O/'results/evidence-packets.json'):
 r=p['records'][0];e=p['event'];c=coords[r['licence']];v=km(e['lat'],e['lon'],c['lat'],c['lon']);assert abs(v-r['distance_surface_km'])<0.001
 audit.append({'packet_id':p['packet_id'],'licence':r['licence'],'event_id':e['id'],'surface_distance_recomputed_km':round(v,6),'prior_surface_distance_km':r['distance_surface_km'],'prior_current_BH_distance_km':r['distance_bh_km'],'historical_stage_distance_km':None,'classification':'indeterminate','BH_distance_status':'Later-snapshot screening proxy; NOT verified February 2025 geometry'})
save('coordinate-history-audit.json',{'surface_coordinates':coords,'method':'GRS80 ellipsoidal geodesic, matching prior screen; original licence NAD83 ATS4.1 numeric coordinates match later ST37. Approximate catalogue epicentre-to-surface distances, not hypocentral/stage distances; location/datum uncertainty not quantified.','packets':audit,'historical_BH_or_stage_geometry_available':False,'result':'Surface screening survives. Historical BH distances and stage rule-area membership remain unverified. Do not backproject October 2025 updates.'})
prior=[]
for n in sorted(ids):
 f=O/'sources'/f'iar-search-{n}.html';m=re.search(r'Total Applications Found:\s*(?:<[^>]+>\s*)*(\d+)',f.read_text());assert m and int(m[1])==0
 prior.append({'licence':n,'source':str(f.relative_to(O)),'prior_root':'research/2026-10-06/alberta-seismic-injection','sha256':sha(f),'displayed_total':0,'inference':'Zero in this query/index only; never proof records or consent absent.'})
save('prior-iar-count-check.json',prior)
# Explicit hashes of every frozen earlier input used by follow-up scripts/review.
deps=['sources/petrinex-vol-2025-02.zip','sources/petrinex-operator-history.zip','results/evidence-packets.json','results/st37-ST37_Surface_Holes.json']+['results/'+n for n in names]+['sources/iar-search-'+n+'.html' for n in sorted(ids)]
save('prior-source-dependencies.json',{'preserved_commit':'e3986e42a96ab70cbd1ed88e9123fecacbb59fb3','root':str(O.relative_to(P.parents[2])),'files':[{'path':n,'bytes':(O/n).stat().st_size,'sha256':sha(O/n)} for n in deps]})
save('source-inventory.json',[{'path':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted((P/'sources').rglob('*')) if f.is_file()])
print('Replayed PDF extracts, current tables, nine coordinate comparisons, prior IAR counts and source inventories.')
