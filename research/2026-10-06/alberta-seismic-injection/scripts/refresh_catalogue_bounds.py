"""Acquire padded UTC catalogues; analysis selects exact Edmonton local dates.
Original snapshots remain in sources/pre-audit/ with their original manifest hashes.
"""
import pathlib, shutil, json
from urllib.parse import urlencode
from acquire import fetch, ROOT
S=ROOT/'sources'; old=S/'pre-audit';old.mkdir(exist_ok=True)
for n in ['earthquakes.json','earthquake-count.json','nrcan-events.txt','nrcan-events.xml']:
 if (S/n).exists() and not (old/n).exists():shutil.move(S/n,old/n)
base='https://services2.arcgis.com/jQV6VMr2Loovu7GU/arcgis/rest/services/Alberta_Earthquakes_view/FeatureServer/0/query?'
where="Datetime_UTC >= '2019-12-31' AND Datetime_UTC < '2026-01-02'"
fetch('earthquakes.json',base+urlencode(dict(f='json',where=where,outFields='*',returnGeometry='true',outSR=4326,resultRecordCount=16000,orderByFields='object_id')))
fetch('earthquake-count.json',base+urlencode(dict(f='json',where=where,returnCountOnly='true')))
base='https://www.earthquakescanada.nrcan.gc.ca/fdsnws/event/1/query?'
params=dict(starttime='2019-12-31T00:00:00',endtime='2026-01-02T00:00:00',minlatitude=51.5,maxlatitude=54.9,minlongitude=-118.3,maxlongitude=-112.9,nodata=404)
fetch('nrcan-events.txt',base+urlencode({**params,'format':'text'}))
fetch('nrcan-events.xml',base+urlencode(params))
