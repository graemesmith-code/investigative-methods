#!/usr/bin/env python3
"""Bounded synthetic check; accepts the exact reviewed scorer, never imports it.

Usage: python3 synthetic-scoring-check.py /path/to/evaluate_deonticbench.py
No inference, repository installation, harness, file fixtures or generated code.
"""
import ast
import hashlib
import json
from pathlib import Path
import sys

PIN = '2fe3aa40bf856d533a79a6052a28eb3fc1b618f1'
# Filled from the acquired and manually reviewed file at PIN.
SHA256 = 'e6fe526d269f37f6c19d017819fe8bd6009cd9c2a8f08a4639a72c7d38f45ea2'

def main():
    source = Path(sys.argv[1]).read_bytes()
    if hashlib.sha256(source).hexdigest() != SHA256:
        raise SystemExit('Refusing unreviewed scorer bytes; obtain the pinned source.')
    tree = ast.parse(source)
    names = {'_macro_f1', '_compute_row'}
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    if {n.name for n in functions} != names:
        raise SystemExit('Reviewed function set missing')
    limited = {'sorted': sorted, 'sum': sum, 'len': len, 'list': list,
               'tuple': tuple, 'dict': dict, 'str': str, 'bool': bool}
    namespace = {'__builtins__': limited,
                 'ACCURACY_DATASETS': ('sara-numeric', 'airline')}
    exec(compile(ast.Module(body=functions, type_ignores=[]),
                 'reviewed-pure-scoring-functions', 'exec'), namespace)
    accuracy = [('', '', True), ('10', '10', False)]
    f1 = [('yes', 'yes', False), ('no', 'yes', False), ('', '', True)]
    score = namespace['_compute_row']
    result = {'pin': PIN, 'accuracy_fixture': accuracy, 'f1_fixture': f1,
              'default_accuracy': score('synthetic', 'airline', accuracy),
              'strict_accuracy': score('synthetic', 'airline', accuracy, strict=True),
              'strict_f1': score('synthetic', 'sara-binary', f1, strict=True)}
    assert result['default_accuracy']['score'] == 1.0
    assert result['strict_accuracy']['score'] == 0.5
    assert result['strict_f1']['n'] == 3
    assert abs(result['strict_f1']['score'] - 1/3) < 1e-12
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
