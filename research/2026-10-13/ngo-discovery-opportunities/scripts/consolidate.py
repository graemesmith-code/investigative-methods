#!/usr/bin/env python3
"""Conservative consolidation; original team records remain authoritative."""
import csv,datetime,hashlib,json,re
from collections import Counter,defaultdict
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit
ROOT=Path(__file__).resolve().parents[1]
START=datetime.date(2016,10,13); END=datetime.date(2026,10,13)
ORGS=['Global Witness','Global Financial Integrity','OCCRP','Tax Justice Network','Public Eye','Spotlight on Corruption','The Sentry','Sherpa','C4ADS','Basel Institute on Governance','Natural Resource Governance Institute','Open Ownership','Transparency International','PPLAAF','AntAC']
ALIASES={'GFI':'Global Financial Integrity','TJN':'Tax Justice Network','NRGI':'Natural Resource Governance Institute','Organized Crime and Corruption Reporting Project':'OCCRP','Basel Institute':'Basel Institute on Governance','Ukraine AntAC':'AntAC','Anti-Corruption Action Centre':'AntAC','Anti-Corruption Action Center':'AntAC','Platform to Protect Whistleblowers in Africa':'PPLAAF'}
def canon(u):
 s=urlsplit(u);return urlunsplit((s.scheme.lower(),s.netloc.lower(),s.path.rstrip('/'),s.query,''))
def datescope(row):
 d=row.get('date') or row.get('publication_date')
 if not d:return 'unknown'
 d=str(d).strip()
 try:
  if re.fullmatch(r'\d{4}',d):
   y=int(d);return 'in_window' if 2017<=y<=2025 else ('outside_window' if y<2016 or y>2026 else 'boundary_uncertain')
  if re.fullmatch(r'\d{4}-\d{2}',d):
   y,m=map(int,d.split('-'));lo=datetime.date(y,m,1);hi=datetime.date(y+int(m==12),(m%12)+1,1)-datetime.timedelta(days=1)
   return 'in_window' if START<=lo and hi<=END else ('outside_window' if hi<START or lo>END else 'boundary_uncertain')
  try:date=datetime.date.fromisoformat(d[:10])
  except ValueError:
   date=None
   for f in ['%d %B %Y','%d %b %Y','%B %d, %Y','%b %d, %Y','%d/%m/%Y','%Y/%m/%d']:
    try:date=datetime.datetime.strptime(d,f).date();break
    except ValueError:pass
   if date is None:return 'unparsed'
  return 'in_window' if START<=date<=END else 'outside_window'
 except (ValueError,TypeError):return 'unparsed'
def main():
 rows=[];duplicates=[];seen={};supporting=[]
 for f in sorted(ROOT.glob('teams/*/inventory*.jsonl')):
  # Use canonical inventory when both split and merged versions exist.
  if f.name!='inventory.jsonl' and (f.parent/'inventory.jsonl').exists():continue
  for line_no,line in enumerate(f.open(),1):
   if not line.strip():continue
   r=json.loads(line);r['original_inventory']=str(f.relative_to(ROOT));r['original_line']=line_no
   r['org']=ALIASES.get(r.get('org'),r.get('org'))
   if r['org'] not in ORGS or r.get('eligible_corpus') is False or r.get('ngo_corpus_record') is False:
    supporting.append(r);continue
   u=r.get('canonical_report_url') or r.get('duplicate_of') or r.get('url','');key=(r['org'],canon(u));r['source_id']='SRC-'+hashlib.sha256((str(r['org'])+'|'+canon(u)).encode()).hexdigest()[:14]
   r['date_scope']=datescope(r)
   r['source_type']=r.get('source_type',r.get('type','unknown'))
   status=str(r.get('acquisition_status','')).lower()
   full=r.get('fulltext_acquired',r.get('fulltext_available'))
   if full is None:full=bool((r.get('report_sha256') or r.get('text_chars') or 'pdf_acquired' in status or 'fulltext_acquired' in status) and 'failed' not in status)
   r['underlying_fulltext_acquired']=bool(full)
   r['context_screened']=bool(r.get('fulltext_screened') or r.get('context_screened') or r.get('contextually_screened'))
   r['complete_fulltext_screened']=bool(r['context_screened'] and r['underlying_fulltext_acquired'])
   r['deeply_read']=bool(r.get('deeply_read'))
   r['retained_finalist']=bool(r.get('retained_finalist',False))
   if key in seen:
    previous=seen[key]
    duplicates.append(dict(source_id=r['source_id'],duplicate_inventory=r['original_inventory'],duplicate_line=line_no,retained_inventory=previous['original_inventory'],retained_line=previous['original_line'],reason='same work canonical URL, explicit translation mirror, or report PDF version'))
    previous.setdefault('source_versions',[]).append(r)
    for field in ['underlying_fulltext_acquired','context_screened','complete_fulltext_screened','deeply_read','retained_finalist']:
     previous[field]=previous[field] or r[field]
    previous['opportunity_ids']=sorted(set(previous.get('opportunity_ids',[])+r.get('opportunity_ids',[])))
    if r['context_screened']:
     previous['latest_screening_rationale']=r['screening_rationale'];previous['latest_read_inventory']=r['original_inventory'];previous['latest_read_line']=r['original_line']
    if previous['date_scope']!='in_window' and r['date_scope']=='in_window':previous['date']=r['date'];previous['date_scope']='in_window';previous['date_source_version']=r['url']
    continue
   seen[key]=r
   rows.append(r)
 machine=[]
 for mf in sorted(ROOT.glob('teams/*/machine-screen.jsonl')):
  for line in mf.open():
   if not line.strip():continue
   m=json.loads(line);org=ALIASES.get(m['org'],m['org']);u=m.get('canonical_source_url') or m.get('canonical_url') or m.get('url')
   m['normalized_org']=org;m['normalized_source_url']=u;m['original_machine_ledger']=str(mf.relative_to(ROOT))
   key=(org,canon(u));m['source_id']=seen[key]['source_id'] if key in seen else None
   if key in seen:seen[key]['machine_screened']=True
   machine.append(m)
 shared='Insights from the United Kingdom’s People with Significant Control register'
 for r in rows:
  r['machine_screened']=bool(r.get('machine_screened'))
  r['cross_org_work_id']='COAUTHORED-UK-PSC-2025' if r['title']==shared else r['source_id']
 selection=json.loads((ROOT/'opportunity-manifest.json').read_text())
 retained_ids=set(s for o in selection.get('pilot_ready',[]) for s in o.get('source_ids',[]))
 for r in rows:r['retained_pilot_source']=r['source_id'] in retained_ids
 (ROOT/'supporting-source-inventory.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in supporting))
 (ROOT/'machine-screen-inventory.jsonl').write_text(''.join(json.dumps(m,ensure_ascii=False)+'\n' for m in machine))
 (ROOT/'source-inventory.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
 (ROOT/'annexes/consolidation-duplicates.json').write_text(json.dumps(duplicates,indent=2,ensure_ascii=False)+'\n')
 counts=[]
 for org in ORGS:
  rr=[r for r in rows if r['org']==org]
  counts.append(dict(org=org,enumerated=len(rr),date_recorded_in_window=sum(r['date_scope']=='in_window' for r in rr),date_unverified_or_boundary=sum(r['date_scope'] not in ('in_window','outside_window') for r in rr),outside_window=sum(r['date_scope']=='outside_window' for r in rr),fulltext_acquired=sum(r['underlying_fulltext_acquired'] for r in rr),machine_screened=sum(r['machine_screened'] for r in rr),context_screened=sum(r['context_screened'] for r in rr),complete_fulltext_screened=sum(r['complete_fulltext_screened'] for r in rr),deeply_read=sum(r['deeply_read'] for r in rr),retained_finalist_sources=sum(r['retained_finalist'] for r in rr),retained_pilot_sources=sum(r['retained_pilot_source'] for r in rr)))
 for count in counts:count.pop('retained_finalist_sources',None)
 (ROOT/'coverage-counts.json').write_text(json.dumps(counts,indent=2)+'\n')
 with (ROOT/'coverage-counts.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(counts[0]),lineterminator="\n");w.writeheader();w.writerows(counts)
 unknown=Counter(r['org'] for r in rows if r['org'] not in ORGS)
 totals={k:sum(r[k] for r in counts) for k in counts[0] if k!='org'}
 totals.update(unique_works=len(set(r['cross_org_work_id'] for r in rows)),unique_context_screened_works=len(set(r['cross_org_work_id'] for r in rows if r['context_screened'])),unique_deeply_read_works=len(set(r['cross_org_work_id'] for r in rows if r['deeply_read'])),machine_text_files=len(machine),machine_unmatched_records=sum(m['source_id'] is None for m in machine))
 totals.update(pilot_ready_opportunities=len(selection.get('pilot_ready',[])),conditional_opportunities=len(selection.get('conditional_opportunities',[])),supporting_external_records=len(supporting),unique_retained_pilot_source_works=len(set(r['cross_org_work_id'] for r in rows if r['retained_pilot_source'])))
 (ROOT/'totals.json').write_text(json.dumps(totals,indent=2)+'\n')
 print(json.dumps(dict(total_records=len(rows),duplicate_urls=len(duplicates),unknown_orgs=dict(unknown),counts=counts),indent=2))
if __name__=='__main__':main()
