#!/usr/bin/env python3
"""Two-page Ukrainian OCR baseline; commits counts/hashes only, never staff text."""
import pathlib,json,urllib.request,hashlib,subprocess,re,time
P=pathlib.Path(__file__).parent;C=pathlib.Path('/tmp/ngo-revisit-integrity');D=C/'ukr-tessdata';D.mkdir(exist_ok=True)
def digest(b):return hashlib.sha256(b).hexdigest()
result=dict(test='bounded two-page suitable-language OCR baseline',language='ukr',actual_spend_usd=0,staff_text_published=False,credential_assessment='unperformed',checks=[])
try:
 for filename in ['ukr.traineddata','LICENSE']:
  u='https://raw.githubusercontent.com/tesseract-ocr/tessdata_fast/main/'+filename
  b=urllib.request.urlopen(u,timeout=35).read();(D/filename).write_bytes(b)
  result[filename]=dict(url=u,sha256=digest(b),bytes=len(b),tls_verification='enabled',license='Apache-2.0' if filename=='LICENSE' else 'See official tessdata_fast LICENSE;Apache-2.0')
 result['tool_versions']=dict(tesseract=subprocess.check_output(['tesseract','--version'],stderr=subprocess.STDOUT,text=True).splitlines()[0],pdftoppm=subprocess.check_output(['pdftoppm','-v'],stderr=subprocess.STDOUT,text=True).splitlines()[0])
 j=json.loads((P/'procurement-bundle.json').read_text());a=next(x for x in j['checks'] if x.get('document_category')=='employment_relationship_evidence_archive');result['archive_document_id']=a['id'];result['archive_sha256']=a['sha256']
 # Fixed first two archive members,one page each,chosen before OCR outcomes.
 for i,m in enumerate(a['archive_members'][:2]):
  b=(C/m['sha256']).read_bytes();pdf=C/(m['sha256']+'.pdf');pdf.write_bytes(b);stem=C/('ukr-baseline-'+str(i));subprocess.run(['pdftoppm','-f','1','-singlefile','-r','200','-png',str(pdf),str(stem)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  started=time.monotonic();out=C/('ukr-baseline-text-'+str(i));subprocess.run(['tesseract',str(stem)+'.png',str(out),'--tessdata-dir',str(D),'-l','ukr','--psm','3'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE);elapsed=time.monotonic()-started;t=out.with_suffix('.txt').read_text(errors='replace');old=(C/(m['sha256']+'.txt')).read_text(errors='replace')
  result['checks'].append(dict(pdf_sha256=m['sha256'],pdf_page=1,rendered_page_sha256=digest(pathlib.Path(str(stem)+'.png').read_bytes()),ocr_total_characters=len(t),ocr_cyrillic_characters=len(re.findall('[А-Яа-яІіЇїЄєҐґ]',t)),ocr_replacement_characters=t.count('\ufffd'),previous_pdftext_total_characters=len(old),previous_pdftext_cyrillic_characters=len(re.findall('[А-Яа-яІіЇїЄєҐґ]',old)),elapsed_seconds=round(elapsed,3),recognition_quality_flag='Cyrillic recognition restored;accuracy not manually annotated;do not infer credentials',ocr_text_sha256=digest(t.encode()),staff_text_saved_only_in_tmp=True))
 result['status']='success'
except Exception as e:result.update(status='failed',error=str(e))
(P/'ukrainian-ocr-baseline.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k in ['status','error','checks','tool_versions']},indent=2))
