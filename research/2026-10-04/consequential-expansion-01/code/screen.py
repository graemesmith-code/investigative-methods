"""Explicit model-authored novelty screening; no Cartesian hypothesis inflation."""
import pathlib,json,csv,hashlib
P=pathlib.Path(__file__).resolve().parents[1];BASE=P.parent/'source-pair-completeness'
# Candidate, family, source roles, disposition, nearest earlier mechanism, difference or reason.
N=[
('X01','medical_disclosure',[247,250,251],'develop','H04; R05','Payment-versus-explicit article conflict declaration and applicable journal disclosure window; not merely a paid trial investigator or changed outcome.'),
('X02','extractive_obligation',[111,107,295],'develop','D05; N01','A fixed contractual amount due supplies an external benchmark; two-sided receipt/payment reconciliation alone cannot establish the amount owed.'),
('X03','waste_destination',[218,38],'develop','C01; P05','Sender-reported waste-management destination versus recipient site capability/authorization; not an emissions estimate or issuer claim.'),
('X04','political_disclosure',[117,118],'develop','I01; I05','Contradictory same-activity foreign-principal declarations across disclosure systems; not generic client ownership or temporal influence.'),
('X05','charity_disclosure',[45,117],'develop','I05; E08','Explicit charity legislative-lobbying declaration compared to documented same-entity legislative activity; definitions and fiscal scope are the central test.'),
('X06','sponsorship_chain',[118,143],'develop','I04; S05','Trace a particular advertisement through an agent’s itemized foreign-principal campaign spending; not aggregate ad spending reconciliation or sanctions overlap.'),
('X07','authorization_sequence',[283,101,304],'develop','C03; C04; E07','Test explicit written-approval-before-construction sequencing against dated physical activity; not protected-area overlap or generalized funded delivery.'),
('X08','reclamation_security',[304,305,288],'develop','C08; E06','Required site-specific reclamation security versus security actually posted; do not substitute a company accounting provision for a bond.'),
('X09','title_claim',[288,309],'develop','F04; C04','A filed assertion of a specific mining right versus authoritative status of that exact instrument on that date; distinct from company existence or surface activity.'),
('X10','supplier_accountability',[228,38],'develop','E02; P05','Verified buyer-supplier relationship during final facility harm finding, with continued sourcing/response evidence; not generic enforcement-to-public-funding overlap.'),
('X11','evidence_independence',[248,250,249],'develop','H02; P01','A synthesis double-counting the same participants as independent studies; not outcome switching, duplicate publication alone or a retraction citation.'),
('X12','assay_attribution',[312,288],'develop','N09; P05','Exact sample-ID/method-attributed numeric assay versus original measurement; not an issuer production upper bound or general compliance assertion.'),
('J01','research_ownership',[246,252],'duplicate','H03','Public funding to resulting patent/assignee already covered; a foreign assignee is a parameter variation without a new obligation.'),
('J02','market_timing',[289,288,38],'duplicate','R16','Adding environmental bad news does not change the existing insider-trade/event mechanism.'),
('J03','safety_recurrence',[281,284],'duplicate','P02','Recurring pipeline causes after claimed repair is the existing defect-rectification mechanism with another transport mode.'),
('J04','funding_delivery',[271,279,259],'duplicate_or_missing_evidence','E07','Broadband licence plus funding does not prove subscriber service; a promised-delivery test already exists and no coverage sample is supplied.'),
('J05','research_integrity',[246,250],'duplicate','P01','Funding that relies on a retracted paper is an existing retracted-evidence-reliance mechanism with a different citing document.'),
('J06','public_grant_flow',[54,45],'defer_scope_attribution','E07; E09','Charity grants cannot be attributed to a particular federal award without restricted-fund ledgers; fungibility defeats a simple onward-money allegation.'),
('J07','duplicate_funding',[245,246,249],'defer_missing_cost_records','H01; N01','Same output can lawfully acknowledge multiple funders; duplicate reimbursement requires the same invoice/cost and exclusivity terms.'),
('J08','regional_eligibility',[62,63],'reject_coverage_mismatch','W09','FTS and cohesion/shared-management programs have different coverage; regional code overlap does not identify a common award.'),
('J09','mineral_rights',[302,308],'reject_geographic_mismatch','C04','BC tenure cannot directly validate Ontario mineral occurrences; source names and regional jurisdiction defeat the pairing.'),
('J10','mineral_claims',[308,288],'defer_ambiguous_claim','N09','Historic occurrence versus a new-discovery headline is not a precise contradiction without the issuer’s exact definition and technical evidence.'),
('J11','cleanup_status',[109,198,214],'duplicate_status_proxy','R14','Changing the observation from electricity generation to light/plume activity does not create a new retired-asset-operation mechanism.'),
('J12','official_travel',[272,76],'reject_passenger_inference','T01; I08','Aircraft tracks cannot establish which official travelled; expense dates lack sufficient passenger/time detail for an impossible-itinerary claim.'),
('J13','privacy_remediation',[337,152,134],'defer_functional_evidence','D03','A surviving certificate/script does not establish continued personal-data collection after a privacy remedy; functionality and exact order scope are missing.'),
('J14','cyber_contracts',[54,149,150],'specialization_only','D01','Procurement indicates possible use but not installed vulnerable version or missed patch SLA; existing CVE exposure gate still applies.'),
('J15','political_roles',[117,272],'reject_jurisdiction_bridge','I08','US lobbying and Canadian official travel cannot establish the same officeholder’s revolving-door conduct without an independent employment chronology.'),
('J16','human_rights_funding',[338,271],'duplicate','E02','Later funding after a rights finding is the existing enforcement-to-funding policy question, not a new mechanism.'),
('J17','protected_land',[302,229],'duplicate','C03','Different licence class or protected-area threshold does not create a new overlap hypothesis.'),
('J18','data_quality',[249,251],'support_only','research_identity','ORCID disagreement can be identity maintenance, not a consequential relationship or independently verified affiliation.')]
N.extend([
('X13','crossborder_asset_condition',[47,7],'develop','F04; S03','Voluntary deregistration asset condition tested against contemporaneous title interest, not general company existence or a sanctions asset match.'),
('X14','crossregulator_accounts',[5,6],'develop','E09','Supposedly identical audited consolidated accounts filed with two regulators; not public-award-to-revenue reconciliation.'),
('REF-H01','trial_reporting_deadline',[246,248],'refinement_not_new','H01','Award-specific results submission deadline and exceptions sharpen the existing grant/trial mechanism; not counted as another discovery.'),
('REF-D01','covered_asset_deadline',[148,149,150],'refinement_not_new','D01','Passive covered-asset/deadline evidence sharpens existing vulnerability exposure reasoning; not counted as a new mechanism.')])
rows=[dict(candidate_id=i,family=f,source_ids=ids,disposition=d,nearest_existing=old,novelty_or_rejection_reason=reason,review_basis='same-model catalog and prior-card reasoning; no record execution') for i,f,ids,d,old,reason in N]
(P/'candidate-screen.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
with (P/'candidate-screen.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
ss=[json.loads(x) for x in (BASE/'sources.jsonl').read_text().splitlines()];(P/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ss));(P/'baseline-manifest.json').write_text(json.dumps(dict(baseline_commit='9fa87b3fe8d36134e888698c997fd4bc0d9ed11a',baseline_cards=32,baseline_mechanisms=65,baseline_active_provisional_combinations=1715,baseline_quarantines=15,original_source_descriptions=344,new_paid_api_calls=0,weekly_telemetry='unavailable'),indent=2)+'\n')
print('Screened',len(rows),'development candidates',sum(r['disposition'].startswith('develop') for r in rows))
