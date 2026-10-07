"""Independently compare every acquired 2025 API amount with original LD-2 fields."""
import json,re,html
from decimal import Decimal,InvalidOperation
from html.parser import HTMLParser
from acquire import P,S
class Form(HTMLParser):
 def __init__(self):super().__init__();self.boxes=[];self.values=[];self.div=False
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='input' and a.get('type')=='checkbox':self.boxes.append('checked' in a)
  if t=='div':self.div=True;self.values.append('')
 def handle_endtag(self,t):
  if t=='div':self.div=False
 def handle_data(self,s):
  if self.div:self.values[-1]+=s
def num(s):
 s=re.sub(r'[\s,\u200b]','',s)
 return None if not s else str(Decimal(s))
out=[]
rows={r['filing_uuid']:r for f in S.glob('lda-annual-*.json') for r in json.loads(f.read_text())['results']}
for r in rows.values():
 if r['filing_type'] in ('RR','RA'):continue
 rec={'uuid':r['filing_uuid'],'source':r['filing_document_url'],'locator':'LD-2 page 1, sections 11-13'}
 try:
  s=(S/('original-'+r['filing_uuid']+'.html')).read_text();start=s.index('INCOME OR EXPENSES');end=s.index('14. REPORTING',start)
  f=Form();f.feed(s[start:end])
  if len(f.values)!=2 or len(f.boxes)!=4:raise ValueError('Unrecognized field structure')
  vals=[num(v) for v in f.values];rec['original_income'],rec['original_expenses']=vals
  rec['income_less_than_5000'],rec['expenses_less_than_5000']=f.boxes[:2]
  rec['matches_api']=all((a is None and r[k] is None) or (a is not None and r[k] is not None and Decimal(a)==Decimal(r[k])) for a,k in zip(vals,['income','expenses']))
 except Exception as e:rec['error']=type(e).__name__;rec['matches_api']=False
 out.append(rec)
(P/'original-amount-verification.json').write_text(json.dumps(out,indent=2))
print('Verified',len(out),'matching',sum(r['matches_api'] for r in out),'exceptions',[r for r in out if not r['matches_api']][:5])
