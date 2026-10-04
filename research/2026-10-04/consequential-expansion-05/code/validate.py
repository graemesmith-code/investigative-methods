import pathlib,json,unittest,collections
from bounds import energy_check,recovery_check
P=pathlib.Path(__file__).resolve().parents[1]
jl=lambda name:[json.loads(x) for x in (P/name).read_text().splitlines()]
class Artifacts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.cards=jl('cards.jsonl');cls.screen=jl('candidate-screen.jsonl')
 def test_counts(self):
  self.assertEqual(len(self.screen),24);self.assertEqual(collections.Counter(c['kind'] for c in self.cards),{'proposed_new':2,'refinement':1})
 def test_six_lenses(self):self.assertEqual(sorted(collections.Counter(r['lens'] for r in self.screen).values()),[4]*6)
 def test_unique_dispositions(self):
  self.assertEqual(len({r['candidate_id'] for r in self.screen}),24)
  self.assertEqual(collections.Counter(r['disposition'] for r in self.screen),{'new':2,'reject':7,'defer':4,'refinement_deferred':7,'refinement':1,'repeat':3})
 def test_provenance(self):
  ss={s['sys_id']:s for s in jl('sources.jsonl')};self.assertEqual(len(ss),344)
  for c in self.cards:
   for s in c['source_manifest']:
    for k,v in s.items():self.assertEqual(ss[s['sys_id']][k],v)
 def test_no_unearned_feasibility(self):
  b=next(c for c in self.cards if c['test_id']=='B01');self.assertIn('exact output, input or efficiency',b['initial_observation']);self.assertIn('reporting-quality lead',b['expected_observation'])
  for c in self.cards:self.assertFalse(c['complete_route_feasible']);self.assertFalse(c['positive_finding']);self.assertFalse(c['case_rule_applicability_verified'])
 def test_doc_references(self):
  ids={d['doc_id'] for d in jl('evidence/documentation.jsonl')}
  for c in self.cards:self.assertTrue(set(c['documentation_ids'])<=ids)
  self.assertEqual(len(jl('evidence/access-log.jsonl')),2)
 def test_ranks(self):
  for c in self.cards:self.assertEqual(c['score'],10*c['consequence']+3*c['testability']+2*c['join_route']-2*c['cost_tier'])
  for k in ['priority_rank','testability_rank','consequence_rank']:self.assertEqual({c[k] for c in self.cards},{1,2,3})
 def test_coverage_is_candidate_coverage(self):
  rows=jl('source-coverage.jsonl');self.assertEqual(len(rows),344)
  actual={int(s['sys_id'][-4:]) for s in rows if s['candidate_ids']}
  self.assertEqual(actual,{s for r in self.screen for s in r['source_ids']})
class ArithmeticIllustrations(unittest.TestCase):
 def setUp(self):
  self.eg=dict(boundary_complete=True,imports_storage_resolved=True,measurement_bounds_verified=True)
  self.rg=dict(permitted_recovery_upper='100',currency='USD',same_cost_verified=True,cost_cap_verified=True,flow_independence_verified=True,measurement_bounds_verified=True)
  self.pay=lambda key,value:dict(canonical_settlement=key,kind='completed_net_cost_recovery',currency='USD',net_recovery_lower=value)
 def test_energy_normal_no_flag(self):self.assertFalse(energy_check(output_lower_mwh=100,input_upper_mmbtu=1000,**self.eg)['unresolved_balance_flag'])
 def test_energy_clear_excess(self):self.assertTrue(energy_check(output_lower_mwh=400,input_upper_mmbtu=1000,**self.eg)['unresolved_balance_flag'])
 def test_energy_unknown_imports_rejected(self):
  self.eg['imports_storage_resolved']=False
  with self.assertRaises(ValueError):energy_check(output_lower_mwh=400,input_upper_mmbtu=1000,**self.eg)
 def test_energy_conservative_rounding(self):self.assertFalse(energy_check(output_lower_mwh='293',input_upper_mmbtu='1000.5',**self.eg)['unresolved_balance_flag'])
 def test_permitted_cofinancing_no_flag(self):self.assertFalse(recovery_check([self.pay('A',60),self.pay('B',40)],**self.rg)['unresolved_excess_flag'])
 def test_independent_recoveries_exceed(self):self.assertTrue(recovery_check([self.pay('A',70),self.pay('B',60)],**self.rg)['unresolved_excess_flag'])
 def test_mirrored_settlement_rejected(self):
  with self.assertRaises(ValueError):recovery_check([self.pay('A',70),self.pay('A',70)],**self.rg)
 def test_advance_not_recovery(self):
  p=self.pay('A',120);p['kind']='advance'
  with self.assertRaises(ValueError):recovery_check([p],**self.rg)
 def test_currency_mismatch_rejected(self):
  p=self.pay('A',120);p['currency']='EUR'
  with self.assertRaises(ValueError):recovery_check([p],**self.rg)
 def test_unknown_pass_through_rejected(self):
  self.rg['flow_independence_verified']=False
  with self.assertRaises(ValueError):recovery_check([self.pay('A',70),self.pay('B',70)],**self.rg)
 def test_combined_cap_below_invoice_cost(self):
  # Invoice face amount100 is NOT the combined permitted-recovery cap60.
  self.rg['permitted_recovery_upper']='60'
  self.assertTrue(recovery_check([self.pay('A',40),self.pay('B',30)],**self.rg)['unresolved_excess_flag'])
if __name__=='__main__':unittest.main(verbosity=2)
