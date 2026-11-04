import unittest,json
from pathlib import Path
from unittest.mock import patch
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import kmeans_utils,pca_utils
ROOT=Path(__file__).parent
class Segmentacion(unittest.TestCase):
 def test_resultados_y_perfiles(self):
  r=kmeans_utils.segmentar_kmeans('qa_simulado',2)
  x,z=kmeans_utils.cargar_y_escalar('qa_simulado')
  self.assertEqual(sum(r['tamanos'].values()),300)
  self.assertEqual(len(r['etiquetas']),300)
  self.assertNotIn('caso',r['variables'])
  self.assertAlmostEqual(r['silueta'],silhouette_score(z,r['etiquetas']))
  np.testing.assert_allclose(z.mean(0),0,atol=1e-12)
  for i,v in r['perfiles'].items():
   np.testing.assert_allclose(list(v.values()),x.loc[np.array(r['etiquetas'])==int(i)].mean(),atol=.00051)
 def test_k_invalido(self):
  for k in (True,1,300,1.5):
   with self.subTest(k=k),self.assertRaises(ValueError): kmeans_utils.segmentar_kmeans('qa_simulado',k)
 def test_datos_degenerados(self):
  with patch('pca_utils.cargar_dataset',return_value=pd.DataFrame({'x':[1,1,1]})):
   with self.assertRaises(ValueError): kmeans_utils.segmentar_kmeans('qa_simulado',2)
  with patch('pca_utils.cargar_dataset',return_value=pd.DataFrame({'x':[1,np.inf,3]})):
   with self.assertRaises(ValueError): kmeans_utils.segmentar_kmeans('qa_simulado',2)
 def test_equivalencia_pca_51(self):
  for name in ('iris','wine'):
   a=pca_utils.ejecutar_pca(name,2)
   b=pca_utils.ejecutar_pca(name,2,True)
   self.assertEqual(a,{k:v for k,v in b.items() if k not in ('proyeccion','filas')})
 def test_mcp_y_local_coinciden(self):
  a=json.loads((ROOT/'tarea_5_2/resultados/analisis.json').read_text())
  self.assertEqual(a['mejor'],kmeans_utils.segmentar_kmeans('qa_simulado',a['mejor']['k']))
  self.assertEqual(a['mejor']['filas'],a['pca']['filas'])
  self.assertEqual(len(a['pca']['proyeccion']),300)
  self.assertEqual(a['mejor']['k'],max(a['comparacion'],key=lambda v:v['silueta'])['k'])
if __name__=='__main__': unittest.main()
