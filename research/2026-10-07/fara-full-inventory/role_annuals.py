"""Verify 2025 API/original amounts for every role-matched major relationship."""
import json,collections,concurrent.futures
from extend_reverse import P,S,query,fetch
from match_full_inventory import core
from reconcile_major import amount

def run():
 edges=json.loads((P/'full-role-edges.json').read_text());ids={x['house_relationship_id'] for x in edges if x['provisional_major']};annual={x['house_relationship_id']:x for x in json.loads((P/'house-annual-provisional.json').read_text())};out=[]
 for id in sorted(ids):
  a=annual[id];regs={int(s.split('-')[0]) for s in a['senate_identifiers'] if s and s.split('-')[0].isdigit()};names={core(n) for n in a['client_names']};rows=[];queries=[]
  for reg in sorted(regs):
   rr,c=query('role-annual-'+str(reg),{'registrant_id':reg,'filing_year':2025});queries.append(c);rows += [r for r in rr if core(r['client']['name']) in names]
  with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:originals=list(pool.map(lambda r:fetch('lda-original-'+r['filing_uuid']+'.html',r['filing_document_url']),rows))
  checks=[];latest={}
  for r,raw in sorted(zip(rows,originals),key=lambda x:x[0]['dt_posted']):
   if r['filing_type'] in ['RR','RA']:continue
   c={'uuid':r['filing_uuid'],'source':r['filing_document_url'],'posted':r['dt_posted'],'period':r['filing_period'],'client_id':r['client']['id']}
   try:
    from decimal import Decimal
    values,boxes=amount(raw);c.update(amounts=values,matches_api=all((v is None and r[k] is None) or (v is not None and r[k] is not None and Decimal(v)==Decimal(r[k])) for k,v in values.items()))
   except Exception as e:c.update(matches_api=False,error=str(e))
   checks.append(c);latest[(r['registrant']['id'],r['client']['id'],r['filing_period'])]=c
  from decimal import Decimal
  sums={k:str(sum(Decimal(x.get('amounts',{}).get(k) or 0) for x in latest.values())) for k in ['income','expenses']}
  item={'house_relationship_id':id,'client_names':a['client_names'],'queries':queries,'matched_forms':len(rows),'originals_acquired':sum(x is not None for x in originals),'checks':checks,'latest_versions':list(latest.values()),'annual_numeric_lower_bounds':sums,'all_amounts_match':all(c['matches_api'] for c in checks),'identity_scope':'API client name normalized within original registrant identifier. Foreign principal identity remains separate.'};out.append(item);(P/'role-annual-verification.json').write_text(json.dumps(out,indent=2));print(id,a['client_names'],len(rows),sums,flush=True)
if __name__=='__main__':run()
