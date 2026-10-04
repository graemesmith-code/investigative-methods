import unittest,pathlib,json,sys,collections
P=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P/'code/generator'))
import build
load=lambda f:[json.loads(x) for x in (P/f).read_text().splitlines()]
class ProductionIntegration(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.rows=load('candidate-inventory.jsonl');c.sources={s['sys_id']:s for s in load('sources.jsonl')};c.reviews=load('reviewed-recipes.jsonl');c.probes=load('evidence/probes.jsonl')
 def test_count_accounting(self):
  self.assertEqual(len(self.rows),1730); self.assertEqual(len(load('rejected.jsonl')),805);self.assertEqual(len(self.sources),344)
 def test_name_only_docs_do_not_promote(self):
  a=self.sources['SYS-0024'];b=self.sources['SYS-0054'];self.assertEqual(build.ranking_dimensions(a,b,'name_or_role_provisional',1,2,'free')[0],1)
 def test_paris_authorization_cost_gate(self):
  self.assertGreaterEqual(build.ranking_dimensions(self.sources['SYS-0024'],self.sources['SYS-0074'],'direct_identifier_conditional',4,2,'free')[1],3)
 def test_emitted_ranking_uses_production(self):
  for r in self.rows:
   if r['join_confidence_score']<3:self.assertEqual(r['testability_score'],1)
   self.assertGreaterEqual(r['cost_tier'],2)
 def test_f02_direction(self):
  rows=[r for r in self.rows if r['mechanism']=='F02'];self.assertTrue(rows)
  for r in rows:self.assertIn('non-EU reporter in UN Comtrade',r['initial_observation']);self.assertIn('EU-member-reported Comext',r['expected_observation'])
 def test_no_execution_promotion(self):
  for r in self.rows:self.assertEqual(r['design_validation'],'mechanically_screened_candidate_not_individually_reviewed')
  for r in self.reviews:self.assertFalse(r['bulk_investigative_execution']);self.assertTrue(r['mandatory_auxiliary_inputs'])
 def test_review_links_exist(self):
  ids={r['test_id'] for r in self.rows}
  for r in self.reviews:
   if not r['base_recipe_id'].startswith('NEW'):self.assertIn(r['base_recipe_id'],ids)
 def test_evidence_references_exist(self):
  docs={r['doc_id'] for r in load('evidence/documentation.jsonl')};labels={r['label'] for r in self.probes}
  for r in self.reviews:
   self.assertTrue(set(r['evidence_doc_ids'])<=docs);self.assertTrue(set(r['sample_labels'])<=labels)
 def test_review_diversity(self):
  counts=collections.Counter(r['base_recipe_id'].split('-')[1] if r['base_recipe_id'].startswith('T-') else r['base_recipe_id'] for r in self.reviews)
  self.assertGreaterEqual(len(counts),16);self.assertLessEqual(max(counts.values()),2)
 def test_probes_bounded(self):
  for r in self.probes:self.assertLessEqual(r.get('bytes_read',0),256000)
 def test_omitted_honesty(self):
  import csv
  rows=list(csv.DictReader((P/'omitted-source-review.csv').read_text().splitlines()));self.assertEqual(len(rows),139);self.assertEqual(sum(r['review_depth']=='source_specific_reasoning' for r in rows),31)
 def test_samples_have_hashes(self):
  import hashlib
  for r in self.probes:
   if r.get('file'):self.assertEqual(hashlib.sha256((P/r['file']).read_bytes()).hexdigest(),r['sha256'])
if __name__=='__main__':unittest.main(verbosity=2)
