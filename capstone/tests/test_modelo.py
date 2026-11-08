import sys,json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from modelo import cargar,ajustar,COLS,silueta

@pytest.fixture
def df(): return cargar()

def test_datos_sinteticos_sin_nulos(df):
    assert len(df)==300 and df.caso.str.startswith('SIM-').all()
    assert np.isfinite(df[COLS].to_numpy()).all()

def test_rechaza_negativos(df,tmp_path):
    df.loc[0,'dias_abiertos']=-1;p=tmp_path/'datos.csv';df.to_csv(p,index=False)
    with pytest.raises(ValueError,match='negativos'): cargar(p)

def test_rechaza_nan(df,tmp_path):
    df.loc[0,'dias_abiertos']=np.nan;p=tmp_path/'datos.csv';df.to_csv(p,index=False)
    with pytest.raises(ValueError,match='no finitos'): cargar(p)

def test_rechaza_casos_repetidos(df,tmp_path):
    df.loc[1,'caso']=df.loc[0,'caso'];p=tmp_path/'datos.csv';df.to_csv(p,index=False)
    with pytest.raises(ValueError,match='repetido'): cargar(p)

def test_rechaza_columnas_ausentes(df,tmp_path):
    p=tmp_path/'datos.csv';df.drop(columns='reaperturas').to_csv(p,index=False)
    with pytest.raises(ValueError,match='Faltan'): cargar(p)

def test_escalado_solo_entrenamiento(df):
    x=df[COLS].to_numpy(float);s,m=ajustar(x[:200],2)
    np.testing.assert_allclose(s.mean_,x[:200].mean(axis=0))
    before=s.mean_.copy();m.predict(s.transform(x[200:]*100));np.testing.assert_array_equal(before,s.mean_)

def test_reproducibilidad(df):
    x=df[COLS].to_numpy(float);s,m=ajustar(x,2);s2,m2=ajustar(x,2)
    np.testing.assert_array_equal(m.labels_,m2.labels_)

def test_metrica_indefinida_no_se_presenta_como_cero():
    assert silueta(np.ones((10,2)),np.zeros(10)) is None

def test_particiones_evidencia():
    r=json.loads((Path(__file__).parents[1]/'evidencia/validacion.json').read_text())
    dev=set(r['desarrollo']);test=set(r['prueba']['indices']);assert not dev&test
    valid=[]
    for f in r['folds']:
        assert not set(f['train'])&set(f['valid']);assert set(f['train'])|set(f['valid'])==dev
        valid+=f['valid']
    assert sorted(valid)==sorted(dev)

def test_linea_base_y_modelo_mismos_casos():
    r=json.loads((Path(__file__).parents[1]/'evidencia/validacion.json').read_text())
    assert r['cv']['distancia2']['n']==r['cv']['distancia2_base']['n']==5
    assert all(np.isfinite(f['distancia2_base']) and np.isfinite(f['distancia2']) for f in r['folds'])

def test_alerta_subgrupo_visible():
    from app import advertencias
    r={'subgrupos':[{'categoria':'multiarea','n':78,'brecha_relativa':.235,'alerta':True}]}
    assert len(advertencias(r))==1 and 'No indica criticidad' in advertencias(r)[0]

def test_no_inventa_alerta():
    from app import advertencias
    assert advertencias({'subgrupos':[{'alerta':False}]})==[]
