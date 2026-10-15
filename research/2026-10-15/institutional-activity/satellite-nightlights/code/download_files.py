#!/usr/bin/env python3
"""Download exact public NASA files after authorized Earthdata login.
Default: one A1/A2 pair (~67 MiB). --all: 18 files (~561 MiB).
Not yet exercised against an authenticated NASA download.
"""
import argparse, datetime as dt, getpass, hashlib, json, pathlib, sys
import urllib.request, urllib.parse, urllib.error
ROOT=pathlib.Path(__file__).resolve().parents[1]
HDF5=b'\x89HDF\r\n\x1a\n'
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        # Never forward a bearer credential to another origin or signed URL.
        return None

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--all',action='store_true')
    p.add_argument('--list',action='store_true',help='List planned files without asking for a token')
    args=p.parse_args()
    items=json.loads((ROOT/'download_manifest.json').read_text())
    if not args.all:items=[m for m in items if m['observation_date_utc']=='2025-06-20']
    print(f'{len(items)} files; catalog size {sum(m["size_mib"] for m in items):.1f} MiB')
    if args.list:
        for m in items:print(m['filename'])
        return
    raw=ROOT/'raw';raw.mkdir(exist_ok=True)
    token=getpass.getpass('Earthdata download token (hidden; never saved): ').strip()
    if not token:raise SystemExit('No token entered. No download attempted.')
    opener=urllib.request.build_opener(NoRedirect)
    for m in items:
        url=m['download_url'];u=urllib.parse.urlparse(url)
        if u.scheme!='https' or u.hostname!='data.laadsdaac.earthdatacloud.nasa.gov':
            raise SystemExit('Unexpected download origin in manifest.')
        dest=raw/m['filename']
        if dest.exists():
            raise SystemExit(f'{dest.name} already exists; inspect it before restarting to avoid overwriting evidence.')
        tmp=dest.with_suffix('.part')
        if tmp.exists():raise SystemExit(f'Partial file {tmp.name} exists; inspect before restarting.')
        req=urllib.request.Request(url,headers={'Authorization':'Bearer '+token})
        started=dt.datetime.now(dt.timezone.utc).isoformat()
        try:
            with opener.open(req,timeout=60) as r, tmp.open('xb') as f:
                first=r.read(8)
                if first!=HDF5:raise ValueError('Response is not a supported HDF5 science file.')
                f.write(first);digest=hashlib.sha256(first);count=8
                while True:
                    b=r.read(1024*1024)
                    if not b:break
                    count+=len(b)
                    if count>128*1024*1024:raise ValueError('Unexpected file size; stopped at 128 MiB limit.')
                    f.write(b);digest.update(b)
            # A large short transfer should be reviewed, not accepted as complete.
            expected=m['size_mib']*1024*1024
            if abs(count-expected)>1024*1024:raise ValueError('Downloaded size differs materially from catalog size.')
            tmp.rename(dest)
            record={'filename':dest.name,'bytes':count,'sha256':digest.hexdigest(),'retrieval_started_utc':started,'retrieval_finished_utc':dt.datetime.now(dt.timezone.utc).isoformat()}
            with (ROOT/'download_receipts.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
            print('Downloaded',dest.name,count,'bytes')
        except urllib.error.HTTPError as e:
            # Do not log response bodies, headers or redirect query strings.
            raise SystemExit(f'NASA returned HTTP {e.code}; stopped. Use NASA login/download instructions. No redirect was followed.') from None
    token=None
if __name__=='__main__':main()
