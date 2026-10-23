"""Check export structure/counts, not source truth or coding reliability."""
import csv
import json
from collections import Counter
from pathlib import Path
root = Path(__file__).resolve().parent
obj = json.loads((root / 'claims.json').read_text())
rows = obj['claims']
assert len(rows) == 90
assert len({r['claim_id'] for r in rows}) == 90
assert Counter(r['country'] for r in rows) == {'United States': 30, 'China': 30, 'Russia': 30}
assert Counter(r['evidence_origin'] for r in rows) == {'News-reported claim': 23, 'Primary-document benchmark': 57, 'Original document reached through news': 3, 'Official document republished by news': 7}
assert sum(r['strict_targeting_core_eligible'] is True for r in rows) == 67
strict_news = [r for r in rows if r['strict_targeting_core_eligible'] is True and r['evidence_origin'] == 'News-reported claim']
assert len(strict_news) == 11
assert Counter(r['country'] for r in strict_news) == {'United States': 5, 'China': 5, 'Russia': 1}
assert len({(r['country'], r['event_id']) for r in rows}) == 15
with (root / 'claims.csv').open(newline='') as f:
    csv_rows = list(csv.DictReader(f))
assert [r['claim_id'] for r in csv_rows] == [r['claim_id'] for r in rows]
for a, b in zip(csv_rows, rows):
    assert all(a[k] == str(v) for k, v in b.items())
print('PASS: 90 unique rows; 30 per country; 15 clusters; 23 news claims; 67 core claims; 11 core news claims. CSV matches JSON.')
print('This verifies bookkeeping only, not representativeness, source accuracy or human agreement.')
