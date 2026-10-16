"""Mandatory evidence lineage contract, shared by validation and smoke tests."""
REQUIRED=('document_id','source_url','raw_locator','source_snapshot_sha256','retrieved_at')
PROJECT_TABLES={'commons_projects.parquet','apfit_fy2022_projects.parquet','darpa_pb2025_programs.parquet','omb_security_fy2019_2026.parquet'}
def issues(frame):
 return {k:len(frame) if k not in frame else int((frame[k].isna() | frame[k].astype(str).str.strip().eq('')).sum()) for k in REQUIRED if k not in frame or (frame[k].isna() | frame[k].astype(str).str.strip().eq('')).any()}

def missing_columns(names):
 return sorted(set(REQUIRED)-set(names))
