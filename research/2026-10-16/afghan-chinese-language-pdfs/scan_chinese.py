"""Scan URL columns in Chinese-language FinePDFs partitions.

Checkpoints are per source file; elapsed time is recorded per invocation.
Signed download locations are never included in audit output.
"""
import concurrent.futures, hashlib, io, json, os, sys, threading, time
from pathlib import Path
from urllib.parse import urlsplit
import requests
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work'
STATE = WORK / 'states'
RECORDS = WORK / 'records'
STATE.mkdir(exist_ok=True)
RECORDS.mkdir(exist_ok=True)
inventory = json.loads((WORK/'source-parquet-inventory.json').read_text())
chinese_codes = {'cdo','cjy','cmn','cpx','czh','czo','gan','hak','hsn','lzh','mnp','nan','wuu','yue','zho'}
files = [f for f in inventory['parquet_files'] if f['config'].split('_')[0] in chinese_codes]
priority = ['cmn_Hani','rus_Cyrl','arb_Arab','urd_Arab','tur_Latn','tuk_Arab','tuk_Latn','uzn_Arab','uzn_Latn','uzn_Cyrl','fra_Latn','deu_Latn']
files.sort(key=lambda f:(priority.index(f['config']) if f['config'] in priority else len(priority), f['size']))
started = time.time()
lock = threading.Lock()
live = {}
finished = threading.Event()

def save(path, obj):
    temp=Path(str(path)+'.tmp')
    temp.write_text(json.dumps(obj,ensure_ascii=False,default=str))
    temp.replace(path)

class Remote(io.RawIOBase):
    def __init__(self, f):
        self.f=f; self.size=f['size']; self.pos=0; self.s=requests.Session(); self.direct=None
        self.bytes=0; self.calls=0; self.cache={}
    def readable(self): return True
    def seekable(self): return True
    def tell(self): return self.pos
    def seek(self,n,whence=0):
        self.pos=n if whence==0 else self.pos+n if whence==1 else self.size+n
        return self.pos
    def read(self,n=-1):
        if n<0: n=self.size-self.pos
        n=min(n,self.size-self.pos)
        if n<=0:return b''
        start=self.pos;end=start+n-1
        key=(start,n)
        if key in self.cache:
            self.pos+=n;return self.cache[key]
        for attempt in range(4):
            try:
                u=self.direct or self.f['url']
                if not self.direct and attempt: u += ('&' if '?' in u else '?')+'scan_retry='+str(int(time.time()))
                r=self.s.get(u,headers={'Range':f'bytes={start}-{end}'},timeout=(20,45))
                self.calls+=1
                if r.status_code==403:
                    self.direct=None;continue
                r.raise_for_status()
                b=r.content
                if r.status_code==200 and len(b)==self.size:b=b[start:end+1]
                elif r.status_code!=206:raise ValueError(f'Expected byte range; HTTP {r.status_code}')
                if len(b)!=n:raise ValueError(f'Unexpected response length: {len(b)} vs {n}')
                self.direct=r.url;self.bytes+=len(r.content);self.pos+=n
                if end==self.size-1:self.cache[key]=b
                return b
            except Exception as e:
                if attempt==3:raise RuntimeError(type(e).__name__) from None
                time.sleep(min(1+attempt,3))
        raise RuntimeError('Download authorization failed after refreshed public URLs')

def scan(f):
    key=f['config']+'--'+f['split']+'--'+f['filename'].replace('.parquet','')
    path=STATE/(key+'.json')
    s=json.loads(path.read_text()) if path.exists() else dict(file=f,groups_done=[],rows_checked=0,hits=[],errors=[])
    with lock: live[key]=s
    if s.get('complete'):return
    s['errors']=[]
    rf=Remote(f)
    try:
        p=pq.ParquetFile(rf)
        s['total_rows']=p.metadata.num_rows;s['total_groups']=p.metadata.num_row_groups
        done=set(s['groups_done'])
        for g in range(p.metadata.num_row_groups):
            if g in done:continue
            try:
                urls=p.read_row_group(g,columns=['url'])['url'].to_pylist()
                hits=[]
                for i,u in enumerate(urls):
                    lower=u.lower()
                    if '.af' not in lower and 'afghan' not in lower:continue
                    host=(urlsplit(u).hostname or '').lower()
                    if host.endswith('.af') or 'afghan' in host:
                        hits.append(dict(url=u,host=host,group=g,row_in_group=i))
                if hits:
                    table=p.read_row_group(g)
                    for h in hits:
                        row=table.slice(h['row_in_group'],1).to_pylist()[0]
                        record_key=hashlib.sha256((key+':'+str(g)+':'+str(h['row_in_group'])).encode()).hexdigest()[:24]
                        row['provenance']=dict(config=f['config'],split=f['split'],file=f['filename'],parquet_url=f['url'],group=g,row_in_group=h['row_in_group'])
                        row['host']=h['host'];row['record_key']=record_key;row['gov_af_domain']=(h['host']=='gov.af' or h['host'].endswith('.gov.af'))
                        save(RECORDS/(record_key+'.json'),row)
                        h['record_key']=record_key
                    s['hits'].extend(hits)
                    print('MATCH',key,g,[h['url'] for h in hits],flush=True)
                s['groups_done'].append(g);s['rows_checked']+=len(urls)
                if g%50==0 or hits:save(path,s)
            except Exception as e:
                s['errors'].append({'group':g,'error':type(e).__name__+': '+str(e)[:160]})
        s['complete']=len(s['groups_done'])==s['total_groups']
    except Exception as e:s['errors'].append({'stage':'file','error':type(e).__name__+': '+str(e)[:160]})
    s['bytes_this_attempt']=rf.bytes;s['requests_this_attempt']=rf.calls
    save(path,s)
    if s.get('errors'):print('FILE_ERRORS',key,len(s['errors']),flush=True)

def report():
    with lock: ss=list(live.values())
    r=dict(seconds_this_run=round(time.time()-started),files_targeted=len(files),files_started=len(ss),files_complete=sum(bool(s.get('complete')) for s in ss),rows_checked=sum(s.get('rows_checked',0) for s in ss),hits=sum(len(s.get('hits',[])) for s in ss),errors=sum(len(s.get('errors',[])) for s in ss))
    save(WORK/'progress.json',r)
    print('PROGRESS',json.dumps(r),flush=True)
    return r

def monitor():
    while not finished.wait(30):report()

save(WORK/'scope.json',dict(dataset='HuggingFaceFW/finepdfs',date='2026-10-16',configs=sorted({f['config'] for f in files}),files=len(files),hostname_rule='hostname == gov.af OR hostname.endswith(.gov.af)',included_language_prefixes=sorted(chinese_codes),additional_candidate_rule='Other .af domains and hosts containing afghan are retained for ownership review'))
threading.Thread(target=monitor,daemon=True).start()
with concurrent.futures.ThreadPoolExecutor(max_workers=24) as pool:
    list(pool.map(scan,files))
finished.set()
save(WORK/'summary.json',report())
