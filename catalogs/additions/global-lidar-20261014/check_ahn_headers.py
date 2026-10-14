#!/usr/bin/env python3
"""Anonymous bounded AHN index/header check; never downloads full point clouds.
Run: python3 check_ahn_headers.py > fresh-ahn-check.json
The coordinates select a Rotterdam civilian tile, not a target identification.
"""
import hashlib
import json
import struct
from datetime import datetime, timezone
from urllib.request import Request, urlopen

INDEX_LIMIT = 3_000_000
HEADER_LIMIT = 4096
POINT = (93000, 437000)  # EPSG:28992; Rotterdam
records = []
for version in (3, 4):
    url = ("https://basisdata.nl/hwh-portal/20230609_tmp/links/"
           f"nationaal/Nederland/AHN{version}_PC.json")
    record = {"epoch": f"AHN{version}", "index_url": url}
    try:
        with urlopen(url, timeout=30) as response:
            raw = response.read(INDEX_LIMIT + 1)
        if len(raw) > INDEX_LIMIT:
            raise ValueError("Index exceeded bounded download limit")
        index = json.loads(raw)
        matches = []
        for feature in index["features"]:
            ring = feature["geometry"]["coordinates"][0]
            xs, ys = zip(*ring)
            if min(xs) <= POINT[0] < max(xs) and min(ys) <= POINT[1] < max(ys):
                matches.append(feature)
        if len(matches) != 1:
            raise ValueError(f"Expected one tile; got {len(matches)}")
        feature = matches[0]
        record.update(index_bytes=len(raw), index_sha256=hashlib.sha256(raw).hexdigest(),
                      feature_count=len(index["features"]), selected_feature=feature,
                      selection_rd_xy=POINT)
        request = Request(feature["properties"]["file"],
                          headers={"Range": f"bytes=0-{HEADER_LIMIT-1}"})
        with urlopen(request, timeout=30) as response:
            record.update(http_status=response.status,
                          content_range=response.headers.get("Content-Range"))
            if response.status != 206:
                raise ValueError("Server did not honor Range; stopped without full download")
            header = response.read(HEADER_LIMIT)
        if header[:4] != b"LASF" or len(header) < 375:
            raise ValueError("Missing or incomplete LAS header")
        record.update(sample_bytes=len(header), sample_sha256=hashlib.sha256(header).hexdigest(),
                      las_header={
                          "version": f"{header[24]}.{header[25]}",
                          "point_format_byte": header[104],
                          "point_format_without_compression_bits": header[104] & 63,
                          "legacy_point_count": struct.unpack_from("<I", header, 107)[0],
                          "scales": struct.unpack_from("<3d", header, 131),
                          "offsets": struct.unpack_from("<3d", header, 155),
                          "max_min_xyz": struct.unpack_from("<6d", header, 179),
                          "creation_day": struct.unpack_from("<H", header, 90)[0],
                          "creation_year": struct.unpack_from("<H", header, 92)[0],
                      })
        if header[25] >= 4:
            record["las_header"]["extended_point_count"] = struct.unpack_from("<Q", header, 247)[0]
    except Exception as error:
        record["error"] = str(error)
    records.append(record)
print(json.dumps({"checked_utc": datetime.now(timezone.utc).isoformat(),
                  "purpose": "Metadata/header check only; acquisition dates and point classifications not decoded",
                  "records": records}, indent=2))
