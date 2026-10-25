#!/usr/bin/env python3
"""Extract exact source sections from F4-audit.txt to a new output directory.
No network; refuses overwrite and unsafe paths. Decompressed sources lose .gz suffix.
Usage: python3 extract_compendium_sections.py F4-audit.txt extracted-results
"""
import argparse,hashlib,json,pathlib,re
def main():
 ap=argparse.ArgumentParser();ap.add_argument('compendium');ap.add_argument('output_directory');a=ap.parse_args();root=pathlib.Path(a.output_directory);root.mkdir(parents=True,exist_ok=True);pending=None;result=[]
 with open(a.compendium,'rb') as f:
  while True:
   line=f.readline()
   if not line:break
   m=re.fullmatch(rb'([FS][0-9]{4})  (.+)\n',line)
   if m:pending={'section':m[1].decode(),'source':m[2].decode('utf-8')};continue
   if not pending:continue
   if line.startswith(b'Representation: '):pending['representation']=line[16:].decode().strip()
   elif line.startswith(b'Content bytes: '):pending['bytes']=int(line[15:])
   elif line.startswith(b'Content SHA-256: '):pending['sha256']=line[17:].decode().strip()
   elif line in (b'BEGIN SOURCE CONTENT\n',b'BEGIN DERIVED CONTENT\n'):
    assert {'bytes','sha256'}<=pending.keys();rel=pathlib.PurePosixPath(pending['source']);assert not rel.is_absolute() and '..' not in rel.parts;name=str(rel)
    if pending.get('representation') in ('full_decompressed_utf8','json_whitespace_compacted') and name.endswith('.gz'):name=name[:-3]
    dst=root/name;assert not dst.exists(),'Refusing overwrite: '+str(dst);dst.parent.mkdir(parents=True,exist_ok=True);n=pending['bytes'];h=hashlib.sha256()
    with dst.open('xb') as out:
     while n:
      b=f.read(min(n,1048576));assert b,'Unexpected EOF';out.write(b);h.update(b);n-=len(b)
    assert h.hexdigest()==pending['sha256'],'Corrupt section: '+name
    assert f.readline()+f.readline() in (b'\nEND SOURCE CONTENT\n',b'\nEND DERIVED CONTENT\n')
    pending['extracted_path']=name;result.append(pending);pending=None
 assert result,'No sections';mp=root/'extraction-manifest.json';assert not mp.exists();mp.write_text(json.dumps({'verified_sections':len(result),'files':result},indent=2)+'\n');print(json.dumps({'verified_sections':len(result),'output_directory':str(root)},indent=2))
if __name__=='__main__':main()
