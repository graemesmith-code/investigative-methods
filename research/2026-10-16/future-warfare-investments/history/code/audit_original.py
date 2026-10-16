#!/usr/bin/env python3
"""Deterministic original-export/boundary audit against a retained source page."""
import collections,csv,gzip,hashlib,json
from pathlib import Path
from collect_history import ROOT,parse,sha,dump,write_csv

def main():
 original=ROOT.parent/'raw/pentagon_contract_paragraphs_10000.csv';rows=list(csv.DictReader(original.open(newline='')))
 html=ROOT/'audit/original_boundary_3523820.html.gz';content=gzip.decompress(html.read_bytes())
 date,title,source,blocks=parse(content,'https://www.defense.gov/News/Contracts/Contract/Article/3523820/')
 boundary=[r for r in rows if r['announcement_date']==date];norm=lambda s:' '.join(s.split())
 findings=dict(original_file='../raw/pentagon_contract_paragraphs_10000.csv',original_sha256=sha(original.read_bytes()),row_count=len(rows),unique_full_rows=len({tuple(r.values()) for r in rows}),unique_paragraphs=len({r['raw_paragraph_verbatim'] for r in rows}),source_pages=len({r['source_url'] for r in rows}),announcement_dates=len({r['announcement_date'] for r in rows}),minimum_date=min(r['announcement_date'] for r in rows),maximum_date=max(r['announcement_date'] for r in rows),ordered_newest_date_first=all(a['announcement_date']>=b['announcement_date'] for a,b in zip(rows,rows[1:])),paragraph_length_range=[min(len(r['raw_paragraph_verbatim']) for r in rows),max(len(r['raw_paragraph_verbatim']) for r in rows)],boundary_date=date,boundary_export_rows=len(boundary),boundary_source_paragraphs=len(source),boundary_export_matches_source_prefix=all(norm(a['raw_paragraph_verbatim'])==norm(b['raw_paragraph_verbatim']) for a,b in zip(boundary,source)),boundary_missing_source_paragraphs=len(source)-len(boundary),source_response_sha256=sha(content),interpretation='Newest-first capped selection; complete paragraphs in boundary prefix, but page-level truncation at 10,000 rows. Original collector, exact sampling/extraction configuration and broader page completeness remain unavailable/unverified. No assertion of comparable full coverage.')
 dump(ROOT/'audit/original_corpus_audit.json',findings)
 write_csv(ROOT/'audit/original_boundary_comparison.csv',[dict(source_paragraph_index=r['paragraph_index'],service_or_agency_section=r['service_or_agency_section'],paragraph_sha256=sha(r['raw_paragraph_verbatim'].encode()),present_in_original=norm(r['raw_paragraph_verbatim']) in {norm(x['raw_paragraph_verbatim']) for x in boundary},paragraph_prefix=r['raw_paragraph_verbatim'][:160]) for r in source],['source_paragraph_index','service_or_agency_section','paragraph_sha256','present_in_original','paragraph_prefix'])
 print(json.dumps(findings,indent=2))
if __name__=='__main__':main()
