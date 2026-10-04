import pathlib,json,unittest,zipfile,hashlib
from lower_bound import concentration_lower_bound
P=pathlib.Path(__file__).resolve().parents[1];jl=lambda n:[json.loads(x) for x in (P/n).read_text().splitlines()]
class ArtifactChecks(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.cards=jl('cards.jsonl');c.by={r['test_id']:r for r in c.cards}
 def test_conservative_counts(self):self.assertEqual(len(jl('candidate-screen.jsonl')),12);self.assertEqual(sum(c['kind']=='proposed_new' for c in self.cards),1);self.assertEqual(sum(c['kind']=='refinement' for c in self.cards),3)
 def test_metadata_integrity(self):
  raw=(P/'evidence/cvm-cda-dictionary.zip').read_bytes();m=json.loads((P/'evidence/metadata-download.json').read_text());self.assertEqual(len(raw),10094);self.assertEqual(hashlib.sha256(raw).hexdigest(),m['sha256'])
  with zipfile.ZipFile(P/'evidence/cvm-cda-dictionary.zip') as z:self.assertIsNone(z.testzip())
 def test_block_specific_identifiers(self):
  rs=jl('evidence/cvm-fields.jsonl');by={f:{r['field'] for r in rs if r['file']==f} for f in {r['file'] for r in rs}}
  self.assertIn('CNPJ_EMISSOR',by['meta_cda_fi_BLC_5.txt']);self.assertIn('CD_ISIN',by['meta_cda_fi_BLC_4.txt']);self.assertNotIn('CD_ISIN',by['meta_cda_fi_BLC_5.txt']);self.assertIn('VL_PATRIM_LIQ',by['meta_cda_fi_PL.txt'])
 def test_provenance_344(self):
  ss={r['sys_id']:r for r in jl('sources.jsonl')};self.assertEqual(len(ss),344)
  for c in self.cards:
   for s in c['source_manifest']:
    for k,v in s.items():self.assertEqual(ss[s['sys_id']][k],v)
 def test_no_execution_promotion(self):
  for c in self.cards:self.assertFalse(c['positive_finding']);self.assertFalse(c['complete_route_feasible']);self.assertFalse(c['case_rule_applicability_verified']);self.assertEqual(c['execution_status'],'not_executed')
 def test_documents_and_ranks(self):
  ids={r['doc_id'] for r in jl('evidence/documentation.jsonl')}
  for c in self.cards:self.assertTrue(set(c['documentation_ids'])<=ids);self.assertEqual(c['score'],10*c['consequence']+3*c['testability']+2*c['join_route']-2*c['cost_tier'])
  for k in ['priority_rank','testability_rank','consequence_rank']:self.assertEqual({c[k] for c in self.cards},{1,2,3,4})
 def test_confidentiality_and_acquisition_scope(self):
  r=self.by['V01'];self.assertIn('never proves compliance',r['basis']);self.assertIn('acquisition-time cap',r['temporal_geographic_scope']);self.assertIn('no holdings were downloaded',r['access_evidence'])
 def test_search_methods_not_results(self):
  r=self.by['REF-SEARCH'];self.assertIn('does not establish legal inadequacy',r['basis']);self.assertIn('not automatically',r['operational_join']);self.assertIn('older public document does not',r['temporal_geographic_scope'])
 def test_evidence_dependence_unknown(self):self.assertIn('dependence unknown',self.by['REF-EVID']['next_cheapest_check']);self.assertEqual(self.by['REF-EVID']['kind'],'refinement')
class SyntheticLowerBoundChecks(unittest.TestCase):
 def setUp(self):
  self.kw=dict(fund_class='F',date='2020-01-31',issuer_group='G',currency='BRL',denominator='100',cap_fraction='.1',additive_nonnegative_measure_confirmed=True,denominator_verified=True,mandate_timing_and_exceptions_resolved=True)
  self.ps=[dict(position_id='p1',fund_class='F',date='2020-01-31',issuer_group='G',currency='BRL',measured_exposure='12')]
 def test_positive_bound(self):self.assertTrue(concentration_lower_bound(self.ps,**self.kw)['lower_bound_exceeds'])
 def test_low_bound_not_compliance(self):
  self.ps[0]['measured_exposure']='2';r=concentration_lower_bound(self.ps,**self.kw);self.assertFalse(r['lower_bound_exceeds']);self.assertFalse(r['compliance_established'])
 def test_exact_cap_not_excess(self):self.ps[0]['measured_exposure']='10';self.assertFalse(concentration_lower_bound(self.ps,**self.kw)['lower_bound_exceeds'])
 def test_duplicate_position_rejected(self):
  with self.assertRaises(ValueError):concentration_lower_bound(self.ps+self.ps,**self.kw)
 def test_wrong_class_date_rejected(self):
  self.ps[0]['date']='2020-02-01'
  with self.assertRaises(ValueError):concentration_lower_bound(self.ps,**self.kw)
 def test_negative_denominator_rejected(self):
  self.kw['denominator']='-10'
  with self.assertRaises(ValueError):concentration_lower_bound(self.ps,**self.kw)
 def test_negative_exposure_not_netting(self):
  self.ps[0]['measured_exposure']='-1'
  with self.assertRaises(ValueError):concentration_lower_bound(self.ps,**self.kw)
 def test_unknown_measure_rejected(self):
  self.kw['additive_nonnegative_measure_confirmed']=False
  with self.assertRaises(ValueError):concentration_lower_bound(self.ps,**self.kw)
if __name__=='__main__':unittest.main(verbosity=2)
