import json,pathlib,unittest
P=pathlib.Path(__file__).resolve().parent
class FinalAudit(unittest.TestCase):
 def test_counterevidence_is_preserved(self):
  a={x['uuid']:x for x in json.loads((P/'all-original-interest-audit.json').read_text())}
  for u,phrase in [('20c64cbe-ef8f-45de-a6e1-d30e32976d45','Novartis'),('9b1de8f1-07e0-4fdb-9bb1-94c7a1e035c5','Honda'),('b81ae0cb-af56-4133-b68c-9717340983b1','foreign company')]:
   self.assertIn(phrase,' '.join(a[u]['narratives']))
 def test_cohort_denominators(self):
  d=json.loads((P/'cohort-triage.json').read_text());self.assertEqual(len(d),343);self.assertEqual(sum(x['major'] for x in d),25)
 def test_versions_are_not_relationships(self):
  d=json.loads((P/'archive-scope.json').read_text());self.assertEqual(d['quarterly_document_records'],d['relationship_quarters']+d['additional_quarter_versions']);self.assertEqual(d['records'],109389)
 def test_historical_amendment_totals(self):
  d=json.loads((P/'historical-amount-verification.json').read_text());self.assertEqual([x['expense_numeric_sum'] for x in d],['150000.00','1330000.00','2117350.49']);self.assertTrue(all(y['matches_api'] for x in d for y in x['selected_originals']))
if __name__=='__main__':unittest.main()
