import sys
if '--live' in sys.argv:raise SystemExit('Archived v1 pilot: live replay disabled; preserve cumulative ledger and original evidence')
"""New authorized budget; labelled synthetic controls only. No calls on real allegations."""
import sys,pathlib,json,os,urllib.request,sqlite3,hashlib,datetime,math
ROOT=pathlib.Path(__file__).resolve().parents[1]; REPO=ROOT.parents[2]
sys.path.insert(0,str(REPO/'code/ati'));import pipeline as legacy
OUT=ROOT/'jev';OUT.mkdir(exist_ok=True)
legacy.CAP=9_000_000;legacy.OUT=OUT;legacy.VERSION='alberta-seismic-controls-v1'
PRICE={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':'https://docs.typesafe.ai/models','endpoint_source':'https://docs.typesafe.ai/api','model':'jev-1.13.0','input_usd_per_million':0.042,'output_usd':0,'authorized_cap_usd':10,'internal_cap_usd':9,'reservation_per_call_usd':0.003,'auto_retries':0,'new_experiment_authorized':True,'prior_experiments_unchanged':True}
(OUT/'price-verification.json').write_text(json.dumps(PRICE,indent=2)+'\n')
RULE='Fictional fixtures for testing reasoning, not real people or discoveries. Apply only supplied facts. The Fox Creek rule effective 2024-11-19 covers hydraulic fracturing in the mapped area from Duvernay through basement; during fracturing an event ML >= 4.0 within 5 km requires immediate cessation/safe state; restart requires written AER consent. Earlier rule covered Duvernay only. Red Deer SO7 begins 2019-12-09, not the May recommendation. Job windows and monthly volumes/hours cannot prove pumping at any instant. Mw is not ML. MLy is separately labelled corrected local magnitude, not automatically a historical available-to-operator ML measurement. Missing public consent is not proof of no consent. Production is not hydraulic fracturing. Geographic proximity is not causality.'
Q={
 'threshold_trigger_supported':{'type':'noul','instructions':'Do the supplied records establish that an applicable hydraulic-fracturing shutdown threshold was triggered at this well during pumping? Require formation, area, effective date, actual pumping at event, specified magnitude type, distance and detection. Do not infer missing facts.'},
 'post_event_pumping_supported':{'type':'noul','instructions':'Do explicit time-resolved pumping logs in the packet establish hydraulic-fracturing pumping after the earthquake? Date-only job windows, monthly totals and later production do not suffice.'},
 'restart_authorization_unresolved':{'type':'noul','instructions':'If a shutdown-triggered operation resumed, is authorization unresolved on the supplied evidence? Answer no when written applicable consent is supplied or no restart is evidenced. A missing public document is an evidence gap, not proof of absence.'}}
base={'date':'2025-01-15','well':'SYNTHETIC-WELL-A','formation':'Duvernay','in_order_area':True,'operation':'hydraulic fracturing','magnitude':4.0,'magnitude_type':'ML','event_time_utc':'2025-01-15T12:00:00Z','distance_km':2.0,'detection_time_utc':'2025-01-15T12:00:00Z','pumping_logs':'11:50 to 12:00 UTC, stopped immediately; no restart','consent':'not needed without restart'}
cases=[]
def add(id,changes,expected):cases.append({'id':id,'fixture_type':'synthetic','facts':{**base,**changes},'expected':expected})
add('C01-inclusive-threshold-stop',{},[True,False,False])
add('C02-monthly-volume-trap',{'pumping_logs':None,'monthly_volume_m3':15000,'job_window':'2025-01-01 through 2025-01-31','consent':'not publicly found'},[False,False,False])
add('C03-written-consent-restart',{'pumping_logs':'11:50 to 12:00 stopped immediately; resumed at 15:00 UTC','consent':'Written AER consent dated 14:00 UTC authorizes this well and resumed operation'},[True,True,False])
add('C04-Mw-not-ML',{'magnitude_type':'Mw'},[False,False,False])
add('C05-before-expanded-formation',{'date':'2024-11-18','event_time_utc':'2024-11-18T12:00:00Z','detection_time_utc':'2024-11-18T12:00:00Z','formation':'below Duvernay'},[False,False,False])
add('C06-production-is-not-fracturing',{'operation':'production only','pumping_logs':None,'production_logs':'production resumed at 15:00 UTC'},[False,False,False])
add('C07-outside-distance',{'distance_km':5.1},[False,False,False])
add('C08-unresolved-restart-permission',{'pumping_logs':'11:50 to 12:00 stopped; resumed 15:00 UTC','consent':'Search of public portal found no consent; actual consent record unavailable'},[True,True,True])
add('C09-MLy-availability-gap',{'magnitude_type':'MLy','detection_time_utc':None,'note':'current revised catalogue, no historical operator detection record'},[False,False,False])
add('C10-below-inclusive-threshold',{'magnitude':3.99},[False,False,False])
(OUT/'synthetic-controls.json').write_text(json.dumps(cases,indent=2)+'\n')
for c in cases:
 b={'model':legacy.MODEL,'state':{'protocol':RULE,'fixture_id':c['id'],'fixture_type':'synthetic','facts':c['facts']},'questions':Q}
 (OUT/(c['id']+'.request.json')).write_text(json.dumps(b,indent=2)+'\n')
# Save reviewable real evidence-gap requests; do not execute without compliance-testable real packets.
real=json.loads((ROOT/'results/sensitivity-MLy-only.json').read_text())
bywell={}
for c in real:bywell.setdefault(c['job']['UWI'],[]).append(c)
for i,(uwi,cs) in enumerate(sorted(bywell.items()),1):
 b={'model':legacy.MODEL,'state':{'packet_type':'real_indeterminate_evidence_gap_NOT_discovery','sources':['sources/SO7.pdf','sources/SummaryChemical-WaterUse.csv.gz','sources/earthquakes.json','results/sensitivity-MLy-only.json'],'records':cs,'warning':RULE},'questions':{'actionable_gap':{'type':'score','instructions':'Rank only whether identified missing documents could resolve this bounded question; never infer misconduct, historical identity, continuous pumping, magnitude equivalence or absent consent.','criteria':['No specific comparison','Specific but missing operational evidence','Named time-resolved records could resolve applicability/response','Complete records ready for expert review']}}}
 (OUT/(f'R{i:02}-UNSENT.request.json')).write_text(json.dumps(b,indent=2)+'\n')
if '--live' not in sys.argv:print('Prepared payloads only');sys.exit()
if '--pilot' not in sys.argv:
 pilot=json.loads((OUT/'pilot-evaluation.json').read_text())
 if len(pilot)!=3 or not all(r['all_correct'] for r in pilot):raise legacy.GuardError('Pilot failed or incomplete; expansion blocked')
# Strict source verification and supported credential. No secret values in files/errors.
assert any(r.get('name')=='jev-models.html' and r.get('retrieved_utc','')[:10]==datetime.datetime.now(datetime.timezone.utc).date().isoformat() for r in [json.loads(l) for l in (ROOT/'sources/manifest.jsonl').read_text().splitlines()]), 'Reverify current primary pricing before live calls'
assert 'jev-1.13.0' in (ROOT/'sources/jev-models.html').read_text() and '0.042' in (ROOT/'sources/jev-models.html').read_text()
assert os.environ.get('JEV_API_KEY'), 'Existing supported credential missing'
ledger=legacy.Ledger(OUT/'ledger.sqlite',mode='alberta-seismic-new-authorized-2026-10-06')
opener=urllib.request.build_opener(legacy.NoRedirect)
def transport(provider,body):
 if provider!='jev':raise legacy.GuardError('Only Jev authorized')
 req=urllib.request.Request(legacy.ENDPOINTS['jev'],data=legacy.packed(body).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+os.environ['JEV_API_KEY']},method='POST')
 with opener.open(req,timeout=60) as r:
  raw=r.read(2_000_001)
  if len(raw)>2_000_000:raise legacy.GuardError('Oversize response')
  answer=json.loads(raw);answer['_raw_response_utf8']=raw.decode();return answer
client=legacy.Client(ledger,transport)
selected=cases[:3] if '--pilot' in sys.argv else cases
results=[]
for c in selected:
 b=json.loads((OUT/(c['id']+'.request.json')).read_text())
 try:
  response=client.call('jev',b);(OUT/(c['id']+'.response.json')).write_text(json.dumps(response,indent=2)+'\n')
  probs=[response['answers'][k]['noul'] for k in Q];pred=[p>=.5 for p in probs]
  results.append({'id':c['id'],'probabilities':probs,'expected':c['expected'],'predicted':pred,'all_correct':pred==c['expected']})
  print(json.dumps(results[-1]),flush=True)
  if '--pilot' in sys.argv and pred!=c['expected']:print('Pilot failed: stop expansion');break
 except Exception as e:
  print('Stopped without retry:',type(e).__name__,flush=True);break
 finally:ledger.export()
(OUT/('pilot-evaluation.json' if '--pilot' in sys.argv else 'control-evaluation.json')).write_text(json.dumps(results,indent=2)+'\n')
print('Accounted microusd',ledger.totals())
