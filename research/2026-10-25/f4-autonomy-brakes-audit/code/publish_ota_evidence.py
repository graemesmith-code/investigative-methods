#!/usr/bin/env python3
"""Export/verify exact public-government OT XML already retrieved; no network.

With --verify-only, reparse the public response bodies and compare complete
identity/money/date/description fields with the authored action registers.
No credentials, private articles or unrelated raw cache bodies are copied.
"""
import argparse,hashlib,json,pathlib,shutil,xml.etree.ElementTree as ET
from decimal import Decimal
P=pathlib.Path(__file__).resolve().parents[1]
A='{http://www.w3.org/2005/Atom}';F='{https://www.fpds.gov/FPDS}'
def run(verify_only=False):
 out=P/'evidence/ota-primary-responses';out.mkdir(exist_ok=True)
 targets=[]
 for name in ('ota-resolution-review.json','ota-keyword-followup-records.json'):
  targets+=json.loads((P/'evidence'/name).read_text())['targets']
 receipts=[];parsed_count=0
 for t in targets:
  actions={}
  for page in t['pages']:
   expected=page['sha256'];dest=out/(expected+'.xml')
   if not verify_only:
    sources=[pathlib.Path('/workspace/scratch/f4-ota')/(expected+'.raw'),pathlib.Path('/workspace/scratch/f4-ota-keywords')/(expected+'.xml')]
    source=next(x for x in sources if x.is_file());shutil.copyfile(source,dest)
   raw=dest.read_bytes();assert hashlib.sha256(raw).hexdigest()==expected and len(raw)==page['bytes']
   root=ET.fromstring(raw)
   for entry in root.findall(A+'entry'):
    payload=entry.find(A+'content')[0];assert payload.tag==F+'OtherTransactionIDV'
    ident=payload.find(F+'OtherTransactionIDVID/'+F+'OtherTransactionIDVContractID');detail=payload.find(F+'contractDetail')
    def value(node,path):return node.findtext('/'.join(F+x for x in path.split('/')),'')
    identity=tuple(value(ident,x) for x in ('agencyID','PIID','modNumber','transactionNumber'))
    assert identity[1]==t['piid'] and identity not in actions
    actions[identity]={k:value(detail,v) for k,v in {'signed_date':'relevantContractDates/signedDate','current_end':'relevantContractDates/currentCompletionDate','potential_end':'relevantContractDates/ultimateCompletionDate','action_obligation_usd':'dollarValues/obligatedAmount','aggregate_obligations_usd':'totalDollarValues/totalObligatedAmount','description':'contractData/descriptionOfContractRequirement'}.items()}
   receipts.append({'piid':t['piid'],'public_path':dest.relative_to(P).as_posix(),**page})
  expected_rows={(r['agency_id'],r['piid'],r['modification'],r['transaction_number']):r for r in t['actions']}
  assert set(actions)==set(expected_rows)
  for identity,row in actions.items():
   for field,val in row.items():assert val==expected_rows[identity][field],(identity,field)
  summed=sum((Decimal(x['action_obligation_usd']) for x in actions.values()),Decimal(0))
  assert summed==Decimal(t['action_obligation_sum_usd']) and len(actions)==t['visible_action_count']
  parsed_count+=len(actions)
 result={'source':'Exact already-retrieved public FPDS government XML, unchanged bytes','bodies':receipts,'body_count':len(receipts),'unique_instruments':len(targets),'verified_unique_actions':parsed_count,'validation':'Every compound action identity, obligation, signed/current/potential date, aggregate field and full description reparsed and exactly compared with authored JSON; sums/counts match. Financial aggregate discrepancies remain unresolved.','paid_calls':0,'network_requests':0,'initial_probe_timing_limit':'Only formal retrieval bodies and their recorded receipts are exported. Original probe HTTP-start times were not separately saved; no timestamps invented.'}
 if not verify_only:
  (out/'response-manifest.json').write_text(json.dumps(result,indent=2)+'\n')
  for name in ('ota-resolution-review.json','ota-keyword-followup-records.json'):
   path=P/'evidence'/name;record=json.loads(path.read_text())
   record['raw_cache_public_at_initial_snapshot']=False
   record['raw_cache_public']=True
   record['public_formal_response_manifest']='evidence/ota-primary-responses/response-manifest.json'
   record['public_body_scope']='Six formal exact-target government XML responses only; unrelated/private caches and original probe timestamp gaps are not represented as published or complete.'
   path.write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='bodies'},indent=2))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--verify-only',action='store_true');run(a.parse_args().verify_only)
