import copy,json,pathlib,tempfile,unittest,urllib.error
import pipeline as p
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.path=pathlib.Path(self.tmp.name)/'ledger.sqlite';self.l=p.Ledger(self.path,'fixture');self.calls=0
  self.b={'model':p.MODEL,'state':'x','questions':{'x':{'type':'score','instructions':'rate','criteria':['low','high']}}}
 def transport(self,provider,body):
  self.calls+=1;return {'model':p.MODEL,'answers':{'x':{'type':'score','score':.9,'confidence':.8,'probabilities':{'0':.1,'1':.9}}},'usage':{'input_tokens':400,'output_tokens':10}}
 def test_cap_before_transport(self):
  l=p.Ledger(pathlib.Path(self.tmp.name)/'cap.sqlite','fixture',{'jev':p.CAP-2000,'exa':0})
  with self.assertRaises(p.GuardError):p.Client(l,self.transport).call('jev',self.b)
  self.assertEqual(self.calls,0)
 def test_cache_and_prompt_version(self):
  c=p.Client(self.l,self.transport);c.call('jev',self.b);c.call('jev',self.b);self.assertEqual(self.calls,1)
  b=copy.deepcopy(self.b);b['questions']['x']['instructions']='changed';c.call('jev',b);self.assertEqual(self.calls,2)
 def test_reopen_cannot_reset(self):
  p.Client(self.l,self.transport).call('jev',self.b);l=p.Ledger(self.path,'fixture',{'jev':0,'exa':0});self.assertEqual(l.totals()['jev'],17)
  with self.assertRaises(p.GuardError):p.Ledger(self.path,'live')
 def test_timeout_blocks_and_retains(self):
  def fail(*a):raise TimeoutError()
  with self.assertRaises(TimeoutError):p.Client(self.l,fail).call('jev',self.b)
  with self.assertRaises(p.GuardError):p.Client(p.Ledger(self.path,'fixture'),self.transport).call('jev',self.b)
  self.assertEqual(self.l.totals()['jev'],3000);self.assertEqual(self.calls,0)
 def test_http_error_retains_no_retry(self):
  def fail(*a):raise urllib.error.HTTPError(p.ENDPOINTS['jev'],429,'rate',{},None)
  with self.assertRaises(urllib.error.HTTPError):p.Client(self.l,fail).call('jev',self.b)
  with self.assertRaises(p.GuardError):p.Client(self.l,self.transport).call('jev',self.b)
  self.assertEqual(self.l.totals()['jev'],3000)
 def test_invalid_response_saved_and_blocks(self):
  def fail(*a):return {'model':p.MODEL,'answers':{}}
  with self.assertRaises(p.GuardError):p.Client(self.l,fail).call('jev',self.b)
  row=self.l.db.execute('SELECT * FROM attempts').fetchone();self.assertEqual(row['status'],'pending');self.assertIsNotNone(row['response']);self.assertEqual(row['accounted'],3000)
 def test_schema_numeric_and_keys(self):
  for field,value in [('score',float('nan')),('score',True),('score',2),('confidence',-1)]:
   r=self.transport('jev',self.b);r['answers']['x'][field]=value
   with self.assertRaises(p.GuardError):p.validate('jev',self.b,r)
  r=self.transport('jev',self.b);r['answers']={}
  with self.assertRaises(p.GuardError):p.validate('jev',self.b,r)
 def test_prices_unknown_and_bounds(self):
  self.assertEqual(p.price_bound('jev',self.b),3000)
  for change in [{'model':'jev-latest'},{'state':'x'*16001}]:
   with self.assertRaises(p.GuardError):p.price_bound('jev',{**self.b,**change})
  with self.assertRaises(p.GuardError):p.price_bound('exa',{'query':'x','type':'deep'})
  for cost in [float('nan'),True,.031,-1,None]:
   with self.assertRaises(p.GuardError):p.validate('exa',{}, {'costDollars':{'total':cost},'results':[]})
 def test_full_context_cost(self):
  r=self.transport('jev',self.b);r['usage']['input_tokens']=64000;self.assertEqual(p.validate('jev',self.b,r)[1],2688)
 def test_redirect_refused(self):
  with self.assertRaises(p.GuardError):p.NoRedirect().redirect_request(None,None,302,'',{},'https://elsewhere.invalid')
 def test_over_reservation_cannot_settle(self):
  a=self.l.reserve('jev','x',self.b,3000)
  with self.assertRaises(p.GuardError):self.l.finish(a,{}, {},3001,'fixture')
  self.assertEqual(self.l.totals()['jev'],3000)
class ArchiveResumeTests(unittest.TestCase):
 def test_missing_ledger_refuses_without_creating(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as tmp, patch.object(p,'OUT',pathlib.Path(tmp)):
   with self.assertRaises(p.GuardError):p.open_live_ledger()
   self.assertFalse((pathlib.Path(tmp)/'ledger.sqlite').exists())
 def test_empty_history_cannot_reset_budget(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as tmp, patch.object(p,'OUT',pathlib.Path(tmp)):
   ledger=p.Ledger(pathlib.Path(tmp)/'ledger.sqlite','live')
   with self.assertRaises(p.GuardError):p.open_live_ledger()
   self.assertEqual(ledger.db.execute('SELECT COUNT(*) FROM attempts').fetchone()[0],0)
if __name__=='__main__':unittest.main()
