"""
Servidor MCP: cuatro tools, dos resources, un prompt.

Este es el archivo que el profesor completa en vivo durante la Clase 5.1,
siguiendo el mismo patrón del curso de Anthropic "Introduction to Model
Context Protocol" (M02), adaptado de un chatbot de documentos a un
servidor de análisis de datos.

Tools    -> operaciones que Claude puede decidir ejecutar (cargar un dataset,
            correr PCA).
Resources -> datos que el cliente puede pedir directamente, sin pasar por
            una decisión de Claude (la lista de datasets, la ficha de uno).
Prompt   -> una plantilla ya evaluada para una tarea recurrente: interpretar
            componentes principales en términos del dominio, no solo en
            términos de varianza.

ESTADO: cinco piezas de 5.1 y dos tools adicionales de 5.2.
Se conserva la lógica PCA del profesor y se exponen sus funciones por MCP.

Para probar este archivo una vez completado, sin cliente ni CLI:
    mcp dev mcp_server.py
Abre el Inspector en el navegador, conecta, y prueba cada tool/resource/prompt
a mano antes de conectarlo a nada más.
"""

from mcp.server.mcpserver import MCPServer, UserMessage
from pydantic import Field

import pca_utils
import kmeans_utils

mcp = MCPServer("analisis-datos")


# ---------------------------------------------------------------------------
# Tools — algo que Claude DECIDE ejecutar, con los argumentos que el modelo
# elige según lo que pida quien está conversando.
# ---------------------------------------------------------------------------

@mcp.tool(name="cargar_dataset", description="Describe filas y columnas del dataset. Usar antes de ejecutar_pca para conocer las variables numéricas.")
def cargar_dataset(nombre: str = Field(description="Nombre disponible en data://datasets")) -> dict:
    return pca_utils.describir_dataset(nombre)


@mcp.tool(name="ejecutar_pca", description="Ejecuta PCA estandarizado y devuelve varianza explicada, varianza acumulada y cargas de las variables originales.")
def ejecutar_pca(nombre: str = Field(description="Nombre disponible en data://datasets"), n_componentes: int = Field(ge=1, description="Cantidad de componentes principales")) -> dict:
    return pca_utils.ejecutar_pca(nombre, n_componentes)


# ---------------------------------------------------------------------------
# Resources — datos que el CLIENTE pide directamente, sin que Claude decida
# nada. Estático (siempre lo mismo) o con plantilla (un parámetro en la URI).
# ---------------------------------------------------------------------------

@mcp.resource("data://datasets", mime_type="application/json")
def listar_datasets() -> list[str]:
    return pca_utils.listar_datasets()


@mcp.resource("data://datasets/{nombre}", mime_type="application/json")
def ficha_dataset(nombre: str) -> dict:
    return pca_utils.describir_dataset(nombre)


# ---------------------------------------------------------------------------
# Prompt — una plantilla YA EVALUADA para una tarea que se repite, en vez de
# dejar que cada usuario improvise su propia pregunta de interpretación.
# ---------------------------------------------------------------------------

@mcp.prompt(name="interpretar_componentes", description="Guía para interpretar las cargas y la varianza de PCA en su dominio.")
def interpretar_componentes(nombre: str = Field(description="Dataset autorizado"), n_componentes: int = Field(ge=1, description="Número de componentes")) -> list[UserMessage]:
    pca_utils.describir_dataset(nombre)
    prompt = f"""Ejecuta ejecutar_pca sobre {nombre} con {n_componentes} componentes.
Identifica las 2–3 variables con mayor carga absoluta por componente y explica
qué patrón del dominio podría representar cada componente. Explica el signo
relativo de las cargas: el signo global del componente puede invertirse sin
cambiar la solución. Distingue interpretación de causalidad.
¿Alcanzan {n_componentes} componentes según la varianza acumulada obtenida?
Usa los resultados reales de la herramienta; no inventes valores."""
    return [UserMessage(prompt)]


@mcp.tool(name="segmentar_kmeans", description="Segmenta variables numéricas estandarizadas; devuelve etiquetas, tamaños, inercia, silueta y perfiles. No evalúa cumplimiento regulatorio.")
def segmentar_kmeans(nombre: str = Field(description="Dataset autorizado"), k: int = Field(ge=2, description="Número de grupos")) -> dict:
    return kmeans_utils.segmentar_kmeans(nombre, k)

@mcp.tool(name="proyectar_pca", description="Reutiliza PCA y devuelve coordenadas 2D y varianza para visualizar los grupos.")
def proyectar_pca(nombre: str = Field(description="Dataset autorizado")) -> dict:
    return pca_utils.ejecutar_pca(nombre, 2, incluir_proyeccion=True)

if __name__ == "__main__":
    mcp.run(transport="stdio")
