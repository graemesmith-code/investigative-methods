from pathlib import Path
import sys,json,concurrent.futures,zlib,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'afghan-chinese-deps'))
import requests,fitz
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import download_pdfs
ROOT=Path(__file__).resolve().parent

def archive(record):
 url='https://data.commoncrawl.org/'+record['file_path'];off=int(record['offset']);dec=zlib.decompressobj(31);body=bytearray();used=0
 with requests.Session() as session:
  a=HTTPAdapter(max_retries=Retry(total=2,backoff_factor=.5,status_forcelist=[429,500,502,503,504]));session.mount('https://',a)
  while not dec.eof and used<32*1024*1024:
   got=0
   with session.get(url,headers={'Range':f'bytes={off+used}-{off+used+262143}'},timeout=(20,40),stream=True) as response:
    response.raise_for_status()
    if response.status_code!=206:raise ValueError('No range response')
    for b in response.iter_content(16384):
     got+=len(b);body.extend(dec.decompress(b))
     if len(body)>100*1024*1024:raise ValueError('Archive member exceeds limit')
     if dec.eof:break
   used+=got
   if not got:raise ValueError('No archive bytes')
 if not dec.eof:raise ValueError('Incomplete archive member')
 header,content=bytes(body).split(b'\r\n\r\n',1);wh={k.decode('latin1').lower():v.strip().decode('latin1') for line in header.split(b'\r\n')[1:] if b':' in line for k,v in [line.split(b':',1)]}
 http,pdf=content[:int(wh['content-length'])].split(b'\r\n\r\n',1)
 if b'%PDF-' not in pdf[:1024]:raise ValueError('Not PDF')
 info={'source':'archive','archive_url':url,'archive_offset':off,'archive_date':wh.get('warc-date'),'warc_truncated':wh.get('warc-truncated'),'pdf_eof_present':b'%%EOF' in pdf[-2048:]}
 info['partial']=bool(info['warc_truncated']) or not info['pdf_eof_present'];return pdf,info

def f(p):
 rec=json.load(open(ROOT/'work/records'/p.name));old=json.load(open(p))
 try:
  b,info=archive(rec);dest=ROOT/'pdfs'/(download_pdfs.file_key(rec)+'.pdf');dest.write_bytes(b)
  out=dict(id=rec['id'],url=rec['url'],record_key=rec['record_key'],errors=old.get('errors',[]),streaming_recovery=True,**info,pdf_path='pdfs/'+dest.name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),status='partial PDF' if info['partial'] else 'PDF downloaded')
  d=fitz.open(dest);out['pdf_pages']=len(d)
  (ROOT/'native-text'/(rec['record_key']+'.txt')).write_text('\n\n'.join(page.get_text() for page in d))
  if len(d):d[0].get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(ROOT/'previews'/(rec['record_key']+'.png'))
  p.write_text(json.dumps(out,ensure_ascii=False));print('RECOVERED',rec['record_key'][:8],len(d),'pages',flush=True)
 except Exception as e:print('FAILED',rec['record_key'][:8],type(e).__name__,str(e)[:150],flush=True)
paths=[p for p in (ROOT/'downloads').glob('*.json') if json.load(open(p))['status']=='PDF unavailable']
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(f,paths))
