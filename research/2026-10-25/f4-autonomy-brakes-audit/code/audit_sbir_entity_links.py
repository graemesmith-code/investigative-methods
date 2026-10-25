#!/usr/bin/env python3
"""Quarantine explicit SBIR UEI conflicts without borrowing another entity's money.
Reads every canonical financial row and both complete SBIR streams. PIID-only
matches are comparison candidates, never evidence resolving recipient identity.
DUNS is not UEI. No network, model/API spend, or financial-register mutation.
"""
import argparse,collections,csv,gzip,hashlib,json,pathlib,re
P=pathlib.Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def norm(s):return re.sub('[^A-Z0-9]','',str(s or '').upper())
def uei(s):return bool(re.fullmatch('[A-Z0-9]{12}',str(s or '')))
def run(root):
 finpaths=list(root.rglob('financial_actions.jsonl.gz'));assert len(finpaths)==1;financial=finpaths[0];by=collections.defaultdict(dict);count=0
 with gzip.open(financial,'rt',encoding='utf-8') as inp:
  for count,line in enumerate(inp,1):
   r=json.loads(line);key=r['award_key'];parts=key.split('_')
   if key.startswith(('CONT_AWD_','ASST_NON_')) and len(parts)>2:
    x=by[norm(parts[2])].setdefault(key,{'ueis':set(),'legal_names':set()});identifier=str(r.get('entity_key') or '').strip()
    if uei(identifier):x['ueis'].add(identifier)
    x['legal_names'].add(str(r.get('entity_name') or ''))
 conflicts=[];files=[]
 for name in ('sbir.jsonl.gz','sbir_current.jsonl.gz'):
  paths=list(root.rglob(name));assert len(paths)==1,(name,len(paths));source=paths[0];statuses=collections.Counter();n=0
  with gzip.open(source,'rt',encoding='utf-8') as inp:
   for n,line in enumerate(inp,1):
    r=json.loads(line);ids=r.get('identifiers_json') or {};ids=json.loads(ids) if isinstance(ids,str) else ids
    su=str(ids.get('UEI') or '').strip();piid=norm(ids.get('Contract') or ids.get('Contract Number') or r.get('award_key'));choices=by.get(piid,{})
    if not uei(su):status='explicit_source_UEI_missing_or_invalid_DUNS_not_substituted'
    elif not choices:status='no_comparison_financial_PIID_not_zero_funding'
    elif len(choices)!=1:status='ambiguous_multiple_financial_award_keys_no_join'
    else:
     key,other=next(iter(choices.items()))
     if not other['ueis']:status='financial_recipient_UEI_unavailable_no_DUNS_substitution'
     elif su in other['ueis']:status='source_UEI_matches_financial_recipient_history_not_SOW_validation'
     else:
      status='explicit_UEI_conflict_quarantined'
      original_description=str(r.get('text') or r.get('evidence_excerpt') or '');description=re.sub(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b','[contact email omitted]',original_description,flags=re.I);description=re.sub(r'(?<!\d)(?:\+1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]\d{3}[-.\s]\d{4}(?!\d)','[contact phone omitted]',description)
      conflicts.append({'source_title':r.get('title'),'source_full_description_contact_details_omitted':description,'source_original_description_sha256':hashlib.sha256(original_description.encode()).hexdigest(),'published_description_sha256':hashlib.sha256(description.encode()).hexdigest(),'source_file':name,'source_physical_row':n,'source_document_id':r.get('document_id'),'source_award_identifier_literal':ids.get('Contract') or r.get('award_key'),'piid_normalized_for_comparison_only':piid,'source_entity_name':r.get('entity_name'),'source_explicit_UEI':su,'source_DUNS_separate_not_UEI':str(ids.get('Duns') or ids.get('DUNS') or ''),'source_agency':ids.get('Agency'),'source_branch':ids.get('Branch'),'comparison_financial_award_key_not_joined':key,'financial_all_recipient_UEIs':sorted(other['ueis']),'financial_all_recipient_legal_names':sorted(other['legal_names']),'source_url':r.get('source_url'),'source_normalized_line_sha256_without_terminator':hashlib.sha256(line.rstrip('\r\n').encode('utf-8')).hexdigest(),'stored_original_source_record_sha256':r.get('record_sha256'),'source_snapshot_sha256':r.get('source_snapshot_sha256'),'disposition':status,'money_assigned_to_SBIR_lead':None,'interpretation':'Keep source entity, agency, full financial identity and recipient separate. Similar names/hash/PIID do not resolve identity. No novation, source error or wrongdoing inferred.'})
    statuses[status]+=1
  files.append({'file':name,'bytes':source.stat().st_size,'sha256':sha(source),'physical_rows':n,'status_counts':dict(statuses)})
 selected={r['piid'] for r in json.loads((P/'evidence/reviewed-cases.json').read_text())};technical={r['piid'] for r in csv.DictReader((P/'evidence/live-technical-scope-review.csv').open())};live={r['piid'] for r in csv.DictReader((P/'evidence/combined-live-inventory.csv').open())}
 ids={r['piid_normalized_for_comparison_only'] for r in conflicts};out=P/'evidence/sbir-entity-linkage-conflicts.json';out.write_text(json.dumps({'source_appearances':conflicts,'no_money_transfer':True},indent=2)+'\n')
 with (P/'evidence/sbir-entity-linkage-conflicts.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(conflicts[0]) if conflicts else ['disposition']);w.writeheader();w.writerows({k:json.dumps(v) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in conflicts)
 audit={'source_files':files,'financial_physical_rows':count,'financial_file_sha256':sha(financial),'conflicting_source_appearances':len(conflicts),'conflicting_PIID_comparison_identifiers_not_award_count':len(ids),'technical58_intersection':sorted(ids&technical),'combined111_intersection':sorted(ids&live),'selected31_intersection':sorted(ids&selected),'all_source_rows_accounted':sum(sum(x['status_counts'].values()) for x in files)==sum(x['physical_rows'] for x in files),'financial_mutations':0,'UEI_validation':'Require the source field itself to be12 uppercase alphanumeric characters after whitespace trimming; do not uppercase mixed-case/nonstandard identifiers into UEIs. This is format gating, not registry validation. DUNS remains a separate namespace.','inference_limit':'UEI conflict is a quarantined attribution question, not proof of wrongdoing or zero funding. Legacy DUNS is not compared as UEI. Source hash domains remain distinct.','code':'code/audit_sbir_entity_links.py'}
 (P/'audit/sbir-entity-linkage-accounting.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps(audit,indent=2))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--extracted',type=pathlib.Path,default=pathlib.Path('/workspace/scratch/f4-data-complete/extracted'));run(a.parse_args().extracted)
