"""Reproduce actual bounded downloads only. No numerical discrepancy investigation.
Read exact files, validate TLS normally, preserve errors. No paid service or model.
"""
import hashlib,json,subprocess,urllib.request,zipfile
from pathlib import Path
ROOT=Path(__file__).parent
CACHE=Path('/tmp/ngo-secrecy-pilot');CACHE.mkdir(exist_ok=True)
if __name__=='__main__':
    expected=json.load(open(ROOT/'drc_pilot_acquisition.json'));out=[]
    for record in expected:
        u=record['url'];d={'url':u}
        try:
            response=urllib.request.urlopen(u,timeout=30);body=response.read();sha=hashlib.sha256(body).hexdigest()
            suffix='.pdf' if '.pdf' in u else '.xlsx';f=CACHE/(sha+suffix);f.write_bytes(body)
            d.update(status=response.status,bytes=len(body),sha256=sha,matches_snapshot_sha256=sha==record.get('sha256'))
            if suffix=='.pdf':
                text=f.with_suffix('.txt');subprocess.run(['pdftotext','-layout',str(f),str(text)],check=True,capture_output=True)
                d.update(parseable=bool(text.read_text().strip()),pages=text.read_text().count('\f'))
            else:
                with zipfile.ZipFile(f) as z:d.update(parseable='xl/workbook.xml' in z.namelist(),zip_members=len(z.namelist()))
        except Exception as e:d['error']=str(e)
        out.append(d)
    json.dump(out,open(CACHE/'access-manifest.json','w'),indent=2)
    print(json.dumps(out,indent=2))
