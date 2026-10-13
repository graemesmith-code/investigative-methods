"""Download published Government of Canada resources; preserve bytes and provenance.

No credentials, spoofed browser headers, cookies or access-control bypass.
Run from this research directory. Failed URLs are logged and not retried here.
"""
import csv
import datetime
import hashlib
import io
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'snapshots'
SOURCES = {
    'contract-history-2026-2027.csv': 'https://canadabuys.canada.ca/opendata/pub/2026-2027-contractHistory-contratsOctroyes.csv',
    'canadabuys-data-dictionary.xml': 'https://donnees-data.tpsgc-pwgsc.gc.ca/ba2/ac-cb/achatscanada-canadabuys-dd.xml',
    'contract-history-support.html': 'https://donnees-data.tpsgc-pwgsc.gc.ca/ba2/ac-cb/COsoutien-CHsupport-eng.html',
    'dnd-cefcom-20090511.html': 'https://www.canada.ca/en/news/archive/2009/05/change-command-canadian-expeditionary-force-command-449469.html',
    'ckan-contract-history-metadata.json': 'https://open.canada.ca/data/api/action/package_show?id=4fe645a1-ffcd-40c1-9385-2c771be956a4',
    'ckan-tender-metadata.json': 'https://open.canada.ca/data/api/action/package_show?id=6abd20d4-7a1c-4b38-baa2-9525d0bb2fd2',
    'ckan-award-metadata.json': 'https://open.canada.ca/data/api/action/package_show?id=a1acb126-9ce8-40a9-b889-5da2b1dd20cb',
}

def main():
    log = []
    for filename, url in SOURCES.items():
        item = {'filename': filename, 'url': url, 'retrieved_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
        try:
            with urllib.request.urlopen(url, timeout=45) as resp:
                data = resp.read()
                item.update(status=resp.status, content_type=resp.headers.get('Content-Type'), last_modified=resp.headers.get('Last-Modified'), size_bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
            # Do not accidentally preserve an access-error response as a source file.
            if filename.endswith('.csv') and not data.lstrip().startswith(b'<'):
                rows = list(csv.DictReader(io.StringIO(data.decode('utf-8-sig'))))
                selected = [r for r in rows if any(t in str(r).lower() for t in ('draganfly','ws5853743341','cw2465414','cw2467949'))]
                # Preserve exact selected row fields; full source may be too large for Git.
                item['rows_total'] = len(rows)
                item['rows_selected'] = len(selected)
                (OUT / 'contract-history-selected-rows.json').write_text(json.dumps(selected, indent=2, ensure_ascii=False)+'\n')
                if len(data) < 40_000_000:
                    (OUT / filename).write_bytes(data)
                    item['archive_mode'] = 'native complete resource'
                else:
                    (Path('/tmp') / filename).write_bytes(data)
                    item['archive_mode'] = 'full source in temporary workspace; exact relevant rows archived'
            else:
                (OUT / filename).write_bytes(data)
                item['archive_mode'] = 'native complete resource'
        except Exception as exc:
            item['error'] = str(exc)
        log.append(item)
        print(filename, item.get('status', 'FAILED'), item.get('size_bytes'), item.get('rows_selected', ''), item.get('error',''), flush=True)
    (OUT / 'native-fetch-log.json').write_text(json.dumps(log, indent=2)+'\n')

if __name__ == '__main__':
    main()
