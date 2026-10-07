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
P=pathlib.Path(__file__).resolve().parents[1];ROOT=P.parents[2]
styles=getSampleStyleSheet();
for st in styles.byName.values():st.fontName='DejaVu'
styles['BodyText'].fontSize=9;styles['BodyText'].leading=13;styles['BodyText'].spaceAfter=7
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
story=blocks((P/'README.md').read_text())+[PageBreak()]+blocks((P/'TECHNICAL-ANNEX.md').read_text())
SimpleDocTemplate(str(P/'lobbying-control-report.pdf'),pagesize=(595,842),rightMargin=42,leftMargin=42,topMargin=40,bottomMargin=42,title='Foreign control and lobbying disclosure: investigative pilot').build(story,onFirstPage=footer,onLaterPages=footer)
# Portable layout preserves the guard's repository-relative import.
out=ROOT/'lobbying-control-pilot-20261007.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(P.rglob('*')):
  if f.is_file() and '__pycache__' not in str(f) and not f.name.endswith(('-wal','-shm')):z.write(f,str(f.relative_to(ROOT)))
 z.write(ROOT/'code/ati/pipeline.py','code/ati/pipeline.py')
 z.writestr('START-HERE.txt','Open research/2026-10-07/lobbying-control-pilot/lobbying-control-report.pdf or README.md. Original source files and code are included. Live replay disabled; do not reset spending ledger.\n')
print(out, out.stat().st_size)
