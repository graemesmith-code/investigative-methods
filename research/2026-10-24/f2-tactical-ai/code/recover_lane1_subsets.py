#!/usr/bin/env python3
"""Recover exact original 65/36 predicates; never replace a missing denominator.

No network access. Original package is read-only. Output CSV is a lossless,
inspectable data-analysis export, with JSON companions and reproducibility audit.
"""
import argparse, csv, gzip, hashlib, json, re, sqlite3
from collections import Counter
from decimal import Decimal
from pathlib import Path

PHASE = r'phase\s*(?:iii|3)\b'
CUTOFF = '2024-01-01'
FIN_HASH = '366c6294aa7d703e37affcab94ad835876943e1d6d6a5565867d5a14728e19e5'
CAND_HASH = '3d9da480674082d8c82c74e72a54be8d72767d8835a84cb25a41c0fec050a43e'

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(2**20), b''): h.update(b)
    return h.hexdigest()

def phase(r):
    return bool(r['net_obligation_2024_2026_cents'] > 0 and
                re.search(PHASE, ' | '.join(r.get('evidence_descriptions', [])), re.I) and
                (set(r['keyword_matches']) & {'ai', 'autonomy'}))

def dump_csv(path, rows, firsts=None, kind=''):
    # Original identifiers and precise cents remain alongside convenience dollars.
    cols = ['selection_id','award_id','recipient_names','recipient_entity_keys','award_key',
            'screen_score','net_obligation_2024_2026_usd','net_obligation_2024_2026_cents',
            'net_obligation_usd','net_obligation_cents','award_first_action','award_last_action',
            'transactions','routes','keyword_categories','substantive_tactical_combo','phase_iii_regex_match',
            'phase_iii_matched_descriptions_json','overlaps_tactical_384',
            'recipient_first_observed_dates_json','qualifying_first_observed_entity_keys_json',
            'qualifying_first_observed_entity_dates_json',
            'source_urls','evidence_descriptions_json','calendar_year_cents_json',
            'subset_membership_basis','review_status']
    with open(path,'w',encoding='utf-8',newline='') as f:
        w = csv.DictWriter(f, cols); w.writeheader()
        for r in rows:
            ds = {e:firsts[e] for e in r['entity_keys'] if firsts and e in firsts}
            d = {k:r.get(k,'') for k in cols}
            d.update(recipient_names='; '.join(r['entity_names']),
                     recipient_entity_keys='; '.join(r['entity_keys']),
                     net_obligation_2024_2026_usd=str(Decimal(r['net_obligation_2024_2026_cents'])/100),
                     net_obligation_usd=str(Decimal(r['net_obligation_cents'])/100),
                     award_first_action=r['first_action'],award_last_action=r['last_action'],
                     routes='; '.join(r['routes']),
                     keyword_categories='; '.join(sorted(r['keyword_matches'])),
                     phase_iii_regex_match=phase(r),
                     phase_iii_matched_descriptions_json=json.dumps([d for d in r['evidence_descriptions'] if re.search(PHASE,d,re.I)],ensure_ascii=False),
                     overlaps_tactical_384=bool(r['substantive_tactical_combo'] and r['net_obligation_2024_2026_cents']>0),
                     recipient_first_observed_dates_json=json.dumps(ds,sort_keys=True) if firsts is not None else '',
                     qualifying_first_observed_entity_keys_json=json.dumps([e for e,d in ds.items() if d >= CUTOFF]) if firsts is not None else '',
                     qualifying_first_observed_entity_dates_json=json.dumps({e:d for e,d in ds.items() if d>=CUTOFF},sort_keys=True) if firsts is not None else '',
                     source_urls='; '.join(r['source_urls']),
                     evidence_descriptions_json=json.dumps(r['evidence_descriptions'],ensure_ascii=False),
                     calendar_year_cents_json=json.dumps(r['calendar_year_cents'],sort_keys=True),
                     subset_membership_basis=kind,
                     review_status=r.get('review_status','Automated candidate, not individually validated by subset membership'))
            w.writerow(d)
    with open(path,encoding='utf-8',newline='') as f:
        check=list(csv.DictReader(f))
    assert len(check)==len(rows)
    assert [x['award_key'] for x in check]==[r['award_key'] for r in rows]

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--package',type=Path,required=True,help='Original package directory containing audit/ and code/')
    p.add_argument('--out',type=Path,required=True,help='Directory for the three final CSVs and public subset audit')
    p.add_argument('--work-dir',type=Path,help='Local intermediates, excluded from publication; default is a sibling lane1-recovery-work directory')
    p.add_argument('--financial',type=Path,help='Verified complete original financial_actions.jsonl.gz')
    p.add_argument('--recipient-map',type=Path,help='Previously generated recipient-first-observed.json')
    p.add_argument('--candidates',type=Path,help='Complete candidate_register.jsonl (or .gz)')
    args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    work=args.work_dir or args.out.parent/'lane1-recovery-work';work.mkdir(parents=True,exist_ok=True)
    orig=args.package/'audit/lane1-tactical-combination-register.json'
    tactical=json.loads(orig.read_text())
    assert len(tactical)==384 and len({r['award_key'] for r in tactical})==384
    assert all(r['substantive_tactical_combo'] and r['net_obligation_2024_2026_cents']>0 for r in tactical)
    dump_csv(args.out/'lane1-tactical-candidates-384.csv',tactical,kind='Complete surviving 384-row positive-recent AI/autonomy plus weapons/contested candidate denominator')
    overlap=[r for r in tactical if phase(r)]
    assert len(overlap)==6
    dump_csv(work/'phase-iii-surviving-tactical-overlap-6.csv',overlap,kind='Exact original Phase III predicate, restricted to surviving tactical register; 6 of 36, NOT full subset')
    (work/'phase-iii-surviving-tactical-overlap-6.json').write_text(json.dumps(overlap,indent=2))
    audit={'tactical_register':{'file':'audit/lane1-tactical-combination-register.json','sha256':sha(orig),'rows':len(tactical)},
        'original_predicate_code':{'file':'code/lane1_summarize_screen.py','sha256':sha(args.package/'code/lane1_summarize_screen.py')},
        'original_screen_code':{'file':'code/lane1_screen_financial.py','sha256':sha(args.package/'code/lane1_screen_financial.py')},
        'recovery_export_code':{'file':'recover_lane1_subsets.py','sha256':sha(Path(__file__))},
        'original_counts':{'full_candidate_awards':89838,'positive_recent_candidate_awards':27175,
                           'positive_recent_tactical_awards':384,'first_observed_recipient_tactical_awards':65,
                           'positive_recent_ai_or_autonomy_explicit_phase_iii_awards':36},
        'phase_iii_regex':PHASE,'phase_iii_flags':'IGNORECASE',
        'phase_iii_predicate':'recent_net_cents > 0 AND regex in join(evidence_descriptions) AND keyword categories intersect {ai, autonomy}; no tactical requirement',
        'first_observed_predicate':'Within 384: ANY listed entity_key has MIN(action_date) >= 2024-01-01 over the FULL financial source_rows',
        'surviving_phase_iii_overlap':len(overlap),'missing_phase_iii_rows_until_full_register':36-len(overlap),
        'phase_iii_complete_status':'pending full candidate register','first_observed_complete_status':'pending full recipient-date map',
        'limitations':['Cases are award keys, not unique programmes or necessarily unique recipients.',
          'First observed means in the preselected FY2019-FY2026 archive, not company founding or first government award.',
          'Calendar 2024-2026 positive net obligations include negative modifications; 2026 source ends September 30.',
          'Phase III text can come from older actions; positive recent dollars do not prove the Phase III action itself was recent.',
          'AI/autonomy is keyword-category evidence, not validated learned AI. Phase III matching uses at most six original stored evidence descriptions per award.',
          'No new research or programme validation is performed.']}
    firsts=None
    if args.financial:
        got=sha(args.financial);assert got==FIN_HASH,(got,'wrong financial source hash')
        firsts={};n=0;tx=set()
        with gzip.open(args.financial,'rt',encoding='utf-8') as f:
            for line in f:
                r=json.loads(line);n+=1;tx.add(r['transaction_key'])
                e,d=r.get('entity_key',''),r.get('action_date','')
                firsts[e]=min(firsts.get(e,d),d)
        assert n==712186 and len(tx)==712186
        assert len(firsts)==18094 and sum(d>=CUTOFF for d in firsts.values())==3963
        data={'source_sha256':got,'source_rows':n,'unique_transaction_keys':len(tx),'first_observed':firsts}
        (work/'recipient-first-observed.json').write_text(json.dumps(data,indent=2,sort_keys=True))
        audit['recipient_date_source']={'file':'data/normalized/financial_actions.jsonl.gz','sha256':got,'rows':n,'entities':len(firsts)}
    elif args.recipient_map:
        data=json.loads(args.recipient_map.read_text());firsts=data['first_observed']
        assert data['source_sha256']==FIN_HASH and data['source_rows']==712186
        assert len(firsts)==18094
        audit['recipient_date_source']={'file':'data/normalized/financial_actions.jsonl.gz','sha256':data['source_sha256'],'rows':data['source_rows'],'entities':len(firsts),
                                      'reused_local_recipient_map_sha256':sha(args.recipient_map)}
    if firsts is not None:
        absent={e for r in tactical for e in r['entity_keys'] if e not in firsts};assert not absent,absent
        emerging=[r for r in tactical if any(firsts[e]>=CUTOFF for e in r['entity_keys'] if e in firsts)]
        assert len(emerging)==65,('first observed predicate count differs',len(emerging))
        dump_csv(args.out/'lane1-first-observed-recipients-65.csv',emerging,firsts,
                 'Exact original predicate: 65 award cases within 384; recipient MIN(action_date) calculated over all 712,186 financial rows')
        enriched=[dict(r,recipient_first_observed_dates={e:firsts[e] for e in r['entity_keys']},
                      qualifying_first_observed_entity_keys=[e for e in r['entity_keys'] if firsts[e]>=CUTOFF]) for r in emerging]
        (work/'first-observed-recipient-awards-65.json').write_text(json.dumps(enriched,indent=2))
        dump_csv(work/'tactical-384-recipient-first-observation-audit.csv',tactical,firsts,
                 'Complete 384-row denominator; qualifying recipient keys identify membership in the exact 65 subset')
        audit['first_observed_complete_status']='complete';audit['first_observed_recovered_awards']=len(emerging)
        audit['first_observed_distinct_qualifying_entities']=len({e for r in emerging for e in r['entity_keys'] if firsts[e]>=CUTOFF})
    if args.candidates:
        opener=gzip.open if args.candidates.suffix=='.gz' else open
        h=hashlib.sha256();cands=[]
        with opener(args.candidates,'rb') as f:
            for b in f:h.update(b);cands.append(json.loads(b))
        assert len(cands)==89838 and len({r['award_key'] for r in cands})==89838
        # Exact hash may differ on deterministic rebuild because source_rows text ordering differs.
        # Count AND complete surviving-row content comparisons are separately verified below.
        audit['full_candidate_source']={'file':'lane1/candidate_register.jsonl','file_sha256':sha(args.candidates),
             'uncompressed_sha256':h.hexdigest(),'matches_original_omitted_hash':h.hexdigest()==CAND_HASH,'rows':len(cands)}
        bykey={r['award_key']:r for r in cands}
        mism=[]
        for old in tactical:
            new=bykey.get(old['award_key'])
            if new is None:mism.append({'award_key':old['award_key'],'missing':True});continue
            dif=[k for k,v in old.items() if k!='review_status' and new.get(k)!=v]
            if dif:mism.append({'award_key':old['award_key'],'different_fields':dif})
        audit['surviving_tactical_row_comparison_mismatches']=mism
        assert not mism,('rebuild disagrees with surviving original rows',mism[:5])
        allphase=[r for r in cands if phase(r)]
        assert len(allphase)==36,('Phase III predicate count differs',len(allphase))
        assert sum(r['net_obligation_2024_2026_cents']>0 for r in cands)==27175
        assert sum(r['substantive_tactical_combo'] and r['net_obligation_2024_2026_cents']>0 for r in cands)==384
        dump_csv(args.out/'lane1-explicit-phase-iii-36.csv',allphase,firsts,
                 'Exact original predicate over ALL 89,838 candidate awards; 36 matches, of which 6 are in the tactical 384')
        (work/'phase-iii-ai-autonomy-awards-36.json').write_text(json.dumps(allphase,indent=2))
        audit['phase_iii_complete_status']='complete';audit['phase_iii_recovered_awards']=len(allphase)
        audit['missing_phase_iii_rows_until_full_register']=0
        audit['phase_iii_recovered_non_tactical_awards']=sum(not r['substantive_tactical_combo'] for r in allphase)
    final_names=['lane1-tactical-candidates-384.csv','lane1-first-observed-recipients-65.csv','lane1-explicit-phase-iii-36.csv']
    audit['outputs']=[{'file':'audit/'+name,'bytes':(args.out/name).stat().st_size,'sha256':sha(args.out/name)} for name in final_names if (args.out/name).exists()]
    (args.out/'lane1-subset-audit.json').write_text(json.dumps(audit,indent=2))
    print(json.dumps({k:v for k,v in audit.items() if k not in {'outputs','limitations'}},indent=2))
if __name__=='__main__':main()
