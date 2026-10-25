#!/usr/bin/env python3
"""Bind audited logical Stage1 results to exact final public physical files.
This prepares only a rule set; assemble_text_v2 enforces final publication gate.
"""
import argparse,collections,gzip,hashlib,json,pathlib

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--inventory',required=True);ap.add_argument('--snapshot',required=True);ap.add_argument('--stage1-prefix',required=True);ap.add_argument('--coverage',required=True);ap.add_argument('--transport-rules',required=True);ap.add_argument('--base-rules');ap.add_argument('--output',required=True);ap.add_argument('--binding-output',required=True);a=ap.parse_args()
 inv=json.loads(pathlib.Path(a.inventory).read_text());root=pathlib.Path(a.snapshot);cov=pathlib.Path(a.coverage);prefix=a.stage1_prefix.rstrip('/')+'/'
 frozen=json.loads((cov/'frozen-artifact-rules.json').read_text());whitelist=json.loads((cov/'DELIVERY-MANIFEST.json').read_text());sm=json.loads((cov/'supplemental-source-map.json').read_text());rules=json.loads(pathlib.Path(a.base_rules).read_text()) if a.base_rules else {'files':[],'supplements':[]}
 transport=json.loads(pathlib.Path(a.transport_rules).read_text());rules['files']+=transport['files'];rules.setdefault('coverage_proofs',[]).extend(transport['coverage_proofs'])
 files={x['path'][len(inv['root']):]:x for x in inv['files']};sources={p:sha(root/p) for p in files if p.startswith(prefix)};bindings={};special=[];physical_full=set()
 for x in frozen['rules']:
  exact=prefix+x['path'];choices=[p for p,h in sources.items() if h==x['sha256']];binding='exact physical bytes'
  if exact in choices:physical=exact
  elif choices:physical=sorted(choices)[0]
  elif not x['path'].endswith('.gz') and exact+'.gz' in sources:
   physical=exact+'.gz';h=hashlib.sha256();n=0
   with gzip.open(root/physical,'rb') as f:
    for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
   assert h.hexdigest()==x['sha256'] and n==x['bytes'],'Not exact gzip counterpart: '+x['path'];binding='exact decompressed bytes from published gzip'
  else:raise AssertionError('Frozen logical file lacks verified public representation: '+x['path'])
  bindings[x['path']]={'logical_path':x['path'],'logical_bytes':x['bytes'],'logical_sha256':x['sha256'],'published_path':physical,'published_sha256':sources[physical],'binding':binding,'action':x['action']}
  special.append((x,physical))
 def ps(s):
  if s in bindings:return [bindings[s]['published_path']]
  if s+'.gz' in bindings:return [bindings[s+'.gz']['published_path']]
  if s=='audit/excluded-observations.jsonl.gz':return [v['published_path'] for k,v in sorted(bindings.items()) if k.startswith('audit/excluded-observations.part-')]
  raise AssertionError('Unbound logical dependency '+s)
 def p(s):
  paths=ps(s);assert len(paths)==1;return paths[0]
 core=p('evidence/brakes-candidate-register.csv');cont=p('evidence/asimov-performer-continuation-local-2025-2026.csv')
 body_targets={core,cont,p('evidence/candidate-financial-transactions.csv.gz')}
 def supplement(n):return 'text-coverage/'+n
 sharedproof={'coverage_proof':supplement('current-coverage-proof.json'),'frozen_manifest_sha256':frozen['package_manifest_sha256'],'fresh_current_results_only':True}
 overrides={}
 for x,physical in special:
  action=x['action'];r={'path':physical,'expected_sha256':sources[physical],'reason':x['reason'],'proof':dict(sharedproof)};target=None
  if physical in body_targets:
   r['representation']='full_decompressed_utf8' if physical.endswith('.gz') else 'full_utf8';r['reason']='Complete canonical CSV body retained once; exact logical bytes verified against frozen source. '+r['reason'];r['proof']['logical_sha256']=next(y['logical_sha256'] for y in bindings.values() if y['published_path']==physical and not y['logical_path'].endswith('.gz')) if physical in (core,cont) else x.get('logical_uncompressed_sha256',x['sha256'])
  elif action in ('retain_original_text_once','retain_complete_current_calibration_JSON_once'):
   continue
  elif action=='catalogue_verified_gzip_CSV_alias':
   r['representation']='gzip_exact_mirror';target=core if 'brakes-candidate-register' in x['path'] else cont
  elif action=='catalogue_verified_equivalent_JSON_alias':
   r['representation']='typed_CSV_equivalent';target=[core,supplement('candidate-csv-type-schema.json'),supplement('reconstruct_typed_csv.py')] if 'brakes-candidate-register' in x['path'] else [cont,supplement('continuation-csv-type-schema.json'),supplement('reconstruct_typed_csv.py')]
  elif action=='catalogue_exact_core_subset_or_projection':
   r['representation']='verified_core_subset';target=[core,supplement('candidate-csv-type-schema.json')]
   if 'ab-high-priority' in x['path']:target.append(supplement('ab-review-order-keys.json'))
  elif action=='retain_complete_typed_CSV_once_catalogue_JSONL_alias':
   r['representation']='typed_CSV_equivalent';target=[supplement('candidate-provenance-complete.csv'),supplement('provenance-csv-type-schema.json'),supplement('reconstruct_typed_csv.py')]
  elif action=='catalogue_original_payload_retain_complete_derived_results':
   r['representation']='source_holding_catalogued';target=[supplement('machine-hit-results-compact.csv'),supplement('machine-hit-compact-schema.json'),supplement('machine-hit-unique-facts.jsonl'),supplement('candidate-provenance-complete.csv')]
  elif action=='catalogue_whole_source_universe_retain_selected_dates':
   r['representation']='source_holding_catalogued';target=supplement('selected-result-date-history.jsonl')
  elif action=='catalogue_whole_source_narrative_cache':
   r['representation']='source_holding_catalogued';target=[core,cont,p('evidence/source-additional-narrative-candidates.jsonl')]
  elif action=='catalogue_original_exclusion_lineage_shards':
   r['representation']='source_holding_catalogued';target=[supplement('identity-quarantine-excluded-observation-results.jsonl'),p('audit/sbir-identity-quarantine.json'),p('audit/recovery-core-review-sbir-uei-conflicts.json')]
  elif action=='catalogue_verified_current_JSON_mirror':
   r['representation']='json_projection_equivalent';target=p('evidence/round2-strongest-leads.json')
  else:raise AssertionError('Unmapped action '+action)
  if target:r['represented_by']=target
  if physical in overrides:assert overrides[physical]==r or physical in body_targets,'Conflicting physical source rules: '+physical
  else:overrides[physical]=r
 rules['files']+=list(overrides.values())
 sm=sm.get('minimal_source_map',sm.get('supplements',sm)) if isinstance(sm,dict) else sm
 if isinstance(sm,list):sm={x['name']:x for x in sm}
 for x in whitelist['include_only']:
  n=x['path'];q=cov/n;assert q.stat().st_size==x['bytes'] and sha(q)==x['sha256'];m=sm[n];srcs=m.get('frozen_logical_source_paths',m.get('logical_sources',m.get('sources')))
  if not srcs:srcs=m.get('applicable_frozen_source_paths',[])
  assert srcs,'No data or applicability references: '+n
  rules.setdefault('supplements',[]).append({'name':supplement(n),'local_path':str(q),'bytes':x['bytes'],'sha256':x['sha256'],'sources':sorted(set(z for k in srcs for z in ps(k))),'description':m['description']})
 binding={'commit':inv['commit'],'public_stage1_prefix':prefix,'frozen_manifest_sha256':frozen['package_manifest_sha256'],'logical_file_count':len(bindings),'physical_file_count':len(set(x['published_path'] for x in bindings.values())),'logical_sources':list(bindings.values()),'unmatched_public_stage1_files':[x for x in sources if x not in {b['published_path'] for b in bindings.values()}]}
 bp=pathlib.Path(a.binding_output);bp.write_text(json.dumps(binding,indent=2)+'\n');rules['supplements'].append({'name':'text-coverage/logical-to-public-source-binding.json','local_path':str(bp),'sha256':sha(bp),'sources':sorted(set(x['published_path'] for x in bindings.values())),'description':'Complete binding of all 141 frozen Stage1 package entries to the exact public source files or their verified gzip equivalents in this pinned commit. Logical and physical hashes are kept distinct.'})
 rules['input_exclusions']=[{'published_path':r['path'],'reason':r['reason'],'retained_result_representations':r.get('represented_by')} for r in rules['files'] if r['representation']=='source_holding_catalogued']
 for name in ['DELIVERY-MANIFEST.json','supplemental-source-map.json']:
  helper=cov/name
  rules['supplements'].append({'name':'text-coverage/'+name,'local_path':str(helper),'sha256':sha(helper),'sources':[p('manifest.json')],'description':'Exact small companion metadata for reproducing the audited text coverage supplements; data dependencies resolve through logical-to-public-source-binding.json.'})
 public_git_hashes={x['sha'] for x in inv['files']}
 for name in ['assemble_text_v2.py','stage_verified_snapshot.py','extract_compendium_sections.py','compact_json_losslessly.py','check_snapshot_requirements.py','verify_transport_aliases.py','build_integrated_rules.py']:
  helper=pathlib.Path(__file__).parent/name
  b=helper.read_bytes();git_hash=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  if git_hash in public_git_hashes:continue
  rules['supplements'].append({'name':'text-assembly-code/'+name,'local_path':str(helper),'sha256':sha(helper),'sources':[],'description':'New reproducible text-assembly/verification implementation used for this deliverable; not additional research observations. Local paths in command examples are configurable. This helper is included in full so the transformation does not depend on a private workspace.'})
 rules['front_matter_notes']=[
  'Recovery disclosure: a workspace loss destroyed the first unuploaded local assembly and some unpublished research working files. The final independent Stage1 screen is an explicitly reconstructed, newly verified version; historical 13,267-key counts are not current. Exact surviving source archives and helpers were restored where possible; recovery notes, prior reviews and source-hash records disclose the differences. This text was freshly assembled from the pinned final public package and verified derived result representations; it is not a claim to reproduce lost original bytes.',
  'Current registry denominators: 22,603 independent Stage1 source/instrument keys and 5,501 reporter-register keys form a 27,276-key union, not a count of verified programs. All 111 live-checked keys are already in that union. The complete current Stage1 register has 56 fields and full untruncated descriptions. 7,964 subaward keys do not inherit prime-award money. 69 conflicted registered source keys are quarantined without attributed recipient funding; 281 corrected source appearances are a different denominator.',
  'Readable representation choices: complete typed CSV retains every current Stage1 candidate, continuation and provenance value, with schemas and decoding code preserving nulls, booleans, nested arrays and order. The reporter register is lossless JSON with only insignificant whitespace removed. Complete signed transaction rows, selected full date histories, every machine-hit derived result and unique relevant source facts are retained. No descriptions or rows are ellipsized.',
  'Scope limits are explicit rather than disguised as deduplication. Original input corpora, unrelated source-date histories, original ingestion payloads and routine excluded-input lineage are catalogued by exact public hashes/links, not reproduced wholesale. All 213 corrected excluded observations, all substantive identity audits and every unique factual result within the declared research-result projection are retained. Raw source caches remain inspectable in the public evidence package; this file does not claim to repeat every stored source byte.',
  'Every published file is listed in I0001 even where it is a byte duplicate, verified semantic export, compressed transport alias, or scoped source holding. Text-coverage supplements are new lossless/result-scoped representations verified against those exact sources; they do not introduce new research observations. Canonical links always pin the exact commit.']
 pathlib.Path(a.output).write_text(json.dumps(rules,indent=2)+'\n');print(json.dumps({'rules':len(rules['files']),'supplements':len(rules['supplements']),'logical_sources':len(bindings),'unmatched_public_stage1_files':binding['unmatched_public_stage1_files']}))
if __name__=='__main__':main()
