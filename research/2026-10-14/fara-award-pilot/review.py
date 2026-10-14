"""Conservative second pass: standard postal abbreviations, same named entity/building.
Unit differences remain visible. Address changes without a shared building are unconfirmed.
Not a beneficial ownership or affiliate join. Run after reproduce.py and canada.py.
"""
from reproduce import *
def address(s):
    # FARA occasionally writes unit before house number: 1100 - 50 O'Connor Street.
    s=re.sub(r'^\s*\d+\s*-\s*(\d+\s)',r'\1',s)
    s=norm(s)
    words={'avenue':'ave','street':'st','boulevard':'blvd','road':'rd','east':'e','west':'w','north':'n','south':'s',
        'suite':'ste','floor':'fl','fourth':'4th'}
    s=' '.join(words.get(t,t) for t in s.split())
    return re.split(r'\s+(?:ste|fl|\d+(?:st|nd|rd|th)\s+fl)\b',s)[0].strip()
def city(s):return re.sub(r'^st\s','saint ',norm(s))
def main():
    gs=json.loads((BASE/'us-candidates.json').read_text());promoted=[]
    for g in gs:
        e=g['entity'];r=g['recipient']
        reason=[]
        if g['method']=='normalized_exact' and address(e['address'])==address(r['recipient_address_line_1']) and city(e['city'])==city(r['recipient_city_name']) and (not e['state'] or e['state'].strip()==r['recipient_state_code']) and len(address(e['address']))>8:
            reason=['exact normalized legal name','same building street after controlled postal abbreviations','same city','same state where supplied']
        g['review_identity_reasons']=reason
        g['source_backed_identity_temporal']=bool(reason and g['temporally_overlapping_transactions'])
        if g['source_backed_identity_temporal']:promoted.append(g)
    save('us-reviewed-candidates.json',gs);save('us-source-backed-overlaps.json',promoted)
    # Once an address anchors a FARA entity to a recipient UEI, carry that bridge
    # only to the SAME legal name and UEI in this recovered archive. This permits
    # address changes without treating unverified names/affiliates as identical.
    anchors={(g['entity']['role'],g['entity']['registration_number'],g['entity']['name'],g['recipient']['recipient_uei']) for g in promoted if g['recipient']['recipient_uei']}
    linked=[]
    for g in gs:
        k=(g['entity']['role'],g['entity']['registration_number'],g['entity']['name'],g['recipient']['recipient_uei'])
        if k in anchors and g['temporally_overlapping_transactions']:
            g['stable_uei_bridge_reason']='Same exact legal name and UEI as address-corroborated anchor in this archive; not a FARA-supplied UEI.'
            linked.append(g)
    save('us-address-anchored-uei-overlaps.json',linked)
    # Keep matching addresses within each actual relationship role. Consultant firm's
    # own registration is never attributed to its Canadian clients.
    cs=json.loads((BASE/'canada-fara-lobbying-candidates.json').read_text());cp=[]
    for c in cs:
        if not c['active_in_both_cached_snapshots']:continue
        e=c['fara_entity'];r=c['registration'];name=c['canadian_name']
        a=r['FIRM_ADDRESS_ADRESSE_FIRME'] if c['canadian_role']=='consultant_firm' else r['CLIENT_ORG_CORP_ADDRESS_ADRESSE_CLIENT_ORG_CORP']
        ea=e['address'];street=ea.split(',')[0]
        first=a.split(',')[0]
        street_match=address(street)==address(first) and len(address(street))>8
        fara_city=e['city']
        if ea.endswith(', Fredericton'):fara_city='Fredericton'
        city_match=bool(fara_city) and city(fara_city) in city(a)
        if street_match and city_match:
            c['review_identity_reasons']=['exact normalized entity name','same street/building after controlled abbreviations','same city in full address','overlapping active cached intervals']
            cp.append(c)
    save('canada-source-backed-active-overlaps.json',cp)
    summary={'us_source_backed_identity_temporal_recipient_address_groups':len(promoted),
        'us_source_backed_active_cached_groups':sum(g['entity']['active_cached_snapshot'] for g in promoted),
        'us_source_backed_by_role':dict(Counter(g['entity']['role'] for g in promoted)),
        'us_address_anchored_stable_uei_address_groups':len(linked),
        'us_address_anchored_stable_uei_role_registration_recipient_keys':len(anchors),
        'us_address_anchored_stable_uei_temporal_transactions':sum(g['temporally_overlapping_transactions'] for g in linked),
        'canada_source_backed_active_version_pairs':len(cp),
        'canada_source_backed_active_distinct_fara_role_registrant_name_keys':len({(c['fara_entity']['role'],c['fara_entity']['registration_number'],c['fara_entity']['name']) for c in cp}),
        'note':'Building-level address corroboration; unit fields retained. No crosswalked FARA UEI exists. These are overlaps, not violations.'}
    save('review-summary.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
