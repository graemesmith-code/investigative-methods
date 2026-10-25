#!/usr/bin/env python3
"""Compare parallel screens of the SAME inputs without adding populations/money.

Only exact source/award keys are joined. No PIID, recipient-name or fuzzy merge is
allowed. Differing lexical memberships are provenance, not a second transaction.
The public membership index retains keys and source-row numbers, not descriptions.
Neither source register is modified.
"""
from __future__ import annotations
import argparse,csv,datetime,gzip,hashlib,io,json,pathlib,re,sys
from decimal import Decimal,InvalidOperation

P=pathlib.Path(__file__).resolve().parents[1]
csv.field_size_limit(sys.maxsize)
WINDOWS=('fy2019_2026','fy2024_2026','cy2024_2026')

def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def norm(s):return re.sub('[^a-z0-9]','',s.lower())

def choose(headers,explicit,aliases,label,optional=False):
 if explicit:
  if explicit not in headers:raise ValueError(f'{label} column {explicit!r} missing')
  return explicit
 for a in aliases:
  hits=[h for h in headers if norm(h)==norm(a)]
  if len(hits)==1:return hits[0]
 if optional:return None
 raise ValueError(f'Cannot identify {label}; specify column explicitly. Headers: {headers}')

def keykind(key):
 if key.startswith('CONT_AWD_'):return 'complete_procurement_award_key'
 if key.startswith('ASST_NON_'):return 'complete_assistance_award_key'
 if key.startswith('CONT_IDV_'):return 'parent_instrument_key'
 return 'source_or_document_key_not_proven_distinct_award'

def money(value,unit):
 if value is None or str(value).strip() in ('','None','null','NULL'):return None
 d=Decimal(str(value).replace(',','').replace('$','').strip())
 if not d.is_finite():raise ValueError('nonfinite monetary value')
 scaled=d*(100 if unit=='dollars' else 1)
 if scaled!=scaled.to_integral_value():raise ValueError('monetary value has fractional cents')
 return int(scaled)

def read_register(path,side,args):
 before=sha(path);raw=path.open('rb');payload=gzip.GzipFile(fileobj=raw) if path.suffix=='.gz' else raw
 text=io.TextIOWrapper(payload,encoding='utf-8',newline='');reader=csv.DictReader(text);headers=reader.fieldnames or []
 keycol=choose(headers,getattr(args,side+'_key_column'),['award_key','register_key','candidate_key','key'],'key')
 categorycol=choose(headers,None,['all_categories_preliminary','automated_categories','categories','category_tags','category_preliminary','primary_category_preliminary'],'category',True)
 moneycols={};units={}
 for window in WINDOWS:
  explicit=getattr(args,side+'_'+window+'_column')
  aliases=[f'obligation_cents_{window}',f'obligations_cents_{window}',f'net_obligations_cents_{window}',f'obligations_{window}_usd',f'obligation_usd_{window}',f'net_obligations_{window}_usd',f'net_obligations_usd_{window}']
  col=choose(headers,explicit,aliases,window,True);moneycols[window]=col
  supplied=getattr(args,side+'_money_unit')
  units[window]=supplied or ('cents' if col and 'cent' in col.lower() else 'dollars' if col and any(x in col.lower() for x in ('usd','dollar')) else None)
  if col and units[window] is None:raise ValueError(f'Unclear unit for {side} {col}; specify --{side}-money-unit')
 rows={};dups=[];errors=[];blankkeys=[];n=0
 for n,r in enumerate(reader,1):
  key=(r.get(keycol) or '').strip()
  if not key:blankkeys.append(n);continue
  values={}
  for window,col in moneycols.items():
   try:values[window]=money(r.get(col),units[window]) if col else None
   except (ValueError,InvalidOperation) as e:values[window]=None;errors.append({'row':n,'key':key,'column':col,'error':str(e)})
  slim={'source_data_row':n,'category_raw':r.get(categorycol,'') if categorycol else '',**values}
  if key in rows:dups.append({'key':key,'first_row':rows[key]['source_data_row'],'duplicate_row':n,'money_equal':all(rows[key][w]==slim[w] for w in WINDOWS)})
  else:rows[key]=slim
 text.close();raw.close();after=sha(path)
 return rows,{'path':str(path),'sha256':before,'sha256_after_read':after,'stable_during_read':before==after,'physical_data_rows':n,'unique_exact_keys':len(rows),'blank_key_rows':blankkeys,'duplicate_key_observations':dups,'monetary_parse_errors':errors,'key_column':keycol,'category_column':categorycol,'money_columns':moneycols,'money_units':units,'fieldnames':headers,'key_kind_counts':{k:sum(keykind(x)==k for x in rows) for k in sorted({keykind(x) for x in rows})}}

def run(args):
 root,ra=read_register(args.root,'root',args);ind,ia=read_register(args.independent,'independent',args)
 for side,a,expected in [('root',ra,args.root_expected_sha256),('independent',ia,args.independent_expected_sha256)]:
  if expected and a['sha256']!=expected:raise ValueError(f'{side} input SHA256 differs from expected')
 common=sorted(root.keys()&ind.keys());onlyroot=sorted(root.keys()-ind.keys());onlyind=sorted(ind.keys()-root.keys())
 comparisons={}
 for w in WINDOWS:
  valid=[];different=[];missing=[];nullzero=[]
  for k in common:
   if keykind(k) not in ('complete_procurement_award_key','complete_assistance_award_key'):continue
   a,b=root[k][w],ind[k][w]
   if a is None or b is None:
    if (a is None and b==0) or (b is None and a==0):nullzero.append(k)
    else:missing.append(k)
   elif a==b:valid.append(k)
   else:different.append({'award_key':k,'root_cents':a,'independent_cents':b,'difference_cents':a-b,'root_source_data_row':root[k]['source_data_row'],'independent_source_data_row':ind[k]['source_data_row']})
  comparisons[w]={'both_nonnull_equal':len(valid),'both_nonnull_differences':different,'one_or_both_values_missing':len(missing),'null_versus_explicit_zero_representation_pairs':len(nullzero),'null_zero_keys':nullzero,'no_zero_imputation':'Blank/missing is preserved; null-vs-zero pairs are not silently classified as financial errors or silently filled.'}
 status='compared_stable_snapshots' if ra['stable_during_read'] and ia['stable_during_read'] else 'inputs_changed_retry_required'
 out={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':status,'scope':'Independent lexical passes over overlapping/same supplied corpus. Exact-key union is a discovery index, NOT distinct verified programs and NOT a sum of money or independent source populations. No source register was modified.','root':ra,'independent':ia,'membership':{'intersection_exact_keys':len(common),'root_only_exact_keys':len(onlyroot),'independent_only_exact_keys':len(onlyind),'union_exact_keys':len(root.keys()|ind.keys()),'complete_financial_keys_intersection':sum(keykind(k) in ('complete_procurement_award_key','complete_assistance_award_key') for k in common),'root_only_by_kind':{kind:sum(keykind(k)==kind for k in onlyroot) for kind in sorted(set(map(keykind,onlyroot)))},'independent_only_by_kind':{kind:sum(keykind(k)==kind for k in onlyind) for kind in sorted(set(map(keykind,onlyind))) }},'comparable_integer_cent_windows':comparisons,'interpretation':['Source-specific SBIR/document keys may refer to the same real award and are not merged by PIID alone.','Different automatic categories or lexical memberships require review; neither establishes actual safeguard scope.','A parent-only hit should remain available as an independent-screen provenance edge/lead, not create a second financial action.','No combined safeguards-dollar total is produced. Financial actions must be aggregated once by complete canonical transaction identity.']}
 args.audit.parent.mkdir(parents=True,exist_ok=True);args.audit.write_text(json.dumps(out,indent=2)+'\n')
 if status!='inputs_changed_retry_required':
  args.membership.parent.mkdir(parents=True,exist_ok=True)
  fields=['award_or_source_key','key_kind','membership','root_source_data_row','independent_source_data_row','root_category_raw','independent_category_raw']
  with args.membership.open('w',newline='',encoding='utf-8') as f:
   wr=csv.DictWriter(f,fieldnames=fields);wr.writeheader()
   for k in sorted(root.keys()|ind.keys()):
    a,b=root.get(k,{}),ind.get(k,{})
    wr.writerow(dict(zip(fields,[k,keykind(k),'both' if a and b else 'root_only' if a else 'independent_only',a.get('source_data_row',''),b.get('source_data_row',''),a.get('category_raw',''),b.get('category_raw','')])))
 # Optional complete logical membership index adds the already audited standard
 # live/OTA source identities. It remains a source/instrument-key union, never a
 # unique-program count, a PIID-only merge or a monetary aggregation.
 if args.available_membership and status!='inputs_changed_retry_required':
  avbefore=sha(args.available_membership)
  with args.available_membership.open(newline='',encoding='utf-8') as f:available={r['exact_award_or_source_identity']:r for r in csv.DictReader(f)}
  avafter=sha(args.available_membership)
  combined=sorted(set(root)|set(ind)|set(available));patterns={}
  args.combined_membership.parent.mkdir(parents=True,exist_ok=True)
  fields=['exact_award_or_source_identity','canonical_archive_screen','independent_stage1_screen','standard_live_record','FPDS_other_transaction_record','root_source_data_row','independent_source_data_row','root_category_raw','independent_category_raw','money_combination_permitted','scope_note']
  with args.combined_membership.open('w',newline='',encoding='utf-8') as f:
   wr=csv.DictWriter(f,fieldnames=fields);wr.writeheader()
   for k in combined:
    av=available.get(k,{});members={x.strip() for x in av.get('membership','').split(';') if x.strip()};flags=[k in root,k in ind,'standard_live_record' in members,'FPDS_other_transaction_record' in members]
    pattern=';'.join(label for label,yes in zip(fields[1:5],flags) if yes);patterns[pattern]=patterns.get(pattern,0)+1
    wr.writerow(dict(zip(fields,[k,*flags,root.get(k,{}).get('source_data_row',''),ind.get(k,{}).get('source_data_row',''),root.get(k,{}).get('category_raw',''),ind.get(k,{}).get('category_raw',''),False,'Exact source/instrument-key membership, not distinct awards/programs; no financial sum or fuzzy cross-schema merge'])))
  out['combined_available_membership']={'available_input':str(args.available_membership),'available_sha256':avbefore,'available_sha256_after_read':avafter,'available_stable_during_read':avbefore==avafter,'union_exact_source_or_instrument_keys':len(combined),'source_membership_patterns':patterns,'independent_keys_not_in_available_view':len(set(ind)-set(available)),'available_keys_not_in_either_archive_screen':len(set(available)-set(root)-set(ind)),'output':str(args.combined_membership),'scope':'Available view includes exact standard live and OTA identities; all populations overlap and cannot be summed as unique awards or money.'}
  if avbefore!=avafter:out['status']='inputs_changed_retry_required';status=out['status']
  args.audit.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'status':status,'membership':out['membership'],'money_comparisons':{w:{k:v for k,v in a.items() if k not in ('null_zero_keys','both_nonnull_differences')}|{'both_nonnull_difference_count':len(a['both_nonnull_differences'])} for w,a in comparisons.items()},'audit':str(args.audit),'membership_index':str(args.membership)},indent=2))
 if status=='inputs_changed_retry_required':return 3
 if ra['blank_key_rows'] or ia['blank_key_rows'] or ra['monetary_parse_errors'] or ia['monetary_parse_errors'] or any(not r['money_equal'] for r in ra['duplicate_key_observations']+ia['duplicate_key_observations']):return 2
 return 0

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--root',type=pathlib.Path,default=P/'evidence/brakes-candidate-register.csv');a.add_argument('--independent',type=pathlib.Path,required=True);a.add_argument('--audit',type=pathlib.Path,default=P/'audit/parallel-register-reconciliation.json');a.add_argument('--membership',type=pathlib.Path,default=P/'evidence/parallel-key-membership.csv');a.add_argument('--available-membership',type=pathlib.Path);a.add_argument('--combined-membership',type=pathlib.Path,default=P/'evidence/combined-key-membership.csv')
 for side in ('root','independent'):
  a.add_argument('--'+side+'-key-column');a.add_argument('--'+side+'-money-unit',choices=('cents','dollars'));a.add_argument('--'+side+'-expected-sha256')
  for window in WINDOWS:a.add_argument('--'+side+'-'+window.replace('_','-')+'-column',dest=side+'_'+window+'_column')
 sys.exit(run(a.parse_args()))
