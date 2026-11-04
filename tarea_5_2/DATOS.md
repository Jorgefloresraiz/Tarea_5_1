# Diccionario de datos simulados

300 casos abiertos en una fecha de corte; semilla 540. No se utilizaron registros empresariales. No hay etiquetas reales ni clusters definidos en el generador.

| Campo | Definición |
|---|---|
| caso | Identificador sintético; excluido del modelo |
| dias_abiertos | Días desde apertura hasta la fecha de corte |
| dias_retraso_capa | Días transcurridos desde la fecha objetivo de CAPA; cero si no hay retraso |
| recurrencias_12m | Repeticiones similares en los 12 meses anteriores |
| reaperturas | Veces que se reabrió el caso |
| acciones_pendientes | Número de acciones aún pendientes |
| areas_involucradas | Áreas participantes en el seguimiento |

El generador usa una variable continua de carga administrativa para inducir correlaciones entre antigüedad, retraso, acciones y áreas. No representa parámetros estimados de una empresa. La muestra no contiene nulos ni duplicados; se conserva el índice para alinear etiquetas y PCA. El preprocesamiento selecciona columnas numéricas, elimina filas incompletas y rechaza infinitos; para datos reales habría que justificar el tratamiento de faltantes.
