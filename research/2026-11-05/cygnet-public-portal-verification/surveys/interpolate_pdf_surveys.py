#!/usr/bin/env python3
"""Extract private PDF survey/stage data and interpolate screening locations.

Requires PyMuPDF. Outputs are private derivatives of supplied PDFs.
No network access. Linear interpolation is of reported ND/ED/TVD by measured
depth, not a new minimum-curvature survey calculation. The optional geographic
projection assumes reported ND/ED are true-north/east offsets from the supplied
WGS84 pad coordinate. That datum/origin is NOT independently established.
"""
import argparse
import bisect
import csv
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path

import fitz

NUMBER = r"-?[\d,]+(?:\.\d+)?"
SURVEY_RE = re.compile(r"Original Hole\s+" + r"\s+".join([f"({NUMBER})"] * 7))
STAGE_RE = re.compile(r"(?m)^(\d{1,2})\n(\d{4}\.\d+)\n(\d{4}\.\d+)\n")


def get_surveys(path):
    rows = {}
    with fitz.open(path) as doc:
        for page_number, page in enumerate(doc, 1):
            for match in SURVEY_RE.finditer(page.get_text()):
                md, dev, direction, tvd, nd, ed, dls = [float(x.replace(",", "")) for x in match.groups()]
                values = (dev, direction, tvd, nd, ed, dls)
                if md in rows:
                    if rows[md]["values"][:5] != values[:5]:
                        raise ValueError(f"Conflicting survey at MD {md} in {path.name}")
                    rows[md]["dls_variants"].add(dls)
                    rows[md]["pages"].append(page_number)
                else:
                    rows[md] = {"values": values, "pages": [page_number], "dls_variants": {dls}}
    if len(rows) < 2:
        raise ValueError(f"Insufficient survey rows in {path}")
    return rows


def interpolate(rows, md):
    depths = sorted(rows)
    if not depths[0] <= md <= depths[-1]:
        raise ValueError(f"Refusing extrapolation for MD {md}; survey {depths[0]}..{depths[-1]}")
    i = bisect.bisect_left(depths, md)
    lo, hi = (depths[i], depths[i]) if depths[i] == md else (depths[i-1], depths[i])
    f = 0 if hi == lo else (md-lo)/(hi-lo)
    v0, v1 = rows[lo]["values"], rows[hi]["values"]
    return {
        "tvd_m": v0[2] + f * (v1[2]-v0[2]),
        "north_offset_m": v0[3] + f * (v1[3]-v0[3]),
        "east_offset_m": v0[4] + f * (v1[4]-v0[4]),
        "survey_lower_md_m": lo,
        "survey_upper_md_m": hi,
        "survey_lower_pages": ";".join(map(str, sorted(set(rows[lo]["pages"])))),
        "survey_upper_pages": ";".join(map(str, sorted(set(rows[hi]["pages"])))),
    }


def write_csv(path, rows):
    if not rows:
        return
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("pdf_directory", type=Path)
    p.add_argument("output_directory", type=Path)
    p.add_argument("--manifest", type=Path, required=True, help="Private JSON mapping well labels to [drilling PDF, service PDF, expected interval count]")
    p.add_argument("--assumed-pad-latitude", type=float)
    p.add_argument("--assumed-pad-longitude", type=float)
    args = p.parse_args()
    if (args.assumed_pad_latitude is None) != (args.assumed_pad_longitude is None):
        p.error("Supply both pad coordinates or neither")
    args.output_directory.mkdir(parents=True, exist_ok=True)
    all_surveys, all_stages, provenance = [], [], []
    wells = json.loads(args.manifest.read_text())
    for well, (drilling_name, service_name, expected) in wells.items():
        drilling = args.pdf_directory / drilling_name
        service = args.pdf_directory / service_name
        rows = get_surveys(drilling)
        for md, r in sorted(rows.items()):
            dev, direction, tvd, nd, ed, dls = r["values"]
            all_surveys.append(dict(well=well, md_m=md, inclination_deg=dev, azimuth_deg=direction, tvd_m=tvd, north_offset_m=nd, east_offset_m=ed, dls_deg_per_30m=";".join(map(str, sorted(r["dls_variants"]))), source_file=drilling_name, source_pages=";".join(map(str,sorted(set(r["pages"]))))))
        with fitz.open(service) as doc:
            stages = [(int(m[1]), float(m[2]), float(m[3])) for m in STAGE_RE.finditer(doc[2].get_text())]
        if len(stages) != expected or [s[0] for s in stages] != list(range(1, expected+1)):
            raise ValueError(f"Unexpected stage rows in {service_name}: {stages}")
        for stage, top, bottom in stages:
            for position, md in [("top_perforation", top), ("midpoint", (top+bottom)/2), ("bottom_perforation", bottom)]:
                if min(rows) <= md <= max(rows):
                    values = interpolate(rows, md)
                    status = "planned interval geometry, not proof interval was pumped"
                else:
                    values = dict(tvd_m=None, north_offset_m=None, east_offset_m=None, survey_lower_md_m=None, survey_upper_md_m=None, survey_lower_pages="", survey_upper_pages="")
                    status = "outside extracted survey range; no extrapolation"
                row = dict(well=well, stage=stage, position=position, measured_depth_m=md, **values, survey_file=drilling_name, perforation_file=service_name, perforation_page=3, status=status)
                if args.assumed_pad_latitude is not None and values["tvd_m"] is not None:
                    # First-order local WGS84 ellipsoid scaling. Suitable for
                    # broad catalogue searches, not surveyed absolute positions.
                    phi = math.radians(args.assumed_pad_latitude)
                    a, e2 = 6378137.0, 0.0066943799901413165
                    w = math.sqrt(1 - e2*math.sin(phi)**2)
                    meridian_radius = a*(1-e2)/w**3
                    prime_vertical_radius = a/w
                    lat = args.assumed_pad_latitude + math.degrees(row["north_offset_m"]/meridian_radius)
                    lon = args.assumed_pad_longitude + math.degrees(row["east_offset_m"]/(prime_vertical_radius*math.cos(phi)))
                    row.update(approximate_latitude=lat, approximate_longitude=lon, coordinate_caveat="Unverified common pad origin and ND/ED reference/datum; first-order WGS84 screening only")
                elif args.assumed_pad_latitude is not None:
                    row.update(approximate_latitude=None, approximate_longitude=None, coordinate_caveat="No extrapolation")
                all_stages.append(row)
        for source in [drilling, service]:
            provenance.append({"file":source.name,"sha256":hashlib.sha256(source.read_bytes()).hexdigest(),"physical_pages":len(fitz.open(source))})
    write_csv(args.output_directory/"survey_points_private.csv", all_surveys)
    write_csv(args.output_directory/"stage_locations_private.csv", all_stages)
    (args.output_directory/"geometry_provenance_private.json").write_text(json.dumps({"accessed_utc":datetime.now(timezone.utc).isoformat(),"method":"Linear interpolation of reported ND/ED/TVD by MD. No extrapolation. Planned intervals include skipped stages.","assumed_pad_latitude":args.assumed_pad_latitude,"assumed_pad_longitude":args.assumed_pad_longitude,"warning":"Unknown wellhead-specific origin, coordinate datum and survey north reference. Geographic coordinates are approximate and not suitable for attribution or fine distance thresholds.","sources":provenance},indent=2))
    print(f"Extracted {len(all_surveys)} unique survey rows; generated {len(all_stages)} interval-location rows")


if __name__ == "__main__":
    main()
