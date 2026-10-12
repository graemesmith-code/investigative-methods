"""Re-extract inspected source versions, preserving reviewed Western claim entries.

Host workbook cells and Peru's SEC production table are extracted by code.
Other Western values and all semantic/entity bridges remain explicit audit judgments.
Changed bytes are rejected before those judgments are reused.
"""
import argparse
from decimal import Decimal
from html.parser import HTMLParser
from io import BytesIO
import json
from pathlib import Path
import re
import zipfile
import openpyxl
from run import HERE, RESEARCH, load_json
from sources import verify


class HTMLText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, text):
        self.parts.append(text)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def workbook(path):
    # EITI downloads use .bin identifiers in the audit manifest but are XLSX files.
    return openpyxl.load_workbook(BytesIO(path.read_bytes()), read_only=True, data_only=True)


def peru_mine_values(html):
    parser = HTMLText()
    parser.feed(html)
    text = re.sub(r"\s+", " ", " ".join(parser.parts).replace("\u200b", " "))
    segments = [text[m.start():m.start() + 1600].split("ZINC (thousand pounds)")[0]
                for m in re.finditer(re.escape("MOLYBDENUM (thousand pounds)"), text)]
    segments = [s for s in segments if "Toquepala" in s and "Cuajone" in s]
    require(len(segments) == 1, "unique per-mine molybdenum table not found")
    mines = {}
    for mine in ("Toquepala", "Cuajone"):
        match = re.search(mine + r"\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", segments[0])
        require(match is not None, f"missing mine row: {mine}")
        # Column order 2024/2023/2022 was checked in this hash-pinned edition.
        mines[mine] = match.group(2).replace(",", "")
    return mines


def extract_peru(cache):
    mines = peru_mine_values((cache / "southern-sec-2024.html").read_text(encoding="utf-8"))
    book = workbook(cache / "audit-peru-annual-2024.xlsx")
    try:
        sheet = book["Mo-Empresas"]
        require(sheet["J4"].value == 2023, "wrong production year")
        require("SOUTHERN" in sheet["A7"].value.upper(), "wrong production company")
        require("preliminares" in sheet["A16"].value.lower() and "2024" in str(sheet["K4"].value),
                "preliminary-year marker changed")
        require(sheet["J7"].value is not None, "missing host production")
        return {"western_thousand_lb": mines, "host_fine_tonnes": str(sheet["J7"].value)}
    finally:
        book.close()


def extract_ity(cache, manual):
    book = workbook(cache / "ivory-annexes.bin")
    cells = []
    try:
        for name, company in (("34.1", "SOCIETE DES MINES D'ITY"),
                              ("34.5", "SOCIETE DES MINES DE DAAPLEU"),
                              ("34.8", "SOCIETE DES MINES DE FLOLEU")):
            sheet = book[name]
            require(sheet["E2"].value == company and sheet["K2"].value == 2024,
                    "Ity entity or year changed")
            for row, percentage in ((27, "85%"), (42, "15%")):
                require(percentage in sheet[f"C{row}"].value and "Royalties" in sheet[f"C{row}"].value,
                        "royalty label changed")
                values = [sheet[f"{col}{row}"].value for col in "EFG"]
                require(all(v is not None for v in values), "missing company royalty cell")
                cells.append(dict(sheet=name, row=row, **dict(zip(
                    ("initial", "adjustment", "final"), map(str, values)))))
        return {"company_cells": cells, "western_usd": manual["western_values"],
                "fx_xof_per_usd": ["595.72", "631.40"]}
    finally:
        book.close()


def extract_kibali(cache, manual):
    book = workbook(cache / "congo-annexes.bin")
    try:
        sheet = book["Annexe 11 "]
        require("2023" in book["Annexe 10"]["A6"].value, "wrong Kibali period")
        require(sheet["C29"].value == "Oui" and sheet["F29"].value == "A0702049L",
                "company submission or entity marker changed")
        require(sheet["L29"].value.upper() == "BARRICK", "wrong ownership party")
        attribution = book["Annexe 13 "]["D27"].value
        require("déclaré" in attribution and "Barrick" in attribution,
                "company-attribution sentence missing")
        require(sheet["N29"].value is not None, "missing company ownership")
        return {"host_percent": {"Barrick": str(sheet["N29"].value)},
                "western_percent_by_date": manual["western_values"]}
    finally:
        book.close()


def extract_essakane(cache, manual):
    with zipfile.ZipFile(cache / "burkina-annexes.bin") as outer:
        embedded = outer.read("xl/embeddings/Microsoft_Excel_Worksheet3.xlsx")
    book = openpyxl.load_workbook(BytesIO(embedded), read_only=True, data_only=True)
    try:
        sheet = book["17.Structure de Capital "]
        require("2024" in sheet["A6"].value and "31/12/2023" in sheet["A12"].value,
                "Essakane date alternatives changed")
        require(sheet["C15"].value == "IAMGOLD CORPORATION", "wrong ownership company")
        require(sheet["D15"].value is not None and sheet["D13"].value is not None,
                "missing ownership fraction")
        return {"host_percent": {"IAMGOLD": str(Decimal(str(sheet["D15"].value)) * 100),
                                 "state": str(Decimal(str(sheet["D13"].value)) * 100)},
                "western_percent_by_date": manual["western_values"]}
    finally:
        book.close()


def extract_cases(cache):
    manifest = {s["source_id"]: s for s in load_json(RESEARCH / "source-manifest.json")}
    cases = [load_json(p) for p in sorted((HERE / "cases").glob("*.json"))]
    ledger = load_json(HERE / "fixtures/manual-western-claims.json")
    hashes = {}
    for sid in sorted({sid for c in cases for sid in c["source_ids"]}):
        hashes[sid] = verify(cache / sid, manifest[sid])
    extractors = {"RAB-MIN-02": lambda c, m: extract_peru(c), "RAB-MIN-03": extract_ity,
                  "RAB-MIN-07": extract_kibali, "RAB-MIN-08": extract_essakane}
    observations = []
    for case in cases:
        values = extractors[case["id"]](cache, ledger[case["id"]])
        observations.append({"schema_version": 1, "case_id": case["id"],
                             "context": case["required_context"],
                             "gates": dict.fromkeys(case["required_gates"], True),
                             "source_hashes": {s: hashes[s] for s in case["source_ids"]},
                             "values": values})
    return {"mode": "verified_originals_with_reviewed_manual_western_claims", "observations": observations}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=HERE / "cache")
    parser.add_argument("--output", type=Path, default=HERE / "output/extracted-observations.json")
    args = parser.parse_args()
    try:
        result = extract_cases(args.cache)
    except (ValueError, KeyError, OSError, zipfile.BadZipFile) as exc:
        parser.exit(2, f"Extraction blocked: {exc}\n")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Re-extracted four specimens; manual Western claim ledger retained. Output: {args.output}")


if __name__ == "__main__":
    main()
