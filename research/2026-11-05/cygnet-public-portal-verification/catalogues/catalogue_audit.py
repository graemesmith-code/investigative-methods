#!/usr/bin/env python3
"""Fetch/audit public AGS and NRCan earthquake records. Standard library only.
Keep --out private. Operational chronology is optional external CSV, never bundled.
"""
import argparse,csv,datetime as dt,hashlib,json,math,pathlib,urllib.parse,urllib.request,xml.etree.ElementTree as ET

def read_csv(path):
    with open(path,newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def write_csv(path,rows,fields):
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def when(s):return dt.datetime.fromisoformat(s.replace('Z','+00:00')).replace(tzinfo=None)
def distance(a,b):
    la,lo,lb,lob=map(math.radians,(*a,*b));return 6371.0088*2*math.asin(math.sqrt(math.sin((la-lb)/2)**2+math.cos(la)*math.cos(lb)*math.sin((lo-lob)/2)**2))
def digest(b):return hashlib.sha256(b).hexdigest()
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',required=True,type=pathlib.Path,help='Private output directory; never the source-code directory')
    p.add_argument('--input',type=pathlib.Path,help='Offline directory containing the saved raw responses; no network requests')
    p.add_argument('--operations',type=pathlib.Path,help='Private CSV: log_number,start_mst,end_mst,interval_semantics,source_basis; times conditionally assumed MST')
    p.add_argument('--start',required=True);p.add_argument('--end',required=True)
    p.add_argument('--bbox',nargs=4,type=float,required=True,metavar=('S','W','N','E'))
    p.add_argument('--pad',nargs=2,type=float,required=True);p.add_argument('--toe',nargs=2,type=float,required=True);p.add_argument('--radius-km',type=float,default=15)
    p.add_argument('--association-seconds',type=float,default=600,help='Audit screening only, not a scientific matching criterion')
    args=p.parse_args();out=args.out.resolve()
    if out==pathlib.Path(__file__).resolve().parent:p.error('--out must not be the source-code directory')
    out.mkdir(parents=True,exist_ok=True);log=[]
    def acquire(name,url,params):
        full=url+'?'+urllib.parse.urlencode(params);beg=dt.datetime.now(dt.timezone.utc).isoformat()
        if args.input:
            path=args.input/name;b=path.read_bytes();status=None;mode='offline copy';source=str(path.resolve())
        else:
            req=urllib.request.Request(full,headers={'User-Agent':'PublicCatalogueAudit/1.0'})
            with urllib.request.urlopen(req,timeout=90) as r:b=r.read();status=r.status
            mode='http';source=full
        (out/name).write_bytes(b)
        log.append(dict(file=name,mode=mode,source=source,query_url=full,parameters=params,started_utc=beg,completed_utc=dt.datetime.now(dt.timezone.utc).isoformat(),http_status=status,bytes=len(b),sha256=digest(b)))
        (out/'audit_access_log.json').write_text(json.dumps(log,indent=2))
        return b
    s,w,n,e=args.bbox
    where=f"Datetime_UTC >= '{args.start}' AND Datetime_UTC < '{args.end.replace('T',' ')}' AND Latitude >= {s} AND Latitude <= {n} AND Longitude >= {w} AND Longitude <= {e}"
    base='https://services2.arcgis.com/jQV6VMr2Loovu7GU/arcgis/rest/services/Alberta_Earthquakes_view/FeatureServer/0'
    raw=json.loads(acquire('ags_bbox.json',base+'/query',dict(f='json',where=where,outFields='*',returnGeometry='false',orderByFields='Datetime_UTC',resultRecordCount=1000)))
    count=json.loads(acquire('ags_count.json',base+'/query',dict(f='json',where=where,returnCountOnly='true')))['count']
    ids=json.loads(acquire('ags_ids.json',base+'/query',dict(f='json',where=where,returnIdsOnly='true')))['objectIds']
    acquire('ags_layer_verified.json',base,dict(f='json'))
    acquire('ags_item_verified.json','https://www.arcgis.com/sharing/rest/content/items/917f3e88b81b45edb18ab29ecd7f1a37',dict(f='json'))
    ags=[x['attributes'] for x in raw['features']]
    if raw.get('exceededTransferLimit') or len(ags)!=count or set(ids)!={x['object_id'] for x in ags}:
        raise RuntimeError('AGS retrieval incomplete; stop rather than silently publish truncated results. Split the query into smaller time windows.')
    ep='https://www.earthquakescanada.nrcan.gc.ca/fdsnws/event/1/query'
    params=dict(starttime=args.start,endtime=args.end,minlatitude=s,maxlatitude=n,minlongitude=w,maxlongitude=e)
    txt=acquire('nrcan_bbox_final.txt',ep,dict(params,format='text')).decode('utf-8')
    xml=acquire('nrcan_bbox_final.xml',ep,dict(params,includeallorigins='true',includeallmagnitudes='true',includearrivals='true'))
    text_rows=list(csv.DictReader(txt.splitlines(),delimiter='|'));text_by_id={x['#EventID']:x for x in text_rows}
    for a in ags:
        a.update(pad_distance_km=round(distance((a['Latitude'],a['Longitude']),args.pad),4),toe_distance_km=round(distance((a['Latitude'],a['Longitude']),args.toe),4),time_uncertainty_s='',horizontal_uncertainty_km='',depth_uncertainty_km='',magnitude_uncertainty='')
        a['within_union_radius']=min(a['pad_distance_km'],a['toe_distance_km'])<=args.radius_km
    ags=[a for a in ags if a['within_union_radius']]
    nr=[];ns={'q':'http://quakeml.org/xmlns/bed/1.2'}
    for ev in ET.fromstring(xml).findall('.//q:event',ns):
        def t(path):return ev.findtext(path,default='',namespaces=ns)
        ident=ev.attrib['publicID'];textrow=text_by_id[ident.rsplit('/',1)[-1]]
        lat=float(t('q:origin/q:latitude/q:value'));lon=float(t('q:origin/q:longitude/q:value'))
        a=dict(source_id=ident,origin_utc=t('q:origin/q:time/q:value'),latitude=lat,longitude=lon,depth_text_km=textrow['Depth/km'],depth_xml_raw=t('q:origin/q:depth/q:value'),depth_type=t('q:origin/q:depthType'),magnitude=t('q:magnitude/q:mag/q:value'),magnitude_type=t('q:magnitude/q:type'),event_type=t('q:type'),type_certainty=t('q:typeCertainty'),creation_time=t('q:origin/q:creationInfo/q:creationTime'),time_uncertainty_s=t('q:origin/q:time/q:uncertainty'),horizontal_uncertainty_km='',depth_uncertainty_km='',magnitude_uncertainty=t('q:magnitude/q:mag/q:uncertainty'),pad_distance_km=round(distance((lat,lon),args.pad),4),toe_distance_km=round(distance((lat,lon),args.toe),4))
        a['xml_standard_metres_vs_text_km_consistent']=math.isclose(float(a['depth_xml_raw'])/1000,float(a['depth_text_km']),abs_tol=1e-9)
        if min(a['pad_distance_km'],a['toe_distance_km'])<=args.radius_km:nr.append(a)
    if not ags or not nr:raise RuntimeError('This audit expects nonempty catalogues; raw responses retained. Adapt explicitly for empty-data investigations.')
    write_csv(out/'ags_events.csv',ags,list(ags[0]));write_csv(out/'nrcan_events.csv',nr,list(nr[0]))
    pairs=[]
    for a in nr:
        b=min(ags,key=lambda b:abs((when(a['origin_utc'])-when(b['Datetime_UTC'])).total_seconds()))
        secs=(when(a['origin_utc'])-when(b['Datetime_UTC'])).total_seconds();km=distance((a['latitude'],a['longitude']),(b['Latitude'],b['Longitude']))
        pairs.append(dict(NRCan_id=a['source_id'],AGS_object_id=b['object_id'],AGS_EDGE_Id=b['EDGE_Id'],NRCan_UTC=a['origin_utc'],AGS_UTC=b['Datetime_UTC'],NRCan_minus_AGS_seconds=secs,epicentre_separation_km=round(km,4),NRCan_magnitude=a['magnitude'],NRCan_magnitude_type=a['magnitude_type'],AGS_MLy=b['MLy'],industry_M=b['M'],status='probable same event; no shared identifier' if abs(secs)<=10 and km<=5 else 'nearest record only; not a verified pair'))
    write_csv(out/'cross_catalogue_pairs.csv',pairs,list(pairs[0]))
    recon=[];matched=set()
    for a in read_csv(args.operations) if args.operations else []:
        utc=when(a['start_mst'])+dt.timedelta(hours=7);end=(when(a['end_mst'])+dt.timedelta(hours=7)) if a.get('end_mst') else None
        b=min(ags,key=lambda b:abs((utc-when(b['Datetime_UTC'])).total_seconds()));secs=(utc-when(b['Datetime_UTC'])).total_seconds();stage=a.get('interval_semantics')=='stage_with_undated_delay'
        assessment='stage interval with undated seismic delay; no distinct new event established' if stage else ('plausible time association; not proof of causation' if abs(secs)<args.association_seconds else 'no close catalogue-time match; nearest event is not an identification')
        if a.get('source_basis')=='nominated_catalogue_origin':
            assessment='nominated catalogue origin, not independent report detection time; cross-catalogue agreement is not log corroboration'
        if not stage and abs(secs)<args.association_seconds:matched.add(b['object_id'])
        recon.append(dict(log_number=a['log_number'],operational_start_MST=a['start_mst'],operational_end_MST=a.get('end_mst',''),interval_semantics=a.get('interval_semantics',''),source_basis=a.get('source_basis','unverified supplied chronology'),clock_basis='MST assumed, not established by source',operational_start_UTC=utc.isoformat()+'Z',operational_end_UTC=end.isoformat()+'Z' if end else '',nearest_AGS_object_id=b['object_id'],nearest_AGS_origin_UTC=b['Datetime_UTC'],operational_start_minus_origin_seconds=secs,AGS_MLy=b['MLy'],industry_M=b['M'],EDGE_id=b['EDGE_Id'],assessment=assessment,catalogue_origins_inside_interval=sum(utc<=when(x['Datetime_UTC'])<=end for x in ags) if end else ''))
    fields=list(recon[0]) if recon else ['log_number','assessment']
    write_csv(out/'operational_reconciliation.csv',recon,fields)
    unmatched=[a for a in ags if a['object_id'] not in matched];write_csv(out/'catalogue_events_without_close_operational_entry.csv',unmatched,list(ags[0]))
    summary=dict(ags_bbox_count=count,ags_radius_count=len(ags),nrcan_radius_count=len(nr),probable_cross_catalogue_pairs=sum(x['status'].startswith('probable') for x in pairs),operational_rows=len(recon),unmatched_ags_rows=len(unmatched),operations_supplied=bool(args.operations),radius_km=args.radius_km,warning='Source classifications and proximity do not identify operator or pad. Missing catalogue records do not prove no earthquakes. Empty uncertainties mean unavailable, not zero. Fixed MST conversion applies only to supplied chronology; not civil MDT.')
    (out/'audit_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
    files=[dict(filename=f.name,bytes=f.stat().st_size,sha256=digest(f.read_bytes())) for f in sorted(out.iterdir()) if f.is_file() and f.name!='sha256_manifest.csv']
    write_csv(out/'sha256_manifest.csv',files,['filename','bytes','sha256'])
if __name__=='__main__':main()
