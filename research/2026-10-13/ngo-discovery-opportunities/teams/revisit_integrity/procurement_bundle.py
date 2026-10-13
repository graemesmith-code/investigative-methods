#!/usr/bin/env python3
"""Read-only bounded public bundle acquisition. No personal contents in committed output."""
import urllib.request,urllib.parse,json,pathlib,hashlib,concurrent.futures,zipfile,io,re,subprocess
P=pathlib.Path(__file__).parent;C=pathlib.Path('/tmp/ngo-revisit-integrity');C.mkdir(exist_ok=True)
URL='https://public.api.openprocurement.org/api/2.5/tenders/bc2b85df808042fa8157d6ddbf79d0c6'
def get(u):
 b=urllib.request.urlopen(u,timeout=35).read();h=hashlib.sha256(b).hexdigest();(C/h).write_bytes(b);return b,h
def parse(b,h):
 chars=0;pages=None;archive_members=[]
 if b.startswith(b'%PDF'):
  f=C/(h+'.pdf');f.write_bytes(b);t=C/(h+'.txt');r=subprocess.run(['pdftotext','-layout',str(f),str(t)],capture_output=True)
  if r.returncode==0:s=t.read_text(errors='replace');chars=len(s);pages=s.count('\f')
 elif b.startswith(b'PK'):
  try:
   z=zipfile.ZipFile(io.BytesIO(b))
   if 'word/document.xml' in z.namelist():
    s=re.sub('<[^>]+>',' ',z.read('word/document.xml').decode());(C/(h+'.txt')).write_text(s);chars=len(s)
   else:
    for n in z.namelist():
     if n.endswith('/'):continue
     info=z.getinfo(n)
     if info.file_size>25000000:continue
     bb=z.read(n);hh=hashlib.sha256(bb).hexdigest();(C/hh).write_bytes(bb);cc,pp,_=parse(bb,hh);archive_members.append(dict(sha256=hh,bytes=len(bb),extension=pathlib.Path(n).suffix,text_characters=cc,pages=pp))
  except Exception:pass
 return chars,pages,archive_members
b,th=get(URL);t=json.loads(b)['data'];docs=[]
for scope,arr in [('tender',t.get('documents',[]))]+[(field+':'+r['id'],r.get('documents',[])+r.get('eligibilityDocuments',[])+r.get('qualificationDocuments',[])) for field in ['bids','awards'] for r in t.get(field,[])]:
 for d in arr:
  docs.append(dict(scope=scope,id=d['id'],format=d.get('format'),datePublished=d.get('datePublished'),dateModified=d.get('dateModified'),documentOf=d.get('documentOf'),relatedItem=d.get('relatedItem'),declared_hash=d.get('hash'),canonical_path=urllib.parse.urlunsplit(urllib.parse.urlsplit(d['url'])._replace(query='')),live_url=d['url'],title=d.get('title'),confidentiality=d.get('confidentiality','public')))
# All non-signature documentary items acquired. Explicitly public only; title classified internally and not published.
def one(d):
 out={k:v for k,v in d.items() if k not in ['live_url','title']}
 if d['confidentiality']!='public':out['acquisition_status']='excluded_nonpublic';return out
 if d['format']=='application/pkcs7-signature':out['acquisition_status']='signature_container_metadata_only';return out
 try:
  b,h=get(d['live_url']);cc,pp,aa=parse(b,h);out.update(acquisition_status='acquired',bytes=len(b),sha256=h,text_characters=cc,pages=pp,archive_members=aa)
  if 'правовідносин' in d['title'].lower():out['document_category']='employment_relationship_evidence_archive'
  elif 'працівників' in d['title'].lower():out['document_category']='staffing_evidence'
 except Exception as e:out.update(acquisition_status='failed',error=str(e))
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:checks=list(ex.map(one,docs))
result=dict(url=URL,tender_response_sha256=th,tender_response_bytes=len(b),tenderID=t['tenderID'],tender_id=t['id'],lot_ids=[l['id'] for l in t.get('lots',[])],bid_ids=[x['id'] for x in t.get('bids',[])],award_ids=[x['id'] for x in t.get('awards',[])],tenderPeriod=t.get('tenderPeriod'),submission_dates=[x.get('submissionDate') for x in t.get('bids',[])],award_dates=[x.get('date') for x in t.get('awards',[])],revisions_present='revisions' in t,complaint_count=len(t.get('complaints',[])),documents_total=len(docs),checks=checks,limitations=['Current snapshot is not an immutable complete revision archive.','Signature containers not separately downloaded; native documents preserve documentary contents.','Uploaded after submission deadline includes winner-stage evidence; publication date is not automatic proof of untimely bidder evidence.','Extracted text is not a human certification of legal eligibility.'])
(P/'procurement-bundle.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print('total',len(docs),'acquired',sum(x['acquisition_status']=='acquired' for x in checks),'metadata_signatures',sum(x['acquisition_status']=='signature_container_metadata_only' for x in checks),'failed',sum(x['acquisition_status']=='failed' for x in checks))
