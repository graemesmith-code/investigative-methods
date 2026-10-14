"""Summarize saved action evidence with decimal arithmetic; no network or broad reread.
Amounts are federal_action_obligation changes, not payments or total award ceilings.
"""
from reproduce import *
from decimal import Decimal
def main():
    entities=json.loads((BASE/'fara-entities.json').read_text())
    linked=json.loads((BASE/'us-address-anchored-uei-overlaps.json').read_text())
    wanted={(g['entity']['role'],g['entity']['registration_number'],g['entity']['name'],g['recipient']['recipient_uei']) for g in linked}
    rows=defaultdict(dict)
    for line in (BASE/'us-candidate-transactions.jsonl').open():
        r=json.loads(line);e=entities[r['entity_index']];t=r['transaction']
        k=(e['role'],e['registration_number'],e['name'],t['recipient_uei'])
        if k in wanted and r['temporal_overlap']:rows[k][t['contract_transaction_unique_key']]=t
    result=[]
    for k,ts in sorted(rows.items(),key=lambda pair:pair[0][2]):
        rs=list(ts.values()); amounts=[Decimal(t['federal_action_obligation'] or '0') for t in rs]
        sample=max(rs,key=lambda t:Decimal(t['federal_action_obligation'] or '0'))
        minimum=min(rs,key=lambda t:Decimal(t['federal_action_obligation'] or '0'))
        result.append(dict(zip(['role','fara_registration','name','recipient_uei'],k))|{
            'transactions':len(rs),'award_or_idv_count':len({r['contract_award_unique_key'] for r in rs}),
            'first_action':min(r['action_date'] for r in rs),'last_action':max(r['action_date'] for r in rs),
            'net_matched_action_obligation_usd':str(sum(amounts)),
            'gross_positive_action_obligation_usd':str(sum(x for x in amounts if x>0)),
            'gross_negative_action_obligation_usd':str(sum(x for x in amounts if x<0)),
            'positive_actions':sum(x>0 for x in amounts),'negative_actions':sum(x<0 for x in amounts),'zero_actions':sum(x==0 for x in amounts),
            'largest_action_obligation_usd':sample['federal_action_obligation'],
            'largest_action_date':sample['action_date'],'largest_action_award_id':sample['contract_award_unique_key'],
            'largest_action_agency':sample['awarding_agency_name'],
            'minimum_action_obligation_usd':minimum['federal_action_obligation'],
            'sample_evidence_url':'https://www.usaspending.gov/award/'+sample['contract_award_unique_key'],
            'meaning':'Net changes in obligations on matched FY2025 contract actions inside FARA interval; not cash payments, campaign spending or total award value.'})
    assert len(result)==12 and sum(r['transactions'] for r in result)==2310
    save('amounts.json',result)
    with (BASE/'amounts.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(result[0]),lineterminator="\n");w.writeheader();w.writerows(result)
    lines=['# Amounts and substantive findings','','US dollars, FY2025 matched actions only. Net obligations sum increases and decreases in government commitments. They are not cash paid, a contractor’s revenue, campaign finance, or an award ceiling. Zero-dollar IDV actions show a vehicle modification, not a funded order. No amounts are attributed to a foreign principal merely because a contractor represents it.','',
        '| US recipient | FARA role / number | UEI | Overlapping actions | Net action obligations, USD |','|---|---|---|---:|---:|']
    for r in result:
        lines.append(f'| {r["name"]} | {r["role"]} / {r["fara_registration"]} | {r["recipient_uei"]} | {r["transactions"]} | {Decimal(r["net_matched_action_obligation_usd"]):,.2f} |')
    lines += ['','## Representative US records','']
    for name in ['Canadian Commercial Corporation','Arnold & Porter Kaye Scholer LLP','Daniel J. Edelman, Inc.','Hunton Andrews Kurth LLP','White & Case LLP','The Burson Group LLC']:
        r=next(r for r in result if r['name']==name)
        lines.append(f'- **{name}:** {r["largest_action_date"]}, {r["largest_action_agency"]}, [{r["largest_action_award_id"]}]({r["sample_evidence_url"]}), action obligation **${Decimal(r["largest_action_obligation_usd"]):,.2f}**. FY2025 matched-action net: **${Decimal(r["net_matched_action_obligation_usd"]):,.2f}**. Positive, negative, zero actions: {r["positive_actions"]}, {r["negative_actions"]}, {r["zero_actions"]}.')
    lines += ['','Hunton illustrates why the largest action is not a spending total: a $3.84 million positive action coexists with larger aggregate deobligations, yielding a negative FY2025 net for these matched actions. Burson, Ruder Finn and Fleishman-Hillard have only zero-obligation matched IDV actions. ArentFox and Rational 360 have only negative matched actions; they do not show new positive FY2025 commitments in this slice.','',
        '## Canadian findings and amounts','',
        '- **The Porter O’Brien Agency Inc. — FARA 7537, registrant:** eight active OCL version pairs have the same Churchill Row building and Fredericton address. Other active exact-name pairs use a different building or an apparent street-number difference and are not included in the eight. These are its consultant-firm records, not proof that Port Saint John, University of New Brunswick or its other clients are FARA registrants. OCL version 994044 is a Port Saint John client registration, effective 2026-07-24, reporting a financial year ended 2025-12-31. Its funding entry lists C$3,096,663.77 from Government of Canada. That amount belongs to the client disclosure, not Porter O’Brien’s fees.','',
        '- **Burke Consulting LLC — FARA {BURKE_REG}, registrant:** one active OCL version 974824 matches the supplied organizational address in Grafton, Wisconsin. The client is Canadian American Business Council; the registration is effective 2025-09-19 and says No to government funding. That is a statement about the client’s qualifying funding, not Burke’s federal procurement or its other FARA work. No matched grant-payment record was recovered, so no inconsistency is established.','',
        '- **Nuclear Waste Management Organization — FARA 7186, separately registrant and principal:** OCL version 985554 is an in-house organization registration effective 2026-03-24, at the same St. Clair Avenue East building in Toronto. The financial year ends 2025-12-31; the funding indicator is Yes. Its disclosure lists **C$3,547,322.81 from Atomic Energy of Canada Limited** and **C$1,876,192.54 from Natural Resources Canada**, total **C$5,423,515.35**. The dictionary defines amount as funding in the last completed financial year; the rows also carry the current-year funding-expected flag Y. These are self-reported funding disclosures, not newly verified grant payments, and are not double-counted because NWMO has two FARA roles.','',
        'The Government of Canada funding rows in OCL are self-reported completed-financial-year amounts, with a separate expected-funding flag. They do not establish a procurement discrepancy: procurement is excluded from this disclosure field. The blocked grants file prevents a receipt-versus-disclosure reconciliation.','',
        '## What warrants further reporting?','',
        'The completed pilot supports a descriptive report that some FARA registrants and one named principal also appear as federal recipients. **It identifies no source-backed violation, contradictory declaration, undisclosed campaign finance, or reporting-duty breach.** Ordinary explanations include unrelated federal professional services, legitimate international procurement, existing disclosures, and simple vehicle modifications.','',
        'For an actual US ownership inconsistency, obtain the dated offer/SAM immediate/highest-level ownership representation and a sourced contrary control fact for the same legal entity and operative award-year clause. FARA registration itself is not that contrary fact. For award-specific lobbying, obtain the contract clause version, lobbying payment/activity evidence and any applicable SF-LLL; federal money and FARA work occurring in parallel do not establish prohibited use. For Canada, match actual qualifying grant/nonrepayable-contribution receipts to the registration’s financial year and amendments. None of these gates is presently satisfied. X04 still requires the exact LD-1 and Exhibit A facts; X06 still requires an itemized campaign and exact ad bridge.']
    # Ensure the FARA ID in the Burke narrative comes from the saved corroborated row.
    cs=json.loads((BASE/'canada-source-backed-active-overlaps.json').read_text())
    burke=next(x['fara_entity']['registration_number'] for x in cs if x['fara_entity']['name']=='Burke Consulting LLC')
    lines=[line.replace('{BURKE_REG}',burke) for line in lines]
    (BASE/'AMOUNTS.md').write_text('\n'.join(lines)+'\n')
    print('Reconstructed 12 keys and 2,310 overlapping actions with exact decimal obligations.')
if __name__=='__main__':main()
