"""Offline audit of saved, non-secret project evidence. No network or model calls.
Counts ledger attempts once, not duplicate response files or cache hits.
Does not inspect environment credentials, session logs or platform internals.
"""
import json,pathlib,collections,hashlib
P=pathlib.Path(__file__).resolve().parent
out={'scope':'This lobbying experiment only; previous sanctions-pilot spend excluded. Whole platform/model usage is unavailable.','stages':[],'inputs':[]}
def load(f):
 raw=f.read_bytes();out['inputs'].append({'path':str(f.relative_to(P.parents[2])),'sha256':hashlib.sha256(raw).hexdigest()});return json.loads(raw)
for stage in ['lobbying-control-pilot','lobbying-control-expansion']:
 d=load(P.parent/stage/'jev/ledger.json');a=d['attempts'];u=[json.loads(x['usage']) for x in a]
 assert all(x['status']=='success' for x in a)
 out['stages'].append({'stage':stage,'calls':len(a),'request_models':sorted({json.loads(x['request'])['model'] for x in a}),'response_models':sorted({json.loads(x['response'])['model'] for x in a}),'reported_input_tokens':sum(x['input_tokens'] for x in u),'reported_output_tokens':sum(x['output_tokens'] for x in u),'estimated_cost_microusd_sum_attempts':sum(x['accounted'] for x in a),'reservation_microusd_sum_attempts':sum(x['reserve'] for x in a)})
out['jev_totals']={k:sum(x[k] for x in out['stages']) for k in ['calls','reported_input_tokens','reported_output_tokens','estimated_cost_microusd_sum_attempts','reservation_microusd_sum_attempts']}
out['jev_totals']['reported_total_tokens']=out['jev_totals']['reported_input_tokens']+out['jev_totals']['reported_output_tokens']
out['whole_experiment_tokens']={'value':None,'credible_upper_bound':None,'reason':'No telemetry for parent conversation, executor reasoning, native/cloud reviews, tools or prior source-inventory creation. File lengths and remaining weekly percentage do not reconstruct billed/model-processed tokens.'}
out['openai_execution_model_ids']={'value':None,'reason':'No deployment model IDs recorded in these ledgers. Parent reports no explicit model overrides; platform labels/defaults do not establish actual execution identities.'}
a=load(P/'all-original-interest-audit.json');out['lda_original_report_year_counts']=dict(sorted(collections.Counter(str(x['year']) for x in a).items()));assert sum(out['lda_original_report_year_counts'].values())==4143
out['house_archive_scope']=load(P/'archive-scope.json');out['fara_provenance']=load(P/'supplied-source-provenance.json');out['client_match_coverage']=load(P/'full-match-coverage.json');out['role_match_coverage']=load(P/'full-role-coverage.json')
assert out['jev_totals']['calls']==50 and out['jev_totals']['reported_total_tokens']==83052
(P/'methodology-audit.json').write_text(json.dumps(out,indent=2));print(json.dumps(out['jev_totals'],indent=2))
