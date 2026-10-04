import unittest,json,pathlib
P=pathlib.Path(__file__).resolve().parents[1];ROOT=P.parent
jl=lambda p:[json.loads(x) for x in p.read_text().splitlines()]
def resolve(ref):
 path=ROOT/ref['file']
 if not path.resolve().is_relative_to(ROOT.resolve()):raise ValueError('outside evidence root')
 rows=[d for d in jl(path) if d['doc_id']==ref['doc_id']]
 if len(rows)!=1:raise ValueError('unresolved/ambiguous evidence')
 return rows[0]
class References(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.rows=jl(ROOT/'consequential-expansion-07/cross-batch-ranked-routes.jsonl');c.by={r['test_id']:r for r in c.rows}
 def test_no_unqualified_inherited_refs(self):
  for r in self.rows:self.assertNotIn('current_batch_applicable_evidence_ids',r)
 def test_all_resolve_with_route_source(self):
  for r in self.rows:
   for ref in r['applicable_evidence_refs']:
    self.assertTrue(resolve(ref)['url'].startswith('https://'));self.assertTrue(set(ref['supporting_source_ids'])<=set(r['route_source_ids']))
 def test_B01_exact_eia_support(self):
  ref=self.by['B01']['applicable_evidence_refs'][0];self.assertEqual(ref['supporting_source_ids'],[255]);self.assertEqual(resolve(ref)['url'],'https://api.eia.gov/v2/electricity/facility-fuel/')
 def test_B02_exact_worldbank_support(self):
  ref=self.by['B02']['applicable_evidence_refs'][0];self.assertEqual(ref['supporting_source_ids'],[145]);self.assertIn('P163533-',resolve(ref)['url']);self.assertIn('invoice/settlement',resolve(ref)['observation'])
 def test_same_id_different_batch_does_not_alias(self):
  a=resolve(dict(file='consequential-expansion-06/evidence/documentation.jsonl',doc_id='D07'));b=resolve(dict(file='consequential-expansion-07/evidence/documentation.jsonl',doc_id='D07'));self.assertNotEqual(a['url'],b['url'])
 def test_missing_id_rejected(self):
  with self.assertRaises(ValueError):resolve(dict(file='consequential-expansion-06/evidence/documentation.jsonl',doc_id='D99'))
 def test_card_documentation_refs(self):
  for c in jl(ROOT/'consequential-expansion-07/cards.jsonl'):
   self.assertEqual([r['doc_id'] for r in c['documentation_refs']],c['documentation_ids'])
   for r in c['documentation_refs']:self.assertTrue(resolve(r)['url'])
 def test_accepted_counts_and_inherency(self):
  cs=jl(ROOT/'consequential-expansion-07/cards.jsonl');self.assertEqual(sum(c['kind']=='reviewed_new' for c in cs),2);j=next(c for c in cs if c['test_id']=='J02');self.assertIn('inherent disclosure',j['expected_observation']);self.assertIn('without assembling missing elements',j['expected_observation'])
 def test_rank_no_changes_from_fix(self):
  self.assertEqual(len(self.rows),70);self.assertEqual(self.rows,sorted(self.rows,key=lambda r:(r['readiness_tier'],r['effort_tier'],r['test_id'])));self.assertEqual(self.by['N01']['applicable_evidence_refs'],[])
class SampleEvidence(unittest.TestCase):
 def test_current08_refs_and_ranking(self):
  rows=jl(P/'cross-batch-ranked-routes.jsonl');self.assertEqual(len(rows),70);counts=json.loads((P/'counts.json').read_text());self.assertEqual(counts['well_identity_records_verified'],0);self.assertEqual(counts['historical_trial_versions_verified'],0)
  self.assertEqual(rows,sorted(rows,key=lambda r:(r['readiness_tier'],r['effort_tier'],r['test_id'])))
  for r in rows:
   for ref in r['applicable_evidence_refs']+r['sample_access_refs']:self.assertTrue(resolve(ref)['url'])
  by={r['test_id']:r for r in rows};self.assertEqual(by['J01']['effort_tier'],3);self.assertFalse(any(r['full_case_feasible'] for r in rows))
 def test_history_dates_not_conflated(self):
  rs=jl(P/'evidence/browser-probes.jsonl');r=next(x for x in rs if x.get('label')=='ct-one-history' and 'observed_fields' in x);f=r['observed_fields'];self.assertFalse(r['usable_as_verified_evidence']);self.assertEqual(r['evidence_status'],'quarantined_certificate_validation_bypassed');self.assertEqual(f['version_submitted_date'],'2005-06-23');self.assertNotEqual(f['first_posted'][:10],f['version_submitted_date']);self.assertFalse(f['public_availability_legally_established'])
 def test_selected_well_not_operation_evidence(self):
  r=next(x for x in jl(P/'evidence/browser-probes.jsonl') if x.get('label')=='aer-well-record-selection-attempt');self.assertFalse(r['usable_as_verified_evidence']);self.assertTrue(r['form_entry_completed']);self.assertEqual(r['observed_fields']['licence'],'0466075');self.assertFalse(r['observed_fields']['operation_dates_obtained']);self.assertFalse(r['observed_fields']['consent_obtained'])
 def test_archive_empty_not_absence_claim(self):
  self.assertEqual(json.loads((P/'evidence/safe-media-availability.json').read_text())['archived_snapshots'],{});r=next(x for x in jl(P/'route-checks.jsonl') if x['test_id']=='J01');self.assertFalse(r['full_case_feasible'])
if __name__=='__main__':unittest.main(verbosity=2)
