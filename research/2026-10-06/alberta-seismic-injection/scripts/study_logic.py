"""Pure rules for a bounded proximity screen, not legal adjudication."""
import datetime as dt
from zoneinfo import ZoneInfo
START='2020-01-01';END='2025-12-31'
def local_date(value):
 t=dt.datetime.fromisoformat(value.replace('Z','+00:00'))
 if t.tzinfo is None:t=t.replace(tzinfo=dt.timezone.utc)
 return t.astimezone(ZoneInfo('America/Edmonton')).date().isoformat()
def in_period(value):return START<=local_date(value)<=END
def rule_version(area,date):
 return 'SO2A' if area=='FoxCreek' and date>='2024-11-19' else {'FoxCreek':'SO2','Brazeau':'SO6','RedDeer':'SO7'}[area]
def shutdown_magnitude_screen(kind,value,threshold,allow_mly=False):
 return kind in (['ML','MLy'] if allow_mly else ['ML']) and value is not None and value>=threshold
