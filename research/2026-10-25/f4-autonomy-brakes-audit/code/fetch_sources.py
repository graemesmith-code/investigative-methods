#!/usr/bin/env python3
"""Hash public documents; retain full third-party bodies in private scratch only."""
import concurrent.futures,datetime,hashlib,json,pathlib,urllib.request
P=pathlib.Path(__file__).resolve().parents[1]; CACHE=pathlib.Path('/workspace/scratch/f4-sources');CACHE.mkdir(parents=True,exist_ok=True)
SOURCES={
 'nspm11':'https://www.govinfo.gov/content/pkg/DCPD-202600387/html/DCPD-202600387.htm',
 'directive300009':'https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodd/300009p.pdf',
 'gao2026':'https://www.gao.gov/products/gao-27-107837',
 'teelaws-sbir':'https://www.sbir.gov/awards/215327',
 'teelaws-army':'https://www.army.mil/article/291926/cadets_work_with_software_using_lethal_autonomous_weapons_systems_that_analyzes_tactical_decisions_provides_ethical_score',
 'camp-navy':'https://www.navy.mil/Press-Office/News-Stories/display-news/Article/4608456/navy-demonstrates-collaborative-autonomy-mission-planning-for-future-combat-air/',
 'camp-vendor':'https://www.ga-asi.com/ga-asi-selected-by-us-navy-pma-281-for-collaborative-autonomy-mission-planning-and-debrief-project',
 'cate-architecture':'https://www.sei.cmu.edu/library/reference-architecture-for-assuring-ethical-conduct-in-laws/',
 'cate-status':'https://www.sei.cmu.edu/projects/cate-increasing-warfighter-trust-autonomous-systems-accelerate-adoption-cutting-edge-capabilities/',
 'raider-topic':'https://navysbir.us/n19_3/N193-141.htm',
 'asimov-status':'https://www.darpa.mil/research/programs/autonomy-standards-and-ideals-with-military-operational-values',
 'ansr':'https://www.darpa.mil/research/programs/assured-neuro-symbolic-learning-and-reasoning',
 'tiamat':'https://www.darpa.mil/research/programs/theory-of-mind-for-ai-teams',
 'gard':'https://www.darpa.mil/research/programs/guaranteeing-ai-robustness-against-deception',
 'assured-autonomy':'https://www.darpa.mil/research/programs/assured-autonomy',
 'caml':'https://www.darpa.mil/research/programs/competence-aware-machine-learning',
 'exa-pricing':'https://exa.ai/docs/admin/pricing',
 'exa-search-docs':'https://exa.ai/docs/reference/search',
}
def fetch(item):
 key,url=item; r={'source_id':key,'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'F4-public-source-audit/1.0'}),timeout=45) as resp:
   raw=resp.read();r.update(status=resp.status,final_url=resp.url,content_type=resp.headers.get('Content-Type',''),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
  (CACHE/key).write_bytes(raw)
 except Exception as e:r.update(status='retrieval_failed',error=type(e).__name__+': '+str(e))
 return r
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:out=list(pool.map(fetch,SOURCES.items()))
 (P/'audit/source-retrieval-register.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
