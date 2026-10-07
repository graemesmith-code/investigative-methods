"""Bounded public-record refresh, separate from September baseline. No retries."""
import datetime, hashlib, json, pathlib, urllib.request
P = pathlib.Path(__file__).resolve().parents[1]
S = P / 'sources'
MANIFEST = S / 'manifest.json'
AWARD = 'CONT_IDV_SPE60523D9402_9700'

def fetch(name, endpoint, body):
    path = S / name
    if path.exists():
        return json.loads(path.read_text())
    request_name = name + '.request.json'
    (S / request_name).write_text(json.dumps(body, indent=2) + '\n')
    url = 'https://api.usaspending.gov/api/v2/' + endpoint
    row = {'name': name, 'url': url, 'method': 'POST', 'request_file': request_name,
           'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'tls_verification': True, 'baseline': False}
    try:
        request = urllib.request.Request(url, data=json.dumps(body).encode(),
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
        with urllib.request.urlopen(request, timeout=25) as response:
            data = response.read(3_000_001)
            if len(data) > 3_000_000: raise RuntimeError('Response bound exceeded')
            row['status'] = response.status
        path.write_bytes(data)
        row.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        return json.loads(data)
    except Exception as error:
        row.update(error_type=type(error).__name__, status=getattr(error, 'code', None))
        raise
    finally:
        records = json.loads(MANIFEST.read_text())
        records.append(row)
        MANIFEST.write_text(json.dumps(records, indent=2) + '\n')

def main():
    children = fetch('nai-child-awards-corrected-page1.json', 'idvs/awards/',
        {'award_id': AWARD, 'type': 'child_awards', 'page': 1, 'limit': 100,
         'sort': 'piid', 'order': 'asc'})
    if children['page_metadata']['hasNext'] or len(children['results']) > 30:
        raise RuntimeError('Child coverage exceeds frozen 30-award bound')
    output = []
    for child in children['results']:
        name = 'nai-child-' + child['piid'] + '-transactions.json'
        history = fetch(name, 'transactions/',
            {'award_id': child['generated_unique_award_id'], 'page': 1, 'limit': 100,
             'sort': 'action_date', 'order': 'asc'})
        if history['page_metadata']['hasNext']:
            raise RuntimeError('Child history exceeds frozen 100-row bound')
        output.append({'award': child, 'transactions_source': name,
                       'transactions': history['results']})
        print(child['piid'], len(history['results']), flush=True)
    (P / 'nai-child-history.json').write_text(json.dumps(output, indent=2) + '\n')

if __name__ == '__main__': main()
