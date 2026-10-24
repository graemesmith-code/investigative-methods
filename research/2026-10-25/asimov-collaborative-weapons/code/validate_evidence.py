#!/usr/bin/env python3
"""Validate the published financial snapshots without network calls or writes.

Optional --source-384 points to the immutable earlier CSV, allowing the
FA8651 prefix selection to be reproduced independently of enriched records.
"""
import argparse
import csv
import hashlib
import json
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    with Path(path).open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


def money(value):
    return Decimal(value or '0')


def unique(data, fields):
    keys = [tuple(row[field] for field in fields) for row in data]
    assert len(keys) == len(set(keys)), (fields, 'duplicate key')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-384', type=Path)
    args = parser.parse_args()
    a = rows(ROOT / 'evidence/asimov/contract-register.csv')
    aa = rows(ROOT / 'evidence/asimov/fpds-actions.csv')
    e = rows(ROOT / 'evidence/eglin/fa8651-cohort-audit.csv')
    ea = rows(ROOT / 'evidence/eglin/fa8651-contract-actions.csv')
    assert (len(a), len(aa), len(e), len(ea)) == (7, 43, 22, 124)
    unique(a, ['piid'])
    unique(e, ['award_id'])
    unique(aa, ['piid', 'modification', 'transaction'])
    unique(ea, ['award_id', 'modification', 'transaction_number'])
    asums = defaultdict(lambda: [Decimal(0), Decimal(0), Decimal(0)])
    for row in aa:
        for index, field in enumerate(['obligation', 'base_exercised_change', 'all_options_change']):
            asums[row['piid']][index] += money(row[field])
    for row in a:
        expected = [money(row[field]) for field in ['obligation_usd', 'base_and_exercised_usd', 'all_options_usd']]
        assert asums[row['piid']] == expected, row['piid']
    esums = defaultdict(lambda: [Decimal(0), Decimal(0), Decimal(0)])
    for row in ea:
        for index, field in enumerate(['obligation_change_usd', 'current_value_change_usd', 'potential_value_change_usd']):
            esums[row['award_id']][index] += money(row[field])
    assert len(esums) == 20
    for row in e:
        if row['award_id'] in esums:
            expected = [money(row[field]) for field in ['net_obligation_usd', 'base_and_exercised_value_usd', 'base_and_all_options_value_usd']]
            assert esums[row['award_id']] == expected, row['award_id']
    named = [row for row in e if row['named_user_case'] == 'True']
    assert len(named) == 6
    assert sum(money(row['net_obligation_usd']) for row in named) == Decimal('12256665.44')
    assert sum(money(row['base_and_exercised_value_usd']) for row in named) == Decimal('13653904.44')
    future = [row['award_id'] for row in e if row['current_completion_date'] > '2026-10-24']
    assert len(future) == 6
    overlap = set(row['piid'] for row in a) & set(row['award_id'] for row in e)
    assert overlap == {'FA865125CB007'}
    assert not overlap.intersection(future)
    for piid in overlap:
        assert asums[piid] == esums[piid], 'shared award financial discrepancy'
    output = {
        'status': 'passed',
        'asimov_awards': len(a), 'asimov_actions': len(aa),
        'asimov_obligations_usd': str(sum(money(row['obligation_usd']) for row in a)),
        'asimov_all_options_usd': str(sum(money(row['all_options_usd']) for row in a)),
        'fa8651_awards': len(e), 'fa8651_contracts_with_actions': len(esums),
        'fa8651_actions': len(ea), 'named_cases': len(named),
        'date_field_matches_not_active_work_count': future,
        'overlapping_award_ids': sorted(overlap),
        'unique_combined_awards': len(set(row['piid'] for row in a) | set(row['award_id'] for row in e)),
        'limitations': 'Validates published derivative tables, not delivery, legal closure, completeness of all programme vehicles, or live API state.'
    }
    if args.source_384:
        source = rows(args.source_384)
        assert len(source) == 384
        selected = {row['award_id'] for row in source if row['award_id'].startswith('FA8651')}
        assert selected == {row['award_id'] for row in e}
        output['source_prefix_selection'] = '22 identifiers reproduced from 384 rows'
        output['source_input_bytes'] = args.source_384.stat().st_size
        output['source_input_sha256'] = hashlib.sha256(args.source_384.read_bytes()).hexdigest()
        output['source_hash_note'] = 'Text-normalized copies can reproduce membership without matching the original byte hash.'
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
