"""New post-workspace-loss independent checks; offline only. Not original lost script."""
import pathlib,csv,json,collections,xml.etree.ElementTree as E,hashlib,types,tempfile,contextlib,io,unittest.mock as mock
from decimal import Decimal as D
R=pathlib.Path(__file__).parent;S=R/'sources';csv.field_size_limit(2**31-1)
def rows(p):return list(csv.DictReader((S/p).open()))
out={'status':'new independent recheck of pinned public a0ed4b2 sources; not byte-identical recovery of lost review artifacts','issues':[]}
act=rows('evidence/fpds-verified-actions.csv');groups=collections.defaultdict(list)
for a in act:groups[a['award_key']].append(a)
ids=[tuple(a[k] for k in ['agency_id','piid','parent_agency_id','parent_piid','modification','transaction']) for a in act];assert len(ids)==len(set(ids))
live=json.load(open(S/'evidence/live-award-register.json'));lm={r['award_key']:r for a in live['awards'] for r in a.get('records',[])}
combined=rows('evidence/combined-live-inventory.csv');cm={r['award_key']:r for r in combined};assert len(cm)==len(combined)
checks=[]
for k,aa in groups.items():
 v=lm[k];r=cm[k]
 windows=[('total_obligation_usd',None,None),('fy2019_2026_fpds_obligations_usd','2018-10-01','2026-09-30'),('fy2024_2026_fpds_obligations_usd','2023-10-01','2026-09-30'),('cy2024_2026_to_cutoff_fpds_obligations_usd','2024-01-01','2026-10-25')]
 for f,lo,hi in windows:
  actual=sum((D(a['obligation_usd']) for a in aa if lo is None or lo<=a['signed_date'][:10]<=hi),D(0));ok=actual==D(v[f]);checks.append(ok)
  if not ok:out['issues'].append({'kind':'standard_action_sum','key':k,'field':f,'computed':str(actual),'reported':v[f]})
 dates={'last_public_action_date':max(a['signed_date'][:10] for a in aa),'last_positive_obligation_date':max((a['signed_date'][:10] for a in aa if D(a['obligation_usd'])>0),default='')}
 dates.update(net_calendar2026_obligations_usd=str(sum((D(a['obligation_usd']) for a in aa if a['signed_date'].startswith('2026')),D(0))),positive_calendar2026_increments_usd=str(sum((D(a['obligation_usd']) for a in aa if a['signed_date'].startswith('2026') and D(a['obligation_usd'])>0),D(0))))
 for f,vv in dates.items():
  ok=D(vv)==D(r[f]) if f.endswith('_usd') else vv==r[f];checks.append(ok)
  if not ok:out['issues'].append({'kind':'date_or_current_year_sum','key':k,'field':f,'computed':vv,'reported':r[f]})
out['standard_actions']={'rows':len(act),'unique_full_identities':len(set(ids)),'award_groups':len(groups),'comparison_count':len(checks),'all_comparisons_pass':all(checks),'standard_live_keys':len(lm),'combined_live_rows':len(cm),'note':'Independent arithmetic against published exports; not fresh agency retrieval of all 86 award histories.'}
ns={'a':'http://www.w3.org/2005/Atom','f':'https://www.fpds.gov/FPDS'}
exports=rows('evidence/ota-verified-actions.csv')+rows('evidence/ota-keyword-followup-actions.csv');em={tuple(x[k] for k in ['agency_id','piid','modification','transaction_number']):x for x in exports};assert len(exports)==len(em)
parsed=[];bodychecks=[]
fields={'agency_id':'OtherTransactionIDVID/OtherTransactionIDVContractID/agencyID','piid':'OtherTransactionIDVID/OtherTransactionIDVContractID/PIID','modification':'OtherTransactionIDVID/OtherTransactionIDVContractID/modNumber','transaction_number':'OtherTransactionIDVID/OtherTransactionIDVContractID/transactionNumber','signed_date':'contractDetail/relevantContractDates/signedDate','effective_date':'contractDetail/relevantContractDates/effectiveDate','current_end':'contractDetail/relevantContractDates/currentCompletionDate','potential_end':'contractDetail/relevantContractDates/ultimateCompletionDate','action_obligation_usd':'contractDetail/dollarValues/obligatedAmount','aggregate_obligations_usd':'contractDetail/totalDollarValues/totalObligatedAmount','action_exercised_value_usd':'contractDetail/dollarValues/baseAndExercisedOptionsValue','action_all_options_value_usd':'contractDetail/dollarValues/baseAndAllOptionsValue','aggregate_exercised_value_usd':'contractDetail/totalDollarValues/totalBaseAndExercisedOptionsValue','aggregate_all_options_value_usd':'contractDetail/totalDollarValues/totalBaseAndAllOptionsValue','description':'contractDetail/contractData/descriptionOfContractRequirement','agreement_type':'contractDetail/contractData/typeOfAgreement','recipient':'contractDetail/vendor/vendorHeader/vendorName'}
for b in json.load(open(R/'ot-response-manifest.json'))['bodies']:
 p=S/b['public_path'];raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==b['sha256'];root=E.fromstring(raw);assert not root.findall("a:link[@rel='next']",ns)
 for e in root.findall('a:entry',ns):
  z=e.find('a:content/f:OtherTransactionIDV',ns);assert z is not None
  r={k:z.findtext('/'.join('f:'+v for v in path.split('/')),default='',namespaces=ns) for k,path in fields.items()};key=tuple(r[k] for k in ['agency_id','piid','modification','transaction_number']);target=em[key]
  for k,v in r.items():
   ok=D(v)==D(target[k]) if k.endswith('_usd') else v==target[k];bodychecks.append(ok)
   if not ok:out['issues'].append({'kind':'OT_xml_vs_export','identity':key,'field':k,'xml':v,'export':target[k]})
  parsed.append(r)
pg=collections.defaultdict(list)
for a in parsed:pg[a['piid']].append(a)
ots=[]
for k,aa in sorted(pg.items()):
 total=sum((D(a['action_obligation_usd']) for a in aa),D(0));aggs={a['aggregate_obligations_usd'] for a in aa};assert len(aggs)==1;aggregate=D(next(iter(aggs)));last=max(aa,key=lambda x:(x['signed_date'],x['modification']));otrow=next(r for r in combined if r['piid']==k)
 for f,v in [('visible_ot_action_obligations_usd',total),('ot_feed_aggregate_obligations_usd',aggregate),('ot_aggregate_minus_actions_usd',aggregate-total)]:
  if D(otrow[f])!=v:out['issues'].append({'kind':'OT_combined_inventory','piid':k,'field':f})
 if aggregate!=total and otrow['net_obligations_usd']!='':out['issues'].append({'kind':'OT_unreconciled_net_not_blank','piid':k})
 ots.append({'piid':k,'actions':len(aa),'visible_action_sum_usd':str(total),'feed_aggregate_usd':str(aggregate),'aggregate_minus_actions_usd':str(aggregate-total),'current_end':last['current_end'],'potential_end':last['potential_end'],'latest_action':last['signed_date'],'last_positive_action':max(x['signed_date'] for x in aa if D(x['action_obligation_usd'])>0)})
out['OT_primary_reparse']={'xml_bodies':6,'actions':len(parsed),'fields_compared':len(bodychecks),'all_fields_pass':all(bodychecks),'four_unresolved_aggregate_discrepancies':sum(D(x['aggregate_minus_actions_usd'])!=0 for x in ots),'instruments':ots}
case=rows('evidence/reviewed-cases.csv');cg=collections.defaultdict(list)
for r in case:
 if r['counted_in_named_case_total']=='True':cg[r['primary_category']].append(r)
out['selected_case_totals']={k:{'count':len(aa),'cumulative_usd':str(sum((D(x['net_obligations_usd']) for x in aa),D(0)))} for k,aa in cg.items()}
adj=[r for r in case if r['scope_tier']=='normative_autonomy_adjacent_weapons_application_unverified'];out['adjacent_case_total']={'count':len(adj),'cumulative_usd':str(sum((D(r['net_obligations_usd']) for r in adj),D(0)))}
out['formerly_blank_technical_url_rows']=[{'piid':r['piid'],'technical_source_urls':r['technical_source_urls'],'technical_review_depth':r['technical_review_depth']} for r in combined if r['piid'] in ['FA87502321015','FA95501910169']]
ledger=rows('audit/exa-query-cost-log.csv');used=D(0);reported=D(0)
for n,r in enumerate(ledger,1):
 used+=D(r['budget_debit_usd']);reported+=D(r['response_reported_usd'] or 0);assert int(r['sequence'])==n and D(r['new_cumulative_usd'])==used and D(r['all_cumulative_usd'])==used+D('4.095')
assert len({r['response_sha256'] for r in ledger})==len(ledger)
out['cost_ledger']={'rows':len(ledger),'endpoints':dict(collections.Counter(r['endpoint'] for r in ledger)),'new_reserved_debit_usd':str(used),'provider_reported_estimate_usd':str(reported),'cumulative_exposure_usd':str(used+D('4.095')),'statuses':dict(collections.Counter(r['status'] for r in ledger)),'invoice_total':'unknown'}
# Execute the unmodified published runner, with only filesystem globals and HTTP stubbed.
# Suppress module-import private-directory creation, then route all test files to a temporary directory.
module=types.ModuleType('isolated_exa_test');module.__file__=str(S/'code/exa_serial.py')
with mock.patch.object(pathlib.Path,'mkdir',return_value=None):exec(compile((S/'code/exa_serial.py').read_bytes(),module.__file__,'exec'),module.__dict__)
class Response:
 def __init__(self,c):self.c=c
 def __enter__(self):return self
 def __exit__(self,*a):pass
 def read(self):return json.dumps({'costDollars':{'total':self.c},'results':[]}).encode()
tests=[]
for name,cost,contents in [('normal',.007,False),('cache_zero',0,True),('over_reservation',.02,False),('timeout',None,False),('ceiling',.007,False)]:
 with tempfile.TemporaryDirectory(prefix='f4-offline-') as td:
  t=pathlib.Path(td);module.PRIVATE=t;module.STOP=t/'STOP';module.LOG=t/'ledger.csv';calls=[]
  if name=='ceiling':
   with module.LOG.open('w') as f:w=csv.DictWriter(f,fieldnames=module.FIELDS);w.writeheader();w.writerow({'budget_debit_usd':'10.905'})
  def fake(*a,**kw):
   calls.append(1)
   if name=='timeout':raise TimeoutError('simulated timeout, no network')
   return Response(cost)
  errors=[]
  with mock.patch.object(module.urllib.request,'urlopen',side_effect=fake),mock.patch.dict(module.os.environ,{'EXA_API_KEY':'offline-test-unused'}),contextlib.redirect_stdout(io.StringIO()):
   try:module.run('https://example.invalid/offline-fixture',contents)
   except Exception as e:errors.append(type(e).__name__)
   if name=='over_reservation':
    try:module.run('second offline fixture')
    except Exception as e:errors.append(type(e).__name__)
  rr=list(csv.DictReader(module.LOG.open()));last=rr[-1]
  if name=='normal':assert last['budget_debit_usd']=='0.007' and len(calls)==1
  if name=='cache_zero':assert last['budget_debit_usd']=='0.001' and len(calls)==1
  if name=='over_reservation':assert last['budget_debit_usd']=='0.02' and module.STOP.exists() and len(calls)==1 and len(errors)==2
  if name=='timeout':assert last['budget_debit_usd']=='0.007' and last['status']=='uncertain_no_retry' and len(calls)==1
  if name=='ceiling':assert len(calls)==0 and len(errors)==1
  tests.append({'test':name,'passed':True,'fake_HTTP_calls':len(calls),'real_network_calls':0})
out['offline_runner_tests']=tests
out['scope_tiers']=dict(collections.Counter(r['scope_tier'] for r in combined))
report=(S/'report.md').read_text();out['small_fix_presence']={'functional_lead_january_2027':'January 1, 2027 designation' in report,'framework_june_2027':'June 1, 2027 framework' in report,'current_IDA_disclosure':'ongoing IDA consulting' in report,'CP_CoE_filename_not_date':'filename date is not treated as a verified publication date' in report,'Bode_accessed_at_cutoff':'university profile accessed at cutoff' in report}
(R/'post-loss-independent-recheck.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));assert not out['issues']
