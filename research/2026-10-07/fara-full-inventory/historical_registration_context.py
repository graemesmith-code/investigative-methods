"""Search registrant-scoped registrations independent of current client IDs."""
from extend_reverse import query,fetch,P
import json,concurrent.futures

def run():
 out=[]
 for name,reg in [('transcanada',400684035),('honda',18546),('novartis',9204)]:
  for kind in ['RR','RA']:
   rows,c=query('context-'+name+'-'+kind,{'registrant_id':reg,'filing_type':kind})
   with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:access=list(pool.map(lambda r:fetch('lda-original-'+r['filing_uuid']+'.html',r['filing_document_url']) is not None,rows))
   c.update(registrant=name,originals_acquired=sum(access),filings=[{'uuid':r['filing_uuid'],'client_id':r['client']['id'],'current_label':r['client']['name'],'posted':r['dt_posted']} for r in rows]);out.append(c);(P/'historical-registration-context.json').write_text(json.dumps(out,indent=2));print(name,kind,len(rows),flush=True)
if __name__=='__main__':run()
