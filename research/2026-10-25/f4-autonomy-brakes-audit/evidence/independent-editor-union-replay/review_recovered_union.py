import pathlib,csv,json,hashlib,collections,gzip
from decimal import Decimal as D
R=pathlib.Path(__file__).parent;csv.field_size_limit(2**31-1)
C=R/'consumer-brakes-candidate-register.csv';I=pathlib.Path('/workspace/shared/f4-stage1-recovery/evidence/brakes-candidate-register.csv');L=pathlib.Path('/workspace/shared/f4-editor-live-overlay-recovery/combined-live-inventory.csv')
def read(p):
 rr=list(csv.DictReader(p.open()));m={r['award_key']:r for r in rr};assert len(m)==len(rr);return m
c=read(C);i=read(I);l=read(L);ck=set(c);ik=set(i);lk=set(l);both=ck&ik
out={'scope':'Independent comparison of actual new recovery register, not forced to lost earlier grain/counts. Exact source/instrument keys, not unique awards or funded safeguards.','inputs':[{ 'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest()} for p in [C,I,L]],'counts':{'consumer':len(c),'new_recovery':len(i),'exact_intersection':len(both),'consumer_only':len(ck-ik),'recovery_only':len(ik-ck),'two_register_union':len(ck|ik),'live':len(lk),'live_missing_from_recovery':len(lk-ik),'live_missing_from_both':len(lk-(ck|ik)),'all_three_union':len(ck|ik|lk)},'money':{},'integrity_issues':[]}
matched=0;diffs=[];nulls=[];blank=0
for k in sorted(both):
 for cf,inf in [('obligation_cents_fy2019_2026','obligations_fy2019_2026_usd'),('obligation_cents_fy2024_2026','obligations_fy2024_2026_usd'),('obligation_cents_cy2024_2026','obligations_cy2024_2026_usd')]:
  a=c[k][cf];b=i[k][inf]
  if bool(a.strip())!=bool(b.strip()):nulls.append({'key':k,'field':cf,'consumer_cents':a,'recovery_dollars':b})
  elif a.strip():
   matched+=1
   if D(a)!=D(b)*100:diffs.append({'key':k,'field':cf,'consumer_cents':a,'recovery_dollars':b})
  else:blank+=1
out['money']={'paired_nonempty_cells':matched,'amount_discrepancies':diffs,'both_blank_cells':blank,'null_representation_cells':len(nulls),'null_representation_keys':len({r['key'] for r in nulls}),'null_representation_types':dict(collections.Counter((r['consumer_cents'] or 'BLANK')+' vs '+(r['recovery_dollars'] or 'BLANK') for r in nulls))}
cfk={k for k,r in c.items() if int(r['financial_transaction_count'] or 0)>0};ifk={k for k,r in i.items() if r['financial_match']=='True'}
out['financial_matched_rows']={'consumer':len(cfk),'recovery':len(ifk),'intersection':len(cfk&ifk),'union':len(cfk|ifk),'shared_keys_with_disagreeing_financial_match_flags':sum((k in cfk)!=(k in ifk) for k in both)}
sub=[r for k,r in i.items() if k.startswith('SUBAWARD:')]
out['subaward_grain']={'rows':len(sub),'with_financial_match':sum(r['financial_match']=='True' for r in sub),'with_any_financial_window_amount':sum(any(r[f] for f in ['obligations_fy2019_2026_usd','obligations_fy2024_2026_usd','obligations_cy2019_2026_usd','obligations_cy2024_2026_usd']) for r in sub),'parent_linked_rows':sum(bool(json.loads(r['parent_award_keys_not_financially_attributed'] or '[]')) for r in sub)}
out['inclusion_basis_combination_counts']=dict(collections.Counter(r['inclusion_basis'] for r in i.values()))
out['SP470124P0068_financial_row']=i.get('CONT_AWD_SP470124P0068_9700_-NONE-_-NONE-')
out['live_seed_rows']=[{'award_key':k,'financial_match':i[k]['financial_match'],'inclusion_basis':i[k]['inclusion_basis'],'live_financial_values_not_combined_with_archive':i[k]['live_financial_values_not_combined_with_archive'],'live_seed_disposition_separate':i[k]['live_seed_disposition_separate']} for k in sorted(lk&ik)]
if lk-ik:out['integrity_issues'].append({'live_keys_missing':sorted(lk-ik)})
if out['subaward_grain']['with_financial_match'] or out['subaward_grain']['with_any_financial_window_amount']:out['integrity_issues'].append('Subaward rows improperly carry financial awards amounts')
if diffs:out['integrity_issues'].append('Some directly comparable shared-key window amounts differ')
(R/'new-recovery-union-review.json').write_text(json.dumps(out,indent=2));(R/'new-recovery-null-differences.json').write_text(json.dumps(nulls,indent=2));(R/'new-recovery-exclusive-keys.json').write_text(json.dumps({'consumer_only':sorted(ck-ik),'recovery_only':sorted(ik-ck)},indent=2))
print(json.dumps({k:v for k,v in out.items() if k not in ['SP470124P0068_financial_row','live_seed_rows']},indent=2))
