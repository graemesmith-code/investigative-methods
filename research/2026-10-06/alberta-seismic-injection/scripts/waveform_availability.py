"""Bounded, free public metadata acquisition. No credentials, no waveform interpretation."""
from acquire import fetch
from urllib.parse import urlencode
items=[('fdsn-I0.html','https://www.fdsn.org/networks/detail/I0/'),('mda-2K.html','https://ds.iris.edu/mda/2K/'),('station-doc.html','https://service.earthscope.org/fdsnws/station/1/'),('dataselect-doc.html','https://service.earthscope.org/fdsnws/dataselect/1/')]
for name,url in items:fetch('waveforms/'+name,url)
for net in ['2K','I0','RV']:
 params=dict(network=net,starttime='2025-02-22T14:04:18',endtime='2025-02-25T06:34:36',latitude=52.215,longitude=-113.957,maxradius=1,level='channel',format='text',includerestricted='false',nodata=404)
 fetch('waveforms/'+net+'-channels.txt','https://service.earthscope.org/fdsnws/station/1/query?'+urlencode(params))
# Public station metadata may describe partly restricted networks; no restricted waveform access requested.
for net in ['2K','I0']:
 fetch('waveforms/'+net+'-all-stations.xml','https://service.earthscope.org/fdsnws/station/1/query?'+urlencode(dict(network=net,starttime='2025-02-22',endtime='2025-02-26',level='station',format='xml',includerestricted='true',nodata=404)))
# Closest returned RV seismic station, selected by distance, not company affiliation.
windows=[('ca2025dscb','2025-02-22T14:04:18','2025-02-22T14:07:18'),('ca2025dwzq','2025-02-25T06:31:36','2025-02-25T06:34:36')]
for eid,start,end in windows:
 params=dict(network='RV',station='REDDA',location='--',channel='HH?',starttime=start,endtime=end,nodata=404)
 fetch('waveforms/'+eid+'-RV-REDDA.mseed','https://service.earthscope.org/fdsnws/dataselect/1/query?'+urlencode(params),limit=10_000_000)
 fetch('waveforms/'+eid+'-RV-REDDA-response.xml','https://service.earthscope.org/fdsnws/station/1/query?'+urlencode({**params,'level':'response','format':'xml','includerestricted':'false'}))
