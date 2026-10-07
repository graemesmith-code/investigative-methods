"""Small fixture check of matching, duplicate handling and unmatched rows."""
import csv,io,json,subprocess,sys,tempfile,zipfile
from pathlib import Path
base=Path(__file__).resolve().parent
name=json.loads((base/'entities.json').read_text())[0]['primary_name']
fields=['contract_transaction_unique_key','contract_award_unique_key','recipient_name','action_date','recipient_uei']
rows=[['t1','a1',name,'2025-01-01','u1'],['t1','a1',name,'2025-01-01','u1'],
      ['t2','a2',name.lower()+' LLC','2025-02-01','u2'],
      ['t3','a3','UNMATCHED TEST ORGANIZATION 8291481','2025-03-01','u3']]
with tempfile.TemporaryDirectory() as temp:
    p=Path(temp); stream=io.StringIO(); w=csv.writer(stream);w.writerow(fields);w.writerows(rows)
    with zipfile.ZipFile(p/'fixture.zip','w') as z:z.writestr('fixture.csv',stream.getvalue())
    subprocess.run([sys.executable,str(base/'screen_contracts.py'),str(p/'fixture.zip'),str(p/'output')],check=True,stdout=subprocess.DEVNULL)
    result=json.loads((p/'output/screen-summary.json').read_text())
    assert result['raw_rows']==4 and result['unique_transactions']==3
    assert result['duplicate_transactions']==1
    assert result['matched_unique_transactions']==2
    assert result['match_methods']=={'normalized_exact':1,'legal_suffix_removed':1}
print('Fixture passed: direct match, suffix match, unrelated name and duplicate transaction.')
