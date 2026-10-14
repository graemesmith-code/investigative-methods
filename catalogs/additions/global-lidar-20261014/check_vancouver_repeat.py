#!/usr/bin/env python3
"""Anonymous bounded municipal tile metadata check; no ZIP payload downloads."""
import hashlib
import json
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import urlopen

records = []
for year, name in [(2013, '4830E_54540N'), (2018, '4830E_54540N'), (2022, '483000_5454000')]:
    url = (f'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/lidar-{year}/records?'
           + urlencode({'where': f'name="{name}"', 'limit': 1}))
    item = {'year': year, 'url': url}
    try:
        with urlopen(url, timeout=30) as response:
            raw = response.read(10001)
            item['http_status'] = response.status
        if len(raw) > 10000:
            raise ValueError('Metadata exceeded 10KB budget')
        data = json.loads(raw)
        if data['total_count'] != 1 or data['results'][0]['name'] != name:
            raise ValueError('Expected exact one matching named tile')
        item.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), tile=data['results'][0])
    except Exception as error:
        item['error'] = str(error)
    records.append(item)
print(json.dumps({'checked_utc': datetime.now(timezone.utc).isoformat(), 'records': records,
                  'note': 'Compare polygons with coordinate rounding tolerance. Metadata only; no payload or surface analysis.'}, indent=2))
