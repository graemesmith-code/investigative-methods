"""Deterministic expansion, source-specific gates, ranking, semantic fingerprints and coverage.
This expands model-authored mechanisms. It does not create hypotheses from shared fields.
"""
import json,csv,hashlib,collections,itertools,gzip,re,pathlib,argparse
from normalize import run, OUT
from design import M,GROUPS

def dump(name,obj): (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def jl(name,rows): (OUT/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
def csvwrite(path,rows):
 if not rows: path.write_text(''); return
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader()
  for r in rows: w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()})
def sid(i): return f'SYS-{i:04d}'
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()[:20]
def scope(i):
 if 301<=i<=324:
  return {301:'Nunavut',302:'BC',303:'BC',304:'BC',305:'BC',306:'Ontario',307:'Ontario',308:'Ontario',309:'Ontario',310:'Quebec',311:'Quebec',312:'Quebec',313:'Quebec',314:'Alberta',315:'Alberta',316:'Saskatchewan',317:'Saskatchewan',318:'Manitoba',319:'New Brunswick',320:'Nova Scotia',321:'Nova Scotia',322:'Newfoundland',323:'Yukon',324:'Northwest Territories'}[i]
 return ''
def nation(s):
 # Only reject explicitly disjoint national spatial scopes; global/mixed is retained conditionally.
 g=s['metadata'].get('Geographic coverage','').lower()
 if 'global' in g or 'multi' in g:return ''
 if 'canada' in g or 263<=int(s['sys_id'][-4:])<=344:return 'CA'
 if g.startswith(('united states','us;','u.s.')):return 'US'
 if g.startswith(('united kingdom','uk;')):return 'UK'
 if g.startswith('australia'):return 'AU'
 return ''
def namespaces(s):
 f='; '.join(s['join_fields']).lower(); out=[]
 for label,pat in [('IMO',r'\bimo\b'),('MMSI',r'\bmmsi\b'),('LEI',r'\blei\b'),('CVE',r'\bcve\b'),('DOI',r'\bdoi\b'),('ORCID',r'\borcid\b'),('ASN',r'\basn\b'),('CNPJ',r'\bcnpj\b'),('CIK',r'\bcik\b'),('UEI',r'\buei\b'),('ACN',r'\bacn\b'),('NZBN',r'\bnzbn\b'),('domain',r'\bdomain\b')]:
  if re.search(pat,f):out.append(label)
 return out

def join(a,b,m):
 mode=m['join']; shared=sorted(set(namespaces(a))&set(namespaces(b)))
 if mode=='vessel':
  if 'IMO' in shared:return 'direct_identifier_conditional','IMO (validate check digit, vessel entity type and recorded value)',4
  return 'bridge_required','Vessel names are provisional; obtain an authoritative dated IMO/official-number/MMSI crosswalk. Do not equate these namespaces.',1
 if mode=='cve':return 'direct_identifier_conditional','Exact CVE; distinguish affected product/version from actual deployed inventory.',4
 if mode=='network':
  if 'ASN' in shared:return 'direct_identifier_conditional','Exact ASN in same namespace and assignment interval; measurement location still needs validation.',4
  return 'bridge_required','Resolve source network/facility identifier to ASN with a dated official crosswalk.',1
 if mode=='domain':return 'domain_conditional','Canonical exact domain, IDN encoding and wildcard scope; common domain does not prove ownership.',3
 if mode=='spatial':return 'spatiotemporal_conditional','Intersect verified footprints/time intervals in a common CRS. First confirm usable geometry, spatial resolution and effective dates in both schemas.',2
 if mode=='aggregate':return 'aggregate_conditional','Harmonize destination/state codes, dates and category meanings; never infer entity identity from country totals.',1
 if mode=='study':return 'bridge_required','Explicit NCT/protocol reference in full publication to trial record; DOI/author/institution similarity alone is insufficient.',1
 if mode=='payment':return 'bridge_required','Payer and payee legal identities, project crosswalk, compatible stream and year; entity name is provisional.',1
 if mode=='institution':return 'name_provisional','Normalize institutional name and verify official identity and reorganizations; not a stable identifier.',1
 if shared and any(x in shared for x in ['CNPJ','UEI','ACN','NZBN','LEI','CIK']):
  return 'direct_identifier_conditional','Exact '+', '.join(shared)+' in its issuing namespace; verify entity type and validity interval.',4
 return 'name_or_role_provisional','Screen the named entity/person in its stated role, then confirm with jurisdiction-scoped registration identifiers or independent biographical evidence. Source-local IDs are not cross-source keys.',1

def evidence_status(i):
 return 'official_documentation_read_not_field_sampled' if i in [1,24,54,218] else 'catalog_only_unverified'
def build(stage):
 sources=run(); ss={int(s['sys_id'][-4:]):s for s in sources}; accepted=[]; rejected=[]; seen={}; attempted=0
 mechanisms=[m for m in M if m['a']==GROUPS['sanctions']] if stage=='early' else M
 for m in mechanisms:
  aa=[24] if stage=='early' else m['a']
  for ai,bi in itertools.product(aa,m['b']):
   attempted+=1; a,b=ss[ai],ss[bi]; reason=None
   if ai==bi:reason='same_source_not_a_cross_source_test'
   elif m['join']=='spatial' and nation(a) and nation(b) and nation(a)!=nation(b):reason='documented_national_spatial_scopes_disjoint'
   elif m['join']=='spatial' and scope(ai) and scope(bi) and scope(ai)!=scope(bi):reason='provincial_spatial_scopes_disjoint'
   # Methane is the independently observed quantity; these registries do not inherently supply methane.
   elif m['key']=='C01' and ai in [38,218]:reason='no_established_common_methane_measure; enforcement/TRI is not a methane-emissions inventory'
   elif m['key']=='C05' and bi==183:reason='dam_inventory_is_not_a_flood_hazard_footprint; use a connected engineering scenario instead'
   elif m['key']=='W05' and bi==146:reason='OONI_censorship_measurements_do_not_by_themselves_measure_general_outages'
   elif m['key']=='S04' and ai in [25,26,27,29]:reason='explicit_fields_do_not_establish_vessel_scope_or_IMO; retain_only_if_a_later_schema_check_confirms_it'
   elif m['key'] in ['S02','E03','E08','I01','I02','C06'] and bi==1:reason='GLEIF_accounting_parent_relationship_does_not_establish_ownership_shares; retained_as_identity_bridge_only'
   elif m['key'] in ['S02','E03','E08','I01','I02','C06'] and bi in [9,10,20,40,48]:reason='explicit_join_fields_show_roles_not_ownership; ownership_inference_quarantined_pending_schema_evidence'
   elif m['key']=='S07' and bi==291:reason='distribution_index_is_not_full_commercial_relationship_disclosure; needs_additional_filing_source'
   elif m['key']=='E09' and bi==291:reason='distribution_index_does_not_supply_accounts_for_reconciliation'
   elif m['key']=='E07' and bi in [278,279,280]:reason='product_or_register_entry_does_not_establish_funded_project_delivery_without_additional_documents'
   elif m['key']=='C02' and ai==295:reason='payment_disclosure_is_not_a_geolocated_industrial_site_inventory'
   elif m['key'] in ['C03','C05'] and ai==295:reason='payment_disclosure_lacks_required_facility_geometry'
   elif m['key']=='C06' and bi==1:reason='GLEIF_accounting_parent_must_not_be_promoted_to_legal_owner; identity_bridge_only'
   if reason:
    rejected.append(dict(mechanism=m['key'],a=sid(ai),b=sid(bi),reason=reason));continue
   route,recipe,jscore=join(a,b,m)
   # Canonical mirrored arms series is an alternative access route, not another test.
   canonical_a=85 if ai==86 else ai
   pair=sorted([canonical_a,bi]) if m['symmetric'] else [canonical_a,bi]
   fp=digest([m['key'],pair,m['join'],m['initial'],m['expected'],m['temporal'],m['outcome']])
   if fp in seen:
    rejected.append(dict(mechanism=m['key'],a=sid(ai),b=sid(bi),reason='duplicate_substantive_test_alternative_access_route:'+seen[fp]));continue
   seen[fp]=f'T-{m["key"]}-{ai:04d}-{bi:04d}'
   costs=' | '.join(dict.fromkeys(ap['fields'].get('Cost or eligibility','not recorded') for s in [a,b] for ap in s['labeled_access_points']))
   paid=bool(re.search(r'paid|subscription|commercial|fee-based|cost varies|charges|pricing|paywall',costs,re.I))
   cost_tier=3 if paid else 2 if route in ['bridge_required','name_or_role_provisional','spatiotemporal_conditional','aggregate_conditional'] else 1
   documented=sum(evidence_status(i)!='catalog_only_unverified' for i in [ai,bi])
   testability=min(3,1+(jscore>=3)+(documented==2))
   score=round(m['priority']*.65+testability*5+jscore*3-(cost_tier-1)*4,2)
   row=dict(test_id=seen[fp],fingerprint=fp,mechanism=m['key'],family=m['family'],source_a=a['sys_id'],source_a_name=a['name'],source_b=b['sys_id'],source_b_name=b['name'],initial_observation=f"IF {a['name']} supplies this verified observation: {m['initial']}",expected_observation=f"THEN inspect {b['name']}: {m['expected']}",basis=m['basis'],basis_strength=m['legal'],interesting_outcome=m['outcome'],timing=m['temporal'],geography=f"Intersect actual coverage: A={a['metadata'].get('Geographic coverage','unknown')}; B={b['metadata'].get('Geographic coverage','unknown')}. Cross-border corporate links require documented identity paths; local observations require overlapping footprints.",ordinary_explanations=m['ordinary'],disqualifiers=m['disqualifiers'],required_evidence=m['evidence'],next_cheapest_check=f"First verify {b['name']}'s documented schema and one permissible record; then: {m['next_check']}",join_status=route,join_recipe=recipe,source_a_description=a['labeled_access_points'][0]['fields'].get('Investigative relevance or methodology','Not recorded'),source_b_description=b['labeled_access_points'][0]['fields'].get('Investigative relevance or methodology','Not recorded'),source_a_fields=a['join_fields'],source_b_fields=b['join_fields'],shared_named_namespaces=sorted(set(namespaces(a))&set(namespaces(b))),source_a_ap_ids=[x['ap_id'] for x in a['labeled_access_points']],source_b_ap_ids=[x['ap_id'] for x in b['labeled_access_points']],source_a_provenance=f"{a['file']}:{a['line_start']}-{a['line_end']} sha256:{a['block_sha256']}",source_b_provenance=f"{b['file']}:{b['line_start']}-{b['line_end']} sha256:{b['block_sha256']}",source_a_weaknesses=list(dict.fromkeys(x['fields'].get('Main weakness','Not recorded') for x in a['labeled_access_points'])),source_b_weaknesses=list(dict.fromkeys(x['fields'].get('Main weakness','Not recorded') for x in b['labeled_access_points'])),availability_a=evidence_status(ai),availability_b=evidence_status(bi),public_interest_score=m['priority'],public_interest_reason=m['basis'],testability_score=testability,join_confidence_score=jscore,cost_tier=cost_tier,cost_basis=costs,estimated_first_check_minutes='15-45 for documentation triage; execution cost unknown',overall_rank_score=score,design_validation='schema_passed_conditional_design',execution_status='not_executed_not_confirmed_feasible',legal_verification='OFAC general guidance only; specific program/activity/exception unverified' if ai==24 else 'No source-pair legal rule established',absence_policy='No absence inference admitted without demonstrated coverage, reporting obligation if alleged, lag, search sensitivity and suppression analysis.',dedup_policy='Parameters, years, thresholds and source-order paraphrases are not separate tests; distinct source pairs are alternative implementations, not independent discoveries.')
   accepted.append(row)
 accepted.sort(key=lambda r:(-r['overall_rank_score'],r['test_id']))
 for rank,r in enumerate(accepted,1):r['rank']=rank
 prefix='checkpoints/early-' if stage=='early' else ''
 jl(prefix+'tests.jsonl',accepted); csvwrite(OUT/(prefix+'tests.csv'),accepted); jl(prefix+'rejected.jsonl',rejected)
 dump(prefix+'counts.json',dict(stage=stage,source_descriptions=344,mechanism_rules=len(mechanisms),expanded_candidates=attempted,accepted_conditional_designs=len(accepted),rejected_or_deduplicated=len(rejected),deduplicated=sum(r['reason'].startswith('duplicate') for r in rejected),schema_validated=len(accepted),record_level_executed=0,confirmed_executable=0,weekly_allowance='unavailable; last user report 99% remaining; no inference from run duration',paid_api_calls=0))
 if stage=='full':
  dump('mechanisms.json',M); dump('roles.json',GROUPS)
  pair_rules=collections.defaultdict(list)
  for r in accepted:pair_rules[(r['source_a'],r['source_b'])].append(r['mechanism'])
  rejpairs=collections.defaultdict(list)
  for r in rejected:rejpairs[(r['a'],r['b'])].append(r['reason'])
  with gzip.open(OUT/'pair-universe.csv.gz','wt',newline='') as f:
   w=csv.writer(f);w.writerow(['source_a','source_b','status','mechanisms_or_reason'])
   for a,b in itertools.permutations(sources,2):
    k=a['sys_id'],b['sys_id']
    w.writerow([*k,'conditional_design' if k in pair_rules else 'rule_candidate_rejected' if k in rejpairs else 'not_admitted', '; '.join(pair_rules.get(k,rejpairs.get(k,['No source-specific mechanism admitted; not proof that no useful test exists.'])))])
  coverage=[]
  for i,s in ss.items():
   rr=[r for r in accepted if s['sys_id'] in [r['source_a'],r['source_b']]]
   groups=[k for k,v in GROUPS.items() if i in v]
   coverage.append(dict(sys_id=s['sys_id'],name=s['name'],roles=groups,explicit_join_fields=s['join_fields'],normalized_namespaces=namespaces(s),entity_types=sorted(set('organization/person' if g in ['sanctions','ownership','company_identity','funding','procurement','political_money','lobbying','enforcement','charity'] else 'vessel' if g=='vessel' else 'spatial feature' if g in ['industrial_site','land_right','population','plume','damage'] else 'role-specific; see fields' for g in groups)),accepted_designs=len(rr),families=sorted(set(r['family'] for r in rr)),disposition='conditional_recipes' if rr else 'support_or_deferred',reason='Source participates in specific conditional mechanisms; no executable claim.' if rr else 'Reviewed as context/crosswalk/discovery-only, aggregate or insufficiently specified role; no standalone high-consequence pairing justified in this pass.',availability=evidence_status(i)))
  jl('source-coverage.jsonl',coverage);csvwrite(OUT/'source-coverage.csv',coverage)
  dump('progress.json',{'phase':'full_model_authored_mechanism_sweep_complete_pending_quality_review','sources_normalized_and_role_reviewed':344,'directed_source_pair_universe':344*343,'unordered_source_pair_universe':344*343//2,'pairs_enumerated_by_policy':344*343,'pairs_with_conditional_designs':len(pair_rules),'pairs_with_rejections_only':len(set(rejpairs)-set(pair_rules)),'pairs_not_admitted':344*343-len(set(pair_rules)|set(rejpairs)),'individual_pair_semantic_review_claimed':False,'mechanism_families':dict(collections.Counter(r['family'] for r in accepted)),'mechanism_counts':dict(collections.Counter(r['mechanism'] for r in accepted)),'source_participation':sum(bool(r['accepted_designs']) for r in coverage),'sources_support_or_deferred':sum(not r['accepted_designs'] for r in coverage),'source_concentration_top20':collections.Counter(x for r in accepted for x in [r['source_a'],r['source_b']]).most_common(20),'rule_status':'All accepted rows conditional; unsupported paths quarantined by explicit gates in code; see rejections.','remaining':'Record-level schema/coverage/terms checks and trial execution; no bulk execution authorized. Review deferred roles for new substantive mechanisms, not paraphrases.','usage':{'weekly_meter_available':False,'model_token_meter_available':False,'last_user_report_remaining_percent':99,'new_paid_api_calls':0}})
 return accepted,rejected
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--stage',choices=['early','full'],default='full');args=ap.parse_args();r,j=build(args.stage);print(json.dumps({'accepted':len(r),'rejected':len(j),'stage':args.stage}))
