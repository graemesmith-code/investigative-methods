"""Exploratory quality, localization and sensitivity tests; no anomaly detector."""
from collections import defaultdict
from datetime import datetime,timedelta,timezone
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path
from zoneinfo import ZoneInfo
import h5py
import numpy as np
from check_measurement import ROOT,GROUP,area,CUTOFFS

SCENARIOS={'primary':(False,False),'allow_a1_straylight_only':(True,False),'allow_medium_cloud_quality':(False,True),'both_relaxations':(True,True)}
NY=ZoneInfo('America/New_York')

def write(name,data): (ROOT/'evidence'/name).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
def key(p): return p['row'],p['col']
def good(p,scenario):
    stray,medium=SCENARIOS[scenario]; c=p['cloud_mask']; h=p['utc_hours']; z=p['zenith_raw']
    tgood=h is not None and 0<=h<=24
    if tgood:
        observed=datetime.fromisoformat(p['date_utc']).replace(tzinfo=timezone.utc)+timedelta(hours=h)
        cutoff=datetime.fromisoformat(CUTOFFS[p['event']]).replace(tzinfo=NY)
        tgood=observed<cutoff
    return bool(p['observed_available'] and p['mandatory_quality']==0 and p['snow_flag']==0 and c!=65535 and (c&0x37c1)==0 and ((c>>4)&3) in ([2,3] if medium else [3]) and p['a1_qf_dnb'] in ([0,16] if stray else [0]) and 0<=z<=9000 and z*p['zenith_scale']<=60 and tgood)

def stats(ps,selected):
    total=math.fsum(p['area_km2'] for p in ps)
    chosen=[p for p in ps if selected(p)]
    a=math.fsum(p['area_km2'] for p in chosen)
    avg=math.fsum(p['area_km2']*p['radiance'] for p in chosen)/a if a else None
    fraction=a/total
    return {'coverage':fraction,'n_valid_cells':len(chosen),'total_cells':len(ps),'valid_area_km2':a,'total_area_km2':total,'mean_valid_subset':avg,'mean_if_75pct':avg if fraction>=.75 else None}

def intersect_weight(p,box):
    lat=40-p['row']/240; lon=-80+p['col']/240; d=1/480
    w,s,e,n=box; west=max(w,lon-d);east=min(e,lon+d);south=max(s,lat-d);north=min(n,lat+d)
    return float(area(west,south,east,north)) if east>west and north>south else 0

def main():
    pre=json.loads((ROOT/'evidence/followup_preanalysis.json').read_text())
    assert hashlib.sha256((ROOT/'FOLLOWUP_PROTOCOL.md').read_bytes()).hexdigest()==pre['files']['FOLLOWUP_PROTOCOL.md']
    old=json.loads((ROOT/'evidence/measurement_results.json').read_text())
    source=json.loads((ROOT/'evidence/pixel_quality_extracts.json').read_text())
    verified=json.loads((ROOT/'evidence/verified_uploads.json').read_text())
    source_sha=hashlib.sha256((ROOT/'evidence/pixel_quality_extracts.json').read_bytes()).hexdigest()
    cfg=json.loads((ROOT/'config.json').read_text()); target=cfg['regions'][0]
    w,s,e,n=target['bbox_wgs84']; x=(w+e)/2;y=(s+n)/2
    boxes={f'core_{metres}m':[x-(e-w)*metres/4000,y-(n-s)*metres/4000,x+(e-w)*metres/4000,y+(n-s)*metres/4000] for metres in [500,1000]}
    groups=defaultdict(list)
    for p in source: groups[(p['event'],p['date_utc'],p['region'])].append(p.copy())
    all_dates=sorted({(p['event'],p['date_utc']) for p in source},key=lambda a:a[1])
    records=[]; contrasts=[]; selection=[]; ancillary=[]
    for event,day in all_dates:
        archive=next(a for a in verified if a['event']==event)
        a2=next(m['filename'] for m in archive['manifest'] if m['product']=='VNP46A2' and m['observation_date_utc']==day)
        a1=next(m['filename'] for m in archive['manifest'] if m['product']=='VNP46A1' and m['observation_date_utc']==day)
        with h5py.File(ROOT/'raw'/a2) as f,h5py.File(ROOT/'raw'/a1) as f1:
            ds=f[GROUP]['DNB_BRDF-Corrected_NTL'];fill=float(np.asarray(ds.attrs['_FillValue']).flat[0]); assert float(np.asarray(ds.attrs['scale_factor']).flat[0])==1
            for region in cfg['regions']:
                ps=groups[(event,day,region['id'])]
                r0,r1=min(p['row'] for p in ps),max(p['row'] for p in ps);c0,c1=min(p['col'] for p in ps),max(p['col'] for p in ps)
                values=ds[r0:r1+1,c0:c1+1]
                for p in ps:
                    v=float(values[p['row']-r0,p['col']-c0]); valid=math.isfinite(v) and v>=0 and v!=fill
                    assert valid==p['observed_available']
                    p['radiance']=v if valid else None
            p=groups[(event,day,'pentagon_broad')][len(groups[(event,day,'pentagon_broad')])//2]
            a={}
            for name in ['Sensor_Zenith','Lunar_Zenith','Moon_Illumination_Fraction']:
                d=f1[GROUP][name]; raw=float(d[p['row'],p['col']]);scale=float(np.asarray(d.attrs['scale_factor']).flat[0]);offset=float(np.asarray(d.attrs['add_offset']).flat[0]); a[name]=raw*scale+offset
            ancillary.append({'event':event,'date_utc':day,'sample_cell':list(key(p)),**a})
        broad=groups[(event,day,'pentagon_broad')]
        for rid,box in boxes.items():
            subset=[]
            for p in broad:
                weight=intersect_weight(p,box)
                if weight>0: subset.append({**p,'region':rid,'area_km2':weight})
            assert math.isclose(sum(p['area_km2'] for p in subset),float(area(*box)),rel_tol=1e-10)
            groups[(event,day,rid)]=subset
        corekeys={key(p) for p in groups[(event,day,'core_500m')]}
        groups[(event,day,'surround_disjoint')]=[{**p,'region':'surround_disjoint'} for p in broad if key(p) not in corekeys]
        assert not corekeys&{key(p) for p in groups[(event,day,'surround_disjoint')]}
        for rid in [r['id'] for r in cfg['regions']]+['core_500m','core_1000m','surround_disjoint']:
            ps=groups[(event,day,rid)]
            for scenario in SCENARIOS:
                st=stats(ps,lambda p:good(p,scenario)); records.append({'event':event,'date_utc':day,'region':rid,'scenario':scenario,**st})
                if rid in [r['id'] for r in cfg['regions']]:
                    previous=next(r for r in old['regional_results'] if (r['event'],r['date_utc'],r['region'])==(event,day,rid))
                    assert abs(st['coverage']-previous['coverage'][scenario])<1e-12
        core=stats(groups[(event,day,'core_500m')],lambda p:good(p,'both_relaxations'))
        ring=stats(groups[(event,day,'surround_disjoint')],lambda p:good(p,'both_relaxations'))
        contrasts.append({'event':event,'date_utc':day,'core_coverage':core['coverage'],'surround_coverage':ring['coverage'],'core_to_surround_ratio':core['mean_if_75pct']/ring['mean_if_75pct'] if core['mean_if_75pct'] is not None and ring['mean_if_75pct'] else None})
        if event=='iran_june_2025':
            for flag in [0,16]:
                selection.append({'event':event,'date_utc':day,'a1_flag':flag,**stats(broad,lambda p:good(p,'allow_a1_straylight_only') and p['a1_qf_dnb']==flag)})
    pairs=[]
    for event in sorted({e for e,d in all_dates}):
        days=sorted(d for e,d in all_dates if e==event)
        for earlier,later in combinations(days,2):
            for scenario in SCENARIOS:
                reg=[]
                for rid in [r['id'] for r in cfg['regions']]+['core_500m','core_1000m','surround_disjoint']:
                    before={key(p):p for p in groups[(event,earlier,rid)]};after={key(p):p for p in groups[(event,later,rid)]}
                    assert before.keys()==after.keys()
                    ks=[k for k in before if good(before[k],scenario) and good(after[k],scenario)]
                    denom=math.fsum(p['area_km2'] for p in before.values()); valid=math.fsum(before[k]['area_km2'] for k in ks)
                    a=math.fsum(before[k]['area_km2']*before[k]['radiance'] for k in ks)/valid if valid else None
                    b=math.fsum(before[k]['area_km2']*after[k]['radiance'] for k in ks)/valid if valid else None
                    cov=valid/denom
                    reg.append({'region':rid,'common_coverage':cov,'common_cells':len(ks),'earlier_mean':a,'later_mean':b,'change_pct_subset':100*(b/a-1) if a else None,'change_pct_if_75pct':100*(b/a-1) if a and cov>=.75 else None})
                controls=[r['change_pct_if_75pct'] for r in reg if r['region'] in ['rosslyn_commercial','reston_town_center','tysons_commercial'] and r['change_pct_if_75pct'] is not None]
                targetrow=next(r for r in reg if r['region']=='pentagon_broad')
                eligible=targetrow['change_pct_if_75pct'] is not None and len(controls)>=2
                median=float(np.median(controls)) if len(controls)>=2 else None
                for r in reg:
                    r['relative_to_controls_pp']=r['change_pct_if_75pct']-median if eligible and r['change_pct_if_75pct'] is not None else None
                pairs.append({'event':event,'earlier':earlier,'later':later,'scenario':scenario,'broad_pair_pass':eligible,'n_controls':len(controls),'control_median_change_pct':median,'regions':reg})
    injection=None
    for event,day in all_dates:
        core=stats(groups[(event,day,'core_500m')],lambda p:good(p,'both_relaxations'))
        broad=groups[(event,day,'pentagon_broad')];st=stats(broad,lambda p:good(p,'both_relaxations'))
        if core['coverage']<.75 or st['coverage']<.75: continue
        ks={key(p) for p in groups[(event,day,'core_500m')]}
        chosen=[p for p in broad if good(p,'both_relaxations')]
        total=math.fsum(p['area_km2']*p['radiance'] for p in chosen)
        affected=math.fsum(p['area_km2']*p['radiance'] for p in chosen if key(p) in ks)
        injection={'event':event,'date_utc':day,'interpretation':'optimistic whole-mixed-cell perturbation; not building or worker sensitivity','core_intersecting_cells':len(ks),'share_of_valid_broad_weighted_light':affected/total,'tests':[{'injected_core_cells_pct':pct,'broad_mean_change_pct':pct*affected/total} for pct in [10,25,50,100]]}
        break
    event,day=all_dates[0];core=groups[(event,day,'core_500m')]
    rr=[p['row'] for p in core];cc=[p['col'] for p in core];half=1/480
    union=[-80+min(cc)/240-half,40-max(rr)/240-half,-80+max(cc)/240+half,40-min(rr)/240+half]
    geom={'centre_lon_lat':[x,y],'boxes':boxes,'core_cell_count':len(core),'core_cell_keys':[list(key(p)) for p in core],'core_union_bbox':union,'core_union_area_km2':float(area(*union)),'nominal_core_area_km2':float(area(*boxes['core_500m'])),'radiance_unit':'nW cm^-2 sr^-1'}
    output={'stage':'exploratory_brightness_followup_not_anomaly_backtest','protocol_sha256':pre['files']['FOLLOWUP_PROTOCOL.md'],'source_quality_extract_sha256':source_sha,'geometry':geom,'regional_stats':records,'within_event_pairs':pairs,'core_surround_contrasts':contrasts,'june_flag_subset_selection':selection,'synthetic_injection':injection,'ancillary_sample':ancillary}
    write('followup_results.json',output)
    write('followup_pixel_values.json',[p for ps in groups.values() for p in ps])
    print('GEOMETRY',json.dumps(geom));print('CONTRASTS',json.dumps(contrasts));print('INJECTION',json.dumps(injection))
    for p in pairs:
        if p['broad_pair_pass']: print('PAIR',json.dumps(p))
    print('SELECTION',json.dumps(selection))

if __name__=='__main__': main()
