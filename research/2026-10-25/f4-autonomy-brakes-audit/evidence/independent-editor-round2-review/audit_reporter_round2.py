import pathlib,json,csv,collections,decimal,hashlib
D=decimal.Decimal;R=pathlib.Path('/tmp/f4-editor/reporter-round2');x=json.load(open(R/'evidence/live-award-register.json'));a=list(csv.DictReader(open(R/'evidence/reviewed-cases.csv')));disp=list(csv.DictReader(open(R/'evidence/live-candidate-disposition.csv')));calc={}
for c in 'ABC':
 rows=[r for r in a if r['primary_category']==c and r['counted_in_named_case_total']=='True'];active=[r for r in rows if r['record_window_overlaps_cutoff']=='True'];calc[c]={'count':len(rows),'sum':str(sum(D(r['net_obligations_usd']) for r in rows)),'fy24_26':str(sum(D(r['fy2024_2026_obligations_usd']) for r in rows)),'active_count':len(active),'active_sum':str(sum(D(r['net_obligations_usd']) for r in active))}
records=[r for p in x['awards'] for r in p['records']];keys=[r['award_key'] for r in records];rmap={r['award_key']:r for r in records};deltas=[]
for r in a:
 if D(r['net_obligations_usd'])!=D(rmap[r['award_key']]['total_obligation_usd']):deltas.append(r['award_key'])
result={'commit':'9cdcb8e363e138067db42cc6a87383ec336f8dea','reviewed_count':len(a),'disposition_count':len(disp),'retrieved_record_count':len(records),'retrieved_categories':dict(collections.Counter(r.get('award_category') for r in records)),'duplicate_record_keys':{k:v for k,v in collections.Counter(keys).items() if v>1},'reviewed_vs_register_money_deltas':deltas,'selected_totals_recomputed':calc,'disposition_categories':dict(collections.Counter(r['classification'] for r in disp)),'source_hashes':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in R.rglob('*') if p.is_file()}}
L=json.load(open(R/'audit/live-retrieval-log.json'))
def walk(v):
 if isinstance(v,dict):
  if 'url'in v and 'method'in v:yield v
  else:
   for y in v.values():yield from walk(y)
 elif isinstance(v,list):
  for y in v:yield from walk(y)
r=list(walk(L));result['retained_logged_requests']=len(r);result['http_status_counts']=dict(collections.Counter(str(q.get('http_status')) for q in r));result['retained_unique_observations']=len({(q.get('url'),q.get('retrieved_utc'),json.dumps(q.get('request_body'),sort_keys=True)) for q in r});result['sam_direct_request_count']=sum('sam.gov/'in q.get('url','') for q in r);result['sbir_direct_request_count']=sum('sbir.gov/'in q.get('url','') for q in r)
(R/'independent-audit.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='source_hashes'},indent=2))
for p in x['awards']:
 if p['piid'] in ['FA239124CB023','FA239124CB020','FA865022P2333','FA864922P0787','FA95501910169','FA87502321015','N6833524C0261','FA930219P1008']:
  r=p['records'][0];print(p['piid'],r['recipient'],r['total_obligation_usd'],r['period_of_performance'],r['description'])
