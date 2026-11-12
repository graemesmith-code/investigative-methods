"""Synthetic labels test software behavior only, never editorial performance."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
import benchmark as b


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.packet = self.root / 'packet'
        self.rows = b.prepare(self.packet)

    def label_file(self, rows=None, value='2'):
        path = self.root / 'synthetic-labels.csv'
        records = [{k: '' for k in b.LABEL_FIELDS} for _ in (rows or self.rows)]
        for label, record in zip(records, rows or self.rows):
            label.update(blind_id=record['blind_id'], reviewer_id='SYNTHETIC_FIXTURE',
                         followup=value, rationale='Synthetic software-test label; not an editorial judgment')
        b.write_csv(path, b.LABEL_FIELDS, records)
        return path

    def test_exact_sample_and_reproducibility(self):
        other = self.root / 'other'
        b.prepare(other)
        for path in self.packet.rglob('*'):
            if path.is_file():
                self.assertEqual(path.read_bytes(), (other / path.relative_to(self.packet)).read_bytes())
        self.assertEqual(len(self.rows), 100)
        self.assertEqual({r['_id'] for r in self.rows}, {r['_id'] for r in b.load_source()})

    def test_blinding_and_bottom_inclusion(self):
        with (self.packet / 'reviewer' / 'records.csv').open() as f:
            records = list(csv.DictReader(f))
        self.assertEqual(set(records[0]), {'blind_id', *b.VISIBLE})
        self.assertFalse(set(b.AXES) & set(records[0]))
        selection = json.loads((self.packet / 'coordinator' / 'starter-selection.json').read_text())
        self.assertEqual(b.Counter(r['band'] for r in selection), {'top': 10, 'middle': 10, 'bottom': 10})
        self.assertEqual(len({r['blind_id'] for r in selection}), 30)
        status = json.loads((self.packet / 'status.json').read_text())
        self.assertIsNone(status['performance_metrics'])

    def test_blank_and_partial_labels_rejected(self):
        with self.assertRaises(ValueError):
            b.evaluate(self.packet, self.packet / 'reviewer' / 'labels.csv', 'followup', [10])
        with self.assertRaises(ValueError):
            b.evaluate(self.packet, self.label_file(self.rows[:30]), 'followup', [10])

    def test_known_metrics_and_null_denominators(self):
        ranking = [{'blind_id': str(i)} for i in range(4)]
        m = b.metrics(ranking, {'0': 3, '1': 2, '2': 1, '3': 0}, 2)
        self.assertEqual(m['precision_at_k'], 1)
        self.assertEqual(m['recall_at_k'], 1)
        self.assertEqual(m['ndcg_at_k'], 1)
        m = b.metrics(ranking, {str(i): 0 for i in range(4)}, 2)
        self.assertEqual(m['precision_at_k'], 0)
        self.assertIsNone(m['recall_at_k'])
        self.assertIsNone(m['ndcg_at_k'])

    def test_complete_fixture_and_bottom_audit(self):
        result = b.evaluate(self.packet, self.label_file(), 'followup', [10, 20])
        self.assertEqual(result['n'], 100)
        self.assertEqual(len(result['bottom_quintile']['positive_records']), 20)
        self.assertEqual(result['rankings']['rank_score']['10']['recall_at_k'], 0.1)
        self.assertEqual(set(result['by_department']), {'dfatd-maecd', 'dnd-mdn'})

    def test_bad_labels_and_metadata_rejected(self):
        for value in ('nan', '4', '2.5', 'unknown'):
            with self.assertRaises(ValueError):
                b.evaluate(self.packet, self.label_file(value=value), 'followup', [10])
        labels = self.label_file()
        with labels.open() as f:
            records = list(csv.DictReader(f))
        records[0]['novelty'] = '2'
        b.write_csv(labels, b.LABEL_FIELDS, records)
        with self.assertRaises(ValueError):
            b.evaluate(self.packet, labels, 'followup', [10])
        records[0]['novelty'] = 'unknown'
        records[0]['reviewer_id'] = 'OTHER'
        b.write_csv(labels, b.LABEL_FIELDS, records)
        with self.assertRaises(ValueError):
            b.evaluate(self.packet, labels, 'followup', [10])

    def test_invalid_k_and_packet_tampering(self):
        for k in (0, 101):
            with self.assertRaises(ValueError):
                b.evaluate(self.packet, self.label_file(), 'followup', [k])
        path = self.packet / 'coordinator' / 'records.json'
        rows = json.loads(path.read_text())
        rows[0]['rank_score'] = 99
        b.dump(path, rows)
        with self.assertRaises(ValueError):
            b.evaluate(self.packet, self.label_file(), 'followup', [10])

    def test_rules_bilingual_dedup_and_no_truth_gate(self):
        r = dict(summary_en='contract', summary_fr='contrat', disposition='NE', pages=0)
        self.assertEqual(b.baseline(r)['rules_text'], 1)
        self.assertEqual(b.baseline(r)['rules_availability'], 0)
        r.update(summary_en='enforcement compliance order', summary_fr='non-conformité')
        self.assertEqual(b.baseline(r)['rules_text'], 2)


if __name__ == '__main__':
    unittest.main()
