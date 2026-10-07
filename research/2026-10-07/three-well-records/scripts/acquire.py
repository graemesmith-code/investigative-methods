import pathlib, json, hashlib, datetime, urllib.request, urllib.error
ROOT=pathlib.Path(__file__).resolve().parents[1]
def fetch(name,url,limit=150_000_000):
    path=ROOT/'sources'/name
    if path.exists(): return path
    rec={'name':name,'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'limit_bytes':limit,'tls_verification':True}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Public-record-research/1.0'})
        with urllib.request.urlopen(req,timeout=90) as r:
            data=r.read(limit+1); rec.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'))
            if len(data)>limit: raise ValueError('Scoped size limit exceeded')
        path.write_bytes(data);rec.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    except Exception as e:
        rec.update(error_type=type(e).__name__,error=str(e))
        if isinstance(e,urllib.error.HTTPError):
            data=e.read(1000000); ep=ROOT/'sources'/(name+'.error.txt');ep.write_bytes(data);rec.update(status=e.code,error_body_file=ep.name,error_body_sha256=hashlib.sha256(data).hexdigest())
        path=None
    with (ROOT/'sources/manifest.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
    print(json.dumps(rec),flush=True)
    return path
if __name__=='__main__':
    import sys
    fetch(sys.argv[1],sys.argv[2])
