#!/usr/bin/env python3
"""Finite FY2019-25 DOE annual report collection from official landing pages."""
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from acquire import fetch
for y in range(2019,2025):
 p=fetch('doe_ldrd',f'https://www.energy.gov/cfo/articles/fy-{y}-ldrd-report',f'FY{y}_landing.html',2_000_000)
 if not p:continue
 s=BeautifulSoup(p.read_text(),'html.parser');links=list(dict.fromkeys(urljoin('https://www.energy.gov',a['href']) for a in s.select('a[href]') if '.pdf' in a['href'].lower() and ('ldrd' in a['href'].lower() or 'directed' in a.get_text().lower())))
 for i,url in enumerate(links[:2]):fetch('doe_ldrd',url,f'DOE_FY{y}_LDRD_{i+1}.pdf',10_000_000)
