"""Recalculate the reviewed follow-up controls. Does not certify claim identity.

Document extraction and year-column decisions were reviewed separately and are
stored with locators and source fingerprints in followup-language-controls.json.
"""
import argparse
import json
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'research/2026-10-12/peru-production-pilot'
UNITS = {'t': ('t', Decimal(1)), 'tm': ('t', Decimal(1)),
         'oz': ('oz', Decimal(1)), 'kt': ('t', Decimal(1000)),
         'koz': ('oz', Decimal(1000)), 'MMoz': ('oz', Decimal(1000000))}


def replay(records):
    seen = set()
    outcomes = []
    for record in records:
        identity = record['control_id']
        if identity in seen:
            raise ValueError('Duplicate control ID: ' + identity)
        seen.add(identity)
        en, es = record['english'], record['spanish']
        enunit, enfactor = UNITS[en['unit']]
        esunit, esfactor = UNITS[es['unit']]
        if enunit != esunit:
            raise ValueError('Incompatible units: ' + identity)
        delta = Decimal(es['value']) * esfactor - Decimal(en['value']) * enfactor
        # Exact controls explicitly require equality; rounded tables allow the
        # conservative display allowance recorded in the original pilot.
        allowance = Decimal(record.get('display_precision_allowance', '0'))
        within = abs(delta) <= allowance
        if delta != Decimal(record['difference_spanish_minus_english']):
            raise ValueError('Saved arithmetic disagrees: ' + identity)
        if within != record['within_precision']:
            raise ValueError('Saved precision decision disagrees: ' + identity)
        outcomes.append({'control_id': identity, 'difference': str(delta),
                         'unit': enunit, 'within_precision': within})
    unique = {(r['entity'], r['year'], r['metal']) for r in records}
    return {'control_checks': len(records), 'distinct_entity_metal_years': len(unique),
            'within_precision': sum(r['within_precision'] for r in outcomes),
            'government_hosted_checks': sum(r['governments_pair'] for r in records),
            'gold_checks': sum(r['metal'] == 'Au' for r in records),
            'confirmed_contradictions': 0,
            'scope': 'Reviewed controls; overlapping checks are not independent trials',
            'results': outcomes}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path, default=DATA / 'followup-language-controls.json')
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    result = replay(json.loads(args.input.read_text()))
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'results'}, indent=2))


if __name__ == '__main__':
    main()
