#!/usr/bin/env python3
"""Re-fetch selected public sources, recording new hashes without overwriting the archive."""
import argparse
import hashlib
import json
import os
import pathlib
import time
import urllib.request

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidate', help='For example RAB-MIN-02')
    p.add_argument('--all', action='store_true', help='Fetch all sources in the source manifest')
    p.add_argument('--output', default='refetched')
    a = p.parse_args()
    if not a.candidate and not a.all:
        p.error('Choose --candidate or --all')
    root = pathlib.Path(__file__).resolve().parent
    manifest = json.loads((root/'source-manifest.json').read_text())
    profiles = json.loads((root/'candidates.json').read_text())['candidates']
    if a.candidate:
        matches = [x for x in profiles if x['id'] == a.candidate]
        if len(matches) != 1:
            p.error('Unknown candidate ID')
        ids = set(matches[0]['western'] + matches[0]['host'])
        manifest = [x for x in manifest if x['id'] in ids]
    agent = os.environ.get('RABBIT_HTTP_USER_AGENT')
    if not agent:
        p.error('Set RABBIT_HTTP_USER_AGENT to a descriptive research User-Agent with your contact address for SEC access.')
    out = pathlib.Path(a.output)
    out.mkdir(parents=True, exist_ok=True)
    log = []
    for src in manifest:
        item = {'id':src['id'], 'url':src['url'], 'tested_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
        try:
            req = urllib.request.Request(src['url'], headers={'User-Agent':agent})
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
                item.update(status=r.status, content_type=r.headers.get('Content-Type'), final_url=r.url)
            dest = out / src['download_filename']
            dest.write_bytes(body)
            item.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest(), path=str(dest))
            item['unchanged_since_research'] = item['sha256'] == src['sha256']
        except Exception as exc:
            item['error'] = str(exc)
        log.append(item)
        print(json.dumps(item, ensure_ascii=False), flush=True)
        time.sleep(1.1)
    (out/'new-access-log.json').write_text(json.dumps(log, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
