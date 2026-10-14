"""$0 local FARA / FY2025 prime contract screen. Python standard library only.
Usage: python reproduce.py /path/to/FY2025_All_Contracts_Full_20260906.zip
The cached FARA data is evaluated as-of 2026-10-06, not claimed current.
Exact normalized names are candidates; terminal legal-form removal is weaker.
No fuzzy, ownership, affiliate, campaign-money or indirect-client inference.
"""
import csv, io, json, re, unicodedata, zipfile, hashlib, sys
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
SNAPSHOT='2026-10-06'
def norm(s):
    return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode().lower()).strip()
SUFFIX=re.compile(r'\s+(?:incorporated|inc|limited|ltd|llc|l l c|corporation|corp|plc|p l c|llp|l l p|gmbh)$')
def relaxed(s):
    s=norm(s)
    while SUFFIX.search(s): s=SUFFIX.sub('',s)
    return s
def date(s):
    if not s:return ''
    return datetime.strptime(s.strip(),'%m/%d/%Y').strftime('%Y-%m-%d')
def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(name,obj): (BASE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
def entities():
    result=[]; counts={}; exclusions=[]
    for fn,role in [('FARA_All_Registrants.csv','registrant'),('FARA_All_ForeignPrincipals.csv','foreign_principal')]:
        rows=list(csv.DictReader((ROOT/'research'/fn).open(encoding='cp1252')))
        counts[role]={'raw_rows':len(rows)}
        for line,r in enumerate(rows,2):
            try:
                if None in r or not r['Registration Number'].isdigit():raise ValueError('malformed CSV/schema')
                start=date(r['Registration Date' if role=='registrant' else 'Foreign Principal Registration Date'])
                end=date(r['Termination Date' if role=='registrant' else 'Foreign Principal Termination Date'])
                if not start:raise ValueError('missing registration date')
            except ValueError as e:
                exclusions.append({'file':fn,'line':line,'reason':str(e),'raw':r});continue
            name=r['Name' if role=='registrant' else 'Foreign Principal']
            result.append({'role':role,'name':name,'registration_number':r['Registration Number'],
                'start':start,'end':end,'active_cached_snapshot':start<=SNAPSHOT and (not end or end>SNAPSHOT),
                'registrant_name':r.get('Registrant Name',name),'country_represented':r.get('Country/Location Represented',''),
                'address':r['Address 1'],'address_2':r['Address 2'],'city':r['City'],'state':r['State'],'zip':r['Zip'],
                'source_file':fn,'source_line':line,'business_name':r.get('Business Name','')})
        es=[e for e in result if e['role']==role]
        counts[role].update(usable_rows=len(es),active_cached_snapshot_rows=sum(e['active_cached_snapshot'] for e in es),
            unique_normalized_names=len({norm(e['name']) for e in es}))
    counts['documents_rows']=sum(1 for _ in csv.DictReader((ROOT/'research/FARA_All_RegistrantDocs.csv').open(encoding='cp1252')))
    save('fara-entities.json',result);save('exclusions.json',exclusions);save('fara-counts.json',counts)
    return result,counts
def main():
    es,counts=entities();exact=defaultdict(list);weak=defaultdict(list)
    for i,e in enumerate(es):
        exact[norm(e['name'])].append(i)
        if len(relaxed(e['name']))>=8:weak[relaxed(e['name'])].append(i)
    archive=Path(sys.argv[1]); groups={};recipients={};names=set(); seen=set();stats=Counter(); files=[]
    fields=['contract_transaction_unique_key','contract_award_unique_key','award_id_piid','parent_award_id_piid',
        'recipient_name','recipient_uei','recipient_duns','recipient_parent_name','recipient_parent_uei',
        'recipient_address_line_1','recipient_address_line_2','recipient_city_name','recipient_state_code',
        'recipient_zip_4_code','recipient_country_code','action_date','period_of_performance_start_date',
        'period_of_performance_current_end_date','award_type_code','awarding_agency_name','funding_agency_name',
        'federal_action_obligation','foreign_funding','foreign_funding_description']
    with (BASE/'us-candidate-transactions.jsonl').open('w') as out,zipfile.ZipFile(archive) as z:
        for m in z.infolist():
            if not m.filename.endswith('.csv'):continue
            n=0
            with z.open(m) as f:
                reader=csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig',newline=''))
                for r in reader:
                    n+=1;stats['raw_rows']+=1
                    if r['award_type_code'] not in ('','A','B','C','D'):stats['excluded_type']+=1;continue
                    dt=r['action_date'][:10]
                    if not '2024-10-01'<=dt<='2025-09-30':stats['excluded_date']+=1;continue
                    tid=r['contract_transaction_unique_key']
                    if not tid:stats['missing_transaction_id']+=1;continue
                    if tid in seen:stats['duplicate_transactions']+=1;continue
                    seen.add(tid);stats['unique_transactions']+=1
                    name=r['recipient_name']; names.add(name)
                    if not name.strip():stats['blank_recipient_name']+=1;continue
                    key=(name,r.get('recipient_uei',''),r.get('recipient_duns',''),r.get('recipient_address_line_1',''),r.get('recipient_city_name',''),r.get('recipient_state_code',''),r.get('recipient_country_code',''))
                    if key not in recipients:
                        recipients[key]={k:r.get(k,'') for k in fields if k.startswith('recipient_')}
                        recipients[key].update(first_action=dt,last_action=dt,transactions=0)
                    rec=recipients[key];rec['transactions']+=1;rec['first_action']=min(rec['first_action'],dt);rec['last_action']=max(rec['last_action'],dt)
                    nk=norm(name);hits=exact.get(nk,[]);method='normalized_exact'
                    if not hits:hits=weak.get(relaxed(name),[]);method='terminal_legal_form_removed'
                    if not hits:continue
                    stats['candidate_unique_transactions']+=1
                    for i in hits:
                        e=es[i];gkey=(i,key);overlap=e['start']<=dt and (not e['end'] or dt<e['end'])
                        city=bool(norm(e['city'])) and norm(e['city'])==norm(r.get('recipient_city_name',''))
                        state=bool(e['state']) and e['state'].strip()==r.get('recipient_state_code','')
                        street=bool(norm(e['address'])) and norm(e['address'])==norm(r.get('recipient_address_line_1',''))
                        # City/state is context only. A precise street + city/state corroborates identity.
                        corroborated=method=='normalized_exact' and street and city and state
                        if gkey not in groups:
                            groups[gkey]={'entity':e,'recipient':{k:r.get(k,'') for k in fields if k.startswith('recipient_')},
                                'method':method,'street_equal':street,'city_equal':city,'state_equal':state,
                                'identity_level':'exact_name_street_city_state' if corroborated else 'name_candidate_only',
                                'transactions':0,'temporally_overlapping_transactions':0,'first_action':dt,'last_action':dt,'awards':set(),'sample_transactions':[]}
                        g=groups[gkey];g['transactions']+=1;g['temporally_overlapping_transactions']+=int(overlap)
                        g['first_action']=min(g['first_action'],dt);g['last_action']=max(g['last_action'],dt);g['awards'].add(r['contract_award_unique_key'])
                        if len(g['sample_transactions'])<2:g['sample_transactions'].append({k:r.get(k,'') for k in fields})
                        out.write(json.dumps({'entity_index':i,'method':method,'temporal_overlap':overlap,'transaction':{k:r.get(k,'') for k in fields}},ensure_ascii=False)+'\n')
            files.append({'member':m.filename,'rows':n});print(m.filename,n,'candidate groups',len(groups),flush=True)
    ds=defaultdict(list)
    for r in csv.DictReader((ROOT/'research/FARA_All_RegistrantDocs.csv').open(encoding='cp1252')):
        if r['Document Type'] in ('Registration Statement','Exhibit AB','Exhibit A','Exhibit-AB','Supplemental Statement','Amendment'):ds[r['Registration Number']].append(r)
    output=[]
    for g in groups.values():
        g['awards']=sorted(g['awards']);e=g['entity']; docs=ds[e['registration_number']]
        relevant=[d for d in docs if e['role']=='registrant' or norm(d['Foreign Principal Name'])==norm(e['name'])]
        g['fara_document_links']=[d for d in sorted(relevant,key=lambda d:date(d['Date Stamped']),reverse=True)[:5]]
        output.append(g)
    save('us-candidates.json',output)
    with (BASE/'us-candidates.csv').open('w') as f:
        cols=['role','fara_name','fara_registration','fara_start','fara_end','active_cached_snapshot','recipient_name','recipient_uei','recipient_city','recipient_state','method','identity_level','transactions','temporal_transactions','award_count','first_action','last_action','fara_links']
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
        for g in output:
            e=g['entity'];r=g['recipient'];w.writerow(dict(zip(cols,[e['role'],e['name'],e['registration_number'],e['start'],e['end'],e['active_cached_snapshot'],r['recipient_name'],r['recipient_uei'],r['recipient_city_name'],r['recipient_state_code'],g['method'],g['identity_level'],g['transactions'],g['temporally_overlapping_transactions'],len(g['awards']),g['first_action'],g['last_action'],'; '.join(d['URL'] for d in g['fara_document_links'])])))
    with (BASE/'us-recipient-index.jsonl').open('w') as f:
        for r in recipients.values():f.write(json.dumps(r,ensure_ascii=False)+'\n')
    summary={'snapshot':SNAPSHOT,'fara':counts,'contract':dict(stats),'distinct_nonblank_raw_recipient_names':len(names-{''}),
        'recipient_name_identifier_address_groups':len(recipients),'candidate_groups':len(output),
        'candidate_groups_by_role':dict(Counter(g['entity']['role'] for g in output)),
        'active_snapshot_candidate_groups_by_role':dict(Counter(g['entity']['role'] for g in output if g['entity']['active_cached_snapshot'])),
        'corroborated_temporal_groups_by_role':dict(Counter(g['entity']['role'] for g in output if g['identity_level']=='exact_name_street_city_state' and g['temporally_overlapping_transactions'])),
        'files':files,'archive_sha256':digest(archive),'external_spend_usd':0,'grants_screened':False}
    save('us-summary.json',summary)
    save('input-manifest.json',[{'path':str(p),'bytes':p.stat().st_size,'sha256':digest(p)} for p in [archive,*sorted((ROOT/'research').glob('FARA*.csv')),ROOT/'experiments/ofac-step1-2026-09-18.zip',ROOT/'experiments/sanctions-screen-evidence-2026-09-18.zip']])
    print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':main()
