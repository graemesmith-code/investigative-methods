# Authored audit code; requires local private source texts, not included for publication.
import json,csv,re,hashlib,collections
from pathlib import Path
P=Path(__file__).resolve().parent; W=P/'private'; P.mkdir(exist_ok=True)
meta={
'D09-15-dc-judgment':('Judgment denying petitions for review','2026-09-25','D.C. Cir.26-1049/26-1162 judgment, September25,2026; number not verified','judicial procedural order','Primary one-page order; not a universal procurement stay'),
'D09-14-mandate-order':('Mandate withholding order','2026-09-25','D.C. Cir.26-1049/26-1162 doc2194986','judicial procedural order','Primary one-page order; not a universal procurement stay'),
'D09-01-district-opinion':('Anthropic PBC v US Department of War; summary-judgment opinion','2026-08-27','N.D. Cal. 3:26-cv-01996-RFL ECF250','judicial ruling','Primary court opinion; not a weapons-law merits holding'),
'D09-02-dc-opinion':('Anthropic PBC v US Department of War; majority and dissent','2026-09-25','D.C. Cir. 26-1049 consolidated26-1162 doc2194984','judicial ruling','Majority denial and dissent must not be conflated; FASCSA procurement exclusion'),
'D09-03-kaplan-initial':('Declaration of Jared Kaplan','2026-03-09','N.D. Cal. ECF6-1','sworn company account','Declarant testimony; separates existing platform contracts and proposed GenAI.mil change'),
'D09-04-ramasamy-initial':('Declaration of Thiyagu Ramasamy','2026-03-09','N.D. Cal. ECF6-3','sworn company account','Public-sector executive; personal knowledge or reviewed company records'),
'D09-05-technical-declaration':('Declaration of Thiyagu Ramasamy','2026-06-10','N.D. Cal. ECF166-4','sworn company account','Contractual restrictions distinguished from technical inability to monitor or intervene in classified deployments'),
'D09-06-amicus-military':('Former service secretaries and retired senior military officers amicus brief','2026-03-12','N.D. Cal. ECF58','amicus legal argument','Civilian control of military and constitutional rule of law are not automatically civilian-protection IHL duties'),
'D09-07-final-relief':('Order of final relief','2026-08-27','N.D. Cal. ECF251','judicial order','Vacatur and injunction subject to express lawful procurement choice carveout'),
'D09-08-judgment':('Judgment','2026-08-27','N.D. Cal. ECF252','judgment','Judgment refers to orders; latest docket not fully accessible'),
'D09-09-rehearing-response-order':('Order requesting rehearing response','2026-10-15','D.C. Cir. doc2198350','procedural order','Requires response within15days; does not grant rehearing or vacate decision'),
'D09-10-rehearing-amicus':('Seventeen former national-security officials amicus on panel rehearing','2026-10-20','D.C. Cir.26-1049/26-1162','amicus legal argument','Counsel argument, not court holding; printedp9 invokes military AI international-law commitment'),
'D09-11-doj-correction':('DOJ letter correcting administrative reconsideration receipt statement','2026-05-12','D.C. Cir. doc2172918','government correction','Email received in wrong channel; agency accepted reconsideration request as timely'),
'D09-12-appendix-vol4':('Appellate appendix volume4 including signed Anthropic–Palantir addenda','2026-04-22','D.C. Cir. doc2169955 App293–422; contractApp391–407','mixed public-filed exhibits','Includes declarations, policy, signed historical contracts and government response; not all content a ruling'),
'D09-13-rehearing-petition':('Anthropic petition for panel rehearing with opinion attachment','2026-10-13','D.C. Cir. doc2197902','party legal argument','Includes duplicate September25 opinion; filing is not relief'),
'D10-01-mistral':('Mistral Inc. bid protest','2024-12-13','GAO B-422905; B-422905.2','GAO decision','Mistral Inc.Bethesda is not Mistral AI; denied sole-source protest; alleged certifications not proven test failures'),
'D10-02-altavian':('Altavian Inc. bid protest','2019-09-17','GAO B-417701; B-417701.2','GAO decision; antecedent','Outside2020–26 period retained only as antecedent; target-accuracy evaluation not IHL determination'),
'D10-03-anduril-2021':('Anduril Industries Inc. bid protest','2021-02-22','GAO B-419420','GAO decision','ABMS competition/task-order scope; not autonomous-weapon safety ruling'),
'D10-04-anduril-2026-docket':('Anduril Industries Inc. bid protest docket','2026-09-04','GAO B-424504.2; solicitation70RDA226R00000001','official docket metadata','FiledAug12, dismissedSep4; no public reasoning retrieved'),
'D10-05-cofc-2023':('System Dynamics International Inc. v United States and Strata-G Solutions LLC','2023-10-06','COFC23-431 ECF61; sealedSept21 publicredactedOct6','judicial ruling','SUAS engineering-support award enjoined for evaluation of personnel qualifications, not failed autonomy test'),
'D11-01-ndia-2024':('NDIA comments on DIB adoption of AI for defense applications','2024-07-22','RFI2024-11195','trade-association advocacy','Mixed position: humanitarian safeguards and human oversight alongside request to remove defence-use licensing restrictions'),
'D11-02-aia-action-plan':('AIA recommendations for AI Action Plan','2025-03','AIA submission','trade-association advocacy; partial access','PDF download403; webview accessible but no local full-text sweep; not promoted'),
'D11-03-aia-aviation':('AIA AI/ML for Aviation policy statement','2026-03-12','AIA20216-01 filename','trade-association policy; partial access','PDF download403; webview2pages; no local full-text sweep; aviation adjacency not weapons-duty claim'),
'D11-04-psc-index':('PSC AI comments announcement','2026-03-20','PSC public announcement','announcement only','Underlying submission not obtained; no inferred policy details'),
'D11-05-ndia-april':('NDIA comments on draft GSA AI clause','2026-04-03','Draft GSAR552.239-7001','trade-association advocacy','Proposed edits and risk allocation, not adopted rule; request13 distinguishes discretionary restrictions from mandatory safeguards'),
'D11-06-ndia-august':('NDIA comments on revised GSA LLM clause','2026-08-03','NoticeMVAC202601','trade-association advocacy','Requests scope/privity/data/IP/notice tailoring; not evidence each request adopted'),
'D11-07-gsar-deviation':('Consolidated GSAM/GSAR class deviation RGO-2026-01','2026-09-28 revision; LLM provisions effective2026-10-19','GSAR539.71;552.239-7001','government class deviation','Consolidated230pages broader than AI; actual applicability requires incorporation; licences lane owns provision analysis'),
'D11-08-gsar-june-proposal':('GSA revised proposed AI clause','2026-06-17','Federal Register2026-12205','government proposal','Says revised after comments; not final adopted text and no individual commenter causation established')}
logs=[]
for f in sorted(W.glob('retrieval-log-*.json')):logs+=json.loads(f.read_text())
byid={r['document_id']:r for r in logs}
sources=[]
for id,m in meta.items():
 r=byid.get(id,{'document_id':id});f=W/(id+'.txt');pages=[]
 if f.exists():
  pages=f.read_text().split('\f');pages=pages[:-1] if not pages[-1].strip() else pages
 r.update(dict(zip(['title','document_date_version','locator','evidence_status','context_and_limit'],m)))
 r.update({'lane':int(id[1:3]),'jurisdiction':'United States','access_depth':'full downloaded text' if pages else 'partial webview or inaccessible download','processed_pages':len(pages),'public_rights_disposition':'CITATION + AUTHORED ANALYSIS + MINIMAL EXTRACT ONLY; raw excluded by conservative whitelist','private_copy':bool(pages),'cutoff':'2026-10-26','currency_limit':'As dated document; no full current docket completeness warranted' if id.startswith('D09') else 'No inference of later amendment or contract incorporation'})
 if id=='D10-04-anduril-2026-docket':r.update(full_text_extracted=True,access_depth='full docket HTML text; no underlying decision')
 sources.append(r)
def dump(name,rows):
 (P/(name+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with (P/(name+'.csv')).open('w',newline='') as f:
  w=csv.DictWriter(f,keys);w.writeheader();w.writerows([{k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in rows])
dump('source-register',sources)
terms={
'explicit_ihl':[r'international humanitarian law',r'global humanitarian law',r'laws? of (?:armed conflict|war)',r'\bIHL\b',r'\bLOAC\b',r'jus in bello',r'Geneva (?:Convention|Conventions)',r'Hague (?:Convention|Conventions)',r'Article 36',r'Martens Clause'],
'clear_substantive_concept':[r'civilian (?:harm|casualt(?:y|ies)|protection)',r'non[- ]combatants?',r'protected (?:persons|objects)',r'war crimes?',r'precautions? in attack',r'military necessity',r'unnecessary suffering',r'superfluous injury',r'indiscriminate attacks?',r'rules of engagement',r'weapons? review',r'meaningful human control',r'human (?:authorization|authorisation)',r'target validation'],
'plausible_indirect':[r'international law',r'international obligations',r'human dignity',r'preservation of life',r'ethical end.use',r'responsible sales',r'controversial weapons',r'prohibited weapons',r'human.in.the.loop',r'human.on.the.loop',r'human (?:oversight|review|judg(?:e)?ment|decision.makers?)',r'human or machine oversight',r'fully autonomous',r'lethal autonomous',r'autonomous weapons?',r'lethal (?:action|warfare|operations?)',r'Kinetic action',r'final determinations',r'legitimate military',r'lawful (?:use|Government purpose|military|purpose)',r'responsible (?:AI|use)',r'operator judg(?:e)?ment',r'escalation',r'de.escalation',r'end.use',r'guardrails?',r'civilian(?:s)?',r'proportionality',r'distinction',r'autonomous',r'weapon(?:s)?',r'target(?:ing)?'],
'generic_legal_ethical':[r'applicable law',r'comply with (?:all )?(?:the )?law',r'legal (?:review|approval|obligations?|requirements?)',r'lawful',r'unlawful',r'human rights',r'ethical',r'export control',r'audit(?:ability)?',r'safety',r'safe(?:guards)?',r'suspend',r'suspension',r'terminat(?:e|ion)',r'indemnif(?:y|ication|ication)',r'liability',r'oversight',r'change (?:control|notice)',r'material change',r'certification',r'approval',r'prohibit(?:ed|ion)?',r'restrict(?:ed|ion|ions)?',r'except(?:ion)?',r'waiv(?:e|er)']}
(P/'lexicon-v1.json').write_text(json.dumps({'version':'F6-D-LEX-1','date':'2026-10-26','case_insensitive':True,'normalization':'whitespace collapsed per PDF page; no autonomy co-occurrence gate','patterns':terms},indent=2)+'\n')
regex=re.compile('|'.join('(?P<c'+str(i)+'>'+p+')' for i,(cat,p) in enumerate((cat,p) for cat,ls in terms.items() for p in ls)),re.I)
lookup=[cat for cat,ls in terms.items() for p in ls]
rows=[];private=[];page_stats=[]
for s in sources:
 id=s['document_id'];f=W/(id+'.txt')
 if not f.exists():continue
 pages=f.read_text().split('\f');pages=pages[:-1] if not pages[-1].strip() else pages
 for pn,t in enumerate(pages,1):
  txt=re.sub(r'\s+',' ',t).strip();matches=list(regex.finditer(txt));page_stats.append({'document_id':id,'pdf_page':pn,'characters':len(txt),'hits':len(matches),'text_sha256':hashlib.sha256(txt.encode()).hexdigest()})
  for j,m in enumerate(matches,1):
   cat=lookup[int(m.lastgroup[1:])];context=txt[max(0,m.start()-180):m.end()+220]
   exact=m.group();near=[x.group() for x in regex.finditer(context)]
   fp=None
   if exact.lower()=='civilian' and re.search(r'civilian (?:control|military leaders|agency|agencies|lawyer)',context,re.I):fp='Civilian governmental status/control, not automatically protection of non-combatants'
   if exact.lower()=='target' and re.search(r'target (?:date|price|rate)',context,re.I):fp='Non-weapons target usage'
   cls='rejected_false_positive' if fp else cat
   reviewed=(id=='D09-12-appendix-vol4' and 99<=pn<=115) or (id=='D11-01-ndia-2024' and pn in [2,3,5,10,12,13,15]) or (id=='D09-10-rehearing-amicus' and pn in [17,18,19]) or id in ['D09-07-final-relief','D09-09-rehearing-response-order']
   row={'occurrence_id':f'{id}:p{pn}:m{j}','document_id':id,'pdf_page':pn,'page_character_offset':m.start(),'clause_locator':'App'+str(pn+292) if id=='D09-12-appendix-vol4' else 'PDF page '+str(pn),'short_original_extract':exact,'classification':cls,'confidence':'low: lexical candidate' if not reviewed else 'medium: passage reviewed; classification contextual','search_reason':cat,'context_summary':fp or s['context_and_limit'],'nearby_reference_terms':'; '.join(dict.fromkeys(near)),'negation_exception_or_disclaimer_nearby':bool(re.search(r'\b(?:not|no|except|unless|however|only|disclaim|without|limited)\b',context,re.I)),'linked_instrument':'See version-incorporation-chains.json for document-level chain','document_date_version':s['document_date_version'],'access_depth':s['access_depth'],'evidence_status':s['evidence_status'],'review_status':'promoted passage manually reviewed' if reviewed else 'retained machine candidate; not individually adjudicated','context_sha256':hashlib.sha256(context.encode()).hexdigest(),'dedup_text_key':hashlib.sha256(re.sub(r'[^a-z ]','',context.lower()).encode()).hexdigest(),'rights':'Common legal/search expression only; surrounding source prose not republished','source_url':s.get('url','')+'#page='+str(pn)}
   rows.append(row);private.append(dict(row,private_exact_context=context))
dump('reference-occurrences',rows);dump('page-coverage',page_stats)
(W/'occurrence-contexts-PRIVATE.json').write_text(json.dumps(private,ensure_ascii=False,indent=2))
summary={'sources_registered':len(sources),'sources_local_full_text':sum(bool(s['processed_pages']) for s in sources),'physical_text_pages':len(page_stats),'lexical_occurrences':len(rows),'unique_context_keys':len({r['dedup_text_key'] for r in rows}),'classification_counts':dict(collections.Counter(r['classification'] for r in rows)),'manual_passage_occurrences':sum('manually' in r['review_status'] for r in rows),'not_a_claim_of_exhaustive_semantic_review':True,'duplicate_opinion_attachment':'D09-13 includes D09-02 opinion; physical counts not unique documentary evidence','limitations':['Local lexicon sweep full text, but semantic candidates not all individually adjudicated','No OCR for every image; signature dates manually rendered and corrected','Appendix non-text content may be missed','Partial webview AIA/PSC not full screened denominator','No complete latest docket retrieved at cutoff']}
(P/'coverage-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
