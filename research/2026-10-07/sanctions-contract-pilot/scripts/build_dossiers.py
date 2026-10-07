import json, hashlib, collections, decimal, pathlib
P=pathlib.Path(__file__).resolve().parents[1]
B=P/'baseline/sanctions-screen-evidence-2026-09-18'
D=decimal.Decimal
dates={'46068':'2023-12-12','25647':'2018-11-05','28534':'2020-02-26','36423':'2022-04-06','50905':'2024-10-30','55921':'2025-10-14','44257':'2023-12-11','57139':'2026-04-24','47650':'2024-02-23','28296':'2020-01-10','43223':'2023-05-19','47535':'2024-02-23'}
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,data):path.parent.mkdir(exist_ok=True,parents=True);path.write_text(json.dumps(data,indent=2)+'\n')
groups=json.loads((B/'results/candidate-groups.json').read_text())
tx=[json.loads(x) for x in (B/'results/candidate-transactions.jsonl').read_text().splitlines()]
assert len(groups)==13 and len(tx)==153
assert len({x['transaction']['contract_transaction_unique_key'] for x in tx})==153
assert len({x['transaction']['contract_award_unique_key'] for x in tx})==72
assert len(json.loads((B/'entities.json').read_text()))==9980
assert len(json.loads((B/'names.json').read_text()))==23398
assert sha(B/'sdn.xml')==json.loads((B/'source-summary.json').read_text())['source_sha256']
other=P/'baseline/ofac-step1-2026-09-18'
assert all((other/f).read_bytes()==(B/f).read_bytes() for f in ['sdn.xml','entities.json','names.json','source-summary.json','prepare.py'])
assert (B/'sanctions-screen-results-2026-09-18.md').read_bytes()==(P.parents[2]/'evidence/ofac/original-report.md').read_bytes()
manifest=[{'path':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in (P/'baseline').rglob('*') if f.is_file()]
write(P/'baseline-file-hashes.json',manifest)
write(P/'recovery-verification.json',{'groups':13,'unique_transactions':153,'unique_awards':72,'entities':9980,'names_and_aliases':23398,'shared_original_files_identical':True,'report_identical_to_repository':True,'full_corpus_counts':'6639176 transactions and 101379 distinct recipient names are preserved original-run metadata, not recomputed without full corpus','bulk_redownload':False})
for n,g in enumerate(groups,1):
 rows=[(i+1,x['transaction']) for i,x in enumerate(tx) if x['ofac_id']==g['ofac_id'] and x['transaction']['recipient_name']==g['recipient_name'] and x['transaction']['recipient_uei']==g['recipient_uei']]
 assert len(rows)==g['transactions']
 date=dates[g['ofac_id']]; source='sources/designation-'+date.replace('-','')+'.txt'
 if g['ofac_id']=='25647':source='sources/treasury-sm1130.txt'
 if g['ofac_id']=='44257':source='sources/ofac-20231211.html'
 text=(P/source).read_text();needle=g['ofac_primary_name'];index=text.lower().find(needle.lower());assert index>=0,(needle,source)
 citation={'path':source,'sha256':sha(P/source),'character_start':index,'excerpt':text[index:index+1100],'date':date,'scope':g['ofac_record']['programs'],'date_note':'2018 government-of-Iran identification; later EO13382 designation discussed in same Treasury release' if g['ofac_id']=='25647' else 'OFAC dated addition notice; not a guarantee of all historical program changes'}
 values=[D(t['federal_action_obligation'] or '0') for _,t in rows]
 compact=[]
 for i,t in rows:
  compact.append({'line':i,'date':t['action_date'],'piid':t['award_id_piid'],'mod':t['modification_number'],'type':t.get('award_type') or t.get('idv_type'),'action':t.get('action_type'),'obligation':t['federal_action_obligation']})
 dossier={'id':f'C{n:02}','recipient':g['recipient_name'],'uei':g['recipient_uei'],'cage_codes':sorted({t.get('cage_code','') for _,t in rows}),'contract_addresses':g['locations'],'ofac':g['ofac_record'],'matched_names':g['matching_names'],'method':g['method'],'designation':citation,'transactions_source':{'path':'baseline/sanctions-screen-evidence-2026-09-18/results/candidate-transactions.jsonl','sha256':sha(B/'results/candidate-transactions.jsonl'),'line_numbers':[i for i,_ in rows]},'transaction_rows':compact,'amounts':{'positive_obligations':str(sum(v for v in values if v>0)),'negative_obligations':str(sum(v for v in values if v<0)),'net_obligations':str(sum(values)),'payment_amount':'not established; award-level outlay fields are not summed','ceilings':'available in original rows; not payments or action obligations'},'before_designation_rows':sum(t['action_date']<date for _,t in rows),'on_or_after_designation_rows':sum(t['action_date']>=date for _,t in rows),'code_only_identity':'strong name/street match' if g['ofac_id']=='44257' else 'name-only collision with conflicting locations; ownership unresolved','strongest_innocent_explanation':'Official US government business authorization may apply; vehicle termination administrative; child rows include offsets' if g['ofac_id']=='44257' else 'Different legal persons sharing generic name or weak alias','missing_evidence':'Signed orders, delivery/payment records, authorization basis' if g['ofac_id']=='44257' else 'Corporate registration/ownership bridge between US UEI and foreign designated entity; current snapshot is not historical coverage','legal_limit':'Triage only. Association is not sanctions coverage; dates do not establish illegality. An old contract is not automatically authorized. Short intervals are not automatically immaterial.'}
 if g['ofac_id']=='44257':
  dossier['refreshed_calibration']={'source':'NAI-calibration.md','vehicle_termination':'2025-03-11 P00002 zero additional obligations; API independently verified','children':'27 linked awards,32 transactions;8 orders dated Dec13-14 2023,13 rows,positive36309.46 negative15662.32 net20647.14 USD; no payments known; four fully offset','identity':'all eight current details same name and UEI; street address matches OFAC','authorization':'31CFR583.509 effectiveDec21 2022 official US government business by employees/grantees/contractors; renumbered583.510 March2024. Potential explanation, qualification not proven. Sources glomag-2022.pdf and glomag-2024.pdf','date_caution':'action dates not actual purchasing/entry timestamps; modifications do not prove cancellation chronology','significance':'bounded procurement authorization question; published designation already known'}
 write(P/'dossiers'/f'C{n:02}.json',dossier)
print('Verified originals and built 13 source-linked dossiers')
