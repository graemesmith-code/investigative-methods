import pathlib,json,re,sys,subprocess
P=pathlib.Path(__file__).resolve().parent/'raw'
def pages(name,term,limit=8,width=650):
 p=P/name
 if name.endswith('.pdf') or name.endswith('.bin'):
  txt=pathlib.Path(str(p)+'.txt')
  if not txt.exists():subprocess.run(['pdftotext','-layout',str(p),str(txt)],check=True)
 else:txt=p
 s=txt.read_text(errors='replace')
 hits=[]
 for i,page in enumerate(s.split('\f'),1):
  matches=list(re.finditer(re.escape(term),page,re.I))
  if matches:
   hits.append({'pdf_page':i,'snippets':[page[max(0,m.start()-150):m.start()+width] for m in matches[:2]]})
 print(json.dumps({'source':name,'term':term,'page_count':len(s.split('\f')),'matching_page_count':len(hits),'hits':hits[:limit]},ensure_ascii=False,indent=2))
if __name__=='__main__':pages(*sys.argv[1:3],int(sys.argv[3]) if len(sys.argv)>3 else 8)
