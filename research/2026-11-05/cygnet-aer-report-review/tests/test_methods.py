"""Synthetic smoke tests only; no source records or actual findings are used."""
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "code"


class MethodTests(unittest.TestCase):
    def test_pdf_extraction_preserves_original_and_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            output = Path(tmp) / "output"
            source.mkdir()
            pdf_path = source / "synthetic.pdf"
            with fitz.open() as pdf:
                pdf.new_page().insert_text((72, 72), "Synthetic seismic review marker")
                pdf.new_page()
                pdf.save(pdf_path)
            original = pdf_path.read_bytes()
            subprocess.run([sys.executable, str(CODE / "extract_aer.py"),
                            str(source), str(output)], check=True, capture_output=True)
            self.assertEqual(pdf_path.read_bytes(), original)
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(manifest[0]["sha256"], hashlib.sha256(original).hexdigest())
            self.assertEqual(manifest[0]["pages"], 2)
            self.assertEqual(manifest[0]["size_bytes"], len(original))
            pages = json.loads((output / "synthetic.json").read_text())
            self.assertEqual([p["page"] for p in pages], [1, 2])
            self.assertEqual(pages[1]["text"], "")
            index = json.loads((output / "review_index.json").read_text())
            self.assertEqual(index[0]["page"], 1)
            self.assertIn("seismic", index[0]["matches"][0]["context"])

    def test_service_index_keeps_page_and_comment_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "synthetic.json"
            output = Path(tmp) / "index.txt"
            source.write_text(json.dumps([
                {"page": 1, "text": "Stage 1 of 1\nStart Frac 09:00 End Frac 09:30\n"
                                     "Frac Comments\nSynthetic comment"},
                {"page": 2, "text": "Synthetic chart text"},
            ]))
            subprocess.run([sys.executable, str(CODE / "extract_service_timeline.py"),
                            str(source), str(output)], check=True, capture_output=True)
            text = output.read_text()
            for expected in ["PAGE 1", "PAGE 2", "End Frac 09:30", "Synthetic comment",
                             "Synthetic chart text"]:
                self.assertIn(expected, text)

    def test_completion_index_preserves_raw_clock_and_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "aer-reports"
            source.mkdir()
            (source / "TR,33458526,0000000,synthetic.json").write_text(json.dumps([
                {"page": 7, "text": "Report - 2025-02-20\n"
                  "23:30 00:30 1.00 h Synthetic row\nContinuation text\n"},
                {"page": 8, "text": "Report - 2025-02-21\n"
                  "Unattached page continuation\n00:30 01:00 0.50 h Next row\n"},
            ]))
            subprocess.run([sys.executable, str(CODE / "extract_completion_chronology.py")],
                           cwd=tmp, check=True, capture_output=True)
            rows = json.loads((source / "completion_chronology_raw.json").read_text())
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["page"], 7)
            self.assertEqual(rows[0]["from"], "23:30")
            self.assertEqual(rows[0]["to"], "00:30")
            self.assertEqual(rows[0]["duration_hours_as_reported"], "1.00")
            self.assertIn("Continuation text", rows[0]["text"])
            self.assertNotIn("Unattached page continuation", rows[0]["text"])
            self.assertEqual(rows[1]["page"], 8)

    def test_boundary_checker_detects_match_and_difference(self):
        spec = importlib.util.spec_from_file_location("boundary", CODE / "check_split_boundary.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            paths = [Path(tmp) / name for name in ["a.pdf", "same.pdf", "different.pdf"]]
            for path, text in zip(paths, ["Synthetic boundary", "Synthetic boundary", "Different boundary"]):
                with fitz.open() as pdf:
                    pdf.new_page().insert_text((72, 72), text)
                    pdf.save(path)
            match = module.compare(str(paths[0]), str(paths[1]))
            different = module.compare(str(paths[0]), str(paths[2]))
            self.assertTrue(match["equal_boundary_text"])
            self.assertTrue(match["equal_boundary_render"])
            self.assertFalse(different["equal_boundary_text"])
            self.assertFalse(different["equal_boundary_render"])


if __name__ == "__main__":
    unittest.main()
