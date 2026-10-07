from acquire import fetch
from concurrent.futures import ThreadPoolExecutor
items=[('st1-2024.zip','https://www.aer.ca/prd/data/well-lic/dwll2024.zip'),('st1-2025.zip','https://www.aer.ca/prd/data/well-lic/dwll2025.zip'),('pod.html','https://webapps.aer.ca/pod'),('pubdocs.html','https://www1.aer.ca/PubDocs/'),('tour-form.html','https://apps.public.aer.ca/tours/')]
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(lambda x:fetch(*x),items))
