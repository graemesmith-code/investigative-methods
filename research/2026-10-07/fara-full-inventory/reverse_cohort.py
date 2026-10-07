"""Source-defined expansion: every 2025 new FARA principal with a US state address.

Governments, individuals and intermediaries stay in the denominator. This is
not a corporate-only selection or a sample chosen by company reputation.
"""
import sqlite3,json,re,pathlib,urllib.parse,urllib.request,time,hashlib,datetime
P=pathlib.Path(__file__).resolve().parent;S=P/'sources';US=set('AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY'.split())
def selection():
    db=sqlite3.connect(P/'inventory.sqlite');rows=[json.loads(x[0]) for x in db.execute('SELECT payload FROM ForeignPrincipals')]
    out=[]
    for r in rows:
        if not r['Foreign Principal Registration Date'].endswith('/2025') or r['State'].strip() not in US:continue
        query=re.split(r'\s+on behalf of\s+',r['Foreign Principal'],flags=re.I)[0]
        query=re.sub(r',?\s+(?:inc\.?|corporation|corp\.?|llc|ltd\.?|limited)\s*$','',query,flags=re.I).strip()
        out.append({'principal_row':r['row'],'principal':r['Foreign Principal'],'registration_number':r['Registration Number'],'registered':r['Foreign Principal Registration Date'],'terminated':r['Foreign Principal Termination Date'],'state':r['State'],'query':query,'basis':'2025 principal registration and a valid US-state/DC address in supplied export; name-query absence is not proof of no LDA filing.'})
    (P/'reverse-cohort-selection.json').write_text(json.dumps(out,indent=2));return out
def fetch(name,url):
    path=S/name
    if path.exists():return path.read_bytes()
    rec={'name':name,'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(url,timeout=40) as r:body=r.read(20_000_001);rec.update(status=r.status,final_url=r.url)
        assert len(body)<=20_000_000
        path.write_bytes(body);rec.update(bytes=len(body),sha256=hashlib.sha256(body).hexdigest());return body
    except Exception as e:rec['error']=str(e);return None
    finally:
        with (P/'retrieval-ledger.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
def acquire():
    selected=selection();queries=list(dict.fromkeys(r['query'] for r in selected));out=[]
    for n,query in enumerate(queries,1):
        key=hashlib.sha256(query.encode()).hexdigest()[:16];url='https://lda.gov/api/v1/filings/?'+urllib.parse.urlencode({'filing_year':2025,'client_name':query,'page_size':25});rows=[];page=0;count=None
        while url and page<100:
            page+=1;t=time.monotonic();raw=fetch(f'lda-reverse-{key}-{page:03}.json',url)
            if raw is None:break
            data=json.loads(raw);count=data['count'];rows+=data['results'];url=data['next'];time.sleep(max(0,4.3-(time.monotonic()-t)))
        out.append({'query':query,'key':key,'count':len(rows),'server_count':count,'complete':url is None,'client_ids':sorted({r['client']['id'] for r in rows}),'uuids':[r['filing_uuid'] for r in rows]})
        (P/'reverse-query-coverage.json').write_text(json.dumps(out,indent=2));print(n,len(queries),query,len(rows),flush=True)
if __name__=='__main__':
    import sys
    if '--acquire' in sys.argv:acquire()
    else:
        rows=selection();print('selected principal relationships',len(rows),'unique literal search terms',len({r['query'] for r in rows}))
