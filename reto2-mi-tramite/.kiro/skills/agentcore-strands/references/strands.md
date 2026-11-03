# Strands Agents 1.63: patrones verificados

Firmas comprobadas con `inspect` sobre la librería instalada. Los ejemplos 1, 2, 3, 4 y 9 **corrieron de verdad** con un modelo local (el 3 nov 2026); los ejemplos 6 (Guardrails) y 7 (MCP/Gateway) solo tienen verificada la firma, porque no hay cuenta con Bedrock.

## 1. Agente con herramientas
```python
from strands import Agent, tool
from strands.models.bedrock import BedrockModel

@tool
def inscritos_sin_ingreso(evento_id: str, empresa: str) -> list[str]:
    """Lista los inscritos de una empresa que aún no ingresan al evento.

    Args:
        evento_id: Identificador del evento.
        empresa: Nombre de la empresa, por ejemplo "Arquitectos S.A.".

    Returns:
        Nombres de las personas que faltan.
    """
    ...

agente = Agent(
    model=BedrockModel(model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0", temperature=0),
    system_prompt="Eres el asistente de eventos de CONFA. Responde en español. Nunca inventes cifras: usa herramientas.",
    tools=[inscritos_sin_ingreso],
)
resultado = agente("¿Quién falta de Arquitectos S.A.?")
print(resultado.metrics.tool_metrics.keys())   # qué herramientas usó (útil en pruebas)
```
**El docstring y los type hints son lo que lee el modelo.** Las herramientas deben devolver errores claros (no lanzar excepciones crudas) para que el agente pueda recuperarse.

## 2. Salida estructurada (lenguaje natural → datos limpios)
```python
from pydantic import BaseModel, Field

class Clasificacion(BaseModel):
    tipo: str = Field(description="vacaciones | incapacidad | certificado | permiso")
    fecha_inicio: str | None = None
    requiere_adjunto: bool

r = clasificador("Necesito vacaciones del 10 al 20 de diciembre", structured_output_model=Clasificacion)
datos: Clasificacion = r.structured_output
```

## 3. Agentes como herramienta
```python
especialista = Agent(model=..., system_prompt="Validas soportes de incapacidad. Nunca reveles diagnósticos.",
                     tools=[leer_soporte])
orquestador = Agent(model=..., tools=[
    especialista.as_tool(name="especialista_incapacidades",
                         description="Atiende incapacidades médicas y valida sus soportes"),
])
# Firma: as_tool(*, name=None, description=None, preserve_context=False, delegate=False)
```

## 4. Graph (proceso con pasos y condiciones)
```python
from strands.multiagent import GraphBuilder

def soporte_valido(state) -> bool:          # condición: recibe GraphState
    ...

g = GraphBuilder()
g.add_node(clasificador, "clasificar")      # add_node(executor, node_id)
g.add_node(validador, "validar")
g.add_node(radicador, "radicar")
g.add_edge("clasificar", "validar")
g.add_edge("validar", "radicar", condition=soporte_valido)
g.set_entry_point("clasificar")
g.set_execution_timeout(120)
grafo = g.build()
resultado = grafo("Adjunto mi incapacidad del 3 al 5 de noviembre")
```
También existen `set_max_node_executions`, `set_node_timeout` y `reset_on_revisit` (para ciclos).

## 5. Swarm (evitar en el camino crítico de la demo)
```python
from strands.multiagent import Swarm
equipo = Swarm([investigador, redactor, revisor], entry_point=investigador,
               max_handoffs=10, execution_timeout=300)
```

## 6. Guardrails de Bedrock
```python
modelo = BedrockModel(
    model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0",
    guardrail_id="<id>", guardrail_version="1",
    guardrail_trace="enabled",
    guardrail_redact_output=True,
    guardrail_redact_output_message="No puedo compartir esa información.",
)
```
El guardrail se crea en la consola de Bedrock o con boto3 (`bedrock.create_guardrail`). La cédula colombiana no es un tipo de PII incorporado: se agrega como regex.

## 7. MCP (herramientas de un servidor MCP o de AgentCore Gateway)
```python
from strands.tools.mcp import MCPClient
cliente = MCPClient(url="https://<gateway-url>/mcp", headers={"Authorization": f"Bearer {token}"})
with cliente:
    agente = Agent(model=..., tools=cliente.list_tools_sync())
```
Firma: `MCPClient(transport_callable=None, *, url=None, headers=None, auth=None, prefix=None, tool_filters=None, ...)`.

## 8. Herramientas incluidas (`strands_tools`)
`calculator`, `current_time`, `http_request`, `use_aws`, `retrieve` (Knowledge Bases), `code_interpreter`, `speak`, `workflow`, `swarm`, `graph`, `agent_core_memory`, `mcp_client`, `handoff_to_user` (humano en el ciclo), `think`...
```python
from strands_tools import calculator, current_time
```

## 9. Modelo local para probar sin Bedrock
```python
# model/load.py
import os
from strands.models.bedrock import BedrockModel

def load_model():
    if os.getenv("LOCAL_MODEL") == "ollama":
        from strands.models.ollama import OllamaModel
        return OllamaModel(host="http://localhost:11434", model_id="qwen3:8b", temperature=0)
    return BedrockModel(model_id="global.anthropic.claude-sonnet-5-5")
```

## 10. Pruebas
```python
# tests/test_herramientas.py: TDD de herramientas (deterministas)
def test_inscritos_sin_ingreso_filtra_por_empresa(db_mock):
    assert inscritos_sin_ingreso("ev1", "Arquitectos S.A.") == ["Luis Pérez"]

# tests/test_eval_agente.py: caso de evaluación (comportamiento del agente)
def test_agente_usa_herramienta_para_ausentes():
    r = agente("¿Quién falta de Arquitectos S.A.?")
    assert "inscritos_sin_ingreso" in r.metrics.tool_metrics
    assert "Luis" in str(r)
```
Para acelerar las pruebas y no gastar tokens, prueba las herramientas directamente; los casos de evaluación, pocos y marcados con `@pytest.mark.eval`.

Registra el marcador en `pyproject.toml` para que la suite rápida no cargue el modelo:
```toml
[tool.pytest.ini_options]
markers = ["eval: casos de evaluación del agente (requieren modelo)"]
addopts = "-m \"not eval\""
```
Correr evaluaciones: `LOCAL_MODEL=ollama uv run pytest -m eval`.

En las aserciones de evaluación usa límites de palabra (`re.search(r"\b3\b", texto)`; `"2" in texto` también coincide con "20 %" o "2026") y verifica **todos** los elementos esperados, no solo uno. Prueba sin modelo que una herramienta no expone el alcance:
```python
def test_herramienta_no_recibe_el_evento():
    props = agente.contar_asistencia.tool_spec["inputSchema"]["json"].get("properties", {})
    assert "evento_id" not in props
```

## 11. System prompt que funciona (verificado en el laboratorio del reto 1)
```python
SYSTEM_PROMPT = """Eres el asistente de <dominio> de CONFA para <usuario>.

Tono: cálido, cercano y profesional. Empieza directamente con la respuesta;
nunca repitas lemas, saludos de marca ni frases institucionales.

Formato: texto plano en español, máximo 3 frases, sin emojis ni markdown.
Ejemplo: "<una respuesta ideal, corta y con cifras>"

Reglas:
- Toda cifra o nombre sale de una herramienta. Nunca estimes ni inventes datos.
- Solo respondes sobre <alcance>. Si te preguntan otra cosa, dilo con amabilidad.
- Nunca muestres números de cédula ni otros datos personales.
"""
```
Con el lema entre comillas en el prompt, el modelo empezaba cada respuesta con "Contigo, con todo:" y llenaba de emojis.

## 12. Herramienta con alcance fijo (el modelo no elige el evento)
```python
EVENTO_ACTIVO = os.getenv("EVENTO_ACTIVO", "ev-001")   # bloque de auth: sale del JWT del usuario

@tool
def ausentes_por_grupo(empresa: str) -> list[str]:
    """Lista los inscritos de una empresa que aún no ingresan al evento actual. ..."""
    return consultas.ausentes_por_grupo(EVENTO_ACTIVO, empresa)
```

## 13. Texto en español: comparar sin mayúsculas ni tildes
`lower()` de SQLite (y de muchos motores con su configuración por defecto) solo pasa a minúsculas el ASCII: "CAFÉ" ≠ "café". Normaliza en Python:
```python
import unicodedata
def normalizar_texto(t: str) -> str:
    sin_tildes = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return " ".join(sin_tildes.casefold().split())
```

## 14. Conexiones y hora
- `with sqlite3.connect(...) as c:` hace commit pero **no cierra** la conexión: usa un `@contextmanager` que haga `close()`.
- Lambda y AgentCore corren en UTC: guarda la hora con zona (`datetime.now(ZoneInfo("America/Bogota"))`).
