# Capstone QA de desviaciones y CAPA

Herramienta académica para que un responsable de QA organice la revisión de carga de trabajo de casos abiertos. Continúa la propuesta de la Tarea 5.2: K-Means, PCA y datos sintéticos representativos del proceso farmacéutico.

## Alcance y datos

300 casos, seis variables numéricas: días abiertos, retraso CAPA, recurrencias en 12 meses, reaperturas, acciones pendientes y áreas involucradas. No hay variable objetivo ni etiquetas de criticidad. `datasets/qa_simulado.csv` fue generado por `tarea_5_2/generar_datos.py` con semilla 540; no procede de una empresa ni contiene datos personales. Se comparte como material académico reproducible del proyecto. El código base del docente conserva su atribución; no se afirma una licencia comercial sobre él.

Los datos utilizados son sintéticos y representan situaciones habituales de los procesos de calidad de la industria farmacéutica. Por confidencialidad no se incluyen registros internos, nombres de empresas ni información propietaria. El escenario se basa en la experiencia profesional del autor, sin reproducir información confidencial de su empleador. Su trabajo como contratista independiente requiere acuerdos de confidencialidad (NDA).

## Instalación desde cero

Python 3.12 y Git. Desde una terminal nueva:

```bash
git clone https://github.com/Jorgefloresraiz/Tarea_5_1.git
cd Tarea_5_1
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r capstone/requirements.txt
python capstone/app.py --salida salida_qa
python -m pytest -v
```

Windows: activar con `.venv\Scripts\Activate.ps1`; usar `py -3.12` para crear el entorno. El capstone CLI usa sus dependencias propias. El servidor MCP y los materiales anteriores conservan `requirements.txt` en la raíz; no mezclar ambos entornos. No se requieren claves ni API de pago para esta herramienta.

La aplicación imprime los perfiles, una alerta para la categoría multiarea y la ruta de `asignaciones.csv` y `perfiles.csv`. Los CSV de entrada deben contener las columnas del ejemplo, identificadores únicos y al menos 50 filas numéricas no negativas; esta versión trabaja por lotes.

```bash
python capstone/app.py --csv datasets/qa_simulado.csv --salida salida_qa
python capstone/modelo.py
```

El segundo comando recalcula la evaluación y escribe JSON/CSV en `capstone/evidencia`. La primera generación de los datos ya está incluida: no es necesario ejecutar el generador.

## Validación y elección

Se reservan 60 casos finales y 240 para desarrollo (semilla 42). Cinco pliegues externos en desarrollo; dentro de cada entrenamiento externo, tres pliegues seleccionan k entre 2 y 8 por silueta media (empate: menor k). StandardScaler se ajusta exclusivamente con entrenamiento en cada nivel. La referencia usa k filas de entrenamiento como centros aleatorios, con el mismo k, escala y filas de evaluación. Es una referencia sencilla de una semilla, no una comparación exhaustiva con otros algoritmos.

| Métrica fuera de muestra en CV | K-Means, media ± DE | Referencia, media ± DE |
|---|---|---|
| Silueta | 0,3518 ± 0,0886 | 0,1438 ± 0,0540 |
| Distancia cuadrática al centro | 4,7292 ± 0,8899 | 9,4753 ± 2,2632 |

Resultado final: k=2; silueta 0,3263 frente a 0,1551 de la referencia; distancia 3,6112 frente a 5,5969. ARI mínimo en diez semillas: 1,0. PCA ajustado en desarrollo conserva 65,64 % en dos componentes. Se mantienen los criterios de la propuesta: silueta >0,25 y ARI >=0,80. Se elige K-Means como candidato exploratorio por esos criterios y su mejora geométrica sobre la referencia, no como prueba de utilidad regulatoria. La evaluación final no se usa para ajustar k.

## Categorías y acciones

La distancia OOF media de los casos multiarea (>=3 áreas, n=78) es 5,8441, un 23,58 % superior al global. Los casos con menos áreas (n=162) tienen 4,1924. La alerta exploratoria se fijó en 20 % con n>=20. El atributo áreas participa en la segmentación: la diferencia es descriptiva y no prueba discriminación ni causalidad.

El grupo con mayor antigüedad/retraso amerita revisar capacidad de seguimiento y coordinación de acciones; el otro permite organizar seguimiento periódico. QA debe contrastar cada caso con su expediente. El identificador de grupo es arbitrario y no equivale a criticidad ni prioridad regulatoria. La app muestra perfiles del lote recibido; los perfiles de referencia se calculan solo con desarrollo.

## Pruebas y auditoría

`python -m pytest -v` ejecuta las pruebas heredadas y del capstone. Cubren rutas autorizadas, segmentación, entradas inválidas, duplicados, reproducibilidad, escalado solo en entrenamiento, particiones y advertencias. La salida completa está en `capstone/evidencia/pytest_completo.txt`.

La Skill original del curso se conserva y adapta en `capstone/skill/SKILL.md`. El informe de auditoría y la revisión del PR documentan hallazgos y correcciones. Accuracy/recall no aplican a segmentación sin etiquetas. La dispersión geométrica no es tasa de error respecto a una verdad de negocio.

## Mantenimiento y límites

Solo demostración con datos sintéticos. No decidir liberación de lotes, criticidad, cumplimiento de Consent Decree ni actuaciones sobre personas. Antes de uso real: autorización, validación independiente de QA, revisión de seguridad y criterios operativos. El ajuste sigue patrones del generador y no demuestra reducción de retrasos.

Revisar distribución de las seis variables, proporción de casos multiarea, distancia al centro y estabilidad de asignaciones. Investigar cambios de proceso o de definiciones antes de reentrenar. Reentrenar en una rama, repetir validación y auditoría, conservar versión anterior y exigir revisión del PR. No adaptar los umbrales a la prueba final. La sensibilidad al retirar retraso CAPA está registrada como análisis descriptivo en validacion.json; no se usa para cambiar el modelo final.

## Prueba de aceptación por otra persona

Pendiente de ejecución humana. Una persona ajena al proyecto debe seguir únicamente estos comandos y registrar nombre o identificación consentida, fecha, equipo, resultado y dificultades. La reproducción automatizada desde una copia limpia se documenta aparte y no sustituye esta prueba.

Autor: Jorge Josué Flores González. MAI 540. Noviembre de 2026.

### Sensibilidad observada

Al retirar días de retraso CAPA, el ARI entre asignaciones finales baja a 0,2544. La estabilidad de 1,0 entre semillas no implica estabilidad frente a cambios de variables. Se conserva el modelo de seis variables definido previamente y se limita su uso a exploración; antes de uso operativo se necesita justificar la selección con QA y validar en nuevos datos.

## Cierre de la Tarea 8.2

La demostración es la CLI descrita arriba; no requiere un servidor público ni claves. Para repetir el análisis por categorías y la prueba de estrés, desde la raíz y con el entorno activo:

```bash
python capstone/analisis82.py
python -m pytest -v
```

`capstone/entrega82/analisis.json` y `categorias.csv` contienen los resultados. Se usan predicciones OOF para áreas, antigüedad y recurrencias. Los cortes de 90 días y dos recurrencias son descriptivos, no regulatorios. El estrés añade 30 días abiertos y 30 días de retraso a los mismos 60 casos finales, con modelo y escala congelados. Cambian 25 asignaciones; la silueta pasa de 0,3263 a 0,1844. No constituye una cohorte futura real ni se utilizó para volver a seleccionar el modelo.

La suite completa de cierre registra 21 pruebas y 8 subpruebas aprobadas. Las dos pruebas nuevas verifican conteos/límites de categorías y que el estrés no modifica entradas, centros ni escalador. La advertencia multiarea de la CLI procede de la validación de referencia, no de una evaluación automática del nuevo lote.

El guion de grabación está en `capstone/entrega82/GUION_VIDEO.md`. Los documentos finales de la Parte 2 contienen informe de ocho páginas (seis de contenido, portada y referencias), presentación y bitácora. La aceptación por otra persona, el video y la presentación oral no se declaran realizados hasta disponer de evidencia. El enlace del video institucional debe incorporarse antes de comprimir la entrega completa.
