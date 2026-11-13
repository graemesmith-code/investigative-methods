#!/usr/bin/env python3
"""Verify saved evidence against SHA256SUMS.txt, without network access."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent
bad=[]
for line in (root/'SHA256SUMS.txt').read_text().splitlines():
    expected,name=line.split('  ',1)
    p=root/name
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
        bad.append(name)
print('PASS: all preserved files match' if not bad else 'FAIL: '+', '.join(bad))
raise SystemExit(bool(bad))
