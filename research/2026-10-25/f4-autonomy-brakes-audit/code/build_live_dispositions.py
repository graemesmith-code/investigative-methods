#!/usr/bin/env python3
"""Account for every live candidate, without turning financial checks into capability proof."""
import csv,json,pathlib
from evidence_views import action_index,temporal
P=pathlib.Path(__file__).resolve().parents[1]
if __name__=='__main__':
 raw=json.loads((P/'evidence/live-award-register.json').read_text());selected={r['award_key']:r for r in json.loads((P/'evidence/reviewed-cases.json').read_text())};actions=action_index(P)
 scopepath=P/'evidence/live-technical-scope-review.csv';scopes={r['piid']:r for r in csv.DictReader(scopepath.open())} if scopepath.exists() else {}
 titles={}
 seed=P.parents[1]/'2026-10-24/f2-tactical-ai/audit/lane2-candidate_register.tsv'
 if seed.exists():
  for r in csv.DictReader(seed.open(),delimiter='\t'):titles.setdefault(r['piid'],r.get('title',''))
 false={'W5170124C0063','W31P4Q20C0021','SP470124P0068','SP470123C0057','SP470122P0039','SP470122P0038','HDTRA124P0013','N6660425F3014','N6660425F3001','FD01','N0016422F3007'}
 adjacent={'FA86552417047','W911NF261A113','W911NF2510079','FA95502310036','FA95502010342','FA95502010130','N629092212005'}
 records=[]
 for a in raw['awards']:
  for r in a.get('records',[]) or [{'piid':a['piid'],'award_key':'','recipient':'','description':''}]:
   key=r['award_key'];piid=r['piid'];scope=titles.get(piid) or r.get('description','');review=selected.get(key);text=(scope+' '+r.get('description','')).lower();sr=scopes.get(piid,{})
   if not key:category='unresolved';disposition='Exact award detail unresolved; not absence evidence';depth='resolution attempts only'
   elif review:category=('A-adjacent' if review.get('scope_tier')=='normative_autonomy_adjacent_weapons_application_unverified' else review['primary_category'])+';'+review['secondary_categories'];disposition=review['limitation'];depth='human-reviewed case; technical access limits stated in report/evidence notes'
   elif sr.get('primary_category')=='C':category='C-described;'+sr.get('secondary_categories','');disposition=sr['disposition']+'; '+sr['limits'];depth='Complete archived SBIR technical abstract adjudicated; proposed mechanism is not achieved validation/deployment'
   elif sr.get('primary_category')=='Excluded':category='excluded_after_technical_abstract_review';disposition=sr['disposition']+'; '+sr['limits'];depth='Complete archived SBIR abstract inspected; outside defined safeguards scope'
   elif piid in false:category='false_positive_or_broad_support';disposition='Described material/electronics/general-support scope does not establish autonomy safeguards; excluded from safeguards totals';depth='primary award description plus inherited SBIR title, where present'
   elif piid in adjacent:category='normative_autonomy_adjacent';disposition='Normative/social-robot/agency research; weapon-specific LOAC technical scope not established; excluded from A case totals';depth='primary finance/title; no award-specific weapons implementation established'
   elif key.startswith('CONT_IDV_'):category='unallocated_parent_vehicle';disposition='Parent vehicle is not a specific safeguard task or absence-of-funding test; parent value excluded';depth='primary parent record'
   elif any(w in text for w in ['ethic','deontic','moral','rules of engagement']):category='A_candidate;C_possible';disposition='Explicit normative-title lead; original technical scope/currentness requires review beyond financial reconciliation; excluded from selected-case sums';depth='primary finance and description; inherited technical title where present'
   elif any(w in text for w in ['assur','verif','valid','robust','trust','uncertain','explain','test','calibr','safe']):category='C_candidate;B_possible';disposition='Technical-assurance lead; no explicit weapons-law acceptance test established from reviewed description; no whole-award safeguards attribution';depth='primary finance and description; inherited technical title where present'
   else:category='scope_unresolved';disposition='Generic contract description or weak lexical lead; financial existence verified, safeguard function not adjudicated';depth='primary finance; inherited title where present'
   records.append({'piid':piid,'award_key':key,'recipient':r.get('recipient'),'technical_title_or_description':scope,'primary_award_description':r.get('description'),'classification':category,'scope_tier':review.get('scope_tier','unadjudicated_or_excluded') if review else 'unadjudicated_or_excluded','disposition':disposition,'technical_review_depth':depth,'technical_source_urls':review.get('technical_source_urls','') if review else '','scope_discrepancy':review.get('scope_discrepancy','') if review else '','in_selected_case_register':bool(review),'in_selected_case_money_sum':bool(review and review['counted_in_named_case_total']),'net_obligations_usd':r.get('total_obligation_usd'),'source_url':r.get('source_url'),'financial_verification':'FPDS/API exact reconciliation' if r.get('fpds_applicable') else ('USAspending assistance actions exact reconciliation' if r.get('usaspending_transaction_reconciliation',{}).get('reconciled') else 'parent or unresolved; not an action reconciliation')})
   records[-1].update(temporal(r,actions) if key else {k:'' for k in temporal({'piid':piid,'award_key':''},actions)})
   records[-1].update(technical_source_file=sr.get('source_file',''),technical_source_row=sr.get('source_row',''),technical_source_row_sha256=sr.get('source_row_sha256',''),described_technical_mechanism=sr.get('specific_tested_or_proposed_mechanism',''),normative_or_roe_content_in_reviewed_abstract=sr.get('normative_or_roe_content','not reviewed'),technical_scope_limit=sr.get('limits','No complete technical abstract adjudicated in this crosswalk'))
 with (P/'evidence/live-candidate-disposition.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
 counts={}
 for r in records:counts[r['classification']]=counts.get(r['classification'],0)+1
 (P/'audit/live-disposition-accounting.json').write_text(json.dumps({'live_candidate_rows_accounted':len(records),'classification_counts':counts,'note':'Every live candidate is represented, including unresolved targets and generic/false-positive leads. A financial reconciliation is not substantive proof of a safeguard. Selected-case totals are an explicit sample, not the complete live or archive universe.'},indent=2)+'\n');print(json.dumps(counts,indent=2))
