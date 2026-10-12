"""New archival checks; not the original research execution code."""
from pathlib import Path
import hashlib
import json
import re
from decimal import Decimal as D

root = Path(__file__).resolve().parents[1]
page = json.loads((root / 'sources/saved-page.json').read_text())
text = (root / 'FINDINGS.md').read_text()
assert text == page['content']['markdown']
blocks = page['content']['blocks']
assert len(blocks) == 132
for block in blocks:
    assert hashlib.sha256(block['markdown'].encode()).hexdigest() == block['hash']
assert '\n\n'.join(b['markdown'] for b in blocks) == text
profiles = re.findall(r'^## (\d+) (.+)$', text, re.M)
assert [int(n) for n, _ in profiles] == list(range(1, 11))
urls = list(dict.fromkeys(re.findall(r'\]\((https?://[^)]+)\)', text)))
inventory = json.loads((root / 'sources/source-urls.json').read_text())
assert urls == [x['url'] for x in inventory]
assert len(urls) == 37
assert 88 == 85 + 3
peru = D(29511000) * D('0.00045359237')
delta = D('13386.3420761') - peru
assert abs(delta) <= D('0.45359237')
ity = [D(27368514903) / D('631.40'), D(27368514903) / D('595.72')]
senegal = [D(12982245458) / D('631.40'), D(12982245458) / D('595.72')]
fekola = [D(32135608890) * D('0.0015936'), D(32135608890) * D('0.0017137')]
assert ity[0] <= D(45145203) <= ity[1]
assert senegal[0] <= D(21399746) <= senegal[1]
assert fekola[1] < D(59060000)
report = {'purpose': 'New archive integrity and recorded specimen arithmetic checks; no original source downloads reproduced', 'passed': True, 'saved_blocks': len(blocks), 'profiles': profiles, 'source_urls': len(urls), 'reported_access_counts': {'requests': 88, 'http_200': 85, 'failed': 3, 'independently_recomputed_from_original_ledger': False}, 'peru': {'tonnes': str(peru), 'host_minus_converted_tonnes': str(delta), 'overlap': True}, 'ity_usd_bounds': list(map(str, ity)), 'senegal_usd_bounds': list(map(str, senegal)), 'fekola_usd_bounds': list(map(str, fekola)), 'fekola_verdict': 'REVIEW REQUIRED: definitions unresolved'}
(root / 'validation/archive-checks.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'passed': True, 'blocks': len(blocks), 'profiles': len(profiles), 'urls': len(urls)}))
