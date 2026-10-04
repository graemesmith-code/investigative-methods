import pathlib,json,unittest,collections
P=pathlib.Path(__file__).resolve().parents[1]
jl=lambda n:[json.loads(x) for x in (P/n).read_text().splitlines()]
class PriorityArtifactChecks(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.cards=jl('cards.jsonl');c.by={r['test_id']:r for r in c.cards};c.rows=jl('priority-subchecks.jsonl');c.sources={r['sys_id']:r for r in jl('sources.jsonl')}
 def test_eight_priorities_three_explicit_subchecks(self):
  self.assertEqual(set(r['prior_gap'] for r in self.rows),{'G16','G17','G18','G19','G20','G21','G22','G23'});self.assertEqual(set(collections.Counter(r['priority'] for r in self.rows).values()),{3});self.assertEqual(len(self.rows),24)
 def test_new_and_refinement_counts(self):self.assertEqual(collections.Counter(r['kind'] for r in self.cards),{'proposed_new':2,'refinement':5})
 def test_selected_rows_match_cards(self):self.assertEqual({r['card_or_baseline'] for r in self.rows if r['disposition'] in ['new_card','refinement_card']},set(self.by))
 def test_all_sources_and_provenance(self):
  self.assertEqual(len(self.sources),344)
  for r in self.cards:
   for s in r['source_manifest']:
    for k,v in s.items():self.assertEqual(v,self.sources[s['sys_id']][k])
 def test_documentation_references(self):
  ids={x['doc_id'] for x in jl('evidence/documentation.jsonl')}
  for r in self.cards:self.assertTrue(set(r['documentation_ids'])<=ids)
 def test_rank_formula_and_separate_dimensions(self):
  for r in self.cards:self.assertEqual(r['score'],10*r['consequence']+3*r['testability']+2*r['join_route']-2*r['cost_tier'])
  for k in ['priority_rank','testability_rank','consequence_rank']:self.assertEqual({r[k] for r in self.cards},set(range(1,8)))
 def test_no_feasibility_or_legal_promotion(self):
  for r in self.cards:self.assertFalse(r['positive_finding']);self.assertFalse(r['complete_route_feasible']);self.assertFalse(r['case_legal_applicability']);self.assertEqual(r['execution_status'],'not_executed');self.assertLessEqual(r['testability'],2)
 def test_dormancy_and_return_gates(self):
  r=self.by['Q01'];self.assertIn('dormant status alone',r['next_cheapest_check']);self.assertIn('returned',r['join']);self.assertIn('failed',r['access_evidence'])
 def test_charity_identity_and_historical_status(self):
  r=self.by['Q02'];self.assertIn('employer text is not donor',r['join']);self.assertIn('not historical proof',r['timing_geography']);self.assertIn('not a shared namespace',r['join']);self.assertEqual(r['join_route'],1)
 def test_guarantee_perimeter_and_instrument(self):
  r=self.by['Q03'];self.assertIn('No blanket',r['basis']);self.assertIn('operative guarantee',r['timing_geography']);self.assertIn('intergovernmental',r['access_evidence']);self.assertIn('all incorporated',r['then_expected'])
 def test_consent_not_name_change(self):self.assertIn('Share sale not covered',str(self.by['REF-CONS']['ordinary_explanations_and_disqualifiers']))
 def test_outage_not_market_manipulation(self):
  r=self.by['REF-OUT'];self.assertIn('does not by itself prove manipulation',r['basis']);self.assertIn('production/generation-unit hierarchy',r['join'])
 def test_compensation_escrow_and_claim_identity(self):
  r=self.by['REF-COMP'];self.assertIn('approved escrow',r['then_expected']);self.assertIn('claimant or parcel ID',r['join']);self.assertIn('not evidence of availability',r['next_cheapest_check'])
 def test_maintenance_not_promoted(self):
  rr=[r for r in self.rows if r['priority']=='maintenance_certifications'];self.assertTrue(all(r['disposition'] in ['defer','refinement_deferred'] for r in rr));self.assertIn('component serial',str(rr))
 def test_access_failure_not_absence(self):
  failed=[r for r in jl('evidence/access-log.jsonl') if r['status']=='failed'];self.assertEqual(len(failed),1);self.assertIn('not legal repeal or absence',failed[0]['interpretation'])
 def test_prior_review_counts_preserved(self):
  old=P.parent/'consequential-expansion-01';r=list(map(json.loads,(old/'new-formulations.jsonl').read_text().splitlines()));self.assertEqual(sum(x['kind']=='new_mechanism' for x in r),12);self.assertEqual(sum(x['kind']=='existing_mechanism_refinement' for x in r),4)
  c=json.loads((P.parent/'consequential-expansion-02/review-corrections.json').read_text());self.assertEqual(c['cumulative_non_refinement_cards'],48)
if __name__=='__main__':unittest.main(verbosity=2)
