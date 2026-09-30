#!/usr/bin/env python3
"""Check article retrieval from 16 outlets using The News API's free plan.

Uses only Python's standard library. Reads THENEWSAPI_TOKEN from the
process environment, or asks for it without displaying it. Never writes
or prints the token. Does not change any existing application.

Source aliases are test inputs, not verified coverage. Successful retrieval does not establish complete coverage.
"""
from __future__ import annotations

import argparse
import calendar
import datetime as dt
import getpass
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

ENDPOINT = "https://api.thenewsapi.com/v1/news/all"
OUTLETS = [
    ("Reuters", ["reuters.com", "www.reuters.com", "us.reuters.com", "uk.reuters.com"]),
    ("Associated Press", ["apnews.com", "www.apnews.com"]),
    ("Bloomberg", ["bloomberg.com", "www.bloomberg.com"]),
    ("Wall Street Journal", ["wsj.com", "www.wsj.com", "online.wsj.com"]),
    ("New York Times", ["nytimes.com", "www.nytimes.com"]),
    ("Washington Post", ["washingtonpost.com", "www.washingtonpost.com"]),
    ("Politico", ["politico.com", "www.politico.com"]),
    ("CNN", ["cnn.com", "www.cnn.com", "edition.cnn.com"]),
    ("NBC", ["nbcnews.com", "www.nbcnews.com"]),
    ("NPR", ["npr.org", "www.npr.org"]),
    ("Defense News", ["defensenews.com", "www.defensenews.com"]),
    ("Breaking Defense", ["breakingdefense.com", "www.breakingdefense.com"]),
    ("Defense One", ["defenseone.com", "www.defenseone.com"]),
    ("Air & Space Forces Magazine", ["airandspaceforces.com", "www.airandspaceforces.com", "airforcemag.com"]),
    ("USNI News", ["news.usni.org"]),
    ("The War Zone", ["twz.com", "www.twz.com"]),
]


def month_bounds(month: str) -> tuple[str, str]:
    start = dt.datetime.strptime(month, "%Y-%m")
    end = start + dt.timedelta(days=calendar.monthrange(start.year, start.month)[1])
    return start.strftime("%Y-%m-%dT00:00:00"), end.strftime("%Y-%m-%dT00:00:00")


def request(token: str, domains: list[str], bounds=None) -> dict:
    parameters = {"domains": ",".join(domains), "limit": 3, "page": 1}
    if bounds:
        parameters.update(published_after=bounds[0], published_before=bounds[1])
    record = {"endpoint": ENDPOINT, "parameters": parameters,
              "requested_at_utc": dt.datetime.now(dt.timezone.utc).isoformat()}
    query = urllib.parse.urlencode({**parameters, "api_token": token})
    req = urllib.request.Request(ENDPOINT + "?" + query,
                                 headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            status, headers, payload = response.status, response.headers, response.read()
    except urllib.error.HTTPError as error:
        status, headers, payload = error.code, error.headers, error.read()
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        record.update(status="NETWORK_ERROR", error_type=type(error).__name__)
        return record
    record.update(http_status=status, quota_headers={
        k: v for k, v in headers.items() if "limit" in k.lower() or "usage" in k.lower()
    })
    try:
        body = json.loads(payload.decode("utf-8").replace(token, "[REDACTED]"))
    except (ValueError, UnicodeDecodeError):
        record["status"] = "UNPARSEABLE_RESPONSE"
        return record
    if not isinstance(body, dict):
        record["status"] = "UNEXPECTED_RESPONSE"
        return record
    record["response"] = body
    if status != 200 or "error" in body:
        record["status"] = "API_ERROR"
        return record
    data, meta = body.get("data"), body.get("meta", {})
    if not isinstance(data, list) or not isinstance(meta.get("found"), int):
        record["status"] = "UNEXPECTED_RESPONSE"
        return record
    record["found"] = meta["found"]
    if not data:
        record["status"] = "ZERO_RESULTS" if meta["found"] == 0 else "INCONSISTENT_RESPONSE"
        return record
    allowed = {domain.removeprefix("www.") for domain in domains}
    warnings = []
    for article in data:
        source = str(article.get("source", "")).lower().removeprefix("www.")
        host = (urllib.parse.urlparse(article.get("url", "")).hostname or "").removeprefix("www.")
        if source not in allowed and host not in allowed:
            warnings.append("Sample article did not match a requested source domain.")
        if bounds:
            published = str(article.get("published_at", ""))
            if not published.startswith(bounds[0][:7]):
                warnings.append("Sample publication date did not match the requested month.")
    record["warnings"] = sorted(set(warnings))
    record["status"] = "REVIEW_REQUIRED" if warnings else "ARTICLES_RETURNED"
    return record


def save(results: list[dict], month: str, output: Path, stopped: str | None) -> None:
    output.mkdir(parents=True, exist_ok=True)
    report = {"month": month, "outlets_requested": len(OUTLETS), "outlets_tested": len(results),
              "requests_attempted": sum(1 + ("undated_check" in row) for row in results),
              "stopped_reason": stopped, "results": results,
              "limitations": [
                  "This is a retrieval spot-check, not a completeness audit or source-catalogue census.",
                  "Counts cover all indexed subjects, not just Pentagon contracting.",
                  "Only up to three article samples per query are downloaded.",
                  "Zero results for tested domains are not proof the outlet is absent under every alias.",
                  "The War Zone's older thedrive.com/the-war-zone archive is not tested.",
                  "No claim that an article was unreported can be made from this test alone.",
              ]}
    (output / "newsapi_source_results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = ["THE NEWS API: 16-OUTLET RETRIEVAL CHECK", "Month: " + month,
             "Counts include ALL subjects, not just contracting.", ""]
    for row in results:
        query = row["month_check"]
        lines.append(f'{row["outlet"]}: {query["status"]}; monthly count: {query.get("found", "unknown")}')
        if "undated_check" in row:
            other = row["undated_check"]
            lines.append(f'  Without date filter: {other["status"]}; count: {other.get("found", "unknown")}')
        for article in query.get("response", {}).get("data", [])[:3]:
            lines.append("  Sample: " + str(article.get("title", "")))
            lines.append("  Published: " + str(article.get("published_at", "")))
            lines.append("  URL: " + str(article.get("url", "")))
            lines.append("  Description: " + str(article.get("description", "")))
            lines.append("  Snippet: " + str(article.get("snippet", "")))
        lines.append("")
    if stopped:
        lines.append("STOPPED: " + stopped)
    lines.extend(["LIMITATIONS", *report["limitations"]])
    (output / "newsapi_source_report.txt").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--month", default="2026-06", help="Month in YYYY-MM format")
    parser.add_argument("--output", default="newsapi_source_check", help="Output directory")
    parser.add_argument("--no-undated-check", action="store_true", help="Skip follow-up searches for zero-result outlets")
    args = parser.parse_args()
    try:
        bounds = month_bounds(args.month)
    except ValueError:
        parser.error("Use --month YYYY-MM, for example 2026-06")
    token = os.environ.get("THENEWSAPI_TOKEN", "").strip()
    if not token:
        token = getpass.getpass("The News API token (input hidden): ").strip()
    if not token:
        print("No token supplied. No requests sent.")
        return 1
    results, stopped = [], None
    for name, domains in OUTLETS:
        query = request(token, domains, bounds)
        row = {"outlet": name, "domains_tested": domains, "month_check": query}
        results.append(row)
        print(f'{name}: {query["status"]}; monthly count: {query.get("found", "unknown")}', flush=True)
        if query["status"] == "NETWORK_ERROR" or query.get("http_status") in (401, 402, 403, 429):
            stopped = "Connection, authentication, plan, or quota restriction. Unchecked outlets are NOT assessed."
        elif query["status"] == "ZERO_RESULTS" and not args.no_undated_check:
            time.sleep(1)
            row["undated_check"] = request(token, domains)
            other = row["undated_check"]
            if other["status"] == "NETWORK_ERROR" or other.get("http_status") in (401, 402, 403, 429):
                stopped = "Follow-up request encountered a connection, authentication, plan, or quota restriction."
        save(results, args.month, Path(args.output), stopped)
        if stopped:
            print(stopped)
            break
        time.sleep(1)
    print("Report and response records saved in: " + str(Path(args.output).resolve()))
    return 1 if stopped else 0


if __name__ == "__main__":
    raise SystemExit(main())
