"""Deterministic search aids; candidates are literal spans, not verified entities."""
import csv, json, pathlib, re
P=pathlib.Path(__file__).parent/'corpus'
DATE=re.compile(r'\b(?:\d{4}-\d{1,2}-\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}|\d{1,2}[- ](?:January|February|March|April|May|June|July|August|September|October|November|December|janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)[- ]\d{4})\b',re.I)
IDENT=re.compile(r'\b(?:[A-Z]{2,8}\d{4}-\d{5,9}|A-\d{4}-\d{3,8}|\d{4,6}-\d{4}|[A-Z]\d{4}-[A-Z0-9]{4,}(?:/[A-Z])?)\b')
ENTITY=re.compile(r'\b(?:[A-ZÀ-ÖØ-Þ][\wÀ-ÿ’\'-]+(?:\s+(?:of|the|de|du|des|and|et|[A-ZÀ-ÖØ-Þ][\wÀ-ÿ’\'-]+)){1,6}|[A-Z]{2,8})\b')
def spans(pattern,text):
    return [{'text':m.group(),'start':m.start(),'end':m.end()} for m in pattern.finditer(text)]
def main():
    rows=json.loads((P/'records.json').read_text());out=[]
    for r in rows:
        item={'_id':r['_id'],'owner_org':r['owner_org'],'request_number':r['request_number'],'closure_year':r['year'],'closure_month':r['month'],'disposition':r['disposition'],'pages':r['pages'],'access_stratum':('disclosed_positive_pages' if r['pages']>0 else 'disclosed_zero_pages') if r['disposition'] in ['DA','DP'] else r['disposition'],'language_spans':{}}
        for field in ['summary_en','summary_fr']:
            text=r[field] or ''
            item['language_spans'][field]={'dates_literal':spans(DATE,text),'identifiers_literal':spans(IDENT,text),'entity_candidates_literal':spans(ENTITY,text)}
        out.append(item)
    (P/'literal-search-aids.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    # Candidate entity spans overcapture title case and miss lowercase names.
    # Date spans preserve ambiguity, and year-like identifiers are not dates.
    print(json.dumps({'records':len(out),'records_with_dates':sum(any(v['dates_literal'] for v in r['language_spans'].values()) for r in out),'records_with_identifiers':sum(any(v['identifiers_literal'] for v in r['language_spans'].values()) for r in out)}))
if __name__=='__main__': main()
