"""Bounded Canadian joins; primary registration clients and consultant firms stay separate.
Registration IDs are version IDs; historical versions are retained, never summed as entities.
No claim that contract omissions from government-funding fields are inconsistencies.
"""
from reproduce import *
def clean(v):return '' if v in ('null',None) else v.strip()
def link(r):return 'https://lobbycanada.gc.ca/app/secure/ocl/lrs/do/vwRg?cno='+r['CLIENT_ORG_CORP_NUM']+'&regId='+r['REG_ID_ENR']
def main():
    ev=BASE/'evidence'; es=json.loads((BASE/'fara-entities.json').read_text());idx=defaultdict(list)
    for i,e in enumerate(es):idx[norm(e['name'])].append(i)
    z=zipfile.ZipFile(ev/'canada-registrations.zip')
    with z.open('Registration_PrimaryExport.csv') as f:
        rows=list(csv.DictReader(io.TextIOWrapper(f,encoding='cp1252')))
    # The raw export includes telephone/contact columns. Keep only relevant public entity fields.
    keep=['REG_ID_ENR','REG_TYPE_ENR','REG_NUM_ENR','VERSION_CODE','EN_FIRM_NM_FIRME_AN','FR_FIRM_NM_FIRME',
        'FIRM_ADDRESS_ADRESSE_FIRME','CLIENT_ORG_CORP_PROFIL_ID_PROFIL_CLIENT_ORG_CORP','CLIENT_ORG_CORP_NUM',
        'EN_CLIENT_ORG_CORP_NM_AN','FR_CLIENT_ORG_CORP_NM','CLIENT_ORG_CORP_ADDRESS_ADRESSE_CLIENT_ORG_CORP',
        'EFFECTIVE_DATE_VIGUEUR','END_DATE_FIN','GOVT_FUND_IND_FIN_GOUV','FY_END_DATE_FIN_EXERCICE',
        'PREV_REG_ID_ENR_PRECEDNT','POSTED_DATE_PUBLICATION','PARENT_IND_SOC_MERE','DIRECT_INT_IND_INT_DIRECT']
    rows=[{k:clean(r[k]) for k in keep} for r in rows]
    lidx=defaultdict(list);fh=[]
    for r in rows:
        start,end=r['EFFECTIVE_DATE_VIGUEUR'],r['END_DATE_FIN']
        r['active_cached_snapshot']=bool(start and start<='2026-10-14' and (not end or end>'2026-10-14'))
        role_names=[('registered_client',r['EN_CLIENT_ORG_CORP_NM_AN'],r['CLIENT_ORG_CORP_ADDRESS_ADRESSE_CLIENT_ORG_CORP'])]
        if r['REG_TYPE_ENR']=='1':role_names.append(('consultant_firm',r['EN_FIRM_NM_FIRME_AN'],r['FIRM_ADDRESS_ADRESSE_FIRME']))
        for role,name,address in role_names:
            if not name:continue
            lidx[norm(name)].append((r,role,name,address))
            for i in idx.get(norm(name),[]):
                e=es[i]; common_start=max(e['start'],start or '9999');common_end=min(e['end'] or '9999',end or '9999')
                addr=bool(norm(e['address'])) and norm(e['address']) in norm(address)
                fh.append({'fara_entity':e,'canadian_role':role,'canadian_name':name,'registration':r,
                    'match_method':'normalized_exact','address_contains_fara_street':addr,
                    'historical_intervals_overlap':common_start<common_end,'active_in_both_cached_snapshots':e['active_cached_snapshot'] and r['active_cached_snapshot'],
                    'identity_level':'name_candidate_only','registration_url':link(r)})
    save('canada-fara-lobbying-candidates.json',fh)
    cr=list(csv.DictReader((ev/'canada-contract-history.csv').open(encoding='utf-8-sig')))
    cf=[];lc=[];matched_contracts=set();fara_contracts=set()
    for line,r in enumerate(cr,2):
        names={r.get(k,'').strip() for k in ['supplierLegalName-nomLegalFournisseur-eng','supplierLegalName-nomLegalFournisseur-fra','supplierStandardizedName-nomNormaliseFournisseur-eng','supplierOperatingName-nomCommercialFournisseur-eng']}
        names={n for n in names if norm(n) not in ('','none','null','n a','unknown','not applicable')}
        dt=r['contractAwardDate-dateAttributionContrat'][:10]
        street=r['supplierAddressLine-ligneAdresseFournisseur-eng'];city=r['supplierAddressCity-fournisseurAdresseVille-eng'];prov=r['supplierAddressProvince-fournisseurAdresseProvince-eng']
        supplier={'names':sorted(names),'street':street,'city':city,'province':prov,'country':r['supplierAddressCountry-fournisseurAdressePays-eng']}
        seenf=set();seenl=set()
        for name in names:
            for i in idx.get(norm(name),[]):
                if i in seenf:continue
                seenf.add(i);e=es[i];overlap=bool(dt) and e['start']<=dt and (not e['end'] or dt<e['end'])
                corroboration=bool(norm(e['address'])) and norm(e['address'])==norm(street) and norm(e['city'])==norm(city)
                cf.append({'source_line':line,'fara_entity':e,'matched_supplier_name':name,'supplier':supplier,'contract':r,
                    'method':'normalized_exact','identity_level':'exact_name_street_city' if corroboration else 'name_candidate_only','temporal_overlap':overlap})
                fara_contracts.add(line)
            for lr,role,lname,address in lidx.get(norm(name),[]):
                k=(lr['REG_ID_ENR'],role)
                if k in seenl:continue
                seenl.add(k);overlap=bool(dt) and lr['EFFECTIVE_DATE_VIGUEUR']<=dt and (not lr['END_DATE_FIN'] or dt<lr['END_DATE_FIN'])
                corroboration=bool(norm(street)) and norm(street) in norm(address) and bool(norm(city)) and norm(city) in norm(address)
                lc.append({'source_line':line,'supplier':supplier,'contract_reference':r['referenceNumber-numeroReference'],
                    'contract_number':r['contractNumber-numeroContrat'],'award_date':dt,'contract_start':r['contractStartDate-contratDateDebut'],
                    'contract_end':r['contractEndDate-dateFinContrat'],'lobbying_role':role,'registration':lr,
                    'method':'normalized_exact','identity_level':'exact_name_street_city' if corroboration else 'name_candidate_only',
                    'temporal_overlap':overlap,'registration_url':link(lr)})
                matched_contracts.add(line)
    save('canada-fara-contract-candidates.json',cf)
    with (BASE/'canada-lobbying-contract-candidates.jsonl').open('w') as f:
        for x in lc:f.write(json.dumps(x,ensure_ascii=False)+'\n')
    funding=[];matched_ids={x['registration']['REG_ID_ENR'] for x in fh}|{x['registration']['REG_ID_ENR'] for x in lc}
    with z.open('Registration_GovtFundingExport.csv') as f:
        funding_total=0
        for r in csv.DictReader(io.TextIOWrapper(f,encoding='cp1252')):
            funding_total+=1
            if r['REG_ID_ENR'] in matched_ids:funding.append(r)
    save('canada-candidate-funding-disclosures.json',funding)
    summary={'retrieval_date':'2026-10-14','primary_registration_version_rows':len(rows),
        'unique_client_profile_ids':len({r['CLIENT_ORG_CORP_PROFIL_ID_PROFIL_CLIENT_ORG_CORP'] for r in rows}),
        'active_primary_version_rows':sum(r['active_cached_snapshot'] for r in rows),
        'latest_effective_date':max(r['EFFECTIVE_DATE_VIGUEUR'] for r in rows),'latest_posted_date':max(r['POSTED_DATE_PUBLICATION'] for r in rows),
        'fara_lobbying_version_candidate_pairs':len(fh),'fara_lobbying_active_pairs':sum(x['active_in_both_cached_snapshots'] for x in fh),
        'fara_lobbying_pairs_by_roles':dict(Counter((x['fara_entity']['role']+' / '+x['canadian_role']) for x in fh)),
        'contract_history_rows':len(cr),'contract_history_unique_reference_numbers':len({r['referenceNumber-numeroReference'] for r in cr}),
        'contract_history_distinct_legal_supplier_names':len({r['supplierLegalName-nomLegalFournisseur-eng'] for r in cr}),
        'fara_contract_candidate_pairs':len(cf),'fara_matched_contract_rows':len(fara_contracts),
        'lobbying_contract_version_candidate_pairs':len(lc),'lobbying_matched_contract_rows':len(matched_contracts),
        'lobbying_contract_temporal_pairs':sum(x['temporal_overlap'] for x in lc),
        'lobbying_contract_address_temporal_pairs':sum(x['temporal_overlap'] and x['identity_level']!='name_candidate_only' for x in lc),
        'funding_disclosure_rows':funding_total,'candidate_funding_disclosure_rows':len(funding),
        'canadian_grants_screened':False,'all_federal_contracts_screened':False,'external_spend_usd':0}
    save('canada-summary.json',summary);print(json.dumps(summary,indent=2))
    save('canada-input-manifest.json',[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(ev.iterdir()) if p.is_file()])
if __name__=='__main__':main()
