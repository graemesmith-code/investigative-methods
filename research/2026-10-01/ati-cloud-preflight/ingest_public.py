"""Public-only snapshot; no credentials or paid provider calls."""
import collections, csv, datetime, hashlib, json, pathlib, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).parent / 'corpus'
RESOURCE = '19383ca2-b01a-487d-88f7-e1ffbc7d39c2'
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

def main():
    ROOT.mkdir(exist_ok=False)
    opener = urllib.request.build_opener(NoRedirect)
    manifest = {'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'resource_id': RESOURCE, 'requests': [], 'institutions': {}}
    rows = []
    for org in ['dfatd-maecd', 'dnd-mdn']:
        collected = []
        total = None
        offset = 0
        while True:
            url = 'https://open.canada.ca/data/api/3/action/datastore_search?' + urllib.parse.urlencode({'resource_id': RESOURCE, 'filters': json.dumps({'owner_org': org, 'year': 2026}), 'sort': '_id asc', 'limit': 250, 'offset': offset})
            with opener.open(url, timeout=45) as response:
                body = response.read()
                status = response.status
            name = f'{org}-{offset:05d}.json'
            (ROOT / name).write_bytes(body)
            manifest['requests'].append({'url': url, 'file': name, 'http_status': status, 'sha256': hashlib.sha256(body).hexdigest(), 'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()})
            payload = json.loads(body)
            assert payload['success'] is True
            result = payload['result']
            if total is None:
                total = result['total']
            assert result['total'] == total, 'Total changed during pagination'
            page = result['records']
            assert all(r['owner_org'] == org and r['year'] == 2026 for r in page)
            if not page:
                break
            collected.extend(page)
            offset += len(page)
            if offset >= total:
                break
        assert len(collected) == total
        ids = [r['_id'] for r in collected]
        assert ids == sorted(set(ids)), 'Repeated or unsorted IDs'
        assert all(1 <= r['month'] <= 12 and r['pages'] >= 0 for r in collected)
        assert all(r['disposition'] in {'DA','DP','EC','EX','NE'} for r in collected)
        keys = collections.Counter(r['request_number'] for r in collected)
        manifest['institutions'][org] = {'reported_total': total, 'retrieved': len(collected), 'unique_ids': len(set(ids)), 'repeated_request_numbers': {k:v for k,v in keys.items() if v>1}, 'closure_months': dict(sorted(collections.Counter(r['month'] for r in collected).items())), 'dispositions': dict(collections.Counter(r['disposition'] for r in collected)), 'released_pages_sum': sum(r['pages'] for r in collected)}
        rows.extend(collected)
    assert len({r['_id'] for r in rows}) == len(rows)
    fingerprints = collections.Counter(json.dumps({k:v for k,v in r.items() if k != '_id'},sort_keys=True,ensure_ascii=False) for r in rows)
    manifest['total'] = len(rows)
    manifest['exact_duplicate_rows_excluding_id'] = sum(v-1 for v in fingerprints.values())
    manifest['completed_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (ROOT/'records.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    with (ROOT/'records.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if k!='requests'},ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
