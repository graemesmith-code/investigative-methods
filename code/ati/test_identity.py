import json,pathlib,unittest
from make_plans import resolve_record,build_plans,validate_plan
OUT=pathlib.Path(__file__).resolve().parents[2]/'research/2026-10-01/ati-live'
class IdentityTests(unittest.TestCase):
 def test_same_number_different_departments_order_independent(self):
  rows=[{'owner_org':'dfatd-maecd','request_number':'A-2025-02382','pages':0},{'owner_org':'dnd-mdn','request_number':'A-2025-02382','pages':303}]
  for order in [rows,list(reversed(rows))]:self.assertEqual(resolve_record(order,'dnd-mdn','A-2025-02382')['pages'],303)
 def test_missing_and_duplicate_composite_fail_closed(self):
  row={'owner_org':'dnd-mdn','request_number':'same'}
  for rows in [[],[row,row]]:
   with self.assertRaises(ValueError):resolve_record(rows,'dnd-mdn','same')
 def test_all_selected_plans_match_corpus(self):
  rows=json.loads((OUT/'full-ranked.json').read_text());plans=build_plans(rows)
  self.assertEqual(len(plans),13)
  for plan in plans:validate_plan(plan,rows)
  audit=next(p for p in plans if p['lead']=='audit-medical-fairness')
  self.assertEqual((audit['owner_org'],audit['pages'],audit['disposition'],audit['rank_score']),('dnd-mdn',303,'DP',1.524))
 def test_original_misattribution_rejected(self):
  rows=json.loads((OUT/'full-ranked.json').read_text())
  original=next(p for p in json.loads((OUT/'coverage-plans-original.json').read_text()) if p['lead']=='audit-medical-fairness')
  with self.assertRaises(ValueError):validate_plan(original,rows)
  original['owner_org']='dnd-mdn'
  with self.assertRaises(ValueError):validate_plan(original,rows)
 def test_missing_owner_rejected(self):
  with self.assertRaises(KeyError):validate_plan({'request_number':'A-2025-02382'},[])
