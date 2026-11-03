from pathlib import Path
import subprocess,json,sys
p=Path(__file__).resolve().parent;e=p/'evidencia';e.mkdir(exist_ok=True)
cases=[('01_cargar_dataset',['--method','tools/call','--tool-name','cargar_dataset','--tool-arg','nombre=iris']),('02_ejecutar_pca',['--method','tools/call','--tool-name','ejecutar_pca','--tool-arg','nombre=iris','n_componentes=2']),('03_listar_datasets',['--method','resources/read','--uri','data://datasets']),('04_ficha_dataset',['--method','resources/read','--uri','data://datasets/wine']),('05_interpretar_componentes',['--method','prompts/get','--prompt-name','interpretar_componentes','--prompt-args','nombre=iris','n_componentes=2'])]
base=['npx','--yes','@modelcontextprotocol/inspector','--cli',str(p/'.venv/bin/python'),str(p/'mcp_server.py')]
for name,args in cases:
 r=subprocess.run(base+args,cwd=p,capture_output=True,text=True,timeout=40)
 (e/(name+'.json')).write_text(json.dumps({'comando':base+args,'codigo_salida':r.returncode,'stdout':r.stdout,'stderr':r.stderr},ensure_ascii=False,indent=2))
 print(name,r.returncode,r.stdout[:180],flush=True)
 if r.returncode: sys.exit(r.returncode)
