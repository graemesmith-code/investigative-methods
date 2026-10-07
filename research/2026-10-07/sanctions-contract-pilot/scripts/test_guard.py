import tempfile
import unittest
from pathlib import Path
import guard as g

BODY = {'model': 'jev-1.13.0', 'state': 'SYNTHETIC CONTROL',
        'questions': {'fact': {'type': 'noul', 'instructions': 'Is a payment explicitly documented?'}}}
ANSWER = {'model': 'jev-1.13.0', 'usage': {'input_tokens': 100},
          'answers': {'fact': {'type': 'noul', 'noul': 0.01}}}

class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.l = g.ledger(Path(self.tmp.name) / 'ledger.sqlite')
    def tearDown(self):
        self.l.db.close()
        self.tmp.cleanup()
    def test_other_provider_blocked_before_transport(self):
        with self.assertRaises(g.base.GuardError):
            g.Client(self.l, lambda *_: self.fail('transport reached')).call('exa', BODY)
    def test_uncertain_retains_reservation_blocks_retry(self):
        def fail(*_): raise TimeoutError()
        c = g.Client(self.l, fail)
        with self.assertRaises(TimeoutError): c.call('jev', BODY)
        self.assertEqual(self.l.totals()['jev'], 3000)
        with self.assertRaises(g.base.GuardError): c.call('jev', BODY)
    def test_cap_reservation(self):
        self.l.reserve('jev', 'first', BODY, 9_000_000)
        self.l.finish(1, {}, {}, 9_000_000, 'fixture')
        with self.assertRaises(g.base.GuardError): self.l.reserve('jev', 'second', BODY, 3000)
    def test_success_cached_and_rounded_up(self):
        calls = []
        def transport(*_): calls.append(1); return ANSWER
        c = g.Client(self.l, transport)
        c.call('jev', BODY); c.call('jev', BODY)
        self.assertEqual(len(calls), 1)
        self.assertEqual(self.l.totals()['jev'], 5)
    def test_invalid_usage_stops_and_retains(self):
        answer = {**ANSWER, 'usage': {'input_tokens': 64001}}
        with self.assertRaises(g.base.GuardError): g.Client(self.l, lambda *_: answer).call('jev', BODY)
        self.assertEqual(self.l.totals()['jev'], 3000)
    def test_exact_passage_rejects_invention(self):
        self.assertFalse(g.validated_passage('A shares an address with B.', 'A owns B.'))
        self.assertFalse(g.validated_passage('A shares an address with B.', ''))
        self.assertTrue(g.validated_passage('A owns 60% of B.', 'A owns 60% of B.'))

if __name__ == '__main__': unittest.main()
