"""Download the five officially listed 2025 House LDA archives, bounded and hashed.

Links are taken unchanged from the downloaded official dropdown JSON, whose
base URL is published in the site's JavaScript. No guessed archive URLs.
"""
import json,pathlib,urllib.request,hashlib,zipfile,datetime,concurrent.futures
P=pathlib.Path(__file__).resolve().parent;S=P/'sources';LIMIT=60_000_000
def one(item):
    name=item['file'];assert name.startswith('2025_') and '/' not in name
    path=S/name;url='https://disclosurespreview.house.gov/data/LD/'+name
    result={'file':name,'url':url,'official_display_name':item['name'],'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        if not path.exists():
            part=path.with_suffix('.part');size=0
            with urllib.request.urlopen(url,timeout=90) as response,part.open('wb') as output:
                result.update(status=response.status,last_modified=response.headers.get('Last-Modified'))
                while True:
                    chunk=response.read(1024*1024)
                    if not chunk:break
                    size+=len(chunk);assert size<=LIMIT,'60 MB per-archive cap';output.write(chunk)
            part.rename(path)
        with zipfile.ZipFile(path) as archive:
            infos=archive.infolist();size=sum(i.file_size for i in infos);assert size<1_500_000_000,'uncompressed cap'
            assert archive.testzip() is None,'CRC failure'
            result.update(bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),members=len(infos),uncompressed_bytes=size,member_examples=[i.filename for i in infos[:3]],crc_verified=True)
        return result
    except Exception as e:result['error']=str(e);return result
def run():
    listing=json.loads((S/'house-ld-archives.json').read_text());selected=[x for x in listing if x['file'].startswith('2025_')];assert len(selected)==5
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for r in pool.map(one,selected):
            results.append(r);(P/'house-archive-downloads.json').write_text(json.dumps(results,indent=2));print(json.dumps(r),flush=True)
if __name__=='__main__':run()
