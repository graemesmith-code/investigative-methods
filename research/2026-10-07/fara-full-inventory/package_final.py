"""Produce readable PDF and a portable offline evidence bundle; no network."""
import pathlib,re,html,zipfile
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Preformatted
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("DejaVu","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold", italic="DejaVu", boldItalic="DejaVu-Bold")
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[2]
styles=getSampleStyleSheet();
for st in styles.byName.values():st.fontName='DejaVu'
styles['BodyText'].fontSize=10;styles['BodyText'].leading=14;styles['BodyText'].spaceAfter=7
styles['Heading1'].textColor=colors.HexColor('#14334a');styles['Heading2'].textColor=colors.HexColor('#14334a')
def inline(s):
 s=html.escape(s);s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:'<a href="'+m[2]+'" color="#165c92">'+m[1]+'</a>',s);s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s);return s.replace('`','')
def blocks(text):
 out=[];lines=text.splitlines();i=0
 while i<len(lines):
  line=lines[i]
  if not line.strip():i+=1;continue
  if line.startswith('```'):
   a=[];i+=1
   while i<len(lines) and not lines[i].startswith('```'):a.append(lines[i]);i+=1
   for x in a:out.append(Paragraph(inline(x),styles['Code']))
  elif line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].startswith('|'):
    if not re.match(r'^\|[\s|:\-]+$',lines[i]):rows.append([Paragraph(inline(x.strip()),styles['BodyText']) for x in lines[i].strip('|').split('|')])
    i+=1
   t=Table(rows,colWidths=[510/len(rows[0])]*len(rows[0]),repeatRows=1);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6eef3')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.25,colors.HexColor('#b8c7cf')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5)]));out+=[t,Spacer(1,10)];continue
  elif line.startswith('# '):out.append(Paragraph(inline(line[2:]),styles['Title']))
  elif line.startswith('## '):out.append(Paragraph(inline(line[3:]),styles['Heading2']))
  else:out.append(Paragraph(inline(line),styles['BodyText']))
  i+=1
 return out
def footer(c,d):
 c.setFont('DejaVu',8);c.setFillColor(colors.grey);c.drawString(42,25,'Private research · 7 October 2026 · Evidence gaps are not findings of misconduct');c.drawRightString(552,25,str(d.page))

story=blocks((P/'REPORT.md').read_text())+[PageBreak()]+blocks((P/'ANNEX.md').read_text())
SimpleDocTemplate(str(P/'foreign-control-final.pdf'),pagesize=(595,842),rightMargin=42,leftMargin=42,topMargin=40,bottomMargin=42,title='Foreign control and lobbying: final source-first review').build(story,onFirstPage=footer,onLaterPages=footer)
import json,hashlib
selected=set()
for case in json.loads((P/'major-original-reconciliation.json').read_text()):
 for event in case['events']+case['latest_2025_forms']:selected.add(ROOT/event['original_file'])
for case in json.loads((P/'historical-amount-verification.json').read_text()):
 for event in case['selected_originals']:selected.add(ROOT/event['original'])
selected.update(f for f in P.glob('*') if f.is_file() and f.suffix in ['.md','.py','.json','.jsonl','.pdf'])
selected.update((P/'sources').glob('browser-*'))
selected.update((P/'sources/selected-house-originals').glob('*.xml'))
selected.add(P/'sources/gotion-annual-report-2024.pdf')
# Include every source-linked LDA original cited directly in the report.
for u in re.findall(r'/filing/([a-f0-9-]+)/', (P/'REPORT.md').read_text()):
 selected.update(P.parent.glob('*/sources/*'+u+'*.html'))
for stage in ['lobbying-control-pilot','lobbying-control-expansion']:
 base=P.parent/stage
 selected.update(base.glob('*.md'))
 selected.update(f for f in base.rglob('*') if f.is_file() and any(w in f.name.lower() for w in ['budget','ledger','calibration','baseline']) and f.suffix in ['.json','.jsonl','.md','.py'])
output=P/'foreign-control-review.zip'
with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(selected):
  if f.exists():z.write(f,str(f.relative_to(ROOT)))
 z.writestr('START-HERE.txt','Read research/2026-10-07/fara-full-inventory/foreign-control-final.pdf. REPORT.md supersedes earlier checkpoints. This compact offline review bundle contains selected originals and audit records; full replay requires the private repository and public archives identified in the manifests. No new paid calls were made in this continuation.\n')
 with_manifest=[{'path':str(f.relative_to(ROOT)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(selected) if f.exists()]
 z.writestr('MANIFEST.json',json.dumps(with_manifest,indent=2))
with zipfile.ZipFile(output) as z:assert z.testzip() is None
print(json.dumps({'pdf_bytes':(P/'foreign-control-final.pdf').stat().st_size,'zip_bytes':output.stat().st_size,'zip_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'members':len(with_manifest)+2}))
