from pathlib import Path
import json,hashlib,re
root=Path('.')
head='''SPINE STAGE 2: TECHNICAL ARCHITECTURE GAPS AND COMPLETE LEDGER
Research date: 16 November 2026
Public-source, bounded recovery and gap-filling run

READ THIS FIRST
We found more actual engineering than the earlier record showed. Britain publishes a detailed architecture separating authorization, interlocks and weapon-release scheduling. A Rigby patent provides a plausible match for safe control of unmanned weapons over unreliable links. RCH155 has an onboard ballistic computer, and existing British fire-control software does more than display warnings. These findings narrow the uncertainty; they do not connect a particular patented protection to a purchased weapon's verified configuration.

The remaining accountability question is concrete: what did the customer require, who tested the delivered build, and what evidence can an independent reviewer or Parliament inspect? Public policy and patents cannot answer that alone. Neither missing public evidence nor a patent withdrawal proves that a safeguard was omitted.

WHAT CHANGED
1. Rigby/Pyramid: US9156552B2 tests remote-command age; it is a strong candidate, not explicitly confirmed as the patent meant in the biography. The complete official Pyramid standard and guidance were preserved. Specific components define authorization, interlocks and release scheduling. No deployed configuration or patent-to-Pyramid implementation was established.
2. RCH155: manufacturer evidence distinguishes onboard ballistic computation from the external artillery command connection. CGI describes distributed fire-safety functions; DE&S describes a human safety-officer check. Calling this 'only a map warning' would overstate the gap. No reviewed acceptance record demonstrates the protected-area blocking mechanism in the British/German purchased build. ADLER must not be asserted to be the onboard computer.
3. Boxer: public architecture and SafeNGVA work supply useful institutional leads, but no recovered current contractual GVA standard or acceptance record proves the precise independent inhibit in the UK RS4 build. A hardware safety barrier does not automatically mean dedicated wiring for every signal.
4. DragonFire: QinetiQ's laser-source and safe-testing work is documented. BAE's precise production work package, and a link to its collateral-risk patent, remain unestablished. A refusal to disaggregate cost is not a refusal to release safety tests.
5. Task1: original German claims13–17 now close the translation-numbering problem; the EPO XML is bibliographic only. INPI records were substantive, with a French revocation entry for Naval Group EP3812690 distinct from FR3102239. The NPS-hosted Wu/Srivastava paper has five Raytheon-affiliated authors; it is not an NPS-authored paper. The BMVg public directive was recovered from a clearly identified public mirror.
6. Oversight: JSP936 paragraph99 requires annual organizational assurances, not a public statement per weapon; paragraph105 recommends independent assurance. Bundestag21/5159 Q52 permits authorized classified inspection;21/9054 Q10 withholds the specified test-method details even classified. These are different access decisions.

OUTSTANDING
RENK retry, GhostPlay ex-ante raw notice/TED XML and the ACTS raw award notice remain acquisition gaps. Full current normative/contracted GVA details, named-system independent acceptance evidence, exact BAE DragonFire role, and deployed patent implementations remain open. A search-index excerpt is not a preserved original; an ex-ante transparency notice is not an executed contract.

PERSISTENCE / INTEGRITY
Destination: https://drive.google.com/drive/folders/1j6bqtnpdci7RGLLS-O7ksLU2-bbWgG2O
Methods repository: https://github.com/graemesmith-code/investigative-methods/tree/main/research/2026-11-16/uk-german-spine-recovery
Raw source files were acquired and uploaded incrementally by task; manifests and notes were checkpointed to GitHub. Existing sharing permissions were not changed. No outreach, FOI filing, accounts, payment or security-challenge bypass occurred. This report contains proposed questions only.
Two direct HTML uploads changed byte size: QinetiQ49909 local versus49911 Drive; Royal Navy134512 local versus134513 Drive. They are NOT byte-verified originals. The correct unchanged originals are INSIDE unchanged_html_originals.zip, Drive1Oc3H-PRh_osqWcBwnSPyckcKCp7CxqEm,184633 bytes, SHA256530c5bc4e5bf42824204f414fff4fa3681b5bfb5e8d4025f52d386f7a2b622c7. The ZIP's remote size was verified. Its member hashes are the original source hashes in the ledger. Hashes generally describe locally acquired bytes; remote size/parent verification is not an independent remote SHA256 verification.
Stage1 inventory is retained from its committed report; this run did not redownload every Stage1 Drive object. Historical verification should not be mistaken for fresh remote verification. Later Stage2 corrections take precedence over earlier wording.

CONTENTS
I. Detailed Task1 completion and Gaps1–4
II. Proposed right-to-reply and parliamentary questions (unsent)
III. Combined Stage1 + Stage2 source/checksum inventory
IV. Methods and exact query logs (returned result counts are not corpus totals)

'''
parts=[head,'\nI. DETAILED FINDINGS\n']
for p in ['stage2_records/TASK1_FINDINGS.txt','stage2_rigby/FINDINGS.txt','stage2_rch/FINDINGS.txt','stage2_boxer/FINDINGS_AND_MANIFEST.txt','stage2_dragonfire/findings.txt']:
 parts+=['\n'+'='*72+'\n'+Path(p).read_text()]
parts+=['\nII. PROPOSED QUESTIONS\n',Path('stage2_questions/PRECISION_QUESTIONS.txt').read_text()]
s1=Path('stage2_questions/STAGE1_RECOVERED.txt').read_text(); inv=s1[s1.index('PART II: CONSOLIDATED'):s1.index('PART III: FULL MANIFESTS')]
parts+=['\nIII. MASTER SOURCE AND CHECKSUM INVENTORY\n\nSTAGE1 INVENTORY (carried forward from committed report)\n',inv]
parts+=['\nSTAGE2 INVENTORY\n']
files=['stage2_records/manifest.json','stage2_rigby/manifest.json','stage2_rch/manifest.json','stage2_boxer/acquisition.json','stage2_dragonfire/manifest_verified.json']
for p in files:
 records=json.loads(Path(p).read_text());parts+=['\nSEGMENT '+p+'\n']
 for r in records:
  name=r.get('name',r.get('file'));url=r.get('source_url',r.get('url'));did=r.get('drive_id');v=r.get('verification',{}).get('structuredContent',{});size=v.get('size',r.get('verified_drive_bytes',r.get('drive_size_verified')))
  if name=='B02_Rheinmetall_Boxer_UK.pdf':did='196aOWv2f-x1MKQiIaq3gxLaiiz9ji7zt';size=r['bytes']
  if name=='B03_LOSA.pdf':did='1LH5TPYPGB_6_MDszxEq6kBJEsqDQRDDv';size=r['bytes']
  parts+=[f"\nFILE: {name}\nSource: {url}\nRetrieved UTC: {r.get('timestamp',r.get('time_utc',r.get('utc','see acquisition record')))}\n"]
  if did:
   status='size verified (see segment manifest)' if isinstance(size,bool) else str(size)
   parts+=[f"MIME: {r.get('mime')}\nOriginal bytes: {r.get('bytes')}\nSHA-256: {r.get('sha256')}\nDrive ID: {did}\nDrive size: {status}\nPreserved copy: https://drive.google.com/file/d/{did}/view\n"]
   if name in ['qinetiq.html','RN.html']:parts+=['INTEGRITY WARNING: direct HTML upload size differs. Use original member in ZIP1Oc3H-PRh_osqWcBwnSPyckcKCp7CxqEm, not this direct HTML copy.\n']
  else:parts+=['Acquisition / preservation status: '+json.dumps(r,ensure_ascii=False)+'\n']
parts+=['\nDERIVED PRESERVATION CONTAINER: unchanged_html_originals.zip\nDrive ID: 1Oc3H-PRh_osqWcBwnSPyckcKCp7CxqEm\nBytes:184633\nMIME:application/zip\nSHA256:530c5bc4e5bf42824204f414fff4fa3681b5bfb5e8d4025f52d386f7a2b622c7\nMembers: qinetiq.html and RN.html; unchanged source bytes with original source URLs/hashes above. Container is not itself an independently published primary document.\n']
parts+=['\nIV. METHODS / EXACT QUERY LOGS\nDates/times, exact search strings and exposed result counts follow. Missing totals remain unknown, not zero. Large search-response bodies are omitted here; original checkpoint query logs remain in GitHub. Source requests and failures are listed above.\n']
for p in ['stage2_records/query_log.json','stage2_rigby/query_log.json','stage2_rch/query_log.json','stage2_dragonfire/query_log_final.json']:
 obj=json.loads(Path(p).read_text())
 def trim(x):
  if isinstance(x,list):return [trim(v) for v in x]
  if isinstance(x,dict):return {k:trim(v) for k,v in x.items() if k not in ['response','results','content','tool_response','raw_response','raw_result','search_response']}
  return x
 parts+=['\n'+p+'\n'+json.dumps(trim(obj),ensure_ascii=False,indent=2)+'\n']
# Append Boxer query log supplied separately when available.
for p in ['stage2_boxer/query_log.json']:
 if Path(p).exists():parts+=['\n'+p+'\n'+Path(p).read_text()]
parts+=['\nACQUISITION MANIFESTS (machine-readable corroboration of inventory and blockers)\n']
for p in files:
 parts+=['\n'+p+'\n'+Path(p).read_text()+'\n']
parts+=['\nEND. No proposed outreach executed.\n']
out=Path('SPINE_STAGE2_GAPS_AND_COMPLETE_LEDGER_2026-11-16.txt');out.write_text(''.join(parts));print(out,len(out.read_bytes()),hashlib.sha256(out.read_bytes()).hexdigest())
