#!/usr/bin/env python3
"""Keep stable public document paths; refresh expiring URL parameters from tender API on reproduction."""
import json,pathlib,urllib.parse
P=pathlib.Path(__file__).parent
def scrub(x):
 if isinstance(x,dict):return {k:scrub(v) for k,v in x.items()}
 if isinstance(x,list):return [scrub(v) for v in x]
 if isinstance(x,str) and 'public-docs.prozorro.gov.ua/get/' in x:
  u=urllib.parse.urlsplit(x);return urllib.parse.urlunsplit((u.scheme,u.netloc,u.path,'',''))
 return x
for name in ['prozorro-pilot.json','prozorro-comparison.json','prozorro-checks.json']:
 p=P/name
 if p.exists():p.write_text(json.dumps(scrub(json.loads(p.read_text())),ensure_ascii=False,indent=2))
