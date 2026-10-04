import json,pathlib,unittest,hashlib
P=pathlib.Path(__file__).resolve().parents[1];ROOT=P.parent
jl=lambda p:[json.loads(x) for x in p.read_text().splitlines()]
class Checks(unittest.TestCase):
 def test_all70_once(self):
  a=jl(P/'all70-original-record-gaps.jsonl');b=jl(P/'cross-batch-ranked-routes.jsonl');self.assertEqual(len(a),70);self.assertEqual({r['test_id'] for r in a},{r['test_id'] for r in b});self.assertEqual(len({r['test_id'] for r in a}),70)
 def test_slate_integrity(self):
  for name,key,n in [('cheapest-meaningful-checks','meaningful_check_shortlist_rank',8),('strongest-news-potential','news_potential_shortlist_rank',7)]:
   rows=jl(P/(name+'.jsonl'));self.assertEqual(len(rows),n);self.assertEqual([r[key] for r in rows],list(range(1,n+1)));self.assertFalse(any(r['full_case_feasible'] for r in rows))
 def test_manifest344(self):self.assertEqual(len(jl(P/'sources.jsonl')),344)
 def test_tls_and_saved_hashes(self):
  for r in jl(P/'evidence/validated-http.jsonl'):
   self.assertTrue(r['tls_validation'])
   if r.get('saved_file'):self.assertFalse(r['truncated']);self.assertEqual(hashlib.sha256((P/r['saved_file']).read_bytes()).hexdigest(),r['sha256'])
 def test_pdf_not_full_priority(self):
  self.assertTrue((P/'evidence/grant-7654321.pdf').read_bytes().startswith(b'%PDF'));d=next(x for x in jl(P/'evidence/documentation.jsonl') if x['doc_id']=='D02');self.assertIn('not a medical prior-art pair or complete priority proof',d['observation'])
 def test_no_archive_positive(self):self.assertEqual(json.loads((P/'evidence/observed-media-archive.json').read_text())['archived_snapshots'],{})
 def test08_quarantine(self):
  r=jl(ROOT/'consequential-expansion-08/evidence/browser-probes.jsonl');q=[x for x in r if x.get('evidence_status')=='quarantined_certificate_validation_bypassed'];self.assertEqual(len(q),5);self.assertTrue(all(x['usable_as_verified_evidence'] is False for x in q));c=json.loads((ROOT/'consequential-expansion-08/counts.json').read_text());self.assertEqual(c['historical_trial_versions_verified'],0);self.assertEqual(c['well_identity_records_verified'],0)
 def test_no_reusable_bypass(self):
  for root in [P/'code',ROOT/'consequential-expansion-08/code']:
   for p in root.glob('*.py'):
    if p.name=='validate.py':continue
    self.assertNotIn('ignore_https_errors=True',p.read_text());self.assertNotIn('CERT_NONE',p.read_text());self.assertNotIn('verify=False',p.read_text());self.assertNotIn('create_unverified_context',p.read_text())
 def test_scoped_evidence_resolves(self):
  for r in jl(P/'cross-batch-ranked-routes.jsonl'):
   self.assertNotIn('current_batch_applicable_evidence_ids',r)
   for ref in r['applicable_evidence_refs']+r['sample_access_refs']:self.assertEqual(sum(x['doc_id']==ref['doc_id'] for x in jl(ROOT/ref['file'])),1)
 def test_no_invented_runtime(self):
  for r in jl(P/'all70-original-record-gaps.jsonl'):self.assertTrue(r['cost_time'].startswith('Unknown:'))
if __name__=='__main__':unittest.main(verbosity=2)
