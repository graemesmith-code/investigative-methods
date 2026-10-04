import pathlib,json,unittest,collections,hashlib
P=pathlib.Path(__file__).resolve().parents[1]
jl=lambda p:[json.loads(x) for x in p.read_text().splitlines()]
class CheckpointChecks(unittest.TestCase):
 def test_catalog_scan(self):
  d=json.loads((P/'evidence/environmental-registry-scan.json').read_text());self.assertEqual(d['system_count'],1555);self.assertEqual(d['matching_source_blocks'],[]);self.assertIn('not proof',d['interpretation'])
 def test_normalized_source_counts(self):
  rows=jl(P/'sources.jsonl');self.assertEqual(len(rows),344)
  cs=collections.Counter(pathlib.Path(r['file']).name for r in rows);self.assertEqual(cs,{'Rabbit2(1).txt':267,'Rabbit3.txt':77})
 def test_supporting_source(self):
  rs=jl(P/'supporting-sources.jsonl');self.assertEqual(len(rs),1);r=rs[0];self.assertEqual(r['sys_id'],'SYS-0854');self.assertIn('AP-1802',r['all_ap_ids']);self.assertEqual(hashlib.sha256(r['source_text'].encode()).hexdigest(),r['block_sha256'])
 def test_eia_schema_distinguishes_allocations(self):
  d=json.loads((P/'evidence/eia-facility-schema.json').read_text())['response'];self.assertIn('total-consumption-btu',d['data']);self.assertIn('consumption-for-eg-btu',d['data']);self.assertIn('plantCode',{x['id'] for x in d['facets']})
 def test_bounded_row_not_whole_population(self):
  d=json.loads((P/'evidence/eia-one-schema-row.json').read_text());self.assertEqual(len(d['response']['data']),1);self.assertEqual(str(d['request']['params']['length']),'1');self.assertGreater(int(d['response']['total']),1);self.assertEqual(d['response']['data'][0]['fuelType'],'ALL')
 def test_ranked_inventory_complete(self):
  rows=jl(P/'cross-batch-ranked-routes.jsonl');self.assertEqual(len(rows),67);self.assertEqual(len({r['test_id'] for r in rows}),67);self.assertEqual([r['cheap_rank'] for r in rows],list(range(1,68)))
  self.assertEqual(sum(r['kind'] in ['refinement','existing_mechanism_refinement'] for r in rows),14)
 def test_rank_uses_documented_readiness(self):
  rows=jl(P/'cross-batch-ranked-routes.jsonl');self.assertEqual({r['test_id'] for r in rows if r['readiness_tier']==1},{'R05','R11','R12'})
  for r in rows:self.assertTrue((P.parent/r['source_file']).exists());self.assertFalse(r['full_case_feasible'])
 def test_no_new_count_from_applications(self):
  d=json.loads((P/'counts.json').read_text());self.assertEqual(d['new_predicates'],0);self.assertEqual(d['reviewed_non_refinement_formulations'],53);self.assertEqual(d['paid_external_api_calls'],0)
 def test_six_route_decisions(self):
  rs=jl(P/'route-screen.jsonl');self.assertEqual(len(rs),6)
  for r in rs:self.assertTrue(r['constraint']);self.assertTrue(r['unresolved']);self.assertTrue(r['next_cheapest_check'])
 def test_document_and_record_scope(self):
  ds=jl(P/'evidence/documentation.jsonl');self.assertEqual(len(ds),8)
  for d in ds:self.assertFalse(d['case_test_executed'])
if __name__=='__main__':unittest.main(verbosity=2)
