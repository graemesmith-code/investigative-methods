#!/usr/bin/env python3
"""Free bounded source checks. Never disables TLS verification; no AI/API spend.
Run python reproduce_audit.py --output /tmp/ngo-audit-recheck
Dependencies: Python3; optional openpyxl; pdftotext for local PDF review.
"""
import argparse,datetime,hashlib,json,pathlib,urllib.request
URLS = [
'https://find-and-update.company-information.service.gov.uk/company/16545784/filing-history',
'https://find-and-update.company-information.service.gov.uk/company/16545784/persons-with-significant-control',
'https://find-and-update.company-information.service.gov.uk/company/16545784/filing-history/MzQ3MTY3NDMyNWFkaXF6a2N4/document?download=0&format=pdf',
'https://www.gov.uk/government/publications/confirmation-statement-form-cs01-new-version',
'https://www.itierdc.net/rapports-itie-rdc/2023/Rapport%20final%20ITIE%20RDC%202023%20%28Annexes%29%20-%2031-12-2025.xlsx',
'https://www.ivanhoemines.com/wp-content/uploads/20231231-00000-Ivanhoe-Mines-Ltd-ESTMA-Reporting-template-vF.pdf']
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',default='/tmp/ngo-audit-recheck');a=p.parse_args();d=pathlib.Path(a.output);d.mkdir(parents=True,exist_ok=True);log=[]
 for u in URLS:
  r={'url':u,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
  try:
   with urllib.request.urlopen(u,timeout=45) as h:
    b=h.read(15000001);r.update(status=h.status,bytes=len(b),content_type=h.headers.get('Content-Type'))
   if len(b)>15000000:raise ValueError('15MB bounded-download cap exceeded')
   r['sha256']=hashlib.sha256(b).hexdigest();suffix='.pdf' if b.startswith(b'%PDF') else '.xlsx' if b.startswith(b'PK') else '.html';f=d/(r['sha256']+suffix);f.write_bytes(b)
   if suffix=='.xlsx':
    import openpyxl
    w=openpyxl.load_workbook(f,read_only=True,data_only=True);extract=[]
    for name in ['Annexe 0 ','Annexe 3','Annexe 49','Annexe 51','Annexe 52']:
     if name not in w:continue
     for i,row in enumerate(w[name].iter_rows(values_only=True),1):
      if any(v and 'KAMOA' in str(v).upper() for v in row) or name=='Annexe 52':
       extract.append({'sheet':name,'row':i,'values':list(row)})
    (d/'kamoa-locations.json').write_text(json.dumps(extract,indent=2,ensure_ascii=False,default=str)+'\n')
  except Exception as e:r['error']=str(e)
  log.append(r)
 (d/'requests.json').write_text(json.dumps(log,indent=2)+'\n')
if __name__=='__main__':main()
