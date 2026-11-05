#!/usr/bin/env python3
"""Compare last page of part A to first page of part B, without modifying PDFs.

Usage: python check_split_boundary.py PART_A.pdf PART_B.pdf
Text and default-rendered pixels are separate checks. A match is reported,
not removed: citations must continue to refer to the original split files.
"""
import argparse
import json

import fitz


def compare(part_a: str, part_b: str) -> dict:
    with fitz.open(part_a) as a, fitz.open(part_b) as b:
        if not len(a) or not len(b):
            raise ValueError("Both PDFs must contain at least one page")
        a_page, b_page = a[-1], b[0]
        a_pix, b_pix = a_page.get_pixmap(), b_page.get_pixmap()
        return {
            "part_a_pages": len(a),
            "part_b_pages": len(b),
            "equal_boundary_text": a_page.get_text() == b_page.get_text(),
            "equal_boundary_render": (a_pix.width, a_pix.height, a_pix.n, a_pix.samples)
            == (b_pix.width, b_pix.height, b_pix.n, b_pix.samples),
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("part_a")
    parser.add_argument("part_b")
    args = parser.parse_args()
    print(json.dumps(compare(args.part_a, args.part_b), indent=2))
