"""Offline-testable Jev-only adaptation; no live transport is exposed yet."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location('sanctions_budget_base', ROOT / 'code/ati/pipeline.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.ENDPOINTS = {'jev': 'https://api.typesafe.ai/v1/systemone'}
base.CAP = 9_000_000
base.VERSION = 'sanctions-pilot-2026-10-07'

def ledger(path):
    return base.Ledger(path, mode=base.VERSION, prior={'jev': 0})

class Client(base.Client):
    def call(self, provider, body):
        if provider != 'jev':
            raise base.GuardError('Only Jev is authorized')
        return super().call(provider, body)

def validated_passage(source, passage):
    """Exact-text check only; never establishes a corporate relationship."""
    return bool(passage) and passage in source
