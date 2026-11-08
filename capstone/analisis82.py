"""Análisis descriptivo posterior; no ajusta hiperparámetros ni sustituye validación."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances_argmin_min, adjusted_rand_score
from modelo import COLS,cargar,ajustar,silueta
OUT=Path(__file__).parent/'entrega82'

def resumen_categorias(oof,df):
    datos=oof.merge(df[['caso','dias_abiertos','recurrencias_12m']],on='caso',validate='one_to_one')
    datos['antiguedad']=np.where(datos.dias_abiertos>90,'Más de 90 días','Hasta 90 días')
    datos['recurrencia']=np.where(datos.recurrencias_12m>=2,'Dos o más recurrencias','Cero o una recurrencia')
    filas=[]
    for eje in ['categoria','antiguedad','recurrencia']:
        for nombre,g in datos.groupby(eje):
            filas.append({'eje':eje,'categoria':nombre,'n':len(g),'distancia2_media':float(g.distancia2.mean()),'distancia2_mediana':float(g.distancia2.median()),'p90':float(g.distancia2.quantile(.9))})
    return filas

def comparar_cambio(s,m,x):
    original=s.transform(x);alterado=x.copy()
    alterado[:,COLS.index('dias_abiertos')]+=30
    alterado[:,COLS.index('dias_retraso_capa')]+=30
    nuevo=s.transform(alterado)
    a=m.predict(original);b=m.predict(nuevo)
    _,da=pairwise_distances_argmin_min(original,m.cluster_centers_)
    _,db=pairwise_distances_argmin_min(nuevo,m.cluster_centers_)
    return {'n':len(x),'escenario':'Mismos casos reservados, +30 días abiertos y +30 días de retraso CAPA; modelo y escala congelados. Prueba de estrés posterior, no cohorte futura real.', 'distancia2_original':float(np.mean(da**2)),'distancia2_alterada':float(np.mean(db**2)), 'silueta_original':silueta(original,a),'silueta_alterada':silueta(nuevo,b),'asignaciones_cambiadas':int((a!=b).sum()),'ari':float(adjusted_rand_score(a,b))}

def main():
    OUT.mkdir(exist_ok=True)
    df=cargar();r=json.loads((OUT.parent/'evidencia/validacion.json').read_text());x=df[COLS].to_numpy(float)
    s,m=ajustar(x[r['desarrollo']],r['prueba']['k'])
    oof=pd.read_csv(OUT.parent/'evidencia/predicciones_oof.csv')
    cats=resumen_categorias(oof,df)
    cambio=comparar_cambio(s,m,x[r['prueba']['indices']])
    pca=PCA(n_components=2).fit(s.transform(x[r['desarrollo']]))
    puntos=pca.transform(s.transform(x[r['prueba']['indices']]))
    result={'categorias':cats,'estres':cambio,'pca_prueba':puntos.tolist(),'grupos_prueba':m.predict(s.transform(x[r['prueba']['indices']])).tolist(),'varianza_pca':float(pca.explained_variance_ratio_.sum()),'nota':'Umbrales de categorías descriptivos: 90 días y 2 recurrencias, no criterios regulatorios ni usados para elegir k. Categorías se solapan entre ejes.'}
    (OUT/'analisis.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
    pd.DataFrame(cats).to_csv(OUT/'categorias.csv',index=False)
    print(json.dumps({'categorias':cats,'estres':cambio},indent=2,ensure_ascii=False))
if __name__=='__main__':main()
