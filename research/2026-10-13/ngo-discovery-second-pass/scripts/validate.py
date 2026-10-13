#!/usr/bin/env python3
"""Offline package/audit checks; no research, network or model calls."""
import hashlib,json,pathlib,re,subprocess,sys,urllib.parse
BASE=pathlib.Path(__file__).resolve().parents[1]
REPO=pathlib.Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=BASE,text=True).strip())
PREFIX=str(BASE.relative_to(REPO))+'/'
ORIGINAL='22ed3314d612f880f16608ed1349fe79cd278238'
AUDIT='research/2026-10-13/ngo-discovery-opportunities'
errors=[]
for p in BASE.rglob('*.json'):
    try: json.loads(p.read_text())
    except Exception as e: errors.append(f'{p.relative_to(BASE)}: {e}')
for p in BASE.rglob('*.md'):
    for target in re.findall(r'\]\(([^\n]+?)\)',p.read_text()):
        target=target.strip().split(' "')[0]
        if urllib.parse.urlsplit(target).scheme or target.startswith('#'): continue
        clean=urllib.parse.unquote(target.split('#')[0])
        if not (p.parent/clean).exists(): errors.append(f'{p.relative_to(BASE)} missing target {target}')
manifest=BASE/'file-manifest.json'
if manifest.exists():
    for item in json.loads(manifest.read_text())['files']:
        p=BASE/item['path']; actual=hashlib.sha256(p.read_bytes()).hexdigest()
        if actual!=item['sha256'] or p.stat().st_size!=item['bytes']: errors.append('manifest mismatch '+item['path'])
else: errors.append('missing file manifest')
old=subprocess.check_output(['git','rev-parse',ORIGINAL+':'+AUDIT],cwd=REPO,text=True).strip()
current=subprocess.check_output(['git','rev-parse','HEAD:'+AUDIT],cwd=REPO,text=True).strip()
if old!=current: errors.append('old audit tree changed')
if subprocess.check_output(['git','diff',ORIGINAL,'--',AUDIT],cwd=REPO): errors.append('old audit working/index bytes changed')
changed=subprocess.check_output(['git','diff','--name-only',ORIGINAL],cwd=REPO,text=True).splitlines()
untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=REPO,text=True).splitlines()
for path in changed+untracked:
    if not path.startswith(PREFIX): errors.append('outside scope: '+path)
if errors:
    print('\n'.join(errors));sys.exit(1)
print('PASS: JSON, relative links, manifest hashes, old audit identity, changed-path confinement')
print('Preserved audit tree:',old)
