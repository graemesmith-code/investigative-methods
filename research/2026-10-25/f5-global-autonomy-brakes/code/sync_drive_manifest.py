#!/usr/bin/env python3
"""Build a complete compact Drive pointer manifest from verified native receipts.

Does not authenticate, upload, alter permissions, or infer successful writes.
Receipts must be produced after native Drive metadata + byte readback. Bundle
inventories preserve all members when large raw snapshots are grouped on Drive.
"""
import argparse, hashlib, json
from pathlib import Path
def build(receipts, output):
    objects=[]; seen=set()
    for receipt in receipts:
        r=json.loads(Path(receipt).read_text())
        for x in r if isinstance(r,list) else [r]:
            required=['filename','drive_file_id','drive_view_url','bytes','row_count','sha256','readback_sha256','readback_bytes','owner_email','anyone_reader']
            missing=[k for k in required if k not in x]
            if missing: raise ValueError('Receipt lacks '+str(missing))
            if x['drive_file_id'] in seen: raise ValueError('Duplicate Drive object')
            seen.add(x['drive_file_id'])
            if x['sha256']!=x['readback_sha256'] or x['bytes']!=x['readback_bytes']: raise ValueError('Readback mismatch')
            if x['owner_email']!='smithg@gmail.com' or x['anyone_reader'] is not True: raise ValueError('Unverified required ownership/sharing')
            if not x['drive_view_url'].startswith('https://drive.google.com/'): raise ValueError('Not a Drive view URL')
            objects.append(x)
    manifest={'schema':'F5-drive-manifest-v1','folder_url':'https://drive.google.com/drive/folders/1JjNctZzLVUzuu0K469FS0cutxsZ4K1sS','scope':'Every F5 uploaded object, including checkpoints; grouped snapshots have complete member inventories inside their bundles. Null row count means non-tabular. Hashes cover exact bytes, not displayed previews.','objects':objects}
    data=(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n').encode()
    if len(data)>100000: raise ValueError('Manifest exceeds GitHub file limit; bundle raw objects with complete inventories')
    Path(output).write_bytes(data)
    return {'objects':len(objects),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('receipts',nargs='+');p.add_argument('--output',required=True);a=p.parse_args();print(json.dumps(build(a.receipts,a.output)))
