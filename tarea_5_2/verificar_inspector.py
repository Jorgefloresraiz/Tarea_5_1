from pathlib import Path
import subprocess,json,sys,shutil
root=Path(__file__).resolve().parents[1]
out=root/'tarea_5_2/resultados'
for name,args in [('segmentar_kmeans',['nombre=qa_simulado','k=2']),('proyectar_pca',['nombre=qa_simulado'])]:
 cmd=[shutil.which('npx') or 'npx','--yes','@modelcontextprotocol/inspector@2.13.0','--cli',str(root/'.venv/bin/python'),str(root/'mcp_server.py'),'--method','tools/call','--tool-name',name,'--tool-arg',*args]
 r=subprocess.run(cmd,cwd=root,capture_output=True,text=True,timeout=45)
 (out/f'inspector_{name}.json').write_text(json.dumps({'comando':cmd,'codigo_salida':r.returncode,'stdout':r.stdout,'stderr':r.stderr},ensure_ascii=False,indent=2))
 assert r.returncode==0,r.stderr
 data=json.loads(r.stdout)
 assert not data.get('isError',False),data
 print(name,'OK',flush=True)
