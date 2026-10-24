#!/usr/bin/env python3
"""Lossless, deterministic export of the original Lane 2 non-exact follow-on filter.
Uses only regenerated original inputs; performs no network requests or publication.
Usage: python export_lane2_followons.py F2_ROOT [OUTPUT_DIRECTORY]
"""
import collections, csv, datetime, hashlib, json, sys
from decimal import Decimal
from pathlib import Path
root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else root / 'audit'
out.mkdir(parents=True, exist_ok=True)
recipient_file = root / 'lane2/recipient_potential_followons.jsonl'
screen_file = root / 'lane2/followon_description_screen.jsonl'
source_audit_file = root / 'lane2/followon_description_audit.json'
source_audit = json.loads(source_audit_file.read_text())
cohort = collections.defaultdict(lambda: {'cents': 0, 'rows': 0, 'dates': []})
for line in recipient_file.open():
    r = json.loads(line)
    if not r['broad_sbir_piids']:
        continue
    a = cohort[r['award_key']]
    a['cents'] += int(r['obligation_cents'] or 0)
    a['rows'] += 1
    a['dates'].append(r['action_date'])
selected = []
award_count = 0
score_point_weights = {'ai': 3, 'tactical': 4, 'transition': 3}
for order, line in enumerate(screen_file.open(), 1):
    r = json.loads(line)
    award_count += 1
    a = cohort[r['award_key']]
    assert a['rows'] == r['action_count_2024_on']
    components = {k: int(bool(r['followon_hits'][k])) * w for k, w in score_point_weights.items()}
    assert sum(components.values()) == r['followon_score']
    if r['exact_piid_in_sbir'] or r['followon_score'] < 7 or a['cents'] <= 0:
        continue
    # Keep every original field, including descriptions and recipient joins.
    r['source_award_stream_order'] = order
    r['representative_transaction_row_number'] = r['row_number']
    r['score_components'] = components
    r['aggregate_2024_on_obligation_cents'] = a['cents']
    r['aggregate_2024_on_obligation_usd_exact'] = format(Decimal(a['cents']) / Decimal(100), '.2f')
    r['first_cohort_action_date'] = min(a['dates'])
    r['last_cohort_action_date'] = max(a['dates'])
    selected.append(r)
# Python's stable sort preserves original award-stream order for exact score/sum ties.
selected.sort(key=lambda r: (r['followon_score'], r['aggregate_2024_on_obligation_cents']), reverse=True)
for rank, r in enumerate(selected, 1):
    r['rank'] = rank
assert sum(a['rows'] for a in cohort.values()) == source_audit['row_count'] == 18741
assert award_count == source_audit['awards'] == 7374
assert len(selected) == source_audit['high_scoring_nonexact_awards'] == 92
stem = 'lane2-high-scoring-nonexact-followons-92'
json_path = out / (stem + '.json')
json_path.write_text(json.dumps(selected, ensure_ascii=False, indent=2) + '\n')
columns = ['rank', 'entity_name', 'entity_key', 'award_key', 'award_id', 'source_url',
           'source_award_stream_order', 'representative_transaction_row_number',
           'transaction_key', 'action_date', 'first_cohort_action_date', 'last_cohort_action_date',
           'followon_score', 'score_components', 'followon_hits',
           'aggregate_2024_on_obligation_cents', 'aggregate_2024_on_obligation_usd_exact',
           'action_count_2024_on', 'description_text', 'all_descriptions',
           'match_kind', 'exact_piid_in_sbir', 'recipient_sbir_piids', 'broad_sbir_piids']
csv_path = out / (stem + '.csv')
with csv_path.open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    for r in selected:
        writer.writerow({k: json.dumps(r[k], ensure_ascii=False) if isinstance(r.get(k), (dict, list)) else r.get(k) for k in columns})
def file_audit(p):
    return {'file': str(p.relative_to(root)) if p.is_relative_to(root) else str(p),
            'bytes': p.stat().st_size, 'sha256': hashlib.file_digest(p.open('rb'), 'sha256').hexdigest()}
audit = {
    'generated_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'recovery_method': 'Deterministic rerun from SHA-256-verified original archive bytes and published original screen scripts; not guessed from remembered examples.',
    'denominator_transaction_rows': sum(a['rows'] for a in cohort.values()),
    'denominator_award_keys': award_count,
    'selected_award_keys': len(selected),
    'original_screen_description_characters': source_audit['chars'],
    'filter': 'Non-exact normalized SBIR PIID AND maximum transaction-description score >= 7 AND positive net 2024-onward obligation sum within broad-SBIR-recipient cohort.',
    'score_weights': score_point_weights,
    'regex_patterns': source_audit['patterns'],
    'representative_rule': 'Original max() retained the first encountered source transaction at the highest score. Original SQLite read had no explicit ORDER BY. Export retains original regenerated source stream and representative row_number.',
    'rank_tie_rule': 'Descending score, then descending exact integer-cent cohort sum; stable ties retain original source award stream order.',
    'money_definition': 'Net action obligations dated >= 2024-01-01 in the October 16 archive, including negative modifications. Not award ceiling, outlay, all-time award total, or newly verified current spending.',
    'lineage_warning': 'Recipient UEI/name joins generate candidates, not established technical transitions, Phase III lineage, or verified AI programmes. A score >= 7 can arise from tactical+transition terms without an AI match.',
    'identifiers': 'Full award_key preserved; short award_id is not used to merge distinct awards.',
    'inputs': [file_audit(p) for p in (recipient_file, screen_file, source_audit_file)],
    'outputs': [file_audit(p) for p in (csv_path, json_path)],
    'historical_membership_status': 'Reconstructed 92 by unmodified published filter; historical membership equality cannot be independently confirmed without a surviving original membership file/hash.',
    'original_high_score_membership_difference_count': None}
comparison_path = root / 'audit/lane2-reconstruction-comparison.json'
if comparison_path.exists():
    comparison = json.loads(comparison_path.read_text())
    audit['broader_join_discrepancy'] = comparison['differing_join_counts']
    audit['historical_comparison_audit'] = 'lane2-reconstruction-comparison.json'
if (root / 'input_verification.json').exists():
    audit['verified_input_manifest'] = file_audit(root / 'input_verification.json')
(out / 'lane2-followon-export-audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'rows': len(selected), 'outputs': audit['outputs']}, indent=2))
