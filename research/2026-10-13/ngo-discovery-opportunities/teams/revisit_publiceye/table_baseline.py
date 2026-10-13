#!/usr/bin/env python3
"""Free German OCR with ordinary-code grid segmentation, one bounded public sample.
No model calls. Human-located table region; grid line positions detected from pixels.
Official deu.traineddata must already be cached; no alternate download or retry.
"""
import pathlib,fitz,numpy as np,json,hashlib,subprocess,os,time
from PIL import Image
D=pathlib.Path(__file__).parent;C=pathlib.Path('/tmp/ngo-revisit-publiceye');doc=fitz.open(C/'amidex-current.pdf');page=doc[5];pix=page.get_pixmap(matrix=fitz.Matrix(4,4),colorspace=fitz.csRGB);im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);gray=np.asarray(im.convert('L'));W,H=im.size
# Narrow bounded region nominated manually from visual review. No trained detector.
x0,x1=int(.09*W),int(.705*W);y0,y1=int(.72*H),int(.94*H);dark=gray[y0:y1,x0:x1]<180
hy=np.where(dark.mean(axis=1)>.32)[0];vx=np.where(dark.mean(axis=0)>.70)[0]
def centers(values):
 groups=[]
 for v in values:
  if not groups or v>groups[-1][-1]+2:groups.append([int(v)])
  else:groups[-1].append(int(v))
 return [int(round(sum(g)/len(g))) for g in groups]
ylines=[v+y0 for v in centers(hy)];xlines=[v+x0 for v in centers(vx)];print('grid',xlines,ylines)
assert len(xlines)==4 and len(ylines)==7,'Unexpected grid geometry; abstain, do not fabricate cells'
rows=[];start=time.perf_counter();gold=[['Slowakei','Zemplin','Konfektion'],['Pakistan','Sindh','Garn- und Stoff-herstellung, vollstufig'],['Pakistan','Punjab','Garn- und Stoff-herstellung, vollstufig'],['China','Hebei','Garn- und Stoff-herstellung, vollstufig'],['Türkei','Denizli, Karamanmaras','Garn- und Stoff-herstellung, vollstufig']]
def norm(s):return ''.join(c.lower() for c in s if c.isalpha())
for r in range(1,6):
 for col in range(3):
  box=(xlines[col]+5,ylines[r]+4,xlines[col+1]-5,ylines[r+1]-4);f=C/f'de-grid-{r}-{col}.png';im.crop(box).save(f);out=f.with_suffix('');p=subprocess.run(['tesseract',str(f),str(out),'--tessdata-dir',str(C/'tessdata'),'-l','deu','--psm','6'],env=dict(os.environ,OMP_THREAD_LIMIT='1'),capture_output=True,timeout=20);b=out.with_suffix('.txt').read_bytes();s=b.decode().strip();g=gold[r-1][col];rows.append({'row':r,'column':col+1,'pixel_clip':box,'physical_pdf_page':6,'ocr_char_count':len(s),'ocr_text_sha256':hashlib.sha256(b).hexdigest(),'ocr_value':s,'manual_gold':g,'normalized_exact_agreement':norm(s)==norm(g),'exit_status':p.returncode})
result={'source_url':'https://amidex.at/downloads/nachhaltigkeitsbericht-2026-01.pdf','source_sha256':hashlib.sha256((C/'amidex-current.pdf').read_bytes()).hexdigest(),'engine':'Tesseract with official tessdata_fast deu','configuration':'German OCR plus raster grid line segmentation; human-located bounded table region; normalization strips nonletters and ignores case','horizontal_lines':ylines,'vertical_lines':xlines,'physical_pdf_page':6,'cells':rows,'cell_count':len(rows),'normalized_exact_cells':sum(r['normalized_exact_agreement'] for r in rows),'country_cells_exact':sum(r['normalized_exact_agreement'] for r in rows if r['column']==1),'wall_seconds_ocr_cells':round(time.perf_counter()-start,3),'model_api_calls':0,'limitations':'One fixed document/table; not generic table detection or a multilingual population accuracy estimate.'}
(D/'german-table-baseline.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps({k:result[k] for k in ['cell_count','normalized_exact_cells','country_cells_exact','wall_seconds_ocr_cells']}))
