"""Read LD-2 foreign-interest narratives from EVERY acquired original HTML.

An empty additions array is not an empty disclosure. PDF/image records abstain.
This applies the role distinction to all locally acquired forms, not just leads.
"""
import json,pathlib,re,sys,collections
P=pathlib.Path(__file__).resolve().parent;E=P.parent/'lobbying-control-expansion';ROOT=P.parents[2];F=P.parent/'lobbying-control-pilot'
sys.path.insert(0,str(E/'scripts'));from ownership_timelines import Text,Boxes
PAT=re.compile(r'19\. Interest of each foreign entity.*?</p>\s*<p\s+class="lightbox">(.*?)</p>',re.S)
def extract(raw):
 if raw.startswith(b'%PDF'):return {'status':'PDF requires original image/text review','narratives':[]}
 s=raw.decode();matches=PAT.findall(s);items=[]
 for fragment in matches:
  t=Text();t.feed(fragment);v=' '.join(t.parts).strip()
  if v:items.append(v)
 headings=len(re.findall(r'19\. Interest of each foreign entity',s))
 return {'status':'parsed HTML' if len(matches)==headings else 'unrecognized section structure','headings':headings,'parsed_sections':len(matches),'narratives':list(dict.fromkeys(items))}
def run():
 metadata={}
 for root in [F/'sources',E/'sources',P/'sources']:
  for f in root.glob('lda-*.json'):
   try:d=json.loads(f.read_text())
   except (ValueError,UnicodeDecodeError):continue
   if isinstance(d,dict):
    for r in d.get('results',[]):
     if r.get('filing_uuid'):metadata[r['filing_uuid']]=r
 originals={}
 for root,pattern,prefix in [(F/'sources','original-*.html','original-'),(E/'sources','original-*.html','original-'),(P/'sources','lda-original-*.html','lda-original-')]:
  for f in root.glob(pattern):originals[f.stem.removeprefix(prefix)]=f
 out=[]
 for u,f in sorted(originals.items()):
  r=metadata.get(u,{});fields=extract(f.read_bytes());out.append({'uuid':u,'original_file':str(f.relative_to(ROOT)),'source':r.get('filing_document_url',f'https://lda.gov/filings/public/filing/{u}/print/'),'client_id':r.get('client',{}).get('id'),'current_index_label':r.get('client',{}).get('name'),'posted':r.get('dt_posted'),'year':r.get('filing_year'),'type':r.get('filing_type'),**fields})
 (P/'all-original-interest-audit.json').write_text(json.dumps(out,indent=2))
 summary={'unique_originals_audited':len(out),'status_counts':dict(collections.Counter(x['status'] for x in out)),'forms_with_nonempty_foreign_interest_narrative':sum(bool(x['narratives']) for x in out),'limitations':'Narrative text preserved, not classified as ownership evidence merely by presence. Original PDF/image forms abstain. Current index labels never substitute for printed historical client names.'}
 (P/'all-original-interest-coverage.json').write_text(json.dumps(summary,indent=2));print(summary)
 for cid in [194108,125608,113305]:
  found=[x for x in out if x['client_id']==cid and x['narratives']];print(cid,len(found),'earliest',min((x['posted'] for x in found),default=None));
  for x in sorted(found,key=lambda x:x['posted'])[:1]:print(x['uuid'],x['narratives'][:2])
if __name__=='__main__':run()
