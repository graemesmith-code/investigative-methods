"""Produce the review report and reproducibility package after screening."""
from pathlib import Path
import json, zipfile

B=Path(__file__).resolve().parent
R=B/'results'
summary=json.loads((R/'screen-summary.json').read_text())
groups=json.loads((R/'candidate-groups.json').read_text())
source=json.loads((B/'source-summary.json').read_text())
archive_url='https://files.usaspending.gov/award_data_archive/FY2025_All_Contracts_Full_20260906.zip'
manifest={
    'retrieved_date':'2026-09-18', 'archive_url':archive_url,
    'archive_listing_updated_date':'2026-09-06',
    'archive_internal_filename_date':'2026-09-07',
    'archive_http_last_modified':'Mon, 14 Sep 2026 01:07:26 GMT',
    'archive_bytes':1914255016,
    'archive_sha256':summary['archive_sha256'],
    'listing_endpoint':'https://api.usaspending.gov/api/v2/bulk_download/list_monthly_files/',
    'listing_request':{'agency':'all','fiscal_year':2025,'type':'contracts'},
    'notes':'Ready-made archive used. The separately requested custom export was not used. File dates differ across the official listing, ZIP members and HTTP header; each is recorded as supplied.'
}
(R/'contract-source.json').write_text(json.dumps(manifest,indent=2))

def cell(x): return str(x).replace('|',' / ').replace('\n',' ')
lines=['# US federal contracts versus OFAC: first screening results',
'', 'Prepared 18 September 2026. **No sanctions violation or failed screening has been established.**', '',
f"Screened **{summary['unique_transactions']:,} unique contract and contract-vehicle transactions**, representing **{summary['distinct_recipient_names']:,} distinct recipient names**, against **{source['names_including_aliases']:,} names and official aliases** for **{source['retained_entities']:,} current OFAC SDN entities**.", '',
f"The name comparison produced **{summary['candidate_groups']:,} candidate pairs** (OFAC entity × recipient name × UEI), involving **{summary['matched_unique_transactions']:,} transactions** and **{summary['matched_unique_awards']:,} award identifiers**. These counts are screening alerts, not violations.", '',
'**Assessment:** One candidate, NAI Logistics B.V., matches by name and street address. Its only FY2025 hit is a zero-dollar termination of a contract vehicle. The other 12 candidate pairs have conflicting recipient and OFAC locations and remain unconfirmed. Nothing in this first pass establishes a failed OFAC check.', '',
'## What was compared', '',
'- Contract action dates: 1 October 2024–30 September 2025 (FY2025); all agencies. The archive includes both ordinary contract actions (award type codes A/B/C/D) and contract vehicles (IDVs, whose award type is blank). Both were screened. This is broader than the initially requested A/B/C/D custom export.',
'- The ready-made USAspending archive is a September 2026 snapshot of FY2025 records; its precise source metadata is in contract-source.json.',
'- OFAC list publication date: 17 September 2026. Only entries marked Entity were retained. Individuals, vessels and aircraft were excluded. Strong and weak aliases were retained and distinguished.',
'- The contract field screened was recipient_name. Case and punctuation were normalised. A second, separately labelled pass removed common terminal company suffixes, such as LLC and Ltd. No fuzzy spelling match was attempted.',
f"- Exact after normalisation: {summary['match_methods'].get('normalized_exact',0)} candidate pairs. Suffix-removed: {summary['match_methods'].get('legal_suffix_removed',0)} candidate pairs.",
f"- Duplicate transactions skipped: {summary['duplicate_transactions']:,}; out-of-period rows: {summary['out_of_period_rows']:,}; other award types excluded: {json.dumps(summary['excluded_award_types'])}; blank recipient names: {summary['blank_recipient_names']:,}.", '',
'## Candidate review table', '',
'Countries and cities below come directly from the two source records. Different locations lower confidence, but do not conclusively rule out a branch or affiliate. No common ownership is inferred. Full addresses, identifiers, matching aliases and original contract rows are in the evidence package.', '',
'| Contract recipient | UEI | Recipient city / country | OFAC entity and ID | OFAC city / country | Match method | Actions / awards |',
'|---|---|---|---|---|---|---|']
for g in sorted(groups,key=lambda g:(g['recipient_name'],g['ofac_id'],g['recipient_uei'])):
    contract_places='; '.join(sorted(set(f'{a[1]}, {a[2]}, {a[3]}' for a in g['locations'])))
    ofac_places='; '.join(sorted(set(f"{a.get('city','')}, {a.get('country','')}" for a in g['ofac_record']['addresses'])))
    vals=[g['recipient_name'],g['recipient_uei'],contract_places,f"{g['ofac_primary_name']} ({g['ofac_id']})",ofac_places,g['method'],f"{g['transactions']} / {len(g['award_ids'])}"]
    lines.append('| '+' | '.join(cell(x) for x in vals)+' |')
lines += ['', '## The strongest observed identity match: NAI Logistics B.V.', '',
'NAI Logistics B.V. matches by full name and street address: Kingsfordweg 151, Amsterdam. Its OFAC ID is 44257. The contract recipient UEI is SLVJF3DR8MN5. This is a strong identity lead; matching corporate registration numbers would provide additional confirmation.', '',
'[OFAC added NAI Logistics B.V. on 11 December 2023](https://ofac.treasury.gov/recent-actions/20231211), naming the same Amsterdam address and Dutch registration number 60346515. The current snapshot still includes the company.', '',
'The saved FY2025 record for vehicle SPE60523D9402, modification P00002, has action date **11 March 2025**, action type **TERMINATE FOR CAUSE**, and **$0.00 federal action obligation**. It is an IDV modification, not a new A/B/C/D contract award. [USAspending vehicle record](https://www.usaspending.gov/award/CONT_IDV_SPE60523D9402_9700/).', '',
'This row records termination after designation. It does not establish that the government awarded new business, made a prohibited payment, or failed an OFAC check. Nor does the interval between designation and recorded termination show that work continued during that interval. The worthwhile follow-up is the vehicle history and its delivery orders between designation and termination, including any FY2024 activity. That history has not been reconstructed in this first pass.', '',
'## Examples of weak name collisions', '',
'Digital Technologies, Inc. in the contracts file is at 760 S Rochester, Ontario, California. [The company website](https://www.digitaltechnologies-inc.com/) gives that address. The matched OFAC company (36423) is Limited Liability Company Digital Technologies, at 19 Vavilova Street, Moscow. This looks like a name collision; no connection has been established.', '',
'Patriot LLC is recorded in Columbia, Maryland. [Its website](https://www.patriotllc.net/about/) describes a Columbia-based technology contractor founded in 2005. The suffix-removed match is Patriot Inc. (57139), a Marshall Islands entity established on 6 December 2024. These differences support treating this as a weak name collision, not an allegation.', '',
'## How to verify the remaining candidates', '',
'1. Open the OFAC entry at https://sanctionssearch.ofac.treas.gov/Details.aspx?id=NUMBER, using the OFAC ID above. Compare full names, addresses, registration numbers and websites with the contractor identified by its UEI and CAGE code in the saved contract rows.',
'2. If identity survives that check, locate the original OFAC designation announcement and any later removal or amendment. Compare the effective designation date with each action date. The saved current list is not a historical list.',
'3. Inspect what each action actually did. An amendment, correction, zero-dollar action or deobligation is not evidence that a new contract was awarded or money paid after designation.',
'4. Check the applicable restrictions and any authorisations or exemptions before alleging a violation. The records alone do not reveal what checks a procurement office performed.', '',
'## Limits of this first pass', '',
'This is a simple direct-recipient name screen. It does not screen recipient_name_raw, trading names, parent names, subsidiaries, beneficial owners, subcontractors, individuals or other sanctions lists. It misses spelling variations and entities removed from the SDN list before this snapshot. A clean result is not a clean bill of health. A name alert is not evidence of wrongdoing.', '',
'Apart from the NAI designation check and the initial identity comparisons above, historical designation dates and corporate identity have not been fully verified. No payments or contract-value totals are reported. No paid data, Jev calls or external outreach were used.', '',
'## Sources and reproducibility', '',
f'- [Official USAspending contract archive]({archive_url})',
'- [Official OFAC SDN XML](https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/SDN.XML)',
'- [OFAC guidance on assessing name matches](https://ofac.treasury.gov/faqs/5)', '',
'The accompanying ZIP contains the sanctions snapshot, scripts, source metadata, screen counts, all candidate groups, and original matching contract rows. The 1.9 GB full contract archive is not included; its URL, byte size and SHA-256 are preserved. Reproduction needs that exact archive; a later official snapshot may differ.', '',
'To reproduce with Python 3.11 or later, place the downloaded archive beside the scripts and run: `python3 screen_contracts.py fy2025-full.zip results`. No third-party Python packages or API key are needed.', '',
'Matching logic was checked with a synthetic direct match, suffix match, unrelated name and duplicate transaction. Every CSV member was read to completion (including ZIP CRC verification during reading).']
report=B.parent/'sanctions-screen-results-2026-09-18.md'
report.write_text('\n'.join(lines)+'\n')
bundle=B.parent/'sanctions-screen-evidence-2026-09-18.zip'
files=[B/'sdn.xml',B/'entities.json',B/'names.json',B/'source-summary.json',B/'prepare.py',B/'screen_contracts.py',B/'check_screen.py',B/'package_results.py',*R.glob('*.json'),R/'candidate-transactions.jsonl',report]
with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.name if p.parent!=R else 'results/'+p.name)
print(report)
print(bundle,bundle.stat().st_size)
