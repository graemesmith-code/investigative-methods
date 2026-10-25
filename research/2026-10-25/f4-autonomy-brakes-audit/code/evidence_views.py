"""Shared temporal view: disclosed actions, metadata and observed activity are distinct."""
import csv
from decimal import Decimal
ACTIVITY={
 'W5170125C0052':('2026-04-23','Army reports West Point use/testing; not engagement enforcement','https://www.army.mil/article/291926/cadets_work_with_software_using_lethal_autonomous_weapons_systems_that_analyzes_tactical_decisions_provides_ethical_score'),
 'HR001125F0028':('2026','DARPA lists 2026 CODORD performer papers; not proof of this support order\'s exact task or weapons deployment','https://www.darpa.mil/research/programs/codord'),
 'W31P4Q26F0015':('2026-09-22','Navy reports CAMP Gray Flag demonstration; order allocation/modification remains ambiguous','https://www.dvidshub.net/news/575299/navy-demonstrates-collaborative-autonomy-mission-planning-future-combat-aircraft'),
}
def action_index(package):
 out={}
 for r in csv.DictReader((package/'evidence/fpds-verified-actions.csv').open()):out.setdefault(r['award_key'],[]).append(r)
 return out
def temporal(record,contracts):
 piid=record['piid'];pop=record.get('period_of_performance',{});iscontract=record.get('fpds_applicable',False)
 actions=contracts.get(record['award_key'],[]) if iscontract else record.get('usaspending_transaction_reconciliation',{}).get('transactions',[])
 def date(r):return (r.get('signed_date') or r.get('action_date') or '')[:10]
 def money(r):return Decimal(str(r.get('obligation_usd',r.get('federal_action_obligation',0)) or 0))
 dated=[(date(r),money(r),r) for r in actions if date(r)];positive=[d for d,m,r in dated if m>0]
 reasons=[d+': '+str(r.get('reason') or r.get('action_type_description') or '') for d,m,r in dated if any(t in str(r.get('reason') or r.get('action_type_description') or '').upper() for t in ['TERMINAT','CLOSE OUT','CLOSEOUT'])]
 activity=ACTIVITY.get(piid,('','No independent activity/test/deployment evidence established for this exact award; finance/record period alone does not prove activity',''))
 end=(pop.get('end_date') or '')[:10];start=(pop.get('start_date') or '')[:10]
 status='record_period_overlaps_cutoff' if start and end and start<='2026-10-25'<=end else ('record_period_ended; continuation and recent changes unresolved' if end and end<'2026-10-25' else 'record_period_status_unresolved')
 return {'date_signed':record.get('date_signed'),'performance_start':start,'current_end':end,'potential_end':pop.get('potential_end_date'),'record_currentness_status':status,'last_public_action_date':max((d for d,m,r in dated),default=''),'last_positive_obligation_date':max(positive,default=''),'net_calendar2026_obligations_usd':str(sum((m for d,m,r in dated if '2026-01-01'<=d<='2026-10-25'),Decimal(0))) if dated else None,'positive_calendar2026_increments_usd':str(sum((m for d,m,r in dated if '2026-01-01'<=d<='2026-10-25' and m>0),Decimal(0))) if dated else None,'termination_completion_evidence':' | '.join(reasons) if reasons else 'No termination/closeout decision established by inspected action reasons; a passed end date is not such a decision','independent_activity_date':activity[0],'independent_activity_evidence':activity[1],'independent_activity_source':activity[2],'reporting_limit':'DoD contract/subcontract release delay; complete disclosed feed is not all real-world recent actions' if iscontract else 'Assistance reporting availability is bounded; do not automatically impose the contract-specific 90-day delay','award_record_last_modified_metadata':pop.get('last_modified_date')}
