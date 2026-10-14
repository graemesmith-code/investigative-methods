from collect import *
TYPES=['A','B','C','D','IDV_A','IDV_B','IDV_B_A','IDV_B_B','IDV_B_C','IDV_C','IDV_D','IDV_E']
fields=['Award ID','Recipient Name','Recipient UEI','generated_internal_id','recipient_id','Award Amount']
queries=[('coverage-duns',{'recipient_search_text':['491319143']}),('coverage-parentuei',{'recipient_search_text':['H9J3LCB6URU8']}),('coverage-parentduns',{'recipient_search_text':['561470928']}),('coverage-address',{'keywords':['"KINGSFORDWEG 151"']}),('coverage-cage',{'keywords':['H2G78']}),('coverage-quote-name',{'recipient_search_text':['"NAI LOGISTICS B.V."']})]
def search(t):
 label,f=t
 for group,types in [('contracts',TYPES[:4]),('idvs',TYPES[4:])]:
  paginate(label+'-'+group,'/api/v2/search/spending_by_award/',{'filters':{'award_type_codes':types,**f},'fields':fields,'sort':'Award ID','order':'asc'})
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(search,queries))
for types,label in [(TYPES[:4],'recipient-tx-contracts'),(TYPES[4:],'recipient-tx-idvs')]:
 paginate(label,'/api/v2/search/spending_by_transaction/',{'filters':{'award_type_codes':types,'recipient_search_text':['SLVJF3DR8MN5']},'fields':['Action Date','Award ID','Recipient Name','Recipient UEI','Transaction Amount','Transaction Description','Action Type','Mod','generated_internal_id','internal_id'],'sort':'Action Date','order':'asc'})
for label in ['download-recipient']:
 d=json.loads((ROOT/'raw'/f'{label}.body').read_text());s=fetch(label+'-status',d['status_url']);print(label,s)
 if s.get('status')=='finished':fetch(label+'-zip',d['file_url'])
for a in ['CONT_IDV_SPE60523D9402_9700']:
 print('amounts',fetch('vehicle-amounts','/api/v2/idvs/amounts/'+a+'/'))
 paginate('vehicle-funding','/api/v2/idvs/funding/',{'award_id':a,'sort':'reporting_fiscal_date','order':'asc'})
for a in json.loads((ROOT/'vehicle-child_awards.json').read_text()):
 paginate('funding-'+a['piid'],'/api/v2/awards/funding/',{'award_id':a['generated_unique_award_id'],'sort':'reporting_fiscal_date','order':'asc'})
