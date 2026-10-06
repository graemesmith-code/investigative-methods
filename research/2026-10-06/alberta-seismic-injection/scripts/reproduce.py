"""Offline reproduction; defaults to saved infrastructure extracts; --full rescans bulk ST37."""
import pathlib,subprocess,sys,json,hashlib
P=pathlib.Path(__file__).resolve().parents[1]
steps=['restore_sources.py','analyze.py']
if '--full' in sys.argv:steps+=['st37_extract.py','enrich.py']
steps+=['extended_analysis.py','corroborate.py','audit_outputs.py','test_study.py']
log=[]
for name in steps:
 print('Running',name,flush=True)
 r=subprocess.run([sys.executable,str(P/'scripts'/name)],cwd=P,capture_output=True,text=True)
 log.append({'script':name,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 if r.returncode:break
(P/'results/reproduction-log.json').write_text(json.dumps(log,indent=2)+'\n')
sys.exit(log[-1]['returncode'])
