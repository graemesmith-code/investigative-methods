"""Independent arithmetic and mask checks from released small pixel extracts."""
from collections import defaultdict
from datetime import datetime,timedelta,timezone
import hashlib
import json
import math
from pathlib import Path
from statistics import median
from zoneinfo import ZoneInfo

root=Path(__file__).resolve().parents[1]
r=json.loads((root/'evidence/followup_results.json').read_text())
ps=json.loads((root/'evidence/followup_pixel_values.json').read_text())
groups=defaultdict(list)
for p in ps: groups[(p['event'],p['date_utc'],p['region'])].append(p)
cut={'iran_june_2025':'2025-06-21','venezuela_jan_2026':'2026-01-02','iran_feb_2026':'2026-02-28'}

def valid(p,s):
    if p['radiance'] is None or not math.isfinite(p['radiance']) or p['radiance']<0: return False
    cloud=p['cloud_mask'];medium=s in ('allow_medium_cloud_quality','both_relaxations');stray=s in ('allow_a1_straylight_only','both_relaxations')
    if cloud==65535 or cloud&1 or ((cloud>>6)&3)!=0: return False
    if ((cloud>>4)&3)<(2 if medium else 3): return False
    if any((cloud>>bit)&1 for bit in (8,9,10,12,13)): return False
    if p['mandatory_quality']!=0 or p['snow_flag']!=0: return False
    if p['a1_qf_dnb']!=0 and not (stray and p['a1_qf_dnb']==16): return False
    if not 0<=p['zenith_raw']<=9000 or p['zenith_raw']*p['zenith_scale']>60: return False
    h=p['utc_hours']
    if h is None or not 0<=h<=24:return False
    when=datetime.fromisoformat(p['date_utc']).replace(tzinfo=timezone.utc)+timedelta(hours=h)
    return when<datetime.fromisoformat(cut[p['event']]).replace(tzinfo=ZoneInfo('America/New_York'))

def near(a,b):
    if a is None or b is None: assert a is b
    else: assert math.isclose(a,b,rel_tol=1e-11,abs_tol=1e-11),(a,b)
def weighted(rows):
    a=math.fsum(p['area_km2'] for p in rows)
    return math.fsum(p['area_km2']*p['radiance'] for p in rows)/a if a else None

for s in r['regional_stats']:
    allp=groups[(s['event'],s['date_utc'],s['region'])]; selected=[p for p in allp if valid(p,s['scenario'])]
    cov=math.fsum(p['area_km2'] for p in selected)/math.fsum(p['area_km2'] for p in allp)
    near(cov,s['coverage']);near(weighted(selected),s['mean_valid_subset'])
    near(weighted(selected) if cov>=.75 else None,s['mean_if_75pct'])
for pair in r['within_event_pairs']:
    controls=[]
    for q in pair['regions']:
        aa={ (p['row'],p['col']):p for p in groups[(pair['event'],pair['earlier'],q['region'])]}
        bb={ (p['row'],p['col']):p for p in groups[(pair['event'],pair['later'],q['region'])]}
        keys=[k for k in aa if valid(aa[k],pair['scenario']) and valid(bb[k],pair['scenario'])]
        for k in keys:near(aa[k]['area_km2'],bb[k]['area_km2'])
        a=weighted([aa[k] for k in keys]);b=weighted([bb[k] for k in keys]);near(a,q['earlier_mean']);near(b,q['later_mean'])
        cov=math.fsum(aa[k]['area_km2'] for k in keys)/math.fsum(p['area_km2'] for p in aa.values());near(cov,q['common_coverage'])
        change=100*(b/a-1) if a else None;near(change,q['change_pct_subset']);near(change if cov>=.75 else None,q['change_pct_if_75pct'])
        if q['region'] in ['rosslyn_commercial','reston_town_center','tysons_commercial'] and cov>=.75:controls.append(change)
    near(median(controls) if len(controls)>=2 else None,pair['control_median_change_pct'])
i=r['synthetic_injection'];rows=groups[(i['event'],i['date_utc'],'pentagon_broad')];rows=[p for p in rows if valid(p,'both_relaxations')]
ks={tuple(k) for k in r['geometry']['core_cell_keys']};before=weighted(rows)
for test in i['tests']:
    changed=[{**p,'radiance':p['radiance']*(1+test['injected_core_cells_pct']/100 if (p['row'],p['col']) in ks else 1)} for p in rows]
    near(100*(weighted(changed)/before-1),test['broad_mean_change_pct'])
for event,day,_ in groups:
    core={(p['row'],p['col']) for p in groups[(event,day,'core_500m')]};ring={(p['row'],p['col']) for p in groups[(event,day,'surround_disjoint')]}
    assert core.isdisjoint(ring)
assert hashlib.sha256((root/'FOLLOWUP_PROTOCOL.md').read_bytes()).hexdigest()==r['protocol_sha256']
out={'result':'passed','pixel_records':len(ps),'regional_mask_summaries':len(r['regional_stats']),'pair_mask_summaries':len(r['within_event_pairs']),'synthetic_perturbations':len(i['tests']),'independent_mask_decoder':True,'core_ring_no_shared_grid_cells':True}
(root/'evidence/followup_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
