"""Segmentación exploratoria; no decide criticidad ni cumplimiento regulatorio."""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import pca_utils

def cargar_y_escalar(nombre):
    df = pca_utils.cargar_dataset(nombre)
    x = df.select_dtypes(include="number").dropna()
    if x.empty or len(x) < 3 or not np.isfinite(x.to_numpy()).all():
        raise ValueError("Se requieren al menos tres filas numéricas finitas.")
    return x, StandardScaler().fit_transform(x)

def segmentar_kmeans(nombre, k, semilla=42):
    x, z = cargar_y_escalar(nombre)
    if isinstance(k, bool) or not isinstance(k, int) or not 2 <= k < len(x):
        raise ValueError("k debe ser entero entre 2 y n-1.")
    if k > len(np.unique(z, axis=0)):
        raise ValueError("k supera el número de observaciones distintas.")
    modelo = KMeans(n_clusters=k, n_init=20, random_state=semilla)
    labels = modelo.fit_predict(z)
    return {"dataset": nombre, "k": k, "semilla": semilla,
            "filas": x.index.tolist(), "variables": x.columns.tolist(),
            "etiquetas": labels.tolist(),
            "tamanos": {str(i): int((labels == i).sum()) for i in range(k)},
            "inercia": float(modelo.inertia_),
            "silueta": float(silhouette_score(z, labels)),
            "perfiles": {str(i): x.loc[labels == i].mean().round(3).to_dict() for i in range(k)}}
