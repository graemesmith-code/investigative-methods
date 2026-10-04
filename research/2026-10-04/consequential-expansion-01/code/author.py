"""Individually authored conditional mechanisms; exports do not execute investigations."""
import json,pathlib,csv,hashlib
P=pathlib.Path(__file__).resolve().parents[1];S={int(s['sys_id'][-4:]):s for s in map(json.loads,(P/'sources.jsonl').read_text().splitlines())};C=[]
def add(i,title,primary,support,initial,expected,basis,join,scope,falsifiers,required,nextcheck,novelty,docs,scores,access,extensions=None,kind='new_mechanism'):
 C.append(dict(test_id=i,title=title,kind=kind,primary_source_ids=primary,supporting_catalog_source_ids=support,initial_observation=initial,expected_observation=expected,possible_finding_and_basis=basis,operational_join=join,temporal_geographic_scope=scope,ordinary_explanations_and_falsifiers=falsifiers,mandatory_evidence=required,next_cheapest_check=nextcheck,novelty_vs_baseline=novelty,documentation_ids=docs,consequence_score=scores[0],feasibility_score=scores[1],join_route_score=scores[2],burden_tier=scores[3],access_status=access,supporting_scope_extensions=extensions or [],pair_sufficient=False,case_rule_applicability_verified=False,legal_or_logical_status='Conditional source-specific predicate; governing document and case facts must be established before a legal assertion.',checks_actually_performed='Catalog fields, prior mechanisms and cited official documentation reviewed; no matching substantive records or positive finding tested.',checks_proposed_not_performed=nextcheck,execution_status='not_executed',positive_finding=False))
add('X01','Direct industry payments versus an explicit article disclosure',[247,250],[251],
'IF an article expressly declares no relevant financial relationships, and a verified author received direct general consulting or honoraria payments from a manufacturer relevant to the article within the journal’s applicable window.',
'THEN read the full declaration, supplements and corrections against the dated direct-payment records and exact policy to determine whether a material relationship is unaccounted for.',
'An undisclosed relevant relationship can affect readers’ interpretation of clinical evidence; a payment alone proves neither bias nor policy breach.',
'CMS physician/profile ID identifies the payment recipient; DOI identifies the article. Author identity requires an independent biographical/affiliation bridge. ORCID is supporting, not an automatic CMS-to-author key.',
'US-covered recipients; payment date versus declaration/submission date and applicable policy version. Product relevance must be established, not inferred from any industry payment.',
['Namesake or wrong author','Research/institutional payment wrongly allocated to the investigator','Supplement or correction discloses the tie','Window, relevance or policy excludes the relationship','Disputed/corrected CMS report'],
['Original article and full disclosure','Journal policy at submission','Verified person identity','Direct general-payment category and payer/product','CMS corrections/dispute status'],
'Read one article’s precise declaration and policy, then confirm a permissible direct-payment record and author identity; do not start by summing institutional research payments.',
'H04 asks about payments and trial participation; R05 compares outcomes. This tests a specific declaration against a directly attributable relationship.', ['E01','E02'],[5,2,1,2],'CMS public routes documented; article/full supplement availability and author bridge unverified.')
add('X02','Fixed extractive-contract obligation versus covered receipts',[111,107],[295],
'IF the operative original contract fixes a particular annual rent, community contribution or guaranteed minimum due for one project/payer/payee and period, and the payment trigger is evidenced.',
'THEN compare that exact obligation with a demonstrably complete matching receipt stream, reconciling any payer disclosure and authorized amendment before describing a shortfall.',
'A fixed amount supplies an independent contractual benchmark for public revenue. A low or absent aggregate does not prove nonpayment.',
'Contract/project identity → legal payer → exact government/community payee → payment stream → period and currency. Company-level EITI totals cannot substitute for a project receipt.',
'Only countries/projects with granular EITI coverage; contract effective dates, trigger, payment deadline, fiscal basis, waiver and amendment history must align.',
['Amendment, waiver or suspension','Trigger not reached','Payment in another covered period or stream','In-kind or netting provision','Incomplete receipt population or confidential amount'],
['Original signed PDF and all operative amendments','Evidence of trigger and due date','Receipt coverage and accounting basis','Payer/project/payee crosswalk'],
'Find a simple fixed clause first; stop if the actual receipt dataset cannot isolate that project and stream. Avoid speculative revenue estimates from commodity prices.',
'D05/N01 reconcile two accounts of money paid. This derives the expected amount from a separately established obligation.', ['E03'],[5,2,2,3],'Contract access documented; project-level receipt completeness and amendments unverified. ESTMA is payer disclosure, not government receipt proof.')
add('X03','Reported waste destination versus actual handling authority',[218,38],[],
'IF a TRI sender reports a chemical/year transfer to a specifically identified off-site receiver under a disposal, treatment, energy-recovery or recycling code.',
'THEN resolve the actual receiving operation and compare the reported handling route with its historical permit/authorization and shipment evidence for the same waste, process and interval.',
'A verified incompatible destination or management account can expose a waste oversight gap; a transfer is not necessarily a release or a hazardous waste.',
'Sender TRIFID is not the receiver RCRA ID. Use the reported receiver identifier/address, validate the receiving site rather than a broker, and crosswalk chemical to actual regulated waste/process evidence.',
'US domestic routes with identifiable receiver; annual TRI totals may span permit changes, so dated shipment evidence is mandatory for event timing.',
['Nonhazardous or exempt stream','Permitted intermediary or onward transfer','Code or address error','Different permitted process/unit','Current permit status differs from historic authorization'],
['Form R transfer record and revisions','Historical receiver site/permit and applicable waste classification','Dated manifests/receipts or equivalent transfer evidence','Actual downstream process'],
'Inspect the transfer fields and one historical permit scope before considering any allegation; absence of a RCRA permit by itself is disqualifying as an illegality inference.',
'C01 compares emissions estimates; C02/C05 are spatial exposure. This follows the sender-to-receiver waste-management chain and its permitted process.', ['E04','E05','E06'],[5,2,3,3],'Current sender guidance and receiver modules documented; no permit, manifest or transfer record sampled. No bulk RCRA files downloaded.', ['ES01'])
add('X04','Explicit foreign-entity declarations that cannot both fit the same facts',[117,118],[],
'IF a dated LD-1 explicitly reports no qualifying foreign entity for a legal client, while a contemporaneous FARA Exhibit A identifies ownership/control of that same client that appears to meet the applicable LD-1 criteria.',
'THEN establish the exact legal entities, registration scope, activity, ownership/control facts and filing-date rules, and compare amendments before calling the declarations inconsistent.',
'Inconsistent public descriptions of who directs a policy campaign can be consequential. FARA registration alone neither triggers every LDA field nor proves a false declaration.',
'LDA registrant/client IDs and FARA registration/principal IDs are distinct. Bridge exact legal client and disclosed control relationship with dated original documents.',
'US disclosures, same legal client and relevant dates/activity. Apply filing-date thresholds; an old semiannual instructions PDF is not current quarterly guidance.',
['Different clients, affiliates or services','Foreign principal is not the qualifying controlling entity','Ownership/control changed','Threshold or report scope not met','Amended or historically appropriate answer'],
['Actual LD-1 and amendments','Actual Exhibit A and referenced ownership evidence','Applicable current or historic LDA criteria','Specific client/activity and date crosswalk'],
'Read the exact yes/no declaration and applicable rule before joining names; confirm the client is the same entity described in Exhibit A.',
'I01 adds ownership context; this tests mutually inconsistent affirmative disclosure facts within carefully matched legal scope.', ['E07','E08','E09','E24'],[5,2,1,3],'Public search/forms documented; field interpretation and cross-regime identity need manual review. No filing sampled.')
add('X05','Charity no-lobbying declaration versus specific legislative activity',[45,117],[],
'IF a charity’s applicable Form 990/Schedule C explicitly denies the relevant legislative-lobbying activity and a lobbying filing identifies that same charity’s work on specific legislation during its tax year.',
'THEN reconcile the exact activity and reporting definitions to determine whether the denial leaves a documented activity unexplained.',
'The public can scrutinize a consequential inconsistency in a tax-exempt organization’s disclosure; LDA spending totals and tax-law lobbying are not identical measures.',
'EIN anchors the charity return; LDA client names/IDs require a verified legal-entity bridge. Fiscal-year activity, not filing date or a shared brand, determines overlap.',
'US charity type, election status, return version and tax year; current instructions guide current returns, historic rules govern historic ones.',
['Executive-branch issue outside relevant legislative definition','Different affiliate','Permitted exception or accounting classification','Noncalendar fiscal year','Corrected return or report'],
['Signed return and Schedule C','Specific legislative issue/activity record','Relevant instructions for that charity/year','Entity and fiscal-year bridge'],
'Select an explicit declaration and a specific legislative activity; reject comparisons based only on rounded annual lobbying totals.',
'E08 concerns related parties; I05 concerns influence on rules. This tests a charity activity declaration under its own reporting definition.', ['E10','E24'],[4,2,1,2],'Public return and lobbying routes known; one same-entity activity and definition comparison remains untested.')
add('X06','Foreign-principal money behind a specific advertised campaign',[118,143],[],
'IF a FARA agreement/supplement itemizes a particular advertisement or campaign financed for a named foreign principal, with a sufficiently specific placement or creative reference.',
'THEN trace that placement to the archived ad and its payer/disclaimer, establishing which principal financed the message rather than treating the displayed intermediary as the ultimate sponsor.',
'A documented financing chain can reveal whose interests a public campaign serves even when it is lawful and all disclosures are technically present.',
'FARA principal/registrant/document → exact campaign/creative/placement reference → Meta ad identifier. Similar slogans, domains or spend totals are not a stable join.',
'Actual campaign dates and covered archive geography/category; receipt, agency fee and advertising spend are different quantities.',
['Different campaign with similar creative','Agent paid from unrelated funds','Disclaimer already names the principal','Agency amount includes nonadvertising services','Archive lacks the relevant ad class'],
['Original principal agreement and itemized campaign spending','Exact ad/creative/placement crosswalk','Full disclaimer and archived ad metadata'],
'Look for an explicit creative or placement identifier in one public FARA document; defer if the bridge is only a generic campaign description.',
'I04 reconciles campaign spending; S05 screens sanctioned principals. This establishes message-specific financing through an intermediary without a sanctions premise.', ['E11'],[4,1,1,3],'FARA disbursement purpose/recipient fields do not guarantee a Meta creative ID. An explicit placement reference or equivalently exact documented creative bridge is mandatory; Meta archival access/coverage remains unverified.')
add('X07','Construction before a specific prerequisite approval',[283,101],[304],
'IF an operative project decision expressly prohibits a defined construction activity until a specified written approval, and both the regulated component and actual approval date are established.',
'THEN inspect suitable dated imagery for that same activity/component before the prerequisite date, corroborating what the change actually represents.',
'A clearly evidenced sequence can expose a failure of project oversight; generic clearing before a project announcement is not the predicate.',
'Assessment project/decision ID → mapped regulated component → written prerequisite approval → image acquisition geometry/time. A registry point is not a work boundary.',
'Canada, exact project/permit component and operative amendments; imagery resolution and acquisition interval must discriminate the prohibited activity.',
['Exempt early works','Earlier valid approval or amendment','Fire or unrelated operator','Boundary error','Image resolution cannot distinguish construction'],
['Original operative condition and amendments','Positive evidence of prerequisite approval date','Component boundary','Before/after images and acquisition/quality metadata','Activity attribution'],
'Read the actual condition and map first. Stop if it does not prohibit an observable activity or if only permit-search absence supports the date.',
'C03 asks protected-area overlap; C04 measures vegetation change. This tests an express authorization sequence using positive documents and physical chronology.', [],[5,1,2,3],'Catalog pathways only for this formulation; no decision, permit or scene sampled.')
add('X08','Reclamation security actually posted versus a specific requirement',[304,305],[288],
'IF a mine’s operative permit or regulator decision sets a site-specific financial-security amount and due date, and a reliable dated record establishes security actually held for that obligation.',
'THEN reconcile the required security with the covered amount and instruments actually posted; distinguish any shortfall from the separate estimated reclamation liability.',
'An evidenced unfunded required security amount can expose public cleanup risk. A liability estimate exceeding security is not automatically a breach, and an accounting provision is not a bond.',
'Mine/permit ID → security requirement and amendments → actual beneficiary/instrument/site coverage. Issuer financial statements may contextualize capacity but cannot substitute for government security records.',
'BC mine, same obligation/date/currency and permitted instrument type; separate current posted amount, statutory requirement and forecast undiscounted liability.',
['Approved staged security or amendment','Letter of credit/guarantee omitted from cash total','Pooled instrument covers this site','Different accounting discount basis','Record predates top-up'],
['Operative security decision','Dated actual-security confirmation','Instrument conditions and beneficiary','Site allocation for pooled security','Relevant amendments'],
'Locate the exact site-specific requirement and an actual-held record. If either is unavailable, retain only a gated lead; do not subtract issuer provisions from liability estimates.',
'C08 is physical cascade risk; E06 is supplier litigation. This tests the funding of a legally specified cleanup safeguard.', ['E12'],[5,1,2,4],'Public annual reporting is documented but does not establish security holdings. Unresolved dependencies: identify the issuing BC mine-permitting office and operative security decision/amendments; identify the government custodian holding the instruments and obtain a dated site allocation or confirmation through an authorized public route. Neither document nor retrieval route is yet verified.')
add('X09','A filed mining-right claim versus that exact instrument’s status',[288,309],[],
'IF an issuer filing says it held a particular numbered Ontario mining claim at a specified reporting date.',
'THEN establish the authoritative historical status and holder/right chain for that exact instrument on that date, checking any renewal, transfer, option or reinstatement.',
'A materially unsupported assertion of project rights can affect investors and public subsidy decisions; current map absence is not evidence of historical nonownership.',
'Exact Ontario claim number and instrument type, followed through issuer subsidiary/option documents. Do not equate a project name, geological occurrence or surface title with mineral rights.',
'Ontario only; historical status at the claimed date. MLAS public active-claim view does not establish complete historical cancellation evidence.',
['Issuer holds through subsidiary or option','Registry lag or reinstatement','Different tenure instrument','Claim converted to lease','Filings describe a past rather than current interest'],
['Exact filed assertion','Authoritative historical title/status record','Subsidiary/option/transfer documents','Amendment and renewal history'],
'Extract the actual claim number from the filing and verify whether a historical record is accessible; stop if only a current absent map feature is available.',
'F04 tests corporate existence; C04 overlays land use. This tests an asserted legal project right against its own dated instrument.', ['E13'],[4,1,3,3],'Current public active-claim view documented; historical status and issuer documents not sampled.')
add('X10','Verified commercial sourcing through a facility with a serious final finding',[228,38],[],
'IF a buyer’s own dated contribution or original supplier disclosure identifies a US production facility and a final EPA finding concerns that facility during the relationship.',
'THEN establish the nature and timing of sourcing, the finding and documented buyer response/continued relationship before explaining the accountability chain.',
'A brand or major buyer may be commercially connected to significant harm not apparent from corporate names. A listing alone does not prove current orders, knowledge or liability.',
'OS Hub facility ID and original contributor evidence → physical facility/operator → EPA FRS/program ID → dated final case. Contributor upload dates are not necessarily sourcing dates.',
'US facility for EPA linkage; buyer relationship and final finding must overlap or be explicitly placed in sequence.',
['Contribution is researcher-supplied or historic','Buyer relationship ended','Different plant on same campus','Finding overturned or activity unrelated to supplied goods','Buyer already disclosed remedy'],
['Buyer-origin supplier evidence with dates','Facility/operator identity','Final enforcement record','Actual sourcing/product scope and response evidence'],
'Check who contributed the supplier assertion and its period before reading the final case; defer if no first-party commercial-relationship evidence exists.',
'E02 links enforcement to public funding. This traces a buyer-to-facility commercial relationship without claiming a public award or a false issuer statement.', ['E14'],[4,1,2,4],'OSH API has credential/commercial access burden; no paid API used. Public document availability must be verified.')
add('X11','A synthesis treating overlapping participants as independent evidence',[248,250],[249],
'IF a review or meta-analysis treats two papers as independent study populations, and explicit trial references suggest their enrolled cohorts may overlap.',
'THEN reconstruct cohorts, arms, recruitment intervals and outcomes from registry history and full papers, and determine whether the synthesis double-counts the same participants for the same comparison.',
'Inflated independent evidence can alter treatment or policy conclusions. Multiple papers from one trial are ordinary and not misconduct when handled correctly.',
'DOI references → explicit NCT/protocol IDs → cohort/arm/recruitment overlap → synthesis study rows. One NCT is not automatically one identical participant set.',
'Matched trial versions and actual synthesis analysis; repeated follow-up, platform trials and subgroup populations need explicit handling.',
['Disjoint cohorts or arms','Synthesis combines dependence correctly','Different outcomes/timepoints validly analyzed','Secondary analysis clearly separated','Registry ID entered incorrectly'],
['Full synthesis methods and included-study table','Both primary papers','Trial history and cohort/arm details','Reproducible participant/effect mapping'],
'Read the synthesis’s exact inclusion rows and the papers’ cohort descriptions before counting shared trial IDs as duplicate evidence.',
'H02 compares prespecified outcomes and P01 checks retractions. This tests independence of the evidence units used in a synthesis.', ['E15'],[5,2,3,3],'Registry and DOI metadata routes documented earlier; full texts/cohort records and synthesis calculation not tested.')
add('X12','Attributed mineral assay versus its original sample measurement',[312,288],[],
'IF a filed technical report attributes a precise assay value to a named Quebec government sample and analytical method.',
'THEN compare the original measurement and any reanalysis to the attributed value, preserving sample matrix, element, method, units and censoring.',
'A materially altered or misattributed input can affect a project valuation or public financing claim. A different assay method or unit is not a contradiction.',
'Sample ID plus survey, matrix, element and method/version—not just coordinates or project name. Confirm identity in original certificate/record before numerical comparison.',
'Quebec source samples; original and reanalysis dates, report version and cited reference. Do not compare sediment, rock and drill-core values as equivalents.',
['Unit conversion','Detection-limit notation','Later valid reanalysis','Different matrix/method','OCR/transcription in the catalog','Cited sample identifier is incomplete'],
['Exact technical-report attribution','Original government/laboratory record','Method, units and detection limits','Reanalysis and amendment history'],
'Choose one explicit sample attribution and verify the original row or certificate. Do not download provincial bulk files merely to look for anomalies.',
'N09 compares production to a provincial total. This verifies a specifically attributed underlying measurement, not a resource/reserve inference.', ['E16'],[4,2,3,2],'Official rock/sediment coverage and access paths documented; sample-level record and filed report not retrieved.')
add('X13','Voluntary deregistration despite a contemporaneous property interest',[47,7],[],
'IF an Australian company is confirmed to have used voluntary deregistration, and contemporaneous title evidence identifies a valuable English/Welsh property interest held by that same legal entity.',
'THEN establish the company’s beneficial/economic interest and valuation at the application date against the applicable voluntary-deregistration asset condition, distinguishing other deregistration routes.',
'Current ASIC guidance separately requires assets below A$1,000 and no outstanding liabilities for voluntary deregistration. Subtracting a mortgage is not automatically a valid asset-condition test; establish the applicable valuation treatment and test liabilities separately. A verified contradictory asset position warrants scrutiny; a stale title entry is not proof of an invalid application.',
'Exact Australian ACN as recorded/verified for the overseas proprietor → ASIC company and deregistration method → title and interest history. ABN, name similarity and registration dates are not substitutes.',
'Australian corporate process and England/Wales property; application-date assets and historical rule version, not today’s company status or property asking price.',
['ASIC-initiated deregistration','Prior disposal with land-register lag','Trustee/nominee rather than economic asset','Different legally established asset interest/valuation; a mortgage is not an automatic offset','Reinstatement or incorrect company identifier'],
['Deregistration application/method and date','Contemporaneous title/transfer record','Nature and value of company interest','Separate outstanding-liabilities evidence; no automatic net-equity substitution','Applicable historical rule'],
'First confirm the deregistration was voluntary. Then check exact ACN and historical interest; stop before paid title or ASIC documents without an authorized free route.',
'F04 asks whether a supplier existed; S03 traces sanctioned assets. This tests the factual asset condition of a specified deregistration process.', ['E17','E18'],[5,2,3,4],'HMLR account gate documented; historical title/ASIC records may cost. No account or paid record requested.')
add('X14','Conflicting copies of the same audited consolidated accounts',[5,6],[],
'IF the same issuer files the same audited consolidated accounts for the same year and accounting basis in EDGAR and EDINET.',
'THEN reconcile the original financial-statement versions and audit reports for a material unresolved difference in a specified cash/debt/related-party figure or opinion.',
'Different regulator-facing versions of supposedly identical accounts can affect investors. Parallel filings commonly differ legitimately in translation, units, local reporting scope or amendment timing.',
'Verified issuer CIK↔EDINET code crosswalk → exact document/form and consolidated group → period, accounting basis, units and original audited version. IDs are not a shared namespace.',
'Same issuer/year/basis and version across US/Japan filings; distinguish annual audited accounts from quarterly or local parent-only statements.',
['Different GAAP or consolidation','Currency/unit scaling','Subsequent amendment','Translation or taxonomy mapping','Different auditor opinion scope'],
['Original audited statements and opinions on both sides','Issuer crosswalk','Amendment history','Basis/consolidation/units mapping'],
'Confirm that two documents purport to contain the same audited accounts before extracting numbers; compare original statement pages before trusting XBRL labels.',
'Related to N06 same-document/version comparison, but tests issuer-account consistency for the same audited statement across regulators rather than agency redaction versions. E09 instead reconciles government funding to issuer accounts.', ['E19','E20'],[5,1,2,3],'SEC route documented; EDINET API version guides available, but auth/language/record access and issuer crosswalk remain unverified.')
# Explicitly separate useful refinements from new-mechanism totals.
add('REF-H01','NIH trial results submission under the applicable award policy',[246,248],[],
'IF an exact NIH award funds a trial covered by the relevant results-submission policy and the actual primary-completion and award dates are established.',
'THEN reconstruct the applicable deadline, exceptions/extensions and actual submission history before assessing whether required results were late or missing.',
'Potential failure to disseminate publicly funded research; absence of posted results is not proof of no timely submission.',
'Explicit award-to-NCT link, not institution/PI similarity; distinguish submission, quality-control review and public posting.',
'Applicable award policy effective dates and BESH flexibilities, including the 2025 notice; infrastructure-only support is not automatically in scope.',
['Timely submission awaiting review','Extension/exception','BESH flexibility','Wrong grant or trial completion date','Infrastructure support only'],
['Award/eligibility facts','Policy version and exception review','Actual submission history','Deadline calculation'],
'Check whether the trial is within the policy before calculating dates; never use the public posting date as a substitute for submission.',
'Refinement of H01, not counted as a new mechanism or an extra independent source pairing.', ['E21','E22'],[5,2,2,3],'Policy documentation read; no award/trial compliance case evaluated.',kind='existing_mechanism_refinement')
add('REF-D01','Covered federal asset after its applicable vulnerability deadline',[148,149],[150],
'IF a permitted existing passive observation identifies a specific product/version on an independently verified covered federal civilian asset after the applicable remediation deadline for its exact CVE.',
'THEN verify current directive scope, asset responsibility and actual remediation/mitigation before reporting a potentially missed requirement.',
'Potentially overdue protection of a public service; a version banner alone does not establish vulnerability or noncompliance.',
'Historical host attribution and observed product/version → NVD affected-version logic → exact KEV CVE and applicable dated directive. Domain/ASN ownership alone is insufficient.',
'Actual FCEB scope and event-date directive, including later changes; no universal deadline is assumed and no active probes are authorized.',
['Stale or spoofed banner','Backported patch','Approved mitigation or decommissioned route','Wrong agency attribution','Different applicable directive/deadline'],
['Permitted historical passive observation','Agency asset attribution','Version/patch/mitigation evidence','Current and event-date authoritative deadline'],
'Confirm allowed historical access and operative directive first; defer if either is unavailable. Do not scan, exploit or publish endpoint details.',
'Refinement of D01 and prior Censys source review; not counted as a genuinely new mechanism.', ['E23'],[5,1,2,4],'A referenced CISA alert failed to open; current/event-date scope unresolved. Passive historical access likely credentialed; no observations acquired.',kind='existing_mechanism_refinement')
strength={'X01':'explicit disclosure versus verified relationship; policy applicability conditional','X02':'fixed contractual obligation; operative case contract not yet verified','X03':'process/authorization compatibility; no illegality inference from absence','X04':'cross-regime declaration consistency; thresholds and scope must be verified','X05':'activity declaration consistency; tax/LDA definitions must align','X06':'documented financing relationship; no breach claim','X07':'explicit authorization sequence; operative case condition required','X08':'specific security requirement; not a generic liability/security comparison','X09':'specific title assertion versus authoritative historical status','X10':'documented commercial relationship and final finding; association not liability','X11':'statistical independence of participants; duplicate publication not itself a breach','X12':'exact measurement attribution; unit/method identity required','X13':'current general legal eligibility condition verified; case/historical applicability unverified','X14':'identical-account consistency; accounting bases must match','REF-H01':'existing obligation-based refinement; eligibility and exceptions unresolved','REF-D01':'existing deadline refinement; current/event-date authority unverified'}
for r in C:
 if r['test_id']=='X01':
  r['kind']='existing_mechanism_refinement'
  r['novelty_vs_baseline']='Independent review correction: H04 already calls for published conflict declarations and payment taxonomy (journalists-guide section 14). This sharpens direct general-payment attribution and policy window; it is not a new mechanism.'
 if r['test_id']=='X10':
  r['kind']='existing_mechanism_refinement'
  r['novelty_vs_baseline']='Independent review: commercial-sourcing specialization of E02. No distinct obligation, contradiction or causal test; retained as useful refinement.'
 r['expectation_strength']=strength[r['test_id']]
 r['source_manifest']=[dict(sys_id=S[n]['sys_id'],name=S[n]['name'],explicit_catalog_fields=S[n]['join_fields'],file=S[n]['file'],line_start=S[n]['line_start'],block_sha256=S[n]['block_sha256']) for n in dict.fromkeys(r['primary_source_ids']+r['supporting_catalog_source_ids'])]
 r['semantic_key']=hashlib.sha256((r['title']+'|'+r['novelty_vs_baseline']).encode()).hexdigest()[:20]
 r['triage_score']=10*r['consequence_score']+3*r['feasibility_score']+2*r['join_route_score']-2*r['burden_tier']
for rank,r in enumerate(sorted(C,key=lambda x:(-x['consequence_score'],x['test_id'])),1):r['importance_rank']=rank
for rank,r in enumerate(sorted(C,key=lambda x:(-x['feasibility_score'],x['burden_tier'],-x['join_route_score'],x['test_id'])),1):r['feasibility_rank']=rank
for rank,r in enumerate(sorted(C,key=lambda x:(-x['triage_score'],x['test_id'])),1):r['triage_rank']=rank
C.sort(key=lambda r:r['triage_rank'])
(P/'new-formulations.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in C))
with (P/'new-formulations.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=C[0]);w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in C)
print('New mechanisms',sum(r['kind']=='new_mechanism' for r in C),'separate refinements',sum(r['kind']!='new_mechanism' for r in C))
