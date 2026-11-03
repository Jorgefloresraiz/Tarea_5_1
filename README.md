# Tarea 5.1 — Servidor MCP para PCA

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

## Cinco verificaciones
1. Tool cargar_dataset: nombre=iris (150 filas).
2. Tool ejecutar_pca: nombre=iris, n_componentes=2 (varianza acumulada 0.9581).
3. Resource data://datasets (iris, wine).
4. Resource data://datasets/wine (178 filas).
5. Prompt interpretar_componentes: nombre=iris, n_componentes=2.

Los JSON en evidencia/ son resultados reales del MCP Inspector CLI, con comando y código de salida. También se verificaron las cinco piezas mediante la interfaz gráfica de Inspector 2.13.0 en Safari, tras iniciar mcp dev desde un proceso nuevo el 3 de noviembre de 2026. Las cinco capturas están en evidencia/capturas/.

## Permisos
Solo iris y wine; lista permitida y comprobación de rutas resueltas. No hay herramientas de escritura, shell ni acceso de red. Esto restringe la interfaz, no los permisos del proceso en el sistema operativo. No introducir datos sensibles en los CSV. .env no está incluido.

## Estado
Cinco piezas implementadas en commits separados. Cinco consultas del Inspector CLI correctas. PCA de ambos datasets idéntico al original con dos componentes. Pruebas de rutas inválidas correctas. Repositorio: https://github.com/Jorgefloresraiz/Tarea_5_1. Comprobación gráfica final completada; cinco capturas incorporadas.

## Material de origen
Demo_PCA_MCP_incompleto del profesor. Se conserva la lógica PCA y se restringe el acceso a archivos. main.py, chat.py y mcp_client.py son clientes opcionales originales; no fueron utilizados ni validados para esta entrega. El cliente conversacional requiere dependencias adicionales y una API de pago.

La configuración mcp_config.json usa rutas relativas: ejecutar desde la raíz del proyecto. Para un cliente iniciado desde otra carpeta, sustituirlas por rutas absolutas.
