"""F6 capital text sweep v1.1. Raw contexts remain private; registers are authored metadata."""
import re,json,csv,hashlib
from pathlib import Path
R=Path(__file__).parent; P=R/'public'; P.mkdir(exist_ok=True)
LEX={
'explicit': [r'international\s+humanitarian\s+law',r'\bIHL\b',r'laws?\s+of\s+war',r'law\s+of\s+armed\s+conflict',r'\bLOAC\b',r'jus\s+in\s+bello',r'Geneva\s+conventions?',r'Hague\s+conventions?',r'customary\s+humanitarian',r'Martens\s+clause',r'humanit[æa]rrett\w*',r'humanitair\s+oorlogsrecht',r'droit\s+international\s+humanitaire',r'humanit[äa]re[ns]?\s+V[öo]lkerrecht'],
'concept_candidate':[r'proportionality',r'precautions?\s+in\s+attack',r'military\s+necessity',r'unnecessary\s+suffering',r'superfluous\s+injury',r'indiscriminate\s+attacks?',r'civilian\s+(?:harm|protection|casualties)',r'non[-\s]?combatants?',r'protected\s+(?:persons|objects)',r'war\s+crimes?',r'rules\s+of\s+engagement',r'weapons?\s+review',r'meaningful\s+human\s+control',r'humanitarian\s+principles',r'folkerettens\s+regler\s+for\s+stridighetene',r'burgerslachtoffers'],
'indirect_candidate':[r'lawful\s+(?:use|purpose)',r'responsible\s+(?:use|sales|trading|AI)',r'legitimate\s+military',r'international\s+obligations',r'human\s+dignity',r'preservation\s+of\s+life',r'ethical\s+end[-\s]?use',r'controversial\s+weapons?',r'prohibited\s+weapons?',r'human\s+(?:authori[sz]ation|oversight|judg(?:e)?ment|control|review)',r'human[-\s]in[-\s]the[-\s]loop',r'target\s+validation',r'operator\s+judg(?:e)?ment',r'auditability',r'escalat\w*',r'end[-\s]?use',r'end[-\s]?user',r'autonomous\s+weapons?',r'lethal\s+autonomous',r'controversi[ëe]le\s+wapens',r'd[øo]delige\s+autonome',r'prohibited\s+use',r'product\s+misuse'],
'generic_no_established_IHL_link':[r'human[-\s]?rights?',r'mensenrechten',r'menneskerettighet\w*',r'Menschenrechte\w*',r'droits\s+(?:de\s+l.homme|humains)',r'applicable\s+law',r'international\s+law',r'export\s+control\w*',r'export\s+licen[cs]\w*',r'eksport\w*',r'\blegal\b',r'\blaws?\b',r'\bethic\w*',r'\bregulat\w*',r'\bcompliance\b',r'due\s+diligence',r'privacy',r'product\s+safety',r'civilian',r'\bUNGP\b',r'guiding\s+principles'],
'ambiguous_candidate':[r'Article\s+36',r'\bdistinction\b',r'\bdiscrimination\b',r'\bLAWS\b',r'\bLOAC\b']}
LEX['explicit'] += [r'humanitarian\s+law']
LEX['concept_candidate'] += [r'principle\s+of\s+necessity',r'humanit[æa]re\s+prinsipper']
LEX['generic_no_established_IHL_link'] += [r'etisk\w*',r'etikk\w*',r'folkerett\w*',r'mänskliga\s+rättigheter',r'järelevalv\w*',r'\bseadus\w*']
LEX['indirect_candidate'] += [r'white\s+phosphorus',r'\bWP\s+illumination',r'cluster\s+munitions?',r'anti[-\s]?personnel\s+mines?',r'blinding\s+laser',r'incendiary\s+weapons?',r'nuclear\s+weapons?',r'chemical\s+weapons?',r'biological\s+weapons?']
compiled=[(cat,p,re.compile(p,re.I if p not in [r'\bLAWS\b',r'\bIHL\b',r'\bLOAC\b'] else 0)) for cat,ps in LEX.items() for p in ps]
def dump(name,rows):
 (P/(name+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2))
 if rows:
  keys=list(dict.fromkeys(k for r in rows for k in r))
  with (P/(name+'.csv')).open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
   for r in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()})
docs=json.loads((R/'private/retrievals.json').read_text()); occ=[]; contexts=[]; coverage=[]
for d in docs:
 if d.get('status')!=200 or not d.get('text_path'):continue
 text=Path(d['text_path']).read_text(); pages=text.split('\f'); pages=pages[:-1] if pages and not pages[-1].strip() else pages
 offset=0; n=0
 for pn,page in enumerate(pages,1):
  seen=set()
  for cat,pat,rx in compiled:
   for m in rx.finditer(page):
    key=(m.start(),m.end(),cat)
    if key in seen:continue
    seen.add(key); n+=1
    left=max(0,m.start()-180);right=min(len(page),m.end()+220)
    context=re.sub(r'\s+',' ',page[left:right]).strip(); h=hashlib.sha256(context.encode()).hexdigest()
    oid=f'{d["id"]}-O{n:05d}'
    flags=[x for x,rx2 in [('negation',r'\b(?:not|no|never|cannot|ikke|niet)\b'),('exception_or_scope',r'\b(?:unless|except|only|limited|however|subject to)\b'),('risk_warning',r'\b(?:may|could|risk|potential|might)\b')] if re.search(rx2,context,re.I)]
    row={'occurrence_id':oid,'document_id':d['id'],'source_url':d['url'],'document_version':d['date_version'],'locator':f'PDF page {pn}, extracted line {page[:m.start()].count(chr(10))+1}' if d.get('pages') else f'HTML extracted line {page[:m.start()].count(chr(10))+1}; character {offset+m.start()}', 'page':pn if d.get('pages') else '', 'character_start':offset+m.start(),'character_end':offset+m.end(),'matched_original_term':m.group(),'search_regex':pat,'provisional_category':cat,'confidence':'candidate only; explicit wording high for explicit class, substantive applicability unverified','review_status':'machine-retained; promoted passages separately manually reviewed','context_cues':flags,'context_sha256':h,'dedup_group':h,'context_description':'A lexical occurrence, not proof of a safeguard. Read source at locator; neighboring negations/scope cues are retained. Claim-level contextual analysis is in candidates and memo.','linked_instrument':'not established at occurrence level; see claim register for reviewed chains','access_depth':d['access_depth'],'rights_disposition':'Common search phrase only, not a paragraph reproduction; copyrighted full context omitted from public package; stable source and context hash supplied.'}
    occ.append(row);contexts.append({'occurrence_id':oid,'original_context':context})
  offset+=len(page)+1
 coverage.append({'document_id':d['id'],'text_characters':len(text),'pdf_pages_processed':d.get('pages') or 0,'html_bodies_processed':0 if d.get('pages') else 1,'lexical_occurrences':n,'low_text_pdf_pages':[i+1 for i,p in enumerate(pages) if d.get('pages') and len(p.strip())<60],'method':'full extracted-text sweep v1.1; no general OCR; HTML navigation retained; no claim of full semantic recall'})
dump('occurrences',occ);dump('text-coverage',coverage)
(R/'private/occurrence-contexts.json').write_text(json.dumps(contexts,ensure_ascii=False,indent=2))
(P/'lexicon-v1.1.json').write_text(json.dumps(LEX,ensure_ascii=False,indent=2))
sources=[]
for d in docs:
 s={k:v for k,v in d.items() if k!='text_path'}
 s['rights_disposition']='Source copies NOT whitelisted; authored metadata and limited common search phrases/short reviewed quotes only.'
 if d['id']=='CG031':s['scope_note']='SEC landing page only; actual correspondence is CG042'
 if d['id'] in ['CG019','CG043']:s['scope_note']='Direct fetch failed; official PDF separately readable through web tool; not counted in downloaded full-text sweep.'
 if d['id']=='CG045':s['date_version']='Consolidated Norwegian FOR-2025-11-07-2231, amended 5 October 2026 by FOR-2026-10-05-2004'
 sources.append(s)
dump('sources',sources)
summary={'documents_registered':len(docs),'documents_full_downloaded_text_swept':len(coverage),'pdf_pages':sum(c['pdf_pages_processed'] for c in coverage),'html_bodies':sum(c['html_bodies_processed'] for c in coverage),'occurrences':len(occ),'unique_context_groups':len(set(o['dedup_group'] for o in occ)),'categories':{c:sum(o['provisional_category']==c for o in occ) for c in LEX},'cost_usd':0,'cutoff':'2026-10-26'}
(P/'coverage-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
