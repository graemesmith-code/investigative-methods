"""Verify fixed-catalog archives, extract science files, record schema (not values)."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile
import h5py
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def plain(x):
    if isinstance(x, bytes): return x.decode('utf-8')
    if isinstance(x, np.ndarray): return [plain(v) for v in x.tolist()] if x.ndim else plain(x.item())
    if isinstance(x, np.generic): return plain(x.item())
    if isinstance(x, (list, tuple)): return [plain(v) for v in x]
    return x

def main(paths):
    fixed = {r['filename']: r for r in json.loads((ROOT/'download_manifest.json').read_text())}
    (ROOT/'raw').mkdir(exist_ok=True)
    verified, schemas, seen = [], {}, set()
    for path in map(Path, paths):
        with zipfile.ZipFile(path) as z:
            manifest = json.loads(z.read('manifest.json'))
            receipts = json.loads(z.read('download_receipts.json'))
            events = {m['event'] for m in manifest}
            assert len(events) == 1
            event = events.pop()
            assert event not in seen, 'Duplicate event archive'
            seen.add(event)
            expected = {n for n,r in fixed.items() if r['event'] == event}
            assert len(expected) == len(manifest) == len(receipts) == 6
            assert {m['filename'] for m in manifest} == expected
            assert {r['filename'] for r in receipts} == expected
            assert set(z.namelist()) == expected | {'manifest.json','download_receipts.json','README.txt'}
            assert len(z.namelist()) == 9
            rec = {r['filename']:r for r in receipts}
            files=[]
            for m in manifest:
                n=m['filename']
                assert m == fixed[n], f'Catalog mismatch: {n}'
                data=z.read(n)  # ZIP CRC checked by zipfile
                assert data[:8] == b'\x89HDF\r\n\x1a\n'
                digest=sha(data)
                assert rec[n]['bytes'] == len(data) and rec[n]['sha256'] == digest
                assert rec[n]['event'] == event
                assert abs(len(data)-m['size_mib']*2**20) <= 1024
                dest=ROOT/'raw'/n
                if dest.exists(): assert sha(dest.read_bytes()) == digest
                else: dest.write_bytes(data)
                with h5py.File(dest) as f:
                    schema={'root_attrs':{k:plain(v) for k,v in f.attrs.items()},'datasets':{}}
                    def visit(name,obj):
                        if isinstance(obj,h5py.Dataset):
                            schema['datasets'][name]={'shape':list(obj.shape),'dtype':str(obj.dtype),'attrs':{k:plain(v) for k,v in obj.attrs.items()}}
                    f.visititems(visit)
                    schemas[n]=schema
                files.append({'filename':n,'bytes':len(data),'sha256':digest})
            verified.append({'event':event,'archive_name':path.name,'archive_bytes':path.stat().st_size,'archive_sha256':sha(path.read_bytes()),'files':files,'manifest':manifest,'download_receipts':receipts})
            print(f'{event}: six science files passed catalog, receipt hash, size, ZIP CRC and HDF5 checks')
    (ROOT/'evidence').mkdir(exist_ok=True)
    (ROOT/'evidence/verified_uploads.json').write_text(json.dumps(verified,indent=2)+'\n')
    (ROOT/'evidence/science_schema.json').write_text(json.dumps(schemas,indent=2)+'\n')

if __name__ == '__main__': main(sys.argv[1:])
