#!/usr/bin/env python3
"""Lossless authored-record integration; source observations are never controls.

Requires the verified native transfer directory and coordinator pilot output.
Preserves every original row with namespace, file/row provenance and row hash.
No source text retrieval, no paid calls, and no source-control count is inferred.
"""
import argparse,csv,hashlib,json,re
from collections import Counter,defaultdict
from pathlib import Path
from urllib.parse import urldefrag

CONFIG={
 'licences':{'sources':'f6-sources/licences/sources.json','ancillary':'f6-sources/licences/ancillary_sources.json','occ':'f6-sources/licences/reference_occurrences.json','claims':'f6-sources/licences/normalized_findings.json','coverage':'f6-sources/licences/screening_coverage.json','panel':'f6-sources/licences/company_coverage.json','lanes':[1,8]},
 'capital':{'sources':'f6-sources/capital/public/sources.json','occ':'f6-sources/capital/public/occurrences.json','manual':'f6-sources/capital/public/manual-occurrences.json','claims':'f6-sources/capital/public/candidates.json','coverage':'f6-sources/capital/public/text-coverage.json','panel':'f6-sources/capital/public/panel-coverage.json','lanes':[4,5,6]},
 'disputes':{'sources':'f6-sources/disputes/source-register.json','occ':'f6-sources/disputes/reference-occurrences.json','claims':'f6-sources/disputes/candidate-register.json','coverage':'f6-sources/disputes/page-coverage.json','panel':'f6-sources/disputes/panel-coverage.json','lanes':[9,10,11]},
 'legal-risk':{'sources':'f6-sources/legal-risk/public/sources.json','occ':'f6-sources/legal-risk/public/reference-occurrences.json','claims':'f6-sources/legal-risk/public/evidence.json','coverage':'f6-sources/legal-risk/public/screening-coverage.json','panel':'f6-sources/legal-risk/public/company-coverage.json','lanes':[2,3,7,12]}}

def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def sha(b):return hashlib.sha256(b).hexdigest()
def get(x,*keys,default=None):
    for k in keys:
        if x.get(k) is not None and x.get(k)!='':return x[k]
    return default
def rows(p):
    if p.suffix=='.jsonl':return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
    return json.loads(p.read_text())
def source_id(r):return str(get(r,'document_id','source_id','id'))
def wrap(domain,path,index,row):
    return {'domain':domain,'original_file':str(path),'original_row_index':index,
            'original_row_sha256':sha(canonical(row).encode()),'original_record':row}
def output(root,name,data):
    (root/(name+'.jsonl')).write_text(''.join(canonical(x)+'\n' for x in data))
    fields=list(dict.fromkeys(k for row in data for k in row if k!='original_record'))
    with (root/(name+'.csv')).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for row in data:w.writerow({k:canonical(v) if isinstance(v,(list,dict)) else v for k,v in row.items() if k!='original_record'})

def integrate(native,pilot,out):
    out.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((native/'TRANSFER_MANIFEST.json').read_text())
    for item in manifest['files']+manifest['transport_files']:
        b=(native/item['path']).read_bytes()
        if len(b)!=item['bytes'] or sha(b)!=item['sha256']:raise ValueError('Native freeze mismatch '+item['path'])
    sources=[];occurrences=[];claims=[];coverage=[];panel=[];by_source={};provenance=[];counts={}
    for domain,cfg in CONFIG.items():
        entries=rows(native/cfg['sources'])
        source_entries=[(cfg['sources'],i,r,'native_source_observation') for i,r in enumerate(entries)]
        if cfg.get('ancillary'):
            source_entries += [(cfg['ancillary'],i,r,'ancillary_cross_reference') for i,r in enumerate(rows(native/cfg['ancillary']))]
        for path,i,r,kind in source_entries:
            sid=source_id(r);gid=domain+':'+sid
            if gid in by_source:raise ValueError('Duplicate source ID '+gid)
            h=get(r,'sha256','source_sha256','hash');h=h if isinstance(h,str) and re.fullmatch('[a-fA-F0-9]{64}',h) else None
            s={**wrap(domain,path,i,r),'source_observation_id':gid,'original_source_id':sid,
              'record_kind':kind,'source_url':get(r,'url','source_url'),
              'legal_entity':get(r,'legal_entity','entity','exact_subject'),
              'document_version':get(r,'version','document_date_version','date_version','date'),
              'retrieved_utc':get(r,'retrieved_utc','retrieved'),'source_sha256':h,
              'text_sha256':r.get('text_sha256'),'access_depth':get(r,'access_depth','access'),
              'rights_disposition':get(r,'rights_disposition','public_rights_disposition','public_rights','rights'),
              'same_body_group':'sha256:'+h.lower() if h else None,
              'unique_document_countable':False,'actual_control_inferred':False}
            sources.append(s);by_source[gid]=s
        entries=rows(native/cfg['occ']);extra=rows(native/cfg['manual']) if cfg.get('manual') else []
        reviewed=0
        for is_manual,path,values in [(False,cfg['occ'],entries),(True,cfg.get('manual'),extra)]:
            for i,r in enumerate(values):
                sid=source_id(r);gid=domain+':'+sid
                if gid not in by_source:raise ValueError('Orphan native occurrence '+gid)
                status=str(r.get('review_status',''))
                human=is_manual or (not status.lower().startswith(('machine','retained machine','lexical candidate')) and 'manual' in status.lower())
                if human:reviewed+=1
                original_id=str(get(r,'occurrence_id','id',default=i))
                classification=get(r,'final_category','classification','reviewed_class','provisional_category')
                o={**wrap(domain,path,i,r),'integrated_occurrence_id':domain+':'+original_id,
                  'original_occurrence_id':original_id,'source_observation_id':gid,
                  'record_kind':'manual_semantic_supplement' if is_manual or 'manual semantic' in status.lower() or 'manually added' in status.lower() else 'native_detection',
                  'lexical_detection':not(is_manual or 'manual semantic' in status.lower() or 'manually added' in status.lower()),
                  'additive_to_native_occurrence_denominator':True,
                  'source_url':get(r,'source_url',default=by_source[gid]['source_url']),
                  'source_sha256':by_source[gid]['source_sha256'],
                  'page_or_clause':get(r,'locator','clause_locator','page_or_scope','pdf_page','page'),
                  'char_start':get(r,'char_start','character_start','page_character_offset'),
                  'char_end':get(r,'char_end','character_end'),
                  'short_anchor':get(r,'normalized_search_term','matched_original_term','short_original_extract','exact_short_extract'),
                  'context_or_rationale':get(r,'context_description','context_summary','necessary_context','context'),
                  'provisional_reference_class':get(r,'provisional_category','bucket','lexicon_family','classification'),
                  'reviewed_reference_class':classification if human else None,'reference_context_reviewed':human,
                  'review_status':status or 'manual semantic supplement',
                  'confidence':get(r,'confidence'),'context_sha256':get(r,'context_sha256','dedup_group','dedup_text_key','dedup_text_key'),
                  'linked_native_claim_ids':get(r,'linked_finding_id','linked_candidate_ids','linked_candidate','linked_record_ids'),
                  'actual_control_status':'not_inferred_from_reference_occurrence','control_countable':False}
                occurrences.append(o)
        claim_entries=rows(native/cfg['claims'])
        for i,r in enumerate(claim_entries):
            cid=str(get(r,'candidate_id','finding_id','record_id'))
            refs=get(r,'source_ids','document_id','source_id',default=[])
            refs=re.split(r'[;,]',refs) if isinstance(refs,str) else refs
            refs=[domain+':'+str(s).strip() for s in refs if str(s).strip()]
            if any(s not in by_source for s in refs):raise ValueError('Orphan claim '+cid+':'+str(refs))
            c={**wrap(domain,cfg['claims'],i,r),'integrated_claim_id':domain+':'+cid,
               'original_claim_id':cid,'source_observation_ids':refs,
               'source_urls':[by_source[s]['source_url'] for s in refs],
               'legal_entity':get(r,'legal_entity','exact_subject'),
               'product_version':r.get('product_version'),'customer_contract':r.get('customer_contract'),
               'jurisdiction':r.get('jurisdiction'),'date_version':get(r,'document_date_version','date_version','versions'),
               'page_clause':get(r,'page_clause','locator'),'claim':get(r,'normalized_claim','source_observation','finding'),
               'control_categories':get(r,'control_category','control_categories','control_function','function_tags'),
               'evidence_level':r.get('evidence_level'),'decision_maker':r.get('decision_maker'),
               'trigger':r.get('trigger'),'exceptions_override':r.get('exceptions_override'),
               'consequence':r.get('consequence'),'contrary_evidence':get(r,'contrary_evidence','contrary_evidence_and_limits','contrary_and_uncertainty'),
               'remaining_gap':get(r,'remaining_gap','next_document_needed'),'novelty':r.get('novelty'),
               'domain_disposition':get(r,'promotion_tier','status','decision_status'),
               'record_kind':'normalized_bounded_claim_not_unique_control','unique_control_countable':False}
            claims.append(c)
        cov=rows(native/cfg['coverage']);byid=defaultdict(list)
        for c in cov:byid[source_id(c)].append(c)
        if any(domain+':'+sid not in by_source for sid in byid):
            raise ValueError('Orphan coverage source')
        for s in sources:
            if s['domain']!=domain:continue
            native_rows=byid.get(s['original_source_id'],[])
            coverage.append({'domain':domain,'source_observation_id':s['source_observation_id'],
              'record_kind':s['record_kind'],'source_url':s['source_url'],
              'native_text_coverage_record_present':bool(native_rows),'native_coverage_rows':len(native_rows),
              'coverage_units':'physical PDF page rows' if domain=='disputes' else 'document/extracted-scope records',
              'native_coverage_file':cfg['coverage'],'original_coverage_records':native_rows,
              'access_depth':s['access_depth'],'full_semantic_or_image_completeness_claim':False,
              'final_disposition':'Bounded extracted-text screening where registered; image/semantic/linked-term limits retained in original source and coverage records. No absence inference.',
              'actual_control_inferred':False})
        for i,r in enumerate(rows(native/cfg['panel'])):
            company=get(r,'company_panel_name','firm','company_brand')
            canonical_company={'Dynamo AI / DynamoFL':'Dynamo AI/DynamoFL'}.get(company,company)
            for lane in cfg['lanes']:
                panel.append({**wrap(domain,cfg['panel'],i,r),'company_panel_label':canonical_company,
                  'original_panel_label':company,'panel_alias_basis':'Whitespace-only display normalization; not legal entity equivalence' if canonical_company!=company else None,'lane':lane,
                  'entity_resolution':get(r,'entity_resolution','legal_entity_resolution','legal_entity_resolved'),
                  'disposition':get(r,'lane'+str(lane)+'_disposition','public_search_disposition','coverage_status','disposition','status'),
                  'details':get(r,'result_or_limit','scope_limit','limitations','search_depth'),
                  'absence_inference_allowed':False})
        counts[domain]={'registered_source_rows':len(rows(native/cfg['sources'])),
          'ancillary_cross_references':len(source_entries)-len(rows(native/cfg['sources'])),
          'occurrence_rows_in_main_native_file':len(entries),'separate_manual_supplement_rows':len(extra),
          'retained_occurrence_rows':len(entries)+len(extra),'context_reviewed_including_manual_supplements':reviewed,
          'machine_only_retained_rows':len(entries)+len(extra)-reviewed,'bounded_claim_records':len(claim_entries)}
    # Coordinator pilot is a second inspection of the identical appendix, not
    # additional native documentary evidence. Preserve its41rows as overlays.
    pilot_sources=rows(pilot/'sources.jsonl')
    for i,r in enumerate(pilot_sources):
        sid='coordinator:'+r['document_id'];s={**wrap('coordinator','sources.jsonl',i,r),
          'source_observation_id':sid,'original_source_id':r['document_id'],
          'record_kind':'coordinator_same_source_overlay','source_url':r['source_url'],
          'source_sha256':r['source_sha256'],'same_body_group':'sha256:'+r['source_sha256'],
          'unique_document_countable':False,'actual_control_inferred':False}
        sources.append(s);by_source[sid]=s
        coverage.append({'domain':'coordinator','source_observation_id':sid,
          'record_kind':'coordinator_same_source_overlay','source_url':r['source_url'],
          'native_text_coverage_record_present':False,'coordinator_coverage_records':rows(pilot/'coverage.jsonl'),
          'ocr_companion':'Coordinator130page raster pass of identical D09-12 source; separate extraction variant, not new source.',
          'full_semantic_or_image_completeness_claim':False,
          'final_disposition':'Overlay audit only; no complete recall or new-document count.',
          'actual_control_inferred':False})
    for i,r in enumerate(rows(pilot/'occurrences.jsonl')):
        occurrences.append({**wrap('coordinator','occurrences.jsonl',i,r),
          'integrated_occurrence_id':'coordinator:'+r['occurrence_id'],
          'original_occurrence_id':r['occurrence_id'],'source_observation_id':'coordinator:'+r['document_id'],
          'record_kind':'coordinator_same_source_overlay','additive_to_native_occurrence_denominator':False,
          'lexical_detection':r.get('lexical_detection'),'source_url':r.get('source_url'),
          'source_sha256':by_source['coordinator:'+r['document_id']]['source_sha256'],
          'page_or_clause':r.get('page'),'char_start':r['char_start'],'char_end':r['char_end'],
          'provisional_reference_class':r.get('screen_class'),'reviewed_reference_class':r.get('reviewed_class'),
          'reference_context_reviewed':r.get('review_status')=='reviewed',
          'review_status':r.get('review_status'),'context_or_rationale':get(r,'rationale','paraphrase'),
          'context_sha256':r.get('context_sha256'),'actual_control_status':'not_inferred_from_reference_occurrence',
          'control_countable':False})
    # Exact source-body identities and URL clusters are diagnostics. Neither
    # makes different versions of a rule into a count of unique controls.
    body_groups=defaultdict(list);url_groups=defaultdict(list)
    for s in sources:
        if s.get('same_body_group'):body_groups[s['same_body_group']].append(s['source_observation_id'])
        if s.get('source_url'):url_groups[urldefrag(s['source_url'])[0]].append(s['source_observation_id'])
    for h,ids in body_groups.items():
        if len(ids)>1:provenance.append({'group_type':'exact_source_body_hash','identity':h,'source_observation_ids':ids,'disposition':'Same retrieved bytes; all source observations retained; not a control count.'})
    for url,ids in url_groups.items():
        if len(ids)>1:provenance.append({'group_type':'same_url_review_cluster','identity':url,'source_observation_ids':ids,'disposition':'Review only: URL identity does not prove date/version or byte equivalence.'})
    if len({o['integrated_occurrence_id'] for o in occurrences})!=len(occurrences):raise ValueError('Duplicate occurrence IDs')
    if len(panel)!=360 or len({r['company_panel_label'] for r in panel})!=30 or len({(r['company_panel_label'],r['lane']) for r in panel})!=360:raise ValueError('Panel reconciliation requires30labels x12lanes')
    for name,data in [('sources',sources),('occurrences',occurrences),('claims',claims),('coverage',coverage),('company_lane_coverage',panel),('dedup_provenance',provenance)]:output(out,name,data)
    summary={'schema':'F6-integrated-review-candidate-v1','domain_counts':counts,
      'native_registered_source_rows':sum(x['registered_source_rows'] for x in counts.values()),
      'ancillary_link_observations':10,'coordinator_same_source_observations':len(pilot_sources),
      'all_source_observation_rows':len(sources),'distinct_valid_source_body_sha256_values':len(body_groups),
      'source_rows_without_valid_body_hash':sum(not s.get('same_body_group') for s in sources),
      'native_retained_occurrence_rows':sum(x['retained_occurrence_rows'] for x in counts.values()),
      'coordinator_nonadditive_overlay_occurrence_rows':sum(o['domain']=='coordinator' for o in occurrences),
      'all_conserved_occurrence_rows':len(occurrences),
      'native_context_reviewed_rows_including_manual_supplements':sum(x['context_reviewed_including_manual_supplements'] for x in counts.values()),
      'native_machine_only_rows':sum(x['machine_only_retained_rows'] for x in counts.values()),
      'normalized_native_claim_records':len(claims),'company_lane_cells':len(panel),
      'unique_control_total':None,'unique_document_total':None,
      'warning':'Source observations, exact-byte identities, lexical rows, reviewed references, bounded claims and implemented controls are different units. No universal semantic/OCR completeness is claimed.',
      'native_bundle_sha256':'f9fb60b07eeeffadf3ef197ac7f686e2666cf482dbec42b515710a86f6a6d725',
      'integration_code_sha256':sha(Path(__file__).read_bytes())}
    (out/'INTEGRATION_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('native',type=Path);p.add_argument('pilot',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();print(json.dumps(integrate(a.native,a.pilot,a.output),indent=2))
