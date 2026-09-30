"""Extract OFAC Entity records without inferring historical sanctions dates.
Run with Python 3: python3 prepare.py (beside sdn.xml).
Uses only the Python standard library. No model calls.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
import json, hashlib, collections, unicodedata, re, zipfile

base = Path(__file__).resolve().parent
raw = (base / 'sdn.xml').read_bytes()
root = ET.fromstring(raw)
for el in root.iter():
    el.tag = el.tag.rsplit('}', 1)[-1]
entries = root.findall('sdnEntry')
declared = int(root.findtext('publshInformation/Record_Count'))
assert len(entries) == declared
assert len({e.findtext('uid') for e in entries}) == len(entries)
def flat(el):
    return {child.tag: child.text or '' for child in el}
def name(el):
    return ' '.join(filter(None, (el.findtext('firstName'), el.findtext('lastName'))))
def key(value):
    # Conservative key: preserve legal suffixes and non-Latin characters.
    value = unicodedata.normalize('NFKC', value).casefold()
    return re.sub(r'[^\w]+', ' ', value, flags=re.UNICODE).strip()
entities, names = [], []
for e in entries:
    if e.findtext('sdnType') != 'Entity':
        continue
    uid = e.findtext('uid')
    aliases = [flat(a) for a in e.findall('akaList/aka')]
    entities.append({'ofac_id': uid, 'primary_name': name(e),
                     'programs': [p.text for p in e.findall('programList/program')],
                     'aliases': aliases,
                     'addresses': [flat(a) for a in e.findall('addressList/address')],
                     'identifiers': [flat(a) for a in e.findall('idList/id')],
                     'remarks': e.findtext('remarks', '')})
    names.append({'ofac_id': uid, 'name': name(e), 'kind': 'primary', 'category': '', 'match_key': key(name(e))})
    for a in e.findall('akaList/aka'):
        names.append({'ofac_id': uid, 'name': name(a), 'kind': a.findtext('type', ''),
                      'category': a.findtext('category', ''), 'match_key': key(name(a))})
assert all(n['name'] and n['match_key'] for n in names)
assert {n['ofac_id'] for n in names} == {e['ofac_id'] for e in entities}
summary = {'source_url': 'https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/SDN.XML',
           'retrieved_date': '2026-09-18', 'source_publish_date': root.findtext('publshInformation/Publish_Date'),
           'source_sha256': hashlib.sha256(raw).hexdigest(), 'source_entries': len(entries),
           'source_types': dict(collections.Counter(e.findtext('sdnType') for e in entries)),
           'retained_entities': len(entities), 'names_including_aliases': len(names),
           'addresses': sum(len(e['addresses']) for e in entities),
           'alias_categories': dict(collections.Counter(n['category'] for n in names if n['kind'] != 'primary')),
           'scope': 'Current Entity entries only. Not a historical list. Individuals, vessels and aircraft excluded. Weak aliases retained and flagged. No award matching or legal conclusions performed.'}
for filename, data in [('entities.json', entities), ('names.json', names), ('source-summary.json', summary)]:
    (base / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
with zipfile.ZipFile(base.parent / 'ofac-step1-2026-09-18.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for filename in ['sdn.xml', 'entities.json', 'names.json', 'source-summary.json', 'prepare.py']:
        z.write(base / filename, filename)
print(json.dumps(summary, indent=2))
