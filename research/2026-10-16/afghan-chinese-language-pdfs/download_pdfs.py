#!/usr/bin/env python3
"""Re-download PDFs listed in manifest.jsonl. Requires: python -m pip install requests
Usage: python download_pdfs.py [--retry]
Archive copies are preferred. Current-site replacements and partial files are labelled.
"""
import argparse, concurrent.futures, datetime, gzip, hashlib, json, pathlib, threading, zlib
import requests
ROOT=pathlib.Path(__file__).resolve().parent
MAX_BYTES=100*1024*1024
HOST_LOCKS={};LOCK=threading.Lock()
def file_key(record):
    return hashlib.sha256(record['id'].encode()).hexdigest()[:24]
def archive(record):
    path=record.get('file_path','');offset=record.get('offset')
    if not path.startswith('crawl-data/') or offset is None:raise ValueError('No public Common Crawl WARC pointer')
    url='https://data.commoncrawl.org/'+path
    decoder=zlib.decompressobj(31);body=bytearray();consumed=0
    with requests.Session() as session:
        while not decoder.eof and consumed<32*1024*1024:
            count=1024*1024;start=int(offset)+consumed
            r=session.get(url,headers={'Range':f'bytes={start}-{start+count-1}'},timeout=(20,45))
            r.raise_for_status()
            if r.status_code!=206:raise ValueError('Archive server did not honor byte range')
            body.extend(decoder.decompress(r.content,MAX_BYTES-len(body)+1));consumed+=len(r.content)
            if len(body)>MAX_BYTES:raise ValueError('Archive exceeds 100 MiB limit')
        if not decoder.eof:raise ValueError('Incomplete gzip record after 32 MiB')
    header,content=bytes(body).split(b'\r\n\r\n',1)
    wh={k.decode('latin1').lower():v.strip().decode('latin1') for line in header.split(b'\r\n')[1:] if b':' in line for k,v in [line.split(b':',1)]}
    http,pdf=content[:int(wh['content-length'])].split(b'\r\n\r\n',1)
    if b'%PDF-' not in pdf[:1024]:raise ValueError('Archive payload is not a PDF')
    info=dict(source='archive',archive_url=url,archive_offset=offset,archive_date=wh.get('warc-date'),archive_target=wh.get('warc-target-uri'),warc_truncated=wh.get('warc-truncated'),pdf_eof_present=b'%%EOF' in pdf[-2048:])
    info['partial']=bool(info['warc_truncated']) or not info['pdf_eof_present']
    return pdf,info
def live(record):
    with LOCK:sem=HOST_LOCKS.setdefault(record['host'],threading.Semaphore(2))
    with sem,requests.get(record['url'],stream=True,timeout=(15,35),headers={'User-Agent':'PDFResearchInspection/1.0'}) as r:
        r.raise_for_status();out=bytearray()
        if int(r.headers.get('Content-Length','0'))>MAX_BYTES:raise ValueError('Live file exceeds 100 MiB limit')
        for chunk in r.iter_content(262144):
            out.extend(chunk)
            if len(out)>MAX_BYTES:raise ValueError('Live file exceeds 100 MiB limit')
        data=bytes(out)
        if b'%PDF-' not in data[:1024]:raise ValueError('Live response is not a PDF')
        eof=b'%%EOF' in data[-2048:]
        return data,dict(source='current website',final_url=r.url,retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),last_modified=r.headers.get('Last-Modified'),pdf_eof_present=eof,partial=not eof)
def download_one(record):
    dest=ROOT/'pdfs'/f"{file_key(record)}.pdf";dest.parent.mkdir(exist_ok=True)
    errors=[];saved=None
    try:
        saved=archive(record)
        if saved[1]['partial']:errors.append('Archived payload is truncated or lacks a PDF EOF marker')
    except Exception as e:errors.append('Archive: '+str(e))
    if saved is None or saved[1]['partial']:
        try:
            current=live(record)
            if saved is None or not current[1]['partial']:saved=current
        except Exception as e:errors.append('Current website: '+str(e))
    info=dict(id=record['id'],url=record['url'],errors=errors)
    if saved:
        data,details=saved;dest.write_bytes(data)
        info.update(details,pdf_path='pdfs/'+dest.name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),status='partial PDF' if details['partial'] else 'PDF downloaded')
    else:info['status']='PDF unavailable'
    return info
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--retry',action='store_true',help='Retry unavailable/partial PDFs; preserve existing complete files');args=ap.parse_args()
    records=[json.loads(line) for line in (ROOT/'manifest.jsonl').read_text().splitlines()]
    old={r['id']:r for r in records};todo=[r for r in records if not (ROOT/r.get('pdf_path','missing')).is_file() or (args.retry and r.get('partial'))]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for result in pool.map(download_one,todo):old[result['id']].update(result);print(result['status'],result['url'],flush=True)
    (ROOT/'manifest.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in old.values()))
    print('Finished. The saved HTML index reflects the original package; consult manifest.jsonl for retry results.')
if __name__=='__main__':main()
