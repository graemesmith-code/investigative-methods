import sqlite3,json,csv,re,collections
from pathlib import Path
B=Path(__import__('os').environ.get('F2_ROOT', str(Path(__file__).resolve().parents[1])));O=B/'lane1';C=sqlite3.connect(B/'data/financial_actions.sqlite');C.row_factory=sqlite3.Row
rs=[dict(r) for r in C.execute("SELECT entity_key,GROUP_CONCAT(DISTINCT entity_name) AS names,MIN(action_date) AS first_action,MAX(action_date) AS last_action,COUNT(*) AS transactions,COUNT(DISTINCT award_key) AS awards,SUM(obligation_cents) AS net_cents,SUM(CASE WHEN action_date<'2024-01-01' THEN obligation_cents ELSE 0 END) AS prior_cents,SUM(CASE WHEN action_date>='2024-01-01' THEN obligation_cents ELSE 0 END) AS recent_cents,SUM(CASE WHEN SUBSTR(action_date,1,4)='2024' THEN obligation_cents ELSE 0 END) AS calendar_2024_cents,SUM(CASE WHEN SUBSTR(action_date,1,4)='2025' THEN obligation_cents ELSE 0 END) AS calendar_2025_cents,SUM(CASE WHEN SUBSTR(action_date,1,4)='2026' THEN obligation_cents ELSE 0 END) AS calendar_2026_cents FROM source_rows GROUP BY entity_key")]
for r in rs:r['first_observed_2024_2026']=r['first_action']>='2024-01-01';r['recent_vs_prior_ratio']=r['recent_cents']/r['prior_cents'] if r['prior_cents']>0 else None;r['calendar_2025_vs_2024_ratio']=r['calendar_2025_cents']/r['calendar_2024_cents'] if r['calendar_2024_cents']>0 else None
with (O/'recipient_growth.tsv').open('w') as f:w=csv.DictWriter(f,rs[0].keys(),delimiter='\t');w.writeheader();w.writerows(sorted(rs,key=lambda r:-r['recent_cents']))
entities={r['entity_key']:r for r in rs}; counts=collections.Counter();unknown=[];selected=[];prior_exclusions=re.compile(r'UNIVERSITY|\bUNIV\b|COLLEGE|REGENTS|INSTITUTE OF TECHNOLOGY|ACADEMY|INSTITUT(E|ION)|RESEARCH FOUNDATION|MASSACHUSETTS INSTITUTE',re.I)
for line in (O/'candidate_register.jsonl').open():
 r=json.loads(line);k=set(r['keyword_matches']);recent=r['net_obligation_2024_2026_cents']>0
 if recent:counts['positive_recent_candidate_awards']+=1
 if 'keyword_metadata' in r['routes'] and not r['vendor_matches']:counts['keyword_awards_outside_named_vendor_list']+=1
 if r['substantive_tactical_combo']:counts['ai_autonomy_plus_weapon_contested_awards']+=1
 if r['substantive_tactical_combo'] and recent:
  counts['positive_recent_ai_autonomy_plus_weapon_contested_awards']+=1;selected.append(r)
  if not r['vendor_matches']:
   counts['positive_recent_tactical_combo_outside_named_vendor_list']+=1
   if not prior_exclusions.search('|'.join(r['entity_names'])):unknown.append(r)
  if any(entities[e]['first_observed_2024_2026'] for e in r['entity_keys'] if e in entities):counts['positive_recent_tactical_combo_first_observed_recipient_awards']+=1
 if recent and 'transition' in k and (k & {'ai','autonomy'}):counts['positive_recent_ai_autonomy_transition_keyword_awards']+=1
 if recent and re.search(r'phase\s*(?:iii|3)\b',' | '.join(r.get('evidence_descriptions',[])),re.I) and (k & {'ai','autonomy'}):counts['positive_recent_ai_autonomy_explicit_phase_iii_awards']+=1
unknown.sort(key=lambda r:(-r['screen_score'],-r['net_obligation_2024_2026_cents']));
with (O/'unknown_recipient_tactical_candidates.jsonl').open('w') as f:
 for r in unknown:f.write(json.dumps(r)+'\n')
with (O/'tactical_combo_candidates.jsonl').open('w') as f:
 for r in selected:f.write(json.dumps(r)+'\n')
# Cross-service traces are relationship flags only, not causal program transitions.
trans=[]
for r0 in C.execute("SELECT t.entity_key,GROUP_CONCAT(DISTINCT t.entity_name) AS names,GROUP_CONCAT(DISTINCT CASE WHEN t.action_date<'2024-01-01' THEN d.funding_sub_agency_code END) AS pre2024_funders,GROUP_CONCAT(DISTINCT CASE WHEN t.action_date>='2024-01-01' THEN d.funding_sub_agency_code END) AS recent_funders FROM source_rows t JOIN description_enrichment e USING(transaction_key) JOIN descriptive_rows d ON d.id=e.first_description_row GROUP BY t.entity_key"):
 r=dict(r0);before=set((r['pre2024_funders'] or '').split(','));after=set((r['recent_funders'] or '').split(','))
 if '97AE' in before and after & {'1700','2100','5700'}:r['interpretation']='Recipient had pre-2024 DARPA funding and 2024–2026 service funding. This is a cross-service lead, not proof that a given programme transitioned.';trans.append(r)
(O/'darpa_to_service_recipient_flags.json').write_text(json.dumps(trans,indent=2))
audit={'counts':dict(counts),'unique_recipient_ueis':len(rs),'first_observed_2024_2026_recipient_ueis':sum(r['first_observed_2024_2026'] for r in rs),'nonacademic_named_vendor_excluded_tactical_candidates':len(unknown),'darpa_pre2024_to_service_recent_recipient_flags':len(trans),'emergence_caveat':'First observed in this preselected archive, not company founding or first government award. Annual values are calendar years; 2026 ends Sept 30 so year-on-year rates are partial-year comparisons.','agency_caveat':'Only agency/subagency codes in recovered source slices; office-level research-to-operational transitions require live API/primary evidence. Generic service agency presence is not an operational-customer claim.'}
(O/'selection_audit.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2))
print('\nUNKNOWN TOP 45')
for r in unknown[:45]:print(r['selection_id'],r['award_id'],','.join(r['entity_names']),r['net_obligation_2024_2026_cents']/100,' | '.join(r['evidence_descriptions'])[:240])
