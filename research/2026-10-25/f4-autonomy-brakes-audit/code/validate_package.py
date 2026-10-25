#!/usr/bin/env python3
"""Validate authored F4 data and links without a network call or paid request.

Run before package_artifacts.py. Re-run with --check-only after packaging to
avoid changing an inventoried audit file. Delivery-container/hash verification
belongs to package_artifacts.py and publication verification, not this script.
Uncompressed complete text is a local/Library delivery, deliberately excluded
from the GitHub per-file limit; the public gzip transport remains subject to it.
"""
from __future__ import annotations
import argparse, collections, csv, datetime, gzip, json, os, pathlib, re, sys
from decimal import Decimal
from urllib.parse import unquote, urlsplit

P = pathlib.Path(__file__).resolve().parents[1]
OUTPUT = 'audit/package-validation.json'
BUNDLE = 'F4-COMPLETE-RESEARCH-PACKAGE.txt'
LIMIT = 100 * 1024 * 1024
csv.field_size_limit(sys.maxsize)
REQUIRED = [
    'report.md', 'README.md', 'READING_PACK.md',
    'evidence/brakes-candidate-register.csv', 'evidence/brakes-candidate-register.json',
    'evidence/asimov-performer-continuation-check.csv',
    'evidence/reviewed-cases.csv', 'evidence/reviewed-cases.json',
    'evidence/fpds-verified-actions.csv', 'evidence/live-award-register.json',
    'audit/EDITOR_REPORTER_LOOP_LOG.md', 'audit/editor-round1.md',
    'audit/editor-round2.md', 'audit/editor-round3.md',
    'audit/exa-query-cost-log.csv', 'audit/methodology-accounting.json',
    'audit/screen-complete-input-coverage.json',
    'audit/screen-final-register-validation.json',
    'audit/reviewed-case-accounting.json', 'audit/parallel-register-reconciliation.json',
    'code/screen_archives.py', 'code/live_verify.py', 'code/exa_serial.py',
    'code/build_reviewed_cases.py', 'code/package_artifacts.py',
    'code/validate_package.py',
]
DEFERRED = {'manifest.json', 'SHA256SUMS', BUNDLE, BUNDLE + '.gz'}

def files():
    return sorted(f for f in P.rglob('*') if f.is_file()
                  and '__pycache__' not in f.parts and '.git' not in f.parts
                  and f.suffix != '.pyc')

def decimal_sum(rows, field):
    return sum((Decimal(str(r[field])) for r in rows if r.get(field) is not None), Decimal(0)) if rows else None

def validate():
    out = {'validated_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'scope': 'Local data, arithmetic, links and literal secret scan; no network or paid calls',
           'checks': {}, 'failures': [], 'remaining_release_gates': []}
    def check(name, fn):
        try:
            data = fn()
            out['checks'][name] = {'status': 'passed', **(data or {})}
        except Exception as exc:
            # Never stringify data assertions: rows could contain private values.
            out['checks'][name] = {'status': 'failed', 'error_type': type(exc).__name__}
            out['failures'].append(name)
    paths = files()
    loaded = {}
    def required():
        missing = [n for n in REQUIRED if not (P/n).is_file()]
        if missing:
            out['missing_required_files'] = missing
            raise ValueError('required files missing')
        return {'required_present': len(REQUIRED),
                'delivery_and_hash_containers_deferred_to_root_build': sorted(DEFERRED)}
    check('required_files', required)
    def parse():
        results = []
        retain = {'evidence/brakes-candidate-register.json', 'evidence/reviewed-cases.json',
                  'audit/reviewed-case-accounting.json', 'evidence/live-award-register.json'}
        for f in paths:
            rel = f.relative_to(P).as_posix()
            if rel == OUTPUT or rel in DEFERRED:
                continue
            name = f.name
            info = {'path': rel}
            op = gzip.open if name.endswith('.gz') else open
            if name.endswith(('.json', '.json.gz')):
                with op(f, 'rt', encoding='utf-8') as inp: obj = json.load(inp)
                if rel in retain: loaded[rel] = obj
                info.update(kind='JSON', top_level_type=type(obj).__name__)
            elif name.endswith(('.jsonl', '.jsonl.gz', '.ndjson', '.ndjson.gz')):
                n = 0
                with op(f, 'rt', encoding='utf-8') as inp:
                    for n, line in enumerate(inp, 1): json.loads(line)
                info.update(kind='JSONL', rows=n)
            elif name.endswith(('.csv', '.csv.gz', '.tsv', '.tsv.gz')):
                n = 0
                delim = '\t' if name.endswith(('.tsv', '.tsv.gz')) else ','
                with op(f, 'rt', encoding='utf-8', newline='') as inp:
                    reader = csv.DictReader(inp, delimiter=delim)
                    if not reader.fieldnames: raise ValueError('missing CSV headers')
                    for n, row in enumerate(reader, 1):
                        if None in row or any(v is None for v in row.values()):
                            raise ValueError('CSV field count differs from headers')
                    columns = len(reader.fieldnames)
                info.update(kind='CSV_or_TSV', rows=n, columns=columns)
            else: continue
            results.append(info)
        return {'files': results, 'files_parsed': len(results),
                'CSV_field_limit': sys.maxsize, 'row_unit': 'parsed records, not physical text lines'}
    check('all_JSON_JSONL_CSV_parsing', parse)
    def main_register():
        rows = loaded['evidence/brakes-candidate-register.json']
        index = {r['award_key']: r for r in rows}
        if len(index) != len(rows): raise ValueError('duplicate JSON key')
        seen = set()
        money = ['financial_transaction_count', 'obligation_cents_fy2019_2026',
                 'obligation_cents_fy2024_2026', 'obligation_cents_cy2024_2026']
        with (P/'evidence/brakes-candidate-register.csv').open(encoding='utf-8', newline='') as inp:
            for row in csv.DictReader(inp):
                key = row['award_key']
                if key in seen: raise ValueError('duplicate CSV key')
                seen.add(key)
                original = index[key]
                if json.loads(row['full_descriptions']) != original['full_descriptions']:
                    raise ValueError('full description mismatch')
                for field in money:
                    value = int(row[field]) if row[field] else None
                    if value != original[field]: raise ValueError('money mismatch')
        if seen != set(index): raise ValueError('key sets differ')
        return {'exact_keys': len(rows), 'all_full_description_strings_equal': True,
                'all_integer_cent_windows_equal': True, 'null_not_coerced_to_zero': True}
    check('main_CSV_JSON_exact_agreement', main_register)
    def arithmetic():
        rows = loaded['evidence/reviewed-cases.json']
        if len({r['award_key'] for r in rows}) != len(rows): raise ValueError('duplicate case key')
        live = loaded['evidence/live-award-register.json']
        index = {r['award_key']: r for award in live['awards'] for r in award.get('records', []) if r.get('award_key')}
        for row in rows:
            if Decimal(row['net_obligations_usd']) != Decimal(index[row['award_key']]['total_obligation_usd']):
                raise ValueError('case does not match live amount')
        accounting = loaded['audit/reviewed-case-accounting.json']
        totals = accounting['totals']
        for cat in 'ABCD':
            subset = [r for r in rows if r['primary_category'] == cat and r['counted_in_named_case_total']]
            expected = totals[cat]
            if len(subset) != expected['awards_in_selected_case_set']: raise ValueError('case count mismatch')
            for field in ['net_obligations_usd', 'fy2019_2026_obligations_usd', 'fy2024_2026_obligations_usd']:
                actual = decimal_sum(subset, field)
                target = Decimal(expected[field]) if expected[field] is not None else None
                if actual != target: raise ValueError('case sum mismatch')
            overlap = [r for r in subset if r['record_window_overlaps_cutoff']]
            if len(overlap) != expected['record_window_overlap_awards']: raise ValueError('overlap count mismatch')
            actual = decimal_sum(overlap, 'net_obligations_usd')
            target = expected['record_window_overlap_net_obligations_usd']
            if actual != (Decimal(target) if target is not None else None): raise ValueError('overlap sum mismatch')
        views = {
            'explicit_weapon_normative_scope_subset': [r for r in rows if r.get('weapon_specific_normative_scope_explicit')],
            'adjacent_view_not_added_to_weapons_totals': [r for r in rows if r.get('scope_tier') == 'normative_autonomy_adjacent_weapons_application_unverified'],
        }
        for label, subset in views.items():
            target = accounting[label]
            if len(subset) != target['award_count']: raise ValueError('scope-view count mismatch')
            if sum((Decimal(r['net_obligations_usd']) for r in subset), Decimal(0)) != Decimal(target['net_obligations_usd']):
                raise ValueError('scope-view sum mismatch')
            overlap = [r for r in subset if r['record_window_overlaps_cutoff']]
            if len(overlap) != target['record_overlap_count']: raise ValueError('scope-view overlap count mismatch')
            if sum((Decimal(r['net_obligations_usd']) for r in overlap), Decimal(0)) != Decimal(target['record_overlap_net_obligations_usd']):
                raise ValueError('scope-view overlap sum mismatch')
        return {'reviewed_unique_awards': len(rows), 'all_selected_amounts_match_live': True,
                'all_category_and_record_overlap_totals_recomputed': True,
                'strict_normative_and_adjacent_views_recomputed': True,
                'financial_meaning': 'Whole associated awards; allocable safeguard-feature spending remains unknown'}
    check('selected_case_arithmetic', arithmetic)
    def budget():
        with (P/'audit/exa-query-cost-log.csv').open(encoding='utf-8', newline='') as inp:
            rows = list(csv.DictReader(inp))
        prior = Decimal('4.095'); total = Decimal(0)
        for sequence, row in enumerate(rows, 1):
            if int(row['sequence']) != sequence: raise ValueError('budget sequence gap')
            debit = Decimal(row['budget_debit_usd'])
            if debit <= 0: raise ValueError('unreserved paid request')
            if row.get('response_reported_usd') and Decimal(row['response_reported_usd']) > debit:
                raise ValueError('reported cost exceeds debit')
            total += debit
            if Decimal(row['new_cumulative_usd']) != total: raise ValueError('new-spend cumulative mismatch')
            if Decimal(row['all_cumulative_usd']) != prior + total: raise ValueError('all-spend cumulative mismatch')
        if total > Decimal('10.905') or prior + total > Decimal('15.000'):
            raise ValueError('authorized budget exceeded')
        return {'ledger_requests': len(rows), 'new_reserved_or_debited_usd': str(total),
                'prior_stipulated_usd': str(prior), 'all_reserved_or_debited_usd': str(prior + total),
                'uncertain_or_unreturned_requests': sum(r['status'] != 'response' for r in rows),
                'invoice_independently_verified': False}
    check('serialized_budget_ledger_arithmetic', budget)
    def links():
        checked = 0; pending = []; missing = []
        for f in paths:
            if f.suffix != '.md': continue
            source = f.read_text(encoding='utf-8')
            source = re.sub(r'(?ms)^\s*(```|~~~).*?^\s*\1\s*$', '', source)
            source = '\n'.join(line for line in source.splitlines() if not line.lstrip().startswith('>'))
            source = re.sub(r'`[^`\n]*`', '', source)
            for target in re.findall(r'\]\(\s*(<[^>]+>|[^)\n]+)\)', source):
                target = target[1:-1] if target.startswith('<') else target.split()[0]
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith('/'): continue
                destination = (f.parent/unquote(parsed.path)).resolve()
                checked += 1
                if destination.is_file() or destination.is_dir(): continue
                try: rel = destination.relative_to(P).as_posix()
                except ValueError: rel = str(destination)
                item = {'source': f.relative_to(P).as_posix(), 'target': rel}
                if rel in DEFERRED or rel == OUTPUT: pending.append(item)
                else: missing.append(item)
        if missing:
            out['relative_link_failures'] = missing
            raise ValueError('missing relative Markdown destinations')
        return {'relative_links_checked': checked, 'pending_generated_container_links': pending,
                'scope': 'All authored Markdown except fenced/inline code and quoted external source text; absolute/remote references excluded'}
    check('relative_Markdown_links', links)
    def sizes():
        oversized = [{'path': f.relative_to(P).as_posix(), 'bytes': f.stat().st_size}
                     for f in paths if f.relative_to(P).as_posix() != BUNDLE and f.stat().st_size >= LIMIT]
        if oversized:
            out['oversized_public_files'] = oversized
            raise ValueError('GitHub per-file limit')
        return {'public_files_checked': len([f for f in paths if f.name != BUNDLE]),
                'limit_bytes_strictly_less_than': LIMIT,
                'excluded_local_Library_plain_text_delivery': BUNDLE,
                'gzip_transport_is_checked': True}
    check('public_file_sizes', sizes)
    def secrets():
        # Scan exact credential-like environment values. Values never enter output.
        literals = {v.encode() for k, v in os.environ.items()
                    if re.search(r'API_KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL', k, re.I)
                    and len(v) >= 12}
        width = max((len(v) for v in literals), default=1)
        matches = []; scanned = 0
        for f in paths:
            if f.relative_to(P).as_posix() == OUTPUT: continue
            # Gzip members are scanned in expanded form too; no decoded content is printed.
            openers = [open] + ([gzip.open] if f.name.endswith('.gz') else [])
            for opener in openers:
                tail = b''
                with opener(f, 'rb') as inp:
                    for chunk in iter(lambda: inp.read(1024 * 1024), b''):
                        block = tail + chunk
                        if any(secret in block for secret in literals):
                            matches.append(f.relative_to(P).as_posix()); break
                        tail = block[-max(width-1, 1):]
                scanned += 1
        if matches:
            out['secret_match_files'] = sorted(set(matches))
            raise ValueError('credential literal found')
        return {'credential_like_environment_literal_count': len(literals),
                'file_or_expanded_streams_scanned': scanned, 'matches': 0,
                'no_secret_values_logged': True, 'limit': 'Exact configured literals only; not a proof against every unknown secret'}
    check('environment_secret_literal_scan', secrets)
    parallel = P/'audit/parallel-register-reconciliation.json'
    if parallel.is_file():
        state = json.loads(parallel.read_text(encoding='utf-8'))
        if str(state.get('status', '')).startswith('pending'):
            out['remaining_release_gates'].append({'gate': 'parent_independent_register_union',
                'status': state['status'], 'action': state.get('action_pending'),
                'target': state.get('target'), 'reason': state.get('reason')})
        elif 'unavailable' in str(state.get('status', '')):
            out['unavailable_original_comparisons'] = [{
                'status': state['status'], 'target': state.get('target'),
                'reason': state.get('reason'),
                'effect': 'Unavailable original parallel comparison is disclosed; it does not invalidate the complete authoritative consumer scan or impose a pending approval gate.'}]
    out['remaining_release_gates'].append({'gate': 'delivery_container_and_remote_hash_verification',
        'status': 'owned_by_root_after_build', 'note': 'This validator intentionally performs no bundle, manifest or remote hash validation.'})
    out['status'] = 'failed' if out['failures'] else 'passed_local_checks_with_explicit_release_gates'
    out['paid_requests_made'] = 0
    return out

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only', action='store_true', help='Do not rewrite inventoried audit output')
    args = parser.parse_args()
    result = validate()
    if not args.check_only:
        destination = P/OUTPUT
        destination.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'failed_checks': result['failures'],
                      'remaining_release_gates': result['remaining_release_gates'],
                      'audit_written': not args.check_only}, ensure_ascii=False))
    return int(bool(result['failures']))

if __name__ == '__main__':
    raise SystemExit(main())
