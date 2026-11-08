"""Segmentación académica QA; ninguna salida es una decisión regulatoria."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold,train_test_split
from sklearn.metrics import silhouette_score,adjusted_rand_score,pairwise_distances_argmin_min
from sklearn.decomposition import PCA
COLS=['dias_abiertos','dias_retraso_capa','recurrencias_12m','reaperturas','acciones_pendientes','areas_involucradas']
ROOT=Path(__file__).resolve().parents[1]

def cargar(ruta=None):
    df=pd.read_csv(ruta or ROOT/'datasets/qa_simulado.csv')
    if not set(COLS+['caso']).issubset(df): raise ValueError('Faltan columnas requeridas')
    if df['caso'].isna().any() or df['caso'].duplicated().any(): raise ValueError('Identificador ausente o repetido')
    x=df[COLS].to_numpy(dtype=float)
    if not np.isfinite(x).all() or (x<0).any(): raise ValueError('Valores no finitos o negativos')
    if len(df)<50: raise ValueError('Se requieren al menos 50 casos')
    return df

def silueta(z,labels):
    return float(silhouette_score(z,labels)) if 1<len(set(labels))<len(z) else None

def ajustar(x,k,seed=42):
    sc=StandardScaler().fit(x);z=sc.transform(x)
    model=KMeans(n_clusters=k,n_init=20,random_state=seed).fit(z)
    return sc,model

def elegir_k(x):
    valores={k:[] for k in range(2,9)}
    for a,b in KFold(3,shuffle=True,random_state=17).split(x):
        for k in valores:
            s,m=ajustar(x[a],k);z=s.transform(x[b]);v=silueta(z,m.predict(z))
            valores[k].append(v)
    medias={k:float(np.mean(v)) if all(t is not None for t in v) else -1 for k,v in valores.items()}
    return max(medias,key=lambda k:(medias[k],-k)),medias

def evaluar(df):
    x=df[COLS].to_numpy(float)
    desarrollo,prueba=train_test_split(np.arange(len(x)),test_size=.2,random_state=42)
    folds=[];registros=[]
    # Cinco folds externos. Elección de k dentro de cada entrenamiento externo.
    for fold,(a,b) in enumerate(KFold(5,shuffle=True,random_state=42).split(desarrollo),1):
        ia,ib=desarrollo[a],desarrollo[b];k,inner=elegir_k(x[ia]);s,m=ajustar(x[ia],k)
        z=s.transform(x[ib]);labels=m.predict(z)
        # Referencia sencilla: centroides como k observaciones aleatorias del entrenamiento.
        rng=np.random.default_rng(42);base=s.transform(x[ia])[rng.choice(len(ia),k,replace=False)]
        lb,db=pairwise_distances_argmin_min(z,base);_,dm=pairwise_distances_argmin_min(z,m.cluster_centers_)
        folds.append({'fold':fold,'k':k,'train':ia.tolist(),'valid':ib.tolist(),'silueta':silueta(z,labels),'silueta_base':silueta(z,lb),'distancia2':float(np.mean(dm**2)),'distancia2_base':float(np.mean(db**2)),'inner':inner})
        registros.extend({'fila':int(i),'caso':df.iloc[i]['caso'],'grupo':int(g),'distancia2':float(v*v),'categoria':'multiarea' if df.iloc[i]['areas_involucradas']>=3 else 'pocas_areas'} for i,g,v in zip(ib,labels,dm))
    k,inner=elegir_k(x[desarrollo]);s,m=ajustar(x[desarrollo],k);zt=s.transform(x[prueba]);lt=m.predict(zt)
    _,dt=pairwise_distances_argmin_min(zt,m.cluster_centers_)
    base=s.transform(x[desarrollo])[np.random.default_rng(42).choice(len(desarrollo),k,replace=False)]
    bt,db=pairwise_distances_argmin_min(zt,base)
    aris=[]
    for seed in range(10):
        _,other=ajustar(x[desarrollo],k,seed);aris.append(float(adjusted_rand_score(lt,other.predict(zt))))
    pca=PCA(n_components=2).fit(s.transform(x[desarrollo]))
    resumen={key:{'media':float(np.mean([f[key] for f in folds if f[key] is not None])),'de':float(np.std([f[key] for f in folds if f[key] is not None],ddof=1)),'n':sum(f[key] is not None for f in folds)} for key in ['silueta','silueta_base','distancia2','distancia2_base']}
    prueba_result={'indices':prueba.tolist(),'k':k,'silueta':silueta(zt,lt),'silueta_base':silueta(zt,bt),'distancia2':float(np.mean(dt**2)),'distancia2_base':float(np.mean(db**2)),'ari_10_semillas':aris,'varianza_pca':float(pca.explained_variance_ratio_.sum())}
    asignados=df.copy();asignados['grupo']=m.predict(s.transform(x))
    perfiles=asignados.groupby('grupo')[COLS].mean().round(3).to_dict('index')
    oof=pd.DataFrame(registros);global_d=float(oof.distancia2.mean());sub=[]
    for grupo,g in oof.groupby('categoria'):
        media=float(g.distancia2.mean());sub.append({'categoria':grupo,'n':len(g),'distancia2':media,'brecha_relativa':abs(media-global_d)/global_d,'alerta':len(g)>=20 and abs(media-global_d)/global_d>.2})
    return {'desarrollo':desarrollo.tolist(),'folds':folds,'cv':resumen,'prueba':prueba_result,'subgrupos':sub,'perfiles':perfiles,'criterios':{'silueta_mayor_025':prueba_result['silueta'] is not None and prueba_result['silueta']>.25,'ari_min_080':min(aris)>=.8},'limite':'Datos sintéticos; distancia al centro es dispersión, no error respecto a una verdad etiquetada.'},oof

if __name__=='__main__':
    r,oof=evaluar(cargar());out=Path(__file__).parent/'evidencia';out.mkdir(exist_ok=True)
    (out/'validacion.json').write_text(json.dumps(r,indent=2,ensure_ascii=False));oof.to_csv(out/'predicciones_oof.csv',index=False)
    print(json.dumps({'cv':r['cv'],'prueba':r['prueba'],'subgrupos':r['subgrupos'],'criterios':r['criterios']},indent=2))
