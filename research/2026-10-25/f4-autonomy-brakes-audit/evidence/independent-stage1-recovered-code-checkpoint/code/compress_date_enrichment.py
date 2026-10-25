#!/usr/bin/env python3
"""Deterministic gzip of the full source date/office enrichment; original retained."""
import pathlib,gzip,shutil,json,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
src=ROOT/'evidence/award-date-fields.jsonl';out=src.with_suffix('.jsonl.gz')
with src.open('rb') as stream,out.open('wb') as target:
 with gzip.GzipFile(filename='',fileobj=target,mode='wb',mtime=0,compresslevel=6) as compressed:shutil.copyfileobj(stream,compressed)
metadata={'source':str(src.relative_to(ROOT)),'source_bytes':src.stat().st_size,'source_sha256':hashlib.file_digest(src.open('rb'),'sha256').hexdigest(),'output':str(out.relative_to(ROOT)),'output_bytes':out.stat().st_size,'output_sha256':hashlib.file_digest(out.open('rb'),'sha256').hexdigest(),'gzip_mtime':0,'gzip_compresslevel':6}
(ROOT/'audit/date-enrichment-compression.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(json.dumps(metadata,indent=2))
