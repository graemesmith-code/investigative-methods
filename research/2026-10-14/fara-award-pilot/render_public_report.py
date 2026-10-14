"""Render existing findings and package an explicit allowlist. No network calls.
Requires installed reportlab only for PDF rendering; analysis uses stdlib.
"""
from pathlib import Path
import csv,hashlib,html,json,re,zipfile
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
BASE=Path(__file__).resolve().parent
PDF=BASE/'FARA-federal-awards-public-report-2026-10-14.pdf'
font=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
if font.exists():
    pdfmetrics.registerFont(TTFont('Findings',str(font)))
    pdfmetrics.registerFont(TTFont('FindingsBold',str(font.with_name('DejaVuSans-Bold.ttf'))))
    pdfmetrics.registerFontFamily('Findings',normal='Findings',bold='FindingsBold',italic='Findings',boldItalic='FindingsBold')
    FONT='Findings'
else:FONT='Helvetica'
styles=getSampleStyleSheet()
for name in ['Normal','BodyText','Heading1','Heading2','Heading3','Title']:styles[name].fontName=FONT
styles['BodyText'].fontSize=9;styles['BodyText'].leading=13;styles['BodyText'].spaceAfter=7
styles['Heading1'].fontSize=18;styles['Heading2'].fontSize=13;styles['Heading3'].fontSize=11
small=ParagraphStyle('small',parent=styles['BodyText'],fontSize=7.2,leading=10,spaceAfter=0)
def inline(s):
    links=[]
    def link(m):
        label,url=m.groups();v='<link href="'+html.escape(url,quote=True)+'">'+html.escape(label)+'</link>' if url.startswith('https://') else html.escape(label)
        links.append(v);return '@@LINK'+str(len(links)-1)+'@@'
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,s)
    s=html.escape(s).replace('`','')
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    for i,v in enumerate(links):s=s.replace('@@LINK'+str(i)+'@@',v)
    return s
def render(text):
    lines=text.splitlines();out=[];i=0;para=[]
    def flush():
        if para:out.append(Paragraph(inline(' '.join(para)),styles['BodyText']));para.clear()
    while i<len(lines):
        line=lines[i].strip()
        if not line:flush();i+=1;continue
        if line.startswith('```'):
            flush();i+=1;code=[]
            while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
            out.append(Paragraph('<br/>'.join(html.escape(l) for l in code),small));out.append(Spacer(1,8));i+=1;continue
        if line.startswith('|'):
            flush();rs=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                row=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',x or 'x') for x in row):rs.append(row)
                i+=1
            n=len(rs[0]);widths=([170,72,269] if n==3 else [155,87,89,45,135] if n==5 else [511/n]*n)
            data=[[Paragraph(inline(c),small) for c in r] for r in rs]
            t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8eef4')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#8195a8')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f7f9fb')]),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
            out += [t,Spacer(1,10)];continue
        m=re.match(r'^(#{1,3})\s+(.+)',line)
        if m:flush();out.append(Paragraph(inline(m[2]),styles['Heading'+str(len(m[1]))]));i+=1;continue
        if line.startswith('- '):flush();out.append(Paragraph('• '+inline(line[2:]),styles['BodyText']));i+=1;continue
        para.append(line);i+=1
    flush();return out
def footer(c,doc):
    c.saveState();c.setFont(FONT,7);c.setFillColor(colors.HexColor('#556779'));c.drawString(42,25,'FARA / federal awards • 14 October 2026 • Descriptive overlaps, not violations')
    c.drawRightString(553,25,str(doc.page));c.restoreState()
story=[Paragraph('FARA and federal awards',styles['Title']),Paragraph('Public baseline • 14 October 2026 • $0 external spend',styles['BodyText'])]
for name in ['README.md','TECHNICAL-ANNEX.md','AMOUNTS.md','DOSSIERS.md']:
    if len(story)>2:story.append(PageBreak())
    story+=render((BASE/name).read_text())
SimpleDocTemplate(str(PDF),pagesize=(595,842),leftMargin=42,rightMargin=42,topMargin=40,bottomMargin=42,title='FARA and federal awards — public baseline',author='Investigative methods pilot').build(story,onFirstPage=footer,onLaterPages=footer)
print(str(PDF))
