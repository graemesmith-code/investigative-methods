import copy
import socket
import unittest
from unittest.mock import patch

from jev_transport import ConfigurationError, JevAdapter


class TransportTests(unittest.TestCase):
    def setUp(self):
        self.network = patch.object(socket.socket, 'connect', side_effect=AssertionError('Network forbidden'))
        self.network.start()
        self.addCleanup(self.network.stop)
        self.calls = []
        self.body = {'model': 'jev-latest', 'messages': [{'role': 'user', 'content': 'fixture'}]}
        self.response = {'model': 'typesafe/jev-fixture-resolved', 'choices': [{'message': {'content': '{}'}}], 'usage': {'prompt_tokens': 7}}

    def adapter(self, route='replit-openrouter', connection='fixture-managed'):
        def send(body):
            self.calls.append(copy.deepcopy(body))
            return copy.deepcopy(self.response)
        return JevAdapter(route=route, send=send, connection_id=connection)

    def test_managed_envelope_preserves_actual_model_and_sources(self):
        result = self.adapter().call(self.body, provenance={'source': 'AP-001', 'sha256': 'fixture'})
        self.assertEqual(self.calls, [self.body])
        self.assertEqual(result['transport']['requested_model'], 'jev-latest')
        self.assertEqual(result['transport']['model'], self.response['model'])
        self.assertEqual(result['transport']['credential_source'], 'replit-managed')
        self.assertEqual(result['transport']['provider'], 'openrouter')
        self.assertEqual(result['provenance']['source'], 'AP-001')
        self.assertEqual(result['response'], self.response)

    def test_direct_payload_and_response_unchanged(self):
        body = {'model': 'jev-1.13.0', 'state': 'x', 'questions': {}}
        self.response = {'model': body['model'], 'answers': {}, 'usage': {'input_tokens': 3}}
        result = self.adapter('typesafe').call(body, provenance={})
        self.assertEqual(self.calls, [body])
        self.assertEqual(result['response'], self.response)
        self.assertEqual(result['transport']['provider'], 'typesafe')

    def test_cache_identity_separates_route_connection_model_and_prompt(self):
        original = self.adapter().request_identity(self.body)['cache_key']
        variants = [self.adapter('typesafe'), self.adapter(connection='another')]
        self.assertTrue(all(a.request_identity(self.body)['cache_key'] != original for a in variants))
        for changed in ({**self.body, 'model': 'pinned'}, {**self.body, 'messages': [{'role': 'user', 'content': 'changed'}]}):
            self.assertNotEqual(self.adapter().request_identity(changed)['cache_key'], original)

    def test_missing_configuration_fails_closed(self):
        for args in ({}, {'send': lambda b: b}, {'send': lambda b: b, 'connection_id': 'fixture', 'route': 'unknown'}):
            with self.assertRaises(ConfigurationError):
                JevAdapter(**args)
        self.assertEqual(self.calls, [])

    def test_native_and_unsupported_requests_rejected_before_send(self):
        for body in ({'model': 'jev-latest', 'state': 'x', 'questions': {}}, {**self.body, 'stream': True}, {**self.body, 'provider': {}}, {**self.body, 'models': ['fallback']}, {'model': 'jev-latest'}, {**self.body, 'model': ''}):
            with self.assertRaises(ConfigurationError):
                self.adapter().call(body, provenance={})
        self.assertEqual(self.calls, [])

    def test_missing_actual_model_is_not_replaced_with_alias(self):
        for model in (None, '', 3):
            self.response['model'] = model
            with self.assertRaises(ConfigurationError):
                self.adapter().call(self.body, provenance={})

    def test_transport_failure_has_no_retry_or_fallback(self):
        def fail(body):
            self.calls.append(body)
            raise TimeoutError()
        adapter = JevAdapter(route='replit-openrouter', send=fail, connection_id='fixture')
        with self.assertRaises(TimeoutError):
            adapter.call(self.body, provenance={})
        self.assertEqual(len(self.calls), 1)

    def test_provenance_is_copied_and_validated_before_send(self):
        source = {'ids': ['one']}
        result = self.adapter().call(self.body, provenance=source)
        source['ids'].append('two')
        self.assertEqual(result['provenance'], {'ids': ['one']})
        with self.assertRaises(ValueError):
            self.adapter().call(self.body, provenance={'bad': float('nan')})
        self.assertEqual(len(self.calls), 1)


if __name__ == '__main__':
    unittest.main()
