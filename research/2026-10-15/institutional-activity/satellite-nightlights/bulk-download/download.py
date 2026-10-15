#!/usr/bin/env python3
"""Fetch only the 18 listed NASA science files, then create three upload ZIPs.
Run this on your own computer. Python 3 and curl are required; no pip install.
The token is read through a hidden prompt and passed to curl on stdin only.
"""
import argparse, datetime as dt, getpass, hashlib, json, pathlib, re
import shutil, subprocess, sys, zipfile
from urllib.parse import urlparse
ROOT = pathlib.Path(__file__).resolve().parent
HDF5 = b'\x89HDF\r\n\x1a\n'
EVENTS = {'iran_june_2025', 'venezuela_jan_2026', 'iran_feb_2026'}


def validate_manifest(items):
    if len(items) != 18:
        raise ValueError('Expected the fixed 18-file first-stage manifest.')
    seen = set()
    for m in items:
        name = m['filename']; u = urlparse(m['download_url'])
        if not re.fullmatch(r'VNP46A[12]\.A\d{7}\.h10v05\.002\.\d{13}\.h5', name):
            raise ValueError('Unexpected science filename.')
        if u.scheme != 'https' or u.hostname != 'data.laadsdaac.earthdatacloud.nasa.gov' or u.port not in (None,443) or u.username or u.password or u.query or u.fragment:
            raise ValueError('Unexpected NASA download origin.')
        if u.path != '/prod-lads/' + m['product'] + '/' + name:
            raise ValueError('URL does not match the listed file.')
        if m['event'] not in EVENTS or m['product'] not in ('VNP46A1','VNP46A2'):
            raise ValueError('Unexpected event or product.')
        if not 0 < m['size_mib'] < 100 or name in seen:
            raise ValueError('Unexpected size or duplicate file.')
        seen.add(name)


def inspect_file(path, item):
    count = path.stat().st_size
    expected = round(item['size_mib'] * 1024 * 1024)
    # NASA's catalog sizes retain fractional MiB. Allow rounding, not truncation.
    if abs(count - expected) > 1024:
        raise ValueError('File size differs from the catalog; download is incomplete or changed.')
    digest = hashlib.sha256()
    with path.open('rb') as f:
        first = f.read(8)
        if first != HDF5:
            raise ValueError('NASA returned a page or unsupported file instead of HDF5 data.')
        digest.update(first)
        while True:
            block = f.read(1024*1024)
            if not block: break
            digest.update(block)
    return {'filename': item['filename'], 'event':item['event'], 'bytes':count,
            'sha256':digest.hexdigest()}


def curl_arguments(curl, item, part):
    return [curl, '--fail', '--silent', '--show-error', '--location',
            '--proto', '=https', '--proto-redir', '=https', '--max-redirs', '8',
            '--connect-timeout', '20', '--max-time', '600', '--cookie', '',
            '--max-filesize', str(round(item['size_mib']*1024*1024)+1024),
            '--output', str(part), '--config', '-', item['download_url']]


def make_archives(items, receipts, raw, output):
    output.mkdir(exist_ok=True)
    paths = []
    for event in sorted(EVENTS):
        selected = [m for m in items if m['event'] == event]
        if not selected: continue
        dest = output / (event + '.zip')
        part = dest.with_suffix('.zip.part')
        with zipfile.ZipFile(part, 'w', compression=zipfile.ZIP_STORED, allowZip64=True) as z:
            z.writestr('manifest.json', json.dumps(selected,indent=2))
            z.writestr('download_receipts.json', json.dumps([r for r in receipts if r['event']==event],indent=2))
            z.writestr('README.txt','NASA VNP46A1/A2 Collection 2 science files. First-stage observation sample only. No baselines or brightness results. No token is stored in this ZIP.\n')
            for m in selected: z.write(raw/m['filename'],arcname=m['filename'])
        part.replace(dest)
        paths.append(dest)
    return paths


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list',action='store_true',help='Show the plan without a token or network request')
    parser.add_argument('--pair',action='store_true',help='Only the initial June 20 matched pair (~67 MiB)')
    args=parser.parse_args()
    items=json.loads((ROOT/'download_manifest.json').read_text())
    validate_manifest(items)
    if args.pair:items=[m for m in items if m['observation_date_utc']=='2025-06-20']
    # Test the schema-check pair first; only proceed after each validates.
    items.sort(key=lambda m:(m['observation_date_utc']!='2025-06-20',m['event'],m['filename']))
    print(f'{len(items)} exact NASA files, approximately {sum(m["size_mib"] for m in items):.1f} MiB.')
    print('No baseline data or extra satellite tiles will be downloaded.')
    if args.list:
        for m in items:print(m['event'],m['filename'])
        return
    curl=shutil.which('curl')
    if not curl:raise ValueError('curl is required. macOS normally includes it.')
    raw=ROOT/'science_files';raw.mkdir(exist_ok=True)
    receipts=[];pending=[]
    for item in items:
        dest=raw/item['filename']
        if dest.exists():
            receipt=inspect_file(dest,item)
            receipt['verification_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
            receipts.append(receipt);print('Reusing verified file:',dest.name)
        else:pending.append(item)
    token=''
    if pending:
        if not sys.stdin.isatty():raise ValueError('Run in Terminal so the token can be entered privately.')
        token=getpass.getpass('Paste NASA Earthdata download token (hidden), then press Return: ').strip()
        if not re.fullmatch(r'[A-Za-z0-9._~+\-/=]+',token):
            raise ValueError('Token is empty or contains unexpected characters. Paste the token only.')
    for n,item in enumerate(pending,1):
        print(f'Downloading {n}/{len(pending)}: {item["filename"]}',flush=True)
        dest=raw/item['filename'];part=dest.with_suffix('.h5.part')
        if part.exists():part.unlink()  # only this script's unfinished scratch file
        command=curl_arguments(curl,item,part)
        started=dt.datetime.now(dt.timezone.utc).isoformat()
        # No shell, no token argument, no token file, no verbose/auth headers in logs.
        config='header = "Authorization: Bearer '+token+'"\n'
        result=subprocess.run(command,input=config.encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        config=''
        if result.returncode:
            if part.exists():part.unlink()
            if result.returncode==22:msg='NASA rejected a request. Check token validity and authorized app access in Earthdata.'
            elif result.returncode in (28,6,7):msg='Network connection failed or timed out. Re-run to reuse finished files.'
            else:msg=f'curl stopped (code {result.returncode}). No response headers or signed URLs were printed.'
            raise ValueError(msg)
        receipt=inspect_file(part,item)
        receipt['retrieval_started_utc']=started
        receipt['retrieval_finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
        part.replace(dest);receipts.append(receipt)
        (ROOT/'download_receipts.json').write_text(json.dumps(receipts,indent=2))
    token=''
    paths=make_archives(items,receipts,raw,ROOT/'UPLOAD_THESE')
    print('\nFinished. Upload these ZIP files to the conversation:')
    for p in paths:print(p)
    print('Your token was not saved. These files establish first-stage coverage, not a completed backtest.')

if __name__=='__main__':
    try:main()
    except KeyboardInterrupt:print('\nStopped. Re-run to reuse completed files.');sys.exit(130)
    except (ValueError,OSError) as e:print('Stopped:',str(e),file=sys.stderr);sys.exit(1)
