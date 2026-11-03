# Verificación gráfica del 3 de noviembre de 2026

Inspector 2.13.0, Safari, servidor iniciado nuevamente con `mcp dev mcp_server.py`.

| Captura | Solicitud | Resultado observado |
| --- | --- | --- |
| 51_01_cargar.png | cargar_dataset, iris | 150 filas, cuatro variables numéricas, species |
| 51_02_pca.png | ejecutar_pca, iris, 2 | 0.7296 y 0.2285; acumulada 0.9581; cargas |
| 51_03_catalogo.png | data://datasets | iris y wine |
| 51_04_wine.png | data://datasets/wine | 178 filas, 13 variables numéricas, cultivar |
| 51_05_prompt.png | interpretar_componentes, iris, 2 | Mensaje de interpretación con argumentos sustituidos |

La lista inicial de capacidades demoró aproximadamente 48 segundos; repetir tools/list devolvió OK y el catálogo quedó disponible. Las cinco consultas posteriores se completaron desde los controles de la interfaz. La recuperación del prompt no ejecuta un LLM. Las capturas conservan la interfaz y los resultados; se recortó la barra de Safari para excluir marcadores personales. No contienen el token temporal del Inspector.
