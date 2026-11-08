# Revisión estructurada del commit b6e9afc
Revisor: Skill auditoria-modelos adaptada a segmentación, aplicada por Codex. No se atribuye esta revisión a un compañero o docente.

Alcance: código capstone/modelo.py y app.py, tests y resultados. 10 pruebas ejecutadas y aprobadas. No se detectan claves ni registros internos en el nuevo directorio; casos SIM- sintéticos.

1. capstone/modelo.py:63–64: los perfiles descriptivos usan las 300 filas, incluidas las 60 reservadas. No altera el ajuste numérico, pero expone el conjunto final a interpretación durante desarrollo. Solicito calcular los perfiles de referencia solo sobre desarrollo y distinguir perfiles de lote de la app.
2. capstone/app.py:14–16: no muestra la alerta de dispersión multiarea detectada (n=78, +23,58 % de distancia media respecto al global). Solicito advertencia explícita, sin afirmar discriminación ni corregir el modelo mirando la prueba final.
3. capstone/modelo.py:60–68: falta medir la sensibilidad prometida a variables correlacionadas. Solicito análisis descriptivo retirando dias_retraso_capa, con mismo conjunto de evaluación; no usarlo para reescoger el modelo tras ver la prueba.
4. Documentación: falta README del capstone con línea base, mantenimiento, permiso/procedencia sintética y prueba por otra persona. La prueba humana está pendiente, no debe darse por realizada.

Decisión: CAMBIOS SOLICITADOS. P2/P3 satisfacen separación del escalado y selección interna. S3 conserva alerta; no basta con que la métrica global sea buena. Las métricas supervisadas son NO APLICA.
