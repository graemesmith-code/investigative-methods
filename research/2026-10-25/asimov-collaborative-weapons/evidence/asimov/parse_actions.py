import pathlib,xml.etree.ElementTree as E,json,csv,decimal
p=pathlib.Path(__file__).resolve().parent; ns={'a':'http://www.w3.org/2005/Atom','f':'https://www.fpds.gov/FPDS'}
rows=[]; summaries=[]
for file in sorted((p/'raw').glob('*-fpds.xml')):
 rt=E.parse(file).getroot(); actions=[]
 for entry in rt.findall('a:entry',ns):
  award=entry.find('a:content/f:award',ns)
  if award is None:continue
  def get(path):
   e=award.find('f:'+path.replace('/','/f:'),ns);return e.text if e is not None else ''
  def attr(path,att='description'):
   e=award.find('f:'+path.replace('/','/f:'),ns);return e.get(att,'') if e is not None else ''
  row={k:get(v) for k,v in {'piid':'awardID/awardContractID/PIID','modification':'awardID/awardContractID/modNumber','transaction':'awardID/awardContractID/transactionNumber','signed_date':'relevantContractDates/signedDate','effective_date':'relevantContractDates/effectiveDate','current_completion':'relevantContractDates/currentCompletionDate','ultimate_completion':'relevantContractDates/ultimateCompletionDate','obligation':'dollarValues/obligatedAmount','base_exercised_change':'dollarValues/baseAndExercisedOptionsValue','all_options_change':'dollarValues/baseAndAllOptionsValue','reason_code':'contractData/reasonForModification','description':'contractData/descriptionOfContractRequirement','recipient':'vendor/vendorHeader/vendorName','solicitation':'contractData/solicitationID','total_obligation':'totalDollarValues/totalObligatedAmount','total_base_exercised':'totalDollarValues/totalBaseAndExercisedOptionsValue','total_all_options':'totalDollarValues/totalBaseAndAllOptionsValue'}.items()}
  row['reason']=attr('contractData/reasonForModification');row['fpds_record_last_modified']=entry.findtext('a:modified','',ns)
  actions.append(row);rows.append(row)
 actions.sort(key=lambda x:(x['signed_date'],x['modification']))
 if actions:
  pos=[r for r in actions if decimal.Decimal(r['obligation'])>0]; neg=[r for r in actions if decimal.Decimal(r['obligation'])<0]
  summary={'piid':actions[0]['piid'],'count':len(actions),'sum_obligation':str(sum(decimal.Decimal(x['obligation']) for x in actions)),'last_signed_action':actions[-1]['signed_date'],'last_positive_action':pos[-1]['signed_date'] if pos else None,'negative_count':len(neg),'option_reason_count':sum('OPTION' in r['reason'] for r in actions),'termination_reason_count':sum('TERMINAT' in r['reason'] for r in actions),'current_completion':actions[-1]['current_completion'],'ultimate_completion':actions[-1]['ultimate_completion']}
  summaries.append(summary);print(json.dumps(summary));print('\n'.join(f"{r['modification']} {r['signed_date'][:10]} obl={r['obligation']} base={r['base_exercised_change']} all={r['all_options_change']} {r['reason_code']} {r['reason']} end={r['current_completion'][:10]}/{r['ultimate_completion'][:10]} desc={r['description']}" for r in actions))
 else:print(file.name,'NO RECORDS')
(p/'fpds-actions.json').write_text(json.dumps(rows,indent=2));(p/'fpds-summary.json').write_text(json.dumps(summaries,indent=2))
with (p/'fpds-actions.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
