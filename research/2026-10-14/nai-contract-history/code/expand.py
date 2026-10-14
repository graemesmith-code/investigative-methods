from collect import *
TYPES=['A','B','C','D']
fields=['Award ID','Recipient Name','Recipient UEI','Award Amount','Start Date','End Date','Description','Awarding Agency','Awarding Sub Agency','generated_internal_id','recipient_id']
def search(label,filters):return paginate(label,'/api/v2/search/spending_by_award/',{'filters':{'award_type_codes':TYPES,**filters},'fields':fields,'sort':'Award ID','order':'asc','subawards':False})
searches=[('search-uei',{'recipient_search_text':['SLVJF3DR8MN5']}),('search-name',{'recipient_search_text':['NAI LOGISTICS']}),('search-vehicle-id',{'award_ids':['SPE60523D9402']}),('search-vehicle-hyphen',{'award_ids':['SPE605-23-D-9402']})]
searches += [(label+'-idvs',{**f,'award_type_codes':['IDV_A','IDV_B','IDV_B_A','IDV_B_B','IDV_B_C','IDV_C','IDV_D','IDV_E']}) for label,f in searches]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for label,r in ex.map(lambda t:(t[0],search(*t)),searches):print(label,'TOTAL',len(r),flush=True)
ids={'CONT_IDV_SPE60523D9402_9700'}
for p in ROOT.glob('search-*.json'):
 for r in json.loads(p.read_text()):
  if r.get('Recipient UEI')=='SLVJF3DR8MN5' or r.get('Recipient Name')=='NAI LOGISTICS B.V.':ids.add(r['generated_internal_id'])
ids.update(r['generated_unique_award_id'] for r in json.loads((ROOT/'vehicle-child_awards.json').read_text()))
(ROOT/'award-ids.json').write_text(json.dumps(sorted(ids),indent=2))
def award(a):
 label=a.replace('CONT_AWD_','').replace('CONT_IDV_','')
 d=fetch('detail-'+label,'/api/v2/awards/'+a+'/')
 tx=paginate('tx-'+label,'/api/v2/transactions/',{'award_id':a,'sort':'action_date','order':'asc'})
 return a,len(tx)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 for a,n in ex.map(award,sorted(ids)):print('collected',a,n,flush=True)
