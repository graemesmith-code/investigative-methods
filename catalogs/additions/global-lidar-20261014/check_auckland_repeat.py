"""Small anonymous metadata-only footprint check. No point-cloud/raster downloads."""
import hashlib
import json
import urllib.request
from datetime import datetime, timezone

SOURCES = {
    'auckland-2013-boundary.json': 'https://raw.githubusercontent.com/OpenTopography/Data_Catalog_Spatial_Boundaries/main/OpenTopography_Point_Cloud_Lidar/Auckland_2013.geojson',
    'BA31_10000_0405.json': 'https://nz-elevation.s3.ap-southeast-2.amazonaws.com/auckland/auckland-part-1_2024/dsm_1m/2193/BA31_10000_0405.json',
    'collection.json': 'https://nz-elevation.s3.ap-southeast-2.amazonaws.com/auckland/auckland-part-1_2024/dsm_1m/2193/collection.json',
}

def in_ring(point, ring):
    x, y = point
    crossing = False
    for a, b in zip(ring, ring[1:] + ring[:1]):
        if (a[1] > y) != (b[1] > y) and x < (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]) + a[0]:
            crossing = not crossing
    return crossing

def in_polygon(point, rings):
    return in_ring(point, rings[0]) and not any(in_ring(point, ring) for ring in rings[1:])

def contains(point, geometry):
    if geometry['type'] == 'MultiPolygon':
        return any(in_polygon(point, polygon) for polygon in geometry['coordinates'])
    if geometry['type'] == 'Polygon':
        return in_polygon(point, geometry['coordinates'])
    raise ValueError('Unsupported geometry type')

if __name__ == '__main__':
    datasets = {}
    checks = {}
    for name, url in SOURCES.items():
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read(100_001)
            if len(data) > 100_000:
                raise ValueError('Metadata exceeded 100 KB budget')
        datasets[name] = json.loads(data)
        checks[name] = {"url": url, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    point = (174.72, -36.85)
    result = {
        'checked_utc': datetime.now(timezone.utc).isoformat(),
        'sources': checks,
        'point_lon_lat': point,
        'point_in_2013_polygon': contains(point, datasets['auckland-2013-boundary.json']['geometry']),
        'point_in_2024_tile_geometry': contains(point, datasets['BA31_10000_0405.json']['geometry']),
        'tile_2024': 'BA31_10000_0405',
        'note': 'Metadata footprint verification only. Tile geometry may include no-data; no raster or point-cloud values tested.',
    }
    print(json.dumps(result, indent=2))
