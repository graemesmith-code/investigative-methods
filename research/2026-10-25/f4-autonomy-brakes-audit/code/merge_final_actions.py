#!/usr/bin/env python3
"""Compile core and six-followup ordinary FPDS actions once by full identity.
No network or money aggregation across parent/subaward schemas. Existing action
amount/date/description disagreements fail rather than being silently replaced.
"""
import csv,json,pathlib,hashlib
P=pathlib.Path(__file__).resolve().parents[1]
def key(r):return tuple(r.get(k,'') for k in ('award_key','agency_id','parent_piid','parent_agency_id','modification','transaction'))
def run():
 path=P/'evidence/fpds-verified-actions.csv';before=hashlib.sha256(path.read_bytes()).hexdigest()
 with path.open() as f:reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
 by={key(r):r for r in rows};assert len(by)==len(rows)
 follow=json.loads((P/'evidence/final-priority-live-followup.json').read_text())['fpds_actions'];added=0
 for r in follow:
  k=key(r)
  if k in by:
   assert all(str(by[k].get(x,''))==str(r.get(x,'')) for x in ('obligation_usd','signed_date','description')),'Conflicting action not overwritten'
  else:rows.append(r);by[k]=r;added+=1
 fields=list(dict.fromkeys(fields+[k for r in rows for k in r]))
 with path.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
 result={'core_ordinary_actions_before_supplement':683,'supplement_ordinary_actions':len(follow),'compiled_unique_ordinary_actions':len(rows),'compiled_full_award_keys':len({r['award_key'] for r in rows}),'added_this_run':added,'pre_run_csv_sha256':before,'compiled_csv_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'rule':'Full award/agency/parent/modification/transaction identity; no money sum, no OT or parent/subaward double-counting','source':'evidence/final-priority-live-followup.json'}
 (P/'audit/final-ordinary-actions-accounting.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':run()
