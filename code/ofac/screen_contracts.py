"""Screen a USAspending CSV ZIP against the saved OFAC Entity names.
Usage: python3 screen_contracts.py /path/to/contracts.zip /path/to/output
No external dependencies, paid services or model calls.
Matches are leads, NOT confirmed identities or sanctions violations.
"""
from pathlib import Path
from collections import defaultdict, Counter
import csv, io, json, re, sys, unicodedata, zipfile, hashlib

BASE = Path(__file__).resolve().parent
START, END = '2024-10-01', '2025-09-30'
def normalize(s):
    return re.sub(r'[^\w]+', ' ', unicodedata.normalize('NFKC', s or '').casefold()).strip()
# Only terminal, unambiguous legal forms. This is a separate weaker matching pass.
SUFFIX = re.compile(r'\s+(?:incorporated|inc|limited|ltd|llc|l l c|corporation|corp|plc|p l c|gmbh)$')
def without_suffix(s):
    s = normalize(s)
    previous = None
    while previous != s:
        previous = s
        s = SUFFIX.sub('', s)
    return s

def main():
    archive, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    names = json.loads((BASE / 'names.json').read_text())
    entities = {e['ofac_id']: e for e in json.loads((BASE / 'entities.json').read_text())}
    exact, relaxed = defaultdict(list), defaultdict(list)
    for n in names:
        exact[normalize(n['name'])].append(n)
        k = without_suffix(n['name'])
        if len(k) >= 5:
            relaxed[k].append(n)
    summary = {'scope': 'FY2025 contract archive, all agencies: A/B/C/D contract actions and rows with blank award_type_code (including IDVs), matched against current OFAC Entity entries only',
               'start_date': START, 'end_date': END, 'raw_rows': 0, 'unique_transactions': 0,
               'duplicate_transactions': 0, 'out_of_period_rows': 0, 'excluded_award_types': {}, 'blank_recipient_names': 0,
               'blank_transaction_ids': 0, 'files': [], 'match_methods': {},
               'limitations': ['Current OFAC list omits entities delisted before the snapshot.',
                   'No historical designation dates or legal authorisations have been checked.',
                   'Contract actions include amendments, corrections and deobligations, not only new awards.',
                   'Name matches do not establish identity. No subsidiary or beneficial-owner matching.',
                   'No payment totals are inferred from contract values or obligations.']}
    seen, recipients, matched_transactions, matched_awards = set(), set(), set(), set()
    groups = {}
    required = {'contract_transaction_unique_key','contract_award_unique_key','recipient_name','action_date'}
    min_date, max_date = '9999', ''
    with (out / 'candidate-transactions.jsonl').open('w') as candidate_file, zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            if not member.filename.lower().endswith('.csv'):
                continue
            with z.open(member) as binary:
                reader = csv.DictReader(io.TextIOWrapper(binary, encoding='utf-8-sig', newline=''))
                if not required.issubset(reader.fieldnames or []):
                    raise ValueError(f'Unexpected CSV schema {member.filename}: {reader.fieldnames}')
                file_rows = 0
                for row in reader:
                    file_rows += 1
                    summary['raw_rows'] += 1
                    award_type = row.get('award_type_code', '')
                    if award_type and award_type not in {'A','B','C','D'}:
                        summary['excluded_award_types'][award_type] = summary['excluded_award_types'].get(award_type,0)+1
                        continue
                    date = row['action_date'][:10]
                    if not START <= date <= END:
                        summary['out_of_period_rows'] += 1
                        continue
                    min_date, max_date = min(min_date, date), max(max_date, date)
                    tid = row['contract_transaction_unique_key']
                    if not tid:
                        summary['blank_transaction_ids'] += 1
                        tid = hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()
                    if tid in seen:
                        summary['duplicate_transactions'] += 1
                        continue
                    seen.add(tid)
                    recipient = row['recipient_name']
                    if not recipient.strip():
                        summary['blank_recipient_names'] += 1
                        continue
                    recipients.add(recipient)
                    hits = exact.get(normalize(recipient), [])
                    method = 'normalized_exact'
                    if not hits:
                        hits = relaxed.get(without_suffix(recipient), [])
                        method = 'legal_suffix_removed'
                    by_entity = defaultdict(list)
                    for hit in hits:
                        by_entity[hit['ofac_id']].append(hit)
                    for uid, evidence in by_entity.items():
                        matched_transactions.add(tid)
                        matched_awards.add(row['contract_award_unique_key'])
                        gkey = (uid, recipient, row.get('recipient_uei',''))
                        if gkey not in groups:
                            groups[gkey] = {'ofac_id':uid,'ofac_primary_name':entities[uid]['primary_name'],
                                'recipient_name':recipient,'recipient_uei':row.get('recipient_uei',''),
                                'method':method,'matching_names':evidence,'ofac_record':entities[uid],
                                'transactions':0,'award_ids':set(),'locations':set(),'agencies':set(),
                                'first_action':date,'last_action':date,'sample_transactions':[]}
                        g=groups[gkey]
                        g['transactions'] += 1
                        g['award_ids'].add(row['contract_award_unique_key'])
                        g['locations'].add(tuple(row.get(k,'') for k in ['recipient_address_line_1','recipient_city_name','recipient_state_code','recipient_country_code']))
                        g['agencies'].add(row.get('awarding_agency_name',''))
                        g['first_action'],g['last_action']=min(g['first_action'],date),max(g['last_action'],date)
                        if len(g['sample_transactions'])<3: g['sample_transactions'].append(row)
                        candidate_file.write(json.dumps({'ofac_id':uid,'method':method,'matching_names':evidence,'transaction':row},ensure_ascii=False)+'\n')
                summary['files'].append({'filename':member.filename,'rows':file_rows,'columns':reader.fieldnames})
                print(f'Finished {member.filename}: {file_rows:,} rows', flush=True)
    assert summary['files'], 'No contract CSV found'
    assert not summary['out_of_period_rows'], 'Unexpected dates: inspect before claiming full screen'
    results=[]
    for g in groups.values():
        for k in ['award_ids','locations','agencies']: g[k]=sorted(g[k])
        results.append(g)
    summary.update(unique_transactions=len(seen),distinct_recipient_names=len(recipients),
                   candidate_groups=len(results),matched_unique_transactions=len(matched_transactions),
                   matched_unique_awards=len(matched_awards),earliest_action=min_date,latest_action=max_date,
                   match_methods=dict(Counter(g['method'] for g in results)))
    with archive.open('rb') as f:
        summary['archive_sha256']=hashlib.file_digest(f,'sha256').hexdigest()
    (out/'candidate-groups.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
    (out/'screen-summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
    for g in results:
        print(json.dumps({k:g[k] for k in ['ofac_id','ofac_primary_name','recipient_name','method','transactions','locations']},ensure_ascii=False))

if __name__ == '__main__': main()
