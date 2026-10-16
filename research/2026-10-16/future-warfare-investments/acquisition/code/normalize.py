#!/usr/bin/env python3
"""Stream CSV/ZIP, validate raw schemas, retain bounded security records and normalized Parquet."""
import collections,csv,datetime,gzip,hashlib,io,json,pathlib,re,sys,zipfile
from decimal import Decimal,InvalidOperation
import pyarrow as pa,pyarrow.parquet as pq
from acquire import ROOT,DATA,save_json
csv.field_size_limit(20_000_000)
TERMS={'hypersonic':r'hyper[- ]?sonic','quantum':r'quantum|qubit','autonomy_drones':r'autonom|unmanned|uncrewed|\bUAS\b|\bUAV\b|drone|swarm','sensors':r'sensor|radar|lidar|infrared|photon|electro.optic','cyber':r'cyber|cryptograph|zero.trust','space':r'satellite|spacecraft|orbital|\bPNT\b|space domain','logistics':r'logistic|contested|supply.chain|additive manufactur|power.beam','communications_ew':r'electronic warfare|spectrum|radio.frequency|tactical network|communications','ai':r'artificial intelligence|machine learning|neural network'}
def digest(x):return hashlib.sha256(x.encode()).hexdigest()
def tags(t):return [k for k,v in TERMS.items() if re.search(v,t,re.I)]
def iso(s):
 for fmt in ['%Y-%m-%d','%m/%d/%Y','%m/%d/%Y %H:%M:%S','%m%d%Y']:
  try:return datetime.datetime.strptime(s[:19],fmt).date().isoformat()
  except ValueError:pass
 return None
def money(s):
 try:return str(Decimal(s.replace(',','').replace('$','').strip())) if s.strip() else None
 except InvalidOperation:return None
class Writer:
 def __init__(self,name):
  self.name=name;self.path=DATA/'normalized'/f'{name}.jsonl.gz';self.path.parent.mkdir(exist_ok=True);self.f=gzip.open(self.path,'wt');self.buf=[];self.pq=None
 def write(self,r):
  self.f.write(json.dumps(r,ensure_ascii=False)+'\n');self.buf.append(r)
  if len(self.buf)>=5000:self.flush()
 def flush(self):
  if not self.buf:return
  # All top-level scalar types are fixed by canonical_record; JSON strings carry nested structures.
  t=pa.Table.from_pylist(self.buf,schema=SCHEMA)
  if self.pq is None:self.pq=pq.ParquetWriter(DATA/'normalized'/f'{self.name}.parquet',SCHEMA,compression='zstd')
  self.pq.write_table(t);self.buf=[]
 def close(self):
  self.flush();self.f.close()
  if self.pq:self.pq.close()
SCHEMA=pa.schema([(k,pa.string()) for k in ['document_id','source','source_record_id','source_url','raw_locator','award_key','transaction_key','entity_key','entity_name','title','text','action_date','fiscal_year','capability_tags','eligibility','money_json','evidence_excerpt','retrieved_at','identifiers_json','record_sha256','source_snapshot_sha256']])
def record(**kwargs):return {k:kwargs.get(k) for k in SCHEMA.names}
def profile(rows,fields):
 return {'rows':rows,'fields':fields}
def snapshot_metadata(path,manifest):
 relative=str(path.relative_to(DATA))
 matches=[m for m in manifest if m.get('outcome')=='downloaded' and m.get('relative_path')==relative]
 if not matches:raise ValueError('No exact-file snapshot metadata: '+relative)
 hashes={m['sha256'] for m in matches}
 if len(hashes)!=1:raise ValueError('Conflicting snapshot metadata: '+relative)
 m=matches[-1]
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 if h.hexdigest()!=m['sha256']:raise ValueError('Raw snapshot checksum mismatch: '+relative)
 return m
def analyze(source):
 p=DATA/'raw'/source; files=list(p.glob('*.csv'))+list(p.glob('*.zip'))
 if not files:raise ValueError('No CSV/ZIP payloads for '+source)
 counts=collections.Counter();missing=collections.Counter();dates=collections.defaultdict(list);years=collections.Counter();agencies=collections.Counter();seen=set();dups=0;samples=[];schema=[];moneyfields=[];idfields=[];retained=0;selected_years=collections.Counter();selected_missing=collections.Counter();selected_seen=set();selected_dups=0;selected_dates=[];rawhash=hashlib.sha256();sourceurl='';retrieved=None;snapshothash=None
 manifest=[json.loads(line) for line in (ROOT/'validation/http_manifest.jsonl').read_text().splitlines()]
 # Bind every row to its exact file, never the last source-level manifest entry.
 snapshots={str(path):snapshot_metadata(path,manifest) for path in files}
 w=Writer(source)
 for path in files:
  m=snapshots[str(path)];sourceurl=m['url'];retrieved=m['retrieved_at'];snapshothash=m['sha256']
  if path.suffix=='.zip':
   z=zipfile.ZipFile(path);save_json(ROOT/'validation'/f'{source}_zip_inventory.json',[{'name':x.filename,'compressed':x.compress_size,'uncompressed':x.file_size} for x in z.infolist()]);streams=[(n,io.TextIOWrapper(z.open(n),encoding='utf-8-sig',errors='replace',newline='')) for n in z.namelist() if n.endswith('.csv') and ('PrimeTransactions' in n)]
  else:streams=[(path.name,path.open(encoding='utf-8-sig',errors='replace',newline=''))]
  for member,f in streams:
   reader=csv.DictReader(f);schema=reader.fieldnames
   if source.startswith('sbir'):idfields=['Agency Tracking Number','Contract','Duns','UEI'];moneyfields=['Award Amount']
   else:
    idfields=[k for k in schema if k in ['contract_transaction_unique_key','contract_award_unique_key','award_id_piid','award_id_fain','award_id_uri','recipient_uei','recipient_duns','assistance_transaction_unique_key','assistance_award_unique_key']]
    moneyfields=[k for k in schema if any(a in k for a in ['obligat','outlay','value','loan','subsidy','non_federal_funding','total_funding']) and not k.endswith('_code')]
   for i,r in enumerate(reader,1):
    counts[f'{path.name}:{member}' if len(files)>1 else member]+=1
    for k in schema:
     if not (r.get(k) or '').strip():missing[k]+=1
    rowjson=json.dumps(r,sort_keys=True);h=digest(rowjson);rawhash.update((h+'\n').encode())
    if h in seen:dups+=1
    seen.add(h)
    if source.startswith('sbir'):
     year=r.get('Award Year','');dt=iso(r.get('Proposal Award Date',''));ag=r.get('Agency','');text=r.get('Abstract','');title=r.get('Award Title','');identity='|'.join(r.get(k,'') for k in ['Agency','Branch','Program','Phase','Agency Tracking Number','Contract','Award Year']);award=r.get('Contract','');ent=r.get('UEI') or r.get('Duns');entity=r.get('Company');key=None
     keep=year in [str(x) for x in range(2019,2027)] and ('defense' in ag.lower() or 'war' in ag.lower() or ('energy' in ag.lower() and tags(title+' '+text)))
     monies={'award_amount':{'value':money(r.get('Award Amount','')),'unit':'USD','meaning':'reported SBIR/STTR award amount; not transaction obligation, outlay or total lifecycle funding'}}
     link='https://www.sbir.gov/awards';eligibility='security_agency_candidate' if 'defense' in ag.lower() or 'war' in ag.lower() else 'mission_review_required'
    else:
     dt=iso(r.get('action_date',''));year=r.get('action_date_fiscal_year','') or (str(int(dt[:4])+(int(dt[5:7])>=10)) if dt else '');ag=r.get('awarding_sub_agency_name','');text=r.get('transaction_description','') or r.get('prime_award_base_transaction_description','');title=r.get('prime_award_base_transaction_description','');award=r.get('contract_award_unique_key','') or r.get('assistance_award_unique_key','');key=r.get('contract_transaction_unique_key','') or r.get('assistance_transaction_unique_key','');identity=key or h;ent=r.get('recipient_uei') or r.get('recipient_duns');entity=r.get('recipient_name');keep=True;monies={k:money(r.get(k,'')) for k in moneyfields};link=r.get('usaspending_permalink','') or 'https://www.usaspending.gov/award/'+award;eligibility='security_agency_candidate'
    years[year]+=1;agencies[ag]+=1
    if dt:dates['action_or_performance_start'].append(dt)
    if not keep:continue
    retained+=1;selected_years[year]+=1
    if dt:selected_dates.append(dt)
    for k in idfields:
     if not r.get(k):selected_missing[k]+=1
    sid=identity
    if sid in selected_seen:selected_dups+=1
    selected_seen.add(sid)
    out=record(document_id=source+':'+digest(identity+'|'+h),source=source,source_record_id=sid,source_url=link,raw_locator=f'{path.name}:{member}:data_row={i}',award_key=award,transaction_key=key,entity_key=ent,entity_name=entity,title=title,text=text,action_date=dt,fiscal_year=year,capability_tags=json.dumps(tags(title+' '+text)),eligibility=eligibility,money_json=json.dumps(monies),evidence_excerpt=text[:650],retrieved_at=retrieved,record_sha256=h,source_snapshot_sha256=snapshothash,identifiers_json=json.dumps({k:r.get(k) for k in (['Agency','Branch','Program','Phase','Agency Tracking Number','Contract','UEI','Duns','Topic Code','Solicitation Number','Award Year'] if source.startswith('sbir') else idfields+['parent_award_agency_id','parent_award_id_piid','awarding_agency_code','awarding_sub_agency_code','funding_agency_code','funding_sub_agency_code','product_or_service_code','naics_code','solicitation_identifier','cfda_number'])}))
    w.write(out)
    if len(samples)<8 and tags(title+' '+text):samples.append(out)
   f.close()
 w.close();total=sum(counts.values())
 result={'source':source,'raw_file_rows':dict(counts),'raw_rows':total,'retained_rows':retained,'raw_year_counts':dict(sorted(years.items())),'retained_year_counts':dict(sorted(selected_years.items())),'agency_counts':dict(agencies),'date_ranges':{k:{'min':min(v),'max':max(v),'valid_count':len(v)} for k,v in dates.items() if v},'exact_raw_duplicate_rows':dups,'retained_duplicate_source_ids':selected_dups,'retained_id_missing':dict(selected_missing),'id_missing_raw':{k:(missing[k] if k in schema else total) for k in idfields},'absent_id_columns':[k for k in idfields if k not in schema],'retained_date_range':{'min':min(selected_dates) if selected_dates else None,'max':max(selected_dates) if selected_dates else None,'valid_count':len(selected_dates)},'all_field_missing_raw':dict(missing),'columns':schema,'money_fields':moneyfields,'logical_rows_sha256':rawhash.hexdigest(),'note':'Rows preserve duplicates; document IDs may repeat where source identity repeats. Inspect differences before deduplication. Counts describe retrieved snapshot, not universe completeness.'}
 save_json(ROOT/'validation'/f'{source}_profile.json',result)
 with (ROOT/'samples'/f'{source}.jsonl').open('w') as f:
  for r in samples:f.write(json.dumps(r,ensure_ascii=False)+'\n')
 print(json.dumps({k:result[k] for k in ['source','raw_rows','retained_rows','retained_year_counts','date_ranges','id_missing_raw','retained_duplicate_source_ids']}))
if __name__=='__main__':analyze(sys.argv[1])
