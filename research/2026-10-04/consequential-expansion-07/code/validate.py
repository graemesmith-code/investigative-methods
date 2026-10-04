import pathlib,json,unittest,collections
from media_chronology import check
P=pathlib.Path(__file__).resolve().parents[1];jl=lambda n:[json.loads(x) for x in (P/n).read_text().splitlines()]
class Artifacts(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.cards=jl('cards.jsonl');c.by={r['test_id']:r for r in c.cards}
 def test_counts(self):self.assertEqual(collections.Counter(r['kind'] for r in self.cards),{'reviewed_new':2,'refinement':1});self.assertEqual(len(jl('candidate-screen.jsonl')),9)
 def test_manifest(self):
  ss={s['sys_id']:s for s in jl('sources.jsonl')};self.assertEqual(len(ss),344)
  for c in self.cards:
   for s in c['source_manifest']:
    for k,v in s.items():self.assertEqual(ss[s['sys_id']][k],v)
 def test_all_document_ids(self):
  ids={d['doc_id'] for d in jl('evidence/documentation.jsonl')}
  for c in self.cards:self.assertTrue(set(c['documentation_ids'])<=ids)
 def test_no_execution_claim(self):
  for c in self.cards:self.assertFalse(c['complete_route_feasible']);self.assertFalse(c['positive_finding']);self.assertFalse(c['case_rule_applicability_verified'])
 def test_patent_specificity(self):
  r=self.by['J02'];self.assertIn('single-reference',r['mandatory_evidence'][3]);self.assertIn('no universal NCT-to-patent',r['operational_join']);self.assertIn('specialist',r['expected_observation'])
 def test_aer_scope_and_magnitude(self):
  r=self.by['REF-AER'];self.assertIn('not all Alberta',r['temporal_geographic_scope']);self.assertIn('preferred magnitude may be Mw',r['operational_join']);self.assertIn('unindexed consent is not proof',r['next_cheapest_check'])
 def test_rank_integrity(self):
  rs=jl('cross-batch-ranked-routes.jsonl');self.assertEqual(len(rs),70);self.assertEqual(len({r['test_id'] for r in rs}),70);self.assertEqual(rs,sorted(rs,key=lambda r:(r['readiness_tier'],r['effort_tier'],r['test_id'])))
  by={r['test_id']:r for r in rs};self.assertEqual(by['N01']['readiness_tier'],3);self.assertEqual(by['N01']['original_testability'],1)
  for c in self.cards:self.assertEqual(by[c['test_id']]['readiness_tier'],3)
 def test_external_support_not_invented_SYS(self):
  for r in json.loads((P/'supporting-scope-extensions.json').read_text()):self.assertIsNone(r['rabbit_sys_id']);self.assertEqual(r['records_retrieved'],0)
class SyntheticChronology(unittest.TestCase):
 def setUp(self):self.kw=dict(media_capture_upper='2020-01-01T00:00:00Z',event_lower='2020-02-01T00:00:00Z',media_response_authenticated=True,original_media_verified=True,explicit_event_capture_attribution=True,media_role='capture_of_this_event')
 def test_exact_pre_event_flag_limited(self):
  r=check(b'synthetic-media',b'synthetic-media',**self.kw);self.assertTrue(r['attribution_review_flag']);self.assertFalse(r['whole_incident_disproved']);self.assertFalse(r['evidence_authentication_performed_by_helper'])
 def test_same_url_different_payload_no_flag(self):self.assertFalse(check(b'old-media',b'new-media',**self.kw)['attribution_review_flag'])
 def test_wrapper_without_media_authentication_rejected(self):
  self.kw['media_response_authenticated']=False
  with self.assertRaises(ValueError):check(b'media',b'media',**self.kw)
 def test_portrait_use_rejected(self):
  self.kw['media_role']='portrait'
  with self.assertRaises(ValueError):check(b'media',b'media',**self.kw)
 def test_equal_time_not_strictly_pre_event(self):
  self.kw['event_lower']=self.kw['media_capture_upper'];self.assertFalse(check(b'media',b'media',**self.kw)['attribution_review_flag'])
 def test_naive_time_rejected(self):
  self.kw['media_capture_upper']='2020-01-01T00:00:00'
  with self.assertRaises(ValueError):check(b'media',b'media',**self.kw)
if __name__=='__main__':unittest.main(verbosity=2)
