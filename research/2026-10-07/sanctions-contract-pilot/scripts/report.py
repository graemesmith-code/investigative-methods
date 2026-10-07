"""Offline report assembly from preserved dossiers, Jev responses and search results."""
import json,pathlib,decimal,collections,hashlib
P=pathlib.Path(__file__).resolve().parents[1]
ledger=json.loads((P/'jev/ledger.json').read_text())
cost=ledger['accounted_microusd']['jev'];assert cost<9_000_000
rows=[];disagreements=[]
for f in sorted((P/'dossiers').glob('*.json')):
 d=json.loads(f.read_text());a=json.loads((P/'jev/stage1'/f'{f.stem}.response.json').read_text())['answers']
 nai=d['ofac']['ofac_id']=='44257';pre=d['on_or_after_designation_rows']==0
 final='credible identity; possible new child-order business; vehicle administrative' if nai else 'unresolved identity; all supplied rows predate identified designation' if pre else 'unresolved identity; likely name collision'
 rank=1 if nai else 3 if pre else 2
 rows.append({'rank_tier':rank,'id':d['id'],'recipient':d['recipient'],'uei':d['uei'],'final_category':final,'jev_identity':a['identity'],'jev_business':a['business'],'designation':d['designation']['date'],'original_net_obligations':d['amounts']['net_obligations'],'actions':len(d['transaction_rows']),'identity_basis':d['code_only_identity']})
 if not nai and a['business']['choice']!='identity_unresolved':disagreements.append({'id':d['id'],'jev_business':a['business']['choice'],'final_override':'Identity unresolved; no attribution to designated person. Dates and action content assessed separately.','temporal_check':'All rows precede designation' if pre else 'Rows on/after designation but identity unresolved'})
 text=f"# {d['id']} — {d['recipient']}\n\n**Final category:** {final}. Rank tier {rank} (ties are intentional).\n\nUEI {d['uei']}; CAGE {', '.join(d['cage_codes'])}. OFAC counterpart {d['ofac']['primary_name']} ({d['ofac']['ofac_id']}); programs {', '.join(d['ofac']['programs'])}. This counterpart is not automatically the recipient.\n\nContract locations: {d['contract_addresses']}. OFAC locations: {d['ofac']['addresses']}. Identifiers and exact aliases are retained in [{d['id']}.json]({d['id']}.json).\n\nDated listing/identification: {d['designation']['date']}; see [official archived notice](../{d['designation']['path']}) and original URL in sources/manifest.json. {d['designation']['date_note']}. C06 also has a 2020-09-21 EO13382 designation, before these records. Historical removals, all other applicable sanctions bases, and unproven ownership are not resolved here.\n\nOriginal matching rows: {len(d['transaction_rows'])}; before listing {d['before_designation_rows']}; on/after {d['on_or_after_designation_rows']}. Positive obligations ${d['amounts']['positive_obligations']}; negative adjustments ${d['amounts']['negative_obligations']}; net ${d['amounts']['net_obligations']}. These are amounts recorded for the procurement recipient, not amounts proven to have gone to a sanctioned person. No payment total; award ceilings and repeated award-level totals are not summed.\n\nStrongest innocent explanation: {d['strongest_innocent_explanation']}. Next evidence: {d['missing_evidence']}.\n\nJev selected identity **{a['identity']['choice']}**, activity **{a['business']['choice']}**, payment **{a['payment']['choice']}**, significance **{a['significance']['choice']}**. Model confidence is not a verified identity probability. Exact [prompt](../jev/stage1/{d['id']}.request.json) and [response](../jev/stage1/{d['id']}.response.json) are preserved. Human category above overrides unsupported activity attribution.\n\nSource: [{d['transactions_source']['path']}](../{d['transactions_source']['path']}), SHA-256 {d['transactions_source']['sha256']}; JSONL lines {', '.join(map(str,d['transactions_source']['line_numbers']))}. Those original rows preserve full award/transaction IDs, modification, action date, addresses, IDs and values; compact rows in the dossier reproduce every matched action.\n"
 if nai:text+='\nSee [NAI calibration](../NAI-calibration.md) for independently refreshed child orders, dated general-license scope, action versus update timing, and unresolved purchasing/payment records.\n'
 f.with_suffix('.md').write_text(text)
rows.sort(key=lambda r:(r['rank_tier'],r['id']))
(P/'ranked-shortlist.json').write_text(json.dumps(rows,indent=2)+'\n')
(P/'jev/human-overrides.json').write_text(json.dumps(disagreements,indent=2)+'\n')
table=['| Tier | Recipient / UEI | Original actions | Listing date | Assessment |','|---|---|---:|---|---|']
for r in rows:table.append(f"| {r['rank_tier']} | [{r['recipient']}](dossiers/{r['id']}.md) / {r['uei']} | {r['actions']} | {r['designation']} | {r['final_category']} |")
intro=f'''# Sanctions versus USAspending: bounded pilot

Completed 7 October 2026. **One credible identity match, one unresolved post-designation purchasing question, no established prohibited payment or sanctions violation.** The five-name expansion produced no additional leads within its stated search scope.

**NAI Logistics B.V. remains the sole credible identity match.** Its FY2025 hit is a vehicle termination for cause on 11 March 2025 with zero additional obligations. Independently retrieved child histories reveal eight delivery orders dated 13–14 December 2023, two to three days after designation: $36,309.46 positive obligations, −$15,662.32 adjustments, **$20,647.14 net**. These are possible new-business records requiring the original instruments, not proof of payments or actual decision timing. Four orders are fully offset; a fifth is partly reduced. All eight reported total-outlay fields are null. [Full calibration and order table](NAI-calibration.md).

A dated official-US-government-business general license offers a concrete possible lawful explanation (31 CFR 583.509 in December 2023; later 583.510). Qualification is not established. Neither a short interval nor the old vehicle automatically resolves authorization. The designation was already public; novelty of the order rows has not been established.

The other 12 pairs have name/alias matches but conflicting locations and no corporate-registration or ownership bridge. Keep them **unresolved**, with likely name collision as the strongest innocent explanation. Do not attribute their contract amounts to sanctioned entities. Two counterpart entities—Geotech Engineering and Patriot Inc.—were listed after all supplied FY2025 actions. That date finding does not exclude an untested earlier ownership-based restriction.

## Ranked reading list

Tier 1 is the supported identity/records question. Tier 2 cases are tied unresolved identity leads, not a risk ranking. Tier 3 adds a temporal reason the current-list screen cannot establish post-designation activity. Every original pair is retained, including both Digital Technologies UEIs.

'''
tail=f'''

## What Jev added—and did not

Jev agreed with the code/source assessment on the one strong identity and 12 weak identities. It added a consistent set of structured judgments and correctly rejected payment inference and the tested alias/ownership inventions. It found no new entity relationship or factual lead beyond the sources and ordinary code. The user-defined options and dossier context constrain this test: this was not a blind accuracy study or an open-ended entity-discovery benchmark.

The original screen already identified NAI and its zero-dollar termination. The useful new factual work—historical designation comparisons, child-order retrieval, separate positive/negative amounts, and the dated government-business authorization—came from official records and code. Jev selected the supported NAI follow-up after being supplied that work.

Jev's weaknesses are retained. One broad short-interval control scored 0.54 and failed the pre-set threshold, so candidate calls stopped. A narrower literal record question scored 0.96; six atomic controls then passed. In candidate output, activity labels often ignored unresolved identity: {len(disagreements)} labels required an identity gate/clarification. It also called Geotech's actions predesignation correctly but labelled Z-AXIS and Phoenix administrative; those labels are not legal clearance. [All overrides](jev/human-overrides.json), [failed control](jev/controls/evaluation.json), [revised controls](jev/controls-v2/evaluation.json).

## Bounded expansion

Only NAI qualified. The original Treasury designation notice supported five separately named members of the same disjunctive Rahmani designation group: NAI Logistics Limited, Fidelis Logistic and Supply Services, Secure Movement Logistics Services, Orbit International FZE, and RG Group FZE. Exact passage offsets/hashes and Jev selections were checked against the original notice and separate OFAC entries before search. These are **not established NAI subsidiaries or aliases**; exact ownership percentages and intermediary roles are unknown. Each is separately designated, so coverage is not inferred from association or the 50% rule.

Ten bounded USAspending queries—contracts and IDVs separately for each name, FY2024–FY2025, at most 20 rows per query—returned zero rows with no next page. This is a null result within these names, filters and dates, not proof of no historical, subcontractor, alias or differently reported activity. No extra seeds were introduced to fill a quota. [Exact extraction and search log](expansion/validated-extractions.json), [null results](expansion/search-summary.json), [rejections](expansion/rejections.json).

## Evidence and cost

Both original ZIPs were recovered from private repository main commit 218de208b504372e06f73abae79de1e2e21d25a1, safely extracted and CRC-checked. Shared OFAC files match byte-for-byte; SDN hash matches the original source manifest; report matches the preserved repository report. The recovered subset confirms 13 pairs, 153 distinct transactions, 72 awards, 9,980 entities and 23,398 names/aliases. The full-run counts of 6,639,176 transactions and 101,379 distinct recipient names remain original-run metadata, not newly recomputed corpus counts. No bulk redownload. [Recovery checks](recovery-verification.json), [original archives and hashes](baseline/manifest.json).

**New Jev usage-derived conservative cost: US${cost/1e6:.6f} across {len(ledger['attempts'])} paid calls.** This includes the failed control and its revision; each call is rounded up to the next microdollar. It is not an invoice. No other paid service. Prior Alberta spending is excluded. The $9 internal reservation cap and $10 authorization ceiling were never approached. [Exact prompts, responses and ledger](jev/ledger.json).

Eight offline guard tests and the original matching fixture passed; original subset counts, child sums and pagination were checked. [Technical annex and reproduction](FINAL-TECHNICAL-ANNEX.md). No outreach, credential changes, TLS bypass or resumed Alberta investigation.

## Remaining questions

Obtain original NAI order/modification instruments and purchasing timestamps; establish authorization scope for the actual transactions; review delivery acceptance and payment evidence if available. For any other candidate, first obtain a dated corporate identity/ownership bridge before attributing activity. Corporate registers, private licenses, original purchasing instruments, universal sanctions history and all NAI awards were not comprehensively obtained. The two bounded pilot stages are complete with those evidence limits; the result is a reading list, not verification of misconduct.
'''
(P/'README.md').write_text(intro+'\n'.join(table)+tail)
spend={'experiment':'sanctions-contract-pilot-2026-10-07','new_jev_accounted_usd':cost/1e6,'microusd':cost,'calls':len(ledger['attempts']),'status':'bounded_pilot_complete','cost_basis':'input usage × verified $0.042/M, rounded up per call; not invoice','internal_cap_usd':9,'authorized_ceiling_usd':10,'prior_alberta_excluded_usd':.000507,'other_paid_services':False}
(P/'spend-ledger.json').write_text(json.dumps(spend,indent=2)+'\n')
print('Report generated',spend)
