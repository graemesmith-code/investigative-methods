# Authored audit code; requires local private source texts, not included for publication.
from pathlib import Path
import json,csv,re,collections,hashlib
P=Path(__file__).resolve().parent;W=P/'private'
def dump(n,rs):
 (P/(n+'.json')).write_text(json.dumps(rs,indent=2,ensure_ascii=False)+'\n')
 ks=list(dict.fromkeys(k for r in rs for k in r))
 with (P/(n+'.csv')).open('w',newline='') as f:
  w=csv.DictWriter(f,ks);w.writeheader();w.writerows([{k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()} for r in rs])
rs=json.loads((P/'reference-occurrences.json').read_text())
# Human reviewer read all 71 human/civilian/kinetic/final-determination contexts.
reviewed=[]
for r in rs:
 if not re.search('human|civilian|Kinetic|final determinations',r['short_original_extract'],re.I):continue
 id=r['document_id'];pn=r['pdf_page'];term=r['short_original_extract'].lower()
 classification='plausible_indirect';note=''
 if term.startswith('civilian'):
  if (id=='D09-02-dc-opinion' and pn==19) or (id=='D09-13-rehearing-petition' and pn==48):
   classification='clear_substantive_concept';note='Court recounts company concern about catastrophic AI error endangering soldiers and civilians; not an adjudicated IHL violation.'
  elif id=='D09-03-kaplan-initial' and pn==11:
   classification='clear_substantive_concept';note='Sworn company account of misidentification and risk to innocent civilians, offered as reason to refuse lethal-autonomy permission; not a court holding.'
  elif id=='D09-12-appendix-vol4' and pn==128:
   classification='clear_substantive_concept';note='Adversarial government declaration claims vendor-imposed limits could endanger personnel and civilians; allegation supporting exclusion, not proven harm.'
  else:
   classification='rejected_false_positive';note='Civilian denotes agency, customer, official or constitutional civilian control rather than protected non-combatants; retained to show contextual rejection.'
 elif id=='D09-03-kaplan-initial' and pn in [5,6] or id=='D09-05-technical-declaration' and pn==7:
  classification='generic_legal_ethical';note='Human review/judgment describes reinforcement-learning feedback during model training; not human authorization of a weapon engagement.'
 elif id=='D09-03-kaplan-initial' and pn==10:
  classification='clear_substantive_concept';note='Kaplan defines the refused lethal-autonomy use as weapons operation without human review, approval or override; sworn company account of negotiating boundary.'
 elif id=='D09-12-appendix-vol4' and pn==9:
  note='Media article reproduced in appendix; reported human-oversight dispute, not a sworn fact or contractual instrument.'
 elif id=='D09-12-appendix-vol4' and pn==108:
  classification='generic_legal_ethical';note='Attached usage-policy exception for locating missing persons is conditioned on liberties/human rights; not automatically a military IHL duty.'
 elif id=='D09-12-appendix-vol4' and pn==112:
  note='Attached high-risk-domain policy requires qualified-professional review for listed advice/decision uses, but only encourages review for other content; government rider modifications may alter applicability.'
 elif id=='D09-12-appendix-vol4' and pn==113:
  classification='clear_substantive_concept';note='Signed RUA §2: final target determinations/direct tracking of kinetic action prohibited, but intelligence collection allows human OR machine oversight; RUA §1 broadly permits defence support. Historical August2025 agreement only.'
 elif id=='D09-12-appendix-vol4' and pn==125:
  note='Government declarant characterizes usage terms as restricting battlefield/missile-defence activity; adversarial interpretation, not substitute for exact signed RUA.'
 elif id=='D11-01-ndia-2024' and pn==2:
  note='NDIA asks DoD to clarify high-risk use cases requiring a responsible human and risk-based safeguards; proposal, not implemented contract.'
 elif id=='D11-01-ndia-2024' and pn==12:
  classification='explicit_ihl';note='NDIA proposes human over-the-loop governance of AI weapon behaviour to comply with humanitarian law. This is trade-association advocacy, not a corporate/customer legal obligation.'
 elif id=='D11-05-ndia-april' and pn==7:
  classification='generic_legal_ethical';note='Human review is restricted for privacy/eyes-off handling of government data; not the human oversight of lethal decisions.'
 elif id=='D11-05-ndia-april' and pn==10:
  note='NDIA argues mandatory decision documentation, human-oversight mechanisms and incident reporting create overhead; requests harmonization rather than proving adopted waiver.'
 elif id=='D11-07-gsar-deviation' and pn in [145,147]:
  note='Final class-deviation LLM clause requires commercially reasonable/available means for government oversight, intervention and traceability, bounded by contracted use case and feasibility; incorporation into specific contract unresolved.'
 elif id=='D11-08-gsar-june-proposal' and pn in [24,26]:
  note='Proposed LLM clause gives government oversight/intervention/traceability means; proposal must not be confused with later class-deviation wording.'
 if not note:note=r['context_summary']
 r.update(classification=classification,context_summary=note,confidence='high contextual classification; no broader applicability inferred',review_status='manual contextual review of human-control/civilian-protection candidate')
 if id=='D09-12-appendix-vol4':r['linked_instrument']='D-V01: July10 master terms (unreviewed) → signed August USG addendum + attached AUP → controlling RUA; January2026 successor unresolved'
 if id.startswith('D11') and id!='D11-01-ndia-2024':r['linked_instrument']='D-V02: draft → April comments → June proposal → August comments → September class deviation; not automatic incorporation'
 reviewed.append({'occurrence_id':r['occurrence_id'],'classification':classification,'context_summary':note})
# Explicit semantic additions after non-hit and full-page reading; preserve lexical count separately.
semantic=[('D09-01-district-opinion',1,'backdoor access','plausible_indirect','Court says post-delivery access premise was abandoned; technical-enforcement contrary evidence, not a direct IHL rule.'),('D09-01-district-opinion',31,'usage policy','plausible_indirect','Court discusses government distrust caused by vendor use limits and speech; constitutional contract dispute, not IHL merits.'),('D09-07-final-relief',3,'in accordance with law','generic_legal_ethical','APA vacatur concerns statutory authorization of procurement sanctions, not an IHL review.'),('D10-05-cofc-2023',24,'Hazardous Material Management','generic_legal_ethical','Footnote distinguishes hazardous-material proposal rating from personnel qualification defect; no autonomy or IHL safety violation established.'),('D11-01-ndia-2024',12,'human','clear_substantive_concept','NDIA uses quoted over-the-loop formulation missed by simple human-in/on-the-loop pattern; proposed oversight to ensure humanitarian-law compliance.')]
for i,(id,pn,extract,cat,note) in enumerate(semantic,1):
 base=next(r for r in rs if r['document_id']==id).copy();base.update(occurrence_id=f'{id}:p{pn}:semantic{i}',pdf_page=pn,page_character_offset='',clause_locator='PDF page '+str(pn),short_original_extract=extract,classification=cat,confidence='high: manual page review',search_reason='semantic recall test; not lexical hit',context_summary=note,nearby_reference_terms='',review_status='manual semantic addition',source_url=base['source_url'].split('#')[0]+'#page='+str(pn),context_sha256='',dedup_text_key=hashlib.sha256((id+str(pn)+extract).encode()).hexdigest());rs.append(base)
dump('reference-occurrences',rs);dump('human-control-context-review',reviewed)
summary=json.loads((P/'coverage-summary.json').read_text());summary.update(lexical_occurrences=len(rs)-len(semantic),manual_semantic_additions=len(semantic),retained_occurrence_rows=len(rs),manual_context_review_count=len(reviewed),manual_reviewed_occurrence_rows=sum(r['review_status']!='retained machine candidate; not individually adjudicated' for r in rs),promoted_candidates=9,classification_counts=dict(collections.Counter(r['classification'] for r in rs)),count_warning='Lexical matches, retained occurrences, reviewed passages and promoted findings are different denominators; none is a count of actual safeguards.')
(P/'coverage-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
samples=[]
for f,method in [('nonhit-sample-selection.json','First non-hit page with >120 characters in first eight eligible source IDs; front matter bias disclosed'),('nonhit-body-sample-selection.json','Longest non-hit page after PDF2 with >500 characters in eight selected litigation/protest/GSAR documents')]:
 for r in json.loads((W/f).read_text()):
  r.update(selection_method=method,review_result='No previously unrecorded explicit IHL phrase found; generic/indirect missed concepts added where noted',added_semantic_rows=[x[2] for x in semantic if x[0]==r['document_id'] and x[1]==r['pdf_page']]);samples.append(r)
dump('nonhit-review-sample',samples)
# Replace condensed candidate descriptions with complete auditable fields.
cs=json.loads((P/'candidate-register.json').read_text())
extra={
'D-C01':('Anthropic PBC; Palantir Technologies Inc.','Anthropic Offerings via Anthropic, AWS Bedrock/Sagemaker, Google Vertex; August2025 government rider','Palantir as customer; July10,2025 master Terms referenced; USG end users','Ryan Taylor, Palantir CRO/CLO; Thiyagu Ramasamy, Anthropic Head of Public Sector (signatories)','Use for final targeting/kinetic tracking or intelligence collection decisions','Broad permitted defence uses; intelligence decisions may have human OR machine oversight; mutual/legal amendment of RUA; master remedies unreviewed','Executed historical boundary; no identified stopped deployment','New actual-contract detail relative to F4/F5; no exclusivity claim','January2026 executed successor; master terms/remedies; deployment-level enforcement'),
'D-C02':('Anthropic PBC','Claude/Claude Gov in described classified partner deployments; versions not fully specified','Existing partner agreements and proposed GenAI.mil renegotiation are separate','Company decision-makers described by Kaplan/Ramasamy; no personal legal-veto attribution','Government demand for blanket all-lawful-uses permission','Most restrictions negotiable; two described exceptions; no post-delivery vendor intervention according to testimony','Refusal documented; procurement exclusion followed, causation/legal basis contested','Sworn technical-enforcement detail extends known dispute','Independent technical verification and complete applicable contract chain'),
'D-C03':('Anthropic PBC; US Department of War and named officials/agencies','Claude procurement; not a particular weapon','District and appellate statutory proceedings, not one contract','Judge Rita Lin; D.C. Circuit majority Katsas/Rao and dissent Henderson','Supply-chain designations and broad directives challenged','District relief excludes certain defendants/claims and permits lawful purchasing choice; mandate withholding not procurement stay','Distinct judicial relief and petition denial; panel rehearing response ordered','F4 baseline corroborated and updated with underlying filings','Complete latest dockets and any later appellate/stay order'),
'D-C04':('National Defense Industrial Association (trade association)','AI for defence and government LLM procurement; not one model release','2024 DoD RFI and 2026 GSA clause consultations','NDIA institutional submission; no named corporate release approver established','Risk, use restrictions, liability and notice obligations in procurement','Risk-based human involvement; mandatory law/security versus discretionary limits; broad defence permissions sought','Proposals submitted; individual proposal adoption not established','New document detail in this audit; publicly available advocacy','Member implementation; final clause incorporation; causal attribution'),
'D-C05':('Mistral Inc., Bethesda; AeroVironment awardee (decision uses LLC/Inc. in different places)','Loitering munitions procurement; no precise autonomous configuration established','Army W91CRB24D0011; GAO B-422905/B-422905.2','Army contracting officials; GAO decision','Sole-source procurement challenged','Statutory public-interest presumption; urgent/compelling CICA override is procedural','Protest denied; no weapons-test failure adjudicated','Adjacent control example, not scoop','Exact awardee entity suffix; any underlying safety certifications'),
'D-C06':('Anduril Industries Inc.','ABMS secure-processing/connectivity task-order scope','Air Force; GAO B-419420','Air Force officials and GAO','Competition and task-order scope challenge','Jurisdiction limits and solicitation scope','Denied claims; not an autonomous-system safety veto','Adjacent procurement example','Any separate operational safeguard record'),
'D-C07':('Anduril Industries Inc.','Solicitation70RDA226R00000001; technical scope not established here','GAO B-424504.2','GAO docket; reason/decision-maker not obtained','Bid protest filed August12,2026','Dismissal reasons unknown','Dismissed September4,2026; no defect finding inferred','New docket lead only','Public dismissal rationale and corrective-action documents'),
'D-C08':('System Dynamics International Inc.; Strata-G Solutions LLC','Soldier Unmanned Aircraft Systems design/engineering support; Group I reconnaissance','Army RFP W58RGZ-22-R-0073; COFC23-431','Judge Kathryn C. Davis; Army evaluation officials','Failure to evaluate minimum personnel education according to solicitation','Discretion over other weaknesses does not cure identified material deficiency','Award performance enjoined; not a failed autonomous-targeting test','Documented procurement gate; not novel IHL control','Subsequent award/remedy and any system-specific normative gate'),
'D-C09':('Seventeen former national-security officials as amici','Military AI and lethal-autonomy negotiating restrictions; no named weapon','D.C. Circuit26-1049/26-1162 panel rehearing','Amici and counsel including Harold Hongju Koh, Bruce Swartz, Alexis Loeb','Challenge to designation process and treatment of corporate guardrails','Political Declaration commitment invoked; no argument establishes every autonomous use unlawful','Amicus filed; not judicial adoption','Underlying amicus detail beyond F4 procedural posture','Court response to argument and full current docket')}
keys=['legal_entity','product_version','customer_contract','decision_maker','trigger','exceptions_override','consequence','novelty','remaining_gap']
for c in cs:
 c.update(dict(zip(keys,extra[c['candidate_id']])))
 c['scope']=c['customer_contract'];c['established']=c['consequence'];c['contrary_and_uncertainty']=c['exceptions_override']+'; '+c['remaining_gap'];c['date_version']=re.sub(r'(?<=[A-Za-z])(?=\d)|(?<=\d)(?=[A-Za-z])',' ',c['date_version'])
dump('candidate-register',cs)
chains=[{'chain_id':'D-V01','subject':'Anthropic–Palantir actual government agreement','sequence':[{'date':'June2024','instrument':'Government addendum described in Ramasamy declaration','access':'Signed text not obtained'},{'date':'July10,2025','instrument':'Master Commercial Terms referenced by signed August agreement','access':'Master text not obtained'},{'date':'August15–16,2025','instrument':'USG Addendum, attached Usage Policy and RUA signed by Palantir/Anthropic','access':'Public appellate appendix App391–407; text and signatures reviewed','priority':'RUA controls conflict with USG policy; USG addendum changes attached policy; master remedies unresolved'},{'date':'January2026','instrument':'Expanded government permissions described in June declaration','access':'Executed successor and exact supersession not established'}],'boundary':'Do not merge with separate direct CDAO agreement, proposed GenAI.mil change, or public AIP terms effectiveOctober5,2026.'},{'chain_id':'D-V02','subject':'GSAR AI clause consultation/adoption chain','sequence':['March2026 draft','April3 NDIA comments','June17 revised proposal2026-12205','August3 NDIA comments','September28 class-deviation revision; relevant LLM provisions effectiveOctober19'],'boundary':'Final wording and actual contract incorporation assessed separately in licence lane; no commenter-specific causal claim.'},{'chain_id':'D-V03','subject':'Anthropic litigation status chain','sequence':['August27 district opinion250, final relief251 and judgment252','September25 D.C. Circuit opinion2194984, judgment and mandate-withholding order2194986','October13 panel-rehearing petition2197902','October15 response order2198350','October20 national-security-officials amicus'],'boundary':'Different statutes/courts; no verified complete latest docket and no assumed reversal or blanket procurement stay.'}]
(P/'version-incorporation-chains.json').write_text(json.dumps(chains,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,indent=2))
