#!/usr/bin/env python3
"""Recreate the 301-record A/B review scan receipt using only the standard library.

Usage:
    python3 review_recovered_ab.py --input /private/path/ab-high-priority-review.csv \
        --output /tmp/recovered-301-ab-scan-receipt.csv

This script scans every supplied description. The 34 full-description human reads
are historical reviewer annotations keyed by complete source identity, not a claim
that this script performs or repeats human adjudication. Findings are explained in
evidence/recovered-301-ab-targeted-review.md. No network requests, financial joins,
money aggregation, classification changes, or writes to the input are performed.
The original input remains private. Default hash/count guards bind reproduction to
the reviewed snapshot; --allow-input-change permits an explicitly different scan,
while still requiring all 34 annotated source keys to exist without duplication.
"""

import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import re

EXPECTED_INPUT_SHA256 = "814dd1cbdabfde56b1dbd77ea33e56840db5bbc8a248a6f19349b4339ba60153"
EXPECTED_ROWS = 301
EXPECTED_DESCRIPTIONS = 1088

# These annotations record the actual full-description shortlist read by the
# reviewer. Keys prevent silently assigning that review to a different row if an
# input is reordered. Notes describe scope, not independently verified results.
HUMAN_FULL_READ_ANNOTATIONS = {
    "CONT_AWD_FA238524CB031_9700_-NONE-_-NONE-": "Alare loitering-strike development; harm benefit, no normative evaluator established.",
    "CONT_AWD_FA238525CB028_9700_-NONE-_-NONE-": "Mobile-target tracking; collateral mitigation as a reason to wait, not a legal test.",
    "CONT_AWD_FA864924P0435_9700_-NONE-_-NONE-": "Polysentry JAG ROE/orders/authorities retrieval; historical period.",
    "CONT_AWD_FA864925P0270_9700_-NONE-_-NONE-": "oneNav PNT resilience; harm contribution does not establish normative testing.",
    "CONT_AWD_FA864925P0310_9700_-NONE-_-NONE-": "Spacecraft supervisory awareness, not lethal authorization.",
    "CONT_AWD_FA864925P0331_9700_-NONE-_-NONE-": "oneNav navigation resilience; no separate legal constraint described.",
    "CONT_AWD_FA864925P0337_9700_-NONE-_-NONE-": "WarRoom simulation/rehearsal claims harm reduction; acceptance metrics unspecified.",
    "CONT_AWD_FA864925P0470_9700_-NONE-_-NONE-": "Kilsar ROE/legal guidance with human validation; legal decision support.",
    "CONT_AWD_N6426725C7123_9700_-NONE-_-NONE-": "NOEMON computer-encoded EW ROE; rule-aware research, no achieved legal assurance proven.",
    "CONT_AWD_N0002424CS204_9700_-NONE-_-NONE-": "Ship mechanical/electrical supervisory control; ROE refers to human/system interaction.",
    "CONT_AWD_W5170125CA287_9700_-NONE-_-NONE-": "Dynamo runtime guardrails; specific normative policy and independent validation unspecified.",
    "CONT_AWD_W911NF24P0033_9700_-NONE-_-NONE-": "Coalesce proposes human approval of all lethal actions; historical period.",
    "SBIR:Department of Defense|Special Operations Command|SBIR|Phase II – Direct to Phase II|S2D-0431|6SVL4-22-C-0014|2022": "AssistMATE ROE-compliant course-of-action claims; unmatched financial source.",
    "SUBAWARD:ASST_NON_FA87501820087_097|6F328D3E-FCD1-11EF-AB59-07ECA35F602B|S9002086|2018-10-23": "Threat-intelligence collateral metrics are cyber-scoped; no parent money attribution.",
    "SUBAWARD:ASST_NON_FA95502010200_097|6F7E8B44-FCD1-11EF-AB59-07ECA35F602B|SUB00002833-01|2022-08-11": "Effects assessment research; no demonstrated autonomous-weapons legal constraints.",
    "SUBAWARD:ASST_NON_HR00112420004_097|4D4D2276-9B13-43B5-A0D0-0B3CD9B9A603|001075|2026-03-26": "AI containment and human governability for cyber protection teams.",
    "ASST_NON_FA95502010130_097": "Normative agency title; historical period and insufficient weapons scope.",
    "ASST_NON_FA95502110359_097": "Moral justification/human-machine trust title; historical period.",
    "ASST_NON_FA95502310283_097": "Theory-of-mind trust calibration; no legal or lethal-authority mechanism described.",
    "ASST_NON_W911NF261A113_097": "Normative agency research title; precise technical and weapons scope unresolved.",
    "CONT_AWD_FA864921P0457_9700_-NONE-_-NONE-": "Joint Air Strike Planner includes ROE; historical planning research.",
    "CONT_AWD_FA864921P0885_9700_-NONE-_-NONE-": "Civilian disposition/collateral context in ISR; historical record and incomplete description.",
    "CONT_AWD_FA864923P0469_9700_-NONE-_-NONE-": "AILA targeting-package legal review, explicit distinction/proportionality; historical period.",
    "CONT_AWD_FA864925P0297_9700_-NONE-_-NONE-": "Weather sensing; planning benefit does not make it a normative autonomy test.",
    "CONT_AWD_FA864925P0472_9700_-NONE-_-NONE-": "Low-collateral counter-drone effects; legal/autonomy control not established.",
    "CONT_AWD_FA864925P0502_9700_-NONE-_-NONE-": "Counter-drone effector design; no normative evaluator described.",
    "CONT_AWD_N6833520C0324_9700_-NONE-_-NONE-": "DSOARS-R explicitly proposes ROE enforcement; historical research.",
    "CONT_AWD_W15QKN19P0032_9700_-NONE-_-NONE-": "FIRE contextual fire-control reasoning and ROE; historical research.",
    "CONT_AWD_W911NF19C0053_9700_-NONE-_-NONE-": "SWIFT ARROW threat confirmation/ROE relevance; historical research.",
    "OPPORTUNITY:362743": "DICE human-controlled decentralized AI opportunity; not an award.",
    "SBIR:Department of Energy||SBIR|Phase I|282129|DE-SC0025059|2024": "Foundation-model evaluation/proliferation context; weapons LOAC scope unestablished.",
    "SUBAWARD:ASST_NON_W56HZV2420001_097|49FC8AE6-FCD2-11EF-AB59-07ECA35F602B|SUBK00021898|2024-04-19": "Clemson trust and navigation simulation; human participation is not lethal authorization.",
    "SUBAWARD:ASST_NON_W56HZV2420001_097|49FCB71E-FCD2-11EF-AB59-07ECA35F602B|SUBK00021898|2024-07-11": "Repeated Clemson subaward appearance; no separate program/money inference.",
    "SUBAWARD:CONT_AWD_W5170124C0138_9700_-NONE-_-NONE-|782AFA72-FCBB-11EF-8E2A-E7034F2D18CD|2024-ROE-001|2024-08-28": "Rules of Engagement LLC is a contractor name, not a specified ROE compliance test.",
}

TERMS = re.compile(
    r"law[s]? of (?:armed conflict|war)|\bLOAC\b|\bIHL\b|rules? of engagement|"
    r"civilian harm|collateral damage|non.?combatant|ethical|ethics|moral|normative|"
    r"nonmaleficence|human.?in.?the.?loop|human.?on.?the.?loop|"
    r"human (?:control|authorization|judgment|judgement)|abort|veto|"
    r"positive (?:control|authorization)|bounded (?:autonomy|engagement)|"
    r"human.{0,30}approv|govern|de.escalat|surrender",
    re.I,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--allow-input-change", action="store_true")
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("Input and output must be different files")
    input_hash = hashlib.sha256(args.input.read_bytes()).hexdigest()
    if not args.allow_input_change and input_hash != EXPECTED_INPUT_SHA256:
        parser.error("Input hash differs from the reviewed snapshot; use --allow-input-change explicitly for a new scan")
    with args.input.open(encoding="utf-8", newline="") as stream:
        records = list(csv.DictReader(stream))
    counts = collections.Counter(row["award_key"] for row in records)
    missing = set(HUMAN_FULL_READ_ANNOTATIONS) - counts.keys()
    duplicate = {key for key, count in counts.items() if count > 1}
    if missing or duplicate:
        parser.error(f"Missing annotated keys: {sorted(missing)}; duplicate input keys: {sorted(duplicate)}")
    assert len(HUMAN_FULL_READ_ANNOTATIONS) == 34
    receipt = []
    description_count = 0
    for index, record in enumerate(records, 1):
        descriptions = json.loads(record["descriptions"])
        if not isinstance(descriptions, list) or any(not isinstance(text, str) for text in descriptions):
            parser.error(f"Invalid description list at input row {index}")
        description_count += len(descriptions)
        detected = sorted({match.group().lower() for text in descriptions for match in TERMS.finditer(text)})
        receipt.append({
            "priority_csv_row_one_based_excluding_header": index,
            "award_key": record["award_key"],
            "description_count": len(descriptions),
            "all_descriptions_scanned": True,
            "description_list_sha256": hashlib.sha256(json.dumps(descriptions, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest(),
            "terms_detected": json.dumps(detected),
            "review_depth": "full supplied descriptions read for shortlist" if record["award_key"] in HUMAN_FULL_READ_ANNOTATIONS else "complete deterministic description scan plus row/context triage; not full SOW review",
            "identity_quarantined_record": "identity_conflict" in record["record_kinds"],
            "source_urls": record["source_urls"],
            "provenance_sidecar": record["provenance_sidecar"],
            "money_attribution": record["financial_attribution"],
        })
    if not args.allow_input_change and (len(records), description_count) != (EXPECTED_ROWS, EXPECTED_DESCRIPTIONS):
        parser.error("Unexpected reviewed-snapshot row or description count")
    if not receipt:
        parser.error("Empty input")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(receipt[0]))
        writer.writeheader()
        writer.writerows(receipt)
    print(json.dumps({"rows": len(records), "descriptions": description_count,
                      "historically_human_read_keys": len(HUMAN_FULL_READ_ANNOTATIONS),
                      "input_sha256": input_hash,
                      "receipt_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest()}, indent=2))


if __name__ == "__main__":
    main()
