"""Optional transport boundary. No credentials, SDK imports, or import-time I/O.

The existing pipeline and its direct TypeSafe budget remain unchanged.
Managed connection and Jev's OpenRouter request construction belong to the
workspace integration; this module does not infer either contract.
"""
import copy
import hashlib
import json


class ConfigurationError(ValueError):
    pass


def packed(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


class JevAdapter:
    """send takes a JSON request and returns a decoded JSON response.

    For typesafe, pass a wrapper around the existing transport('jev', body).
    For replit-openrouter, pass the workspace's verified managed connection.
    Neither path retries or falls back. Results must be persisted as envelopes.
    """

    def __init__(self, *, route='typesafe', send=None, connection_id=None):
        if route not in ('typesafe', 'replit-openrouter'):
            raise ConfigurationError('Unknown Jev route')
        if not callable(send):
            raise ConfigurationError('An explicitly configured send callable is required')
        if not isinstance(connection_id, str) or not connection_id.strip():
            raise ConfigurationError('A non-secret connection identifier is required')
        self.route, self.send, self.connection_id = route, send, connection_id

    def request_identity(self, body):
        if not isinstance(body, dict) or not isinstance(body.get('model'), str) or not body['model'].strip():
            raise ConfigurationError('Explicit request model required')
        if self.route == 'replit-openrouter':
            if 'state' in body or 'questions' in body:
                raise ConfigurationError('Native TypeSafe payload cannot be sent as OpenRouter chat')
            if not isinstance(body.get('messages'), list) or not body['messages']:
                raise ConfigurationError('Workspace-verified OpenRouter messages required')
            if body.get('stream', False) is not False:
                raise ConfigurationError('Only non-streaming responses supported')
            if any(k in body for k in ('provider', 'models', 'route')):
                raise ConfigurationError('Routing/privacy overrides are outside this boundary')
        identity = {'route': self.route,
                    'provider': 'typesafe' if self.route == 'typesafe' else 'openrouter',
                    'credential_source': 'direct' if self.route == 'typesafe' else 'replit-managed',
                    'connection_id': self.connection_id, 'requested_model': body['model'],
                    'request_sha256': hashlib.sha256(packed(body).encode()).hexdigest()}
        identity['cache_key'] = hashlib.sha256(packed(identity).encode()).hexdigest()
        return identity

    def call(self, body, *, provenance):
        if not isinstance(provenance, dict):
            raise ConfigurationError('Source/run provenance must be a dictionary')
        request = copy.deepcopy(body)
        sources = copy.deepcopy(provenance)
        packed(sources)  # Reject non-JSON provenance before invoking transport.
        identity = self.request_identity(request)
        response = self.send(request)
        if not isinstance(response, dict) or not isinstance(response.get('model'), str) or not response['model'].strip():
            raise ConfigurationError('Response must report its actual model identifier')
        return {'transport': {**identity, 'model': response['model']},
                'provenance': sources, 'response': response}
