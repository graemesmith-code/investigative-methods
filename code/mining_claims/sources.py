"""Fetch or verify the exact inspected originals; changed bytes require review."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import time
import urllib.request
import zipfile
from run import HERE, RESEARCH, load_json


def verify(path, record):
    if not path.is_file():
        raise ValueError(f"missing source: {record['source_id']}")
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != record["sha256"] or len(data) != record["bytes"]:
        raise ValueError(f"changed source: {record['source_id']}; re-audit before comparison")
    name = record["source_id"]
    if name.endswith(".pdf") and not data.startswith(b"%PDF-"):
        raise ValueError(f"not a PDF: {name}")
    if name.endswith((".xlsx", ".bin")) and not zipfile.is_zipfile(path):
        raise ValueError(f"not an Excel archive: {name}")
    if name.endswith(".html") and b"<html" not in data[:20000].lower():
        raise ValueError(f"not HTML: {name}")
    return digest


def selected_sources(case_id=None, all_audit=False):
    manifest = load_json(RESEARCH / "source-manifest.json")
    cases = [load_json(p) for p in sorted((HERE / "cases").glob("*.json"))]
    if case_id:
        cases = [c for c in cases if c["id"] == case_id]
        if not cases:
            raise ValueError("unknown retained case")
    ids = {s for c in cases for s in c["source_ids"]}
    return [s for s in manifest if all_audit or s["source_id"] in ids]


def fetch_one(record, cache, user_agent):
    """Stream to a temporary file; never replace a verified specimen with a revision."""
    path = cache / record["source_id"]
    if path.exists():
        verify(path, record)
        return {"source_id": record["source_id"], "status": "verified_cached"}
    temporary = path.with_name(path.name + ".partial")
    if temporary.exists():
        raise ValueError(f"partial download already exists: {temporary}")
    request = urllib.request.Request(record["url"], headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(request, timeout=60) as response, temporary.open("xb") as out:
            size = 0
            while chunk := response.read(1024 * 1024):
                size += len(chunk)
                if size > max(record["bytes"] * 2, 5_000_000):
                    raise ValueError("unexpected response size")
                out.write(chunk)
            final_url = response.url
        verify(temporary, record)
        temporary.rename(path)
        return {"source_id": record["source_id"], "status": "downloaded_verified", "final_url": final_url}
    except Exception:
        if temporary.exists():
            temporary.unlink()
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=HERE / "cache")
    parser.add_argument("--case", choices=["RAB-MIN-02", "RAB-MIN-03", "RAB-MIN-07", "RAB-MIN-08"])
    parser.add_argument("--all-audit", action="store_true", help="Include sources for all ten audited cases")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if args.case and args.all_audit:
        parser.error("choose --case or --all-audit")
    agent = os.environ.get("RABBIT_HTTP_USER_AGENT", "")
    if not args.verify_only and not agent:
        parser.error("set RABBIT_HTTP_USER_AGENT to a descriptive research agent and contact address")
    args.cache.mkdir(parents=True, exist_ok=True)
    failed = False
    for source in selected_sources(args.case, args.all_audit):
        event = {"tested_at_utc": datetime.now(timezone.utc).isoformat(), "source_id": source["source_id"]}
        try:
            if args.verify_only:
                event.update(status="verified", sha256=verify(args.cache / source["source_id"], source))
            else:
                event.update(fetch_one(source, args.cache, agent))
        except Exception as exc:
            failed = True
            event.update(status="blocked", error=str(exc))
        with (args.cache / "retrieval-log.jsonl").open("a", encoding="utf-8") as out:
            out.write(json.dumps(event, ensure_ascii=False) + "\n")
        print(json.dumps(event, ensure_ascii=False))
        if not args.verify_only:
            time.sleep(0.25)
    return 2 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
