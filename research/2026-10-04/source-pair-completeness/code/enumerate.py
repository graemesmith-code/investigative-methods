import pathlib,json,csv,itertools,sys,collections
P=pathlib.Path(__file__).resolve().parents[1];OLD=P.parent/'source-test-deep-review';sys.path.insert(0,str(OLD/'code/generator'));import build
ss=list(map(json.loads,(OLD/'sources.jsonl').read_text().splitlines()));M=json.loads((OLD/'mechanisms.json').read_text());rulepairs={(a,b) for m in M for a,b in itertools.product(m['a'],m['b']) if a!=b};active=list(map(json.loads,(OLD/'candidate-inventory.jsonl').read_text().splitlines()));existing={(int(r['source_a'][-4:]),int(r['source_b'][-4:])) for r in active};rows=[]
for a,b in itertools.combinations(ss,2):
 shared=sorted(set(build.namespaces(a))&set(build.namespaces(b)))
 if not shared:continue
 ai=int(a['sys_id'][-4:]);bi=int(b['sys_id'][-4:]);rows.append(dict(source_a=a['sys_id'],name_a=a['name'],source_b=b['sys_id'],name_b=b['name'],shared_catalog_namespaces=shared,in_rule_ab=(ai,bi) in rulepairs,in_rule_ba=(bi,ai) in rulepairs,in_inventory_either=(ai,bi) in existing or (bi,ai) in existing,namespace_caveat='Declared fields only; actual entity type, namespace and dates require verification. DOI/ORCID, IMO/company and domain/control are not interchangeable.'))
(P/'named-identifier-pairs.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
with (P/'named-identifier-pairs.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print('Named namespace unordered pairs',len(rows),'outside both rule directions',sum(not r['in_rule_ab'] and not r['in_rule_ba'] for r in rows))
for r in rows:
 if not r['in_rule_ab'] and not r['in_rule_ba']:print(r['source_a'],r['source_b'],r['shared_catalog_namespaces'])
