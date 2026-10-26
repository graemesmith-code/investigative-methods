#!/usr/bin/env python3
"""F6 licences v2. Read private source texts; publish offsets/labels, not source bodies."""
import pathlib,json,csv,re,hashlib,collections,datetime,os
ROOT=pathlib.Path(__file__).parent
P=pathlib.Path(os.environ.get('F6_SOURCE_DIR', str(ROOT/'private_working')))
R=pathlib.Path(os.environ.get('F6_OUTPUT_DIR', str(ROOT/'private_working'/'lexical_rebuild')))
R.mkdir(parents=True,exist_ok=True)
# Rebuild creates candidate outputs in a separate directory; it never overwrites reviewed public registers.
def dump(name,rows):
 (R/(name+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 if rows:
  fields=list(dict.fromkeys(k for r in rows for k in r))
  with (R/(name+'.csv')).open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()} for r in rows)
versions={
'6abf8606f3b5be6e77c772a9':'2026-10-05 onward at cutoff','6a71fc900a1dd8dd3ab8ab60':'2026-08-04–2026-10-05','6996e129419a5ab7b8e1437c':'2026-02-19–2026-08-04','690cf7ae2d02e5d77d62665c':'2025-11-06–2026-02-19','68ffd60edb2da36d2ec7ae3f':'2025-10-27–2025-11-06','68519cc227a6232295ce367b':'2025-07-11–2025-10-27','67f82652fa8ceb7af1542f67':'2025-04-12–2025-07-11','679bba07525289e24a6cc05a':'2025-02-03–2025-04-12','6785ae3cb9988e0b5f4262a9':'2025-01-14–2025-02-03','6751c17a4189a5fd3cc6683a':'2024-12-06–2025-01-14','66c8584212f4607b0a978b97':'2024-08-27–2024-12-06','66b6e131138124a6b3af9afc':'2024-08-10–2024-08-27','66b6dcb0c840f9f84cbb9023':'2024-08-10–2024-08-10 (portal same-day anomaly)','66630ff93937e7d0ac684c48':'2024-06-07–2024-08-10','6638f0e6dc40b63bb55f5bdc':'2024-05-06–2024-06-07','657c6fb5d2d35ace6e78a7bf':'2023-12-15–2024-05-06','649b3192ed79b18a284396fe':'2023-06-27–2023-12-15','6495c2734003c6cdfa56464a':'2023-06-23–2023-06-27','64650d4e24d2cebd0d8cbaf9':'2023-05-17–2023-06-23','6463855268f3c907f95ea969':'2023-05-17–2023-05-17 (portal same-day anomaly)','645135a9fb29deecdd332f9d':'2023-05-02–2023-05-17','644fedc94a10e02157a8df14':'2023-05-01–2023-05-02'}
meta={
'anduril':('Anduril Industries, Inc.','Delaware, USA','Lattice SDK','updated 2026-07-31; developer agreement, not operational contract'),
'skydio':('Skydio, Inc.','USA; federal exceptions; California for non-government customers','Enterprise offerings','live text retrieved 2026-10-26; contract applicability unresolved'),
'palantir':('Palantir Technologies Inc. / entity defined by underlying agreement','Underlying agreement jurisdiction','AIP; Carahsoft licence separately identified','current AIP 2026-10-05; seed 2025-02-03–2025-04-12'),
'aip':('Palantir entity defined by underlying agreement','Underlying agreement jurisdiction','AIP third-party model addendum','See dated version chain'),
'auterion':('Auterion Inc. unless order names another entity','Delaware entity; California governing law','Software; hosted services in undated live form','2022-11-10 PDF and undated live webpage are parallel public texts, chronology unresolved'),
'dir':('Skydio, Inc. and Texas Department of Information Resources','Texas, USA','DIR-CPO-5863 COTS framework','start 2025-10-21; terms through 2027-10-21; documents posted 2026-02-18'),
'helsing':('Helsing Limited, England and Wales no.13447361','England and Wales; G-Cloud framework precedence','G-Cloud 14 software and related services','cover October 2024; URL date May 2024 is not effective date'),
'northrop':('Northrop Grumman Systems Corporation','USA; federal contractual flowdown','Ridgeback program supplier addendum PA3051','Ridgeback Additional Contract Clauses 2021-12-15'),
'dynamo':('DynamoFL, Inc. trading as Dynamo AI','California, USA','Non-production evaluation agreement; AUP','trial updated 2025-06-20; AUP undated retrieved 2026-10-26'),
'applied':('Applied Intuition, Inc. and Kodiak Robotics, Inc.','Delaware entities; California contract','Simulation software; 2018 master and 2024 order','master dated 2018-09-27, executed 09-28; order dated 2024-09-19, executed 09-30'),
'dfars':('US Department of Defense','USA federal procurement','Commercial software vs technical data rules','current official text retrieved 2026-10-26'),
'anthropic':('Anthropic, PBC','USA; contract-specific','AUP; Bedrock; Vertex','Bedrock last modified 2023-10-03; Vertex 2024-03-19; AUP version-specific'),
'google':('Google LLC','Agreement-specific','Google model/Cloud AUP','live retrieved 2026-10-26; current acceptance unresolved'),
'azure':('Microsoft Corporation','Agreement-specific','Azure OpenAI code of conduct','live retrieved 2026-10-26; current acceptance unresolved'),
'nvidia':('NVIDIA Corporation','Agreement-specific','Trustworthy AI incorporated into model licence','last modified 2024-06-27'),
'quantum':('Quantum-Systems, Inc.; German form entity separately unresolved','USA vs Germany','Standard terms of sale','US filename August2025; German filename31May2023; not military order'),
'leidos':('Leidos, Inc.','USA; federal exceptions','GeoRover','EULA 2020-09-09'),
'bae':('BAE Systems Information and Electronic Systems Integration Inc.','USA','GXP desktop','2026-04 URL; full version not retrieved'),
'shield':('Shield AI; contracting entity unresolved','Unresolved','Hivemind software licence and general terms linked by official hub','viewer only; underlying PDF not retrieved'),
'openai':('OpenAI entity per agreement','Agreement-specific','Usage policy','not locally retrieved; do not infer applicability')}
logs=[]
for n in ['fetch_log.json','fetch_more_log.json','fetch_last_log.json']:
 if (P/n).exists():logs+=json.loads((P/n).read_text())
sources={}
for d in logs:
 k=d['id']; prefix=k.split('-')[0];m=meta.get(prefix,('Unresolved','Unresolved','Unresolved','Unresolved'))
 d={k2:v for k2,v in d.items() if k2 not in ['local_file']}
 d.update(document_id=k,legal_entity=m[0],jurisdiction=m[1],product=m[2],version=m[3],rights='Citation and short justified extracts only; source body excluded from publication; copyright clearance not established',cutoff='2026-10-26',access_depth='fetch failed' if d.get('status')=='failed' else 'downloaded text; full lexical screen where eligible; promoted passages manually reviewed')
 files=[x for x in [P/(k+'.pdf'),P/(k+'.html')] if x.exists()]
 if files:
  f=files[0];d.update(sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size,source_format=f.suffix)
 if k.startswith('aip-'):d['version']=versions.get(k[4:],'unresolved')
 if k.startswith('skydio-20'):d['version']=k[7:]
 if k=='skydio-eula':d['version']='Archived EULA last updated 2023-09-20; pointed to by 2024 manual'
 if k=='skydio-x10d-intl':d.update(version='Document3.0, 2024-06-27; vehicle34.1.125/controller34.1.81',product='X10D INTL Operator Manual',rights='Citation and governance-only short extract; full manual and operating instructions excluded')
 if k=='skydio-safety-guide':d['version']='Updated 2026-09-02; distinct from 2024 operator manual'
 sources[k]=d
# Exclude navigation/empty viewer text from fully processed denominator.
excluded={'palantir-aip-versions','shield-sla-viewer','dir-skydio-contract-viewer','dir-skydio-appendix-viewer','google-cloud-aup'}
alias={'palantir-aip-current':'aip-6abf8606f3b5be6e77c772a9','palantir-aip-seed':'aip-679bba07525289e24a6cc05a','helsing-ai-infra-terms':'helsing-gcloud14'}
lex={
'explicit':r'\b(?:international humanitarian law|IHL|law(?:s)? of war|law of armed conflict|LOAC|jus in bello|Geneva|Hague|customary humanitarian law|Article\s+36|Martens Clause|rules of engagement|war crimes|weapons review)\b',
'concept':r'\b(?:distinction|proportionality|precautions in attack|military necessity|unnecessary suffering|superfluous injury|indiscriminate|civilian harm|non.?combatants|protected persons|protected objects|meaningful human control)\b',
'oblique':r'\b(?:weapon\w*|battlefield|human review|natural person|human being|human.in.the.loop|human oversight|human control|human authorization|operator judgment|pilot in command|civilian|human rights|human dignity|preservation of life|responsible use|responsible sales|ethical|end.use|lawful|illegal|unlawful|international obligations|treaties|authoriz\w*|warnings?|audit\w*|suspend\w*|suspension|deactivat\w*|disabl\w*|terminat\w*|territor\w*|safety|harm\w*|applicable law\w*|all laws|local laws|federal laws|generally accepted practices|regulations|military|training|risk|review)\b'}
(R/'LEXICON_v2.json').write_text(json.dumps({'version':'F6-licence-lexicon-v2-2026-10-26','patterns':lex,'change_from_v1':'Replaced narrow as-a-weapon phrase probe with broad weapon stem; added generic treaties, aviation-law and natural-person forms; all eligible archives rescanned. v1 was exploratory, not a retained complete run.','method':'No autonomy/weapon co-occurrence filter. Match boundaries checked; semantic promotion review separate. German/French equivalents required for any future non-English full-text extension; German source here unavailable.'},indent=2)+'\n')
occ=[];coverage=[];direct=[]
for k,d in sources.items():
 p=P/(k+'.txt')
 if not p.exists() or k in excluded or k in alias:
  d['screen_status']='excluded duplicate alias of '+alias[k] if k in alias else 'not fully screenable locally; see access log'
  continue
 t=p.read_text();
 if k=='nvidia-trustworthy':
  # Full HTML is retained privately; isolate legal body from navigation without changing source hash.
  a=t.find('Ethical Use.');b=t.find('Company Information',a);t=t[a:b if b>a else a+2500]
  (P/(k+'.screen.txt')).write_text(t)
 pages=t.split('\f');np=len(pages)-(1 if not pages[-1].strip() else 0)
 d.update(screen_status='full extracted-text lexical screen v2; not a claim of full image/OCR or every-link semantic completeness',text_sha256=hashlib.sha256(t.encode()).hexdigest(),screened_characters=len(t),screened_pages=np if (P/(k+'.pdf')).exists() else None)
 counts=collections.Counter();off=0
 for pn,page in enumerate(pages,1):
  for kind,pattern in lex.items():
   for mm in re.finditer(pattern,page,re.I):
    token=mm.group();start=off+mm.start();line=t.count('\n',0,start)+1
    # Original phrases are not copied repeatedly; lexicon pattern + offset identifies the occurrence.
    status='possible explicit anchor; requires context review' if kind=='explicit' else 'possible substantive concept; requires context review' if kind=='concept' else 'generic legal/ethical or adjacent control; IHL link unestablished'
    if kind=='explicit':direct.append((k,pn,line,token))
    if re.search(r'weapon|battlefield|human review|natural person|human being|human.in.the.loop|human oversight|human control|human rights|lawful|treaties',token,re.I):status='plausible indirect connection; context and exceptions must be read'
    if k=='azure-code' and kind=='explicit':status='rejected false positive';context='Penetration-testing Rules of Engagement, not military ROE.'
    if token.lower() in ['distinction'] and 'distinction' in page.lower():status='ambiguous ordinary-language term; not established law-of-war concept'
    context='Occurrence retained without assuming an IHL duty. See source page/line, normalized findings and reviewed occurrence notes; an audit/termination/warning may protect IP, safety or payment rather than civilians.'
    if k.startswith('skydio') and re.search('pilot|safety|warning|law|regulation',token,re.I):context='Flight safety, pilot responsibility or legal compliance context; not by itself target verification, training completion or military practice.'
    if k.startswith('applied') and token.lower()=='natural person':status='rejected false positive for human decision control';context='Licensed-seat definition in commercial simulation order; not human review of a target decision.'
    if k=='azure-code' and kind=='explicit':status='rejected false positive';context='Penetration-testing Rules of Engagement, not military ROE.'
    occ.append({'occurrence_id':f'LC-O{len(occ)+1:05d}','document_id':k,'page':pn if (P/(k+'.pdf')).exists() else '', 'extracted_line':line,'char_start':start,'char_end':off+mm.end(),'lexicon_family':kind,'matched_pattern_key':kind,'normalized_search_term':token.lower(),'extract_method':'Exact short lexical anchor recoverable at source offset; no surrounding proprietary text republished','context':context,'classification':status,'confidence':'low unless linked to reviewed finding','version':d['version'],'access_depth':d['access_depth'],'source_url':d['url'],'rights':d['rights'],'dedup_text_key':hashlib.sha256(re.sub(r'\s+',' ',page[max(0,mm.start()-90):mm.end()+90].lower()).encode()).hexdigest()[:16]})
    counts[kind]+=1
  off+=len(page)+1
 coverage.append({'document_id':k,'pages':d['screened_pages'],'characters':len(t),'explicit_anchor_hits':counts['explicit'],'concept_hits':counts['concept'],'oblique_hits':counts['oblique'],'method':'Full extracted text lexical v2; manual promoted-passages and nonhit sample; no unqualified no-safeguard conclusion','image_limit':'Text PDFs; selected visual checks only. Unextracted image text not certified complete.'})
dump('sources',list(sources.values()));dump('reference_occurrences',occ);dump('screening_coverage',coverage)
(R/'direct_hits.json').write_text(json.dumps(direct,indent=2))
v=[]
for k,period in versions.items():v.append({'document_id':'aip-'+k,'family':'Palantir AIP','public_effective_period':period,'source_url':'https://palantir.pactsafe.io/versions/'+k+'.pdf','status':'portal-listed version; actual customer incorporation not established','comparison':'Natural-person review and hosting-specific conditions; no assumption all model rows identical'})
for k,d in sources.items():
 if k.startswith('skydio-20') or k=='skydio-enterprise':
  t=(P/(k+'.txt')).read_text();has=bool(re.search(r'(duly authorized governmental actions|lawful government actions)',t,re.I));v.append({'document_id':k,'family':'Skydio enterprise','public_effective_period':d['version'],'source_url':d['url'],'status':'public archive/live page; no named military order establishes accepted version','comparison':'government exception present' if has else 'no express government weapon exception in reviewed prohibition; 2022 says as weapon without article'})
dump('version_comparison',v)
print(json.dumps({'source_records':len(sources),'fully_lexically_screened':len(coverage),'pdf_pages':sum(x['pages'] or 0 for x in coverage),'occurrences':len(occ),'direct_hits':direct,'unique_context_keys':len(set(x['dedup_text_key'] for x in occ))},indent=2))
