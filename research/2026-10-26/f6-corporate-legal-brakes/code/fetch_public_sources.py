#!/usr/bin/env python3
"""Single-attempt free public GET queue; source bytes stay in private storage.

Input JSONL: document_id, source_url and optional expected_source_sha256.
No accounts, cookies, POSTs, licence acceptance, retries or paid services.
An HTTP/body failure is an access observation, never evidence of source absence.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import datetime,hashlib,ipaddress,json,subprocess,time
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlparse,parse_qsl
from urllib.request import urlopen

class AllVisibleText(HTMLParser):
    def __init__(self):super().__init__();self.hidden=0;self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag in ['script','style']:self.hidden+=1
        if not self.hidden:self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in ['script','style'] and self.hidden:self.hidden-=1
        if not self.hidden:self.parts.append('\n')
    def handle_data(self,data):
        if not self.hidden:self.parts.append(data)

def acquire(row,private_dir,max_bytes):
    doc=row['document_id'];url=row['source_url'];parsed=urlparse(url)
    sensitive_keys={'access_token','token','api_key','apikey','sig','signature',
                    'x-amz-signature','x-amz-credential','x-goog-signature'}
    signed_or_secret=any(k.lower() in sensitive_keys for k,v in parse_qsl(parsed.query))
    base={'document_id':doc,'source_url':url,
          'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'attempts':1,'paid_cost_usd':'0','status':'started'}
    if signed_or_secret:
        return {**base,'source_url':parsed._replace(query='',fragment='').geturl(),
                'status':'rejected_signed_or_credentialed_url','query_redacted':True}
    if parsed.scheme!='https' or parsed.username or parsed.password or not parsed.hostname:
        return {**base,'status':'rejected_nonpublic_request_shape'}
    if parsed.hostname=='localhost' or parsed.hostname.endswith(('.localhost','.local','.internal')):
        return {**base,'status':'rejected_nonpublic_address'}
    try:
        if ipaddress.ip_address(parsed.hostname).is_global is False:
            return {**base,'status':'rejected_nonpublic_address'}
    except ValueError:pass
    # IDs never become path components. A fixed digest isolates each request.
    token=hashlib.sha256((doc+'\n'+url).encode()).hexdigest()
    source=private_dir/(token+'.body');text=private_dir/(token+'.txt')
    if source.exists() or text.exists():
        return {**base,'status':'existing_snapshot_preserved_no_request','snapshot_token':token}
    try:
        with urlopen(url,timeout=45) as response:
            kind=response.headers.get('Content-Type','');charset=response.headers.get_content_charset() or 'utf-8'
            chunks=[];length=0
            while True:
                chunk=response.read(1024*1024)
                if not chunk:break
                length+=len(chunk)
                if length>max_bytes:raise ValueError('Declared source-byte bound exceeded')
                chunks.append(chunk)
            body=b''.join(chunks)
        source.write_bytes(body);digest=hashlib.sha256(body).hexdigest()
        expected=row.get('expected_source_sha256')
        if expected and expected!=digest:
            return {**base,'status':'source_hash_difference_review_required',
                    'source_sha256':digest,'source_bytes':len(body),'snapshot_token':token}
        if body.startswith(b'%PDF-'):
            subprocess.run(['pdftotext','-layout',str(source),str(text)],check=True,
                           timeout=60,capture_output=True)
            content=text.read_text(encoding='utf-8')
            pages=content.count('\f') or 1
            text_kind='pdftotext-layout; image/OCR validation pending'
        elif 'html' in kind.lower() or body.lstrip().lower().startswith((b'<!doctype html',b'<html')):
            parser=AllVisibleText();parser.feed(body.decode(charset,errors='replace'))
            content=''.join(parser.parts);text.write_text(content);pages=1
            text_kind='all visible HTML text including navigation; scripts/styles excluded'
            if len(content)<5000 and any(x in content.lower() for x in
                    ['access denied','just a moment','verify you are human','captcha']):
                return {**base,'status':'suspected_access_interstitial',
                        'source_sha256':digest,'source_bytes':len(body),'snapshot_token':token}
        elif kind.startswith('text/') or 'json' in kind:
            content=body.decode(charset,errors='strict');text.write_text(content);pages=1
            text_kind='complete decoded text body'
        else:
            return {**base,'status':'unsupported_body_retained_private','content_type':kind,
                    'source_sha256':digest,'source_bytes':len(body),'snapshot_token':token}
        return {**base,'status':'retrieved_extraction_unvalidated','content_type':kind,
                'source_sha256':digest,'source_bytes':len(body),
                'text_sha256':hashlib.sha256(content.encode()).hexdigest(),
                'text_units':pages,'extraction':text_kind,'snapshot_token':token,
                'full_text_completeness':'not_certified','public_copy_clearance':'not_assessed'}
    except HTTPError as e:return {**base,'status':'http_access_failure','http_status':e.code}
    except Exception as e:return {**base,'status':'request_or_extraction_failure','error_type':type(e).__name__}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('queue',type=Path);p.add_argument('private_dir',type=Path)
    p.add_argument('audit_jsonl',type=Path);p.add_argument('--workers',type=int,default=3)
    p.add_argument('--max-source-bytes',type=int,default=100000000);a=p.parse_args()
    if not 1<=a.workers<=4:raise ValueError('workers must be1–4')
    rows=[json.loads(l) for l in a.queue.read_text().splitlines() if l.strip()]
    a.private_dir.mkdir(parents=True,exist_ok=True);a.audit_jsonl.parent.mkdir(parents=True,exist_ok=True)
    with a.audit_jsonl.open('x') as audit,ThreadPoolExecutor(max_workers=a.workers) as pool:
        for result in pool.map(lambda r:acquire(r,a.private_dir,a.max_source_bytes),rows):
            audit.write(json.dumps(result)+'\n');audit.flush()
            print(json.dumps({'document_id':result['document_id'],'status':result['status']}),flush=True)
