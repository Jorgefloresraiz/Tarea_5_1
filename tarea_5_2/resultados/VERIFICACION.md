# Verificación del 4 de noviembre de 2026

- Siete pruebas unitarias aprobadas; salida original en pruebas.txt.
- Dos consultas reales mediante MCP Inspector CLI 2.13.0, código de salida 0, sin isError: segmentar_kmeans y proyectar_pca.
- Nueve respuestas del cliente SDK MCP conservadas en mcp_llamadas.json.
- Comparación del PCA actual contra pca_utils.py del commit fa8683d: diccionarios completos idénticos para Iris y Wine con dos componentes. La prueba se realizó cargando la versión histórica desde Git en un módulo independiente con el mismo directorio de datasets.
- Dataset: 300 filas, cero nulos, cero duplicados y cero casos con retraso superior a antigüedad.
- La nueva evidencia no incluye una demostración gráfica de Inspector; los JSON corresponden a su CLI oficial.
- Documentos renderizados y revisados: informe con portada, tres páginas de contenido y referencias; propuesta de una página; interpretación breve y bitácora de una página.

Estos controles prueban el funcionamiento del prototipo, no su validez para decisiones regulatorias reales.
