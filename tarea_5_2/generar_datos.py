"""Simulación académica sin registros ni parámetros internos de empresas."""
from pathlib import Path
import numpy as np
import pandas as pd
rng = np.random.default_rng(540)
n = 300
carga = rng.gamma(2, 1, n)
recurrencia = rng.poisson(1.1, n)
df = pd.DataFrame({
    'caso': [f'SIM-{i:04d}' for i in range(n)],
    'dias_abiertos': np.round(np.clip(12 + 24*carga + rng.normal(0, 10, n), 1, 240)),
    'dias_retraso_capa': np.round(np.clip(10*carga + 5*recurrencia + rng.normal(-15, 10, n), 0, 180)),
    'recurrencias_12m': recurrencia,
    'reaperturas': rng.poisson(.3 + .25*recurrencia),
    'acciones_pendientes': rng.poisson(1 + carga),
    'areas_involucradas': np.clip(rng.poisson(1 + .45*carga), 1, 8)
})
df.to_csv(Path(__file__).resolve().parents[1]/'datasets/qa_simulado.csv',index=False)
