from acquire import fetch
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode
base='https://services2.arcgis.com/jQV6VMr2Loovu7GU/arcgis/rest/services/Alberta_Earthquakes_view/FeatureServer/0'
items=[('SummaryChemical-WaterUse.csv','https://www.aer.ca/documents/by-topic/hydraulic-fracturing/SummaryChemical-WaterUse.csv'),('WaterSourceData.csv','https://www.aer.ca/documents/by-topic/hydraulic-fracturing/WaterSourceData.csv'),('earthquakes.json',base+'/query?'+urlencode({'f':'json','where':"Datetime_UTC >= '2019-12-31' AND Datetime_UTC < '2026-01-02'",'outFields':'*','returnGeometry':'true','outSR':4326,'resultRecordCount':16000,'orderByFields':'object_id'})),('tableau.html','https://www2.aer.ca/t/Production/views/PRD_1000_Hydraulic_Fracture_Fluid_Search_EXT/HydraulicFractureFluidSearch'),('bulletin-2024-29.html','https://www.aer.ca/about-aer/media-centre/bulletins/bulletin-2024-29'),('Directive065.pdf','https://www.aer.ca/documents/directives/Directive065.pdf')]
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(lambda x:fetch(*x),items))
