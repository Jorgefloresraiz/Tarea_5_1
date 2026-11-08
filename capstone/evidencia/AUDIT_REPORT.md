# Auditoría del capstone QA

Revisor: Codex aplicando Skill auditoria-modelos v2 para segmentación. Alcance: revisión de código, ejecuciones de validación y pytest; no validación regulatoria ni revisión humana independiente. Se conserva la versión inicial y los comentarios del PR.

## Veredictos y evidencia

- P1 PASA para simulación independiente: modelo.py:42 divide 240/60 con semilla 42; líneas 45–52 separan folds. Tests comprueban disyunción y cobertura. No se demuestra separación temporal para datos operativos reales.
- P2 PASA: modelo.py:26–29 ajusta StandardScaler en x de entrenamiento. Los pliegues externos llaman elegir_k con x[ia], sin el conjunto final. Prueba test_escalado_solo_entrenamiento.
- P3 PASA: modelo.py:30–38 selecciona k en tres folds internos; líneas 45–56 evalúan externamente y reservan prueba final. El prototipo anterior tarea_5_2/analizar.py seleccionaba y reportaba silueta sobre los mismos datos; sus resultados se consideran exploratorios, no evidencia confirmatoria del capstone.
- D1 PASA con límite: modelo.py:14–19 rechaza identificadores repetidos y valores no finitos/negativos. Cada caso SIM es una entidad sintética distinta; no acredita independencia de futuros expedientes reales.
- Métricas: NO APLICA accuracy, recall y R². CV: silueta 0,3518 ± 0,0886 frente a 0,1438 ± 0,0540; distancia2 4,7292 ± 0,8899 frente a 9,4753 ± 2,2632. Cinco folds y misma escala/filas. Prueba final: silueta 0,3263 vs 0,1551. Sin verdad de criticidad, la dispersión no mide errores regulatorios.
- S3 ALERTA: modelo.py:68–70; multiarea n=78, distancia2=5,8441 y brecha relativa +23,58 %. Pocas áreas n=162, distancia2=4,1924. Umbral exploratorio 20 %, n>=20. El grupo se define mediante un predictor; no se infiere sesgo causal.
- Estabilidad: ARI mínimo entre diez semillas 1,0. Sensibilidad al retirar retraso CAPA: ARI 0,2544. NO PASA una interpretación de robustez general; el resultado impone un límite explícito.

## Hallazgos, correcciones y comprobación

1. Perfiles de referencia incluían filas reservadas (b6e9afc, modelo.py:63). Se restringieron a desarrollo (versión corregida:66). El ajuste y las métricas principales no cambian; se evita contaminar interpretación posterior con la muestra final.
2. La app no mostraba la alerta multiarea. Se agregó advertencias (app.py:6–7,18) y dos pruebas; se conserva la alerta, no se altera un umbral para ocultarla. Mitigación operativa, no eliminación de la disparidad.
3. Faltaba sensibilidad prevista en la propuesta. Se incorporó prueba sin retraso (modelo.py:61–63), registrada como descriptiva y no usada para seleccionar nuevamente el modelo. El README declara el ARI bajo y restringe el uso.
4. Faltaban instalación, mantenimiento y límites específicos: README del capstone incorpora esos apartados. Prueba humana de aceptación todavía pendiente, expresamente diferenciada de reproducción automatizada.

## Omisiones y falsos positivos

La Skill original solo cubría clasificación/regresión; exigir matriz de confusión aquí sería un requisito inaplicable. Se documentó la adaptación sin inventar etiquetas. No se afirma ausencia de falsos positivos de la auditoría porque no existe una revisión independiente. La línea base usa una única semilla y no representa todas las alternativas. Los datos sintéticos comparten factores de generación; la validación aleatoria no prueba generalización a otra empresa, tiempo o proceso. No se usaron datos internos ni se presume aprobación de QA.

Decisión: controles técnicos corregidos y pruebas aprobadas; demostración exploratoria. No autorizada para uso operativo. La prueba de instalación por otra persona sigue pendiente antes de declarar cumplimiento completo de la entrega.
