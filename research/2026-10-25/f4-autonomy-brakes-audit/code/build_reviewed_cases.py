#!/usr/bin/env python3
"""Build a deliberately small, human-reviewed financial case set.

This is not the machine-screen universe or an estimate of all safeguards spending.
Categories overlap; each selected award has one primary bucket for additive totals.
Mixed-purpose vehicles and unallocated FFRDC tasks are excluded from totals.
"""
import csv,json,pathlib
from decimal import Decimal
from evidence_views import action_index,temporal
P=pathlib.Path(__file__).resolve().parents[1]
M={}
for n in [1,2,3,4,6,7,18]:M[f'FA865125CB{n:03d}']=('ASIMOV','A','D','benchmark research','Normative benchmark; DARPA marks complete; no fielded legal governor established')
M.update({
 'HR001125F0028':('CODORD support order / JHU APL','A','B;C','rule-reasoning assurance research','Explicit ROE/legal ambition; exact task SOW not inspected; public civilian-domain benchmarks are not weapons LOAC validation or fielded enforcement'),
 'FA9550261B207':('HAMLET / FY26 MURI ethical reasoning','A','B;C','ethical-reasoning TEVV research','Grant title and MURI topic establish ethics/autonomy research; exact award SOW and delivered weapons-specific validation not established'),
 'W5170125C0052':('TEELAWS','A','D','training/evaluation','LOAC-linked scoring and instruction; expressly does not make engagement decisions'),
 'FA864922P1015':('CETLAWS','A','B','research prototype','Historical ethical decision-support lineage; expired record is not current implementation'),
 'N6833525C0110':('Robust maritime target recognition / RDRTec','C','A','distinction-enabling research','Combatant/noncombatant vessel classification; A-enabling contribution retained, not contextual legal target determination'),
 'N0002425CS104':('NSAM / Arete','C','A','distinction-enabling research','Multi-sensor vessel classification; A-enabling contribution retained, not comprehensive LOAC enforcement'),
 'W5170124C0035':('EpochGeo civilian-infrastructure harm context','A','D','contextual civilian-harm decision-support research','Explicit civilian-infrastructure collateral-harm context; AI/autonomous-weapon integration and achieved harm reduction not established'),
 'FA864921P1296':('Ethical trust calibration / CETLAWS Phase I','A','B','historical normative feasibility research','Ethical behavior of lethal robots and trust calibration; historical Phase I, not current deployment'),
 'N6833521C0510':('RAIDER / Soar, now Accelint AI','B','A;C','constraint research','ROE-constrained autonomy topic; historical award; implementation/currentness limits'),
 'N6833521C0549':('RAIDER / Weather Gage','B','A;C','constraint research','Historical research tied to ROE requirements; no current operational proof'),
 'W31P4Q26F0015':('CAMP mission planning and debrief','B','A;C','demonstrated mission-constraint workflow','Whole mission-planning order, not normative-feature-only allocation; blocking effectiveness and combat deployment not established'),
 'FA945326CX013':('Spectral performance-modeling toolkit','C','','technical modeling','Detection/tracking/classification performance; no reviewed explicit normative acceptance test'),
 'W5170124C0174':('Latent AI / Linchpin','C','D','technical AI pipeline','Record-expired award; does not prove entire Linchpin program ended'),
 'FA864926P0169':('ResilienX model-health monitoring','C','','technical monitoring','Record-expired at cutoff; not an ethical governor'),
 'FA864926P0093':('Quasistatics secure key loader','C','','security provisioning','Secure provisioning does not demonstrate positive authorization of a particular target'),
 'FA865124CB024':('TALON','C','','sensor classification','Uncertainty and sensor coordination can support lawful operation; not a legal test by themselves'),
 'FA248722FA002':('TETRAS A2WSD','C','D','mixed-purpose T&E vehicle','Whole-order obligations not allocable to safeguards or ethics; excluded from additive case totals'),
 'FA86552417047':('CASPER++ social-robot collaboration','A','C','normative-autonomy-adjacent research','Ethical/transparent social-robot collaboration; weapons-specific scope unresolved'),
 'W911NF261A113':('Georgia Tech normative and justified agency','A','C','normative-autonomy-adjacent research','Computational normative agency; exact weapons/LOAC task scope and PI not verified'),
 'W911NF2510079':('Syracuse human judgments of AI moral violations','A','D','normative-autonomy-adjacent research','Human moral judgments/social-science research; not established technical weapons restraint'),
 'FA95502310036':('George Mason robot moral agency','A','C','normative-autonomy-adjacent research','Qualification of robot moral agency; weapons scope unresolved; record period ended'),
 'FA95502010342':('Clemson ethical behavior and trust','A','B','normative-autonomy-adjacent research','Human-autonomy trust and ethics; weapons-specific technical restraint not established'),
 'FA95502010130':('Stanford normative and justified agency','A','C','normative-autonomy-adjacent research','Historical normative agency; successor relationship and weapons task scope unresolved'),
 'N629092212005':('Nottingham normative cooperation','A','C','normative-autonomy-adjacent research','Autonomous-agent normative cooperation; specific weapons-law application unverified'),
})
ADJACENT={'FA9550261B207','FA86552417047','W911NF261A113','W911NF2510079','FA95502310036','FA95502010342','FA95502010130','N629092212005'}
TECH={
 'ASIMOV':['https://www.darpa.mil/research/programs/autonomy-standards-and-ideals-with-military-operational-values'],
 'W5170125C0052':['https://www.sbir.gov/awards/215327','https://www.army.mil/article/291926/cadets_work_with_software_using_lethal_autonomous_weapons_systems_that_analyzes_tactical_decisions_provides_ethical_score'],
 'HR001125F0028':['https://www.darpa.mil/research/programs/codord','https://www.darpa.mil/sites/default/files/attachment/2024-11/codord-info-session-distro-a.pdf'],
 'FA9550261B207':['https://www.onr.navy.mil/assets/2025-03/N0001425SF002.pdf'],
 'FA864922P1015':['https://www.tandfonline.com/doi/full/10.1080/15027570.2024.2366094'],
 'N6833525C0110':['https://www.sbir.gov/awards/218158'],
 'N0002425CS104':['https://www.sbir.gov/awards/218265'],
 'N6833521C0510':['https://navysbir.us/n19_3/N193-141.htm','https://navyfst.com/wp-content/uploads/2023/03/2023-ITS-Tech-Guide.pdf'],
 'N6833521C0549':['https://navysbir.us/n19_3/N193-141.htm','https://www.sbir.gov/awards/192723'],
 'W31P4Q26F0015':['https://www.dvidshub.net/news/575299/navy-demonstrates-collaborative-autonomy-mission-planning-future-combat-aircraft','https://www.ga-asi.com/ga-asi-selected-by-us-navy-pma-281-for-collaborative-autonomy-mission-planning-and-debrief-project'],
 'W5170124C0174':['https://cpeisw.army.mil/wp-content/uploads/2023/09/Project-Linchpin-Approved-for-Release-1.pdf'],
 'FA865124CB024':['https://www.sbir.gov/awards/208992'],
 'W5170124C0035':['https://www.sbir.gov/awards/209584','https://www.epochgeo.com/projects'],
}
if __name__=='__main__':
 raw=json.loads((P/'evidence/live-award-register.json').read_text());rows=[];seen=set();actions=action_index(P)
 scopepath=P/'evidence/live-technical-scope-review.csv';scopes={r['piid']:r for r in csv.DictReader(scopepath.open())} if scopepath.exists() else {}
 for a in raw['awards']:
  for r in a.get('records',[]):
   piid=r['piid'];key=r['award_key']
   if piid not in M or key in seen:continue
   seen.add(key);program,cat,sec,maturity,limit=M[piid];pop=r.get('period_of_performance',{});end=pop.get('end_date','') or ''
   active=bool(end and end[:10]>='2026-10-25' and (pop.get('start_date','') or '9999')<='2026-10-25')
   tx=r.get('usaspending_transaction_reconciliation',{})
   def window(k):return r.get(k.replace('_obligations_usd','_fpds_obligations_usd')) if r.get('fpds_applicable') else tx.get(k)
   rows.append({'award_key':key,'piid':piid,'program':program,'primary_category':cat,'secondary_categories':sec,'category_status':'human-reviewed function; enabling is not enforcement','maturity':maturity,'recipient':r.get('recipient'),'description':r.get('description'),'net_obligations_usd':r.get('total_obligation_usd'),'fy2019_2026_obligations_usd':window('fy2019_2026_obligations_usd'),'fy2024_2026_obligations_usd':window('fy2024_2026_obligations_usd'),'cy2024_cutoff_obligations_usd':window('cy2024_2026_to_cutoff_obligations_usd'),'current_end':end,'potential_end':pop.get('potential_end_date'),'record_window_overlaps_cutoff':active,'counted_in_named_case_total':piid!='FA248722FA002','limitation':limit,'source_url':r.get('source_url'),'response_sha256':r.get('response_sha256'),'verification_route':'FPDS plus USAspending award' if r.get('fpds_applicable') else 'USAspending award plus complete assistance transactions','fpds_complete':r.get('fpds_complete'),'fpds_api_delta_usd':r.get('fpds_minus_usaspending_usd'),'assistance_transaction_delta_usd':tx.get('minus_award_total_obligation_usd')})
   row=rows[-1]
   row['scope_tier']='normative_autonomy_adjacent_weapons_application_unverified' if piid in ADJACENT else ('mixed_purpose_vehicle' if piid=='FA248722FA002' else ('technical_assurance_component' if cat=='C' else 'explicit_weapons_or_military_norms_function'))
   row['tier_rule']='Explicit weapon/ROE/civilian-harm function in award or directly linked technical source; adjacent title/general ethics alone is separate. Intended function does not prove achieved validation or fielded implementation.'
   if piid in ADJACENT:row['counted_in_named_case_total']=False
   urls=TECH.get(piid,TECH.get(program,[r.get('source_url')]))
   row['technical_source_urls']=' | '.join(u for u in urls if u)
   row['technical_evidence_depth']='Linked program/award technical text and specialist review; exact SOW/deployment gaps remain as stated' if piid in TECH or program in TECH else 'Primary award description only; no independent technical paper or acceptance test inspected for this row'
   row['category_basis']=limit
   row['allocable_safeguard_only_usd']=None
   row['money_interpretation']='Whole-award associated obligation, not isolated safeguard-feature spending; no separate allocation measured'
   row['scope_discrepancy']='Original 2026-01-28 +1988634 explicitly Navy CAMP; 2026-04-28 P00001 $0 says JSIL USMC SERVICE LEVEL TRAINING EXERCISES PHASE5A; task SOW/allocation unresolved' if piid=='W31P4Q26F0015' else ''
   row['function_view']=('broader_normative_autonomy; exact weapons application unverified' if piid in ADJACENT else ('perceptual_classification_enabling; not full contextual legal distinction' if piid in {'N6833525C0110','N0002425CS104'} else ('human normative training/evaluation' if piid=='W5170125C0052' else maturity)))
   sr=scopes.get(piid,{})
   row['technical_archive_source_file']=sr.get('source_file','');row['technical_archive_source_row']=sr.get('source_row','');row['technical_archive_source_row_sha256']=sr.get('source_row_sha256','')
   row['technical_mechanism_from_abstract']=sr.get('specific_tested_or_proposed_mechanism','')
   row['technical_abstract_limits']=sr.get('limits','')
   if piid=='FA864921P1296':row['technical_evidence_depth']='Complete archived SBIR abstract with exact file/row/hash; not full SOW or proof of delivered prototype'
   row['scope_actions_file']='evidence/camp-scope-actions.csv' if piid=='W31P4Q26F0015' else ''
   row.update(temporal(r,actions))
 rows.sort(key=lambda r:(r['primary_category'],r['program'],r['piid']))
 (P/'evidence/reviewed-cases.json').write_text(json.dumps(rows,indent=2)+'\n')
 with (P/'evidence/reviewed-cases.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 totals={}
 for c in 'ABCD':
  rr=[r for r in rows if r['primary_category']==c and r['counted_in_named_case_total']]
  def add(rs,k):return str(sum((Decimal(str(x[k])) for x in rs if x.get(k) is not None),Decimal(0))) if rs else None
  totals[c]={'awards_in_selected_case_set':len(rr),'net_obligations_usd':add(rr,'net_obligations_usd'),'fy2019_2026_obligations_usd':add(rr,'fy2019_2026_obligations_usd'),'fy2024_2026_obligations_usd':add(rr,'fy2024_2026_obligations_usd'),'record_window_overlap_awards':sum(r['record_window_overlaps_cutoff'] for r in rr),'record_window_overlap_net_obligations_usd':add([r for r in rr if r['record_window_overlaps_cutoff']],'net_obligations_usd')}
 adj=[r for r in rows if r['piid'] in ADJACENT]
 out={'scope':'Selected human-reviewed named awards only; not comprehensive program counts or allocable total safeguards budgets. Historical/cumulative obligations, not remaining balances or annual expenditure. Secondary tags never add dollars. D and unmatched frameworks unknown, not zero. TETRAS excluded as mixed purpose. ALL normative-autonomy-adjacent awards, including HAMLET, are excluded symmetrically from weapons-linked A subtotals; retained in separate view. Record window overlap is not direct verification of ongoing work.','totals':totals,'adjacent_view_not_added_to_weapons_totals':{'award_count':len(adj),'net_obligations_usd':str(sum((Decimal(str(r['net_obligations_usd'])) for r in adj),Decimal(0))),'record_overlap_count':sum(r['record_window_overlaps_cutoff'] for r in adj),'record_overlap_net_obligations_usd':str(sum((Decimal(str(r['net_obligations_usd'])) for r in adj if r['record_window_overlaps_cutoff']),Decimal(0)))},'missing_named_piids':sorted(set(M)-set(r['piid'] for r in rows))}
 (P/'audit/reviewed-case-accounting.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
