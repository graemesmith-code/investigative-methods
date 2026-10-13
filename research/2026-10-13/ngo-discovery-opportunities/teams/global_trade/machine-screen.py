#!/usr/bin/env python3
"""Ordinary-code lexical screen of cached Public Eye PDFs, without publishing text.
Run: python machine-screen.py [--cache /tmp/ngo-global-trade] [--inventory inventory.jsonl]
PDF/text acquisition is separate. This script makes no requests or model calls.
Offsets refer to pdftotext -layout UTF-8 output decoded with errors='replace'.
Page numbers are physical PDF positions delimited by form-feed, not printed folios.
Term hits nominate passages for subsequent human/model contextual review; they do not
establish a bottleneck, opportunity, contradiction, identity match or wrongdoing.
"""
import argparse,collections,hashlib,json,pathlib,re
TERMS={
 'bottleneck':r'\bbottlenecks?\b|\bbarriers?\b|\bobstacles?\b|\bintractable\b|\blabor[- ]intensive\b|\blabour[- ]intensive\b|\btime[- ]consuming\b|\bengp[aä]ss\w*|\bhinderniss\w*|\bobstacles?\b|\bgoulots?\b',
 'manual_processing':r'\bmanual(?:ly)?\b|\bmanuell\w*|\bmanuelle(?:ment)?\b|\bhand[- ]collect\w*|\bone[- ]by[- ]one\b',
 'data':r'\bdata(?:base|set)?s?\b|\bdaten\w*|\bdonn[ée]es\b|\bbases? de donn[ée]es\b',
 'document_format':r'\bPDFs?\b|\bscann?ed\b|\bOCR\b|\bspreadsheets?\b|\bExcel\b|\bnumeris\w*|\bnum[ée]ris\w*',
 'registry':r'\bregistr(?:y|ies)\b|\bregisters?\b|\bregistr[eo]s?\b|\bregistre\w*|\bHandelsregister\w*',
 'ownership':r'\bowners?\b|\bownership\b|\bbeneficial\b|\bshareholders?\b|\bb[ée]n[ée]ficiaires?\b|\bactionnaires?\b|\bEigent[üu]m\w*|\bwirtschaftlich\w* Berechtigt\w*',
 'payments':r'\bpayments?\b|\bpaid\b|\bpayable\b|\bversements?\b|\bpaiements?\b|\bZahlungen?\b|\broyalt(?:y|ies)\b|\bredevances?\b',
 'loans_finance':r'\bloans?\b|\blending\b|\bfinanc\w*|\bunderwriting\b|\bcredit\b|\bcr[ée]dit\w*|\bpr[êe]ts?\b|\bKredit\w*|\bDarlehen\w*',
 'trade_valuation':r'\bmisinvoic\w*|\binvoices?\b|\bvaluations?\b|\bunit values?\b|\bCIF\b|\bFOB\b|\btransfer pric\w*|\bfactur\w*|\bVerrechnungspreis\w*|\bZoll\w*|\bcustoms\b|\bdouan\w*',
 'access_secrecy':r'\binaccessib\w*|\bnot public\b|\bnon[- ]public\b|\bunpublished\b|\bundisclos\w*|\bsecret\w*|\bopaque\b|\bopacity\b|\bredact\w*|\bconfidential\w*|\bgeheim\w*|\bvertraulich\w*|\bopacit\w*|\bconfidentiel\w*',
 'methodology':r'\bmethod(?:s|ology)?\b|\bmethodolog\w*|\bm[ée]thod\w*|\bappendi(?:x|ces)\b|\bannexe?s?\b|\bAnhang\b|\bproxies\b|\bproxy\b|\blimitations?\b',
 'entity_matching':r'\bidentifiers?\b|\bmatching\b|\bjoins?\b|\bidentifiants?\b|\bidentit\w*|\bcompany numbers?\b',
}
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cache',default='/tmp/ngo-global-trade');ap.add_argument('--inventory',default=str(pathlib.Path(__file__).with_name('inventory.jsonl')));ap.add_argument('--output',default=str(pathlib.Path(__file__).with_name('machine-screen.jsonl')));args=ap.parse_args()
 cache=pathlib.Path(args.cache);records=[json.loads(x) for x in pathlib.Path(args.inventory).read_text().splitlines()];out=[]
 for r in records:
  if r['org']!='Public Eye' or r['acquisition_status']!='pdf_acquired':continue
  key=r['cache_key'];fp=cache/(key+'.txt');pdf=cache/(key+'.pdf')
  record={'org':r['org'],'title':r['title'],'date':r['date'],'canonical_source_url':r['url'],'report_download_url':r.get('pdf_urls',[None])[0],'report_sha256':r['sha256'],'machine_screened':False,'screening_method':'case-insensitive multilingual regex over pdftotext -layout output; no AI; all hits ledger','reading_claim':'Machine screening only; contextual/deep-reading fields in source inventory unchanged.','cache_key':key,'text_sha256':None,'text_bytes':None,'text_char_count':None,'nonempty_parsed_text':False,'pages_with_text':0,'category_hit_counts':{},'hits':[]}
  if not fp.exists():record['status']='text_cache_missing';out.append(record);continue
  b=fp.read_bytes();text=b.decode('utf-8',errors='replace');record.update(text_sha256=sha(b),text_bytes=len(b),text_char_count=len(text),nonempty_parsed_text=bool(text.strip()))
  if pdf.exists():record['report_hash_matches_inventory']=sha(pdf.read_bytes())==r['sha256']
  else:record['report_hash_matches_inventory']=None
  if not text.strip():record['status']='empty_parsed_text';out.append(record);continue
  offset=0;counts=collections.Counter();pages=text.split('\f');record['pages_with_text']=sum(bool(p.strip()) for p in pages)
  for page_number,page in enumerate(pages,1):
   for category,pattern in TERMS.items():
    for m in re.finditer(pattern,page,re.I):
     counts[category]+=1;record['hits'].append({'category':category,'physical_pdf_page':page_number,'page_char_start':m.start(),'page_char_end':m.end(),'text_char_start':offset+m.start(),'text_char_end':offset+m.end()})
   offset+=len(page)+1
  record.update(machine_screened=True,status='screened_nonempty_text',category_hit_counts=dict(sorted(counts.items())),total_hits=sum(counts.values()))
  out.append(record)
 pathlib.Path(args.output).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in out))
 print(json.dumps({'eligible_acquired_pdfs':len(out),'nonempty_parsed_pdfs':sum(r['nonempty_parsed_text'] for r in out),'machine_screened':sum(r['machine_screened'] for r in out),'total_term_hits':sum(r.get('total_hits',0) for r in out),'hash_mismatches':sum(r.get('report_hash_matches_inventory') is False for r in out),'paid_calls':0}))
if __name__=='__main__':main()
