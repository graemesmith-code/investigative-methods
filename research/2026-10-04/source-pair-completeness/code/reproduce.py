import pathlib,subprocess,sys,time,json
P=pathlib.Path(__file__).resolve().parents[1];runs=[]
for script in ['generator/build.py','enumerate.py','assess.py','correct_and_extend.py','test_validation.py']:
 args=[sys.executable,str(P/'code'/script)]+(['--stage','full'] if script=='generator/build.py' else [])
 started=time.perf_counter();r=subprocess.run(args,text=True,capture_output=True);elapsed=time.perf_counter()-started
 runs.append(dict(script=script,returncode=r.returncode,elapsed_seconds=round(elapsed,4)))
 if script=='test_validation.py':(P/'evidence/validation-results.txt').write_text(r.stdout+r.stderr)
 if r.returncode:print(r.stdout+r.stderr);raise SystemExit(r.returncode)
 print(script,round(elapsed,3),'seconds')
(P/'evidence/reproduction-timing.json').write_text(json.dumps(dict(runs=runs,total_command_seconds=round(sum(x['elapsed_seconds'] for x in runs),4),interpretation='local deterministic execution only; no model token, weekly allowance or dollar telemetry; no network calls'),indent=2)+'\n')
counts=json.loads((P/'counts.json').read_text());coverage=json.loads((P/'coverage-summary.json').read_text());summary=dict(counts=counts,pair_completeness=coverage,detailed_cards=32,new_formulations_this_pass=5,pair_specific_recommended_queue=9,validation_checks=26,bulk_investigations=0,complete_scope='bounded catalog/mechanism and selected compatible-pair assessment; not exhaustive discovery',paid_api_calls=0,weekly_allowance='unavailable')
(P/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
