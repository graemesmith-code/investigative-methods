from collect import *
def funding(a):
 label=a.replace('CONT_AWD_','').replace('CONT_IDV_','')
 if a.startswith('CONT_IDV_'):
  return a,paginate('recipient-funding-idv-'+label,'/api/v2/idvs/funding/',{'award_id':a,'sort':'reporting_fiscal_date','order':'asc'})
 return a,paginate('recipient-funding-'+label,'/api/v2/awards/funding/',{'award_id':a,'sort':'reporting_fiscal_date','order':'asc'})
rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 for a,rr in ex.map(funding,json.loads((ROOT/'award-ids.json').read_text())):
  rows.extend({**r,'queried_award_id':a} for r in rr)
(ROOT/'all-recipient-funding.json').write_text(json.dumps(rows,indent=2))
print('TOTAL',len(rows),flush=True)
