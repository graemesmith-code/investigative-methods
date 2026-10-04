"""Evidence overlays never mutate the original Rabbit description."""
ACCESS={
4:dict(route='public company API',credential_required=True,evidence='D05'),
71:dict(route='fishing API',credential_required=True,evidence='phase1 official documentation'),
72:dict(route='GISIS records',credential_required=True,evidence='catalog; verify route'),
73:dict(route='Equasis',credential_required=True,evidence='D04'),
74:dict(route='inspection storage/reuse',authorization_required=True,evidence='D03'),
75:dict(route='inspection search',manual_required=True,evidence='catalog; verify route'),
149:dict(route='schema download',access_failed=True,evidence='phase1 HTTP403'),
214:dict(route='Carbon Mapper scoped API',credential_required=True,evidence='D09'),
255:dict(route='EIA API',credential_required=True,evidence='D16'),
256:dict(route='ENTSO-E API',credential_required=True,authorization_required=True,evidence='D17')}
GOOGLE_BUILDINGS=dict(sys_id='SYS-0164',catalog_claim='Geographic coverage: Global; AP weakness already says not global',verified_scope='V3 listed countries in Africa, South/Southeast Asia, Latin America and Caribbean; Puerto Rico and US Virgin Islands listed, US mainland and Canada absent',evidence_url='https://sites.research.google/gr/open-buildings/',checked_on='2026-10-04',requires_actual_aoi_coverage=True)
def geography_gate(a,b):
 if 164 not in {int(a['sys_id'][-4:]),int(b['sys_id'][-4:])}:return 'unverified_actual_AOI_and_vintage_required'
 other=b if a['sys_id']=='SYS-0164' else a
 i=int(other['sys_id'][-4:])
 if i in {220,221,222} or 263<=i<=344:return 'quarantined_no_verified_geographic_overlap_with_Google_V3'
 if i in {38,217,218}:return 'territory_only_candidate_PR_or_USVI; US_mainland_excluded; verify_actual_AOI'
 return 'Google_V3_country_and_tile_overlap_required; global_catalog_label_rejected'
def record_identifier_equal(namespace,left,right,left_entity_type,right_entity_type):
 """Execution gate for future users; no actual investigative match is asserted here."""
 if namespace=='IMO':
  if left_entity_type!='vessel' or right_entity_type!='vessel':return False
  def valid(v):
   v=str(v).removeprefix('IMO').strip()
   return len(v)==7 and v.isdigit() and sum(int(d)*w for d,w in zip(v[:6],[7,6,5,4,3,2]))%10==int(v[-1])
  return valid(left) and valid(right) and str(left).removeprefix('IMO').strip()==str(right).removeprefix('IMO').strip()
 return bool(left) and left==right and left_entity_type==right_entity_type

def mirror_trade_tuple(reporter,partner,flow,product,period):
 if flow not in {'M','X'}:raise ValueError('Specify imports M or exports X')
 return (partner,reporter,{'M':'X','X':'M'}[flow],product,period)
