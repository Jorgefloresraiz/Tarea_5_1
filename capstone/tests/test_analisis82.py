import sys
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from analisis82 import resumen_categorias,comparar_cambio
from modelo import cargar,ajustar,COLS

def test_categorias_preservan_casos_y_limites():
    df=pd.DataFrame({'caso':['a','b'],'dias_abiertos':[90,91],'recurrencias_12m':[1,2]})
    oof=pd.DataFrame({'caso':['a','b'],'categoria':['pocas_areas','multiarea'],'distancia2':[2.,6.]})
    r=resumen_categorias(oof,df)
    assert all(sum(t['n'] for t in r if t['eje']==e)==2 for e in ['categoria','antiguedad','recurrencia'])
    assert next(t for t in r if t['categoria']=='Más de 90 días')['distancia2_media']==6.

def test_estres_no_modifica_datos_ni_modelo():
    x=cargar()[COLS].to_numpy(float);s,m=ajustar(x[:200],2)
    test=x[200:].copy();original=test.copy();centros=m.cluster_centers_.copy();media=s.mean_.copy()
    r=comparar_cambio(s,m,test)
    np.testing.assert_array_equal(test,original)
    np.testing.assert_array_equal(centros,m.cluster_centers_)
    np.testing.assert_array_equal(media,s.mean_)
    assert r['n']==100 and 0<=r['asignaciones_cambiadas']<=100
