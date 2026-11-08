# Capstone QA del Módulo 8

Consultar [documentación del capstone](capstone/README.md), [auditoría](capstone/evidencia/AUDIT_REPORT.md) y [pull request revisado](https://github.com/Jorgefloresraiz/Tarea_5_1/pull/1). Los materiales 5.1/5.2 originales se conservan debajo.

# Tareas 5.1 y 5.2 — Servidor MCP para PCA y segmentación

Jorge Josué Flores González · MAI 540 · Atlantis University

## Instalación
Python 3.11 o posterior y Node.js compatible con MCP Inspector.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mcp dev mcp_server.py
```

Conecta el Inspector por stdio usando el Python de .venv y mcp_server.py. El SDK y el Inspector son herramientas distintas. No se necesita API de Anthropic.

## Cinco verificaciones históricas de la Tarea 5.1
1. Tool cargar_dataset: nombre=iris (150 filas).
2. Tool ejecutar_pca: nombre=iris, n_componentes=2 (varianza acumulada 0.9581).
3. Resource data://datasets (iris, wine en 5.1; ahora incluye qa_simulado).
4. Resource data://datasets/wine (178 filas).
5. Prompt interpretar_componentes: nombre=iris, n_componentes=2.

Los JSON en evidencia/ son resultados reales del MCP Inspector CLI, con comando y código de salida. También se verificaron las cinco piezas mediante la interfaz gráfica de Inspector 2.13.0 en Safari, tras iniciar mcp dev desde un proceso nuevo el 3 de noviembre de 2026. Las cinco capturas están en evidencia/capturas/.

## Permisos
iris, wine y qa_simulado; lista permitida y comprobación de rutas resueltas. No hay herramientas de escritura, shell ni acceso de red. Esto restringe la interfaz, no los permisos del proceso en el sistema operativo. No introducir datos sensibles en los CSV. .env no está incluido.

## Estado
Cinco piezas implementadas en commits separados. Cinco consultas del Inspector CLI correctas. PCA de ambos datasets idéntico al original con dos componentes. Pruebas de rutas inválidas correctas. Repositorio: https://github.com/Jorgefloresraiz/Tarea_5_1. Comprobación gráfica final completada; cinco capturas incorporadas.

## Material de origen
Demo_PCA_MCP_incompleto del profesor. Se conserva la lógica PCA y se restringe el acceso a archivos. main.py, chat.py y mcp_client.py son clientes opcionales originales; no fueron utilizados ni validados para esta entrega. El cliente conversacional requiere dependencias adicionales y una API de pago.

La configuración mcp_config.json usa rutas relativas: ejecutar desde la raíz del proyecto. Para un cliente iniciado desde otra carpeta, sustituirlas por rutas absolutas.


## Tarea 5.2 — QA farmacéutica

Se extiende este mismo servidor, sin crear otro repositorio. La simulación representa 300 casos de desviaciones y CAPA en un escenario hipotético de remediación. No identifica empresas ni acredita cumplimiento de un Consent Decree.

Los datos utilizados son simulados y representan situaciones habituales de los procesos de calidad de la industria farmacéutica. El escenario se basa en mi experiencia profesional como contratista independiente, actividad que requiere la firma de acuerdos de confidencialidad (NDA). Por ello, no se incluyen registros internos, nombres de empresas ni información propietaria, y no se reproduce información confidencial de mi empleador o de las organizaciones contratantes.

### Reproducir
Desde la raíz, con el entorno activado:
```bash
python tarea_5_2/generar_datos.py
python tarea_5_2/analizar.py
python tarea_5_2/graficar.py
python -m unittest test_permisos test_segmentacion -v
python tarea_5_2/verificar_inspector.py
```
Las tres primeras instrucciones producen datos, respuestas MCP y SVG; no requieren Matplotlib ni una API de pago. El cliente de analizar.py inicia el servidor por stdio y utiliza realmente sus respuestas para seleccionar k y proyectar PCA. El análisis tiene límite de 90 segundos y cada llamada 30 segundos. Inspector requiere Node.js/npx y puede necesitar red la primera vez para obtener el paquete; cada consulta se limita a 45 segundos.

### Nuevas herramientas
- `segmentar_kmeans(nombre="qa_simulado", k=2)`: etiquetas, tamaños, inercia, silueta y perfiles.
- `proyectar_pca(nombre="qa_simulado")`: reutiliza PCA y añade coordenadas y filas, preservando la respuesta previa de ejecutar_pca.

Se entrenó K-Means sobre seis variables estandarizadas. Se eligió k=2 por máxima silueta en 2..8 (0.3561); grupos de 47 y 253 casos. PCA conserva 64.39 %. Diez semillas adicionales dieron ARI mínimo 0.9828. Los perfiles corresponden a mayor/menor carga administrativa, no a riesgo de producto. Las respuestas incluyen información por fila: no introducir datos internos en los datasets autorizados.

### Entrega
- [Informe APA](tarea_5_2/documentos/Informe_Tarea_5_2.docx): tres páginas de contenido, portada y referencias aparte.
- [Interpretación breve](tarea_5_2/documentos/Interpretacion_Tarea_5_2.docx): grupos y acciones.
- [Propuesta de capstone PDF](tarea_5_2/documentos/Propuesta_Capstone.pdf): una página.
- [Bitácora](tarea_5_2/documentos/Bitacora_Tarea_5_2.docx): asistencia y decisiones verificables.
- [Gráfico de k](tarea_5_2/graficas/seleccion_k.svg) y [PCA](tarea_5_2/graficas/pca_grupos.svg).
- `tarea_5_2/resultados/`: respuestas reales MCP/Inspector, tabla de k, perfiles y siete pruebas aprobadas.

La evidencia nueva usa Inspector CLI; no se afirma una verificación gráfica nueva. Las capturas de evidencia/capturas/ corresponden exclusivamente a 5.1. La consigna adjunta pide interpretación breve y propuesta; el informe y la bitácora complementan los requisitos publicados en la plataforma.

Los datos no permiten validar desempeño operativo real. La correlación introducida por la simulación favorece un eje de carga; no prueba que existan clases naturales. No hay evaluación predictiva ni conjunto de prueba: se trata de segmentación exploratoria de la muestra completa. La estabilidad entre semillas no sustituye estabilidad entre muestras o periodos.
