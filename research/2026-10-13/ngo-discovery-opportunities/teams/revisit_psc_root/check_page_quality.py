#!/usr/bin/env python3
"""Page-level extraction quality control, not an ownership adjudication."""
import hashlib,json,pathlib,subprocess
P=pathlib.Path(__file__).parent;C=pathlib.Path('/tmp/ngo-revisit-psc');r=json.loads((P/'history-companion.json').read_text());out=[]
for c in r['controls']:
 for d in c['documents']:
  if d['form_type']!='NEWINC':continue
  sha=d['sha256'];pdf=C/(sha+'.pdf');pages=(C/(sha+'.txt')).read_text().split('\f')[:-1];chars=[len(''.join(p.split())) for p in pages];blank=[i+1 for i,n in enumerate(chars) if n<30];samples=[]
  # Three evenly spaced low-text pages expose OCR/companion need; no full-read claim.
  chosen=sorted(set(blank[i] for i in [0,len(blank)//2,len(blank)-1])) if blank else []
  for i in chosen:
   stem=C/(sha+'-quality-'+str(i));subprocess.run(['pdftoppm','-f',str(i),'-l',str(i),'-singlefile','-r','150','-png',str(pdf),str(stem)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   p=subprocess.run(['tesseract',str(stem)+'.png','stdout','-l','eng','--psm','3'],capture_output=True,text=True,check=True);text=p.stdout;(C/(sha+'-quality-'+str(i)+'.ocr.txt')).write_text(text)
   samples.append({'physical_page':i,'ocr_nonwhitespace_chars':len(''.join(text.split())),'ocr_sha256':hashlib.sha256(text.encode()).hexdigest(),'tool':'local tesseract; recognition output unverified until page review'})
  out.append({'company_number':c['company_number'],'pdf_sha256':sha,'pdf_pages':d['pages'],'nonwhitespace_chars_by_page':chars,'low_text_pages':blank,'ocr_samples':samples,'scope':'page quality sample; not complete rights/history interpretation'})
(P/'page-quality.json').write_text(json.dumps({'controls':out,'paid_calls':0,'no_allegations':True},indent=2)+'\n');print(json.dumps(out,indent=2))
