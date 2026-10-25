#!/usr/bin/env python3
"""Exact primary follow-up of SRI/SIFT identities found by bounded keyword scans."""
import csv,json
import verify_ota_sources as ota
EXTRA={'HR00112590099':'CODORD / SRI SOLON','HR00112590098':'CODORD / SIFT'}
if __name__=='__main__':
 ota.TARGETS.update(EXTRA);records=[ota.fpds(piid) for piid in EXTRA]
 (ota.P/'evidence/ota-keyword-followup-records.json').write_text(json.dumps({'targets':records,'selection':'Exact SRI/SIFT identities discovered by deontic/program keyword search; not an open-ended OTA census.','paid_calls':0},indent=2)+'\n')
 rows=[r for t in records for r in t['actions']]
 with (ota.P/'evidence/ota-keyword-followup-actions.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 a=json.loads((ota.P/'audit/ota-keyword-followups.json').read_text());a['exact_identity_followup_requests']=ota.LOG;a['exact_identity_followup_request_count']=len(ota.LOG)
 (ota.P/'audit/ota-keyword-followups.json').write_text(json.dumps(a,indent=2)+'\n')
 print(json.dumps([{k:v for k,v in r.items() if k not in ['actions','pages']} for r in records],indent=2))
