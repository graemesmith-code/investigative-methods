#!/usr/bin/env python3
"""Discovery only: scan complete financial index and join exact-key descriptions.

Archives must match supplied source hashes. This does not hydrate or quote award
totals. No subaward amounts or IDV ceilings are added to prime action obligations.
"""
import argparse,csv,gzip,hashlib,json,pathlib,re,tarfile,collections
HASHES={'FWI-20261016-normalized-research-context.tar.gz':'b9ad7acc6061f21792c4d26efc57940e4506702e22c490046d69f5e5b292a8eb','FWI-20261016-normalized-rd-contracts.tar.gz':'63809f0fbf8fc5427341e637054cfe2012f6f7f5c28379af9178f735a6762317','FWI-20261016-normalized-capabilities.tar.gz':'a06375165baf25a4532ee6bef8c3cb47aba05ebb6c03cc55db8253487953b96e'}
TERMS=[r'\b882E\b',r'\bSSSTRP\b',r'\bWSESRB\b',r'\bFISTRP\b',r'SYSTEM SAFETY',r'WEAPON[S]? SAFETY',r'FLIGHT TERMINATION',r'\bAFTS\b',r'SAFE[ -]AND[ -]ARM',r'\bESAD\b',r'RANGE SAFETY',r'HAZARD TRACKING']
R=re.compile('|'.join('('+x+')' for x in TERMS),re.I)
def rows(t,name):
 with gzip.open(t.extractfile(name),'rt') as f:
  for i,line in enumerate(f,1):yield i,json.loads(line)
def main():
 a=argparse.ArgumentParser();a.add_argument('--archives',type=pathlib.Path,required=True);a.add_argument('--out',type=pathlib.Path,required=True);args=a.parse_args();args.out.mkdir(parents=True,exist_ok=True)
 identities={};covered=set();audit={'scope':'Complete financial_actions index read; exact award and transaction-key joins to primary contract descriptions; local discovery only','archive_verification':[],'members':[],'terms':TERMS};counts=collections.Counter();awards={}
 for name,want in HASHES.items():
  p=args.archives/name;got=hashlib.sha256(p.read_bytes()).hexdigest();assert got==want,(name,got);audit['archive_verification'].append({'file':name,'sha256':got,'bytes':p.stat().st_size})
 with tarfile.open(args.archives/'FWI-20261016-normalized-research-context.tar.gz') as t:
  for i,r in rows(t,'normalized/financial_actions.jsonl.gz'):
   counts['financial_index_physical_rows']+=1;k=r.get('transaction_key');identities[k]=r
  audit['members'].append({'archive':'research-context','member':'normalized/financial_actions.jsonl.gz','physical_rows':i})
 counts['financial_index_unique_transaction_keys']=len(identities)
 for archive in ['FWI-20261016-normalized-rd-contracts.tar.gz','FWI-20261016-normalized-capabilities.tar.gz','FWI-20261016-normalized-research-context.tar.gz']:
  with tarfile.open(args.archives/archive) as t:
   for m in t.getmembers():
    if not m.name.endswith('.jsonl.gz') or '_subaward' in m.name or not m.name.startswith('normalized/usaspending_'):continue
    for i,r in rows(t,m.name):
     counts['description_physical_rows']+=1;desc=' '.join(str(r.get(x) or '') for x in ['title','text','evidence_excerpt']);hit=R.search(desc)
     key=r.get('award_key');tx=r.get('transaction_key');mandatory=key and any(x in key for x in ['N0042123F3004','N0016422F3007'])
     if tx in identities:covered.add(tx)
     if not key or (not hit and not mandatory):continue
     rec=awards.setdefault(key,{'award_key':key,'recipient_names':set(),'matched_terms':set(),'transaction_keys':set(),'description_transaction_keys':set(),'descriptions':set(),'discovery_members':set(),'in_financial_index':False})
     rec['recipient_names'].add(r.get('entity_name',''));rec['descriptions'].add(desc);rec['discovery_members'].add(m.name);rec['description_transaction_keys'].add(tx)
     rec['matched_terms'].update(x.group(0).upper() for x in R.finditer(desc));rec['in_financial_index']|=tx in identities
    audit['members'].append({'archive':archive,'member':m.name,'physical_rows':i})
 # Count all archived actions for matched awards, not just matching-description rows.
 for tx,r in identities.items():
  if r.get('award_key') in awards:awards[r['award_key']]['transaction_keys'].add(tx)
 with (args.out/'safety-contract-discovery-register.csv').open('w',newline='') as f:
  fields=['award_key','recipient_names','matched_terms','archived_action_count','description_action_count','in_financial_index','descriptions','discovery_members','promotion_status'];w=csv.DictWriter(f,fields);w.writeheader()
  for key,r in sorted(awards.items()):
   w.writerow({**{x:' | '.join(sorted(r[x])) for x in ['recipient_names','matched_terms','descriptions','discovery_members']},'award_key':key,'archived_action_count':len(r['transaction_keys']),'description_action_count':len(r['description_transaction_keys']),'in_financial_index':r['in_financial_index'],'promotion_status':'discovery_only_not_award_total'})
 counts['financial_index_keys_with_primary_description']=len(covered);counts['financial_index_keys_without_primary_description']=len(identities)-len(covered)
 audit['counts']=dict(counts);audit['matched_awards']=len(awards);audit['note']='712186 is checked as a physical financial-index row count; primary-description coverage is separately counted by exact transaction key. Unmatched records are not evidence of absent safety controls.'
 (args.out/'safety-contract-screen-audit.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps({'counts':dict(counts),'matched_awards':len(awards)}))
if __name__=='__main__':main()
