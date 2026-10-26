#!/usr/bin/env python3
"""F6 conservative occurrence screen. Standard library; no network or paid calls.

Input: JSONL source records, local UTF-8 text_path (relative to input file),
optional segments [{page,clause,text}], and metadata. Source text stays private.
Output: public-safe registers. Pattern hits are candidates, never legal findings.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

VERSION = 'f6-screen-0.6'
CLASSES = ['explicit_ihl_reference', 'substantive_concept_unlabelled',
           'plausible_indirect_connection', 'generic_no_established_ihl_link',
           'rejected_false_positive']
# Even direct acronyms and Article 36 require context adjudication.
TERMS = {
 'explicit_ihl_reference': [r'(?:international|global) humanitarian law',r'\bIHL\b',
  r'laws? of war',r'laws? of armed conflict',r'\bLOAC\b',r'jus in bello',
  r'Geneva.{0,30}conventions?',r'Hague.{0,30}conventions?',
  r'customary humanitarian law',r'Article\s+36\b',r'Martens clause',
  r'droit international humanitaire',r'Humanit[aä]r(?:es|en)? V[oö]lkerrecht',
  r'derecho internacional humanitario',r'internationaal humanitair recht'],
 'substantive_concept_unlabelled': [r'\bdistinction\b',r'\bproportionality\b',
  r'precautions? in attack',r'military necessity',r'unnecessary suffering',
  r'superfluous injur(?:y|ies)',r'indiscriminate attacks?',r'civilian harm',
  r'non[- ]combatants?',r'protected (?:persons|objects)',r'war crimes?',
  r'rules of engagement',r'weapons? reviews?',r'meaningful human control'],
 'plausible_indirect_connection': [r'lawful (?:military )?uses?',
  r'responsible (?:military )?use',r'legitimate military purpose',
  r'international obligations',r'human dignity',r'preserv(?:ation|e) of life',
  r'civilian protection',r'ethical end[- ]use',r'responsible sales',
  r'(?:controversial|prohibited) weapons',r'human authori[sz]ation',
  r'target validation',r'operator judg(?:e)?ment',r'auditab(?:ility|le)',
  r'(?:de[- ]?)?escalation',r'changed capabilities',r'human[- ]in[- ]the[- ]loop',
  r'human (?:review|oversight|control)',r'(?:suspend|suspension|deactivat\w*|terminat\w*)',
  r'incorporat(?:ed|ion) by reference',r'(?:customer|territor\w*|mission) restrictions?',
  r'international law',r'lawful government actions?',r'civilian(?:s| protection)?',
  r'(?:final|human) (?:determinations?|decisions?|decision makers?)',
  r'(?:human|operator) (?:verif\w*|approv\w*|authori\w*)',
  r'(?:prohibited|restricted) uses?',r'(?:changed|modified) (?:use|mission|capabilit\w*)',
  r'lawful military applications?',r'(?:human|machine) oversight',
  r'(?:respect|protect\w*) human life',r'fully autonomous weapons?'],
 'generic_no_established_ihl_link': [r'applicable laws?',r'export controls?',
  r'human rights',r'ethic\w*',r'indemnif\w*',r'governing law',
  r'liability',r'compliance with.{0,30}law',r'end[- ]us(?:e|er)',
  r'restricted (?:customers|territories|missions)',r'legal review',r'board approval']}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def flexible_spaces(pattern):
    # Preserve character classes such as [- ] while spanning layout whitespace.
    return ''.join(piece if piece.startswith('[') else piece.replace(' ',r'\s+')
                   for piece in re.split(r'(\[[^]]+\])',pattern))

def write_jsonl(path, rows):
    path.write_text(''.join(json.dumps(r, ensure_ascii=False, sort_keys=True)+'\n'
                            for r in rows), encoding='utf-8')

def load_jsonl(path):
    return [json.loads(l) for l in path.read_text(encoding='utf-8').splitlines() if l.strip()]

def run(input_path, output, reviews_path=None):
    sources = load_jsonl(input_path)
    if len({s['document_id'] for s in sources}) != len(sources):
        raise ValueError('Duplicate document_id: use a distinct ID per version')
    output.mkdir(parents=True, exist_ok=True)
    lexicon = {'version': VERSION, 'terms': TERMS, 'classification_values': CLASSES}
    lexbytes = json.dumps(lexicon, ensure_ascii=False, sort_keys=True).encode()
    (output/'lexicon.json').write_bytes(lexbytes+b'\n')
    reviews = load_jsonl(reviews_path) if reviews_path else []
    source_ids={s['document_id'] for s in sources}
    for review in reviews:
        if review['document_id'] not in source_ids:
            raise ValueError('Review references an unknown document')
        if review.get('kind') not in ['adjudication','semantic_addition','full_document_semantic_review']:
            raise ValueError('Unknown review kind')
        if not review.get('reviewer'):
            raise ValueError('Review must identify its reviewer')
    occurrences, coverage, failures, candidates, links = [], [], [], [], []
    for source in sources:
        doc = source['document_id']
        for ref in source.get('incorporated_references', []):
            links.append({'from_document_id':doc, **ref})
        try:
            if source.get('source_path'):
                raw=(input_path.parent/source['source_path']).read_bytes()
                if digest(raw)!=source['source_sha256']:
                    raise ValueError('Source byte hash mismatch for '+doc)
            if 'segments' in source:
                segments = source['segments']
                text = '\f'.join(x['text'] for x in segments)
            else:
                text = (input_path.parent/source['text_path']).read_text(encoding='utf-8')
                segments = [{'page':i+1,'clause':None,'text':p}
                            for i,p in enumerate(text.split('\f'))]
        except (OSError, UnicodeError, KeyError) as e:
            failures.append({'document_id':doc,'status':'text_unavailable',
                             'error_type':type(e).__name__})
            coverage.append({'document_id':doc,'processed':False,'no_reference_claim_allowed':False,
                             'final_disposition':source.get('final_disposition')})
            continue
        text_hash = digest(text.encode())
        source_reviews = [r for r in reviews if r['document_id']==doc]
        if any(r.get('text_sha256') != text_hash for r in source_reviews):
            raise ValueError('Review hash mismatch for '+doc)
        quote_remaining = min(20, int(source.get('public_quote_word_budget',0)))
        start = 0
        doc_hits = []
        span_hits = {}
        for segment in segments:
            page = segment.get('page')
            part = segment['text']
            for category, patterns in TERMS.items():
                for index, pattern in enumerate(patterns):
                    bounded=r'(?<!\w)(?:'+flexible_spaces(pattern)+r')(?!\w)'
                    for match in re.finditer(bounded, part, flags=re.I|re.S):
                        a,b = start+match.start(),start+match.end()
                        signal=f'{category}:{index}'
                        if (a,b) in span_hits:
                            span_hits[(a,b)]['signal_ids'].append(signal)
                            continue
                        hit_id = 'occ-'+digest(f'{doc}:{a}:{b}'.encode())[:20]
                        # No long source context is emitted. Stable offsets allow inspection
                        # against the cited original or private working snapshot.
                        words = match.group().split()
                        quote = match.group() if len(words)<=quote_remaining else ''
                        if quote: quote_remaining -= len(words)
                        ca,cb = max(0,a-180),min(len(text),b+180)
                        hit = {'occurrence_id':hit_id,'document_id':doc,
                         'page':page,'clause':segment.get('clause'),
                         'line':text.count('\n',0,a)+1,'char_start':a,'char_end':b,
                         'utf8_byte_start':len(text[:a].encode()),
                         'utf8_byte_end':len(text[:b].encode()),
                         'context_char_start':ca,'context_char_end':cb,
                         'context_sha256':digest(text[ca:cb].encode()),
                         'short_original_extract':quote,
                         'extract_disposition':'short_quote' if quote else 'offsets_and_paraphrase_only',
                         'paraphrase':'Potential '+category.replace('_',' ')+' signal; context review required.',
                         'signal_id':signal,'signal_ids':[signal],
                         'screen_class':category,'reviewed_class':None,
                         'confidence':'unadjudicated','negation_exception_status':'requires_context_review',
                         'linked_instruments':source.get('incorporated_references',[]),
                         'text_sha256':text_hash,
                         'passage_dedupe_sha256':digest(re.sub(r'\s+',' ',text[ca:cb]).strip().lower().encode()),
                         'review_status':'pending','source_url':source.get('source_url'),
                         'document_version':source.get('document_version'),
                         'access_depth':source.get('access_depth')}
                        doc_hits.append(hit)
                        span_hits[(a,b)]=hit
            start += len(part)+1
        # Semantic additions retain all unmatched passages; no keyword co-occurrence.
        for review in source_reviews:
            if review.get('kind') == 'semantic_addition':
                if review.get('classification') not in CLASSES:
                    raise ValueError('Unknown semantic classification')
                a,b = review['char_start'],review['char_end']
                if not (0<=a<b<=len(text)): raise ValueError('Invalid semantic span')
                hit_id = 'semantic-'+digest(f'{doc}:{a}:{b}'.encode())[:20]
                page_start=0
                locator={}
                for segment in segments:
                    if page_start<=a<page_start+len(segment['text']):
                        locator={'page':segment.get('page'),'clause':segment.get('clause')}
                        break
                    page_start+=len(segment['text'])+1
                doc_hits.append({'occurrence_id':hit_id,'document_id':doc,
                    **locator,'char_start':a,'char_end':b,'text_sha256':text_hash,
                    'utf8_byte_start':len(text[:a].encode()),'utf8_byte_end':len(text[:b].encode()),
                    'context_char_start':max(0,a-180),'context_char_end':min(len(text),b+180),
                    'context_sha256':digest(text[max(0,a-180):min(len(text),b+180)].encode()),
                    'screen_class':None,'reviewed_class':review['classification'],
                    'paraphrase':review['rationale'],'short_original_extract':'',
                    'extract_disposition':'offsets_and_paraphrase_only',
                    'review_status':'reviewed','confidence':review['confidence'],
                    'reviewer':review['reviewer'],'source_url':source.get('source_url'),
                    'document_version':source.get('document_version'),
                    'access_depth':source.get('access_depth'),
                    'negation_exception_status':review.get('negation_exception_status','requires_context_review')})
        for review in source_reviews:
            if review.get('kind') == 'adjudication':
                hit = next((h for h in doc_hits if h['occurrence_id']==review['occurrence_id']),None)
                if hit is None: raise ValueError('Unknown reviewed occurrence')
                if review['classification'] not in CLASSES: raise ValueError('Unknown classification')
                hit.update(reviewed_class=review['classification'],review_status='reviewed',
                           confidence=review['confidence'],reviewer=review['reviewer'],
                           rationale=review['rationale'],
                           negation_exception_status=review['negation_exception_status'])
        occurrences.extend(doc_hits)
        for hit in doc_hits:
            hit['lexical_detection']=hit.get('screen_class') is not None
            hit['actual_control_status']='not_inferred_from_reference_occurrence'
            hit['control_id']=None
            hit['unique_control_countable']=False
        expected = source.get('expected_pages')
        missing = source.get('missing_sections',[])
        images = source.get('image_text_status','unknown')
        extraction_complete = (bool(text.strip()) and bool(source.get('full_accessible_text_verified')) and not missing
                               and images in ['not_applicable','visually_checked','ocr_and_visual_checked']
                               and (expected is None or expected==len(segments)))
        semantic = any(r.get('kind')=='full_document_semantic_review' for r in source_reviews)
        complete = extraction_complete and semantic
        coverage.append({'document_id':doc,'processed':True,'text_sha256':text_hash,
           'characters':len(text),'utf8_bytes':len(text.encode()),'pages_processed':len(segments),
           'expected_pages':expected,'extraction_complete':extraction_complete,
           'image_text_status':images,'missing_sections':missing,
           'full_document_semantic_review':semantic,
           'machine_hits':sum(h.get('screen_class') is not None for h in doc_hits),
           'semantic_additions':sum(h.get('screen_class') is None for h in doc_hits),
           'reviewed_occurrences':sum(h['review_status']=='reviewed' for h in doc_hits),
           'no_reference_claim_allowed':complete and not doc_hits,
           'final_disposition':source.get('final_disposition'),
           'status':'fully_processed' if complete else 'partial_or_review_pending'})
        if not extraction_complete:
            failures.append({'document_id':doc,'status':'coverage_incomplete',
              'missing_sections':missing,'image_text_status':images,'pages_processed':len(segments),
              'expected_pages':expected})
        for h in doc_hits:
            candidates.append({'candidate_id':'cand-'+h['occurrence_id'],
              'document_id':doc,'occurrence_ids':[h['occurrence_id']],
              **{k:source.get(k) for k in ['legal_entity','product_version','customer_contract',
               'jurisdiction','document_date','effective_period','governing_status','source_url',
               'retrieved_utc','source_sha256','access_depth','rights_disposition']},
              'control_categories':[],'evidence_level':None,'decision_maker':None,
              'trigger':None,'exceptions_override':'unresolved','consequence':None,
              'novelty':'not_assessed','contrary_evidence':[],'remaining_gap':'context_and_applicability_review',
              'promotion_status':'not_promoted','short_evidence':None,
              'evidence_form':'linked_occurrence','evidence_occurrence_ids':[h['occurrence_id']],
              'origin':'lexical_hit' if h.get('screen_class') else 'semantic_addition',
              'lexical_signal_ids':h.get('signal_ids',[]),
              'reviewed_reference_class':h.get('reviewed_class'),
              'reference_review_status':h['review_status'],
              'actual_control_status':'requires_separate_normalized_control_review',
              'control_id':None,'unique_control_countable':False})
    source_public = [{k:v for k,v in s.items() if k not in ['text_path','source_path','segments'] } for s in sources]
    for name, rows in [('sources',source_public),('occurrences',occurrences),('candidates',candidates),
                       ('coverage',coverage),('access_failures',failures),('incorporation_links',links)]:
        write_jsonl(output/(name+'.jsonl'), rows)
    write_jsonl(output/'semantic_review_log.jsonl', reviews)
    summary={'schema':VERSION,'source_records':len(sources),'processed_documents':sum(c['processed'] for c in coverage),
      'occurrences':len(occurrences),'reviewed_occurrences':sum(h['review_status']=='reviewed' for h in occurrences),
      'candidate_records':len(candidates),'fully_processed_documents':sum(c.get('status')=='fully_processed' for c in coverage),
      'promoted_claims':0,'coverage_failures':len(failures),'incorporation_links':len(links),
      'unique_passage_hashes':len({h.get('passage_dedupe_sha256',h['occurrence_id']) for h in occurrences}),
      'lexicon_sha256':digest(lexbytes+b'\n'),'input_sha256':digest(input_path.read_bytes()),
      'code_sha256':digest(Path(__file__).read_bytes()),
      'limitation':'Pattern recall is unmeasured until manual non-hit sampling; machine zero is not absence of IHL.'}
    (output/'screen_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('sources',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--reviews',type=Path);a=p.parse_args()
    print(json.dumps(run(a.sources,a.output,a.reviews),indent=2))
