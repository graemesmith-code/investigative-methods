import pathlib,json,collections,datetime
P=pathlib.Path(__file__).parent
rs=[json.loads(l) for l in (P/'inventory.jsonl').read_text().splitlines()]
ex=[];keep=[]
for r in rs:
 if 'newsletter' in r['title'].lower() or r['title'] in ['Green Corruption - interview with Miljøkrim','Hoja informativa del Programa GFP Subnacional']:
  ex.append(dict(url=r['url'],title=r['title'],reason='Newsletter/interview/programme factsheet outside primary corpus'));continue
 if r['org']=='Sherpa' and not r['bytes']:r['acquisition_status']='api_metadata_only';r['sha256']=None
 if r['date'] and not __import__('re').match(r'^\d{4}-',r['date']):
  try:r['date']=datetime.datetime.strptime(r['date'],'%d %b %Y').date().isoformat()
  except ValueError:pass
 keep.append(r)
# Explicit multilingual manifestations merged under substantive original identity.
groups=[['Illicit Enrichment: A Guide to Laws Targeting Unexplained Wealth','Enrichissement illicite : Guide sur les lois ciblant la richesse inexpliquée','Enriquecimiento ilícito: Una guía sobre las leyes que abordan los activos de procedencia inexplicable'],['Gold Laundering: the dirty secrets of the gold trade – and how to clean up','Goldwäsche: Die schmutzigen Geheimnisse des Goldhandels'],['A capacidade do Brasil de recuperar ativos ilícitos: Um diagnóstico de acordo com os 9 princípios da recuperação de ativos','La capacidad de Brasil para recuperar activos ilícitos: Un diagnóstico conforme a los 9 principios de la recuperación de activos'],['Engaging the private sector in Collective Action against corruption: A practical guide for anti-corruption agencies in Africa','Action Collective - Coopérer avec le secteur privé: Guide pratique pour les agences nationales de lutte contre la corruption'],['Non-conviction based forfeiture as a tool for asset recovery: Recommendations of the Lisbon Conference, 5 –7 July 2022','Perda sem condenação na recuperação de ativos: Recomendações da Conferência de Lisboa – 5, 6 e 7 de Julho 2022']]
for g in groups:
 found=[r for r in keep if r['title'] in g]
 if len(found)>1:
  primary=found[0];primary['versions']=[{k:r.get(k) for k in ['title','date','url','report_url','report_sha256','report_bytes','pages']} for r in found[1:]]
  keep=[r for r in keep if r not in found[1:]]
spot=json.load(open(P/'spotlight-browser-metadata.json'));seen=set()
for r in spot:
 if r['url'] in seen:continue
 seen.add(r['url'])
 try:r['date']=datetime.datetime.strptime(r['date'],'%d %B, %Y').date().isoformat()
 except (ValueError,TypeError):pass
 keep.append(r)
# Contextual reading ledger, no automatic fetch-as-read.
reads={
'SNA_IWT':('Methods and confidentiality surrounding empirical intelligence dataset, annex PDF pp49-54.','LE-REJ-IWT',True),
'how-technology-can-support-border-corruption-investigations':('Read methods, public/private evidence sources, fictitious scenario, dashboard access and conclusion; PDF pp5-8,12-17,23-24.','LE-REJ-FALCON',True),
'quick-guide-17-open-source-intelligence-0':('Read full four-page OSINT guide, source access and paywall caveats.','LE-REJ-OSINT',True),
'research-case-3':('Read complete three-page public-source network case study, methods and findings.','LE-REJ-ODEBRECHT',True),
'research-case-4':('Read complete three-page intelligence-derived network case study, methods and sources.','LE-REJ-IWT',True),
'working-paper-36-revealing-networks-behind-corruption-and-money-laundering-schemes':('Read surrounding empirical-data and network-measure passages PDF pp10-14 plus case construction. Method predates2026.','LE-REJ-ODEBRECHT',False),
'edition-2020-du-radar-du-devoir-de-vigilance-yves-rocher-castorama-picard-mcdonalds-france-televisions-bigard-27-des-entreprises-hors-la-loi':('Read complete substantial HTML; employee threshold, nonexhaustive universe and sources Orbis/Sirene/Infogreffe.','LE-REJ-VIGILANCE',True),
'entreprises-soumises-devoir-de-vigilance-radar-ong':('Read full launch HTML, scope, methods and access recommendation.','LE-REJ-VIGILANCE',False),
'open-data-lexemple-industries-extractives':('Read full substantial HTML; extraction-payment bottleneck and PDF access. Original report link not retrieved.','LE-SUPPORT-PAYMENTS',True),
'transparence-industries-extractives-francaises-cest-flou':('Read substantial HTML including reporting limitations and original claimant/company response. Original report not read.','LE-SUPPORT-PAYMENTS',True),
'laffaire-biens-mal-acquis-enseignements-apres-10-ans-de-combat-judiciaire-2':('Read HTML abstract only; PDF article not screened.','LE-REJ-BMA',False),
'broken-record-legal-sector-aml':('Full PDF contextual section screened via browser: pp22-28, self-declarations and supervisory constraints. Local PDF acquisition403.','LE-REJ-AML',True),
'back-of-the-courtroom-queue-rpt':('PDF via browser pp5-8: trial-delay causes, disclosure, seized devices, MLA; local acquisition403.','LE-REJ-DISCLOSURE',True),
'all-bark-and-no-bite-report':('Read HTML abstract and report scope only, not counted full report screening.','LE-REJ-SANCTIONS',False),
'power-without-responsibility':('Read HTML abstract/report introduction only, not counted full report screening.','LE-REJ-EXECUTIVES',False)}
for r in keep:
 slug=r['url'].rstrip('/').rsplit('/',1)[-1]
 if slug in reads:
  rationale,opp,deep=reads[slug];r['screening_rationale']=rationale;r['opportunity_ids']=[opp];r['deeply_read']=deep;r['fulltext_screened']=slug not in ['laffaire-biens-mal-acquis-enseignements-apres-10-ans-de-combat-judiciaire-2','all-bark-and-no-bite-report','power-without-responsibility']
 for check in json.load(open(P/'access-checks.json')):
  if (slug=='broken-record-legal-sector-aml' and 'Broken-Record' in check['url']) or (slug=='back-of-the-courtroom-queue-rpt' and 'BotCQ' in check['url']):r.update(report_url=check['url'],report_local_status=check['status'],pages=39 if slug.startswith('broken') else 18,acquisition_status='browser_pdf_acquired')
P.joinpath('inventory.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in keep));P.joinpath('excluded-discovery.json').write_text(json.dumps(ex,ensure_ascii=False,indent=2))
counts={}
for org in sorted(set(r['org'] for r in keep)):
 rr=[r for r in keep if r['org']==org];counts[org]=dict(enumerated=len(rr),acquired=sum(r['acquisition_status'] not in ['api_metadata_only','catalog_only'] for r in rr),pdf_acquired=sum('report_sha256' in r or r['acquisition_status']=='browser_pdf_acquired' for r in rr),fulltext_screened=sum(r['fulltext_screened'] for r in rr),deeply_read=sum(r['deeply_read'] for r in rr),retained_finalists=0)
P.joinpath('counts.json').write_text(json.dumps(counts,indent=2));print(json.dumps(counts,indent=2))
