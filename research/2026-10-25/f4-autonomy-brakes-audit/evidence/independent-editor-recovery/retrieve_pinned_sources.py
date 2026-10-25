import urllib.request,pathlib,json,datetime,hashlib,concurrent.futures
R=pathlib.Path(__file__).parent
base='https://raw.githubusercontent.com/graemesmith-code/investigative-methods/a0ed4b2c24083287120c1bb8523652f959ffd1b6/research/2026-10-25/f4-autonomy-brakes-audit/'
paths=['report.md','evidence/live-award-register.json','evidence/fpds-verified-actions.csv','evidence/combined-live-inventory.csv','evidence/reviewed-cases.csv','evidence/live-technical-scope-review.csv','evidence/ota-resolution-review.json','evidence/ota-keyword-followup-records.json','evidence/ota-verified-actions.csv','evidence/ota-keyword-followup-actions.csv','audit/exa-query-cost-log.csv','audit/exa-discovery-accounting.json','audit/reviewed-case-accounting.json','audit/r3-04-corrections.json','code/exa_serial.py']
manifest=json.load(open(R/'ot-response-manifest.json'))
paths += [x['public_path'] for x in manifest['bodies']]
expected={x['public_path']:x['sha256'] for x in manifest['bodies']}
def get(p):
 u=base+p;st=datetime.datetime.now(datetime.timezone.utc).isoformat();b=urllib.request.urlopen(u,timeout=90).read();q=R/'sources'/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);h=hashlib.sha256(b).hexdigest();assert p not in expected or h==expected[p];return {'path':p,'url':u,'bytes':len(b),'sha256':h,'retrieved_utc':st,'expected_raw_xml_hash_matches':h==expected[p] if p in expected else None}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:out=list(ex.map(get,paths))
(R/'retrieval-receipts.json').write_text(json.dumps(out,indent=2));print(len(out),'files recovered;',sum(x['bytes'] for x in out),'bytes')
