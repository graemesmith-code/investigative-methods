"""Retrieve selected public originals and compare their SHA-256 with the pilot.

Sequential requests; no credentials. A changed source is retained separately and
reported, never silently accepted as the evidence used by the pilot.
"""
import argparse,datetime,hashlib,json,sys,urllib.parse,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'research/2026-10-12/peru-production-pilot'
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--id',action='append',required=True,help='Source ID from source-manifest.json; repeat to select more')
    ap.add_argument('--output',type=Path,required=True,help='Local source cache, outside committed report files')
    ap.add_argument('--user-agent',required=True,help='Identify your project and a real contact; respect source access rules')
    ap.add_argument('--manifest',type=Path,default=DATA/'source-manifest.json',help='Reviewed source manifest; accepts followup-source-manifest.json')
    a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    manifest=json.loads(a.manifest.read_text());lookup={s['id']:s for s in manifest}
    unknown=set(a.id)-set(lookup)
    if unknown:ap.error('Unknown source IDs: '+', '.join(sorted(unknown)))
    bad=False
    for source_id in a.id:
        s=lookup[source_id]
        if Path(source_id).name!=source_id:raise ValueError('Unsafe source filename')
        result={'id':source_id,'url':s['url'],'tested_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
        try:
            fields=s.get('request_fields')
            if s.get('method')=='POST' and not fields:raise ValueError('POST source lacks saved request fields')
            headers={'User-Agent':a.user_agent}
            if fields and s.get('request_encoding')=='json':
                body=json.dumps(fields).encode();headers['Content-Type']='application/json'
            else:body=urllib.parse.urlencode(fields).encode() if fields else None
            req=urllib.request.Request(s['url'],data=body,headers=headers)
            with urllib.request.urlopen(req,timeout=45) as response:payload=response.read();result['status']=response.status
            sha=hashlib.sha256(payload).hexdigest();match=sha==s.get('sha256')
            dest=a.output/(source_id if match else source_id+'.changed-'+sha[:12])
            dest.write_bytes(payload);result.update(bytes=len(payload),sha256=sha,expected_sha256=s.get('sha256'),hash_matches_pilot=match,saved_as=str(dest))
            bad=bad or not match
        except Exception as exc:result['error']=str(exc);bad=True
        with (a.output/'replay-log.jsonl').open('a') as f:f.write(json.dumps(result)+'\n')
        print(json.dumps(result))
    return int(bad)
if __name__=='__main__':sys.exit(main())
