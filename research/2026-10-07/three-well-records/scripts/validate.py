"""Offline evidence validation only; no network or paid calls."""
import pathlib,json,hashlib,xml.etree.ElementTree as ET
P=pathlib.Path(__file__).resolve().parents[1];checks=[]
records=[json.loads(l) for l in (P/'sources/manifest.jsonl').read_text().splitlines()]
for r in records:
 if 'sha256' in r:assert hashlib.sha256((P/'sources'/r['name']).read_bytes()).hexdigest()==r['sha256']
checks.append({'check':'acquisition source hashes','verified':sum('sha256' in r for r in records)})
a=json.loads((P/'results/alias-monthly.json').read_text());assert len(a['aliases'])==3 and len(a['petrinex_identifier_mapping'])==6 and not a['matched_rows']
changes=(P/'sources/st1-2025-WELLS1030.TXT').read_text()
for w in a['aliases']:assert w['licence'] in changes and w['old'] in changes and w['current'] in changes
checks.append({'check':'three official UWI mappings and six monthly aliases','passed':True})
idx=json.loads((P/'results/public-document-index.json').read_text());assert len(idx)==15 and len({r['event'] for r in idx})==5 and all(r['attachment']['IsConfidential']=='N' for r in idx)
for r in idx:assert (P/r['file']).stat().st_size==r['attachment']['FileSize']
checks.append({'check':'15 public attachments across five unique events; sizes match index','passed':True})
summary=[]
for expected in ['ca2025dscb','ca2025dwzq']:
 f=P/'sources'/f'nrcan-{expected}-details.xml';root=ET.parse(f).getroot();e=root.find('.//{*}event');assert e.attrib['publicID'].endswith(expected)
 summary.append({'source':str(f.relative_to(P)),'event_id':expected,'origins':len(e.findall('{*}origin')),'magnitudes':len(e.findall('{*}magnitude')),'picks':len(e.findall('{*}pick')),'arrivals':len(e.findall('.//{*}arrival')),'origin_time':e.find('{*}origin/{*}time/{*}value').text,'creation_time':e.find('{*}origin/{*}creationInfo/{*}creationTime').text,'magnitude':e.find('{*}magnitude/{*}mag/{*}value').text,'magnitude_type':e.find('{*}magnitude/{*}type').text,'operator_notification_time':None})
assert all(r['origins']==r['magnitudes']==1 and r['picks']==r['arrivals']==0 for r in summary)
(P/'results/nrcan-detail-summary.json').write_text(json.dumps(summary,indent=2)+'\n');checks.append({'check':'event identities and actual returned XML fields','passed':True})
prior=json.loads((P/'results/prior-iar-count-check.json').read_text());assert all(x['displayed_total']==0 for x in prior)
checks.append({'check':'original IAR zero counts distinguished from new errors','passed':True})
(P/'results/validation.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2))
