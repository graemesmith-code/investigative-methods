#!/usr/bin/env python3
"""Screen the verified FWI inputs without network requests or paid services.

The SQLite workspace is private; only derived registers/accounting are published.
Classification is a deliberately broad machine screen, never a capability finding.
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
from decimal import Decimal, InvalidOperation
import gzip
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import sys
import tarfile
import time

# Full descriptions exceed csv's small default field limit; never truncate them.
csv.field_size_limit(sys.maxsize)

EXPECTED = {
    "FWI-20261016-normalized-research-context.tar.gz": "b9ad7acc6061f21792c4d26efc57940e4506702e22c490046d69f5e5b292a8eb",
    "FWI-20261016-normalized-rd-contracts.tar.gz": "63809f0fbf8fc5427341e637054cfe2012f6f7f5c28379af9178f735a6762317",
    "FWI-20261016-normalized-capabilities.tar.gz": "a06375165baf25a4532ee6bef8c3cb47aba05ebb6c03cc55db8253487953b96e",
}
EXPECTED_ROWS = {
    "apfit_fy2022_projects.jsonl.gz": 10, "apfit_pages.jsonl.gz": 11,
    "army_budget_pages.jsonl.gz": 0, "commons_pages.jsonl.gz": 26,
    "commons_projects.jsonl.gz": 57, "darpa_budget_pages.jsonl.gz": 252,
    "darpa_pb2025_programs.jsonl.gz": 256, "doe_ldrd_pages.jsonl.gz": 167,
    "doe_ldrd_table1_fy2019_2025.jsonl.gz": 123,
    "federal_funds_source_rows.jsonl.gz": 8355, "ffrdc_source.jsonl.gz": 862,
    "financial_actions.jsonl.gz": 712186, "govinfo_budget_pages.jsonl.gz": 114,
    "grants.jsonl.gz": 3283, "grants_selected_source.jsonl.gz": 3283,
    "navy_budget_pages.jsonl.gz": 0, "omb_security_fy2019_2026.jsonl.gz": 38600,
    "sandia_ldrd_pages.jsonl.gz": 131, "sbir.jsonl.gz": 18814,
    "sbir_current.jsonl.gz": 25770, "usaspending_dod_research_grants.jsonl.gz": 88273,
    "usaspending_dod_research_grants_subawards.jsonl.gz": 14143,
    "usaspending_darpa.jsonl.gz": 12057,
    "usaspending_dod_capabilities.jsonl.gz": 305768,
    "usaspending_dod_capabilities_fy2019.jsonl.gz": 24383,
    "usaspending_dod_capabilities_fy2026.jsonl.gz": 35822,
    "usaspending_dod_rd_contracts.jsonl.gz": 342900,
    "usaspending_dod_rd_fy2019.jsonl.gz": 44337,
    "usaspending_dod_rd_fy2026.jsonl.gz": 33089,
}
# Boundary-delimited acronyms avoid ROE matching "aerospace" and RAI matching "training".
# Spelling separators are normalized below; longer variants remain explicit here.
TERMS = {
    "A": ["ETHIC*", "MORAL*", "LAW OF WAR", "LAWS OF WAR", "LOAC", "IHL", "RULES OF ENGAGEMENT", "ROE", "PROPORTIONALITY", "DISTINCTION", "NON-COMBATANT", "NONCOMBATANT", "BYSTANDER", "CIVILIAN HARM", "COLLATERAL DAMAGE", "UNINTENDED ENGAGEMENT", "NONMALEFICENCE", "DE-ESCALATION", "CALVIN", "ASIMOV", "RESPECT", "REBAR", "GEARS", "MAGNET", "CETLAWS", "TEELAWS", "RAIDER", "CODORD", "DONATELLO", "DEONTIC", "ETHICAL CONSTRUCTS", "ARMOR2025", "ARMOR 2025"],
    "B": ["FAIL-SAFE", "FAILSAFE", "ABORT", "HUMAN CONTROL", "HUMAN JUDGMENT", "HUMAN JUDGEMENT", "HUMAN-IN-THE-LOOP", "HUMAN-ON-THE-LOOP", "POSITIVE HUMAN", "HUMAN AUTHORIZATION", "HUMAN AUTHORISATION", "TARGET AUTHORIZATION", "BOUNDED AUTONOMY", "BOUNDED ENGAGEMENT", "ENGAGEMENT ENVELOPE", "REACHABILITY ENVELOPE", "VETO", "SELF-DESTRUCT", "QUASISTATICS"],
    "C": ["RUN-TIME ASSURANCE", "RUNTIME ASSURANCE", "RTA", "ASSURED AUTONOMY", "TRUSTED AUTONOMY", "TRUST-AWARE", "SAFE AUTONOMY", "SAFETY CRITICAL", "FORMAL VERIFICATION", "FORMAL METHODS", "GUARDRAIL*", "TEVV", "TEST AND EVALUATION", "V&V", "IV&V", "CERTIFICATION", "EXPLAINABLE AI", "XAI", "CALIBRAT*", "UNCERTAINTY QUANTIFICATION", "RED TEAM*", "SIMPLEX", "SAFE REINFORCEMENT", "ADVERSARIAL ROBUSTNESS", "DATA POISONING", "SENSOR FUSION CONFIDENCE", "TALON", "ANSR", "TIAMAT", "GARD", "COMPETENCE-AWARE", "COMPETENCY-AWARE", "TRUSTWORTHY AI", "TRUSTED AI", "LINCHPIN", "DCIST", "STRONG"],
    "D": ["RESPONSIBLE AI", "RAI", "ELSI", "3000.09", "SHIELD", "SHIELDS", "CDAO", "CHIEF DIGITAL AND AI", "CHIEF DIGITAL AND ARTIFICIAL INTELLIGENCE", "DOT&E", "DIRECTOR OPERATIONAL TEST", "TEST RESOURCE MANAGEMENT CENTER", "TRMC", "TETRAS", "JATIC", "CHMR", "CIVILIAN PROTECTION CENTER", "SENIOR OFFICIAL REVIEW", "NSPM-11", "DEFENSE TEST RESOURCE MGMT CENTER", "CHIEF DIGITAL & AI", "OPERATIONAL TEST AND EVALUATION", "OPERATIONAL TEST CMD"],
}
ANCHORS = ["CHIEF DIGITAL & AI", "OPERATIONAL TEST AND EVALUATION", "OPERATIONAL TEST CMD", "DEFENSE TEST RESOURCE MGMT CENTER", "CODORD", "DONATELLO", "DEONTIC", "ETHICAL CONSTRUCTS", "ARMOR2025", "ARMOR 2025", "CDAO", "CHIEF DIGITAL AND AI", "CHIEF DIGITAL AND ARTIFICIAL INTELLIGENCE", "DOT&E", "DIRECTOR OPERATIONAL TEST", "TRMC", "TEST RESOURCE MANAGEMENT CENTER", "TETRAS", "JATIC", "ASIMOV", "CALVIN", "CETLAWS", "TEELAWS", "ANSR", "TIAMAT", "ASSURED AUTONOMY", "GUARANTEEING AI ROBUSTNESS", "COMPETENCE-AWARE MACHINE LEARNING", "COMPETENCY-AWARE MACHINE LEARNING", "LINCHPIN", "DCIST", "AFRL SAFE AUTONOMY", "SHIELD", "SHIELDS"]
DOMAIN = ["ARTIFICIAL INTELLIGENCE", "AI", "AI/ML", "MACHINE LEARNING", "NEURAL", "AUTONOM*", "ROBOT*", "TARGET*", "WEAPON*", "MUNITION*", "UNMANNED", "UNCREWED", "UAV", "UAS", "USV", "UUV", "UGV", "SWARM*", "LETHAL*", "HUMAN MACHINE", "DECISION SUPPORT", "KILL CHAIN"]
PERFORMERS = {
    "Kitware": r"\bKITWARE\b", "RTX/Raytheon": r"\b(?:RTX|RAYTHEON)\b", "STR": r"\bSYSTEMS\s*(?:&|AND)?\s*TECHNOLOGY\s+RESEARCH\b",
    "CoVar": r"\bCOVAR\b", "UNSW": r"\b(?:UNIVERSITY OF NEW SOUTH WALES|UNSW)\b", "Saab": r"\bSAAB\b", "Lockheed Martin": r"\bLOCKHEED\s+MARTIN\b",
    "MIT": r"\b(?:MASSACHUSETTS INSTITUTE OF TECHNOLOGY|MIT LINCOLN)\b", "Georgia Tech": r"\bGEORGIA (?:INSTITUTE OF TECHNOLOGY|TECH)\b",
    "Penn State": r"\b(?:PENNSYLVANIA STATE|PENN STATE)\b", "Virginia Tech": r"\b(?:VIRGINIA POLYTECHNIC|VIRGINIA TECH)\b",
    "SIFT": r"\b(?:SMART INFORMATION FLOW TECHNOLOG|SIFT)\w*\b", "Duality AI": r"\bDUALITY\b", "Charles River Analytics": r"\bCHARLES RIVER ANALYTICS\b", "ASU": r"\b(?:ARIZONA STATE|ASU RESEARCH ENTERPRISE)\b",
}
PRX = {k: re.compile(v, re.I) for k, v in PERFORMERS.items()}


def normal(s):
    return re.sub(r"[\s\-‐‑–—_]+", " ", str(s).upper())


def pattern(term):
    t = normal(term)
    return re.compile(r"(?<![A-Z0-9])" + re.escape(t).replace(r"\*", r"[A-Z0-9]*") + r"(?![A-Z0-9])")


RX = {k: [(t, pattern(t)) for t in v] for k, v in TERMS.items()}
DRX = [(t, pattern(t)) for t in DOMAIN]
ARX = [(t, pattern(t)) for t in ANCHORS]
GATE = re.compile(r"(?<![A-Z0-9])(?:" + "|".join(re.escape(normal(t)).replace(r"\*", r"[A-Z0-9]*") for t in DOMAIN + ANCHORS) + r")(?![A-Z0-9])")


def classify(text):
    t = normal(text)
    if not GATE.search(t):
        return False, [], {k: [] for k in RX}, [], []
    domain = [term for term, rx in DRX if rx.search(t)]
    anchors = [term for term, rx in ARX if rx.search(t)]
    if not domain and not anchors:
        return False, [], {k: [] for k in RX}, [], []
    hits = {k: [term for term, rx in v if rx.search(t)] for k, v in RX.items()}
    selected = bool(anchors or (domain and any(hits.values())))
    tags = [k for k in "ABCD" if hits[k]] if selected else []
    return selected, tags, hits, domain, anchors


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def jdump(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=True)


def obj(v):
    if isinstance(v, dict):
        return v
    try:
        x = json.loads(v or "{}")
        return x if isinstance(x, dict) else {}
    except (ValueError, TypeError):
        return {}


def flatten(v, prefix=""):
    if isinstance(v, dict):
        for k, x in v.items():
            yield from flatten(x, (prefix + "." if prefix else "") + str(k))
    elif isinstance(v, list):
        for i, x in enumerate(v):
            yield from flatten(x, prefix + "." + str(i))
    else:
        yield prefix, "" if v is None else str(v)


def cents(v):
    if v in (None, ""):
        return None
    try:
        n = Decimal(str(v).replace(",", "").replace("$", "")) * 100
        return int(n.quantize(Decimal("1"))) if n.is_finite() else None
    except (InvalidOperation, ValueError, TypeError):
        return None


def is_end_date_field(field):
    return bool(re.search(r"(?:end|completion|expiration).*date|date.*(?:end|completion|expiration)", field, re.I))


def award_id(key, ids):
    explicit = ids.get("award_id_piid") or ids.get("award_id_fain") or ids.get("Contract") or ids.get("Contract Number")
    if explicit:
        return str(explicit), "explicit_source_identifier"
    if key.startswith(("CONT_AWD_", "ASST_NON_")):
        parts = key.split("_")
        return parts[2], "parsed_generated_key_unvalidated"
    return key, "source_key_only"


def strings(r, ids):
    full = dict(r)
    for key, value in list(full.items()):
        if key.endswith("_json") and isinstance(value, str):
            try:
                full[key] = json.loads(value)
            except ValueError:
                pass
    fields = list(flatten(full))
    # Preserve every textual description field, without implicit length limits.
    desc = [v for k, v in fields if re.search(r"(?:^|\.)(?:title|text(?:_.*)?|.*_text|abstract|description|evidence_excerpt|purpose|project_name|summary|content|body)$", k, re.I) and v]
    psc = sorted(set(v for k, v in fields if re.search(r"product.*service.*code|(?:^|\.)psc(?:_code)?$", k, re.I) and v))
    naics = sorted(set(v for k, v in fields if "naics" in k.lower() and v))
    dates = {k: v for k, v in fields if v and is_end_date_field(k)}
    # Search every non-provenance scalar field as well as recognized prose. This
    # covers table cells, nested Grants.gov source fields and budget dimensions.
    text = " | ".join(v for k, v in fields if not re.search(r"source_url|raw_locator|source_snapshot_sha256|record_sha256|document_id|retrieved_at", k, re.I))
    return text, list(dict.fromkeys(desc)), psc, naics, dates


def create_db(path):
    if path.exists():
        raise RuntimeError(f"Refusing populated workspace DB {path}; choose a fresh --work-dir")
    c = sqlite3.connect(path)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA synchronous=NORMAL")
    c.executescript("""
    CREATE TABLE financial(tx TEXT PRIMARY KEY,award TEXT,entity TEXT,entity_key TEXT,action_date TEXT,fy INTEGER,cents INTEGER,source_file TEXT,source_row INTEGER,source_url TEXT);
    CREATE INDEX fin_award ON financial(award);
    CREATE TABLE observations(id INTEGER PRIMARY KEY,tx TEXT,award TEXT,piid TEXT,identifier_status TEXT,entity TEXT,entity_key TEXT,action_date TEXT,fy INTEGER,descriptions TEXT,psc TEXT,naics TEXT,dates TEXT,source_file TEXT,source_row INTEGER,source_url TEXT,document_id TEXT,selected INTEGER,tags TEXT,hits TEXT,domain TEXT,anchors TEXT,performers TEXT);
    CREATE INDEX obs_award ON observations(award);
    CREATE INDEX obs_tx ON observations(tx);
    CREATE INDEX obs_selected ON observations(selected);
    """)
    return c


def extract_archives(paths, root, audit):
    inputs = []
    for archive in paths:
        h = sha(archive)
        expected = EXPECTED.get(archive.name)
        audit["archives"].append({"filename": archive.name, "bytes": archive.stat().st_size, "sha256": h, "expected_sha256": expected, "verified": h == expected})
        if expected is None or h != expected:
            raise RuntimeError(f"Archive hash/name verification failed: {archive.name}")
        dest = root / archive.name.removesuffix(".tar.gz")
        dest.mkdir(parents=True, exist_ok=True)
        with tarfile.open(archive, "r:gz") as tar:
            for member in tar:
                rec = {"archive": archive.name, "name": member.name, "bytes": member.size, "kind": "file" if member.isfile() else "directory" if member.isdir() else "unsupported"}
                audit["archive_members"].append(rec)
                target = dest / member.name
                if member.name.startswith("/") or ".." in Path(member.name).parts or not target.resolve().is_relative_to(dest.resolve()):
                    raise RuntimeError(f"Unsafe archive member {member.name}")
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                elif member.isfile():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with tar.extractfile(member) as src, target.open("wb") as out:
                        while b := src.read(1024 * 1024):
                            out.write(b)
                    inputs.append(target)
                else:
                    audit["failures"].append({"target": member.name, "reason": "symlink/special archive member excluded"})
    return inputs


def ingest(c, files, audit):
    seen = {}
    for path in sorted(files):
        rec = {"name": path.name, "path": str(path), "bytes": path.stat().st_size, "sha256": sha(path), "physical_rows": 0, "parsed_rows": 0, "selected_rows": 0, "errors": [], "status": "pending"}
        audit["files"].append(rec)
        if rec["sha256"] in seen:
            rec.update(status="duplicate_bytes_accounted_not_rescanned", duplicate_of=seen[rec["sha256"]])
            continue
        seen[rec["sha256"]] = str(path)
        if not path.name.endswith((".jsonl", ".jsonl.gz", ".ndjson", ".ndjson.gz")):
            rec["status"] = "non_jsonl_inventory_only"
            continue
        is_fin = path.name == "financial_actions.jsonl.gz" or path.name == "financial_actions.jsonl"
        rec["role"] = "financial_actions" if is_fin else "descriptive_or_context"
        op = gzip.open if path.name.endswith(".gz") else open
        try:
            with op(path, "rt", encoding="utf-8") as f:
                for n, line in enumerate(f, 1):
                    rec["physical_rows"] = n
                    try:
                        r = json.loads(line)
                        if not isinstance(r, dict):
                            raise ValueError("JSONL row is not an object")
                        rec["parsed_rows"] += 1
                        key = str(r.get("award_key") or "")
                        tx = str(r.get("transaction_key") or "")
                        name = str(r.get("entity_name") or "")
                        date = str(r.get("action_date") or "")
                        try:
                            fy = int(r.get("fiscal_year") or 0) or None
                        except (ValueError, TypeError):
                            fy = None
                        if is_fin:
                            amount = cents(r.get("action_obligation_usd"))
                            if not tx or not key:
                                raise ValueError("Financial row lacks exact transaction/award key")
                            existing = c.execute("SELECT award,action_date,cents FROM financial WHERE tx=?", (tx,)).fetchone()
                            if existing:
                                rec["duplicate_financial_transactions"] = rec.get("duplicate_financial_transactions", 0) + 1
                                if tuple(existing) != (key, date, amount):
                                    raise ValueError("Conflicting duplicate financial transaction")
                            else:
                                c.execute("INSERT INTO financial VALUES(?,?,?,?,?,?,?,?,?,?)", (tx, key, name, str(r.get("entity_key") or ""), date, fy, amount, str(path), n, str(r.get("source_url") or "")))
                            if amount is None:
                                rec["missing_or_invalid_financial_amounts"] = rec.get("missing_or_invalid_financial_amounts", 0) + 1
                        else:
                            ids = obj(r.get("identifiers_json"))
                            text, descriptions, psc, naics, dates = strings(r, ids)
                            selected, tags, hits, domain, anchors = classify(text)
                            piid, id_status = award_id(key, ids)
                            if not key:
                                # These are source document observations, not invented contracts.
                                key = "SOURCE_DOCUMENT:" + str(r.get("document_id") or rec["sha256"] + ":" + str(n))
                            performers = [label for label, rx in PRX.items() if rx.search(name)]
                            c.execute("INSERT INTO observations(tx,award,piid,identifier_status,entity,entity_key,action_date,fy,descriptions,psc,naics,dates,source_file,source_row,source_url,document_id,selected,tags,hits,domain,anchors,performers) VALUES(" + ",".join("?" * 22) + ")", (tx, key, piid, id_status, name, str(r.get("entity_key") or ""), date, fy, jdump(descriptions), jdump(psc), jdump(naics), jdump(dates), str(path), n, str(r.get("source_url") or ""), str(r.get("document_id") or ""), int(selected), jdump(tags), jdump(hits), jdump(domain), jdump(anchors), jdump(performers)))
                            rec["selected_rows"] += int(selected)
                        if n % 10000 == 0:
                            c.commit()
                        if n % 100000 == 0:
                            print(path.name, n, flush=True)
                    except (ValueError, TypeError, sqlite3.Error) as e:
                        rec["errors"].append({"row": n, "error": str(e)})
            rec["status"] = "full_stream_crc_read_passed" if path.name.endswith(".gz") else "full_stream_read_passed"
        except (OSError, EOFError, UnicodeError) as e:
            rec["status"] = "retrieval_or_stream_failure"
            rec["errors"].append({"row": rec["physical_rows"], "error": str(e)})
        c.commit()
        print(path.name, rec["physical_rows"], rec["selected_rows"], rec["status"], flush=True)


def money_summary(c, key):
    rows = c.execute("SELECT action_date,fy,cents FROM financial WHERE award=?", (key,)).fetchall()
    def total(predicate):
        vals = [v for date, fy, v in rows if predicate(date, fy) and v is not None]
        return sum(vals) if vals else None
    return {"financial_transaction_count": len(rows), "obligation_cents_fy2019_2026": total(lambda d, y: y is not None and 2019 <= y <= 2026), "obligation_cents_fy2024_2026": total(lambda d, y: y is not None and 2024 <= y <= 2026), "obligation_cents_cy2024_2026": total(lambda d, y: "2024-01-01" <= d <= "2026-10-25"), "money_status": "net_within_acquired_action_corpus_and_window_not_complete_award_funding" if rows else "no_exact_financial_award_key_match_not_zero", "money_scope_limitation": "Acquisition filters can omit older positive, negative or zero actions. These corpus nets are not complete award funding or guaranteed lower bounds.", "financial_first_action": min((r[0] for r in rows), default=""), "financial_latest_action": max((r[0] for r in rows), default=""), "invalid_financial_amount_count": sum(r[2] is None for r in rows)}


def aggregate(c, key):
    cols = [r[1] for r in c.execute("PRAGMA table_info(observations)")]
    obs = [dict(zip(cols, r)) for r in c.execute("SELECT * FROM observations WHERE award=?", (key,))]
    tags = set()
    hits = {k: set() for k in "ABCD"}
    descriptions, names, ids, urls, psc, naics, dates, refs, domains, anchors = set(), set(), set(), set(), set(), set(), set(), [], set(), set()
    roles = set()
    for r in obs:
        tags.update(json.loads(r["tags"]))
        if r["selected"]:
            for k, v in json.loads(r["hits"]).items():
                hits[k].update(v)
        descriptions.update(json.loads(r["descriptions"]))
        names.add(r["entity"])
        role = "reported_first_tier_subawardee_prime_award_key" if "_subawards" in r["source_file"] else "SBIR_reported_recipient" if Path(r["source_file"]).name.startswith("sbir") else "source_prime_recipient_or_context_entity"
        if r["entity"]:
            roles.add((r["entity"], r["entity_key"], role))
        ids.add(r["piid"])
        urls.add(r["source_url"])
        psc.update(json.loads(r["psc"]))
        naics.update(json.loads(r["naics"]))
        for field, value in json.loads(r["dates"]).items():
            dates.add((field, value))
        domains.update(json.loads(r["domain"]))
        anchors.update(json.loads(r["anchors"]))
        refs.append({"file": Path(r["source_file"]).name, "row": r["source_row"], "tx": r["tx"], "document_id": r["document_id"]})
    primary = next((k for k in "ABCD" if k in tags), "")
    institutional_sources = []
    if c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='institutional_hits'").fetchone():
        institutional_sources = [json.loads(x[0]) for x in c.execute("SELECT evidence_json FROM institutional_hits WHERE award=?", (key,))]
        if institutional_sources:
            tags.add("D")
            hits["D"].update(x["anchor"] for x in institutional_sources)
            anchors.update(x["anchor"] for x in institutional_sources)
            primary = next((k for k in "ABCD" if k in tags), "")
    auxiliary_sources = []
    if c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='auxiliary_hits'").fetchone():
        auxiliary_sources = [json.loads(x[0]) for x in c.execute("SELECT evidence_json FROM auxiliary_hits WHERE award=?", (key,))]
        for source in auxiliary_sources:
            tags.update(source.get("categories_preliminary", []))
            for k, v in source.get("term_matches", {}).items():
                hits[k].update(v)
            anchors.update(source.get("institutional_anchor_matches", []))
            domains.update(source.get("domain_matches", []))
            psc.update(source.get("psc", []))
            naics.update(source.get("naics", []))
            if source.get("source_url"):
                urls.add(source["source_url"])
        primary = next((k for k in "ABCD" if k in tags), "")
    public_descriptions = []
    description_hashes = []
    for original in sorted(descriptions - {""}):
        public, emails = re.subn(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", "[contact email omitted]", original, flags=re.I)
        public, phones = re.subn(r"(?<!\d)(?:\+1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]\d{3}[-.\s]\d{4}(?!\d)", "[contact phone omitted]", public)
        public_descriptions.append(public)
        description_hashes.append({"original_sha256": hashlib.sha256(original.encode()).hexdigest(), "published_sha256": hashlib.sha256(public.encode()).hexdigest(), "contact_emails_omitted": emails, "contact_phones_omitted": phones})
    auxiliary_refs = [{"source_file": s["source_file"], "source_sha256": s["source_sha256"], "source_row": s["source_row"], "matching_field_names": s.get("matching_field_names", []), "scope_warning": s.get("scope_warning", ""), "complete_metadata_register": "evidence/auxiliary-candidates.jsonl"} for s in auxiliary_sources]
    return {"award_key": key, "award_ids": sorted(ids - {""}), "entity_names": sorted(names - {""}), "recipient_roles": [{"entity_name": name, "entity_key": ek, "role": role} for name, ek, role in sorted(roles)], "primary_category_preliminary": primary, "secondary_categories_preliminary": sorted(tags - {primary}), "all_categories_preliminary": sorted(tags), "review_status": "machine_screen_requires_human_scope_and_currentness_review", "full_descriptions": public_descriptions, "description_hashes_and_contact_redactions_same_order": description_hashes, "term_matches": {k: sorted(v) for k, v in hits.items()}, "domain_matches": sorted(domains), "institutional_anchor_matches": sorted(anchors), "institutional_anchor_source_observations": institutional_sources, "auxiliary_source_observations": auxiliary_refs, "auxiliary_funding_goals_scope_warning": any(any("funding_opportunity_goals_text" in field for field in s.get("matching_field_names", [])) for s in auxiliary_sources), "psc": sorted(psc), "naics": sorted(naics), "end_date_source_fields": [{"field": k, "value": v} for k, v in sorted(dates)], "end_date_status": "source_fields_retained_unreconciled" if dates else "not_present_in_accessible_normalized_row_fields", "source_urls": sorted(urls - {""}), "source_observation_count": len(obs), "source_refs": refs, "record_kind": "source_document_or_program" if key.startswith("SOURCE_DOCUMENT:") else "source_award_key", **money_summary(c, key)}


def write_csv(path, rows):
    if not rows:
        path.write_text("award_key,review_status\n", encoding="utf-8")
        return
    fields = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: jdump(v) if isinstance(v, (list, dict)) else v for k, v in row.items()})


def auxiliary_sweep(root, package, work):
    """Check semantic mirrors and screen unique auxiliary fields without money sums."""
    import pyarrow
    import pyarrow.parquet as pq
    work.mkdir(parents=True, exist_ok=True)
    package.joinpath("audit").mkdir(parents=True, exist_ok=True)
    package.joinpath("evidence").mkdir(parents=True, exist_ok=True)
    audit = {"started_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "runtime": {"python": sys.version, "pyarrow": pyarrow.__version__}, "lexicon": TERMS, "domain_lexicon": DOMAIN, "institutional_anchors": ANCHORS, "files": [], "failures": [], "money_rule": "No auxiliary monetary fields enter obligation sums; canonical exact-key financial_actions remain sole accounting source.", "public_output_rule": "Only identifiers, match terms, matching field names, source hash/row, corporate performer names and performance dates are published; full auxiliary candidate rows stay private.", "status": "started"}
    dc = sqlite3.connect(work / "auxiliary-dates.sqlite")
    dc.execute("CREATE TABLE IF NOT EXISTS dates(award TEXT,action_date TEXT,source_file TEXT,source_row INTEGER,dates_json TEXT)")
    dc.execute("CREATE INDEX IF NOT EXISTS date_award ON dates(award)")
    public_path = package / "evidence/auxiliary-candidates.jsonl"
    private_path = work / "auxiliary-full-candidates.jsonl"
    with public_path.open("w", encoding="utf-8") as out, private_path.open("w", encoding="utf-8") as private:
        def process(row, f, n, info):
            if not isinstance(row, dict):
                row = {"value": row}
            text, descriptions, psc, naics, dates = strings(row, obj(row.get("identifiers_json")))
            selected, tags, hits, domain, anchors = classify(text)
            # Raw transaction tables expose end dates omitted by normalized JSONL.
            ak = str(row.get("contract_award_unique_key") or row.get("assistance_award_unique_key") or row.get("prime_award_unique_key") or row.get("award_key") or "")
            action = str(row.get("action_date") or row.get("subaward_action_date") or row.get("prime_award_latest_action_date") or "")
            if dates and ak:
                dc.execute("INSERT INTO dates VALUES(?,?,?,?,?)", (ak, action, str(f), n, jdump(dates)))
            # Actor names are organization matches, not personal contact information.
            named_fields = {k: v for k, v in flatten(row) if re.search(r"entity_name|recipient_name|subawardee_name|prime_awardee_name", k, re.I)}
            performers = sorted({name for value in named_fields.values() for name, rx in PRX.items() if rx.search(value)})
            trace = bool(performers and "2025-01-01" <= action <= "2026-10-25")
            if not selected and not trace:
                return
            matching_fields = []
            matched_patterns = [rx for k, values in RX.items() for term, rx in values if term in hits[k]]
            for field, value in flatten(row):
                nv = normal(value)
                if any(rx.search(nv) for rx in matched_patterns):
                    matching_fields.append(field)
            identifiers = {k: str(v) for k, v in row.items() if v and re.search(r"(?:award.*(?:key|piid|fain)|transaction_unique_key|contract_string|document_id|subaward_number|inst_id)$", k, re.I)}
            summary = {"source_file": f.name, "source_sha256": info["sha256"], "source_row": n, "identifiers": identifiers, "categories_preliminary": tags, "term_matches": hits, "domain_matches": domain, "institutional_anchor_matches": anchors, "matching_field_names": matching_fields, "psc": psc, "naics": naics, "source_action_date": action, "end_date_source_fields": dates, "performer_matches": performers, "performer_temporal_match": trace, "status": "auxiliary_machine_lead_not_verified_safeguard_or_continuation", "source_url": str(row.get("source_url") or row.get("usaspending_permalink") or "")}
            out.write(jdump(summary) + "\n")
            private.write(jdump({"source_file": str(f), "source_row": n, "row": row}) + "\n")
            info["selected_rows"] += 1
        for f in sorted(root.rglob("*")):
            if not f.is_file() or f.suffix not in (".parquet", ".json", ".txt"):
                continue
            info = {"file": str(f), "name": f.name, "bytes": f.stat().st_size, "sha256": sha(f), "rows": 0, "selected_rows": 0, "status": "started"}
            audit["files"].append(info)
            try:
                if f.suffix == ".parquet":
                    pf = pq.ParquetFile(f)
                    info["metadata_rows"] = pf.metadata.num_rows
                    info["columns"] = pf.schema_arrow.names
                    typed_fields = [field.name for field in pf.schema_arrow if pyarrow.types.is_date(field.type) or pyarrow.types.is_timestamp(field.type) or pyarrow.types.is_decimal(field.type)]
                    if typed_fields:
                        info["lossless_JSON_scalar_conversion"] = {name: str(pf.schema_arrow.field(name).type) for name in typed_fields}
                    mirror = f.with_suffix(".jsonl.gz")
                    if not mirror.exists():
                        mirror = f.with_suffix(".jsonl")
                    g = (gzip.open(mirror, "rt", encoding="utf-8") if mirror.suffix == ".gz" else mirror.open(encoding="utf-8")) if mirror.exists() else None
                    mismatches = 0
                    equal = 0
                    try:
                        for batch in pf.iter_batches(batch_size=1000):
                            for row in batch.to_pylist():
                                for name in typed_fields:
                                    value = row[name]
                                    if value is not None:
                                        row[name] = value.isoformat() if isinstance(value, (dt.date, dt.datetime)) else str(value)
                                info["rows"] += 1
                                mirrored = False
                                if g is not None:
                                    line = g.readline()
                                    mirrored = bool(line and json.loads(line) == row)
                                    equal += int(mirrored)
                                    mismatches += int(not mirrored)
                                if not mirrored:
                                    process(row, f, info["rows"], info)
                            dc.commit()
                            if info["rows"] % 100000 == 0:
                                print("aux", f.name, info["rows"], flush=True)
                        extra = sum(1 for _ in g) if g is not None else 0
                    finally:
                        if g is not None:
                            g.close()
                    if mirror.exists():
                        info.update(mirror=str(mirror), mirror_sha256=sha(mirror), row_by_row_semantic_equal=equal, row_by_row_semantic_mismatches=mismatches, extra_jsonl_rows=extra)
                        info["status"] = "semantic_row_equivalent_to_screened_JSONL" if not mismatches and not extra else "mismatching_parquet_rows_independently_screened"
                    else:
                        info["status"] = "all_parquet_rows_independently_screened"
                elif f.suffix == ".json":
                    value = json.loads(f.read_text(encoding="utf-8"))
                    if isinstance(value, dict) and isinstance(value.get("pages"), dict):
                        rows = [{"page": key, "text": text, "raw_file": value.get("raw_file")} for key, text in value["pages"].items()]
                    else:
                        rows = value if isinstance(value, list) else [value]
                    for n, row in enumerate(rows, 1):
                        process(row, f, n, info)
                        info["rows"] = n
                    info["status"] = "all_JSON_records_or_OCR_pages_screened"
                else:
                    for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                        process({"text": line}, f, n, info)
                        info["rows"] = n
                    info["status"] = "all_text_lines_screened"
            except Exception as e:
                info["status"] = "failed_or_partial"
                info["error"] = str(e)
                audit["failures"].append({"file": str(f), "error": str(e)})
            dc.commit()
            print("aux", f.name, info["rows"], info["status"], flush=True)
    dc.close()
    audit["status"] = "completed_with_gaps" if audit["failures"] else "completed"
    audit["finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    audit["total_auxiliary_rows_accounted"] = sum(x["rows"] for x in audit["files"])
    audit["semantic_mirror_rows_not_double_counted"] = sum(x.get("row_by_row_semantic_equal", 0) for x in audit["files"])
    audit["public_candidate_observations_not_distinct_awards"] = sum(x["selected_rows"] for x in audit["files"])
    (package / "audit/screen-auxiliary-accounting.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(jdump({k: v for k, v in audit.items() if k != "files"}))
    return int(bool(audit["failures"]))


def enrich_end_dates(package, database):
    """Reconcile exact-key candidate end-date observations; never update money."""
    c = sqlite3.connect("file:" + str(database.resolve()) + "?mode=ro", uri=True)
    p = package / "evidence/brakes-candidate-register.json"
    rows = json.loads(p.read_text(encoding="utf-8"))
    counts = collections.Counter()
    for row in rows:
        observations = c.execute("SELECT action_date,source_file,source_row,dates_json FROM dates WHERE award=? ORDER BY action_date,source_file,source_row", (row["award_key"],)).fetchall()
        values = {}
        provenance = []
        for date, source_file, n, date_json in observations:
            dates = {k: v for k, v in json.loads(date_json).items() if is_end_date_field(k)}
            for field, value in dates.items():
                if field not in values or date >= values[field][0]:
                    values[field] = (date, value)
            provenance.append({"action_date": date, "source_file": Path(source_file).name, "source_row": n, "fields": dates})
        row["end_date_source_observations"] = provenance
        row["latest_end_date_fields_by_source_action_date"] = {field: {"source_action_date": date, "value": value} for field, (date, value) in sorted(values.items())}
        row["end_date_status"] = "exact_award_key_raw_source_fields_observed_latest_by_action_date_not_proof_of_work" if values else row["end_date_status"]
        counts["candidate_awards_with_raw_end_dates" if values else "candidate_records_without_raw_end_dates"] += 1
    p.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(package / "evidence/brakes-candidate-register.csv", rows)
    # Keep a CSV performer trace synchronized with exact-key date observations.
    trace = package / "evidence/asimov-performer-continuation-check.csv"
    if trace.exists():
        with trace.open(encoding="utf-8", newline="") as f:
            tr = list(csv.DictReader(f))
        for row in tr:
            obs = c.execute("SELECT action_date,source_file,source_row,dates_json FROM dates WHERE award=? ORDER BY action_date,source_file,source_row", (row["award_key"],)).fetchall()
            row["raw_source_end_date_observations"] = [{"action_date": d, "source_file": Path(s).name, "source_row": n, "fields": {k: v for k, v in json.loads(j).items() if is_end_date_field(k)}} for d, s, n, j in obs]
        write_csv(trace, tr)
    c.close()
    note = {"status": "completed", "counts": dict(counts), "join": "Complete exact award key only, never PIID/name matching", "money_changed": False, "limitation": "All date observations retained; latest source action is not proof of active technical work, option exercise or legal restraint. Same-date conflicting fields remain visible in source observations.", "retrieved_utc": dt.datetime.now(dt.timezone.utc).isoformat()}
    (package / "audit/screen-end-date-enrichment.json").write_text(json.dumps(note, indent=2) + "\n", encoding="utf-8")
    print(jdump(note))
    return 0


def merge_auxiliary_parts(parts, package, work):
    """Merge disjoint local auxiliary partitions with coverage/hash conservation."""
    work.mkdir(parents=True, exist_ok=True)
    package.joinpath("evidence").mkdir(parents=True, exist_ok=True)
    package.joinpath("audit").mkdir(parents=True, exist_ok=True)
    db = work / "auxiliary-dates.sqlite"
    if db.exists():
        raise RuntimeError("Refusing existing merged auxiliary database; choose fresh --work-dir")
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE dates(award TEXT,action_date TEXT,source_file TEXT,source_row INTEGER,dates_json TEXT)")
    merged = {"status": "completed", "partition_runs": [], "files": [], "failures": [], "runtime": {"python": sys.version}, "money_rule": "Auxiliary fields never added to canonical financial_actions money", "public_output_rule": "Identifiers, terms, matching field names and dates only; full auxiliary rows remain private in partition workspaces", "local_parallelism": "Independent archive partitions; no API calls or spending"}
    seen = set()
    line_count = 0
    with (package / "evidence/auxiliary-candidates.jsonl").open("w", encoding="utf-8") as out:
        for i, (part, partwork) in enumerate(parts):
            ap = part / "audit/screen-auxiliary-accounting.json"
            audit = json.loads(ap.read_text(encoding="utf-8"))
            if audit["status"] != "completed":
                raise RuntimeError(f"Incomplete auxiliary partition {part}")
            for f in audit["files"]:
                if f["file"] in seen:
                    raise RuntimeError(f"Overlapping partition input {f['file']}")
                seen.add(f["file"])
                merged["files"].append(f)
            local_lines = 0
            cp = part / "evidence/auxiliary-candidates.jsonl"
            with cp.open(encoding="utf-8") as src:
                for line in src:
                    summary = json.loads(line)
                    summary["end_date_source_fields"] = {k: v for k, v in summary.get("end_date_source_fields", {}).items() if is_end_date_field(k)}
                    out.write(jdump(summary) + "\n")
                    local_lines += 1
            if local_lines != audit["public_candidate_observations_not_distinct_awards"]:
                raise RuntimeError(f"Candidate row conservation failed {part}")
            line_count += local_lines
            c.execute("ATTACH DATABASE ? AS partdb", (str(partwork / "auxiliary-dates.sqlite"),))
            before = c.execute("SELECT COUNT(*) FROM dates").fetchone()[0]
            source_count = c.execute("SELECT COUNT(*) FROM partdb.dates").fetchone()[0]
            c.execute("INSERT INTO dates SELECT * FROM partdb.dates")
            c.commit()
            after = c.execute("SELECT COUNT(*) FROM dates").fetchone()[0]
            if after - before != source_count:
                raise RuntimeError("Date observation conservation failed")
            c.execute("DETACH DATABASE partdb")
            merged["partition_runs"].append({"partition": part.name, "audit_sha256": sha(ap), "candidate_file_sha256": sha(cp), "candidate_observations": local_lines, "date_observations": source_count, "started_utc": audit.get("started_utc"), "finished_utc": audit.get("finished_utc"), "runtime": audit.get("runtime")})
    c.execute("CREATE INDEX date_award ON dates(award)")
    c.commit()
    merged["date_observations_not_distinct_awards"] = c.execute("SELECT COUNT(*) FROM dates").fetchone()[0]
    c.close()
    merged["total_auxiliary_rows_accounted"] = sum(f["rows"] for f in merged["files"])
    merged["semantic_mirror_rows_not_double_counted"] = sum(f.get("row_by_row_semantic_equal", 0) for f in merged["files"])
    merged["public_candidate_observations_not_distinct_awards"] = line_count
    merged["finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    (package / "audit/screen-auxiliary-accounting.json").write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(jdump({k: v for k, v in merged.items() if k not in ("files", "partition_runs")}))
    return 0


def supplemental_editor_screen(package, database):
    """Fresh editor terms applied to every stored full description, preserving old hits."""
    c = sqlite3.connect(database)
    institution_path = package / "audit/screen-institution-supplement.json"
    if institution_path.exists():
        institution = json.loads(institution_path.read_text(encoding="utf-8"))
        prior_selected = {r[0] for r in c.execute("SELECT DISTINCT award FROM observations WHERE selected=1")}
        institutional_keys = {r["award_key"] for r in institution.get("office_matches", [])}
        institution["already_selected_by_original_text_screen"] = len(institutional_keys & prior_selected)
        institution["additional_award_keys_recovered_by_office_alias"] = len(institutional_keys - prior_selected)
        institution["missing_canonical_award_observations"] = sum(not c.execute("SELECT 1 FROM observations WHERE award=? LIMIT 1", (key,)).fetchone() for key in institutional_keys)
        institution_path.write_text(json.dumps(institution, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        c.execute("CREATE TABLE IF NOT EXISTS institutional_hits(award TEXT,evidence_json TEXT UNIQUE)")
        c.execute("CREATE INDEX IF NOT EXISTS institution_award ON institutional_hits(award)")
        for match in institution.get("office_matches", []):
            c.execute("INSERT OR IGNORE INTO institutional_hits VALUES(?,?)", (match["award_key"], jdump(match)))
    terms = ["CODORD", "DONATELLO", "DEONTIC", "ETHICAL CONSTRUCTS", "ARMOR2025", "ARMOR 2025"]
    predicates = " OR ".join("UPPER(descriptions) LIKE ?" for _ in terms)
    params = tuple("%" + t + "%" for t in terms)
    matches = c.execute("SELECT id,award,piid,entity,descriptions,tags,hits,domain,anchors FROM observations WHERE " + predicates, params).fetchall()
    register = []
    for oid, award, piid, entity, descriptions, old_tags, old_hits, old_domain, old_anchors in matches:
        selected, tags, hits, domain, anchors = classify(" | ".join([entity, *json.loads(descriptions)]))
        if not selected:
            continue
        tags = sorted(set(tags) | set(json.loads(old_tags)))
        prior_hits = json.loads(old_hits)
        hits = {k: sorted(set(v) | set(prior_hits.get(k, []))) for k, v in hits.items()}
        domain = sorted(set(domain) | set(json.loads(old_domain)))
        anchors = sorted(set(anchors) | set(json.loads(old_anchors)))
        c.execute("UPDATE observations SET selected=1,tags=?,hits=?,domain=?,anchors=? WHERE id=?", (jdump(tags), jdump(hits), jdump(domain), jdump(anchors), oid))
        register.append({"observation_id": oid, "award_key": award, "piid": piid, "entity": entity, "new_editor_term_matches": sorted(set(hits["A"]) & set(terms)), "previously_selected": bool(json.loads(old_tags)), "primary_category_preliminary": tags[0]})
    # Refresh named-organization aliases consistently for every source observation.
    c.execute("CREATE INDEX IF NOT EXISTS obs_entity ON observations(entity)")
    changed_entities = []
    for (entity,) in c.execute("SELECT DISTINCT entity FROM observations"):
        performers = [name for name, rx in PRX.items() if rx.search(entity)]
        prior = c.execute("SELECT performers FROM observations WHERE entity=? LIMIT 1", (entity,)).fetchone()
        if prior and set(json.loads(prior[0])) != set(performers):
            c.execute("UPDATE observations SET performers=? WHERE entity=?", (jdump(performers), entity))
            changed_entities.append({"entity": entity, "performers": performers})
    c.commit()
    refresh = {}
    export(c, package, refresh)
    c.close()
    audit = {"status": "completed", "terms": terms, "scope": "Every full description stored from every parsed canonical JSONL observation; broad new aliases applied as independent anchors. Earlier hits preserved.", "total_stored_description_observations": refresh["counts"]["descriptive_context_physical_observations"], "matching_observations": register, "performer_alias_entity_updates": changed_entities, "revised_counts": refresh, "editor_gap": "Initial requested lexicon did not contain CODORD/DONATELLO/deontic aliases. Fresh editor challenge prompted this additional full-description pass; do not misrepresent as part of initial lexicon.", "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat()}
    (package / "audit/screen-editor-supplement.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(jdump({"status": audit["status"], "matching_observations": len(register), "revised_counts": refresh}))
    return 0


def institution_supplement(root, package):
    """Fresh raw-office alias challenge and explicit assistance-goals field QA."""
    import pyarrow.parquet as pq
    aliases = ["DEFENSE TEST RESOURCE MGMT CENTER", "CHIEF DIGITAL & AI", "OPERATIONAL TEST AND EVALUATION", "OPERATIONAL TEST CMD"]
    value_alias_cache = {}
    audit = {"status": "completed", "aliases": aliases, "scope": "All raw transaction/subaward parquet source office/agency-name columns; independent anchors without AI-domain requirement", "office_matches": [], "files": [], "failures": [], "funding_opportunity_goals_field_QA": [], "initial_gap": "Initial institution lexicon omitted MGMT, CHIEF DIGITAL & AI punctuation, generic OPERATIONAL TEST AND EVALUATION office and Army OPERATIONAL TEST CMD forms; normalized JSONL also omitted these office fields. Fresh editor challenge and raw-office value inspection prompted follow-up. No additional monetary observations are added."}
    for f in sorted(root.rglob("*_source.parquet")):
        pf = pq.ParquetFile(f)
        cols = pf.schema_arrow.names
        offices = [k for k in cols if re.search(r"(?:office|agency).*name$", k, re.I)]
        goals = [k for k in cols if "funding_opportunity_goals_text" in k]
        if not offices and not goals:
            continue
        identifiers = [k for k in ("contract_award_unique_key", "assistance_award_unique_key", "prime_award_unique_key", "award_key", "action_date", "subaward_action_date", "prime_award_latest_action_date") if k in cols]
        info = {"file": f.name, "sha256": sha(f), "metadata_rows": pf.metadata.num_rows, "rows_checked": 0, "office_fields": offices, "goals_fields": goals, "office_matching_rows": 0, "office_field_appearances": 0}
        audit["files"].append(info)
        goal_values = {k: collections.Counter() for k in goals}
        try:
            for batch in pf.iter_batches(batch_size=5000, columns=list(dict.fromkeys(offices + goals + identifiers))):
                for row in batch.to_pylist():
                    info["rows_checked"] += 1
                    for k in goals:
                        value = row.get(k)
                        if value is not None and str(value).strip():
                            goal_values[k][str(value)] += 1
                    matches = collections.defaultdict(dict)
                    for k in offices:
                        value = row.get(k)
                        if not value:
                            continue
                        value = str(value)
                        if value not in value_alias_cache:
                            value_alias_cache[value] = [alias for alias in aliases if alias in normal(value)]
                        for alias in value_alias_cache[value]:
                            matches[alias][k] = value
                    if not matches:
                        continue
                    key = str(row.get("contract_award_unique_key") or row.get("assistance_award_unique_key") or row.get("prime_award_unique_key") or row.get("award_key") or "")
                    if not key:
                        raise ValueError("Matching institution office row has no exact award key")
                    info["office_matching_rows"] += 1
                    for alias, matched in matches.items():
                        info["office_field_appearances"] += len(matched)
                        audit["office_matches"].append({"award_key": key, "source_file": f.name, "source_sha256": info["sha256"], "source_row": info["rows_checked"], "action_date": str(row.get("action_date") or row.get("subaward_action_date") or row.get("prime_award_latest_action_date") or ""), "matched_fields": matched, "anchor": alias, "classification": "D_preliminary_institutional_award_not_verified_weapon_safeguard"})
        except Exception as e:
            audit["failures"].append({"file": f.name, "error": str(e)})
            audit["status"] = "completed_with_gaps"
        for k, values in goal_values.items():
            audit["funding_opportunity_goals_field_QA"].append({"file": f.name, "field": k, "metadata_rows": pf.metadata.num_rows, "rows_with_nonempty_field": sum(values.values()), "unique_nonempty_values": len(values), "all_values_private_not_published": True, "screen_coverage": "The full auxiliary sweep searches every raw-field value, including this field; QA here checks its denominator independently."})
    audit["matching_source_rows"] = len({(r["source_file"], r["source_row"]) for r in audit["office_matches"]})
    audit["matching_field_appearances"] = sum(len(x["matched_fields"]) for x in audit["office_matches"])
    audit["distinct_complete_award_keys"] = len({r["award_key"] for r in audit["office_matches"]})
    audit["per_alias"] = {alias: {"matching_source_rows": sum(r["anchor"] == alias for r in audit["office_matches"]), "matching_field_appearances": sum(len(r["matched_fields"]) for r in audit["office_matches"] if r["anchor"] == alias), "distinct_complete_award_keys": len({r["award_key"] for r in audit["office_matches"] if r["anchor"] == alias})} for alias in aliases}
    audit["finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    (package / "audit/screen-institution-supplement.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(jdump({k: v for k, v in audit.items() if k not in ("files", "office_matches")}))
    return int(bool(audit["failures"]))


def import_auxiliary_award_hits(package, database):
    """Unify exact-key auxiliary award leads without introducing financial rows."""
    c = sqlite3.connect(database)
    keys = {r[0] for r in c.execute("SELECT DISTINCT award FROM observations WHERE selected=1")}
    if c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='institutional_hits'").fetchone():
        keys.update(r[0] for r in c.execute("SELECT DISTINCT award FROM institutional_hits"))
    c.execute("CREATE TABLE IF NOT EXISTS auxiliary_hits(award TEXT,evidence_json TEXT UNIQUE)")
    c.execute("CREATE INDEX IF NOT EXISTS auxiliary_award ON auxiliary_hits(award)")
    counts = collections.Counter()
    imported_keys = set()
    with (package / "evidence/auxiliary-candidates.jsonl").open(encoding="utf-8") as f:
        for line in f:
            source = json.loads(line)
            counts["auxiliary_candidate_observations_read"] += 1
            if not source.get("categories_preliminary"):
                counts["performer_only_observations_retained_in_auxiliary_trace"] += 1
                continue
            ids = source.get("identifiers", {})
            key = next((str(ids[k]) for k in ("contract_award_unique_key", "assistance_award_unique_key", "prime_award_unique_key", "usaspending_award_key", "award_key") if ids.get(k)), "")
            if not key:
                counts["context_only_observations_without_award_key_remain_auxiliary"] += 1
                continue
            source["scope_warning"] = "Funding-opportunity goals describe the funding program and do not establish what this individual award actually tests" if any("funding_opportunity_goals_text" in k for k in source.get("matching_field_names", [])) else "Auxiliary machine term match requires individual award-scope and currentness review"
            c.execute("INSERT OR IGNORE INTO auxiliary_hits VALUES(?,?)", (key, jdump(source)))
            imported_keys.add(key)
            counts["award_key_observations_imported"] += 1
    c.commit()
    refresh = {}
    export(c, package, refresh)
    counts["distinct_auxiliary_award_keys"] = len(imported_keys)
    counts["already_present_candidate_award_keys"] = len(imported_keys & keys)
    counts["additional_award_keys_from_auxiliary_fields"] = len(imported_keys - keys)
    counts["exact_canonical_financial_award_keys"] = sum(bool(c.execute("SELECT 1 FROM financial WHERE award=? LIMIT 1", (k,)).fetchone()) for k in imported_keys)
    c.close()
    audit = {"status": "completed", "counts": dict(counts), "revised_register_counts": refresh, "money_rule": "No auxiliary amounts imported; totals still exact-key canonical financial_actions only, one candidate per exact source awardkey", "scope": "All auxiliary safeguard matches having actual award keys unified into main register; context-only and performer-only leads remain fully available in auxiliary-candidates.jsonl", "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat()}
    (package / "audit/screen-auxiliary-award-integration.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(jdump(audit))
    return 0


def validate_complete_coverage(package):
    main = json.loads((package / "audit/screen-accounting.json").read_text(encoding="utf-8"))
    auxiliary = json.loads((package / "audit/screen-auxiliary-accounting.json").read_text(encoding="utf-8"))
    all_files = {r["path"]: r for r in main["files"]}
    extra = {r["file"]: r for r in auxiliary["files"]}
    canonical = {k: r for k, r in all_files.items() if r["status"].startswith("full_stream")}
    missing = sorted(set(all_files) - set(canonical) - set(extra))
    unknown = sorted(set(extra) - set(all_files))
    hash_conflicts = sorted(k for k, r in extra.items() if k in all_files and r["sha256"] != all_files[k]["sha256"])
    overlap = sorted(set(canonical) & set(extra))
    passed = not (missing or unknown or hash_conflicts or overlap or main.get("missing_or_mismatched_expected_files") or auxiliary.get("failures"))
    result = {"status": "passed" if passed else "gaps_or_conflicts", "input_files_inventoried": len(all_files), "canonical_JSONL_files_fully_read": len(canonical), "auxiliary_parquet_JSON_TXT_files_fully_accounted": len(extra), "missing_files": missing, "unknown_files": unknown, "cross_format_hash_conflicts": hash_conflicts, "canonical_auxiliary_file_overlap": overlap, "canonical_physical_rows": sum(r["physical_rows"] for r in canonical.values()), "auxiliary_rows_including_mirror_representations": auxiliary["total_auxiliary_rows_accounted"], "total_source_representation_rows_NOT_distinct_awards": sum(r["physical_rows"] for r in canonical.values()) + auxiliary["total_auxiliary_rows_accounted"], "semantic_mirror_rows_not_counted_as_new_financial_actions": auxiliary["semantic_mirror_rows_not_double_counted"], "auxiliary_status_counts": dict(collections.Counter(r["status"] for r in extra.values())), "canonical_expected_missing_or_mismatched_files": main["missing_or_mismatched_expected_files"], "archive_hashes_verified": [{"filename": r["filename"], "sha256": r["sha256"], "verified": r["verified"]} for r in main["archives"]]}
    (package / "audit/screen-complete-input-coverage.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(jdump(result))
    return int(not passed)


def validate_financial_joins(root, database, package):
    """Check every descriptive transaction observation against canonical money."""
    c = sqlite3.connect("file:" + str(database.resolve()) + "?mode=ro", uri=True)
    counts = collections.Counter()
    conflicts = []
    files = []
    for f in sorted(root.rglob("usaspending*.jsonl.gz")):
        info = {"file": f.name, "sha256": sha(f), "physical_rows": 0, "transaction_rows_checked": 0}
        with gzip.open(f, "rt", encoding="utf-8") as g:
            for n, line in enumerate(g, 1):
                info["physical_rows"] = n
                row = json.loads(line)
                tx = row.get("transaction_key")
                if not tx:
                    counts["nontransaction_context_or_subaward_rows_not_added_to_prime_money"] += 1
                    continue
                counts["transaction_observations_checked"] += 1
                info["transaction_rows_checked"] += 1
                match = c.execute("SELECT award,cents,action_date,fy FROM financial WHERE tx=?", (tx,)).fetchone()
                if match is None:
                    counts["description_transactions_outside_financial"] += 1
                    conflicts.append({"file": f.name, "row": n, "transaction_key": tx, "problem": "no_canonical_financial_match"})
                    continue
                counts["exact_transaction_matches"] += 1
                money = obj(row.get("money_json"))
                value = money.get("federal_action_obligation")
                if value is None:
                    counts["description_missing_action_obligation"] += 1
                if cents(value) != match[1]:
                    counts["action_obligation_conflicts"] += 1
                    conflicts.append({"file": f.name, "row": n, "transaction_key": tx, "problem": "action_obligation_cents_mismatch", "financial_cents": match[1], "description_cents": cents(value)})
                if row.get("award_key") != match[0]:
                    counts["award_key_conflicts"] += 1
                    conflicts.append({"file": f.name, "row": n, "transaction_key": tx, "problem": "award_key_mismatch"})
                if str(row.get("action_date") or "") != match[2]:
                    counts["action_date_conflicts"] += 1
                if str(row.get("fiscal_year") or "") != str(match[3]):
                    counts["fiscal_year_conflicts"] += 1
        files.append(info)
    counts["canonical_financial_actions"] = c.execute("SELECT COUNT(*) FROM financial").fetchone()[0]
    counts["canonical_financial_missing_amounts"] = c.execute("SELECT COUNT(*) FROM financial WHERE cents IS NULL").fetchone()[0]
    for key in ("description_transactions_outside_financial", "description_missing_action_obligation", "action_obligation_conflicts", "award_key_conflicts", "action_date_conflicts", "fiscal_year_conflicts"):
        counts[key] += 0
    c.close()
    failed = bool(conflicts or counts["action_date_conflicts"] or counts["fiscal_year_conflicts"] or counts["canonical_financial_missing_amounts"])
    result = {"status": "conflicts_recorded" if failed else "passed", "counts": dict(counts), "conflicts": conflicts, "files": files, "scope": "Every USAspending canonical descriptive JSONL row, exact transaction/award keys, action obligations, action dates and fiscal years; duplicate source observations are comparisons only, never additional money", "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat()}
    (package / "audit/screen-financial-cross-validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(jdump({"status": result["status"], "counts": result["counts"]}))
    return int(failed)


def export(c, package, audit):
    candidate_keys = [r[0] for r in c.execute("SELECT DISTINCT award FROM observations WHERE selected=1 ORDER BY award")]
    if c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='institutional_hits'").fetchone():
        candidate_keys = sorted(set(candidate_keys) | {r[0] for r in c.execute("SELECT DISTINCT award FROM institutional_hits")})
    if c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='auxiliary_hits'").fetchone():
        candidate_keys = sorted(set(candidate_keys) | {r[0] for r in c.execute("SELECT DISTINCT award FROM auxiliary_hits")})
    candidates = [aggregate(c, key) for key in candidate_keys]
    piid_keys = collections.defaultdict(set)
    for r in candidates:
        for piid in r["award_ids"]:
            piid_keys[re.sub(r"[^A-Z0-9]", "", piid.upper())].add(r["award_key"])
    for r in candidates:
        r["potential_same_PIID_source_keys_requires_agency_parent_review"] = sorted({key for piid in r["award_ids"] for key in piid_keys[re.sub(r"[^A-Z0-9]", "", piid.upper())] if key != r["award_key"]})
    evidence = package / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "brakes-candidate-register.json").write_text(json.dumps(candidates, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(evidence / "brakes-candidate-register.csv", candidates)
    # Include all temporally relevant named-recipient awards, retaining missing-code cases.
    # Flag substantive relevance rather than excluding potential false negatives.
    trace_keys = [r[0] for r in c.execute("SELECT DISTINCT award FROM observations WHERE performers<>'[]' AND ((action_date>='2025-01-01' AND action_date<='2026-10-25') OR (action_date='' AND fy IN (2025,2026))) ORDER BY award")]
    trace = []
    for key in trace_keys:
        r = aggregate(c, key)
        performers = sorted({p for (s,) in c.execute("SELECT performers FROM observations WHERE award=?", (key,)) for p in json.loads(s)})
        source_dates = sorted({d for (d,) in c.execute("SELECT action_date FROM observations WHERE award=?", (key,)) if d})
        temporal_status = "dated_source_action_in_2025_2026" if any("2025-01-01" <= d <= "2026-10-25" for d in source_dates) else "source_FY2025_2026_only_exact_calendar_date_unresolved"
        trace.append({"award_key": key, "award_ids": r["award_ids"], "performers": performers, "entity_names": r["entity_names"], "recipient_roles": r["recipient_roles"], "source_action_dates": source_dates, "temporal_status": temporal_status, "psc": r["psc"], "naics": r["naics"], "relevance": "AI_autonomy_or_safeguard_text_match" if r["domain_matches"] or r["all_categories_preliminary"] else "named_recipient_temporal_match_scope_unresolved", "continuation_status": "unverified_recipient_match_does_not_establish_ASIMOV_continuation", "full_descriptions": r["full_descriptions"], "description_hashes_and_contact_redactions_same_order": r["description_hashes_and_contact_redactions_same_order"], "end_date_source_fields": r["end_date_source_fields"], "source_urls": r["source_urls"], **money_summary(c, key)})
    write_csv(evidence / "asimov-performer-continuation-check.csv", trace)
    audit["counts"] = {"financial_unique_transactions": c.execute("SELECT COUNT(*) FROM financial").fetchone()[0], "financial_unique_awards": c.execute("SELECT COUNT(DISTINCT award) FROM financial").fetchone()[0], "descriptive_context_physical_observations": c.execute("SELECT COUNT(*) FROM observations").fetchone()[0], "financial_transactions_missing_description": c.execute("SELECT COUNT(*) FROM financial f WHERE NOT EXISTS(SELECT 1 FROM observations o WHERE o.tx=f.tx)").fetchone()[0], "description_transaction_key_award_conflicts": c.execute("SELECT COUNT(*) FROM (SELECT tx FROM observations WHERE tx<>'' GROUP BY tx HAVING COUNT(DISTINCT award)>1)").fetchone()[0], "financial_description_award_key_mismatches": c.execute("SELECT COUNT(*) FROM observations o JOIN financial f ON o.tx=f.tx WHERE o.award<>f.award").fetchone()[0], "machine_screened_candidate_awards_and_documents": len(candidates), "performer_trace_awards": len(trace)}
    audit["primary_category_counts"] = dict(collections.Counter(r["primary_category_preliminary"] for r in candidates))
    audit["all_category_membership_counts_overlap_do_not_sum"] = {k: sum(k in r["all_categories_preliminary"] for r in candidates) for k in "ABCD"}
    # Primary category is one accounting bucket only. This is a broad candidate exposure,
    # not verified safeguard-specific spending and not an estimate of program budgets.
    audit["candidate_primary_category_obligation_cents_fy2024_2026_NOT_safeguard_spending"] = {k: sum(r["obligation_cents_fy2024_2026"] or 0 for r in candidates if r["primary_category_preliminary"] == k) for k in "ABCD"}


def validate_final_register(package, database):
    """Verify final financial conservation, complete CSV fields and public hashes."""
    rows = json.loads((package / "evidence/brakes-candidate-register.json").read_text(encoding="utf-8"))
    keys = [r["award_key"] for r in rows]
    if len(keys) != len(set(keys)):
        raise RuntimeError("Duplicate candidate award keys")
    c = sqlite3.connect("file:" + str(database.resolve()) + "?mode=ro", uri=True)
    checks = {}
    for field, condition in [("obligation_cents_fy2019_2026", "fy BETWEEN 2019 AND 2026"), ("obligation_cents_fy2024_2026", "fy BETWEEN 2024 AND 2026"), ("obligation_cents_cy2024_2026", "action_date BETWEEN '2024-01-01' AND '2026-10-25'")]:
        direct = c.execute("SELECT SUM(cents) FROM financial WHERE " + condition + " AND award IN (SELECT value FROM json_each(?))", (json.dumps(keys),)).fetchone()[0]
        published = sum(r[field] or 0 for r in rows)
        if direct != published:
            raise RuntimeError(f"Financial conservation failed: {field}")
        checks[field] = {"direct_canonical_sum": direct, "published_sum": published, "passed": True}
    with (package / "evidence/brakes-candidate-register.csv").open(encoding="utf-8", newline="") as f:
        csv_rows = list(csv.DictReader(f))
    if [r["award_key"] for r in csv_rows] != keys:
        raise RuntimeError("JSON/CSV candidate-key mismatch")
    for row, csv_row in zip(rows, csv_rows):
        if json.loads(csv_row["full_descriptions"]) != row["full_descriptions"]:
            raise RuntimeError("JSON/CSV full-description mismatch")
        if len(row["full_descriptions"]) != len(row["description_hashes_and_contact_redactions_same_order"]):
            raise RuntimeError("Description/hash count mismatch")
        for text, info in zip(row["full_descriptions"], row["description_hashes_and_contact_redactions_same_order"]):
            if hashlib.sha256(text.encode()).hexdigest() != info["published_sha256"]:
                raise RuntimeError("Published description hash mismatch")
        if any("start_date" in field for field in row["latest_end_date_fields_by_source_action_date"]):
            raise RuntimeError("Start date incorrectly treated as end date")
    with (package / "evidence/asimov-performer-continuation-check.csv").open(encoding="utf-8", newline="") as f:
        trace = list(csv.DictReader(f))
    expected_trace = c.execute("SELECT COUNT(DISTINCT award) FROM observations WHERE performers<>'[]' AND ((action_date>='2025-01-01' AND action_date<='2026-10-25') OR (action_date='' AND fy IN (2025,2026)))").fetchone()[0]
    if len(trace) != expected_trace:
        raise RuntimeError("Performer trace row conservation failed")
    first, last, october = c.execute("SELECT MIN(action_date),MAX(action_date),SUM(action_date>'2026-09-30') FROM financial").fetchone()
    financial_source_window = {"first_action_date": first, "latest_action_date": last, "actions_after_2026_09_30": october, "source_fiscal_year_rows": {str(y): n for y, n in c.execute("SELECT fy,COUNT(*) FROM financial GROUP BY fy")}, "limitation": "Archive creation/retrieval date does not extend action coverage. October2026 continuations require live checks. FY2019 begins2018-10-01; FY2024 includesOct-Dec2023."}
    c.close()
    paths = ["evidence/brakes-candidate-register.json", "evidence/brakes-candidate-register.csv", "evidence/asimov-performer-continuation-check.csv", "evidence/auxiliary-candidates.jsonl"]
    sizes = {name: (package / name).stat().st_size for name in paths}
    if any(size >= 100 * 1024 * 1024 for size in sizes.values()):
        raise RuntimeError("A public register exceeds GitHub's 100MiB file limit")
    result = {"status": "passed", "candidate_source_award_or_document_keys": len(rows), "unique_keys": len(set(keys)), "performer_trace_keys": len(trace), "financial_source_window": financial_source_window, "money_conservation": checks, "JSON_CSV_full_description_equality": True, "all_published_description_hashes_verified": True, "no_start_dates_labeled_as_end_dates": True, "max_candidate_CSV_field_chars": max(len(v) for row in csv_rows for v in row.values()), "max_performer_CSV_field_chars": max(len(v) for row in trace for v in row.values()), "files_bytes": sizes, "all_files_under_GitHub_100MiB_limit": True, "primary_category_counts_PRELIMINARY_not_verified_programs": dict(collections.Counter(row["primary_category_preliminary"] for row in rows)), "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat()}
    result["financial_action_corpus_scope_limitation"] = "Money conservation validates net obligations within the acquired action corpus/window only. Acquisition filters can omit older positive, negative and zero actions; complete award funding and history completeness are not established. Live history figures remain separate."
    (package / "audit/screen-final-register-validation.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(jdump(result))
    return 0


def main():
    global TERMS, DOMAIN, ANCHORS, RX, DRX, ARX, GATE
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--archives", type=Path, nargs="*", default=[])
    p.add_argument("--extracted-dir", type=Path)
    p.add_argument("--work-dir", type=Path, default=Path("/workspace/scratch/f4-data"))
    p.add_argument("--package", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--auxiliary-only", action="store_true", help="Requires pyarrow; screen parquet/JSON/TXT and check JSONL semantic mirrors")
    p.add_argument("--enrich-end-dates", type=Path, help="Private auxiliary-dates.sqlite; update exact-key register end dates after both sweeps")
    p.add_argument("--editor-supplement", type=Path, help="Private canonical screen.sqlite; add fresh editor terms and regenerate registers")
    p.add_argument("--validate-financial-joins", type=Path, help="Private screen.sqlite; requires --extracted-dir, validates all descriptive monetary observations")
    p.add_argument("--merge-auxiliary-part", type=Path, nargs=2, action="append", metavar=("PACKAGE", "WORKSPACE"), help="Repeat for disjoint completed auxiliary partitions")
    p.add_argument("--lexicon-config", type=Path, help="Recorded screen-accounting.json or compatible lexicon/domain_lexicon/institutional_anchors JSON")
    p.add_argument("--institution-supplement", action="store_true", help="Requires pyarrow and --extracted-dir; checks raw TRMC office alias and funding-goals denominator")
    p.add_argument("--import-auxiliary-award-hits", type=Path, help="Private screen.sqlite; integrate exact-key auxiliary safeguard leads and regenerate main registers")
    p.add_argument("--validate-complete-coverage", action="store_true", help="Check canonical/auxiliary file union and cross-format hashes against full input inventory")
    p.add_argument("--validate-final-register", type=Path, help="Private screen.sqlite; validate final CSV/JSON hashes, row counts and canonical financial conservation")
    args = p.parse_args()
    if args.lexicon_config:
        config = json.loads(args.lexicon_config.read_text(encoding="utf-8"))
        TERMS = config["lexicon"]
        DOMAIN = config["domain_lexicon"]
        ANCHORS = config["institutional_anchors"]
        RX = {k: [(t, pattern(t)) for t in v] for k, v in TERMS.items()}
        DRX = [(t, pattern(t)) for t in DOMAIN]
        ARX = [(t, pattern(t)) for t in ANCHORS]
        GATE = re.compile(r"(?<![A-Z0-9])(?:" + "|".join(re.escape(normal(t)).replace(r"\*", r"[A-Z0-9]*") for t in DOMAIN + ANCHORS) + r")(?![A-Z0-9])")
    if args.institution_supplement:
        if args.extracted_dir is None:
            p.error("--institution-supplement requires --extracted-dir")
        return institution_supplement(args.extracted_dir, args.package)
    if args.import_auxiliary_award_hits:
        return import_auxiliary_award_hits(args.package, args.import_auxiliary_award_hits)
    if args.validate_complete_coverage:
        return validate_complete_coverage(args.package)
    if args.validate_final_register:
        return validate_final_register(args.package, args.validate_final_register)
    if args.merge_auxiliary_part:
        return merge_auxiliary_parts(args.merge_auxiliary_part, args.package, args.work_dir)
    if args.validate_financial_joins:
        if args.extracted_dir is None:
            p.error("--validate-financial-joins requires --extracted-dir")
        return validate_financial_joins(args.extracted_dir, args.validate_financial_joins, args.package)
    if args.editor_supplement:
        return supplemental_editor_screen(args.package, args.editor_supplement)
    if args.enrich_end_dates:
        return enrich_end_dates(args.package, args.enrich_end_dates)
    if args.auxiliary_only:
        if args.extracted_dir is None:
            p.error("--auxiliary-only requires --extracted-dir")
        return auxiliary_sweep(args.extracted_dir, args.package, args.work_dir)
    started = time.time()
    audit = {"started_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "status": "started", "archives": [], "archive_members": [], "files": [], "failures": [], "lexicon": TERMS, "domain_lexicon": DOMAIN, "institutional_anchors": ANCHORS, "limitations": ["Machine hits are broad leads, not evidence of implemented safeguards.", "Primary A>B>C>D precedence is accounting only; all overlapping memberships retained.", "All obligation sums use exact-key, transaction-deduplicated financial_actions rows, preserving negative amounts. Ceilings and SBIR headline values are never added.", "Missing amounts and missing end dates remain null/explicitly missing, not zero or assumed inactive.", "FY windows use source fiscal_year. CY window uses action_date through 2026-10-25. Snapshot coverage does not extend automatically to cutoff.", "Performer-recipient matching is not proof of ASIMOV continuation; PSC/NAICS and scope review remain necessary.", "Input source universe is bounded; screening does not establish worldwide or classified-program absence."]}
    args.package.joinpath("audit").mkdir(parents=True, exist_ok=True)
    audit_path = args.package / "audit/screen-accounting.json"
    try:
        if not args.archives and args.extracted_dir is None:
            raise RuntimeError("No archives or extracted directory supplied; full-row screening is blocked, not completed")
        args.work_dir.mkdir(parents=True, exist_ok=True)
        files = extract_archives(args.archives, args.work_dir / "extracted", audit)
        if args.extracted_dir:
            files.extend(x for x in args.extracted_dir.rglob("*") if x.is_file())
            audit["extracted_input_verification"] = "Archive hashes not verified for --extracted-dir; per-file hashes and rows recorded"
        c = create_db(args.work_dir / "screen.sqlite")
        ingest(c, files, audit)
        by_name = collections.defaultdict(list)
        for f in audit["files"]:
            by_name[f["name"]].append(f)
        audit["expected_file_coverage"] = {
            name: {"expected_rows": expected, "appearances": len(by_name[name]),
                   "observed_unique_content_row_counts": [x["physical_rows"] for x in by_name[name] if x["status"] != "duplicate_bytes_accounted_not_rescanned"],
                   "matches_expected": any(x["physical_rows"] == expected and x["status"].startswith("full_stream") for x in by_name[name])}
            for name, expected in EXPECTED_ROWS.items()
        }
        audit["missing_or_mismatched_expected_files"] = [name for name, r in audit["expected_file_coverage"].items() if not r["matches_expected"]]
        export(c, args.package, audit)
        c.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        c.close()
        audit["status"] = "completed_with_recorded_gaps" if audit["failures"] or any(x.get("errors") for x in audit["files"]) or audit["missing_or_mismatched_expected_files"] else "completed"
    except Exception as e:
        audit["status"] = "blocked_or_failed"
        audit["failures"].append({"error": str(e)})
        print(str(e), file=sys.stderr)
    audit["finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    audit["elapsed_seconds"] = round(time.time() - started, 2)
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(jdump({"status": audit["status"], "counts": audit.get("counts"), "audit": str(audit_path)}))
    return 1 if audit["status"] == "blocked_or_failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
