"""Reproducible F6 legal-risk reference candidate sweep v1.2.
Run from legal-risk folder containing private extracted texts and public/sources.json.
No network; no publication. Candidate classification is conservative, not semantic-completeness certification.
"""
import re,json,csv,hashlib,pathlib,collections
import argparse
a=argparse.ArgumentParser();a.add_argument('--workspace',default='.');args=a.parse_args()
P=pathlib.Path(args.workspace).resolve();D=P/'private';O=P/'public'
lex={
'explicit':[r'international\s+humanitarian\s+law',r'\bIHL\b',r'laws?\s+of\s+war(?:fare)?',r'law\s+of\s+armed\s+conflict',r'\bLOAC\b',r'jus\s+in\s+bello',r'Geneva',r'Hague',r'Article\s+36',r'Martens',r'war\s+crimes?',r'crimes?\s+against\s+humanity',r'Kriegsverbrechen',r'Völkerstrafgesetzbuch',r'folkrättsbrott',r'krigsbrott',r'droit\s+international\s+humanitaire',r'crimes?\s+de\s+guerre',r'humanitäre[nmsr]?\s+Völkerrecht',r'Genfer\s+Abkommen',r'humanitära\s+rätt',r'humanitär\s+rätt',r'krigets\s+lagar',r'droit\s+des\s+conflits\s+armés'],
'concept':[r'distinction',r'proportionality',r'precautions?\s+in\s+attack',r'military\s+necessity',r'unnecessary\s+suffering',r'superfluous\s+injury',r'indiscriminate',r'civilian\s+harm',r'non[- ]?combatants?',r'protected\s+(?:persons|objects)',r'rules\s+of\s+engagement',r'weapons?\s+review',r'meaningful\s+human\s+control',r'civilian\s+population',r'civilian\s+objects',r'lawful\s+attack',r'international\s+law'],
'indirect':[r'lawful\s+(?:use|force)',r'responsible\s+(?:use|sales)',r'legitimate\s+military',r'international\s+obligations',r'human\s+dignity',r'preservation\s+of\s+life',r'civilian\s+protection',r'ethical\s+end[- ]?use',r'controversial\s+weapons',r'prohibited\s+weapons',r'human\s+authori[sz]ation',r'target\s+validation',r'operator\s+judgment',r'auditability',r'escalat\w*',r'reassessment',r'changed\s+capabilit',r'prior\s+(?:written\s+)?(?:approval|consent|permission)',r'end[- ]?use',r'human\s+rights',r'human[- ]in[- ]the[- ]loop',r'principles?\s+of\s+use',r'unlawful\s+surveillance',r'knowingly',r'intentional\w*'],
'generic':[r'applicable\s+law',r'compliance',r'legal\s+(?:counsel|department|unit)',r'general\s+counsel',r'board\s+of\s+directors',r'warning\w*',r'hazard\w*',r'insurance',r'indemnif\w*',r'export\s+control',r'audit\w*',r'ethic\w*',r'war\s+risk',r'war[- ]hazard']}
(O/'lexicon.json').write_text(json.dumps({'version':'legal-risk-v1.2','patterns':lex,'method':'case-insensitive multiline text; all matches retained; no autonomy co-occurrence filter; source-specific semantic follow-up documented separately'},indent=2))
rows=[];counts=[];seen={}
for s in json.loads((O/'sources.json').read_text()):
 if not s['screened']:continue
 sid=s['source_id'];f=D/(sid+('-scoped' if sid=='LR47' else '')+'.txt');t=f.read_text();n0=len(rows)
 for bucket,patterns in lex.items():
  for pat in patterns:
   for m in re.finditer(pat,t,re.I):
    start=t.rfind('\n',0,m.start())+1;end=t.find('\n',m.end());end=len(t) if end<0 else end
    context=t[max(0,m.start()-160):min(len(t),m.end()+180)];sig=hashlib.sha256((sid+'|'+re.sub(r'\s+',' ',context).lower()).encode()).hexdigest()
    oid=f'LRO{len(rows)+1:05d}';dupe=seen.get(sig,'');seen.setdefault(sig,oid)
    cl={'explicit':'explicit IHL reference candidate','concept':'possible substantive concept; generic/false-positive context possible','indirect':'plausible indirect connection; IHL link unestablished','generic':'generic legal/ethical language; no established IHL connection'}[bucket]
    if sid in ['LR24','LR25'] and bucket=='generic':cl='generic insurance/loss allocation; not an IHL restraint'
    rows.append(dict(occurrence_id=oid,source_id=sid,page_or_scope=('PDFpage'+str(t[:m.start()].count('\f')+1) if s.get('pdf_pages') else ('sections801/876' if sid=='LR47' else 'HTML')),extracted_line=t[:m.start()].count('\n')+1,char_start=m.start(),char_end=m.end(),exact_short_extract=m.group(0),necessary_context='Candidate in '+s['title']+'; source-level scope/version controls in sources register. Locator and private context hash permit checking; legal conclusion only if linked promoted evidence row.',context_sha256=hashlib.sha256(context.encode()).hexdigest(),search_term_or_reason=pat,bucket=bucket,classification=cl,confidence='candidate only; manual evidence passages separately checked',negation_exception_status='not automatically inferred; read associated legal evidence exception field',linked_instrument='see evidence and version-chain registers; no automatic incorporation inference',document_date_version=s['date'],source_url=s['url'],retrieved_utc=s.get('retrieved_utc',''),source_sha256=s.get('sha256',''),access_depth=s['access'],extraction=s.get('extraction',''),duplicate_of=dupe,rights='minimal matched legal phrase only; full contextual source not redistributed'))
 counts.append(dict(source_id=sid,full_extracted_scope=True,scope=s['screening_scope'],pdf_pages=s.get('pdf_pages',''),processed_chars=len(t),occurrences=len(rows)-n0,unique_contexts=len(set(r['context_sha256'] for r in rows[n0:])),image_ocr=False,manual_semantic_review='promoted passages plus purposive nonhit sample; not certified whole-document human semantic review'))
def save(n,rs):
 (O/(n+'.json')).write_text(json.dumps(rs,ensure_ascii=False,indent=2)+'\n')
 with (O/(n+'.csv')).open('w',newline='') as f:
  w=csv.DictWriter(f,list(rs[0]) if rs else []);w.writeheader();w.writerows(rs)

# Reviewed direct/concept groups and manually added nonhit-language signals.
evidence=json.loads((O/'evidence.json').read_text());links=collections.defaultdict(list)
for e in evidence:links[e['source_id']].append(e['record_id'])
links['LR11']=['LRE21'];links['LR12']=['LRE21'];links['LR22']=['LRE21'];links['LR23']=['LRE21'];links['LR14']=['LRE22'];links['LR42']=['LRE22'];links['LR18']=['LRE20'];links['LR45']=['LRE19']
false=[]
for r in rows:
 sid=r['source_id'];term=re.sub(r'\s+',' ',r['exact_short_extract']).lower()
 r['linked_record_ids']=';'.join(links[sid]);r['review_status']='lexical candidate retained; not individually adjudicated'
 r['manual_context_note']='No substantive safeguard inferred from candidate label.'
 if r['bucket'] in ['explicit','concept']:
  r['review_status']='manual contextual review2026-10-26; source/term groups with every locator retained'
  r['confidence']='reviewed reference classification; applicability limited by linked claim'
  if r['bucket']=='explicit':
   r['classification']='explicit IHL reference'
   r['manual_context_note']='Legal text or procedural reference, not by itself a company product safeguard.'
   if term in ['hague','article 36'] and sid in ['LR17','LR18']:
    r['classification']='rejected false positive';r['manual_context_note']='The Hague is a location/communication address, or RomeStatuteArticle36 concerns judges, not Additional Protocol I weapons review.';false.append(r['occurrence_id'])
   elif 'against humanity' in term or 'völkerstrafgesetzbuch' in term:
    r['classification']='plausible indirect connection';r['manual_context_note']='International criminal law/crimesagainsthumanity context; not necessarily armedconflict/IHL offence. Statutory title crossreference not corporatecontrol.'
   if sid=='LR09':r['manual_context_note']='Court case status/link headings in Swedish/English; allegations/pending judgment, not guilt or vendor rule.'
   if sid=='LR18' and r['classification']!='rejected false positive':r['manual_context_note']='Treaty participation declarations/communications; statement belongs to declaring state, not uniform treaty text or company duty.'
   if sid=='LR27':r['manual_context_note']='Unofficial English translation of2021judgment; includes party pleas as well as court response. Not final conviction or authoritative Frenchoriginal.'
   if sid=='LR37':r['manual_context_note']='2024Code operative section and historical amendment/EO notes both retained; old/revoked provisions not current authority.'
   if sid=='LR38':r['manual_context_note']='Issuer reports pending complicity investigation, not final conviction; source is corporate procedural disclosure.'
   if sid=='LR44':r['manual_context_note']='ExplicitIHL clause in2020FMS/BPC militaryUAS templates. Current note incorporation unresolved; governmentrecipient duty.'
   if sid=='LR46':r['manual_context_note']='CurrentSAMMC4.4.18.4 governance/training-support LOAC reference. Technical operational explanation not republished.'
  else:
   r['classification']='plausible indirect connection'
   r['manual_context_note']='Reviewed international-law/protection context; not necessarily an IHL-specific requirement or corporate restraint.'
   if term=='distinction':
    r['classification']='rejected false positive';r['manual_context_note']='Ordinary distinction between legal categories or nondiscrimination, not combatant/civilian distinction.';false.append(r['occurrence_id'])
   elif term in ['military necessity','unnecessary suffering','superfluous injury','indiscriminate','civilian objects','lawful attack'] or (sid=='LR15' and term=='noncombatants'):
    r['classification']='clear substantive law-of-war concept without its label';r['manual_context_note']='Reviewed protection/means-of-war or lawful-attack context; rule/declaration scope remains source-specific, not proof of corporate application.'
   if sid=='LR44':r['manual_context_note']='Template combines IHL and law-on-resort-to-force; do not conflate jusinbello and jusadbellum.'
# Fully reviewed genuinely zero-lexical-hit sample yielded legal-context misses.
for sid,term,reason,translation in [
 ('LR22','Beihilfe','German intentional-assistance general criminal provision, imported throughVStGB§2; generic law not independentIHLcontrol','assistance/aiding; labelled research translation'),
 ('LR23','Geldbuße gegen juristische Personen','Corporate administrative-fine heading; distinct from corporateICCcriminaljurisdiction','fine against legal persons; labelled research translation'),
 ('LR20','Ausfuhrgenehmigung','German export-permission allegation in2023prosecutor release; procedural allegations notIHLsafeguard','export licence; labelled research translation')]:
 t=(D/(sid+'.txt')).read_text();m=re.search(re.escape(term),t,re.I)
 if not m:continue
 s=next(x for x in json.loads((O/'sources.json').read_text()) if x['source_id']==sid)
 r=dict(rows[0]);r.update(occurrence_id='LROM'+sid,source_id=sid,page_or_scope='HTML',extracted_line=t[:m.start()].count('\n')+1,char_start=m.start(),char_end=m.end(),exact_short_extract=m.group(),necessary_context=reason,context_sha256=hashlib.sha256(t[max(0,m.start()-100):m.end()+150].encode()).hexdigest(),search_term_or_reason='manual nonhit semantic review; German-language legal-context miss',bucket='manual_indirect',classification='generic legal/ethical language with no established IHL connection',confidence='manual contextual review',negation_exception_status='see linked criminal-law record',linked_instrument='VStGB/generalGermanlaw or Germanexportlicensing',document_date_version=s['date'],source_url=s['url'],retrieved_utc=s.get('retrieved_utc',''),source_sha256=s.get('sha256',''),access_depth=s['access'],extraction=s.get('extraction',''),duplicate_of='',review_status='manually added nonhit review2026-10-26',manual_context_note=reason+'; '+translation,linked_record_ids=';'.join(links[sid]))
 rows.append(r)
save('reference-occurrences',rows);save('screening-coverage',counts)

summary=dict(source_records=len(json.loads((O/'sources.json').read_text())),full_extracted_documents=len(counts)-1,scoped_enacted_act=1,failed_or_unprocessed=49-len(counts),pdf_pages_extracted=sum(x['pdf_pages'] or 0 for x in counts),processed_chars=sum(x['processed_chars'] for x in counts),occurrences=len(rows),lexical_occurrences=sum(r['bucket']!='manual_indirect' for r in rows),manual_added=sum(r['bucket']=='manual_indirect' for r in rows),reviewed_occurrences=sum(r['review_status']!='lexical candidate retained; not individually adjudicated' for r in rows),reviewed_false_positives=len(false),promoted_evidence_records=len(evidence),deduplicated_context_occurrences=sum(not x['duplicate_of'] for x in rows),lexicon_version='legal-risk-v1.2',scope_limit='Complete regex occurrence register for stated extracted text. Not complete semantic IHL recall; no image OCR; inaccessible incorporated annexes excluded. Candidate labels not findings.')
(O/'coverage-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary)
