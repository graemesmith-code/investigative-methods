"""Independent stdlib recheck of masks, time cutoffs and area aggregation."""
from collections import defaultdict
from datetime import datetime,timedelta,timezone
import json
import math
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[1]
CUTOFFS={'iran_june_2025':'2025-06-21','venezuela_jan_2026':'2026-01-02','iran_feb_2026':'2026-02-28'}
data=json.loads((ROOT/'evidence/measurement_results.json').read_text())
pixels=json.loads((ROOT/'evidence/pixel_quality_extracts.json').read_text())
groups=defaultdict(list)
for p in pixels:
    groups[(p['event'],p['date_utc'],p['region'])].append(p)
for result in data['regional_results']:
    ps=groups[(result['event'],result['date_utc'],result['region'])]
    total=math.fsum(p['area_km2'] for p in ps)
    assert math.isclose(total,result['area_km2'],rel_tol=1e-12)
    for name,scenario in data['scenarios'].items():
        area=[]
        for p in ps:
            c=p['cloud_mask']; h=p['utc_hours']; z=p['zenith_raw']
            qgood=(c&48) in ([32,48] if scenario['allow_medium_cloud_quality'] else [48])
            fgood=p['a1_qf_dnb'] in ([0,16] if scenario['allow_a1_straylight_only'] else [0])
            tgood=h is not None and 0<=h<=24
            if tgood:
                observed=datetime.fromisoformat(p['date_utc']).replace(tzinfo=timezone.utc)+timedelta(hours=h)
                limit=datetime.fromisoformat(CUTOFFS[p['event']]).replace(tzinfo=ZoneInfo('America/New_York'))
                tgood=observed<limit
            good=(p['observed_available'] and p['mandatory_quality']==0 and p['snow_flag']==0 and c!=65535 and (c&0x37C1)==0 and qgood and fgood and 0<=z<=9000 and z*p['zenith_scale']<=60 and tgood)
            if name=='primary': assert good==p['primary_pass']
            if good: area.append(p['area_km2'])
        assert math.isclose(math.fsum(area)/total,result['coverage'][name],rel_tol=0,abs_tol=1e-12)
for d in data['dates']:
    rows=[r for r in data['regional_results'] if (r['event'],r['date_utc'])==(d['event'],d['date_utc'])]
    for s in data['scenarios']:
        target=next(r for r in rows if r['role']=='target')
        ok=target['coverage'][s]>=.75 and sum(r['coverage'][s]>=.75 for r in rows if r['role']=='comparison')>=2
        assert ok==d['date_pass'][s]
result={'pixel_checks':len(pixels),'regional_checks':len(groups),'scenarios':len(data['scenarios']),'result':'passed','tolerance_absolute':1e-12}
(ROOT/'evidence/independent_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
