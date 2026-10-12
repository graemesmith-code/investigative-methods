import copy
import hashlib
from pathlib import Path
import tempfile
import unittest
from compare import assess
from run import HERE, RESEARCH, load_json
from sources import verify


class ComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = {s["source_id"]: s for s in load_json(RESEARCH / "source-manifest.json")}
        cls.cases = {c["id"]: c for c in (load_json(p) for p in (HERE / "cases").glob("*.json"))}
        cls.observations = {o["case_id"]: o for o in load_json(HERE / "fixtures/observations.json")["observations"]}

    def specimen(self, number):
        key = f"RAB-MIN-{number:02}"
        return self.cases[key], copy.deepcopy(self.observations[key])

    def result(self, case, observation):
        return assess(case, observation, self.manifest)["status"]

    def test_four_inspected_pairs_are_consistent(self):
        for number in (2, 3, 7, 8):
            with self.subTest(number=number):
                self.assertEqual(self.result(*self.specimen(number)), "consistent")

    def test_changed_source_requires_review(self):
        case, obs = self.specimen(2)
        obs["source_hashes"][case["source_ids"][0]] = "0" * 64
        self.assertEqual(self.result(case, obs), "blocked")

    def test_unknown_period_metric_and_company_block(self):
        for field in ("period", "metric", "entity_scope", "basis", "attribution"):
            case, obs = self.specimen(2)
            obs["context"][field] = "different"
            self.assertEqual(self.result(case, obs), "blocked")

    def test_preliminary_or_unreviewed_claim_blocks(self):
        for gate in ("non_preliminary", "company_attribution_reviewed", "amendment_status_reviewed"):
            case, obs = self.specimen(2)
            obs["gates"][gate] = False
            self.assertEqual(self.result(case, obs), "blocked")

    def test_peru_rounding_boundary_and_synthetic_gap(self):
        case, obs = self.specimen(2)
        obs["values"]["host_fine_tonnes"] = "10056.14284290"
        self.assertEqual(self.result(case, obs), "consistent")
        obs["values"]["host_fine_tonnes"] = "11000"
        self.assertEqual(self.result(case, obs), "contradiction_candidate")

    def test_missing_zero_and_nonfinite_are_distinct(self):
        for value in (None, "NaN", "Infinity", True):
            case, obs = self.specimen(2)
            obs["values"]["host_fine_tonnes"] = value
            self.assertEqual(self.result(case, obs), "blocked")

    def test_wrong_mine_population_blocks(self):
        case, obs = self.specimen(2)
        obs["values"]["western_thousand_lb"]["Mexico"] = "100"
        self.assertEqual(self.result(case, obs), "blocked")

    def test_incomplete_or_duplicate_royalty_basket_blocks(self):
        for duplicate in (False, True):
            case, obs = self.specimen(3)
            cells = obs["values"]["company_cells"]
            cells.pop()
            if duplicate:
                cells.append(copy.deepcopy(cells[0]))
            self.assertEqual(self.result(case, obs), "blocked")

    def test_negative_refund_and_reconciliation_block(self):
        for values in (("-1", "0", "-1"), ("100", "2", "102"), (None, "0", None)):
            case, obs = self.specimen(3)
            obs["values"]["company_cells"][0].update(zip(("initial", "adjustment", "final"), values))
            self.assertEqual(self.result(case, obs), "blocked")

    def test_ity_synthetic_gap_is_candidate(self):
        case, obs = self.specimen(3)
        obs["values"]["western_usd"] = "60000000"
        self.assertEqual(self.result(case, obs), "contradiction_candidate")

    def test_changed_fx_basis_blocks(self):
        case, obs = self.specimen(3)
        obs["values"]["fx_xof_per_usd"] = ["604.935", "604.935"]
        self.assertEqual(self.result(case, obs), "blocked")

    def test_one_compatible_date_prevents_contradiction(self):
        case, obs = self.specimen(8)
        obs["values"]["western_percent_by_date"]["2024"] = {"IAMGOLD": "85", "state": "15"}
        self.assertEqual(self.result(case, obs), "blocked")

    def test_incompatible_at_every_date_is_candidate(self):
        case, obs = self.specimen(8)
        obs["values"]["host_percent"] = {"IAMGOLD": "80", "state": "20"}
        self.assertEqual(self.result(case, obs), "contradiction_candidate")

    def test_missing_date_or_party_blocks(self):
        case, obs = self.specimen(8)
        del obs["values"]["western_percent_by_date"]["2024"]
        self.assertEqual(self.result(case, obs), "blocked")

    def test_direct_versus_group_interest_blocks(self):
        case, obs = self.specimen(7)
        obs["context"]["basis"] = "direct registered holding"
        self.assertEqual(self.result(case, obs), "blocked")

    def test_invalid_ownership_blocks(self):
        case, obs = self.specimen(7)
        obs["values"]["host_percent"]["Barrick"] = "101"
        self.assertEqual(self.result(case, obs), "blocked")

    def test_missing_observation_blocks(self):
        self.assertEqual(self.result(self.specimen(2)[0], {}), "blocked")

    def test_wrong_bytes_and_html_landing_page_block(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.pdf"
            data = b"<html>Not the promised PDF</html>"
            path.write_bytes(data)
            record = {"source_id": "sample.pdf", "bytes": len(data),
                      "sha256": hashlib.sha256(data).hexdigest()}
            with self.assertRaisesRegex(ValueError, "not a PDF"):
                verify(path, record)
            record["sha256"] = "0" * 64
            with self.assertRaisesRegex(ValueError, "changed source"):
                verify(path, record)


if __name__ == "__main__":
    unittest.main()
