import unittest,json,pathlib,importlib.util
P=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('reconcile_major',P/'reconcile_major.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class OriginalRegression(unittest.TestCase):
 def test_originals_exist(self):
  rows=json.loads((P/'major-original-reconciliation.json').read_text())
  for c in rows:
   self.assertFalse(c['missing_originals'])
   for e in c['events']:self.assertTrue((P.parent.parent.parent/e['original_file']).exists())
 def test_gotion_amounts_and_amendments(self):
  rows=json.loads((P/'major-original-reconciliation.json').read_text());c=next(c for c in rows if c['client_id']==59928)
  self.assertEqual(c['annual_numeric_lower_bounds_2025']['expenses'],'2459072.00');self.assertEqual(len(c['latest_2025_forms']),4)
  self.assertTrue(all(x['matches_api'] for x in c['latest_2025_forms']))
 def test_pdf_metadata_is_not_checkbox(self):
  c=next(c for c in json.loads((P/'major-original-reconciliation.json').read_text()) if c['client_id']==158453)
  for e in c['events']:self.assertNotIn('registration_section14_response',e)
  manual=json.loads((P/'manual-image-review.json').read_text())['reviews'];self.assertEqual(next(e for e in manual if e['uuid']=='15b1e8df-cd1c-4820-902a-65da4da5fc7e')['original_section14'],'No')
 def test_exact_original_not_current_label(self):
  c=next(c for c in json.loads((P/'major-original-reconciliation.json').read_text()) if c['client_id']==125608)
  self.assertIn('AMERICAN HONDA',c['current_api_client_label']);self.assertIn('Honda North America',c['events'][0]['original_text'])
if __name__=='__main__':unittest.main()
