import json,pathlib,zipfile,io,csv,re
P=pathlib.Path(__file__).resolve().parents[1];OLD=P.parents[1]/'2026-10-06/alberta-seismic-injection'
aliases=[{'licence':'0515889','old':'02/16-28-037-28W4/0','current':'00/15-28-037-28W4/0','original_issued':'102/16-28-037-28W4/00','change_report_date':'2025-10-30'},{'licence':'0516327','old':'00/08-33-037-28W4/0','current':'00/07-33-037-28W4/0','original_issued':'100/08-33-037-28W4/00','change_report_date':'2025-10-30'},{'licence':'0516328','old':'03/01-33-037-28W4/0','current':'00/02-33-037-28W4/0','original_issued':'103/01-33-037-28W4/00','change_report_date':'2025-10-30'}]
ids={}
for a in aliases:
 for typ in ['old','current']:ids['ABWI1'+re.sub(r'[/\-]','',a[typ])+'0']={'licence':a['licence'],'alias':a[typ],'alias_kind':typ}
def rows(path):
 z=zipfile.ZipFile(path);n=z.namelist()[0]
 if n.endswith('.zip'):z=zipfile.ZipFile(io.BytesIO(z.read(n)));n=z.namelist()[0]
 return csv.DictReader(io.TextIOWrapper(z.open(n),encoding='utf-8-sig'))
found=[];count=0
for row in rows(OLD/'sources/petrinex-vol-2025-02.zip'):
 count+=1
 if row['FromToID'] in ids:found.append({'matched_alias':ids[row['FromToID']],'row':row})
fac={x['row']['ReportingFacilityID'] for x in found};history=[r for r in rows(OLD/'sources/petrinex-operator-history.zip') if r['FacilityID'] in fac]
out={'aliases':aliases,'source_for_aliases':'ST1 October30 2025 exact licence amendment entries; original issue lists October30/November18 2024','petrinex_identifier_mapping':ids,'monthly_source':'prior preserved February2025 volumetric snapshot','rows_scanned':count,'matched_rows':found,'linked_facilities':sorted(fac),'facility_history':history,'limitations':'Monthly aggregates never establish pumping after an earthquake. Facility operator is not automatically well licensee or HF contractor. UWI amendment publication date does not establish when the physical bore geometry changed.'}
(P/'results/alias-monthly.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
