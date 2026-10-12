#!/usr/bin/env python3
"""Compare already-normalised claims; this is deliberately not an extraction engine."""
import argparse
import json
from decimal import Decimal

GATES = (
    'company_attribution', 'same_entity_project', 'same_period',
    'same_fact_definition', 'same_scope', 'same_unit_basis',
    'version_checked', 'extraction_verified',
)

def compare(pair):
    missing = [g for g in GATES if pair.get('gates', {}).get(g) is not True]
    result = {'id': pair.get('id'), 'unresolved_gates': missing}
    if missing:
        return {**result, 'status': 'REVIEW_REQUIRED'}
    a, b = pair['western'], pair['host']
    if a['kind'] != b['kind']:
        return {**result, 'status': 'REVIEW_REQUIRED', 'reason': 'Claim kinds differ'}
    if a['kind'] == 'interval':
        if a.get('unit') != b.get('unit'):
            return {**result, 'status': 'REVIEW_REQUIRED', 'reason': 'Units differ'}
        lo_a, hi_a = Decimal(a['low']), Decimal(a['high'])
        lo_b, hi_b = Decimal(b['low']), Decimal(b['high'])
        if lo_a > hi_a or lo_b > hi_b:
            raise ValueError('Reversed interval')
        incompatible = max(lo_a, lo_b) > min(hi_a, hi_b)
    elif a['kind'] == 'exclusive_category':
        # Categories must come from the same human-approved exclusive vocabulary.
        if a.get('vocabulary') != b.get('vocabulary'):
            return {**result, 'status': 'REVIEW_REQUIRED', 'reason': 'Vocabularies differ'}
        incompatible = a['value'] != b['value']
    else:
        raise ValueError('Unsupported claim kind; missing values must not be encoded as zero')
    return {**result, 'status': 'INCOMPATIBLE_CLAIMS' if incompatible else 'COMPATIBLE_WITH_PRECISION',
            'meaning': 'A logical comparison of supplied assertions, not a determination of truth, intent or liability.'}

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', help='JSON list of pairs or an object with a pairs member')
    args = p.parse_args()
    with open(args.input, encoding='utf-8') as f:
        data = json.load(f)
    pairs = data['pairs'] if isinstance(data, dict) else data
    print(json.dumps([compare(x) for x in pairs], ensure_ascii=False, indent=2))
