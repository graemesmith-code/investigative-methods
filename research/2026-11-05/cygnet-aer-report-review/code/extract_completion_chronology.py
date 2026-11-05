"""Original executed extraction code, preserved verbatim below this docstring.

Run from the workspace directory containing aer-reports/. Requires existing
page-text JSON inputs (list of {page, text}) generated separately from PDFs.
Python standard library only. Writes completion_chronology_raw.json and prints
source frac-summary excerpts and the extracted row count.

LIMITATIONS: This is a raw index, not a validated chronology. Glob selection is
specific to this document set. Input order follows filesystem glob order; output
is not chronologically sorted. Rows require HH:MM HH:MM decimal-hours 'h'. Text
is appended until another matching row or the page ends, excluding copyright
lines. Continuation text before the first row on a new page is not attached to
the prior page's row. Source errors, placeholders, duplicate/copy-forward rows,
overlapping intervals and malformed times remain unchanged. Midnight crossings
are not resolved. No time-zone conversion or earthquake matching is performed.
No inferred corrections, deduplication, causal analysis or totals are applied.
Review original PDF pages before relying on any entry. Output overwrites the
same local filename on rerun. No network or external write is performed.
"""
import json,glob,re
out=[]
for f in glob.glob('aer-reports/TR,334585[235]*.json'):
 pgs=json.load(open(f));lic=f.split(',')[2]
 for p in pgs:
  t=p['text'];date=re.search(r'Report - (\d{4}-\d\d-\d\d)',t)[1]
  if 'Frac Summary' in t:
   z=t[t.index('Frac Summary'):];print(lic,'PAGE',p['page'],re.sub(' +',' ',z[:1200]))
  cur=None
  for l in t.splitlines():
   m=re.match(r'\s*(\d\d:\d\d)\s+(\d\d:\d\d)\s+([\d.]+) h\s*(.*)',l)
   if m:
    cur={'file':f.split('/')[-1].replace('.json','.pdf'),'license':lic,'page':p['page'],'date':date,'from':m[1],'to':m[2],'duration_hours_as_reported':m[3],'text':m[4].strip()};out.append(cur)
   elif cur and l.strip() and not l.startswith('©'):cur['text']+='\n'+l.strip()
json.dump(out,open('aer-reports/completion_chronology_raw.json','w'),indent=2)
print('records',len(out))
