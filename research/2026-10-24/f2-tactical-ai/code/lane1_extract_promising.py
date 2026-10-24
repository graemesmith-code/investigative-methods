import sqlite3,json
from pathlib import Path
B=Path(__import__('os').environ.get('F2_ROOT', str(Path(__file__).resolve().parents[1])));C=sqlite3.connect(B/'data/financial_actions.sqlite');C.row_factory=sqlite3.Row
ids=['FA865925CB002','FA865124FB014','FA865124CB014','W5170125CA242','FA462524C0011','FA462524C0009','FA462524C0010','W5170125CA246','W5170125CA253','W56KGU24C0023','N0001424C1114','FA865023C1054','FA875021C1505','N0001424C2411','N0001424C2202','N0001422C1033','N0001420C2019','FA237724CB048','FA865125FB046','W58RGZ26F0223','FA873024PB019','N6600126C0027','FA864926P0135','N0042125F0151']
out=[]
for aid in ids:
 rows=[dict(r) for r in C.execute('SELECT * FROM transaction_details WHERE award_id=? ORDER BY action_date,row_number',(aid,))]
 keys=sorted(set(r['award_key'] for r in rows))
 for key in keys:
  rr=[r for r in rows if r['award_key']==key];byyear={}
  for r in rr:byyear[r['action_date'][:4]]=byyear.get(r['action_date'][:4],0)+(r['obligation_cents'] or 0)
  out.append({'award_id':aid,'award_key':key,'names':sorted(set(r['entity_name'] for r in rr)),'archive_transactions':len(rr),'archive_net_obligation_cents':sum(r['obligation_cents'] or 0 for r in rr),'calendar_year_net_obligation_cents':byyear,'first_action':rr[0]['action_date'],'last_action':rr[-1]['action_date'],'titles':sorted(set(r['title'] or '' for r in rr)),'descriptions':sorted(set(r['description_text'] or '' for r in rr)),'awarding_sub_agencies':sorted(set(r['awarding_sub_agency_code'] or '' for r in rr)),'funding_sub_agencies':sorted(set(r['funding_sub_agency_code'] or '' for r in rr)),'pscs':sorted(set(r['psc_text'] for r in rr)),'naics':sorted(set(r['naics_text'] for r in rr)),'parent_award_ids':sorted(set(r['parent_award_id'] or '' for r in rr)),'source_urls':sorted(set(r['source_url'] for r in rr)),'latest_money_json_unsummed':json.loads(rr[-1]['money_json'] or '{}'),'transactions':[{'row_number':r['row_number'],'action_date':r['action_date'],'transaction_key':r['transaction_key'],'obligation_usd':r['action_obligation_usd'],'raw_locator':r['raw_locator']} for r in rr]})
(B/'lane1/promising_funding_extract.json').write_text(json.dumps(out,indent=2))
for a in out:print(a['award_id'],','.join(a['names']),a['archive_net_obligation_cents']/100,a['calendar_year_net_obligation_cents'],a['titles'][-1][:180])
