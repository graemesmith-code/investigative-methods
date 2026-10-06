"""One real, indeterminate evidence-gap assessment. No accusation or compliance schema."""
import pathlib,json,sys,os,urllib.request,datetime,hashlib
P=pathlib.Path(__file__).resolve().parents[1];J=P/'jev';D=J/'gap-only';D.mkdir(exist_ok=True)
sys.path.insert(0,str(P.parents[2]/'code/ati'));import pipeline as b
b.CAP=9_000_000;b.OUT=J;b.VERSION='alberta-gap-only-v1'
if (D/'cluster.response.json').exists():raise SystemExit('Completed gap-only call is archived. Replay and payload overwrite disabled.')
packets=json.loads((P/'results/evidence-packets.json').read_text());cross=json.loads((P/'results/catalogue-crosschecks.json').read_text())
sources=[]
for name in ['sources/SO7.pdf','sources/SummaryChemical-WaterUse.csv.gz','sources/earthquakes.json','sources/nrcan-events.txt','results/evidence-packets.json','results/catalogue-crosschecks.json']:
 sources.append({'id':name,'sha256':hashlib.sha256((P/name).read_bytes()).hexdigest()})
state={'packet_type':'REAL EVIDENCE-GAP REVIEW; ALL PACKETS INDETERMINATE; NOT AN ALLEGATION',
 'fixed_conclusions':['No packet establishes pumping at the earthquake or after it.','No shutdown breach, absent consent, causation or misconduct has been established.','Current names and projected formations do not establish historical operator or actual stimulated interval.','Nine catalogue-event-well packets describe two candidate matched events and three wells, not nine discoveries.','Scores are editorial usefulness heuristics, not calibrated probabilities or legal decisions.'],
 'study_scope':'2020–2025; three rule areas chosen before inspecting entities/results; this Red Deer cluster emerged from data joins.',
 'sources':sources,
 'records':{'current_licences':[{'licence':p['well']['licence'],'uwi':p['well']['uwi'],'target_formation':p['well']['current_licence']['ProjectedFormation']} for p in {p['well']['licence']:p for p in packets}.values()],
 'event_comparisons':[{'NRCan_id':c['NRCan']['id'],'NRCan_time':c['NRCan']['time'],'NRCan_mag':c['NRCan']['magnitude'],'NRCan_type':c['NRCan']['magnitude_type'],'AGS_matched_id':c['candidate_matches'][0]['AGS']['object_id'],'AGS_MLy':c['candidate_matches'][0]['AGS']['MLy'],'AGS_industry_M':c['candidate_matches'][0]['AGS']['M'],'match_seconds':c['candidate_matches'][0]['seconds_difference'],'match_distance_km':c['candidate_matches'][0]['horizontal_km_difference']} for c in cross],
 'timing':'Only date-window summaries, including2025-02-15 to2025-02-28 and narrower windows, are supplied. Exact Start_Date/End_Date derivation is not independently verified; they are neither established continuous-pumping intervals nor assumed rig dates.',
 'space_and_rule':'Both surface and bottomhole coordinates in SO7 AppendixB outsideA; all candidate distances roughly1.04–3.33km. Licence target Duvernay, actual stimulated interval/trajectory missing. Rule begins2019-12-09; inclusive3ML red clause. Red clause does not explicitly repeat5km; screen is bounded, not exhaustive rule interpretation.',
 'permissions':'No stop/restart logs or written consent supplied. Public IAR searches returned0applications; not proof no permission exists.',
 'control_warning':'Jev missed explicit positive pumping examples in synthetic tests. It must not infer any pumping or permission fact here.'}}
criteria=['Low: would not resolve a material uncertainty in this packet','Useful background, but not decisive for this bounded question','Material: narrows one identified uncertainty','Essential: needed to test the event/operation/response comparison']
questions={k:{'type':'score','instructions':text+' Rank ONLY the usefulness of acquiring the specified evidence from the cited packet. Never score likelihood of misconduct or invent facts. All fixed conclusions are mandatory.','criteria':criteria} for k,text in {
 'time_resolved_operations':'How useful are original stage-level pumping/stop records and the actual stimulated interval/formation?',
 'contemporaneous_magnitude':'How useful are contemporaneous seismic detection reports and the basis for the NRCan/AGS magnitude disagreement?',
 'historical_identity':'How useful are dated licence-transfer/operator records identifying who controlled these operations at the event?',
 'window_schema':'How useful is the official derivation of the summary Start_Date/End_Date and Number_Of_Stages fields, compared with original fracture dates?'
}.items()}
payload={'model':b.MODEL,'state':state,'questions':questions};raw=json.dumps(payload,indent=2)+'\n';(D/'cluster.request.json').write_text(raw)
(D/'request-cost-bound.json').write_text(json.dumps({'requests':1,'request_bytes':len(b.packed(payload).encode()),'reservation_usd':.003,'full_64000_input_token_list_price_usd':.002688,'actual_input_tokens_unknown_before_call':True,'paid_replay_disabled_by_cache_and_persistent_ledger':True},indent=2)+'\n')
if '--live' not in sys.argv:print('Prepared real gap-only request');sys.exit()
assert (J/'ledger.sqlite').exists(),'Existing ledger required'
assert len(json.loads((J/'v2/evaluation.json').read_text()))==12,'Balanced control review required'
assert any(json.loads(l).get('name')=='jev-models.html' and json.loads(l).get('retrieved_utc','')[:10]==datetime.datetime.now(datetime.timezone.utc).date().isoformat() for l in (P/'sources/manifest.jsonl').read_text().splitlines()),'Reverify current pricing'
ledger=b.Ledger(J/'ledger.sqlite',mode='alberta-seismic-new-authorized-2026-10-06');op=urllib.request.build_opener(b.NoRedirect)
def transport(provider,body):
 assert provider=='jev' and os.environ.get('JEV_API_KEY')
 req=urllib.request.Request(b.ENDPOINTS['jev'],data=b.packed(body).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+os.environ['JEV_API_KEY']},method='POST')
 with op.open(req,timeout=60) as r:
  data=r.read(2_000_001)
  if len(data)>2_000_000:raise b.GuardError('Oversize response')
  x=json.loads(data);x['_raw_response_utf8']=data.decode();return x
try:
 answer=b.Client(ledger,transport).call('jev',payload);(D/'cluster.response.json').write_text(json.dumps(answer,indent=2)+'\n')
 summary={'classification':'indeterminate','no_compliance_decision':True,'interpretation':'Editorial gap-importance scores only. These do not establish facts or calibrate reporting success.','scores':{k:v['score'] for k,v in answer['answers'].items()}}
 (D/'guarded-result.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
except Exception as e:print('Stopped with no retry:',type(e).__name__)
finally:ledger.export();print('Cumulative microusd',ledger.totals())
