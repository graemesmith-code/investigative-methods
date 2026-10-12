"""Fetch Nexa Peru's observed public document registry; never infer production year.

This endpoint was observed in the company's own file-manager JavaScript and
successfully tested on 12 October 2026. No credentials or paid service needed.
"""
import argparse
import datetime
import hashlib
import json
import time
import urllib.request
from pathlib import Path

BASE = 'https://api.mziq.com/mzfilemanager/company/fa653160-ea78-4cd6-897a-335d2c6c4b9f'
CATEGORIES = ['annual_reports', 'results_center_informes_de_governanca']


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--year', type=int, action='append', required=True,
                    help='Registry bucket, NOT necessarily the production year; repeat as needed')
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--user-agent', required=True, help='Identify your project and a real contact')
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    queries = [('nexa-es-years.json', '/categoryInternalName/document/language/years',
                {'categoryInternalNames': CATEGORIES, 'language_code': 'es_ES'})]
    for year in dict.fromkeys(args.year):
        if not 2000 <= year <= 2100:
            ap.error('Year outside expected registry range')
        queries.append((f'nexa-es-{year}-registry.json', '/filter/categories/year/meta',
                        {'year': year, 'categories': CATEGORIES,
                         'language': 'es_ES', 'published': True}))
    failed = False
    for name, route, payload in queries:
        entry = {'id': name, 'url': BASE + route, 'method': 'POST',
                 'request_encoding': 'json', 'request_fields': payload,
                 'tested_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
        started = time.perf_counter()
        try:
            request = urllib.request.Request(entry['url'], json.dumps(payload).encode(),
                      headers={'Content-Type': 'application/json', 'User-Agent': args.user_agent})
            with urllib.request.urlopen(request, timeout=35) as response:
                content = response.read()
                entry['status'] = response.status
            digest = hashlib.sha256(content).hexdigest()
            dest = args.output / name
            if dest.exists() and dest.read_bytes() != content:
                dest = args.output / (name + '.version-' + digest[:12])
            dest.write_bytes(content)
            document = json.loads(content)
            if document.get('success') is not True:
                raise ValueError('Registry returned unsuccessful envelope')
            if route.endswith('/meta'):
                metas = document['data']['document_metas']
                if not isinstance(metas, list):
                    raise ValueError('Unexpected document metadata shape')
                entry['document_count'] = len(metas)
            entry.update(bytes=len(content), sha256=digest, saved_as=str(dest))
        except Exception as exc:
            entry['error'] = str(exc)
            failed = True
        entry['elapsed_seconds'] = round(time.perf_counter() - started, 4)
        with (args.output / 'registry-access-log.jsonl').open('a') as log:
            log.write(json.dumps(entry) + '\n')
        print(json.dumps(entry))
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
