import pathlib,json,hashlib,sqlite3,decimal
P=pathlib.Path(__file__).resolve().parents[1];D=decimal.Decimal
for row in json.loads((P/'baseline-file-hashes.json').read_text()):
 assert hashlib.sha256((P/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
ledger=json.loads((P/'jev/ledger.json').read_text());attempts=ledger['attempts']
assert len(attempts)==21 and all(a['status']=='success' and a['provider']=='jev' for a in attempts)
assert sum(a['accounted'] for a in attempts)==2443
assert all(a['accounted']<=a['reserve']==3000 for a in attempts)
db=sqlite3.connect('file:'+str(P/'jev/ledger.sqlite')+'?mode=ro',uri=True)
assert db.execute('select count(*),sum(accounted) from attempts').fetchone()==(21,2443);db.close()
assert len(list((P/'jev/stage1').glob('*.response.json')))==13
assert all(r['passed'] for r in json.loads((P/'jev/controls-v2/evaluation.json').read_text()))
searches=json.loads((P/'expansion/search-summary.json').read_text())
assert len(searches)==5 and all(r['returned_rows']==0 and r['complete_within_query'] for r in searches)
for r in json.loads((P/'expansion/validated-extractions.json').read_text()):
 c=r['citation'];s=(P/c['path']).read_text();assert r['validated'] and s[c['start_character']:c['end_character']]==c['exact_passage']
 assert hashlib.sha256((P/c['path']).read_bytes()).hexdigest()==c['sha256']
children=json.loads((P/'nai-child-history.json').read_text());assert len(children)==27
tx=[t for r in children for t in r['transactions']];assert len(tx)==32
assert sum(D(str(t['federal_action_obligation'])) for t in tx)==D('148422.44')
post=[t for t in tx if t['action_date']>='2023-12-11'];assert len(post)==13
assert sum(D(str(t['federal_action_obligation'])) for t in post)==D('20647.14')
assert len(json.loads((P/'ranked-shortlist.json').read_text()))==13
print('PASS: baseline hashes, 13 dossiers/responses, 21-call ledger, six revised controls, five null expansions, 27 child histories and amount sums')
