"""Quality and timing assessment only. Does not calculate brightness or anomaly scores.

Primary rules are the original config/protocol. Sensitivity scenarios are post hoc
diagnostics motivated by earlier Iran quality coverage, not replacement rules.
"""
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
from zoneinfo import ZoneInfo
import h5py
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
GROUP='HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields'
NY=ZoneInfo('America/New_York')
CUTOFFS={'iran_june_2025':'2025-06-21','venezuela_jan_2026':'2026-01-02','iran_feb_2026':'2026-02-28'}
SCENARIOS={'primary':(False,False),'allow_a1_straylight_only':(True,False),'allow_medium_cloud_quality':(False,True),'both_relaxations':(True,True)}
R=6371.0088

def scalar(v): return np.asarray(v).reshape(-1)[0].item()
def dec(v): return v.decode() if isinstance(v,bytes) else str(v)
def stamp(v): return datetime.fromisoformat(dec(v)).replace(tzinfo=timezone.utc)
def area(w,s,e,n): return R**2*np.deg2rad(e-w)*(np.sin(np.deg2rad(n))-np.sin(np.deg2rad(s)))

def cells(lat,lon,bbox):
    w,s,e,n=bbox; half=1/480
    rows=np.where((lat+half>s)&(lat-half<n))[0]
    cols=np.where((lon+half>w)&(lon-half<e))[0]
    weights=np.array([[area(max(w,lon[c]-half),max(s,lat[r]-half),min(e,lon[c]+half),min(n,lat[r]+half)) for c in cols] for r in rows])
    assert np.all(weights>0) and np.isclose(weights.sum(),area(w,s,e,n),rtol=1e-10)
    return rows,cols,weights

def extract(group,name,rows,cols):
    ds=group[name]
    assert ds.shape==(2400,2400)
    return ds[rows[0]:rows[-1]+1,cols[0]:cols[-1]+1]

def main():
    cfg=json.loads((ROOT/'config.json').read_text())
    assert cfg['screen']=={'mandatory_quality_flag':0,'cloud_confidence':0,'cloud_mask_quality':3,'night_only':True,'snow_free':True,'reject_shadow_cirrus_aurora_eclipse':True,'a1_qf_dnb':0,'max_sensor_zenith_degrees':60,'min_valid_area_fraction':0.75}
    verified=json.loads((ROOT/'evidence/verified_uploads.json').read_text())
    output=[]; pixels=[]; dates=[]
    for archive in verified:
        event=archive['event']; cutoff=datetime.fromisoformat(CUTOFFS[event]).replace(tzinfo=NY)
        entries=archive['manifest']; bydate={}
        hashes={r['filename']:r['sha256'] for r in archive['files']}
        for m in entries: bydate.setdefault(m['observation_date_utc'],{})[m['product']]=m
        for day,pair in sorted(bydate.items()):
            assert set(pair)=={'VNP46A1','VNP46A2'}
            for m in pair.values():
                assert hashlib.sha256((ROOT/'raw'/m['filename']).read_bytes()).hexdigest()==hashes[m['filename']]
            with h5py.File(ROOT/'raw'/pair['VNP46A1']['filename']) as f1,h5py.File(ROOT/'raw'/pair['VNP46A2']['filename']) as f2:
                g1,g2=f1[GROUP],f2[GROUP]
                for product,f in [('VNP46A1',f1),('VNP46A2',f2)]:
                    assert dec(f.attrs['LocalGranuleID'])==pair[product]['filename']
                    assert dec(f.attrs['RangeBeginningDate'])==day
                    assert stamp(f.attrs['ProductionTime'])==datetime.fromisoformat(pair[product]['production_time_utc'])
                assert pair['VNP46A1']['filename'] in dec(f2.attrs['InputPointer']).split(',')
                lat,lon=g1['lat'][:],g1['lon'][:]
                assert lat.shape==lon.shape==(2400,)
                assert np.allclose(lat,40-np.arange(2400)/240,atol=1e-10,rtol=0)
                assert np.allclose(lon,-80+np.arange(2400)/240,atol=1e-10,rtol=0)
                assert np.array_equal(lat,g2['lat'][:]) and np.array_equal(lon,g2['lon'][:])
                assert scalar(g2['DNB_BRDF-Corrected_NTL'].attrs['scale_factor'])==1
                assert scalar(g2['DNB_BRDF-Corrected_NTL'].attrs['offset'])==0
                assert scalar(g1['UTC_Time'].attrs['scale_factor'])==1
                assert scalar(g1['Sensor_Zenith'].attrs['add_offset'])==0
                zen_scale=scalar(g1['Sensor_Zenith'].attrs['scale_factor'])
                assert np.isclose(zen_scale,.01)
                midnight=datetime.fromisoformat(day).replace(tzinfo=timezone.utc)
                record={'event':event,'date_utc':day,'cutoff_local':cutoff.isoformat(),'a1_filename':pair['VNP46A1']['filename'],'a2_filename':pair['VNP46A2']['filename'],'a1_production_utc':stamp(f1.attrs['ProductionTime']).isoformat(),'a2_production_utc':stamp(f2.attrs['ProductionTime']).isoformat(),'a2_produced_before_cutoff':stamp(f2.attrs['ProductionTime'])<cutoff,'date_pass':{}}
                region_results=[]
                for region in cfg['regions']:
                    rows,cols,weights=cells(lat,lon,region['bbox_wgs84'])
                    cm=extract(g2,'QF_Cloud_Mask',rows,cols).astype(np.int64)
                    mq=extract(g2,'Mandatory_Quality_Flag',rows,cols).astype(np.int64)
                    snow=extract(g2,'Snow_Flag',rows,cols).astype(np.int64)
                    qf=extract(g1,'QF_DNB',rows,cols).astype(np.int64)
                    zen=extract(g1,'Sensor_Zenith',rows,cols).astype(np.int64)
                    hours=extract(g1,'UTC_Time',rows,cols).astype(float)
                    radiance=extract(g2,'DNB_BRDF-Corrected_NTL',rows,cols)
                    available=np.isfinite(radiance)&(radiance>=0)&(radiance!=scalar(g2['DNB_BRDF-Corrected_NTL'].attrs['_FillValue']))
                    del radiance  # no values, means, or event rankings retained
                    timegood=np.isfinite(hours)&(hours>=0)&(hours<=24)
                    precut=np.zeros(hours.shape,dtype=bool)
                    for ij in np.ndindex(hours.shape):
                        if timegood[ij]: precut[ij]=(midnight+timedelta(hours=float(hours[ij])))<cutoff
                    zengood=(zen>=0)&(zen<=9000)&(zen*zen_scale<=60)
                    cloudknown=cm!=65535
                    common=available&(mq==0)&(snow==0)&cloudknown&((cm&1)==0)&(((cm>>6)&3)==0)&((cm&sum(1<<bit for bit in [8,9,10,12,13]))==0)&zengood&timegood&precut
                    def fraction(mask): return float(weights[mask].sum()/weights.sum())
                    masks={}; fractions={}
                    for scenario,(allow16,allowmedium) in SCENARIOS.items():
                        mask=common&(((cm>>4)&3)>= (2 if allowmedium else 3))&((qf==0)|((qf==16)&allow16))
                        masks[scenario]=mask; fractions[scenario]=fraction(mask)
                    localtimes=[(midnight+timedelta(hours=float(h))).astimezone(NY) for h in hours[timegood]]
                    result={'event':event,'date_utc':day,'region':region['id'],'role':region['role'],'cell_count':int(weights.size),'area_km2':float(weights.sum()),'coverage':fractions,'local_time_min':min(localtimes).isoformat() if localtimes else None,'local_time_max':max(localtimes).isoformat() if localtimes else None,'work_nights':sorted({(t.date()-timedelta(days=t.hour<12)).isoformat() for t in localtimes}),'diagnostic_area_fractions':{'observed_missing_or_invalid':fraction(~available),'mandatory_high_quality':fraction(mq==0),'mandatory_flag_1':fraction(mq==1),'a1_straylight_only':fraction(qf==16),'a1_flag_zero':fraction(qf==0),'cloud_quality_high':fraction(cloudknown&(((cm>>4)&3)==3)),'cloud_quality_medium':fraction(cloudknown&(((cm>>4)&3)==2)),'confidently_clear':fraction(cloudknown&(((cm>>6)&3)==0)),'probably_clear':fraction(cloudknown&(((cm>>6)&3)==1)),'confidently_cloudy':fraction(cloudknown&(((cm>>6)&3)==3)),'snow_flag':fraction(snow==1),'angle_failure':fraction(~zengood),'time_failure':fraction(~timegood),'not_pre_cutoff':fraction(~precut)}}
                    for bit,label in [(0,'daytime'),(8,'shadow'),(9,'cirrus'),(10,'cloud_mask_snow_ice'),(12,'aurora'),(13,'eclipse')]:
                        result['diagnostic_area_fractions'][label]=fraction(cloudknown&((cm&(1<<bit))!=0))
                    result['mandatory_quality_distribution']={str(v):fraction(mq==v) for v in np.unique(mq)}
                    result['cloud_mask_distribution']={str(v):fraction(cm==v) for v in np.unique(cm)}
                    region_results.append(result); output.append(result)
                    for i,j in np.ndindex(weights.shape):
                        pixels.append({'event':event,'date_utc':day,'region':region['id'],'row':int(rows[i]),'col':int(cols[j]),'area_km2':float(weights[i,j]),'cloud_mask':int(cm[i,j]),'mandatory_quality':int(mq[i,j]),'snow_flag':int(snow[i,j]),'a1_qf_dnb':int(qf[i,j]),'zenith_raw':int(zen[i,j]),'zenith_scale':zen_scale,'utc_hours':float(hours[i,j]) if np.isfinite(hours[i,j]) else None,'observed_available':bool(available[i,j]),'primary_pass':bool(masks['primary'][i,j])})
                for scenario in SCENARIOS:
                    target=next(r for r in region_results if r['role']=='target')
                    controls=sum(r['coverage'][scenario]>=.75 for r in region_results if r['role']=='comparison')
                    record['date_pass'][scenario]=target['coverage'][scenario]>=.75 and controls>=2
                dates.append(record)
    cases=[]
    for event in sorted({r['event'] for r in dates}):
        counts={s:sum(d['date_pass'][s] for d in dates if d['event']==event) for s in SCENARIOS}
        cases.append({'event':event,'eligible_dates':counts,'primary_case_status':'passes_quality_gate_only' if counts['primary']>=2 else 'unscorable','diagnostic_case_gate':{s:n>=2 for s,n in counts.items()}})
    result={'stage':'measurement_feasibility_only','brightness_anomalies_computed':False,'baseline_acquired':False,'scenarios':{s:{'allow_a1_straylight_only':v[0],'allow_medium_cloud_quality':v[1],'post_hoc':s!='primary'} for s,v in SCENARIOS.items()},'cases':cases,'dates':dates,'regional_results':output}
    (ROOT/'evidence/measurement_results.json').write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'evidence/pixel_quality_extracts.json').write_text(json.dumps(pixels,indent=2)+'\n')
    print(json.dumps(cases,indent=2))
    for r in output:
        if r['role']=='target': print(r['event'],r['date_utc'],{k:round(v*100,3) for k,v in r['coverage'].items()},r['local_time_min'])

if __name__=='__main__': main()
