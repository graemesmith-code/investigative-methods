#!/usr/bin/env python3
"""Free official sources; downloads to this script's directory. No model or paid API."""
from pathlib import Path
from urllib.request import urlopen
import hashlib,json
root=Path(__file__).resolve().parent
manifest=[]
for year in [2004,2005,2006]:
 url=f'https://www.occ.gov/publications-and-resources/publications/survey-of-credit-underwriting-practices/files/pub-survey-cred-under-{year}.pdf'
 path=root/f'occ{year}.pdf'
 data=urlopen(url,timeout=60).read();path.write_bytes(data)
 manifest.append({'year':year,'url':url,'filename':path.name,'sha256':hashlib.sha256(data).hexdigest()})
print(json.dumps(manifest,indent=2))
