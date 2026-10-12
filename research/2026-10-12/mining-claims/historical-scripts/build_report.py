from pathlib import Path
import sys, json, csv, shutil, hashlib, zipfile, html, datetime
from decimal import Decimal
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from candidates_data import CANDIDATES

ROOT=Path(__file__).resolve().parent.parent
RAW=ROOT/'research/raw'; OUT=ROOT/'output'; KIT=OUT/'starter-kit'
KIT.mkdir(parents=True, exist_ok=True); (KIT/'sources').mkdir(exist_ok=True)
log=[json.loads(s) for s in (ROOT/'research/access-log.jsonl').read_text().splitlines()]
byid={x['id']:x for x in log if x.get('status')==200}
extra=['canada-estma.csv','sec-submissions-fcx.json','rio-submissions.json','sec-master-q12024.gz',
       'uk-rio-reports.json','uk-extractives-2024.json','uk-extractives-developer.html','uk-extractives-endpoints.html',
       'eiti-country-api.json','eiti-senegal-api.json','eiti-revenue-sample.json','congo-summary-2023.xlsx',
       'mali-annexes-2024.xlsx','mauritania-2024.pdf']
ids=list(dict.fromkeys([n for x in CANDIDATES for n in x['western']+x['host']]+extra))
included={'canada-estma.csv','brazil-dams.csv','uk-rio-2023.json','uk-rio-reports.json','uk-extractives-2024.json',
          'sec-submissions-fcx.json','rio-submissions.json','sec-master-q12024.gz',
          'eiti-country-api.json','eiti-senegal-api.json','eiti-revenue-sample.json'}
for prior in (KIT/'sources').iterdir():
    if prior.is_file(): prior.unlink()
manifest=[]
for name in ids:
    r=byid[name]
    src=RAW/name
    assert hashlib.sha256(src.read_bytes()).hexdigest()==r['sha256']
    destname=name
    if name.endswith('.bin'):
        destname=name[:-4]+'.xlsx'
    dest=KIT/'sources'/destname
    if name in included: shutil.copyfile(src,dest)
    manifest.append({k:r[k] for k in ['id','url','final_url','tested_at_utc','status','content_type','bytes','sha256']})
    manifest[-1]['download_filename']=destname
    manifest[-1]['archive_path']=('sources/'+destname) if name in included else None
embedded='burkina-embedded-Microsoft_Excel_Worksheet3.xlsx'
embedded_hash=hashlib.sha256((RAW/embedded).read_bytes()).hexdigest()
(KIT/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(KIT/'candidates.json').write_text(json.dumps({'as_of':'2026-10-12','status':'Source-tested opportunities, not proven contradictions',
    'candidates':CANDIDATES,'embedded_specimen':{'sha256':embedded_hash,
      'container':'burkina-annexes.bin','zip_path':'xl/embeddings/Microsoft_Excel_Worksheet3.xlsx',
      'provenance':'Annexe 10 row 9; sheet11 relationship rId10; anchor row 8 zero-based'}},ensure_ascii=False,indent=2))
cleanlog=[{k:v for k,v in x.items() if k not in ['links','prefix','local_path']} for x in log]
(KIT/'access-log.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in cleanlog))

glossary=[
 {'language':'French','source':'Paiements Entreprises / Societes','meaning':'Company-declared payments','caution':'Distinguish initial, adjustments and final.'},
 {'language':'French','source':'Paiements Regies / Gouvernement','meaning':'Government-side amounts','caution':'Not a second company statement.'},
 {'language':'French','source':'Ristourne miniere','meaning':'Local share of a mining royalty in the Madagascar specimen','caution':'Do not automatically translate as a refund or discount.'},
 {'language':'French','source':'Taxe ad valorem / ISCP','meaning':'Distinct payment streams in Mali','caution':'A regulatory category crosswalk is required before summing into ESTMA royalties.'},
 {'language':'Portuguese','source':'Alteamento a jusante','meaning':'Downstream raising','caution':'Match the same dam and construction stage.'},
 {'language':'Portuguese','source':'Alteamento por linha de centro','meaning':'Centreline raising','caution':'Modified centreline may be a subtype, not an incompatible category.'},
 {'language':'Portuguese','source':'Dano Potencial Associado','meaning':'Potential consequence classification','caution':'Different from failure probability or the risk category.'},
 {'language':'Spanish','source':'TMF','meaning':'Fine metric tonnes','caution':'Do not compare with gross concentrate weight.'},
 {'language':'Spanish','source':'Produccion empresas','meaning':'Production by company','caution':'May aggregate several mines.'},
]
(KIT/'glossary.json').write_text(json.dumps(glossary,ensure_ascii=False,indent=2))
sys.path.insert(0,str(KIT));from compare_claims import GATES,compare
allg={x:True for x in GATES}
controls={'description':'Curated demonstration inputs. Gate values are for exercising the kernel; the PDF governs investigative readiness.', 'pairs':[
 {'id':'PERU-MOLYBDENUM-2024-CONTROL','gates':allg,
  'western':{'kind':'interval','unit':'metric_tonnes_fine_molybdenum','low':'13385.51083870','high':'13386.41802344'},
  'host':{'kind':'interval','unit':'metric_tonnes_fine_molybdenum','low':'13386.3420761','high':'13386.3420761'},
  'expected':'COMPATIBLE_WITH_PRECISION','note':'29,511 thousand lb, with +/-1 thousand lb combined rounding; this does not prove the statements true.'},
 {'id':'ITY-ROYALTY-FX-ARITHMETIC-CONTROL','gates':allg,
  'western':{'kind':'interval','unit':'USD','low':'45145202.5','high':'45145203.5'},
  'host':{'kind':'interval','unit':'USD','low':'43345763.2293','high':'45941910.4664'},
  'expected':'COMPATIBLE_WITH_PRECISION','note':'Conditional on the approved SMI/SMD/SMF basket. Do not infer source truth from overlap.'},
 {'id':'MALI-DIVIDEND-DEFINITION-GATE','gates':{**allg,'same_fact_definition':False,'same_scope':False},
  'western':{'kind':'interval','unit':'USD','low':'59055000','high':'59065000'},
  'host':{'kind':'interval','unit':'USD','low':'51211306.3271','high':'55070792.9548'},
  'expected':'REVIEW_REQUIRED','note':'Non-overlapping arithmetic is not a verdict while gross/net and entitlement definitions are unresolved.'},
 {'id':'SYNTHETIC-NO-REAL-COMPANY-EXAMPLE','gates':allg,
  'western':{'kind':'interval','unit':'same_unit','low':'100','high':'101'},
  'host':{'kind':'interval','unit':'same_unit','low':'103','high':'104'},
  'expected':'INCOMPATIBLE_CLAIMS','note':'Invented values solely to verify the incompatible branch.'},
]}
(KIT/'controls.json').write_text(json.dumps(controls,ensure_ascii=False,indent=2))
results=[compare(x) for x in controls['pairs']]
assert all(x['status']==y['expected'] for x,y in zip(results,controls['pairs']))
(KIT/'control-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))

pdfmetrics.registerFont(TTFont('DV','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
navy=colors.HexColor('#152D3F');teal=colors.HexColor('#087F83');muted=colors.HexColor('#566774');pale=colors.HexColor('#EDF5F5')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyD',fontName='DV',fontSize=9.3,leading=13.2,spaceAfter=7,textColor=navy))
styles.add(ParagraphStyle(name='SmallD',fontName='DV',fontSize=7.4,leading=10.1,spaceAfter=4,textColor=muted))
styles.add(ParagraphStyle(name='TitleD',fontName='DVB',fontSize=27,leading=32,spaceAfter=14,textColor=navy))
styles.add(ParagraphStyle(name='H1D',fontName='DVB',fontSize=20,leading=25,spaceAfter=14,textColor=navy))
styles.add(ParagraphStyle(name='H2D',fontName='DVB',fontSize=10,leading=14,spaceBefore=6,spaceAfter=4,textColor=teal))
styles.add(ParagraphStyle(name='TableD',fontName='DV',fontSize=8.1,leading=11,textColor=navy))
styles.add(ParagraphStyle(name='KickerD',fontName='DVB',fontSize=9,leading=13,spaceAfter=8,textColor=teal))
story=[]
def p(s,style='BodyD'):
    return Paragraph(s,styles[style])
def add(s,style='BodyD'):story.append(p(s,style))
def esc(s):return html.escape(str(s))
def head(s):add(esc(s),'H2D')
def url(label,href):return f'<link href="{html.escape(href,quote=True)}" color="#087F83"><u>{esc(label)}</u></link>'
def table(data,widths,header=True):
    cells=[[p(esc(v),'TableD') for v in row] for row in data]
    t=Table(cells,colWidths=widths,repeatRows=1 if header else 0,hAlign='LEFT')
    st=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,0),.8,teal),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F4F7F8')])]
    if header:st += [('BACKGROUND',(0,0),(-1,0),pale)]
    t.setStyle(TableStyle(st));story.append(t)
def newpage():story.append(PageBreak())

add('RABBIT / INVESTIGATIVE RESEARCH / 12 OCTOBER 2026','KickerD')
add('One project.\nTwo governments.\nOne set of facts.'.replace('\n','<br/>'),'TitleD')
add('<b>Ten evidence-tested mining-project pairings</b> for detecting company statements that cannot both be true.')
add('The source hunt succeeded: both sides of all ten candidates were retrieved, opened and matched to the named company or project. These are immediately usable investigative starting points, not ten proven false statements. Several have consistent control values; others need a specific definition or scope question resolved before automated verdicts.')
add(f'<b>{len(CANDIDATES)} pairings</b> across <b>10 host jurisdictions</b> · <b>{len(log)} direct access tests</b>, {sum(x.get("status")==200 for x in log)} HTTP 200 responses · <b>3 Western access systems</b> tested.','KickerD')
data=[['Rank','Project / host country','First fact to compare']]
for c in CANDIDATES:data.append([str(c['rank']),c['project']+' / '+c['country'],c['topic'].split(';')[0]])
table(data,[40,257,190])
add('Priority reflects a mixture of clean logic, public importance and accessible evidence, not a forecast of wrongdoing. Start the extraction pilot with Peru molybdenum, Brazil dam attributes and Ity royalties.','SmallD')
newpage()

add('The free access routes that actually worked','H1D')
head('United States: SEC submissions API + bulk filing index')
add('A real submissions JSON response was fetched for Freeport and Rio Tinto, plus SEC-hosted 10-K, AIF and technical-report exhibits. The Q1 2024 master.gz bulk index downloaded successfully (4.49 MB). The index identifies filings; project claims still require extracting the underlying HTML/PDF. Companyfacts is not a substitute for those narrative tables.')
add(url('SEC API sample',byid['sec-submissions-fcx.json']['url'])+' · '+url('Bulk quarterly index',byid['sec-master-q12024.gz']['url']),'SmallD')
head('Canada: government bulk ESTMA index + original returns')
add('Statistics Canada\'s CSV downloaded in full: 53.26 MB and 114,594 records. It includes entity, payee/project, payment category, reporting-period dates and the original-report link. The sample has year labels 2021-2026; that does not imply complete coverage for every company or year. Use the actual start/end dates. Values are converted to CAD and parent data may also appear for subsidiaries; do not sum duplicated group rows.')
add(url('Download the tested Canada CSV',byid['canada-estma.csv']['url'])+' · Original B2Gold, Barrick, Endeavour and Galiano returns were independently downloaded and inspected.','SmallD')
head('United Kingdom: Companies House extractives JSON')
add('The unauthenticated all-company 2024 endpoint returned 52 reports. Rio Tinto\'s company endpoint returned reporting years 2015-2025, including multiple historical versions. A direct 2023 endpoint returned QMM\'s project royalty. Inspect reportEndDate and version in the response; never infer the period solely from a URL or filing date.')
add(url('Bulk 2024 JSON',byid['uk-extractives-2024.json']['url'])+' · '+url('Rio all years and versions',byid['uk-rio-reports.json']['url'])+' · '+url('API documentation',byid['uk-extractives-endpoints.html']['url']),'SmallD')
head('Host jurisdictions: prefer national annexes to summary APIs')
add('Brazil provides a full operator-level dam CSV; Peru a company-production XLSX. Burkina Faso, DRC, Cote d\'Ivoire, Senegal and Mali supply national Excel annexes. Ghana, Zambia and Madagascar provide downloadable reconciliation PDFs containing named company declarations. These are bulk document downloads, not necessarily query APIs.')
add('The EITI API itself returned country metadata, Senegal summary data and an individual revenue record. But an API field labelled "company" can mean government revenue broken down by company: the inspected DRC summary template explicitly instructs use of government figures. It cannot automatically serve as the second company declaration.')
head('What counts as a government representation here')
add('Eight host-side pairings use returns to national, state-led EITI processes, often compiled by independent administrators. They expose company assertions to the national reporting process. They are not all proven to be legally compulsory regulatory filings. Brazil and Peru are the strictest direct-regulator examples. Legal consequences require a separate jurisdiction-specific assessment.','SmallD')
newpage()

for c in CANDIDATES:
    add(f'{c["id"]} / PRIORITY {c["rank"]} / {c["country"].upper()}','KickerD')
    add(esc(c['project']),'H1D')
    add('<b>'+esc(c['topic'])+'</b><br/>'+esc(c['period']))
    head('Two attributable statements')
    add(esc(c['actor']))
    add('<b>Join keys:</b> '+esc(c['identifiers']))
    head('Evidence inspected')
    add(esc(c['specimen']))
    head('The if/then test')
    add(esc(c['rule']))
    head('Do this first; reject these false positives')
    add(esc(c['pilot']))
    add(esc(c['gates']))
    head('Why a surviving mismatch matters')
    add(esc(c['value']))
    add('<b>Readiness:</b> '+esc(c['readiness']),'SmallD')
    lines=[]
    for role,group in [('Western',c['western']),('Host',c['host'])]:
        for n in group:
            r=byid[n]
            label=n.replace('.bin','.xlsx')
            lines.append(f'{role}: '+url(label,r['url'])+f' - HTTP 200; {r["bytes"]/1000000:.2f} MB')
    add('<br/>'.join(lines),'SmallD')
    newpage()

add('Turn a mismatch into a logical contradiction','H1D')
add('The strict test is a conditional one: once two statements are verified to concern the same fact, their allowed values must have no overlap. The system can establish incompatibility without choosing which statement is true. A different number by itself does not establish that condition.')
table([
 ['Required alignment','What the system must retain'],
 ['Speaker and recipient','Company-original statement, filing/submission identity, host publication provenance. A compiler or translation error is not proof the company made the false claim.'],
 ['Entity and project','Operator ID, parent/subsidiary bridge, project components, recipient and share class where relevant.'],
 ['Time and version','Covered period, effective date, submission date, revision date, initial declaration and reconciled replacement.'],
 ['Definition and scope','Fine metal vs concentrate; 100% vs attributable; legal vs economic ownership; paid vs owed; gross vs net; offsets and refunds.'],
 ['Precision and currency','Original units, rounding increments, actual transaction rates or defensible bounds. Never use a guessed tolerance or annual-average FX as proof.'],
 ['Completeness','Blank, non-response, below-threshold and omitted fields remain unknown, not zero.'],
 ],[111,376])
head('A particularly useful currency rule')
add('For positive payments in one local currency, with local total L and known payment-date rates between r_min and r_max local units per USD, the USD total must lie in [L/r_max, L/r_min]. Add only documented rounding uncertainty. With mixed currencies, refunds or offsets, derive bounds component by component instead.')
head('Actual calibration from this research')
add('Ity royalties fall inside the FX interval; Senegal royalties also fall inside it. Southern Copper\'s molybdenum values overlap within the published table precision. Those controls demonstrate usable joins, not truth. Fekola\'s dividend arithmetic does not overlap before definition adjustments, so it is held for review rather than labelled false.')
head('Output language')
add('Return COMPATIBLE WITH PRECISION, REVIEW REQUIRED, or INCOMPATIBLE CLAIMS. Only the last requires every alignment gate to be satisfied. Even then the conclusion is "these verified assertions cannot both be correct"; it does not establish deliberate lying, criminal conduct or which regulator received the wrong figure.')
newpage()

add('Use AI for language and extraction, not the verdict','H1D')
add('Retain the original-language span, page/cell, company attribution, table headers and footnotes beside every extracted claim. Ask the model to produce a literal translation plus a structured record; have a reviewer approve each new document template and each new category mapping. Then run deterministic arithmetic and set comparisons.')
table([['Source term','Working meaning / caution']]+[[x['source'],x['meaning']+'. '+x['caution']] for x in glossary],[172,315])
head('A compact claim record')
add('Store: company ID; parent; project ID; factual predicate; value and precision; original unit; currency; covered period; effective date; filing version; share/scope basis; gross/net basis; source URL; SHA-256; page/cell; original text; translation; author; recipient; confidence; and unresolved gates.')
head('The supplied comparison kernel')
add('The starter kit includes a small Python kernel that compares already-normalised intervals or mutually exclusive categories. It deliberately refuses to issue an incompatibility result while an alignment gate is unresolved. Four controls were executed successfully, including a synthetic disjoint pair and the quarantined Mali dividend example. This is a starting component, not a finished document crawler or a completed audit of all ten projects.')
newpage()

add('Where to invest the first work','H1D')
head('1. Prove extraction on three different fact types')
add('Use Peru molybdenum for unit conversion and aggregation; Brazil Tank XII for translated categorical assertions; Ity for subsidiary aggregation and bounded FX. Preserve their consistent values as regression controls. Run the first pilot on a few dozen precise claims, then broaden by year and operator.')
head('2. Resolve the three highest-value financial questions')
add('For Fekola, establish dividend gross/net and equity-entitlement treatment before interpreting the non-overlap. For Sabodala, document the SGO/SMC-to-project bridge. For QMM, document the royalty basket and legitimate MGA/USD conversion bounds. Each question is bounded and begins from evidence already downloaded.')
head('3. Use ownership declarations as an independent branch')
add('Kibali and Essakane supply attributable company ownership data. Build date-aware ownership graphs and preserve holding-company layers. The Burkina workbook embeds original forms; the DRC workbook tells you which companies supplied a declaration. Those provenance fields are essential filters.')
head('Routes deliberately not promoted into the ten')
table([
 ['Route','Reason / observed test'],
 ['Mauritania - Tasiast','2024 report PDF p. 60 already explicitly compares the local declaration with Kinross ESTMA. A precedent, not evidence of an unchecked new pairing.'],
 ['Mongolia - Oyu Tolgoi','National PDFs downloaded, but the live reporting portal returned 502. Detailed royalty appendix is government-side; company totals include broader flows. Insufficient attribution for the desired exact payment test.'],
 ['DRC - Kamoa payment API','Summary XLSX downloaded, but its company-level amounts are government revenues. The annex points to a separate reconciliation file that was not located; ownership declaration marked not supplied.'],
 ['Philippines - MGB bulletin','Direct production-bulletin download returned 403. EITI report was accessible, but a stronger, precise company-government match was not established in this session.'],
 ['EITI bulk company-revenue query','One filtered revenue query returned 403 although an individual revenue record worked. Use national originals; do not claim the bulk query was verified.'],
 ['Canadian securities bulk access','Do not assume SEDAR+ bulk availability from the Rabbit catalogue. The tested Western securities route here is EDGAR.'],
 ],[132,355])
add('These are not assertions that the underlying information is unavailable everywhere. They record why these particular routes failed the selection standard during this research.','SmallD')
newpage()

add('Evidence custody and research limits','H1D')
add(f'The kit contains a manifest of {len(manifest)} selected original downloads, retrieval metadata and hashes, candidate specimens, and {len(included)} machine-readable source snapshots. Full third-party narrative reports are linked rather than reproduced. Every source used in a candidate returned HTTP 200 and was parsed far enough to locate the named project or company. A page title or search snippet alone was not counted as an availability test.')
head('What the archive lets an investigator reproduce')
add('candidates.json contains the full candidate cards and embedded-form provenance. source-manifest.json supplies exact URLs, final redirect URLs, UTC retrieval times, content types, byte counts and SHA-256 hashes. archive_path identifies the snapshots included in the kit; other reports can be fetched using download_filename and the source URL. access-log.jsonl records all direct fetches, including the three failed routes. fetch_sources.py can re-fetch one candidate\'s documents without overwriting the evidence snapshot.')
head('What this search did not establish')
add('No material cross-government contradiction has been established to publication standard. No company was contacted. Local filing law, admissibility, assurance and attribution to the original submitter remain case-specific. Download access today is not an uptime guarantee, an unrestricted redistribution licence or a promise that every year is complete.')
head('Relationship to yesterday\'s Rabbit idea')
add('This extends the earlier if/then mechanism and the Rabbit ESTMA source SYS-0295. The crucial refinement is speaker attribution: the host-side comparison must be the company\'s own representation, not simply government receipts. Existing reconciliation already checks many company-versus-government payment differences; the proposed additional check runs across the company\'s statements to different national systems.')
head('The assumption about a previously unchecked space')
add('Treat low cross-jurisdiction checking as a hypothesis, not an established fact. Mauritania provides a direct counterexample: its 2024 report discusses matching the local Tasiast declaration to ESTMA. The defensible opportunity is broader coverage, reproducibility, multilingual extraction and logically stricter predicates, rather than claiming nobody has attempted the comparison.')
add(url('Mauritania 2024 report - see PDF p. 60',byid['mauritania-2024.pdf']['url']),'SmallD')
head('Key reading on access and reporting')
add(url('Companies House: file or search an extractives report','https://www.gov.uk/guidance/file-or-search-for-an-extractives-report')+'<br/>'+url('SEC: public disclosure API','https://www.sec.gov/newsroom/whats-new/osd-announcement-090821-sec-disclosure-data-api')+'<br/>'+url('Peru: mandatory ESTAMIN reporting','https://mineria.minem.gob.pe/obligaciones_mineras/estamin/')+'<br/>'+url('Ghana original national report page','https://gheiti.gov.gh/site/index.php?catid=3%3Anewsflash&id=86%3A2023-gheiti-mining-sector-reconciliation-report&option=com_content&view=article'),'SmallD')

def pagepaint(c,doc):
    w,h=A4;c.saveState();c.setFillColor(teal);c.rect(0,h-9,w,9,fill=1,stroke=0)
    c.setStrokeColor(colors.HexColor('#D7E1E5'));c.line(54,42,w-54,42)
    c.setFont('DV',7);c.setFillColor(muted);c.drawString(54,28,'RABBIT  /  MINING CLAIMS  /  RESEARCH SNAPSHOT 12 OCTOBER 2026')
    c.drawRightString(w-54,28,str(doc.page));c.restoreState()

pdf=OUT/'pdf/Rabbit_Mining_Claim_Pairings_2026-10-12.pdf';pdf.parent.mkdir(exist_ok=True)
doc=SimpleDocTemplate(str(pdf),pagesize=A4,leftMargin=54,rightMargin=54,topMargin=40,bottomMargin=55,
    title='Rabbit - Ten Mining Company Cross-Government Claim Pairings',author='Research prepared for Graeme Smith')
doc.build(story,onFirstPage=pagepaint,onLaterPages=pagepaint)
print(json.dumps({'pdf':str(pdf),'source_count':len(manifest),'controls':results,'archive_source_bytes':sum(x['bytes'] for x in manifest)},indent=2))
