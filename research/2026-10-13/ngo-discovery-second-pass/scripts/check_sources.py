#!/usr/bin/env python3
"""Bounded source-access checks only. No model API, cohort or entity pilot.
Downloads stay in a disposable cache; the repository receives metadata only.
"""
import argparse, datetime, hashlib, json, pathlib, urllib.request
SOURCES = [
('commission-2024', 'https://commission.europa.eu/document/download/e8fc367d-1d98-47ca-8f77-dd0121be3d8e_en?filename=2024_Annual-report-activities-senior-officials-after-service_EN.PDF.pdf'),
('manaus-rima', 'https://www.ipaam.am.gov.br/wp-content/uploads/2023/05/RIMA-UTE-Manaus-I.pdf'),
('manaus-prior-licence', 'https://www.ipaam.am.gov.br/wp-content/uploads/2022/09/300822-LP-No-026-2022-1a-Alteracao-Global-Participacoes-em-Energia-S.A..pdf'),
('aneel-operation', 'https://www.gov.br/aneel/pt-br/assuntos/noticias/2026-defeso-eleitoral/termeletrica-manaus-i-inicia-operacao-comercial-parcial-com-114-8-mw'),
('world-bank-sanctions', 'https://www.worldbank.org/en/Projects-operations/procurement/debarred-firms'),
('uk-debarment-guidance', 'https://www.gov.uk/government/publications/procurement-act-2023-guidance-documents-procure-phase/guidance-debarment-html'),
('fca-supervision-transition', 'https://www.fca.org.uk/firms/aml-supervisory-reform'),
('ibori-return-annex', 'https://www.gov.uk/government/publications/return-of-stolen-assets-confiscated-by-the-uk-agreement-between-the-uk-and-nigeria/mou-between-uk-and-nigeria-on-the-modalities-for-return-of-stolen-assets-confiscated-by-the-uk-annex-1'),
('nrgi-indonesia', 'https://resourcegovernance.org/articles/what-happens-after-mining-license-granted-indonesia-first-rga'),
]
def main():
    p=argparse.ArgumentParser(); p.add_argument('--cache', required=True); p.add_argument('--output', required=True); a=p.parse_args()
    cache=pathlib.Path(a.cache); cache.mkdir(parents=True, exist_ok=True)
    records=[]
    for key,url in SOURCES:
        row={'id':key,'requested_url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'channel':'urllib HTTPS; default TLS verification', 'depth':'access only; substantive reading recorded separately'}
        try:
            req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (bounded public-source verification)'})
            with urllib.request.urlopen(req, timeout=25) as response:
                body=response.read(20*1024*1024+1)
                if len(body)>20*1024*1024: raise ValueError('20 MiB bounded retrieval exceeded')
                row.update(status=response.status,final_url=response.geturl(),content_type=response.headers.get('Content-Type'),bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
                ext='.pdf' if body.startswith(b'%PDF') else '.html'
                (cache/(key+ext)).write_bytes(body)
                row['format_signature']='PDF' if ext=='.pdf' else 'non-PDF; may require content inspection'
        except Exception as e:
            row.update(status=getattr(e,'code',None),error=str(e),bytes=None,sha256=None)
        records.append(row); print(key, row.get('status'), row.get('bytes'), row.get('error',''))
    pathlib.Path(a.output).write_text(json.dumps(records,indent=2)+'\n')
if __name__=='__main__': main()
