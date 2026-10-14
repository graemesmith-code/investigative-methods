"""Verify saved evidence and result counts without redownloading or broad reanalysis.
Also compare historical archive provenance to the recovered original OFAC audit.
"""
from reproduce import *
from decimal import Decimal
def main():
    s=json.loads((BASE/'us-summary.json').read_text())
    old=json.loads((BASE/'evidence/prior-ofac-screen-summary.json').read_text())
    assert s['archive_sha256']==old['archive_sha256']
    assert s['contract']['raw_rows']==s['contract']['unique_transactions']==old['unique_transactions']==6639176
    assert s['distinct_nonblank_raw_recipient_names']==old['distinct_recipient_names']==101379
    assert sum(x['rows'] for x in s['files'])==6639176 and len(s['files'])==7
    recipients=[]
    for line in (BASE/'us-recipient-index.jsonl').open():recipients.append(json.loads(line))
    assert len(recipients)==s['recipient_name_identifier_address_groups']==126350
    assert sum(r['transactions'] for r in recipients)+s['contract']['blank_recipient_name']==6639176
    assert len({r['recipient_name'] for r in recipients})==101379
    tids=set();keys=set();es=json.loads((BASE/'fara-entities.json').read_text())
    for line in (BASE/'us-candidate-transactions.jsonl').open():
        r=json.loads(line);t=r['transaction'];tids.add(t['contract_transaction_unique_key'])
        keys.add((r['entity_index'],t['recipient_name'],t['recipient_uei'],t['recipient_duns'],t['recipient_address_line_1'],t['recipient_city_name'],t['recipient_state_code'],t['recipient_country_code']))
        e=es[r['entity_index']];dt=t['action_date'][:10]
        assert r['temporal_overlap']==(e['start']<=dt and (not e['end'] or dt<e['end']))
    assert len(tids)==s['contract']['candidate_unique_transactions']==10898
    assert len(keys)==s['candidate_groups']==273
    gs=json.loads((BASE/'us-candidates.json').read_text())
    assert len(gs)==273
    assert Counter(g['method'] for g in gs)=={'normalized_exact':200,'terminal_legal_form_removed':73}
    assert sum(g['entity']['active_cached_snapshot'] for g in gs)==35
    assert len(list(csv.DictReader((BASE/'us-candidates.csv').open())))==273
    strong=json.loads((BASE/'us-source-backed-overlaps.json').read_text())
    assert len(strong)==14 and sum(g['transactions'] for g in strong)==79
    assert all(g['method']=='normalized_exact' and g['temporally_overlapping_transactions'] for g in strong)
    linked=json.loads((BASE/'us-address-anchored-uei-overlaps.json').read_text())
    assert len(linked)==21 and sum(g['temporally_overlapping_transactions'] for g in linked)==2310
    amounts=json.loads((BASE/'amounts.json').read_text())
    assert len(amounts)==12 and sum(x['transactions'] for x in amounts)==2310
    for x in amounts:
        assert Decimal(x['gross_positive_action_obligation_usd'])+Decimal(x['gross_negative_action_obligation_usd'])==Decimal(x['net_matched_action_obligation_usd'])
        assert x['positive_actions']+x['negative_actions']+x['zero_actions']==x['transactions']
    ca=json.loads((BASE/'canada-fara-contract-candidates.json').read_text())
    assert len(ca)==7 and len({x['source_line'] for x in ca})==4
    assert not any(x['temporal_overlap'] for x in ca)
    assert not any(norm(x['matched_supplier_name']) in ('none','null','') for x in ca)
    cactive=json.loads((BASE/'canada-source-backed-active-overlaps.json').read_text())
    assert len(cactive)==11 and len({x['fara_entity']['name'] for x in cactive})==3
    assert len({(x['fara_entity']['role'],x['fara_entity']['registration_number'],x['fara_entity']['name']) for x in cactive})==4
    crows=[json.loads(l) for l in (BASE/'canada-lobbying-contract-candidates.jsonl').open()]
    assert len(crows)==6646 and len({x['source_line'] for x in crows})==254
    assert sum(x['temporal_overlap'] for x in crows)==473
    good=[x for x in crows if x['temporal_overlap'] and x['identity_level']!='name_candidate_only']
    assert len(good)==112 and len({x['source_line'] for x in good})==48
    # Public metadata anomalies are retained as discovery pointers, not silently repaired.
    anomalies=[]
    for r in csv.DictReader((ROOT/'research/FARA_All_RegistrantDocs.csv').open(encoding='cp1252')):
        m=re.search(r'-(\d{8})-\d+\.pdf$',r['URL'])
        if '-0-0.pdf' in r['URL'] or (m and m[1]>SNAPSHOT.replace('-','')):
            anomalies.append(r)
    save('catalogue-url-anomalies.json',anomalies)
    save('followup-validation.json',{'verification':'Passed against saved evidence; Canada and review scripts also rerun with identical summaries.',
        'us_archive_rows':6639176,'us_recipient_names':101379,'candidate_pairs':273,'exact_candidates':200,'weaker_candidates':73,
        'active_candidate_pairs':35,'direct_address_anchors':14,'uei_bridged_pairs':21,'corroborated_keys':12,
        'overlapping_us_actions':2310,'canadian_active_address_pairs':11,'canadian_names':3,'canadian_role_keys':4,
        'canadian_contract_temporal_fara_matches':0,'catalogue_url_anomalies':len(anomalies),'external_spend_usd':0})
    print('All census, candidate, temporal, UEI, amount and Canadian output checks passed; no broad rerun or retrieval.')
if __name__=='__main__':main()
