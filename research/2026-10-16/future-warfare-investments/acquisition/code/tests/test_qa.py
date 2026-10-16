import contextlib,hashlib,io,json,os,pathlib,subprocess,sys,tempfile,unittest,zipfile
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import normalize
from lineage import issues,REQUIRED,missing_columns
import pandas as pd
class QA(unittest.TestCase):
 def test_restore_empty_partial_corrupt_and_complete(self):
  with tempfile.TemporaryDirectory() as d:
   root=pathlib.Path(d);(root/'validation').mkdir();(root/'raw').mkdir()
   (root/'retrieve.py').write_text((pathlib.Path(__file__).resolve().parents[1]/'retrieve.py').read_text())
   (root/'acquire.py').write_text("import pathlib\nROOT=DATA=pathlib.Path(__file__).parent\ndef fetch(*a):raise AssertionError('network forbidden')\ndef save_json(*a):pass\ndef now():return ''\n")
   entries=[{'source':'test','outcome':'downloaded','relative_path':'raw/'+n,'bytes':1,'sha256':hashlib.sha256(b'x').hexdigest(),'url':'https://example.invalid/'+n} for n in ['one','two']]
   (root/'validation/http_manifest.jsonl').write_text('\n'.join(map(json.dumps,entries)))
   def run(source='test'):return subprocess.run([sys.executable,str(root/'retrieve.py'),'--verify-only','--source',source],capture_output=True).returncode
   self.assertNotEqual(run('absent'),0);self.assertNotEqual(run(),0)
   (root/'raw/one').write_bytes(b'x');self.assertNotEqual(run(),0)
   (root/'raw/two').write_bytes(b'y');self.assertNotEqual(run(),0)
   (root/'raw/two').write_bytes(b'x');self.assertEqual(run(),0)
 def test_required_lineage(self):
  frame=pd.DataFrame([{k:'value' for k in REQUIRED}]);self.assertEqual(issues(frame),{})
  for k in REQUIRED:
   self.assertIn(k,issues(frame.drop(columns=k)));self.assertIn(k,missing_columns(frame.drop(columns=k).columns))
   broken=frame.copy();broken[k]='';self.assertIn(k,issues(broken))
 def test_hypersonic_and_untagged(self):
  self.assertIn('hypersonic',normalize.tags('Hypersonic glide vehicle'))
  self.assertIn('hypersonic',normalize.tags('hyper-sonic sensor'))
  self.assertEqual(normalize.tags('unclassified descriptive project'),[])
 def test_dry_run_preserves_untagged(self):
  import gzip
  with tempfile.TemporaryDirectory() as d:
   root=pathlib.Path(d)
   for folder in ['normalized','samples','validation']:(root/folder).mkdir()
   (root/'dry_run.py').write_text((pathlib.Path(__file__).resolve().parents[1]/'dry_run.py').read_text())
   (root/'acquire.py').write_text("import pathlib,json\nROOT=DATA=pathlib.Path(__file__).parent\ndef save_json(p,v):p.write_text(json.dumps(v))\n")
   with gzip.open(root/'normalized/sbir_current.jsonl.gz','wt') as f:
    for i in range(40):f.write(json.dumps({'document_id':str(i),'source':'sbir_current','capability_tags':json.dumps(['hypersonic'] if i<20 else []),'title':'example','text':'example','raw_locator':'fixture','source_url':'https://example.invalid','source_snapshot_sha256':'a'*64,'retrieved_at':'2026-10-16T00:00:00Z'})+'\n')
   run=subprocess.run([sys.executable,str(root/'dry_run.py')],capture_output=True,text=True);self.assertEqual(run.returncode,0,run.stderr)
   rows=[json.loads(x) for x in (root/'samples/dry_run_candidates.jsonl').read_text().splitlines()]
   self.assertEqual(len(rows),16);self.assertEqual(sum(not json.loads(x['capability_tags']) for x in rows),2)
   self.assertTrue(all(x['deterministic_checks']['novelty_score'] is None for x in rows))
 def test_two_vintages_exact_file_lineage(self):
  olddata,oldroot=normalize.DATA,normalize.ROOT
  try:
   with tempfile.TemporaryDirectory() as d:
    root=pathlib.Path(d);normalize.DATA=normalize.ROOT=root
    for folder in ['raw/usaspending_fixture','validation','samples','normalized']:(root/folder).mkdir(parents=True)
    entries=[]
    for i in [1,2]:
     p=root/f'raw/usaspending_fixture/vintage{i}.zip'
     with zipfile.ZipFile(p,'w') as z:z.writestr('PrimeTransactions.csv',f'contract_transaction_unique_key,transaction_description,action_date\nT{i},hypersonic test {i},2025-01-01\n')
     entries.append({'source':'usaspending_fixture','outcome':'downloaded','relative_path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'retrieved_at':f'2026-10-0{i}T00:00:00Z','url':f'https://example.invalid/{i}'})
    (root/'validation/http_manifest.jsonl').write_text('\n'.join(map(json.dumps,entries)))
    with contextlib.redirect_stdout(io.StringIO()):normalize.analyze('usaspending_fixture')
    df=pd.read_parquet(root/'normalized/usaspending_fixture.parquet');self.assertEqual(len(df),2)
    self.assertEqual(json.loads((root/'validation/usaspending_fixture_profile.json').read_text())['raw_rows'],2)
    for i,e in enumerate(entries,1):
     row=df[df.transaction_key==f'T{i}'].iloc[0];self.assertEqual(row.source_snapshot_sha256,e['sha256']);self.assertEqual(row.retrieved_at,e['retrieved_at']);self.assertIn(f'vintage{i}.zip',row.raw_locator)
  finally:normalize.DATA,normalize.ROOT=olddata,oldroot
if __name__=='__main__':unittest.main()
