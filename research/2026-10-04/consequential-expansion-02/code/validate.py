import json,pathlib,unittest,copy,hashlib
from bid_compare import compare
from inventory_time import overlaps_established_presence
P=pathlib.Path(__file__).resolve().parents[1]
def jl(n):return [json.loads(x) for x in (P/n).read_text().splitlines()]
class ArtifactChecks(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.cards=jl('cards.jsonl');c.by={r['test_id']:r for r in c.cards};c.gaps=jl('predicate-coverage.jsonl');c.sources={s['sys_id']:s for s in jl('sources.jsonl')}
 def test_counts_and_pending_not_screened(self):
  self.assertEqual(len(self.cards),5);self.assertEqual(sum(r['kind']=='proposed_new' for r in self.cards),4);self.assertEqual(sum(g['status']=='queued_unexamined' for g in self.gaps),8);self.assertEqual(len(self.gaps),24)
 def test_all_sources_preserved_and_coverage_honest(self):
  rows=jl('source-coverage.jsonl');self.assertEqual(len(rows),344);self.assertEqual({r['sys_id'] for r in rows},set(self.sources));self.assertEqual(sum(bool(r['this_pass_gap_ids']) for r in rows),54)
 def test_original_provenance_preserved(self):
  for r in self.cards:
   for s in r['source_manifest']:
    orig=self.sources[s['sys_id']]
    for k in ['all_ap_ids','block_sha256','line_start','line_end','file','join_fields']:self.assertEqual(s[k],orig[k])
 def test_docs_resolve(self):
  ids={r['doc_id'] for r in jl('evidence/documentation.jsonl')}
  for r in self.cards:self.assertTrue(set(r['documentation_ids'])<=ids)
 def test_no_feasibility_or_findings_promotion(self):
  for r in self.cards:
   self.assertFalse(r['positive_finding']);self.assertFalse(r['complete_route_feasible']);self.assertFalse(r['case_legal_applicability_verified']);self.assertEqual(r['execution_status'],'not_executed');self.assertLessEqual(r['testability'],2)
 def test_rank_reproducible(self):
  for r in self.cards:self.assertEqual(r['score'],10*r['consequence']+3*r['testability']+2*r['join_route']-2*r['cost_tier'])
  for k in ['priority_rank','testability_rank','consequence_rank']:self.assertEqual({r[k] for r in self.cards},set(range(1,6)))
 def test_sample_is_not_conflicting_pair(self):
  r=jl('evidence/sample-observations.jsonl')[0];self.assertFalse(r['matched_second_agreement']);self.assertFalse(r['positive_finding'])
 def test_inventory_not_population(self):
  r=self.by['Z02'];self.assertIn('cannot establish occupancy',r['logical_or_legal_basis']);self.assertIn('exact claimed date',r['expected_observation']);self.assertIn('cannot resolve',r['next_cheapest_check'])
 def test_ad_exact_product_and_context(self):
  r=self.by['Z03'];self.assertIn('Ingredient alone is not',r['operational_join']);self.assertIn('Canadian',r['timing_geography']);self.assertIn('prescribing',str(r['ordinary_explanations_and_disqualifiers']))
 def test_licence_scope_and_credential_gate(self):
  r=self.by['Z04'];self.assertIn('field',r['initial_observation']);self.assertIn('territory',r['initial_observation']);self.assertIn('master licence',str(r['ordinary_explanations_and_disqualifiers']));self.assertIn('requires credentials',r['access_evidence'])
 def test_procurement_scope_and_nonprice_guard(self):
  r=self.by['Z01'];self.assertIn('project ID alone cannot match',r['operational_join']);self.assertIn('Nonprice',str(r['ordinary_explanations_and_disqualifiers']));self.assertIn('not a finding of rigging',r['logical_or_legal_basis'])
 def test_prior_corrections_applied(self):
  baseline=json.loads((P/'baseline.json').read_text());self.assertEqual(baseline['prior_non_refinement_detailed_cards'],44)
  old={r['test_id']:r for r in map(json.loads,(P.parent/'consequential-expansion-01/new-formulations.jsonl').read_text().splitlines())}
  for k in ['X01','X10']:self.assertEqual(old[k]['kind'],'existing_mechanism_refinement')
  self.assertIn('no outstanding liabilities',old['X13']['possible_finding_and_basis']);self.assertIn('mortgage',old['X13']['possible_finding_and_basis']);self.assertIn('N06',old['X14']['novelty_vs_baseline'])
 def test_no_exact_duplicates(self):self.assertEqual(len({r['exact_fingerprint'] for r in self.cards}),5)
class SyntheticBidArithmeticChecks(unittest.TestCase):
 def setUp(self):
  self.items=[dict(id='a',unit='m',q0=100,q1=1),dict(id='b',unit='m',q0=1,q1=100)]
  self.bids=[dict(id=i,eligible=True,revised_basket_equivalence_confirmed=True,quantity_pricing_confirmed=True,fixed_charges_accounted=True,specifications_equivalent=True,performance_comparable=True,rate_adjustments_accounted=True,prices={k:dict(rate=v,unit='m',currency='USD') for k,v in zip(['a','b'],rates)}) for i,rates in [('winner',[1,10]),('rival',[2,2])]]
 def test_reversal_arithmetic(self):
  r=compare(self.items,self.bids,'winner','USD');self.assertTrue(r['price_rank_reversal']);self.assertEqual(r['totals'][0]['original'],'110');self.assertEqual(r['totals'][0]['revised'],'1001');self.assertEqual(r['totals'][1]['revised'],'202')
 def test_missing_price_rejected(self):
  del self.bids[1]['prices']['a']
  with self.assertRaises(ValueError):compare(self.items,self.bids,'winner','USD')
 def test_unit_currency_mismatch_rejected(self):
  self.bids[1]['prices']['a']['unit']='km'
  with self.assertRaises(ValueError):compare(self.items,self.bids,'winner','USD')
 def test_noncomparable_or_ineligible_rival_rejected(self):
  self.bids[1]['eligible']=False
  with self.assertRaises(ValueError):compare(self.items,self.bids,'winner','USD')
 def test_no_original_advantage_not_reversal(self):
  r=compare(self.items,self.bids,'rival','USD');self.assertFalse(r['winner_had_original_lowest_price']);self.assertFalse(r['price_rank_reversal'])
 def test_initial_tie_is_not_strict_reversal(self):
  self.items[0]['q0']=1;self.items[1]['q0']=1;self.items[0]['q1']=1;self.items[1]['q1']=2
  self.bids[0]['prices']['a']['rate']=1;self.bids[0]['prices']['b']['rate']=3
  r=compare(self.items,self.bids,'winner','USD');self.assertFalse(r['price_rank_reversal']);self.assertTrue(r['initial_tie_to_loss']);self.assertEqual(r['comparisons'][0]['original_rival_minus_winner'],'0');self.assertEqual(r['comparisons'][0]['revised_rival_minus_winner'],'-1');self.assertEqual(len(r['comparisons'][0]['item_contributions']),2)
 def test_unresolved_fixed_charges_rejected(self):
  self.bids[1]['fixed_charges_accounted']=False
  with self.assertRaises(ValueError):compare(self.items,self.bids,'winner','USD')
 def test_nonfinite_rejected(self):
  self.items[0]['q1']='NaN'
  with self.assertRaises(ValueError):compare(self.items,self.bids,'winner','USD')
class SyntheticTemporalChecks(unittest.TestCase):
 def test_old_image_is_not_presence_at_cutoff(self):self.assertFalse(overlaps_established_presence('2020-06-01','2020-06-01','2020-01-01','2020-01-01'))
 def test_same_date_presence(self):self.assertTrue(overlaps_established_presence('2020-06-01','2020-06-01','2020-06-01','2020-06-01'))
 def test_claimed_interval_requires_overlap(self):self.assertTrue(overlaps_established_presence('2020-01-01','2020-06-01','2020-03-01','2020-03-01'))
if __name__=='__main__':unittest.main(verbosity=2)
