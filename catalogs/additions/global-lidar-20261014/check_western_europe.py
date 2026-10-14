#!/usr/bin/env python3
"""Anonymous small metadata checks; production cloud range stops unless HTTP206.
No authentication, full cloud downloads or certificate overrides.
"""
import json, struct, urllib.parse, urllib.request

def fetch_json(url, maximum=500000):
    with urllib.request.urlopen(url, timeout=30) as r:
        raw = r.read(maximum + 1)
        if len(raw) > maximum:
            raise ValueError('Metadata exceeds byte budget')
        return json.loads(raw), {'url': url, 'http_status': r.status, 'bytes': len(raw)}

results = {}
base = 'https://environment.data.gov.uk/spatialdata/survey-index-files/wfs'
p = dict(service='WFS', version='2.0.0', request='GetFeature',
         typeNames='dataset-9f0fa3fc-a860-4729-adc9-47fe53f658d0:National_LIDAR_Programme_Index_Catalogue',
         outputFormat='application/json', count=20, srsName='EPSG:27700',
         bbox='537600,180200,537610,180210,EPSG:27700')
u = base + '?' + urllib.parse.urlencode(p)
j, meta = fetch_json(u)
results['england_docklands'] = dict(meta, records=[f['properties'] for f in j['features']])
u = 'https://data.geo.admin.ch/api/stac/v1/collections/ch.swisstopo.swisssurface3d/items?bbox=8.537,47.372,8.54,47.374&limit=100'
j, meta = fetch_json(u)
results['switzerland_zurich'] = dict(meta, records=[{'id': f['id'], 'bbox': f['bbox'], 'properties': f['properties'], 'assets': f['assets']} for f in j['features']])
f = next(f for f in j['features'] if f['id'] == 'swisssurface3d_2024_2682-1247')
u = next(iter(f['assets'].values()))['href']
req = urllib.request.Request(u, headers={'Range': 'bytes=0-4095'})
with urllib.request.urlopen(req, timeout=30) as r:
    if r.status != 206:
        raise ValueError('Server did not honor range; no asset read')
    b = r.read(4096)
    if b[:4] != b'LASF':
        raise ValueError('Unexpected LAS signature')
    results['swiss_range_header'] = {'url': u, 'http_status': r.status,
        'content_range': r.headers.get('Content-Range'), 'bytes': len(b),
        'las_version': f'{b[24]}.{b[25]}', 'point_format_and_compression_flag': b[104],
        'bounds_maxmin_xyz': struct.unpack('<6d', b[179:227])}
print(json.dumps(results, indent=2))
