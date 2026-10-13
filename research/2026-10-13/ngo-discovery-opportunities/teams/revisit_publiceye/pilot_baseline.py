#!/usr/bin/env python3
"""No model API calls. Free local OCR plus deterministic country/tense nominations.
Inputs are two public company PDFs already downloaded in /tmp/ngo-revisit-publiceye.
Restricted Green Button standards/guide are NOT inputs to this program.
Copyrighted image/text caches stay in /tmp. Git output contains hashes and nominations.
"""
import pathlib,json,hashlib,subprocess,time,os,re,concurrent.futures,argparse
import fitz
D=pathlib.Path(__file__).parent
COUNTRIES={'Austria':r'Austria|[ÖO]sterreich','Slovakia':r'Slovakia|Slowakei','Turkey':r'Turkey|T[üu]rkei|Tiirkei','Pakistan':r'Pakistan','China':r'China'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cache',default='/tmp/ngo-revisit-publiceye');args=ap.parse_args();C=pathlib.Path(args.cache);jobs=[]
 for name in ['amidex-old','amidex-current']:
  doc=fitz.open(C/(name+'.pdf'))
  for n,page in enumerate(doc,1):
   image=C/(name+'-single-'+str(n)+'.png');page.get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(image);jobs.append((name,n,image,len(page.get_text().strip())))
 def job(j):
  name,n,image,nativechars=j;dest=C/(name+'-single-ocr-'+str(n));env=dict(os.environ,OMP_THREAD_LIMIT='1');start=time.perf_counter()
  result=subprocess.run(['tesseract',str(image),str(dest),'-l','eng','--psm','6'],env=env,capture_output=True,timeout=35);f=dest.with_suffix('.txt');b=f.read_bytes() if f.exists() else b'';t=b.decode(errors='replace');countries=[]
  for country,pattern in COUNTRIES.items():
   for m in re.finditer(pattern,t,re.I):countries.append({'country':country,'char_start':m.start(),'char_end':m.end()})
  return {'document_id':name,'physical_pdf_page':n,'native_text_nonwhitespace_chars':nativechars,'ocr_engine':'tesseract','ocr_language':'eng (German language pack unavailable)','ocr_psm':6,'threads':1,'exit_status':result.returncode,'wall_seconds':round(time.perf_counter()-start,3),'ocr_chars':len(t),'ocr_text_sha256':hashlib.sha256(b).hexdigest(),'country_nominations':countries,'interpretation_warning':'Country presence is not supplier scope or matched time; manually validate context.','ai_calls':0}
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:rows=list(ex.map(job,jobs))
 (D/'ocr-baseline.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows));print(json.dumps({'pages':len(rows),'nonempty_ocr_pages':sum(r['ocr_chars']>0 for r in rows),'raw_text_pages':sum(r['native_text_nonwhitespace_chars']>0 for r in rows),'ocr_chars':sum(r['ocr_chars'] for r in rows),'total_worker_seconds':sum(r['wall_seconds'] for r in rows),'paid_calls':0}))
if __name__=='__main__':main()
