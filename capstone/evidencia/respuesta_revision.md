# Respuesta y cierre de revisión técnica

Revisor: Skill auditoria-modelos v2 aplicada por Codex. Revisión asistida, no docente ni compañero.

1. Perfiles de referencia: corregidos en capstone/modelo.py:66–67; ahora solo utilizan los 240 casos de desarrollo. Las métricas principales permanecen iguales.
2. Alerta multiarea: capstone/app.py:6–7 y 18 imprime la advertencia. test_alerta_subgrupo_visible y test_no_inventa_alerta comprueban su comportamiento. La disparidad se reconoce, no se oculta ni se atribuye a causalidad.
3. Sensibilidad: capstone/modelo.py:61–63 mide ARI sin retraso CAPA (0,2544). README declara que estabilidad entre semillas no implica robustez a variables. No se reeligió modelo mirando el conjunto final.
4. README completo y prueba automatizada desde copia limpia. La prueba humana por alguien ajeno al proyecto sigue pendiente y se registra explícitamente; no se presenta la automatización como una persona.

Pruebas completas: 19 aprobadas y 8 subpruebas aprobadas; advertencia del sistema sobre conteo de núcleos, sin fallo. El hook ejecutó pytest antes del commit de correcciones. Se verificó la CLI y se conservó su salida.

Decisión: APROBADO PARA INTEGRACIÓN TÉCNICA como demostración académica con limitaciones documentadas. No autoriza uso operativo ni acredita el requisito pendiente de prueba humana del README.
