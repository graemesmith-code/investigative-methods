"""Safety and integrity fixtures: these test inference gates, not source availability."""
import unittest,json,pathlib,collections
from normalize import OUT,ROOT

def identity(a,b):
 if a.get('type')!=b.get('type'):return False
 if a.get('namespace') and a.get('namespace')==b.get('namespace') and a.get('id') and a.get('id')==b.get('id'):return True
 return False # Name, address and employer matches never establish identity here.
def post_restriction(action,listing):return action['date']>=listing['start'] and (not listing.get('end') or action['date']<listing['end'])
def restricted_activity(action,listing):
 return identity(action,listing) and post_restriction(action,listing) and listing.get('applicable_restriction_confirmed',False) and action.get('jurisdiction_confirmed',False) and action.get('actual_activity',False) and action.get('exceptions_checked',False) and not action.get('authorized',False)
def blocked_share_edge(edge):return edge.get('kind')=='ownership' and edge.get('dated_verified',False) and edge.get('blocked_owner',False) and edge.get('aggregate_percent',0)>=50

def unique_award_total(rows):
 awards={}
 for r in rows:
  key=(r['namespace'],r['award'],r['action'])
  if key in awards and awards[key]!=r['amount']:raise ValueError('conflicting duplicate requires review')
  awards[key]=r['amount']
 return sum(awards.values())
class InferenceGates(unittest.TestCase):
 def test_name_collision(self):self.assertFalse(identity({'type':'person','name':'Alex Lee'},{'type':'person','name':'Alex Lee'}))
 def test_namespace_collision(self):self.assertFalse(identity({'type':'company','namespace':'NZ','id':'123'},{'type':'company','namespace':'UK','id':'123'}))
 def test_entity_type_collision(self):self.assertFalse(identity({'type':'vessel','namespace':'IMO','id':'123'},{'type':'company','namespace':'IMO','id':'123'}))
 def test_exact_namespace(self):self.assertTrue(identity({'type':'vessel','namespace':'IMO','id':'123'},{'type':'vessel','namespace':'IMO','id':'123'}))
 def test_pre_designation(self):self.assertFalse(post_restriction({'date':'2024-01-01'},{'start':'2025-01-01'}))
 def test_delisted(self):self.assertFalse(post_restriction({'date':'2026-01-01'},{'start':'2024-01-01','end':'2025-01-01'}))
 def test_non_sdn_not_automatic(self):self.assertFalse(restricted_activity({'date':'2026-01-01','type':'company','namespace':'reg','id':'123'},{'start':'2025-01-01','type':'company','namespace':'reg','id':'123','list':'non-SDN'}))
 def test_control_not_ownership(self):self.assertFalse(blocked_share_edge({'kind':'control','dated_verified':True,'blocked_owner':True,'aggregate_percent':100}))
 def test_accounting_parent_not_share(self):self.assertFalse(blocked_share_edge({'kind':'accounting_consolidation','dated_verified':True,'blocked_owner':True,'aggregate_percent':100}))
 def test_minority_not_automatic(self):self.assertFalse(blocked_share_edge({'kind':'ownership','dated_verified':True,'blocked_owner':True,'aggregate_percent':25}))
 def test_many_to_many_inflation(self):self.assertEqual(unique_award_total([{'namespace':'US','award':'A','action':'1','amount':10}]*4),10)
 def test_conflicting_duplicate(self):
  with self.assertRaises(ValueError):unique_award_total([{'namespace':'US','award':'A','action':'1','amount':v} for v in [10,20]])
 def test_termination_not_payment(self):
  a=dict(type='company',namespace='reg',id='1',date='2026-01-01',jurisdiction_confirmed=True,actual_activity=False,exceptions_checked=True)
  b=dict(type='company',namespace='reg',id='1',start='2025-01-01',applicable_restriction_confirmed=True)
  self.assertFalse(restricted_activity(a,b))
 def test_license_exception(self):
  a=dict(type='company',namespace='reg',id='1',date='2026-01-01',jurisdiction_confirmed=True,actual_activity=True,exceptions_checked=True,authorized=True)
  b=dict(type='company',namespace='reg',id='1',start='2025-01-01',applicable_restriction_confirmed=True)
  self.assertFalse(restricted_activity(a,b))
class Artifacts(unittest.TestCase):
 def test_catalog(self):
  a=[json.loads(x) for x in (OUT/'sources.jsonl').read_text().splitlines()]; self.assertEqual(len(a),344)
  for r in a:
   raw=(ROOT/r['file']).read_bytes()[r['byte_start']:r['byte_end']]
   import hashlib
   self.assertEqual(hashlib.sha256(raw).hexdigest(),r['block_sha256'])
   self.assertTrue(r['labeled_access_points'])
 def test_designs(self):
  for p in [OUT/'checkpoints/early-tests.jsonl',OUT/'tests.jsonl']:
   if not p.exists():continue
   rows=[json.loads(x) for x in p.read_text().splitlines()]
   self.assertEqual(len(rows),len(set(r['fingerprint'] for r in rows)))
   for r in rows:
    self.assertNotEqual(r['source_a'],r['source_b'])
    for field in ['initial_observation','expected_observation','basis','interesting_outcome','timing','geography','ordinary_explanations','disqualifiers','required_evidence','next_cheapest_check','source_a_provenance','source_b_provenance','absence_policy']:
     self.assertTrue(r[field],(r['test_id'],field))
    self.assertEqual(r['execution_status'],'not_executed_not_confirmed_feasible')
    self.assertNotIn('established',r['basis_strength'])
    if 'provisional' in r['join_status']:self.assertLessEqual(r['join_confidence_score'],1)
    if r['mechanism'] in ['S02','E03','E08','I01','I02','C06']:self.assertNotIn(r['source_b'],['SYS-0001','SYS-0009','SYS-0010','SYS-0020','SYS-0040','SYS-0048'])
if __name__=='__main__':unittest.main()
