#!/usr/bin/env python3
"""Illustrative retrospective source-only audit, not a predictive fraud benchmark.
Python standard library only. No language-model or paid API calls.
Run: python run_test.py [--download]
All metrics are based on explicitly transcribed source values, with source spans.
"""
import argparse, datetime, hashlib, html, json, re, time, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'sources'; OUT=ROOT/'output'
SOURCE.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)
CUTOFF='2000-03-31'
DOCS=[
 dict(id='enron_1998_10k', company='Enron', form='10-K', fiscal_period='1998-12-31', filed='1999-03-31', url='https://www.sec.gov/Archives/edgar/data/1024401/000102440199000007/0001024401-99-000007.txt', role='eligible'),
 dict(id='enron_1999q2_10q', company='Enron', form='10-Q', fiscal_period='1999-06-30', filed='1999-08-16', url='https://www.sec.gov/Archives/edgar/data/1024401/0001024401-99-000020.txt', role='eligible'),
 dict(id='enron_1999_10k', company='Enron', form='10-K', fiscal_period='1999-12-31', filed='2000-03-30', url='https://www.sec.gov/Archives/edgar/data/1024401/000102440100000002/0001024401-00-000002.txt', role='eligible'),
 dict(id='duke_1999_10k', company='Duke Energy', form='10-K', fiscal_period='1999-12-31', filed='2000-03-21', url='https://www.sec.gov/Archives/edgar/data/30371/0000950109-00-001035.txt', role='eligible'),
 dict(id='enron_2000_proxy', company='Enron', form='DEF 14A', fiscal_period='2000-05-02 shareholder meeting', filed='2000-03-21', document_date='2000-03-28', url='https://www.sec.gov/Archives/edgar/data/1024401/0000950129-00-001279.txt', role='eligible'),
 dict(id='enron_2000_10k', company='Enron', form='10-K', fiscal_period='2000-12-31', filed='2001-04-02', url='https://www.sec.gov/Archives/edgar/data/1024401/000102440101500010/ene10-k.txt', role='future_excluded_from_main_test'),
]

def main_part(s):
    """Use primary filing, not exhibits. Preserve original newline counts/locators."""
    m=re.search(r'<DOCUMENT>\s*<TYPE>(?:10-[KQ]|DEF 14A)\b.*?<TEXT>(.*?)</TEXT>',s,re.S|re.I)
    if m: return m.group(1),s[:m.start(1)].count('\n')+1
    return s,1

def paragraphs(s, offset):
    for m in re.finditer(r'\S[^\n]*(?:\n[^\n]+)*',s):
        raw=m.group(0)
        t=html.unescape(re.sub(r'<[^>]*>',' ',raw))
        t=re.sub(r'\s+',' ',t).strip()
        if not t: continue
        a=offset+s[:m.start()].count('\n'); b=a+raw.count('\n')
        yield dict(line_start=a,line_end=b,text=t)

patterns={
 'related_party':r'\brelated part(?:y|ies)\b',
 'officer_control':r'\bofficer\b.{0,160}\b(?:managing member|general partner)\b',
 'stock_investment_support':r'\bcommon (?:stock|shares)\b.*\b(?:hedg\w*|put option)\b|\b(?:hedg\w*|put option)\b.*\bcommon (?:stock|shares)\b',
 'unconsolidated_entity':r'\bunconsolidated\b',
 'valuation_estimates':r'\b(?:mark-to-market|unrealized gains|estimated fair value)\b',
}

def extract_candidates(s, offset):
    ps=list(paragraphs(s,offset)); hits=[]
    for p in ps:
        cues=[k for k,v in patterns.items() if re.search(v,p['text'],re.I)]
        if cues: hits.append({**p,'cues':cues})
    # A Boolean trigger, not a calibrated risk/fraud score; intentionally generic.
    return dict(paragraph_count=len(ps),cue_paragraph_count=len(hits),
                officer_control_hits=[p for p in hits if 'officer_control' in p['cues']],
                candidates=hits)

# Source values manually checked in original, contemporaneous filings.
# Numbers are $ million; CFI is signed. Deltas use the same filing's comparative.
DATA={
 'Enron':dict(source='enron_1999_10k',current=1999,prior=1998,
   net_income=[893,703],operating_cash_flow=[1228,1640],investing_cash_flow=[-3507,-3965],
   operating_income=[802,1378],revenue=[40112,31260],
   source_lines={'income_statement':[4092,4136],'cash_flow':[4290,4335]},
   income_before_accounting_change=[1024,703],tax_expense=[104,175],asset_sale_gains=[541,56],
   merchant_sale_proceeds=[2217,1434],capex=[2363,1905]),
 'Duke Energy':dict(source='duke_1999_10k',current=1999,prior=1998,
   net_income=[1507,1252],operating_cash_flow=[2684,2331],investing_cash_flow=[-3800,-2476],
   operating_income=[1795,2433],revenue=[21742,17610],
   source_lines={'income_statement':[2948,3020],'cash_flow':[3059,3101]},
   extraordinary_gain_after_tax=[660,-8],capital_and_investment_expenditures=[5936,2500]),
}

def change(x): return 100*(x[0]/x[1]-1)

def calc(d):
    ni,cfo,oi=d['net_income'],d['operating_cash_flow'],d['operating_income']
    return dict(net_income_growth_pct=change(ni),operating_cash_flow_growth_pct=change(cfo),
                operating_income_growth_pct=change(oi),revenue_growth_pct=change(d['revenue']),
                operating_cash_flow_to_net_income=cfo[0]/ni[0],
                operating_plus_investing_cash_flow=cfo[0]+d['investing_cash_flow'][0],
                flags={
                  'net_income_rises_and_operating_cash_flow_falls':ni[0]>ni[1] and cfo[0]<cfo[1],
                  'operating_cash_flow_below_net_income':cfo[0]<ni[0],
                  'operating_income_falls_while_net_income_rises':oi[0]<oi[1] and ni[0]>ni[1],
                  'operating_plus_investing_cash_flow_negative':cfo[0]+d['investing_cash_flow'][0]<0})

def main():
    download=argparse.ArgumentParser(); download.add_argument('--download',action='store_true'); args=download.parse_args()
    reference_path=ROOT/'manifest.json'
    try:
        reference={d['id']:d for d in json.loads(reference_path.read_text())}
        if set(reference)!={d['id'] for d in DOCS} or any(
            not re.fullmatch(r'[0-9a-f]{64}',d.get('sha256','')) for d in reference.values()
        ):
            raise ValueError('unexpected source IDs or invalid SHA-256 values')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise SystemExit(f'Cannot load the supplied reference manifest {reference_path}: {exc}. '
                         'No numerical calculations were performed.')
    manifest=[]; result={}; source_texts={}
    for d in DOCS:
        p=SOURCE/(d['id']+'.txt')
        if args.download or not p.exists():
            req=urllib.request.Request(d['url'],headers={'User-Agent':'Historical-filing-methods-replay/1.0'})
            with urllib.request.urlopen(req,timeout=60) as r: b=r.read()
            time.sleep(1)
        else:
            b=p.read_bytes()
        actual_hash=hashlib.sha256(b).hexdigest()
        expected_hash=reference[d['id']]['sha256']
        if actual_hash!=expected_hash:
            raise SystemExit(f'Source hash mismatch for {d["id"]}: expected {expected_hash}, '
                             f'got {actual_hash}. Stop and inspect the source change; '
                             'the fixed numerical inputs apply only to the supplied reference bytes. '
                             'No numerical calculations or new result files were produced.')
        if args.download or not p.exists(): p.write_bytes(b)
        s=b.decode('utf-8',errors='replace'); source_texts[d['id']]=s
        primary,offset=main_part(s)
        entry={**d,'file':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':actual_hash,
               'verified_local_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'eligible':d['filed']<=CUTOFF,'primary_document_only':True}
        # Filing dates verified against SEC header where present, and SEC index for 2000-year 10-K.
        date=re.search(r'FILED AS OF DATE:\s*(\d{8})',s)
        if date: assert date.group(1)==d['filed'].replace('-',''),(d['id'],date.group(1))
        manifest.append(entry)
        if entry['eligible']:
            result[d['id']]=extract_candidates(primary,offset)
    for company,d in DATA.items():
        txt=source_texts[d['source']].splitlines()
        lo=min(v[0] for v in d['source_lines'].values()); hi=max(v[1] for v in d['source_lines'].values())
        span='\n'.join(txt[lo-1:hi])
        for field in ['net_income','operating_cash_flow','investing_cash_flow','operating_income','revenue']:
            for n in d[field]: assert f'{abs(n):,}' in span,(company,field,n)
    metrics={k:calc(v) for k,v in DATA.items()}
    en=metrics['Enron']; en['non_diagnostic_context']={
      'asset_sale_gains_over_income_before_tax_and_accounting_change_pct':100*541/(1024+104),
      'operating_cash_flow_minus_merchant_sale_proceeds_NOT_GAAP_CFO':1228-2217,
      'reported_CFO_still_exceeds_net_income':True,
      'merchant_sale_subtraction_warning':'Diagnostic sensitivity only. Does not reverse cash costs/additions or establish improper classification; merchant sales may belong to ordinary operations.'}
    metrics['Duke Energy']['non_diagnostic_context']={'extraordinary_gain_after_tax_over_net_income_pct':100*660/1507}
    # Future document is an audit-only contradiction check, never model input in as-of test.
    future={'source':'enron_2000_10k','filed':'2001-04-02','CFO':4779,'net_income':979,'CFO_to_net_income':4779/979,
            'warning':'A low-CFO/earnings rule would not flag this reported year either. Future input is inadmissible for March 2000 or pre-McLean tests.'}
    for name,obj in [('manifest.json',manifest),('numeric_inputs.json',DATA),('metrics.json',metrics),('text_candidates.json',result),('future_contradiction_check.json',future)]:
        (OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
    summary={'as_of_cutoff':CUTOFF,'status':'post_hoc_illustrative_replay_not_blind_predictive_test',
             'metrics':metrics,
             'text_counts':{k:{f:v[f] for f in ['paragraph_count','cue_paragraph_count']}|{'officer_control_hits':len(v['officer_control_hits'])} for k,v in result.items()},
             'future_excluded':future}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
