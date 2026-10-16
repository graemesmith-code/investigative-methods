#!/usr/bin/env python3
"""Distinguish populated identifiers from valid-looking syntax, and check date/money semantics."""
import collections,json,re
from decimal import Decimal
import pandas as pd
from acquire import ROOT,DATA,save_json
sbir=pd.read_parquet(DATA/'normalized/sbir_current.parquet');audit={'retained_rows':len(sbir),'reported_award_fy_vs_performance_start_fy_mismatch':[],'performance_start_outside_action_window':[],'money_checks':collections.Counter(),'id_checks':collections.Counter()}
for r in sbir.to_dict('records'):
 ids=json.loads(r['identifiers_json']);dt=r['action_date'];derived=str(int(dt[:4])+(int(dt[5:7])>=10)) if dt else None
 info={'document_id':r['document_id'],'source_record_id':r['source_record_id'],'reported_award_fy':r['fiscal_year'],'performance_start':dt,'raw_locator':r['raw_locator']}
 if derived!=r['fiscal_year']:audit['reported_award_fy_vs_performance_start_fy_mismatch'].append(info)
 if dt and not ('2018-10-01'<=dt<='2026-09-30'):audit['performance_start_outside_action_window'].append(info)
 value=json.loads(r['money_json'])['award_amount']['value']
 if value is None:audit['money_checks']['missing_or_unparseable']+=1
 else:
  n=Decimal(value);audit['money_checks']['valid']+=1;audit['money_checks']['negative' if n<0 else ('zero' if n==0 else 'positive')]+=1
 for k in ['UEI','Duns','Contract','Agency Tracking Number']:
  v=(ids.get(k) or '').strip()
  if not v:audit['id_checks'][k+':blank']+=1
  elif v.upper() in ['N/A','NA','NONE','UNKNOWN','TBD','NOT AVAILABLE','-']:audit['id_checks'][k+':placeholder']+=1
  elif k=='UEI' and not re.fullmatch(r'[A-Za-z0-9]{12}',v):audit['id_checks']['UEI:syntax_flag']+=1
  elif k=='Duns' and not re.fullmatch(r'\d{9}',v):audit['id_checks']['Duns:syntax_flag']+=1
save_json(ROOT/'validation/sbir_retained_semantic_checks.json',audit)
usa=[]
for p in sorted((ROOT/'validation').glob('usaspending_*_source_table_profiles.json')):
 source=p.name.removesuffix('_source_table_profiles.json');path=DATA/'normalized'/f'{source}_transactions_source.parquet';df=pd.read_parquet(path,columns=['recipient_uei','awarding_agency_code','action_date','action_date_fiscal_year']+(['product_or_service_code'] if source.startswith('usaspending_dod_rd') else []));uei=df.recipient_uei;fiscal=df.action_date.str[:4].astype(int)+(df.action_date.str[5:7].astype(int)>=10).astype(int);usa.append({'source':source,'rows':len(df),'non_rd_psc_prefix_rows':int((~df.product_or_service_code.str.startswith('A')).sum()) if 'product_or_service_code' in df else None,'blank_ueis':int((uei=='').sum()),'nonempty_uei_syntax_flags':int(((uei!='')&~uei.str.fullmatch(r'[A-Za-z0-9]{12}')).sum()),'awarding_agency_counts':df.awarding_agency_code.value_counts().to_dict(),'reported_action_fy_mismatches':int((fiscal.astype(str)!=df.action_date_fiscal_year).sum()),'actions_after_2026_07_18':int((df.action_date>'2026-07-18').sum()),'warning':'UEI syntax check is not registry/entity identity verification. Recent public rows do not establish complete quarter coverage.'})
save_json(ROOT/'validation/usaspending_semantic_checks.json',usa);print('Semantic audits',len(sbir),'SBA rows;',len(usa),'spending extracts')
