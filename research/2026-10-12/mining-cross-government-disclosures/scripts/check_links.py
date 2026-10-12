"""Current HEAD checks only; not original GET/download/parser access tests."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import json
import urllib.request
import urllib.error

root = Path(__file__).resolve().parents[1]
inventory = json.loads((root / 'sources/source-urls.json').read_text())
def check(item):
    record = dict(item, checked_at=datetime.now(timezone.utc).isoformat(), method='HEAD')
    request = urllib.request.Request(item['url'], method='HEAD', headers={'User-Agent': 'Mozilla/5.0 (archive link validation)'})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            record.update(status=response.status, final_url=response.url, content_type=response.headers.get('Content-Type'))
    except urllib.error.HTTPError as error:
        record.update(status=error.code, final_url=error.url, error=str(error))
    except Exception as error:
        record.update(status=None, error=str(error))
    return record
with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(check, inventory))
report = {'purpose': 'New archival HEAD availability checks; these do not validate contents, reproduce original access counts, or establish contradictions', 'results': results}
(root / 'validation/link-checks.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'checked': len(results), 'http_200': sum(r.get('status') == 200 for r in results), 'other': [{'id': r['id'], 'status': r.get('status'), 'error': r.get('error')} for r in results if r.get('status') != 200]}))
