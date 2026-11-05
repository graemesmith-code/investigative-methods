#!/usr/bin/env python3
"""Read local AER PDFs; preserve page boundaries and produce review aids.

This is text extraction and indexing, not an automated compliance assessment.
Install PyMuPDF, then run: python extract_aer.py INPUT_DIR OUTPUT_DIR
Source PDFs are never edited. Output contains source text and is private.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

import fitz


def extract(source: Path, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    manifest = []
    index = []
    terms = re.compile(r"seismi|earthquake|suspend|restart|shut.?down|cut sand|skip|Duvernay|Start Frac|End Frac", re.I)
    for path in sorted(source.glob("*.pdf")):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        with fitz.open(path) as pdf:
            pages = [{"page": i + 1, "text": page.get_text(sort=True)} for i, page in enumerate(pdf)]
        (output / (path.stem + ".json")).write_text(json.dumps(pages, ensure_ascii=False, indent=2))
        (output / (path.stem + ".txt")).write_text("\n\n".join(f"PAGE {p['page']}\n{p['text']}" for p in pages))
        manifest.append({"file": path.name, "sha256": digest, "pages": len(pages), "size_bytes": path.stat().st_size})
        for page in pages:
            lines = page["text"].splitlines()
            matches = [{"line": i + 1, "context": "\n".join(lines[max(0, i - 1):i + 3])} for i, line in enumerate(lines) if terms.search(line)]
            if matches:
                index.append({"file": path.name, "page": page["page"], "matches": matches})
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2))
    (output / "review_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2))
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    extract(args.source, args.output)
