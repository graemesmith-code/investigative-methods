"""Offline, byte-preserving validation of user-supplied official FARA CSV exports.

CSV logical records may span physical lines. Fifteen malformed-width principal
records can be recovered with the export's literal quoted-field separator;
every such intervention retains raw text, both parses, and physical locators.
No row is silently dropped or deduplicated. Database IDs are local locators,
not invented official principal identifiers.
"""
import csv,io,json,pathlib,collections,datetime,hashlib,subprocess,sqlite3,re
P=pathlib.Path(__file__).resolve().parent
COMMIT='8557d0d9c6b8c1effe2d53e8b95d2425cb6d0e5f'
KINDS=('Registrants','ForeignPrincipals','RegistrantDocs')
def date(v):
    return datetime.datetime.strptime(v,'%m/%d/%Y').date().isoformat() if v else None
def read(kind):
    f=P/'sources'/f'FARA_All_{kind}.csv';raw=f.read_bytes()
    # Official documentation specifies latin-1. Keep C1 bytes losslessly; report
    # the compatible Windows-1252 display convention separately, not as proof.
    text=raw.decode('iso-8859-1');lines=io.StringIO(text).readlines()
    reader=csv.reader(io.StringIO(text));header=next(reader);end=reader.line_num
    records=[];repairs=[];parse_differences=[]
    for n,fields in enumerate(reader,1):
        start=end+1;end=reader.line_num;fragment=''.join(lines[start-1:end]).rstrip('\r\n')
        alternate=fragment[1:-1].split('\",\"') if fragment.startswith('"') and fragment.endswith('"') else []
        if len(fields)!=len(header):
            assert kind=='ForeignPrincipals' and len(alternate)==len(header),(kind,n,'unresolved width')
            assert alternate[4].isdigit();date(alternate[2]);date(alternate[5]);date(alternate[0])
            repairs.append({'row':n,'physical_lines':[start,end],'raw':fragment,'standard_fields':fields,'recovered_fields':alternate,'basis':'Literal quoted-field separators yield expected columns; registration number and all date positions validate. Raw source retained.'})
            fields=alternate
        elif len(alternate)==len(header) and fields!=alternate:
            parse_differences.append({'row':n,'physical_lines':[start,end],'raw':fragment,'standard_fields':fields,'literal_separator_fields':alternate,'interpretation':'Possible quoted-name rendering difference; standard CSV retained. Consult original for exact entity identity.'})
        records.append({'row':n,'line_start':start,'line_end':end,**dict(zip(header,fields))})
    return raw,header,records,repairs,parse_differences
def run():
    db=sqlite3.connect(P/'inventory.sqlite');db.execute('PRAGMA journal_mode=DELETE')
    summaries=[];allrows={};audit=[]
    for kind in KINDS:
        raw,header,rows,repairs,differences=read(kind);allrows[kind]=rows
        sha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        expected=subprocess.check_output(['git','rev-parse',f'{COMMIT}:research/FARA_All_{kind}.csv'],text=True).strip();assert sha==expected
        dates={}
        for col in header:
            if 'Date' in col:
                valid=[];invalid=[];implausible=[]
                for row in rows:
                    try:
                        value=date(row[col])
                        if value:
                            valid.append(value)
                            if value<'1938-01-01' or value>'2026-10-07':implausible.append({'row':row['row'],'value':row[col]})
                    except ValueError:invalid.append({'row':row['row'],'value':row[col]})
                dates[col]={'nonempty_valid':len(valid),'min':min(valid) if valid else None,'max':max(valid) if valid else None,'invalid':invalid,'implausible':implausible}
        duplicate=collections.Counter(tuple(r[h] for h in header) for r in rows)
        statuscol='Termination Date' if kind=='Registrants' else 'Foreign Principal Termination Date' if kind=='ForeignPrincipals' else None
        summary={'dataset':kind,'source_commit':COMMIT,'source_path':f'research/FARA_All_{kind}.csv','git_blob_sha1_verified':sha,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'declared_encoding':'iso-8859-1','rows':len(rows),'columns':header,'exact_duplicate_rows_retained':sum(n-1 for n in duplicate.values()),'malformed_width_rows_recovered':len(repairs),'other_quote_parse_differences_flagged':len(differences),'date_coverage':dates,'nonterminated_rows':sum(not r[statuscol] for r in rows) if statuscol else None,'terminated_rows':sum(bool(r[statuscol]) for r in rows) if statuscol else None,'provenance_limitation':'User-supplied official export preserved byte-for-byte from GitHub. Publication timestamp and direct DOJ checksum unavailable; current nonterminated status is not historical status.'}
        summaries.append(summary);audit.append({'dataset':kind,'repairs':repairs,'other_parse_differences':differences})
        db.execute(f'DROP TABLE IF EXISTS {kind}');db.execute(f'CREATE TABLE {kind}(row_id INTEGER PRIMARY KEY,registration_number TEXT,principal TEXT,stamp TEXT,kind TEXT,url TEXT,payload TEXT)')
        db.executemany(f'INSERT INTO {kind} VALUES(?,?,?,?,?,?,?)',[(r['row'],r['Registration Number'],r.get('Foreign Principal',r.get('Foreign Principal Name','')),r.get('Date Stamped',r.get('Foreign Principal Registration Date',r.get('Registration Date'))),r.get('Document Type',''),r.get('URL',''),json.dumps(r,ensure_ascii=True)) for r in rows])
        db.execute(f'CREATE INDEX idx_{kind}_reg ON {kind}(registration_number)')
    regs=allrows['Registrants'];fp=allrows['ForeignPrincipals'];docs=allrows['RegistrantDocs'];ids={r['Registration Number'] for r in regs}
    relation={'unique_registration_numbers':len(ids),'duplicate_registration_rows':[r for r in regs if sum(x['Registration Number']==r['Registration Number'] for x in regs)>1],'principal_registration_numbers_missing_from_registrants':sorted({r['Registration Number'] for r in fp}-ids),'document_registration_numbers_missing_from_registrants':sorted({r['Registration Number'] for r in docs}-ids),'principal_rows_with_no_official_principal_id_column':len(fp),'distinct_document_urls':len({r['URL'] for r in docs}),'document_types':dict(collections.Counter(r['Document Type'] for r in docs)),'registrants_with_no_document_row':len(ids-{r['Registration Number'] for r in docs}),'registrants_with_no_principal_row':len(ids-{r['Registration Number'] for r in fp}),'document_2025_rows':sum(r['Date Stamped'].endswith('/2025') for r in docs),'non_downloadable_url_values':dict(collections.Counter(r['URL'] for r in docs if not re.fullmatch(r'https://efile\.fara\.gov/docs/[^/]+\.pdf',r['URL'])))}
    db.commit();db.close()
    for name,data in [('supplied-source-provenance.json',summaries),('csv-parse-audit.json',audit),('inventory-relations.json',relation)]:
        (P/name).write_text(json.dumps(data,indent=2))
    print(json.dumps({'datasets':[{k:s[k] for k in ['dataset','rows','nonterminated_rows','terminated_rows','malformed_width_rows_recovered','other_quote_parse_differences_flagged']} for s in summaries],'relations':{k:v for k,v in relation.items() if k!='duplicate_registration_rows'}}))
if __name__=='__main__':run()
