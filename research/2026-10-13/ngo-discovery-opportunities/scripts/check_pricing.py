#!/usr/bin/env python3
"""Free official documentation fetch. Never invokes inference APIs."""
import argparse, datetime, hashlib, json, urllib.request, urllib.error
from pathlib import Path
URLS = [
 ('luna_current','https://developers.openai.com/api/docs/models/gpt-5.6-luna.md'),
 ('luna_price_change','https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/'),
 ('haiku_current','https://www.anthropic.com/claude/haiku'),
 ('haiku_release','https://www.anthropic.com/claude-haiku-5-5'),
 ('historical_mini','https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/')]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True); a=p.parse_args()
 rows=[]
 for name,url in URLS:
  row=dict(id=name,url=url,checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),kind='official_model_documentation',paid_call=False)
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'NGOResearchMethods/1.0 (public documentation review)'})
   with urllib.request.urlopen(req,timeout=30) as r:
    b=r.read(4_000_001); row.update(status=r.status,final_url=r.url,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),truncated=len(b)>4_000_000)
  except Exception as e: row.update(status='failed',error=str(e))
  rows.append(row)
 a.output.write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in rows)+'\n')
 print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
