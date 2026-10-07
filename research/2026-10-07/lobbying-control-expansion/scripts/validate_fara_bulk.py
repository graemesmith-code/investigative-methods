"""Validate official FARA CSVs or CSV ZIPs without extracting archive paths.

Usage: python validate_fara_bulk.py DIRECTORY
No download is attempted: the official routes returned 403 in this executor.
This can validate the exact official downloads once access is restored.
"""
import pathlib,zipfile,csv,io,json,hashlib,sys,collections
KINDS=('Registrants','ForeignPrincipals','RegistrantDocs')
def validate(root):
    results=[]
    for kind in KINDS:
        path=root/f'FARA_All_{kind}.csv.zip'
        direct=root/f'FARA_All_{kind}.csv'
        if direct.exists():
            raw=direct.read_bytes();reader=csv.reader(io.StringIO(raw.decode('iso-8859-1')));fields=next(reader);rows=list(reader)
            bad=[i+1 for i,r in enumerate(rows) if len(r)!=len(fields)]
            results.append({'dataset':kind,'status':'direct CSV inspected; malformed records require explicit repair before joins' if bad else 'direct CSV structurally valid','sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'fields':fields,'rows':len(rows),'malformed_width_record_numbers':bad,'raw_bytes_preserved':True})
            continue
        if not path.exists():
            results.append({'dataset':kind,'status':'not materialized'});continue
        raw=path.read_bytes()
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            assert sum(x.file_size for x in z.infolist())<250_000_000,'Uncompressed safety limit'
            assert z.testzip() is None,'ZIP CRC failure'
            members=[x for x in z.infolist() if x.filename.lower().endswith('.csv')]
            assert len(members)==1,'Unexpected CSV topology'
            body=z.read(members[0]).decode('iso-8859-1')
            reader=csv.DictReader(io.StringIO(body));rows=list(reader)
            assert rows and reader.fieldnames and len(set(reader.fieldnames))==len(reader.fieldnames)
            assert all(None not in r for r in rows),'Ragged CSV row'
            normalized={x:''.join(c for c in x.lower() if c.isalnum()) for x in reader.fieldnames}
            reg=next((x for x,n in normalized.items() if n in ('registrationnumber','registrationno')),None)
            urls=[v for r in rows for v in r.values() if isinstance(v,str) and v.startswith(('https://','http://'))]
            results.append({'dataset':kind,'status':'validated local CSV; completeness still requires snapshot reconciliation','zip_sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'member':members[0].filename,'fields':reader.fieldnames,'rows':len(rows),'distinct_registration_numbers':len({r[reg] for r in rows}) if reg else None,'url_values':len(urls),'distinct_url_values':len(set(urls)),'exact_duplicate_rows':sum(n-1 for n in collections.Counter(tuple(r.items()) for r in rows).values()),'raw_rows_preserved':True})
    return results
if __name__=='__main__':print(json.dumps(validate(pathlib.Path(sys.argv[1])),indent=2))
