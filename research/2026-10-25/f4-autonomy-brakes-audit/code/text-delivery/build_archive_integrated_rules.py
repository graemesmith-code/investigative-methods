#!/usr/bin/env python3
"""Exact public archive-member binding for the complete readable F4 text.
No network, uploads, extraction to source trees, or source mutations.
Archive config: {archive_sha256,archive_bytes,parts:[{path,bytes,sha256}]}.
Paths are relative to the final target directory; parts are in exact order.
"""
import argparse,gzip,hashlib,json,pathlib,tarfile,tempfile,zipfile

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser()
 for n in ['inventory','snapshot','package','coverage','archive-config','transport-rules','base-rules','output','binding-output','rendered']:
  ap.add_argument('--'+n,required=True)
 a=ap.parse_args();inv=json.loads(pathlib.Path(a.inventory).read_text());root=pathlib.Path(a.snapshot);pkg=pathlib.Path(a.package);cov=pathlib.Path(a.coverage);render=pathlib.Path(a.rendered);render.mkdir(parents=True,exist_ok=True)
 cfg=json.loads(pathlib.Path(a.archive_config).read_text());frozen=json.loads((cov/'frozen-artifact-rules.json').read_text());fr={x['path']:x for x in frozen['rules']};whitelist=json.loads((cov/'DELIVERY-MANIFEST.json').read_text());sm=json.loads((cov/'supplemental-source-map.json').read_text())['minimal_source_map']
 files={x['path'][len(inv['root']):]:x for x in inv['files']};public_hashes={p:sha(root/p) for p in files};byhash={}
 for p,h in public_hashes.items():byhash.setdefault(h,[]).append(p)
 parts=[x['path'] for x in cfg['parts']];members={};ch=hashlib.sha256();cn=0
 with tempfile.TemporaryFile() as tmp:
  for x in cfg['parts']:
   assert x['path'] in files and files[x['path']]['size']==x['bytes'] and public_hashes[x['path']]==x['sha256']
   with (root/x['path']).open('rb') as f:
    for b in iter(lambda:f.read(1048576),b''):tmp.write(b);ch.update(b);cn+=len(b)
  assert cn==cfg['archive_bytes'] and ch.hexdigest()==cfg['archive_sha256'];tmp.seek(0)
  with tarfile.open(fileobj=tmp,mode='r:gz') as tar:
   for m in tar:
    if m.isdir():continue
    assert m.isfile(),'Non-regular archive member';q=pathlib.PurePosixPath(m.name);assert not q.is_absolute() and '..' not in q.parts
    logical=m.name
    if logical not in fr:
     matches=[x for x in fr if logical.endswith('/'+x)];assert len(matches)==1,'Unrecognized archive member '+logical;logical=matches[0]
    assert logical not in members;h=hashlib.sha256();n=0
    with tar.extractfile(m) as f:
     for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
    x=fr[logical];assert n==x['bytes'] and h.hexdigest()==x['sha256'];assert (pkg/logical).stat().st_size==n and sha(pkg/logical)==h.hexdigest()
    members[logical]={'archive_member':m.name,'logical_bytes':n,'logical_sha256':h.hexdigest()}
 assert set(members)==set(fr),'Archive must contain exactly the 141 frozen logical entries'
 archiveproof={'archive_bytes':cn,'archive_sha256':ch.hexdigest(),'parts':cfg['parts'],'member_count':len(members),'every_member_byte_verified_against_frozen_package':True,'frozen_manifest_sha256':frozen['package_manifest_sha256']}
 rules=json.loads(pathlib.Path(a.base_rules).read_text());rules.setdefault('files',[]);rules.setdefault('supplements',[]);transport=json.loads(pathlib.Path(a.transport_rules).read_text());rules['files']+=transport['files'];rules.setdefault('coverage_proofs',[]).extend(transport['coverage_proofs']+[archiveproof]);overrides={};targets={};supplements={};retained_hash_targets={};bindings={}
 def sn(n):return 'text-coverage/'+n
 def exact_public(logical):
  choices=byhash.get(fr[logical]['sha256'],[])
  return sorted(choices,key=lambda p:(0 if 'stage1' in p else 1,p))[0] if choices else None
 def content_target(logical):
  if logical in targets:return targets[logical]
  x=fr[logical];p=exact_public(logical);gz=None
  if p is None and logical+'.gz' in fr:
   gz=exact_public(logical+'.gz')
   if gz:
    h=hashlib.sha256();n=0
    with gzip.open(root/gz,'rb') as f:
     for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
    assert n==x['bytes'] and h.hexdigest()==x['sha256'];p=gz
  if p:
   targets[logical]=p;return p
  src=pkg/logical;body=src;name='archived-stage1/'+logical
  if logical.endswith('.gz'):
   body=render/(logical[:-3]);body.parent.mkdir(parents=True,exist_ok=True)
   with gzip.open(src,'rb') as f,body.open('wb') as g:
    for b in iter(lambda:f.read(1048576),b''):g.write(b)
   name=name[:-3]
  h=sha(body)
  if h in retained_hash_targets:targets[logical]=retained_hash_targets[h];return targets[logical]
  # Prefer an already public byte-identical representation over a new section.
  if h in byhash:targets[logical]=sorted(byhash[h])[0];return targets[logical]
  supplements[name]={'name':name,'local_path':str(body),'sha256':h,'sources':parts,'description':'Complete readable content of verified archive member '+members[logical]['archive_member']+'. Logical source SHA-256: '+x['sha256']+'. Archive SHA-256: '+cfg['archive_sha256']+'. '+('Gzip member decompressed exactly; ' if logical.endswith('.gz') else '')+'not a separately published Git blob.'}
  retained_hash_targets[h]=name;targets[logical]=name;return name
 core=content_target('evidence/brakes-candidate-register.csv');cont=content_target('evidence/asimov-performer-continuation-local-2025-2026.csv');transactions=content_target('evidence/candidate-financial-transactions.csv.gz');body_targets={core,cont,transactions}
 for logical,x in fr.items():
  if x['action'] in ('retain_original_text_once','retain_complete_current_calibration_JSON_once'):content_target(logical)
 def projected_targets(logical):
  x=fr[logical];action=x['action']
  if action in ('retain_original_text_once','retain_complete_current_calibration_JSON_once','retain_complete_CSV_once','retain_all_decompressed_transaction_rows'):return [content_target(logical)],'full_logical_content'
  if action=='catalogue_verified_gzip_CSV_alias':return [core if 'brakes-candidate-register' in logical else cont],'verified_gzip_CSV_alias'
  if action=='catalogue_verified_equivalent_JSON_alias':return [core,sn('candidate-csv-type-schema.json'),sn('reconstruct_typed_csv.py')] if 'brakes-candidate-register' in logical else [cont,sn('continuation-csv-type-schema.json'),sn('reconstruct_typed_csv.py')],'typed_CSV_equivalent'
  if action=='catalogue_exact_core_subset_or_projection':return [core,sn('candidate-csv-type-schema.json')]+([sn('ab-review-order-keys.json')] if 'ab-high-priority' in logical else []),'verified_core_subset'
  if action=='retain_complete_typed_CSV_once_catalogue_JSONL_alias':return [sn('candidate-provenance-complete.csv'),sn('provenance-csv-type-schema.json'),sn('reconstruct_typed_csv.py')],'typed_CSV_equivalent'
  if action=='catalogue_original_payload_retain_complete_derived_results':return [sn('machine-hit-results-compact.csv'),sn('machine-hit-compact-schema.json'),sn('machine-hit-unique-facts.jsonl'),sn('candidate-provenance-complete.csv')],'source_holding_catalogued'
  if action=='catalogue_whole_source_universe_retain_selected_dates':return [sn('selected-result-date-history.jsonl')],'source_holding_catalogued'
  if action=='catalogue_whole_source_narrative_cache':return [core,cont,content_target('evidence/source-additional-narrative-candidates.jsonl')],'source_holding_catalogued'
  if action=='catalogue_original_exclusion_lineage_shards':return [sn('identity-quarantine-excluded-observation-results.jsonl'),content_target('audit/sbir-identity-quarantine.json'),content_target('audit/recovery-core-review-sbir-uei-conflicts.json')],'source_holding_catalogued'
  if action=='catalogue_verified_current_JSON_mirror':return [content_target('evidence/round2-strongest-leads.json')],'json_projection_equivalent'
  raise AssertionError(action)
 proof={'coverage_proof':sn('current-coverage-proof.json'),'archive_sha256':cfg['archive_sha256'],'frozen_manifest_sha256':frozen['package_manifest_sha256']}
 for logical,x in fr.items():
  rt,representation=projected_targets(logical);p=exact_public(logical)
  bindings[logical]={**members[logical],'logical_path':logical,'archive_public_parts':parts,'individual_public_alias':p,'action':x['action'],'representation':representation,'represented_by':rt,'reason':x['reason']}
  if not p:continue
  if p in body_targets:overrides[p]={'path':p,'expected_sha256':public_hashes[p],'representation':'full_decompressed_utf8' if p.endswith('.gz') else 'full_utf8','reason':'Complete current canonical CSV, retained once.','proof':proof}
  elif representation!='full_logical_content':overrides[p]={'path':p,'expected_sha256':public_hashes[p],'representation':representation,'represented_by':rt,'reason':x['reason'],'proof':proof}
 # A public gzip alias may be the canonical body of a missing plaintext member.
 for p in body_targets:
  if p in files:overrides[p]={'path':p,'expected_sha256':public_hashes[p],'representation':'full_decompressed_utf8' if p.endswith('.gz') else 'full_utf8','reason':'Complete current canonical CSV, exact bytes verified from archive member and/or published gzip; retained once.','proof':proof}
 def source_paths(logical):
  if logical in fr:return [exact_public(logical)] if exact_public(logical) else parts
  if logical+'.gz' in fr:return source_paths(logical+'.gz')
  if logical=='audit/excluded-observations.jsonl.gz':return parts
  raise AssertionError('Unbound logical dependency '+logical)
 for x in whitelist['include_only']:
  n=x['path'];q=cov/n;assert q.stat().st_size==x['bytes'] and sha(q)==x['sha256'];m=sm[n];srcs=m['frozen_logical_source_paths'] or m.get('applicable_frozen_source_paths',[]);assert srcs
  supplements[sn(n)]={'name':sn(n),'local_path':str(q),'sha256':x['sha256'],'sources':sorted(set(z for k in srcs for z in source_paths(k))),'description':m['description']+' Dependencies may be archive members; the complete source binding lists each logical hash and exact public container.'}
 for n in ['DELIVERY-MANIFEST.json','supplemental-source-map.json']:
  q=cov/n;supplements[sn(n)]={'name':sn(n),'local_path':str(q),'sha256':sha(q),'sources':parts,'description':'Exact small companion metadata for reproducing coverage; logical source paths resolve through logical-to-public-source-binding.json.'}
 binding={'commit':inv['commit'],'archive':archiveproof,'logical_file_count':len(bindings),'logical_sources':list(bindings.values()),'scope':'All 141 logical archive entries are accounted for, but whole source holdings are explicitly catalogued rather than repeated. Physical Git blobs are inventoried separately in the compendium. No direct GitHub file URL is invented for an archive-only member.'};bp=pathlib.Path(a.binding_output);bp.write_text(json.dumps(binding,indent=2)+'\n');bindingname=sn('logical-to-public-source-binding.json');supplements[bindingname]={'name':bindingname,'local_path':str(bp),'sha256':sha(bp),'sources':parts,'description':'Complete verified archive-member and optional individual-alias source mapping, exact hashes and result representations.'}
 for p in parts:overrides[p]={'path':p,'expected_sha256':public_hashes[p],'representation':'transport_catalogued','represented_by':bindingname,'reason':'Public binary archive container, not additional observations. Every archive member is verified and explicitly represented or scoped in the member binding; binary bytes are not printed as text.','proof':archiveproof}
 # Code-only ZIP: validate its complete member manifest; never print binary bytes.
 zip_member_hashes=set()
 for p,h in public_hashes.items():
  if not p.endswith('.zip'):continue
  assert 'text-delivery' in p and pathlib.PurePosixPath(p).name.startswith('F4-text-delivery-reproducibility-code-'),'Unclassified public ZIP: '+p
  refs=[]
  with zipfile.ZipFile(root/p) as z:
   manifest=json.loads(z.read('assembly-helper-manifest.json'));expected={x['path']:x for x in manifest['files']};assert set(z.namelist())==set(expected)|{'assembly-helper-manifest.json'}
   assert all(n.endswith('.py') and pathlib.PurePosixPath(n).name==n for n in expected)
   for zi in z.infolist():
    assert not zi.is_dir() and pathlib.PurePosixPath(zi.filename).name==zi.filename
    data=z.read(zi);dh=hashlib.sha256(data).hexdigest();data.decode('utf-8')
    if zi.filename in expected:assert len(data)==expected[zi.filename]['bytes'] and dh==expected[zi.filename]['sha256']
    zip_member_hashes.add(dh)
    if dh in byhash:refs.append(sorted(byhash[dh])[0]);continue
    q=render/'public-code-zip'/h/zi.filename;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data);name='archived-text-delivery-code/'+pathlib.PurePosixPath(p).stem+'/'+zi.filename;refs.append(name);supplements[name]={'name':name,'local_path':str(q),'sha256':dh,'sources':[p],'description':'Complete authored code/manifest member '+zi.filename+' of the verified public text-delivery helper ZIP.'}
  overrides[p]={'path':p,'expected_sha256':h,'representation':'transport_catalogued','represented_by':refs,'reason':'Manifest-verified assembly-code ZIP; every member is represented as readable text.','proof':{'members':len(refs),'zip_sha256':h,'all_members_included':True}}
 rules['files']+=list(overrides.values());rules['supplements']+=list(supplements.values())
 # The archive adapter itself is also a complete reproducibility result.
 for name in ['assemble_text_v2.py','build_archive_integrated_rules.py']:
  helper=pathlib.Path(__file__).parent/name;h=sha(helper)
  if h not in byhash and h not in zip_member_hashes:rules['supplements'].append({'name':'text-assembly-code/'+helper.name,'local_path':str(helper),'sha256':h,'sources':parts,'description':'Complete current archive-aware text assembly implementation used for this deliverable; applies exact public archive/member verification and emits all authored prose before data appendices.'})
 rules['input_exclusions']=[{'logical_path':x['logical_path'],'logical_sha256':x['logical_sha256'],'archive_public_parts':parts,'reason':x['reason'],'retained_result_representations':x['represented_by']} for x in bindings.values() if x['representation']=='source_holding_catalogued']
 rules['front_matter_notes']=[
  'Recovery disclosure: a workspace loss destroyed the first unuploaded local assembly and some unpublished working files. The final independent Stage1 screen is an explicitly reconstructed and newly verified version, not a claim to recreate lost original bytes. Historical 13,267-key counts are not current. Exact surviving source archives and helpers were restored where possible; recovery notes and prior reviews document the changes.',
  'Current denominators: 22,603 independent Stage1 source/instrument keys and 5,501 reporter-register keys form a 27,276-key union, not a count of verified programs. All 111 live-checked keys are already included. Complete current Stage1 data retain 56 fields and full descriptions. 7,964 subaward keys do not inherit prime money. The 69 conflicted registered source keys carry no attributed recipient funding; 281 corrected source appearances are a different denominator.',
  'Archive-aware coverage: the 141-entry Stage1 package is published as ordered binary archive parts plus selected individual fast-access aliases. This text verifies the complete archive hash, every member hash, and every individual alias it uses. Archive-only members link to the actual public container and retain their own member path/hash; they are never mislabelled as separate Git blobs. All authored member text and substantive results appear here, while binary transport bytes are only catalogued.',
  'Readable representation: complete typed CSV preserves every current candidate, continuation and provenance value, with schemas/code preserving nulls, booleans, nested arrays and row order. The reporter JSON has only insignificant whitespace removed. Complete signed transactions, selected full date histories, all machine-hit derived results and unique relevant source facts are retained without ellipses or truncation.',
  'Explicit source-holding limits: unrelated original input corpora/date histories, ingestion payloads and routine excluded-input lineage are catalogued by exact archive/member hashes, not repeated wholesale. All 213 corrected excluded observations, substantive identity audits and unique factual results within the declared research-result projection are retained. This is a complete research-results text, not a claim to reproduce every stored raw input byte.',
  'The physical file inventory is I0001. The separate logical-to-public-source-binding section accounts for all 141 Stage1 archive members. Prior reviews remain as an audit trail; the final master report controls interpretation. Each emitted body has exact byte length and SHA-256 for independent extraction.']
 pathlib.Path(a.output).write_text(json.dumps(rules,indent=2)+'\n');print(json.dumps({'archive_members_verified':len(members),'rules':len(rules['files']),'supplements':len(rules['supplements']),'body_targets':sorted(body_targets)}))
if __name__=='__main__':main()
