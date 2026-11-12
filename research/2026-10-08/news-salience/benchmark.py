#!/usr/bin/env python3
"""Offline ranking benchmark. Python standard library only; no inference or network."""
import argparse
import csv
import hashlib
import json
import math
import random
import re
import unicodedata
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent.parent / '2026-10-01' / 'ati-live'
SEED = 20261008
VERSION = 'rules-v1'
VISIBLE = ('year', 'month', 'owner_org_title', 'request_number', 'summary_en',
           'summary_fr', 'disposition', 'pages', 'comments_en', 'comments_fr')
AXES = ('followup', 'significance', 'evidence_strength', 'novelty', 'prominence')
LABEL_FIELDS = ('blind_id', 'reviewer_id', *AXES, 'rationale', 'novelty_basis',
                'prominence_basis', 'evidence_basis')
# Each category fires at most once across both languages. No label-dependent tuning.
RULES = {
    'harm_rights': (2, r'\b(death|deaths|killed|fatal|mental health|involuntar\w*|torture|human rights|mort\w*|deces|sante mentale|droits de la personne)\b'),
    'accountability': (2, r'\b(non.compliance|compliance order|investigat\w*|audit\w*|fraud\w*|misconduct|corrupt\w*|enquet\w*|non.conform\w*)\b'),
    'money_decisions': (1, r'\b(contract\w*|procure\w*|cost\w*|expenditure\w*|funding|contrat\w*|cout\w*|depense\w*|financement)\b'),
    'specific_identifier': (1, r'\b(?:[a-z]{2}\d{4}-\d+|\d{4}-\d{2}-\d{2})\b'),
}

def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')

def write_csv(path, fields, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_source(source=SOURCE):
    rows = json.loads((source / 'calibration-ranked.json').read_text(encoding='utf-8'))
    ids = json.loads((source / 'calibration-ids.json').read_text(encoding='utf-8'))
    if len(rows) != 100 or len(ids) != 100 or len(set(ids)) != 100:
        raise ValueError('Expected exactly 100 unique calibration IDs')
    if len({r['_id'] for r in rows}) != 100 or set(ids) != {r['_id'] for r in rows}:
        raise ValueError('Calibration records and IDs differ')
    for r in rows:
        for field in ('rank_score', 'consequence', 'specificity', 'evidence', 'question'):
            if not isinstance(r[field], (int, float)) or not math.isfinite(r[field]):
                raise ValueError(f'Invalid saved {field}')
    if Counter(r['owner_org'] for r in rows) != {'dfatd-maecd': 36, 'dnd-mdn': 64}:
        raise ValueError('Department strata changed')
    return rows

def baseline(row):
    text = ' '.join(row.get(k) or '' for k in ('summary_en', 'summary_fr'))
    text = ''.join(c for c in unicodedata.normalize('NFKD', text.lower()) if not unicodedata.combining(c))
    hits = {name: weight for name, (weight, pattern) in RULES.items() if re.search(pattern, text)}
    available = int(row['disposition'] in ('DA', 'DP') and row['pages'] > 0)
    # Small capped page term; page count is acquisition metadata, not proof.
    availability = available + min(math.log1p(max(0, row['pages'])) / 10, 0.5)
    return {'rules_text': sum(hits.values()), 'rules_availability': availability,
            'rules_combined': sum(hits.values()) + availability, 'rule_hits': hits}

def ordered(rows, score):
    return sorted(rows, key=lambda r: (-r[score], str(r['_id'])))

def prepare(out, source=SOURCE):
    rows = load_source(source)
    for r in rows:
        r.update(baseline(r))
    ranks = {r['_id']: i + 1 for i, r in enumerate(ordered(rows, 'rank_score'))}
    # Sort before seeded shuffle so source ordering does not affect blinding.
    shuffled = sorted(rows, key=lambda r: r['_id'])
    random.Random(SEED).shuffle(shuffled)
    for i, r in enumerate(shuffled):
        r['blind_id'] = f'B{i + 1:03d}'
        r['jev_rank'] = ranks[r['_id']]
    coordinator = out / 'coordinator'
    reviewer = out / 'reviewer'
    coordinator.mkdir(parents=True, exist_ok=True)
    reviewer.mkdir(parents=True, exist_ok=True)
    dump(coordinator / 'records.json', shuffled)
    public = [{'blind_id': r['blind_id'], **{k: r.get(k) for k in VISIBLE}} for r in shuffled]
    write_csv(reviewer / 'records.csv', ('blind_id', *VISIBLE), public)
    labels = [{k: (r['blind_id'] if k == 'blind_id' else '') for k in LABEL_FIELDS} for r in shuffled]
    write_csv(reviewer / 'labels.csv', LABEL_FIELDS, labels)
    # 10 highest, 10 randomly selected middle, 10 randomly selected bottom quintile.
    rng = random.Random(SEED + 1)
    selected = (ordered(rows, 'rank_score')[:10] +
                rng.sample([r for r in rows if 11 <= r['jev_rank'] <= 80], 10) +
                rng.sample([r for r in rows if r['jev_rank'] >= 81], 10))
    selected_ids = {r['blind_id'] for r in selected}
    write_csv(reviewer / 'starter-records.csv', ('blind_id', *VISIBLE),
              [r for r in public if r['blind_id'] in selected_ids])
    write_csv(reviewer / 'starter-labels.csv', LABEL_FIELDS,
              [r for r in labels if r['blind_id'] in selected_ids])
    dump(coordinator / 'starter-selection.json', [{'blind_id': r['blind_id'],
         'source_id': r['_id'], 'jev_rank': r['jev_rank'],
         'band': 'top' if r['jev_rank'] <= 10 else 'bottom' if r['jev_rank'] >= 81 else 'middle'} for r in selected])
    dump(coordinator / 'manifest.json', {
        'seed': SEED, 'baseline_version': VERSION, 'n': 100,
        'records_sha256': digest(coordinator / 'records.json'),
        'department_counts': dict(Counter(r['owner_org'] for r in rows)),
        'source_sha256': {p: digest(source / p) for p in
            ('calibration-ranked.json', 'calibration-ids.json', 'ranking-prompt.json')},
        'rules': {k: {'weight': v[0], 'pattern': v[1]} for k, v in RULES.items()},
        'tie_break': 'source _id lexicographic ascending',
        'model_scores': 'saved Jev scores; no new calls; see original ranking-prompt.json',
        'human_labels': 'none generated; blank templates only',
    })
    dump(out / 'status.json', {'status': 'awaiting_human_labels', 'n_records': 100,
         'performance_metrics': None, 'completed': ['input validation', 'rules scoring',
         'blinded full packet', '30-record starter with 10 bottom-quintile records'],
         'pending': ['independent editorial labels', 'ranking evaluation',
         'observed article placement and record/article links', 'verified novelty and release evidence']})
    return shuffled

def read_labels(path, rows, axis):
    expected = {r['blind_id'] for r in rows}
    labels = {}
    reviewers = set()
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if not set(LABEL_FIELDS).issubset(reader.fieldnames or []):
            raise ValueError('Label columns missing')
        for r in reader:
            key = r['blind_id']
            if key not in expected or key in labels:
                raise ValueError(f'Unknown or duplicate blind_id: {key}')
            if not r['reviewer_id'].strip() or not r['rationale'].strip():
                raise ValueError('Reviewer ID and rationale required on every row')
            reviewers.add(r['reviewer_id'].strip())
            for a in AXES:
                if r[a] not in ('', 'unknown', '0', '1', '2', '3'):
                    raise ValueError(f'Invalid ordinal value for {a}')
                if a in ('novelty', 'prominence') and r[a] not in ('', 'unknown') and not r[a + '_basis'].strip():
                    raise ValueError(f'{a} needs an external evidence basis')
            if r['evidence_strength'] in ('2', '3') and not r['evidence_basis'].strip():
                raise ValueError('Evidence strength 2/3 needs an obtained-material basis')
            if r[axis] in ('', 'unknown'):
                raise ValueError(f'Complete {axis} labels required; missing {key}')
            labels[key] = int(r[axis])
    if set(labels) != expected or len(reviewers) != 1:
        raise ValueError('Use one reviewer or adjudicated consensus, covering all 100 records')
    return labels, next(iter(reviewers))

def dcg(values):
    return sum((2 ** v - 1) / math.log2(i + 2) for i, v in enumerate(values))

def metrics(ranking, labels, k):
    values = [labels[r['blind_id']] for r in ranking]
    total_positive = sum(v >= 2 for v in values)
    found = sum(v >= 2 for v in values[:k])
    ideal = dcg(sorted(values, reverse=True)[:k])
    return {'precision_at_k': found / k, 'recall_at_k': found / total_positive if total_positive else None,
            'ndcg_at_k': dcg(values[:k]) / ideal if ideal else None,
            'positives_found': found, 'positives_total': total_positive}

def evaluate(packet, label_file, axis, ks):
    rows = json.loads((packet / 'coordinator' / 'records.json').read_text(encoding='utf-8'))
    manifest = json.loads((packet / 'coordinator' / 'manifest.json').read_text(encoding='utf-8'))
    if manifest.get('records_sha256') != digest(packet / 'coordinator' / 'records.json'):
        raise ValueError('Coordinator packet changed; prepare a fresh frozen packet')
    if len(rows) != 100 or len({r['blind_id'] for r in rows}) != 100:
        raise ValueError('Packet must contain 100 unique records')
    labels, reviewer = read_labels(label_file, rows, axis)
    if any(k < 1 or k > len(rows) for k in ks):
        raise ValueError('k must be between 1 and 100')
    methods = ('rank_score', 'consequence', 'specificity', 'evidence', 'question',
               'rules_text', 'rules_availability', 'rules_combined')
    results = {}
    for method in methods:
        if any(not isinstance(r[method], (float, int)) or not math.isfinite(r[method]) for r in rows):
            raise ValueError('Non-finite ranking score')
        ranking = ordered(rows, method)
        results[method] = {str(k): metrics(ranking, labels, k) for k in ks}
    low = [r for r in rows if r['jev_rank'] >= 81]
    low_positives = [{'blind_id': r['blind_id'], 'source_id': r['_id'],
                     'jev_rank': r['jev_rank'], 'label': labels[r['blind_id']]} for r in low if labels[r['blind_id']] >= 2]
    # Recompute within each department; this is a different ranking universe.
    by_department = {}
    for org in sorted({r['owner_org'] for r in rows}):
        subset = [r for r in rows if r['owner_org'] == org]
        by_department[org] = {m: {str(k): metrics(ordered(subset, m), labels, k)
             for k in ks if k <= len(subset)} for m in methods}
    return {'status': 'evaluated_against_human_labels', 'axis': axis, 'reviewer': reviewer,
        'n': len(rows), 'positive_threshold': 2, 'baseline_version': manifest['baseline_version'],
        'labels_sha256': digest(label_file), 'packet_sha256': digest(packet / 'coordinator' / 'records.json'),
        'rankings': results, 'by_department': by_department,
        'bottom_quintile': {'n': len(low), 'positive_records': low_positives},
        'limitations': ['Descriptive pilot, not population accuracy or causal evidence.',
            'Ordinal gains 2^label-1 and threshold >=2 are predeclared conventions.',
            'Observed prominence is a different target; homepage placement is not print A1/A16.',
            'Jev evidence measures comparison potential, not verified evidence strength.',
            'Ties broken by source ID; many rule ties can affect top-k.',
            'Scores are not calibrated probabilities; no model-confidence accuracy claim.']}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('prepare')
    p.add_argument('--source', type=Path, default=SOURCE)
    p.add_argument('--out', type=Path, default=HERE / 'packet')
    e = sub.add_parser('evaluate')
    e.add_argument('--packet', type=Path, default=HERE / 'packet')
    e.add_argument('--labels', type=Path, required=True)
    e.add_argument('--axis', choices=AXES, default='followup')
    e.add_argument('--k', type=int, nargs='+', default=[10, 20])
    e.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'prepare':
            prepare(args.out, args.source)
            print('Prepared 100 blinded records. No benchmark performance measured.')
        else:
            report = evaluate(args.packet, args.labels, args.axis, args.k)
            dump(args.out, report)
            print(f'Wrote human-label comparison to {args.out}')
    except (ValueError, KeyError) as exc:
        parser.error(str(exc))

if __name__ == '__main__':
    main()
