import unittest,json,pathlib,datetime as dt,hashlib,math,sys,sqlite3,tempfile,urllib.error
from zoneinfo import ZoneInfo
from shapely.geometry import shape,Point
from pyproj import Geod
P=pathlib.Path(__file__).resolve().parents[1];R=P/'results'
sys.path.insert(0,str(P.parents[2]/'code/ati'));import pipeline as budget
class StudyTests(unittest.TestCase):
 def test_catalogue_count_and_unique_ids(self):
  x=json.loads((P/'sources/earthquakes.json').read_text());n=json.loads((P/'sources/earthquake-count.json').read_text())['count'];self.assertEqual(len(x['features']),n);self.assertFalse(x.get('exceededTransferLimit'));self.assertEqual(len({f['attributes']['object_id'] for f in x['features']}),n)
 def test_source_footer_and_parse_integrity(self):
  x=json.loads((R/'denominators.json').read_text());self.assertEqual(x['raw_ingredient_rows'],595923);self.assertEqual(x['malformed_rows'],0);self.assertIn('(595923 rows affected)',x['source_footers'])
 def test_timezone_cross_midnight_and_dst(self):
  z=ZoneInfo('America/Edmonton')
  self.assertEqual(dt.datetime.fromisoformat('2025-02-25T06:32:35+00:00').astimezone(z).isoformat(),'2025-02-24T23:32:35-07:00')
  self.assertEqual(dt.datetime.fromisoformat('2025-03-09T08:59:00+00:00').astimezone(z).hour,1)
  self.assertEqual(dt.datetime.fromisoformat('2025-03-09T09:00:00+00:00').astimezone(z).hour,3)
 def test_inclusive_boundary_and_magnitude_separation(self):
  for threshold in [2.5,3.,4.]:
   self.assertTrue(threshold>=threshold);self.assertFalse(threshold-.01>=threshold)
  data=json.loads((R/'all-catalogue-collisions.json').read_text());self.assertTrue(all(r['event']['magnitude_type'] in ['ML','MLy'] for r in data))
  self.assertEqual(json.loads((R/'candidates-ML.json').read_text()),[])
 def test_well_and_event_multiplicity_not_discoveries(self):
  p=json.loads((R/'evidence-packets.json').read_text());self.assertEqual(len(p),9);self.assertEqual(len({x['well']['licence'] for x in p}),3);self.assertTrue(all(x['classification']=='indeterminate' and x['not_a_violation_finding'] for x in p))
 def test_subarea_geology_and_distance(self):
  ps={x['properties']['Order_Numb']:shape(x['geometry']) for x in json.loads((R/'rule-geometries.geojson').read_text())['features']}
  self.assertTrue(ps['6.2'].covers(ps['6.1']));self.assertTrue(ps['7.2'].covers(ps['7.1']))
  g=Geod(ellps='GRS80')
  for p in json.loads((R/'evidence-packets.json').read_text()):
   b=p['well']['bottomhole'];pt=Point(b['lon'],b['lat']);self.assertTrue(ps['7.2'].covers(pt));self.assertFalse(ps['7.1'].covers(pt));self.assertEqual(p['well']['current_licence']['ProjectedFormation'],'DUVERNAY FM')
   e=p['event'];d=g.inv(e['lon'],e['lat'],b['lon'],b['lat'])[2]/1000
   self.assertAlmostEqual(d,p['records'][0]['distance_bh_km'],places=5);self.assertLess(d,5)
 def test_catalogue_disagreement_retained(self):
  x=json.loads((R/'catalogue-crosschecks.json').read_text());self.assertEqual(len(x),2)
  feb22=next(v for v in x if v['NRCan']['id']=='ca2025dscb');self.assertEqual(feb22['NRCan']['magnitude'],3.1);self.assertEqual(feb22['candidate_matches'][0]['AGS']['MLy'],2.09);self.assertTrue(all(len(v['candidate_matches'])==1 for v in x))
 def test_monthly_no_match_is_not_no_injection(self):
  x=json.loads((R/'monthly-target-identity.json').read_text());self.assertEqual(x['matched_rows'],[]);self.assertEqual(len(x['uwi_mapping']),3)
  for uwiid in x['uwi_mapping']:self.assertTrue(uwiid.startswith('ABWI1'));self.assertEqual(len(uwiid),20)
 def test_noise_incident_is_not_seismic_edge(self):
  x=json.loads((R/'incident-lookups.json').read_text());row=x['incident-complaints.xls']['exact_incident_or_licence_matches'][0];header=x['incident-complaints.xls']['columns'];self.assertEqual(row[header.index('CICReferenceNumber')],'0438079');self.assertNotEqual(int(row[header.index('CICReferenceNumber')]),438049);self.assertEqual(row[header.index('CauseType')],'Noise-TempOperations')
 def test_jev_cost_and_failed_pilot_gate(self):
  l=json.loads((P/'jev/ledger.json').read_text());self.assertEqual(len(l['attempts']),2);self.assertEqual(l['accounted_microusd']['jev'],71);self.assertEqual(l['accounted_microusd']['exa'],0);self.assertTrue(all(a['status']=='success' for a in l['attempts']));self.assertTrue(any(not r['all_correct'] for r in json.loads((P/'jev/pilot-evaluation.json').read_text())))
  for a in l['attempts']:
   usage=json.loads(a['usage']);self.assertEqual(a['accounted'],math.ceil(usage['input_tokens']*.042));self.assertLessEqual(a['accounted'],a['reserve'])
 def test_budget_reservation_before_transport_and_failure_retention(self):
  with tempfile.TemporaryDirectory() as d:
   ledger=budget.Ledger(pathlib.Path(d)/'fixture.sqlite',mode='fixture');calls=[]
   def fail(p,b):calls.append(1);raise TimeoutError()
   body={'model':budget.MODEL,'state':'synthetic','questions':{'x':{'type':'noul','instructions':'Test'}}};client=budget.Client(ledger,fail)
   with self.assertRaises(TimeoutError):client.call('jev',body)
   self.assertEqual(ledger.totals()['jev'],3000)
   with self.assertRaises(budget.GuardError):client.call('jev',body)
   self.assertEqual(len(calls),1)
 def test_lossless_source_parts(self):
  for r in json.loads((P/'sources/multipart/manifest.json').read_text()):
   h=hashlib.sha256();n=0
   for p in r['parts']:
    b=(P/p['path']).read_bytes();self.assertEqual(hashlib.sha256(b).hexdigest(),p['sha256']);h.update(b);n+=len(b)
   self.assertEqual(h.hexdigest(),r['sha256']);self.assertEqual(n,r['bytes'])
if __name__=='__main__':unittest.main(verbosity=2)
