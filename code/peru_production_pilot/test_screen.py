"""Checks of evidence gates and adversarial changes, not proof of real-world recall."""
import copy,json,unittest
from decimal import Decimal as D
from pathlib import Path
from screen import compare,conversion,DEFAULT
class ScreenControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=json.loads((DEFAULT/'comparison-input.json').read_text())
        cls.base=next(r for r in cls.rows if r['record_id']=='PERU-hudbay-Cu-2023')
    def sample(self):return copy.deepcopy(self.base)
    def test_known_agreement(self):self.assertEqual(compare(self.sample())['result'],'consistent_with_display_precision')
    def test_injected_ten_percent_gap(self):
        r=self.sample();r['host_original_value']=str(D(r['host_original_value'])*D('1.10'))
        x=compare(r);self.assertTrue(x['numeric_flag']);self.assertFalse(x['confirmed_company_contradiction'])
    def test_wrong_year(self):
        r=self.sample();r['western_claim']['year']=2022;self.assertEqual(compare(r)['result'],'blocked_metadata_mismatch')
    def test_wrong_entity(self):
        r=self.sample();r['western_claim']['entity_id']='consolidated_group';self.assertEqual(compare(r)['result'],'blocked_metadata_mismatch')
    def test_gold_equivalent_not_gold(self):
        r=self.sample();r['western_claim']['metal']='Au_equivalent';self.assertEqual(compare(r)['result'],'blocked_metadata_mismatch')
    def test_missing_host_not_zero(self):
        r=self.sample();r['host_original_value']=None;self.assertEqual(compare(r)['result'],'missing_observation')
    def test_missing_component_not_zero(self):
        r=self.sample();r['western_claim']['components']=[None];self.assertEqual(compare(r)['result'],'missing_numeric_component')
    def test_scope_block_survives_numerical_agreement(self):
        r=self.sample();r['blocker']='partial_year';self.assertEqual(compare(r)['result'],'blocked_comparability')
    def test_unknown_unit_refused(self):
        with self.assertRaises(ValueError):conversion('avoirdupois_ounce','Au')
    def test_exact_rounding_boundary(self):
        r=self.sample();r['host_original_value']='100488';self.assertFalse(compare(r)['numeric_flag'])
        r['host_original_value']='100488.0001';self.assertTrue(compare(r)['numeric_flag'])
    def test_conversion_constants(self):
        self.assertEqual(conversion('oz','Au'),D('31.1034768'))
        self.assertEqual(conversion('oz','Ag'),D('0.0311034768'))
        self.assertEqual(conversion('thousand_lb','Cu'),D('0.45359237'))
    def test_provenance_required_even_for_flag(self):
        r=self.sample();r['host_original_value']='110000';r['strict_proof']={k:False for k in r['strict_proof']}
        self.assertFalse(compare(r)['confirmed_company_contradiction'])
    def test_frozen_denominator_and_no_duplicate_records(self):
        self.assertEqual(len(self.rows),100);self.assertEqual(len({r['record_id'] for r in self.rows}),100)
        self.assertEqual(sum(r['metal']=='Au' for r in self.rows),35)
if __name__=='__main__':unittest.main()
