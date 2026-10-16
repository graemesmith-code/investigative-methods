#!/usr/bin/env python3
"""Finite official document collection. Known URLs only; no crawling around access controls."""
from acquire import fetch,ROOT,save_json
import requests,bs4,concurrent.futures
JOBS=[
 ('darpa_budget','https://www.darpa.mil/sites/default/files/attachment/2024-11/u-rdte-mjb-darpa-pb-2025-06-mar-2024-final.pdf','DARPA_PB2025.pdf'),
 ('navy_budget','https://www.secnav.navy.mil/fmc/fmb/Documents/26pres/RDTEN_BA1-3_Book.pdf','NAVY_PB2026_BA1-3.pdf'),
 ('army_budget','https://www.asafm.army.mil/Portals/72/Documents/BudgetMaterial/2026/Discretionary%20Budget/rdte/RDTE%20-%20Vol%204%20-%20Budget%20Activity%206.pdf','ARMY_PB2026_BA6.pdf'),
 ('govinfo_budget','https://www.govinfo.gov/content/pkg/BUDGET-2026-DOD/pdf/BUDGET-2026-DOD.pdf','BUDGET-2026-DOD.pdf'),
 ('ffrdc','https://ncses.nsf.gov/819/assets/0/files/ffrdc_r_and_d_2025.zip','ffrdc_r_and_d_2025.zip'),
 ('commons','https://www.cto.mil/wp-content/uploads/2025/04/Quantum-Technology-Q-Projects.pdf','Quantum-Technology-Q-Projects.pdf'),
 ('commons','https://www.cto.mil/wp-content/uploads/2025/04/Electromagnetic-Warfare.pdf','Electromagnetic-Warfare.pdf'),
 ('commons','https://www.cto.mil/wp-content/uploads/2025/04/Secure-Edge-1.pdf','Secure-Edge-1.pdf'),
 ('apfit','https://ac.cto.mil/apfit/','index.html'),
 ('apfit','https://calvert.house.gov/sites/evo-subsites/calvert.house.gov/files/evo-media-document/20230321-apfit-biannual-report.pdf','APFIT_20230321.pdf'),
 ('sbir_docs','https://www.sbir.gov/data-resources/data-dictionary','data_dictionary.html'),
 ('usaspending_docs','https://www.usaspending.gov/data/about-the-data-download.pdf','about-the-data-download.pdf'),
 ('usaspending_docs','https://www.usaspending.gov/data/Federal-Spending-Guide.pdf','Federal-Spending-Guide.pdf'),
]
if __name__=='__main__':
 # Sequential downloads bound pressure and make the global storage limit reliable.
 for source,url,name in JOBS:fetch(source,url,name,150_000_000)
