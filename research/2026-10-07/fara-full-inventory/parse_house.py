"""Parse every supplied official 2025 House XML archive member without extraction.

Amounts are discovery inputs. Latest signing time is a provisional version order,
not a substitute for checking the unified API's filing chronology and originals.
"""
import pathlib,json,zipfile,xml.etree.ElementTree as ET,sqlite3,collections,hashlib,datetime,re
P=pathlib.Path(__file__).resolve().parent
def signed(value):
    for fmt in ('%m/%d/%Y %I:%M:%S %p','%m/%d/%Y','%Y-%m-%dT%H:%M:%S'):
        try:return datetime.datetime.strptime(value,fmt).isoformat()
        except ValueError:pass
    return None
def run():
    db=sqlite3.connect(P/'house-filings.sqlite');db.execute('PRAGMA journal_mode=DELETE');db.execute('DROP TABLE IF EXISTS filings')
    db.execute('CREATE TABLE filings(docid TEXT PRIMARY KEY,archive TEXT,member TEXT,sha256 TEXT,house_id TEXT,senate_id TEXT,client TEXT,registrant TEXT,year TEXT,quarter TEXT,report_type TEXT,signed TEXT,income TEXT,expenses TEXT,self_select TEXT,payload TEXT)')
    coverage=[];failures=[];repairs=[];types=collections.Counter();allids=set()
    for item in json.loads((P/'house-archive-downloads.json').read_text()):
        assert item.get('crc_verified');archive=P/'sources'/item['file'];q=next((str(n) for n,word in [(1,'1st'),(2,'2nd'),(3,'3rd'),(4,'4th')] if word in archive.name),'registration');count=0;bad_dates=0
        with zipfile.ZipFile(archive) as z:
            for info in z.infolist():
                try:
                    assert info.filename.endswith('.xml') and info.file_size<4_000_000
                    raw=z.read(info);assert b'<!DOCTYPE' not in raw.upper() and b'<!ENTITY' not in raw.upper()
                    try:root=ET.fromstring(raw)
                    except ET.ParseError:
                        changes=[]
                        def preserve_reference(m):
                            code=int(m.group(1)[1:],16) if m.group(1).startswith(b'x') else int(m.group(1))
                            valid=code in (9,10,13) or 32<=code<=0xD7FF or 0xE000<=code<=0xFFFD or 0x10000<=code<=0x10FFFF
                            if valid:return m.group(0)
                            changes.append(m.group(0).decode());return b'&amp;'+m.group(0)[1:]
                        recovered=re.sub(rb'&#(x[0-9A-Fa-f]+|[0-9]+);',preserve_reference,raw)
                        assert changes,'Unresolved XML syntax error';root=ET.fromstring(recovered)
                        repairs.append({'archive':archive.name,'member':info.filename,'original_sha256':hashlib.sha256(raw).hexdigest(),'invalid_references_preserved_as_literal_text':changes,'raw_original_unchanged':True})
                    assert root.tag in ('LOBBYINGDISCLOSURE1','LOBBYINGDISCLOSURE2')
                    fields={c.tag:(c.text or '').strip() for c in root if not list(c)}
                    fields['foreign_entities']=[{c.tag:(c.text or '').strip() for c in entity} for entity in root.findall('.//foreignEntity') if any((c.text or '').strip() for c in entity)]
                    fields['affiliated_organizations']=[{c.tag:(c.text or '').strip() for c in entity} for entity in root.findall('.//affiliatedOrg') if (entity.findtext('affiliatedOrgName') or '').strip()]
                    fields['foreign_interest_narratives']=[(e.text or '').strip() for e in root.findall('.//foreign_entity_issues') if (e.text or '').strip()]
                    fields['removed_foreign_entities']=[(e.text or '').strip() for e in root.findall('.//inactive_ForeignEntity') if (e.text or '').strip()]
                    fields['specific_issue_text']=[(e.text or '').strip() for e in root.findall('.//description') if (e.text or '').strip()]
                    docid=pathlib.PurePosixPath(info.filename).stem;stamp=signed(fields.get('signedDate',''));bad_dates+=stamp is None;types[fields.get('reportType','')]+=1
                    assert docid not in allids,'Duplicate document ID across archives';allids.add(docid)
                    db.execute('INSERT INTO filings VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(docid,archive.name,info.filename,hashlib.sha256(raw).hexdigest(),fields.get('houseID',''),fields.get('senateID',''),fields.get('clientName',''),fields.get('organizationName',''),fields.get('reportYear',''),q,fields.get('reportType',''),stamp,fields.get('income',''),fields.get('expenses',''),fields.get('selfSelect',''),json.dumps(fields)))
                    count+=1
                except Exception as e:failures.append({'archive':archive.name,'member':info.filename,'error':str(e)})
        db.commit();coverage.append({'archive':archive.name,'members':item['members'],'parsed':count,'unparsed_signing_dates':bad_dates});print(coverage[-1],flush=True)
    for column in ('client','house_id','senate_id'):db.execute(f'CREATE INDEX idx_house_{column} ON filings({column})')
    db.commit();summary={'archives':coverage,'parsed_filings':db.execute('select count(*) from filings').fetchone()[0],'distinct_client_name_strings':db.execute('select count(distinct client) from filings').fetchone()[0],'distinct_house_relationship_ids':db.execute("select count(distinct house_id) from filings where house_id!=''").fetchone()[0],'report_type_counts':dict(types),'parse_failures':failures,'explicit_character_reference_repairs':repairs,'scope':'All members of five officially listed 2025 House archives. House snapshot coverage is not independently proven equal to the unified API. Acquisition and field parsing do not mean complete legal review.'}
    (P/'house-parse-coverage.json').write_text(json.dumps(summary,indent=2));print({k:v for k,v in summary.items() if k not in ('archives','parse_failures','explicit_character_reference_repairs')});db.close()
if __name__=='__main__':run()
