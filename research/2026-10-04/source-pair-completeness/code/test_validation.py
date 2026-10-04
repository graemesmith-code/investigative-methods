import unittest,pathlib,json,csv,sys,re,collections
P=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'code/generator'))
import build
from evidence_overrides import geography_gate,record_identifier_equal,mirror_trade_tuple
jl=lambda p:[json.loads(x) for x in p.read_text().splitlines()]
class Validation(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.rows=jl(P/'candidate-inventory.jsonl');c.ss={x['sys_id']:x for x in jl(P/'sources.jsonl')};c.cards=jl(P/'reviewed-recipes.jsonl')
 def test_all_sources_individually_covered(self):
  rows=list(csv.DictReader((P/'all-344-source-reasoning.csv').read_text().splitlines()));self.assertEqual({r['sys_id'] for r in rows},set(self.ss));self.assertEqual(len(rows),344)
 def test_all_mechanisms_reviewed(self):self.assertEqual({r['mechanism'] for r in jl(P/'mechanism-review.jsonl')},{r['key'] for r in json.loads((P/'mechanisms.json').read_text())})
 def test_partition(self):self.assertEqual(len(jl(P/'remaining-108-reviews.jsonl')),108);self.assertEqual(len(jl(P/'participating-205-reviews.jsonl')),205)
 def test_counts(self):self.assertEqual(len(self.rows),1730);self.assertEqual(sum(r['admission_status']=='quarantined_geography' for r in self.rows),15);self.assertEqual(len(self.cards),32)
 def test_google_propagated(self):
  affected=[r for r in self.rows if 'SYS-0164' in [r['source_a'],r['source_b']]];self.assertEqual(len(affected),31)
  for r in affected:self.assertTrue(r['source_evidence_overrides']);self.assertEqual(r['testability_score'],1);self.assertIn('global labels are not',r['geography'])
 def test_google_canada_rejected(self):self.assertTrue(geography_gate(self.ss['SYS-0220'],self.ss['SYS-0164']).startswith('quarantined'))
 def test_google_echo_territories_only(self):self.assertIn('US_mainland_excluded',geography_gate(self.ss['SYS-0038'],self.ss['SYS-0164']))
 def test_r07_correction(self):
  r=next(r for r in self.cards if r['review_id']=='R07');self.assertIn('Puerto Rico',r['initial_observation']);self.assertIn('US mainland',r['expected_observation']);self.assertIn('D23',r['evidence_doc_ids'])
 def test_access_routes_in_production_ranking(self):
  for n in [214,255,256]:self.assertEqual(build.ranking_dimensions(self.ss['SYS-0217'],self.ss[f'SYS-{n:04d}'],'spatiotemporal_conditional',2,2,'free')[1],3)
 def test_manual_route_changes_tier(self):
  a=dict(self.ss['SYS-0054']);b=dict(self.ss['SYS-0058']);a['labeled_access_points']=[{'fields':{'Original access method':'manual browser only'}}];self.assertEqual(build.ranking_dimensions(a,b,'name',1,2,'free')[1],3)
 def test_provisional_documentation(self):self.assertEqual(build.ranking_dimensions(self.ss['SYS-0024'],self.ss['SYS-0054'],'name',1,2,'free')[0],1)
 def test_imo_record_semantics_used_by_join(self):
  a,b=self.ss['SYS-0024'],self.ss['SYS-0074'];m={'join':'vessel'};ship={'value':'9074729','entity_type':'vessel'};company={'value':'9074729','entity_type':'company'}
  self.assertEqual(build.join(a,b,m,ship,company)[0],'rejected_identifier_semantics');self.assertEqual(build.join(a,b,m,ship,ship)[0],'direct_identifier_conditional')
  self.assertFalse(record_identifier_equal('IMO','9074728','9074728','vessel','vessel'))
 def test_imo_company_schema_not_ship(self):
  a=dict(self.ss['SYS-0072']);a['join_fields']=['IMO company number','company name'];self.assertEqual(build.join(a,self.ss['SYS-0074'],{'join':'vessel'})[0],'bridge_required')
 def test_directional_trade_tuple(self):
  self.assertEqual(mirror_trade_tuple('USA','DEU','X','1001','2025'),('DEU','USA','M','1001','2025'))
  for r in self.rows:
   if r['mechanism']=='F02':self.assertIn('non-EU reporter in UN Comtrade',r['initial_observation']);self.assertIn('EU-member-reported Comext',r['expected_observation'])
 def test_saved_trial_link_and_retrospective_dates(self):
  cross=json.loads((P/'evidence/crossref-one.json').read_text())['message']['items'][0];trial=json.loads((P/'evidence/trial-crossref-linked.json').read_text())['protocolSection'];ids=[x['clinical-trial-number'].upper() for x in cross['clinical-trial-number']];self.assertIn(trial['identificationModule']['nctId'],ids)
  status=trial['statusModule'];self.assertGreater(status['studyFirstPostDateStruct']['date'],status['primaryCompletionDateStruct']['date'])
 def test_saved_worldbank_exact_link_and_date_caution(self):
  docs=json.loads((P/'evidence/worldbank-doc-one.json').read_text())['documents'];doc=next(v for k,v in docs.items() if k!='facets');projects=json.loads((P/'evidence/worldbank-project-linked.json').read_text())['projects'];self.assertIn(doc['projectid'],projects);self.assertEqual(projects[doc['projectid']]['id'],doc['projectid']);self.assertTrue(doc['docdt'].startswith('2026-12-31'));self.assertIn('30-Dec-2024',(P/'evidence/worldbank-linked-agreement-text.txt').read_text().splitlines()[0])
 def test_saved_ooni_asn_and_negative_flags(self):
  o=json.loads((P/'evidence/ooni-one-metadata.json').read_text())['results'][0];r=json.loads((P/'evidence/ripe-asn-one.json').read_text());self.assertEqual(o['probe_asn'].removeprefix('AS'),r['data']['resource']);self.assertFalse(o['anomaly']);self.assertFalse(o['confirmed']);self.assertIn('hours old',str(r['messages']))
 def test_falsifiers_separated_from_performed(self):
  rows=list(csv.DictReader((P/'adversarial-review.csv').read_text().splitlines()));self.assertEqual(len(rows),32)
  for r in rows:self.assertNotEqual(r['proposed_falsifier'],r['check_actually_performed']);self.assertTrue(r['observed_result'])
 def test_no_execution_claims(self):
  for r in self.cards:self.assertFalse(r['bulk_investigative_execution']);self.assertTrue(r['mandatory_auxiliary_inputs'])
 def test_source81_identity_corrected(self):
  rows=list(csv.DictReader((P/'prior-31-reviews-corrected.csv').read_text().splitlines()));r=next(r for r in rows if r['sys_id']=='SYS-0081');self.assertIn('Space-Track',r['finding']);self.assertIn('mistakenly',r['finding'])
class FinalRepairs(Validation):
 def test_election_source_roles(self):
  m=next(r for r in jl(P/'mechanism-review.jsonl') if r['mechanism']=='W09');self.assertEqual(m['preferred_source_b'],'SYS-0201');self.assertIn('Elections',self.ss[m['preferred_source_b']]['name'])
  r=next(r for r in jl(P/'remaining-108-reviews.jsonl') if r['sys_id']=='SYS-0171');self.assertEqual(r['partner_sys_id'],'SYS-0201')
 def test_supplemental_membership(self):
  ms={m['key']:m for m in json.loads((P/'mechanisms.json').read_text())};supp=[]
  for r in jl(P/'mechanism-review.jsonl'):
   m=ms[r['mechanism']];valid=int(r['preferred_source_a'][-4:]) in m['a'] and int(r['preferred_source_b'][-4:]) in m['b']
   self.assertEqual(valid,r['membership_status']=='emitted_rule_representative')
   if not valid:self.assertTrue(r['supplemental_reference']);supp.append(r['mechanism'])
  self.assertEqual(set(supp),{'E01','C05','F04'})
 def test_status_propagation_all_ledgers(self):
  import gzip
  active=[r for r in self.rows if r['admission_status']=='conditional_candidate'];quarantine=[r for r in self.rows if r['admission_status']!='conditional_candidate'];ap={(r['source_a'],r['source_b']) for r in active};qp={(r['source_a'],r['source_b']) for r in quarantine}
  with gzip.open(P/'pair-universe.csv.gz','rt') as f: pairs=list(csv.DictReader(f))
  self.assertEqual(len(pairs),117992);self.assertEqual({(r['source_a'],r['source_b']) for r in pairs if r['status']=='conditional_design'},ap);self.assertEqual({(r['source_a'],r['source_b']) for r in pairs if r['status']=='quarantined_geography'},qp-ap)
  coverage=jl(P/'source-coverage.jsonl');self.assertEqual(sum(r['active_designs'] for r in coverage),2*len(active));self.assertEqual(sum(r['quarantined_designs'] for r in coverage),2*len(quarantine));self.assertEqual(sum(r['raw_inventory_designs'] for r in coverage),2*len(self.rows))
  progress=json.loads((P/'progress.json').read_text());self.assertEqual(progress['active_candidate_rows'],len(active));self.assertEqual(progress['quarantined_rows'],len(quarantine));self.assertEqual(progress['pairs_with_conditional_designs'],len(ap));self.assertEqual(sum(progress['mechanism_counts'].values()),len(active))
 def test_state_request_contribution(self):
  r=next(r for r in self.cards if r['review_id']=='N05');self.assertIn('US State Department',r['initial_observation']);self.assertIn('reading room',r['expected_observation']);self.assertIn('single-source',r['ordinary_explanations_and_falsifiers'])
 def test_pair_enumeration_reproducible(self):
  r=jl(P/'named-identifier-assessment.jsonl');self.assertEqual(len(r),70);self.assertEqual(sum(not x['in_rule_ab'] and not x['in_rule_ba'] for x in r),45);self.assertEqual(len({(x['source_a'],x['source_b']) for x in r}),70)
 def test_queue_pair_specific(self):
  q=jl(P/'recommended-next-tests.jsonl');self.assertEqual(len(q),9)
  for r in q:self.assertTrue(r['pair_specific_reason']);self.assertTrue(r['evidence_gaps']);self.assertTrue(r['next_cheapest_check']);self.assertEqual(r['status'],'not_executed')
if __name__=='__main__':
 # Run inherited checks once, plus the six new repair checks.
 unittest.main(defaultTest='FinalRepairs',verbosity=2)
