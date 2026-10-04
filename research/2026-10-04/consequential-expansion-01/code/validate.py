import pathlib,json,unittest,collections,hashlib
P=pathlib.Path(__file__).resolve().parents[1]
jl=lambda n:[json.loads(x) for x in (P/n).read_text().splitlines()]
class ExpansionValidation(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.rows=jl('new-formulations.jsonl');c.by={r['test_id']:r for r in c.rows};c.sources={int(s['sys_id'][-4:]):s for s in jl('sources.jsonl')};c.screen=jl('candidate-screen.jsonl')
 def test_counts_no_refinement_inflation(self):self.assertEqual(len(self.screen),34);self.assertEqual(sum(r['kind']=='new_mechanism' for r in self.rows),12);self.assertEqual(sum(r['kind']=='existing_mechanism_refinement' for r in self.rows),4)
 def test_screen_coverage(self):
  selected={r['candidate_id'] for r in self.screen if r['disposition'].startswith('develop') or r['disposition']=='refinement_not_new'};self.assertEqual(selected,set(self.by));self.assertEqual(len(self.screen)-len(selected),18)
 def test_source_id_and_provenance_integrity(self):
  for r in self.rows:
   ids=r['primary_source_ids']+r['supporting_catalog_source_ids'];self.assertTrue(set(ids)<=set(self.sources));self.assertEqual([m['sys_id'] for m in r['source_manifest']],[self.sources[n]['sys_id'] for n in dict.fromkeys(ids)])
   for m in r['source_manifest']:self.assertEqual(m['block_sha256'],self.sources[int(m['sys_id'][-4:])]['block_sha256'])
 def test_declared_doc_references(self):
  docs={r['doc_id'] for r in jl('evidence/documentation.jsonl')}
  for r in self.rows:self.assertTrue(set(r['documentation_ids'])<=docs)
 def test_scope_extension_explicit(self):
  ex=json.loads((P/'supporting-scope-extensions.json').read_text());self.assertEqual(self.by['X03']['supporting_scope_extensions'],['ES01']);self.assertEqual(ex[0]['used_by'],['X03']);self.assertIn('outside',ex[0]['status'])
 def test_no_execution_promotion(self):
  for r in self.rows:self.assertFalse(r['positive_finding']);self.assertEqual(r['execution_status'],'not_executed');self.assertFalse(r['case_rule_applicability_verified']);self.assertFalse(r['pair_sufficient']);self.assertTrue(r['mandatory_evidence'])
 def test_rank_dimensions_separate_and_reproducible(self):
  for k in ['importance_rank','feasibility_rank','triage_rank']:self.assertEqual({r[k] for r in self.rows},set(range(1,17)))
  for r in self.rows:self.assertEqual(r['triage_score'],10*r['consequence_score']+3*r['feasibility_score']+2*r['join_route_score']-2*r['burden_tier']);self.assertLessEqual(r['feasibility_score'],2)
 def test_name_bridge_not_stable(self):
  for k in ['X01','X04','X05','X06']:self.assertEqual(self.by[k]['join_route_score'],1)
  self.assertIn('not an automatic',self.by['X01']['operational_join'])
 def test_cms_payment_recipient_semantics(self):
  r=self.by['X01'];self.assertIn('direct general',r['initial_observation']);self.assertIn('institutional',str(r['ordinary_explanations_and_falsifiers']));self.assertEqual(r['primary_source_ids'],[247,250])
 def test_waste_sender_receiver_and_no_absence_claim(self):
  r=self.by['X03'];self.assertEqual(r['primary_source_ids'],[218,38]);self.assertIn('Sender TRIFID is not the receiver RCRA ID',r['operational_join']);self.assertIn('absence of a RCRA permit',r['next_cheapest_check']);self.assertIn('annual',r['temporal_geographic_scope'].lower())
 def test_lobbying_historical_rule_guard(self):
  self.assertIn('old semiannual',self.by['X04']['temporal_geographic_scope']);self.assertIn('not current',self.by['X04']['temporal_geographic_scope'])
 def test_property_route_and_namespace(self):
  r=self.by['X13'];self.assertEqual(r['primary_source_ids'],[47,7]);self.assertIn('voluntary',r['initial_observation']);self.assertIn('ACN',r['operational_join']);self.assertIn('ABN',r['operational_join']);self.assertGreaterEqual(r['burden_tier'],4)
 def test_title_geography_and_history(self):
  r=self.by['X09'];self.assertEqual(r['primary_source_ids'],[288,309]);self.assertIn('Ontario',r['temporal_geographic_scope']);self.assertIn('not evidence',r['possible_finding_and_basis'])
 def test_assay_unit_of_observation(self):
  r=self.by['X12'];self.assertEqual(r['primary_source_ids'],[312,288]);self.assertIn('matrix',r['operational_join']);self.assertIn('method',r['operational_join']);self.assertIn('Detection-limit',str(r['ordinary_explanations_and_falsifiers']))
 def test_no_institutional_or_accounting_substitution(self):
  self.assertIn('accounting provision is not a bond',self.by['X08']['possible_finding_and_basis']);self.assertIn('not automatically one identical participant set',self.by['X11']['operational_join'])
 def test_refinements_and_legal_exceptions(self):
  self.assertEqual(self.by['REF-H01']['kind'],'existing_mechanism_refinement');self.assertIn('BESH',self.by['REF-H01']['temporal_geographic_scope']);self.assertIn('posting date',self.by['REF-H01']['next_cheapest_check']);self.assertIn('no active probes',self.by['REF-D01']['temporal_geographic_scope'])
 def test_no_exact_duplicate_fingerprints(self):self.assertEqual(len({r['semantic_key'] for r in self.rows}),16)
 def test_original_baseline_preserved(self):
  base=json.loads((P/'baseline-manifest.json').read_text());self.assertEqual(base['baseline_cards'],32);self.assertEqual(base['baseline_active_provisional_combinations'],1715);self.assertEqual(base['baseline_quarantines'],15)
if __name__=='__main__':unittest.main(verbosity=2)
