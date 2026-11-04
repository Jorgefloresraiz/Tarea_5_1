from pathlib import Path
import asyncio,json,sys,csv
import numpy as np
from sklearn.metrics import adjusted_rand_score
from mcp import Client
from mcp.client.stdio import StdioServerParameters
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import kmeans_utils
OUT=ROOT/'tarea_5_2/resultados'
async def main():
 OUT.mkdir(parents=True,exist_ok=True)
 params=StdioServerParameters(command=sys.executable,args=[str(ROOT/'mcp_server.py')],cwd=ROOT)
 calls=[]
 async with Client(params,raise_exceptions=True,read_timeout_seconds=30) as client:
  async def call(name,args):
   r=await client.call_tool(name,args)
   raw=r.model_dump(mode='json',by_alias=True)
   calls.append({'herramienta':name,'argumentos':args,'respuesta':raw})
   value=raw.get('structuredContent') or raw.get('structured_content')
   if not value:
    value=json.loads(next(c['text'] for c in raw['content'] if c['type']=='text'))
   return value
  ficha=await call('cargar_dataset',{'nombre':'qa_simulado'})
  resultados=[await call('segmentar_kmeans',{'nombre':'qa_simulado','k':k}) for k in range(2,9)]
  mejor=max(resultados,key=lambda r:(r['silueta'],-r['k']))
  pca=await call('proyectar_pca',{'nombre':'qa_simulado'})
  assert mejor['filas']==pca['filas']
 estabilidad=[]
 for seed in range(10):
  r=kmeans_utils.segmentar_kmeans('qa_simulado',mejor['k'],seed)
  estabilidad.append({'semilla':seed,'ARI':adjusted_rand_score(mejor['etiquetas'],r['etiquetas'])})
 resumen={'ficha':ficha,'comparacion':[{'k':r['k'],'inercia':r['inercia'],'silueta':r['silueta']} for r in resultados], 'mejor':mejor,'pca':pca,'estabilidad':estabilidad,'criterio':'Mayor silueta entre k=2..8; empate: menor k. K-Means sobre seis variables estandarizadas; PCA solo visualiza.'}
 for name,obj in [('mcp_llamadas',calls),('analisis',resumen)]:
  (OUT/f'{name}.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2))
 for name,rows in [('comparacion_k',resumen['comparacion']),('estabilidad',estabilidad),('perfiles',[{'grupo':k,**v} for k,v in mejor['perfiles'].items()])]:
  with (OUT/f'{name}.csv').open('w') as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print(json.dumps({k:resumen[k] for k in ['comparacion','estabilidad']},indent=2))
 print('k:',mejor['k'],'tamanos:',mejor['tamanos'],'varianza:',pca['varianza_acumulada'],'perfiles:',mejor['perfiles'])
if __name__=='__main__': asyncio.run(asyncio.wait_for(main(),timeout=90))
