"""Publish sanitized, source-linked results from the completed local pilot.
No network, source collection or credentials. Raw intermediates stay ignored.
Run after reproduce.py, canada.py, review.py and summarize.py.
"""
from reproduce import *
from decimal import Decimal
def csvout(name,rows):
    with (BASE/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n");w.writeheader();w.writerows(rows)
def safe_link(u):
    m=re.search(r'-(\d{8})-\d+\.pdf$',u)
    return '-0-0.pdf' not in u and (not m or m[1]<=SNAPSHOT.replace('-',''))
def main():
    gs=json.loads((BASE/'us-candidates.json').read_text())
    anchors=json.loads((BASE/'us-source-backed-overlaps.json').read_text())
    linked=json.loads((BASE/'us-address-anchored-uei-overlaps.json').read_text())
    amounts=json.loads((BASE/'amounts.json').read_text())
    ca=json.loads((BASE/'canada-source-backed-active-overlaps.json').read_text())
    assert len(gs)==273 and len(anchors)==14 and len(linked)==21 and len(amounts)==12
    assert sum(g['transactions'] for g in anchors)==79
    assert sum(r['transactions'] for r in amounts)==2310
    results=[]
    for r in amounts:
        same=lambda g:g['entity']['role']==r['role'] and g['entity']['registration_number']==r['fara_registration'] and g['entity']['name']==r['name'] and g['recipient']['recipient_uei']==r['recipient_uei']
        direct=[g for g in anchors if same(g)]; expanded=[g for g in linked if same(g)];e=expanded[0]['entity']
        docs=list(dict.fromkeys(d['URL'] for g in expanded for d in g['fara_document_links'] if safe_link(d['URL'])))
        results.append({'name':r['name'],'fara_role':r['role'],'fara_agent_registration_number':r['fara_registration'],
            'recipient_uei':r['recipient_uei'],'fara_start':e['start'],'fara_end':e['end'],'active_cached_2026_10_06':e['active_cached_snapshot'],
            'direct_address_groups':len(direct),'direct_address_actions':sum(g['transactions'] for g in direct),
            'expanded_same_name_uei_address_groups':len(expanded),'expanded_same_name_uei_actions':r['transactions'],
            'expanded_award_or_idv_ids':r['award_or_idv_count'],'expanded_first_action':r['first_action'],'expanded_last_action':r['last_action'],
            'expanded_net_action_obligations_usd':r['net_matched_action_obligation_usd'],
            'largest_action_obligation_usd':r['largest_action_obligation_usd'],'largest_action_date':r['largest_action_date'],
            'award_example':r['sample_evidence_url'],'fara_discovery_links':'; '.join(docs),
            'identity_reason':'Exact name and building/city anchor; carry only same legal name and recipient UEI; action dates inside FARA interval.',
            'classification':'Descriptive overlap; no disclosure violation established.'})
    csvout('US-RESULTS.csv',results);csvout('compact-candidates.csv',results)
    # No contact, street, postal-code or individual address fields in public tables.
    candidates=[]
    for i,g in enumerate(gs,1):
        e=g['entity'];r=g['recipient']
        candidates.append({'opaque_address_group_id':i,'fara_role':e['role'],'fara_name':e['name'],
            'fara_agent_registration_number':e['registration_number'],'fara_source_file':e['source_file'],'fara_source_line':e['source_line'],
            'recipient_name':r['recipient_name'],'recipient_uei':r['recipient_uei'],'match_method':g['method'],
            'active_cached_2026_10_06':e['active_cached_snapshot'],'fara_start':e['start'],'fara_end':e['end'],
            'candidate_actions':g['transactions'],'temporally_overlapping_candidate_actions':g['temporally_overlapping_transactions'],
            'classification':'Candidate only; names do not establish identity. See US-RESULTS.csv for separately corroborated keys.'})
    csvout('CANDIDATE-SCREEN.csv',candidates)
    cg=defaultdict(list)
    for c in ca:
        e=c['fara_entity'];cg[(e['role'],e['registration_number'],e['name'])].append(c)
    cr=[]
    for (role,reg,name),items in cg.items():
        e=items[0]['fara_entity'];cr.append({'name':name,'fara_role':role,'fara_agent_registration_number':reg,
            'fara_start':e['start'],'fara_end':e['end'],'canadian_role':items[0]['canadian_role'],
            'ocl_version_pairs':len(items),'ocl_version_ids':'; '.join(c['registration']['REG_ID_ENR'] for c in items),
            'ocl_client_numbers':'; '.join(sorted({c['registration']['CLIENT_ORG_CORP_NUM'] for c in items})),
            'ocl_effective_dates':'; '.join(c['registration']['EFFECTIVE_DATE_VIGUEUR'] for c in items),
            'source_links':'; '.join(c['registration_url'] for c in items),
            'classification':'Active cached identity overlap; no grant receipt reconciliation or disclosure violation established.'})
    csvout('CANADA-RESULTS.csv',cr)
    ex=json.loads((BASE/'exclusions.json').read_text())
    save('EXCLUSIONS.json',{'malformed_or_missing_date_fara_principal_rows':[
        {'source_file':x['file'],'source_line':x['line'],'reason':x['reason'],'principal_name_discovery_only':x['raw'].get('Foreign Principal','')} for x in ex],
        'other_exclusions':['Blank recipient names: 3 actions, retained in transaction census but not name matching.',
            'Canadian supplier placeholders such as None removed before matching.',
            'Weaker legal-form and uncorroborated name matches not promoted.',
            'Termination-day actions conservatively outside interval.',
            'Four active US address pairs have no FY2025 action inside the recorded FARA interval.',
            'FARA catalogue has 32 anomalous URL pointers; no PDF was read or repaired.'],
        'privacy':'Raw malformed rows and address fields omitted from this public exclusion ledger; source line and input hash permit review.'})
    manifests=json.loads((BASE/'input-manifest.json').read_text())+json.loads((BASE/'canada-input-manifest.json').read_text())
    urls={Path(x['url']).name:x['url'] for x in json.loads((BASE/'retrieval-ledger.json').read_text())['requests']}
    urls.update({'canada-registrations.zip':'https://lobbycanada.gc.ca/media/zwcjycef/registrations_enregistrements_ocl_cal.zip','canada-dictionary.xlsx':'https://lobbycanada.gc.ca/media/hcvmsu4e/dictionary_registrations_dictionnaire_enregistrements.xlsx','canada-contract-history.csv':'https://canadabuys.canada.ca/opendata/pub/2026-2027-contractHistory-contratsOctroyes.csv'})
    unique={m['path']:m for m in manifests}
    for m in unique.values():m['source_url']=urls.get(Path(m['path']).name,'Repository input or pinned recovered baseline; see TECHNICAL-ANNEX.md')
    save('SOURCE-MANIFEST.json',{'inputs':list(unique.values()),'new_bulk_inputs_published':False,
        'scope':'Fingerprints identify the inspected sources. Large inputs and copied prior dossiers are intentionally not included.'})
    save('SOURCE-LEDGER.json',json.loads((BASE/'retrieval-ledger.json').read_text()))
    us=json.loads((BASE/'us-summary.json').read_text());can=json.loads((BASE/'canada-summary.json').read_text());review=json.loads((BASE/'review-summary.json').read_text())
    save('RESULTS-SUMMARY.json',{'us':us,'canada':can,'review':review,'direct_scope':{'address_groups':14,'actions':79,'award_or_idv_ids':37},
        'expanded_scope':{'same_name_uei_address_groups':21,'recipient_role_registration_keys':12,'actions':2310,'award_or_idv_ids':1719},
        'ccc_expanded_actions':2184,'external_spend_usd':0,'classification':'No disclosure violation established.'})
    lines=['# Corroborated overlaps: direct anchors and expanded recipient actions','','These are descriptive, source-backed bulk-record overlaps, not accusations. Original FARA PDFs were inaccessible. A principal’s FARA number belongs to its agent registration, not to a unique principal ID. Amounts are obligations, not payments.','',
        'Every US row below separates the narrow direct-building scope from the expanded exact-name-and-UEI scope. The totals are **79 direct actions** and **2,310 expanded actions**. The direct actions are included in the expanded count; do not add them.','']
    for r in results:
        lines += [f'## {r["name"]}',f'Role: {r["fara_role"]}; FARA agent registration {r["fara_agent_registration_number"]}; recipient UEI `{r["recipient_uei"]}`. Recorded FARA interval: {r["fara_start"]} through {r["fara_end"] or "no termination in cached source"}.',
            f'Direct scope: **{r["direct_address_actions"]} actions**, {r["direct_address_groups"]} building/address groups. Expanded same-name/UEI scope: **{r["expanded_same_name_uei_actions"]} actions**, {r["expanded_same_name_uei_address_groups"]} groups and {r["expanded_award_or_idv_ids"]} award/IDV IDs, {r["expanded_first_action"]}–{r["expanded_last_action"]}.',
            f'Expanded-scope net action obligations: **US${Decimal(r["expanded_net_action_obligations_usd"]):,.2f}**. [Representative award/vehicle]({r["award_example"]}); largest action amount US${Decimal(r["largest_action_obligation_usd"]):,.2f} on {r["largest_action_date"]}. This can be zero or negative; it is not cash received.',
            'Identity reason: '+r['identity_reason'],
            'Ordinary explanation: '+('ordinary federal professional services alongside unrelated foreign-client engagements.' if r['fara_role']=='registrant' else 'international procurement by the named recipient; its separate FARA agent is not the contracting recipient.'),
            'Next missing evidence: the exact dated and applicable ownership representation plus a contradictory control fact, or award-specific lobbying/payment facts and operative clause. None was recovered. FARA status alone does not provide that contradiction.',
            'FARA catalogue discovery links (not PDFs read): '+('; '.join(r['fara_discovery_links'].split('; ')[:2]) or 'registration-number catalogue lookup')+'.','']
    lines += ['## Canada','','11 active address-corroborated version pairs represent three names and four FARA role/registration keys. NWMO is recorded in two roles; this does not create a second organization. Consultant-firm matches do not transfer FARA status to their clients.','']
    for r in cr:
        lines += [f'### {r["name"]} — {r["fara_role"]}',f'FARA agent registration {r["fara_agent_registration_number"]}; {r["ocl_version_pairs"]} OCL pairs, version IDs {r["ocl_version_ids"]}; Canadian role {r["canadian_role"]}. FARA starts {r["fara_start"]}; relevant OCL effective dates {r["ocl_effective_dates"]}. Organizational address corroboration was reviewed locally; bulk street/contact fields are not republished.',
            'OCL discovery links, constructed from sourced client and version IDs: '+r['source_links'],
            'No procurement/funding-disclosure inconsistency is alleged. A valid grant comparison needs actual qualifying receipts, the completed financial year and relevant amendments.','']
    lines += ['NWMO’s registration already reports C$3,547,322.81 from AECL and C$1,876,192.54 from NRCan for its financial year ended 2025-12-31. These total C$5,423,515.35 in self-reported funding; they are not independently verified grant payments.','Porter O’Brien’s Port Saint John client registration lists C$3,096,663.77 from Government of Canada; that is the client’s disclosure, not the consultant’s fees. Burke’s Canadian American Business Council client registration says No to qualifying government funding, but no contradictory receipt record was recovered.']
    (BASE/'DOSSIERS.md').write_text('\n\n'.join(lines)+'\n')
    # Keep the published amount narrative consistent with the explicit two-scope tables.
    p=BASE/'AMOUNTS.md';s=p.read_text()
    scope='\nScope: the table below uses 2,310 expanded same-name/UEI actions. Its 79 direct-address anchor actions are included in that count, not added to it. The expanded figures are changes in obligations, not payments.\n'
    if scope.strip() not in s:s=s.replace('\n\n', '\n'+scope+'\n',1)
    p.write_text(s)
    print('Sanitized publication tables: 12 US keys, 4 Canadian role keys, 273 candidate pairs; 79 direct / 2310 expanded actions.')
if __name__=='__main__':main()
