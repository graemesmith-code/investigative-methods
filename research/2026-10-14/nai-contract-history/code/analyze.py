import os
import csv,json,pathlib,collections,decimal,hashlib
R=pathlib.Path(os.environ['NAI_AUDIT_DIR']);D=decimal.Decimal
p=next((R/'exports/download-recipient').glob('*PrimeTransactions*'));rows=list(csv.DictReader(p.open()));awards=list(csv.DictReader(next((R/'exports/download-recipient').glob('*PrimeAwardSummaries*')).open()));vehicle='SPE60523D9402';v=[r for r in rows if r['parent_award_id_piid']==vehicle];vh=[r for r in rows if r['award_id_piid']==vehicle];fy=[r for r in v if r['action_date_fiscal_year']=='2024'];post=[r for r in v if r['action_date']>='2023-12-11'];pre=[r for r in v if r['action_date']<'2023-12-11']
def money(rs):return str(sum(D(r['federal_action_obligation']) for r in rs))
def savecsv(name,rs,fields=None):
 if not fields:fields=list(rs[0]) if rs else []
 with (R/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rs)
for name,rs in [('all-recipient-transactions.csv',rows),('all-recipient-awards.csv',awards),('vehicle-order-transactions.csv',v),('vehicle-modifications.csv',vh),('fy2024-order-transactions.csv',fy),('post-designation-transactions.csv',post)]:savecsv(name,rs)
by=collections.defaultdict(list)
for r in v:by[r['award_id_piid']].append(r)
summary=[]
for piid,rr in sorted(by.items()):
 base=[x for x in rr if x['modification_number']=='0'][0];mods=[x for x in rr if x['modification_number']!='0'];a=json.loads((R/'raw'/('detail-'+base['contract_award_unique_key'].replace('CONT_AWD_','')+'.body')).read_text())
 summary.append({'piid':piid,'award_unique_key':base['contract_award_unique_key'],'initial_action_date':base['action_date'],'date_signed':a['date_signed'],'gross_initial_obligation':base['federal_action_obligation'],'deobligations':money(mods) if mods else '0.00','net_obligation':money(rr),'performance_start':a['period_of_performance']['start_date'],'performance_end':a['period_of_performance']['end_date'],'modifications':'; '.join(x['modification_number']+': '+x['action_date']+' '+x['action_type']+' '+x['federal_action_obligation'] for x in mods),'initial_report_date':base['initial_report_date'],'last_modified_date':a['period_of_performance']['last_modified_date'],'source':base['usaspending_permalink']})
savecsv('vehicle-orders-summary.csv',summary);savecsv('fy2024-orders-summary.csv',[r for r in summary if r['initial_action_date']>='2023-10-01' and r['initial_action_date']<'2024-10-01'])
fund=json.loads((R/'vehicle-funding.json').read_text());savecsv('vehicle-account-funding.csv',fund)
s={'recipient_awards':len(awards),'recipient_contract_awards':sum(a['award_or_idv_flag']=='AWARD' for a in awards),'recipient_idvs':sum(a['award_or_idv_flag']=='IDV' for a in awards),'recipient_transactions':len(rows),'recipient_action_date_range':[min(r['action_date'] for r in rows),max(r['action_date'] for r in rows)],'recipient_lifetime_net_obligations':money(rows),'vehicle_orders':len(by),'vehicle_order_transactions':len(v),'vehicle_modifications':len(vh),'vehicle_lifetime_net_obligation':money(v),'pre_designation_order_transactions':len(pre),'pre_designation_net_obligations':money(pre),'post_designation_new_order_count':len({r['award_id_piid'] for r in post if r['modification_number']=='0'}),'post_designation_transactions':len(post),'post_designation_gross_positive_obligations':money([r for r in post if D(r['federal_action_obligation'])>0]),'post_designation_deobligations':money([r for r in post if D(r['federal_action_obligation'])<0]),'post_designation_net_obligations':money(post),'fully_deobligated_post_designation_orders':[r['piid'] for r in summary if r['initial_action_date']>='2023-12-11' and D(r['net_obligation'])==0],'fy2024_orders':len({r['award_id_piid'] for r in fy}),'fy2024_order_transactions':len(fy),'fy2024_net_obligation':money(fy),'fy2023_net_obligation':money([r for r in v if r['action_date_fiscal_year']=='2023']),'last_positive_obligation_date':max(r['action_date'] for r in v if D(r['federal_action_obligation'])>0),'account_funding_rows':len(fund),'account_funding_gross_outlays':[x['gross_outlay_amount'] for x in fund],'account_funding_obligation_sum':str(sum(D(str(x['transaction_obligated_amount'])) for x in fund))}
(R/'findings-summary.json').write_text(json.dumps(s,indent=2));print(json.dumps(s,indent=2))
metadata=[]
for p in sorted((R/'raw').glob('*.request.json')):
 m=json.loads(p.read_text());m['evidence_file']=str(p.with_name(p.name.replace('.request.json','.body')));metadata.append(m)
(R/'query-manifest.json').write_text(json.dumps(metadata,indent=2))
# Reconcile independent API routes to downloaded CSVs.
ids=set(json.loads((R/'award-ids.json').read_text()));checks={'unique_csv_awards':len({a['contract_award_unique_key'] for a in awards}),'csv_award_ids_equal_api':ids=={a['contract_award_unique_key'] for a in awards},'csv_transaction_keys_unique':len(rows)==len({a['contract_transaction_unique_key'] for a in rows}),'vehicle_csv_order_ids_equal_relationship_api':{r['contract_award_unique_key'] for r in v}=={r['generated_unique_award_id'] for r in json.loads((R/'vehicle-child_awards.json').read_text())},'api_tx_count_equals_csv':len(json.loads((R/'recipient-tx-contracts.json').read_text()))+len(json.loads((R/'recipient-tx-idvs.json').read_text()))==len(rows),'download_total_rows':len(rows)+len(awards)}
(R/'reconciliation.json').write_text(json.dumps(checks,indent=2));print(checks)
