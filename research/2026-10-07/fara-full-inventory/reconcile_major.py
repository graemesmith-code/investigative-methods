"""Offline original-form verification; API metadata locates but does not prove facts.

Current API client labels can differ from names printed on historical originals.
Amounts are independently parsed; amendment chronology uses posted timestamps.
"""
import pathlib,json,sys,collections,datetime
from decimal import Decimal
from html.parser import HTMLParser
P=pathlib.Path(__file__).resolve().parent;E=P.parent/'lobbying-control-expansion'
sys.path.insert(0,str(E/'scripts'))
from ownership_timelines import extract_fields,Text
class Amount(HTMLParser):
 def __init__(self):super().__init__();self.boxes=[];self.values=[];self.div=False
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='input' and a.get('type')=='checkbox':self.boxes.append('checked' in a)
  if t=='div':self.div=True;self.values.append('')
 def handle_endtag(self,t):
  if t=='div':self.div=False
 def handle_data(self,s):
  if self.div:self.values[-1]+=s

def number(s):
 s=s.replace(',','').replace('\u200b','').strip();return None if not s else str(Decimal(s))
def amount(raw):
 text=raw.decode();a=text.index('INCOME OR EXPENSES');b=text.index('14. REPORTING',a);p=Amount();p.feed(text[a:b])
 assert len(p.values)==2 and len(p.boxes)==4,'Unrecognized amount field structure'
 return dict(zip(['income','expenses'],map(number,p.values))),p.boxes

def run():
 selections=json.loads((P/'major-history-coverage.json').read_text());ids={i for x in selections for i in x['resolved_client_ids']}|{57856,57857}
 rows={}
 for root in [E/'sources',P/'sources']:
  for f in root.glob('lda-*.json'):
   try:d=json.loads(f.read_text())
   except (ValueError,UnicodeDecodeError):continue
   if isinstance(d,dict):
    for r in d.get('results',[]):
     if r.get('client',{}).get('id') in ids and r.get('filing_uuid'):rows[r['filing_uuid']]=r
 out=[];checks=[]
 for cid in sorted(ids):
  rr=[r for r in rows.values() if r['client']['id']==cid];events=[];latest={};missing=[]
  for r in sorted(rr,key=lambda x:(datetime.datetime.fromisoformat(x['dt_posted']),x['filing_uuid'])):
   u=r['filing_uuid'];f=P/'sources'/f'lda-original-{u}.html'
   if not f.exists():f=E/'sources'/f'original-{u}.html'
   if not f.exists():missing.append(u);continue
   raw=f.read_bytes();fields=extract_fields(raw)
   record={'uuid':u,'source':r['filing_document_url'],'original_file':str(f.relative_to(P.parent.parent.parent)),'posted':r['dt_posted'],'filing_type':r['filing_type'],'year':r['filing_year'],'period':r['filing_period']}
   if r['filing_type'] in ['RR','RA'] or r.get('foreign_entities') or fields.get('removed_foreign_entities'):
    p=Text()
    if fields.get('format')=='html':p.feed(raw.decode())
    events.append({**record,**fields,'index_foreign_entities_requiring_original_confirmation':r.get('foreign_entities',[]),'original_text':'\n'.join(p.parts) if p.parts else None})
   if r['filing_year']==2025 and r['filing_type'] not in ['RR','RA']:
    c={**record,'client_id':cid}
    try:
     values,boxes=amount(raw);c.update(original_amounts=values,amount_checkboxes=boxes,matches_api=all((v is None and r[k] is None) or (v is not None and r[k] is not None and Decimal(v)==Decimal(r[k])) for k,v in values.items()))
    except Exception as e:c.update(matches_api=False,error=str(e))
    checks.append(c)
    key=(r['registrant']['id'],r['filing_period'])
    # chronological iteration; ties explicitly flagged rather than silently certified
    if key in latest and latest[key]['posted']==r['dt_posted']:c['posting_timestamp_tie']=True
    latest[key]=c
  annual={k:str(sum(Decimal(r.get('original_amounts',{}).get(k) or 0) for r in latest.values())) for k in ['income','expenses']}
  out.append({'client_id':cid,'current_api_client_label':rr[0]['client']['name'],'forms':len(rr),'missing_originals':missing,'events':events,'annual_numeric_lower_bounds_2025':annual,'unknown_latest_amount_cells':sum(v is None for r in latest.values() for v in r.get('original_amounts',{}).values()),'latest_2025_forms':list(latest.values()),'caveats':'Current API labels may differ from historical printed clients. Unknown amounts are not asserted zero. Income and expense totals are separate; overlapping outside fees and in-house expenses must not be added. Events are observed disclosures, not a complete current ownership register.'})
 (P/'major-original-reconciliation.json').write_text(json.dumps(out,indent=2));(P/'major-amount-verification.json').write_text(json.dumps(checks,indent=2))
 summary={'major_relationships_selected':len(selections),'major_histories_complete':sum(bool(x['histories']) and all(h['complete'] for h in x['histories']) for x in selections),'major_history_forms':sum(h['forms'] for x in selections for h in x['histories']),'additional_gotion_outside_relationships':2,'total_unique_reviewed_history_forms':len(rows),'original_amount_checks_2025':len(checks),'original_amount_matches_api':sum(c['matches_api'] for c in checks),'exceptions':[c for c in checks if not c['matches_api']],'posting_timestamp_ties':[c for c in checks if c.get('posting_timestamp_tie')]}
 (P/'major-reconciliation-coverage.json').write_text(json.dumps(summary,indent=2));print(summary)
if __name__=='__main__':run()
