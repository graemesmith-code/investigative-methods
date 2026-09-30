#!/usr/bin/env python3
"""Reproduce aggregate ATI corpus counts without retaining unrelated records.

Python 3 standard library only. Two public read-only GET requests; no key,
account, model API, document request or payment. Counts can change between runs.
The default output is stdout. An existing --output file is never overwritten.
"""

import argparse
import datetime
import hashlib
import json
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request


ORGANIZATIONS = {
    "dfatd-maecd": "Global Affairs Canada",
    "dnd-mdn": "National Defence",
}
BASE_URL = "https://search.open.canada.ca/ati/"


def summarize_response(payload, owner_org):
    """Return aggregate fields only; deliberately omit payload['docs']."""
    if not isinstance(payload, dict) or not isinstance(payload.get("num_count"), int):
        raise ValueError("Unexpected response: integer num_count is missing")
    facets = payload.get("facets")
    if not isinstance(facets, dict):
        raise ValueError("Unexpected response: facets object is missing")
    disposition_rows = facets.get("disposition")
    month_rows = facets.get("month")
    if not isinstance(disposition_rows, list) or not isinstance(month_rows, list):
        raise ValueError("Unexpected response: disposition/month facets missing")
    dispositions = []
    for row in disposition_rows:
        if not isinstance(row.get("count"), int):
            raise ValueError("Unexpected disposition count")
        dispositions.append({"code": row["code"], "label": row.get("label_en"),
                             "count": row["count"]})
    months = []
    for row in month_rows:
        if not isinstance(row.get("count"), int):
            raise ValueError("Unexpected month count")
        months.append({"month": int(row["code"]), "label": row.get("label_en"),
                       "count": row["count"]})
    if sum(row["count"] for row in dispositions) != payload["num_count"]:
        raise ValueError("Disposition totals do not reconcile with num_count")
    if sum(row["count"] for row in months) != payload["num_count"]:
        raise ValueError("Month totals do not reconcile with num_count")
    # Check that the page actually respects the requested organization filter.
    for row in payload.get("docs", []):
        if row.get("owner_org") != owner_org:
            raise ValueError("Organization filter mismatch in returned page")
    return {
        "organization_code": owner_org,
        "organization": ORGANIZATIONS[owner_org],
        "num_count": payload["num_count"],
        "fully_or_partly_disclosed_count": sum(
            row["count"] for row in dispositions if row["code"] in {"DA", "DP"}
        ),
        "dispositions": dispositions,
        "completion_months_returned": sorted(months, key=lambda row: row["month"]),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", type=int, default=2026)
    parser.add_argument("--output", type=pathlib.Path,
                        help="Write JSON to a new file instead of stdout")
    args = parser.parse_args()
    if not 2000 <= args.year <= 2100:
        parser.error("--year must be between 2000 and 2100")
    if args.output and args.output.exists():
        parser.error("--output already exists; choose a new filename")

    result = {
        "probe": "Canadian completed ATI request aggregate counts",
        "year_filter": args.year,
        "started_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "requests": [],
        "interpretation": [
            "The year/month refer to completed-request summary fields, not event dates.",
            "Fully/partly disclosed is an access proxy, not evidence of useful content.",
            "Results are live aggregates and can change between runs.",
            "Unrelated first-page records are not retained.",
        ],
    }
    failed = False
    for owner_org in ORGANIZATIONS:
        query = urllib.parse.urlencode({"owner_org": owner_org,
                                       "year": args.year, "search_format": "json"})
        url = BASE_URL + "?" + query
        record = {"url": url, "method": "GET"}
        try:
            request = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(request, timeout=45) as response:
                body = response.read()
                record.update({"http_status": response.status,
                               "response_bytes": len(body),
                               "response_sha256": hashlib.sha256(body).hexdigest()})
            payload = json.loads(body)
            # Check year as well as organization to detect silently ignored filters.
            if any(row.get("year") != args.year for row in payload.get("docs", [])):
                raise ValueError("Year filter mismatch in returned page")
            record.update(summarize_response(payload, owner_org))
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as exc:
            failed = True
            record["error"] = str(exc)
            if isinstance(exc, urllib.error.HTTPError):
                record["http_status"] = exc.code
        record["observed_at_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        result["requests"].append(record)

    if not failed:
        result["combined_num_count"] = sum(x["num_count"] for x in result["requests"])
        result["combined_fully_or_partly_disclosed_count"] = sum(
            x["fully_or_partly_disclosed_count"] for x in result["requests"]
        )
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(text)
    else:
        sys.stdout.write(text)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
