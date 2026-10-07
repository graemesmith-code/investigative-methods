"""Observed relationship-level filing events, not inferred current ownership."""
import json,re,collections
from html.parser import HTMLParser
from acquire import P,S
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,s):
  s=s.replace('\u200b','').strip()
  if s:self.parts.append(s)
class Boxes(HTMLParser):
 def __init__(self):super().__init__();self.values=[]
 def handle_starttag(self,t,a):
  if t=='input' and dict(a).get('type')=='checkbox':self.values.append('checked' in dict(a))
def extract_fields(raw):
 if raw.startswith(b'%PDF'):return {'format':'pdf','field_parse':'not inferred from image PDF metadata'}
 s=raw.decode();out={'format':'html','field_parse':'parsed original HTML'}
 if '14. Is there any foreign entity' in s:
  start=s.index('14. Is there any foreign entity');end=s.index('</table>',start)+8;b=Boxes();b.feed(s[start:end])
  out['registration_section14_response']={(True,False):'No',(False,True):'Yes'}.get(tuple(b.values),'unresolved')
 start=s.find('28. Name of each previously reported foreign entity')
 if start>=0:
  end=s.find('CONVICTIONS DISCLOSURE',start);fragment=s[start:end if end>=0 else len(s)]
  p=Text();p.feed(fragment)
  out['removed_foreign_entities']=[v for v in p.parts if not v.startswith('28. Name of each previously reported foreign entity') and not re.fullmatch(r'\d+',v)]
 return out
def run():
 clients={r['client_id']:r for r in json.loads((P/'client-screen.json').read_text())};rows={}
 for f in S.glob('lda-*.json'):
  try:d=json.loads(f.read_text())
  except (ValueError,UnicodeDecodeError):continue
  if isinstance(d,dict):
   for r in d.get('results',[]):
    if r.get('client',{}).get('id') in clients and 'filing_uuid' in r:rows[r['filing_uuid']]=r
 latest={}
 for r in rows.values():
  if r['filing_type'] not in ('RR','RA'):
   k=(r['client']['id'],r['registrant']['id'],r['filing_year'],r['filing_period'])
   if k not in latest or r['dt_posted']>latest[k]['dt_posted']:latest[k]=r
 events=collections.defaultdict(list);unparsed=0
 for r in sorted(rows.values(),key=lambda r:(r['dt_posted'],r['filing_uuid'])):
  id=r['client']['id'];file=S/('original-'+r['filing_uuid']+'.html');fields=extract_fields(file.read_bytes()) if file.exists() else {'field_parse':'original missing'}
  if fields.get('format')=='pdf':unparsed+=1
  additions=r.get('foreign_entities',[]);removed=fields.get('removed_foreign_entities',[])
  if r['filing_type'] in ('RR','RA') or additions or removed:
   current=True if r['filing_type'] in ('RR','RA') else latest[(id,r['registrant']['id'],r['filing_year'],r['filing_period'])]['filing_uuid']==r['filing_uuid']
   events[id].append({'uuid':r['filing_uuid'],'posted':r['dt_posted'],'reporting_year':r['filing_year'],'period':r['filing_period'],'filing_type':r['filing_type'],'registrant_id':r['registrant']['id'],'registrant':r['registrant']['name'],'source':r['filing_document_url'],'locator':'LD-1 section 14 or LD-2 sections 27-28','registration_entities_or_ld2_additions':additions,'latest_acquired_version_for_quarter':current,**fields})
 histories={int(f.name.split('-')[2]):json.loads(f.read_text()) for f in S.glob('lda-history-*-summary.json')}
 rr={r['client_id']:r for r in json.loads((P/'rr-coverage.json').read_text())};out=[]
 for id,c in clients.items():
  h=histories.get(id);out.append({'client_id':id,'client':c['client_name'],'country':c['country'],'complete_all_years_query_acquired':bool(h and h['complete']),'all_years_form_count':h['count'] if h else None,'original_rr_rows':rr[id]['rr_count'],'initial_registration_gap':rr[id]['rr_count']==0,'interpretation':'Observed filing events only; no claim of complete current ownership. Posted dates are disclosure dates, not ownership-effective dates. Empty LD-2 additions do not mean No. Image-PDF fields need original inspection.','events':events[id]})
 (P/'ownership-timelines.json').write_text(json.dumps(out,indent=2))
 summary={'relationships':len(out),'relationships_with_complete_all_years_query':sum(x['complete_all_years_query_acquired'] for x in out),'zero_rr_retrievals':sum(x['initial_registration_gap'] for x in out),'relationships_with_observed_events':sum(bool(x['events']) for x in out),'observed_events':sum(len(x['events']) for x in out),'original_image_pdf_records_not_field_parsed':unparsed,'removal_events':sum(bool(e.get('removed_foreign_entities')) for x in out for e in x['events'])}
 (P/'ownership-timeline-coverage.json').write_text(json.dumps(summary,indent=2));print(summary)
if __name__=='__main__':run()
