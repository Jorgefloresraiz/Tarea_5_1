# Guion de demostración: 3 minutos

Preparación: entorno instalado según el README, terminal en la raíz del repositorio y PDF de la presentación abierto. Grabar pantalla y voz. Usar solo el CSV sintético incluido. Cronometrar y ajustar el ritmo para terminar a los tres minutos; este guion no es evidencia de una grabación realizada.

## 0:00–0:25 · Problema
«Mi proyecto organiza desviaciones y acciones correctivas y preventivas de calidad farmacéutica mediante grupos con perfiles similares. Busca apoyar la revisión de carga de trabajo de QA. Los trescientos registros son sintéticos y representativos; no contienen información de mi empleador. Mi trabajo como contratista requiere acuerdos de confidencialidad.»

Mostrar la primera diapositiva.

## 0:25–0:55 · Ejecutar
Mostrar y ejecutar:

```bash
python capstone/app.py --csv datasets/qa_simulado.csv --salida salida_qa
```

«La aplicación valida el archivo, aplica la escala y el modelo ajustados con desarrollo y genera dos archivos: las asignaciones de cada caso y los perfiles de los grupos. Esta advertencia sobre casos multiarea corresponde a la validación de referencia, no a un diagnóstico del archivo nuevo.»

## 0:55–1:25 · Interpretar la salida
Abrir salida_qa/perfiles.csv. Mostrar la diferencia en días abiertos, retraso y acciones pendientes.

«Estos números identifican grupos, no niveles de criticidad. Un perfil con mayor antigüedad y retraso orienta a revisar seguimiento y coordinación; QA debe contrastar cada expediente. La herramienta no decide liberación de lotes ni cumplimiento.»

## 1:25–1:55 · Resultados
Mostrar diapositivas 3 y 4.

«Se reservaron sesenta casos. En la validación externa la silueta fue 0,3518, frente a 0,1438 de la referencia. Los casos de más de noventa días mostraron distancia media 8,63 frente a 4,13 en los demás. Esta distancia indica dispersión, no una tasa de errores regulatorios. No disponemos de etiquetas reales para medirla.»

## 1:55–2:25 · Controles
Ejecutar:

```bash
python -m pytest -q
```

«Las veintiuna pruebas verifican entradas, particiones, reproducibilidad y controles del análisis. El repositorio conserva la auditoría y un pull request revisado. El escalado se ajusta solo con entrenamiento, y la selección de grupos se realiza dentro de la validación.»

## 2:25–3:00 · Límites y cierre
Mostrar diapositivas 5 y 7.

«La estabilidad entre semillas no elimina la sensibilidad a las variables. Al retirar retraso CAPA, el ARI baja a 0,2544. Al añadir treinta días en una prueba artificial, cambian veinticinco de sesenta asignaciones. Antes de uso real hacen falta validación de QA, datos autorizados y seguimiento de cambios del proceso. El aporte actual es una demostración reproducible que muestra tanto sus resultados como sus límites.»

## Después de grabar

Revisar duración, voz y que no se vean datos privados. Subir a Drive institucional y habilitar acceso por enlace. Comprobar el enlace sin iniciar sesión. Entregar únicamente ese enlace en `04_Enlace_Video.txt`; no incluir el video dentro del ZIP.
