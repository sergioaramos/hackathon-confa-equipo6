---
name: agentcore-strands
description: Referencia técnica VERIFICADA de Strands Agents y de la CLI de Amazon Bedrock AgentCore (@aws/agentcore 1.0.1). Úsala siempre que escribas código de agentes, herramientas @tool, grafos multiagente, Guardrails, Memory o Gateway, o comandos agentcore (create, dev, deploy, invoke). Evita usar comandos o APIs de memoria, que suelen estar desactualizados.
---

# AgentCore + Strands: referencia verificada

Verificado el **3 nov 2026** con `@aws/agentcore` 1.0.1, `strands-agents` 1.63.0, `strands-agents-tools` 0.8.12 y `bedrock-agentcore` 1.25.2, ejecutando los comandos reales.

## ⚠️ Errores que NO cometer
| ❌ Viejo o incorrecto | ✅ Correcto |
|---|---|
| `pip install bedrock-agentcore-starter-toolkit` | `npm install -g @aws/agentcore` (desinstala el toolkit viejo: chocan) |
| `agentcore configure` / `agentcore launch` | `agentcore create` → `agentcore dev` → `agentcore deploy` |
| `agentcore invoke --prompt "..."` en un Runtime | `agentcore invoke --runtime <nombre> --payload '{"prompt":"..."}'` (`--prompt` es solo para un *harness*) |
| `agentcore invoke --local --payload ...` | Agrega `--runtime <nombre>`: es obligatorio |
| IDs de modelo sin prefijo (`anthropic.claude-...`) | Con perfil de inferencia: `us.` o `global.` (`global.anthropic.claude-sonnet-5-5`) |
| `agent.structured_output(...)` como único camino | `agent(prompt, structured_output_model=Modelo)` → `resultado.structured_output` |
| `@tool def consultar(evento_id: str, ...)`: el **modelo** decide el alcance | El alcance (evento, colaborador, usuario) va **fijo en código** o sale del JWT; nunca es parámetro de la herramienta. Un prompt malicioso puede pedir otro evento |
| Dejar la memoria de la plantilla tal cual (`eventExpiryDuration: 30`, 4 estrategias) | `agentcore remove memory --name agentMemory` + `agentcore add memory --name agentMemory --event-expiry-duration 3 --strategies SUMMARIZATION`, y ajustar `memory/session.py` a los namespaces que quedan |
| `NullConversationManager` de la plantilla (historial infinito) | `SlidingWindowConversationManager(window_size=20)` |
| Construir el agente en `main.py` y aparte en las pruebas | Una sola fábrica `crear_agente(**kwargs)`; `main.py` le pasa `session_manager` y `conversation_manager`. Lo que se prueba es lo que se despliega |
| System prompt con el lema entre comillas (`tono "Contigo, con todo"`) | El modelo lo copia literal al inicio de cada respuesta. Describe el tono con adjetivos, prohíbe lemas y emojis, y da un ejemplo de respuesta (ver `references/strands.md` §11) |

## Flujo de la CLI
```bash
agentcore create --name <Proyecto> --template agent-python-strands   # crea el proyecto (+ uv sync y npm install)
cd <Proyecto>
agentcore dev                       # servidor local en :8080 (carga agentcore/.env.local)
agentcore dev --mode browser        # igual, con el Agent Inspector en el navegador
agentcore invoke --runtime agent --local --payload '{"prompt":"hola","actorId":"u1"}'
agentcore deploy                    # despliega con CDK a la cuenta y región de aws-targets.json (la crea en el primer deploy)
agentcore invoke --runtime agent --payload '{"prompt":"hola"}'
agentcore status | agentcore logs | agentcore traces
```
Detalle de comandos, plantillas y recursos (`add memory`, `add gateway`, `add gateway-target`, `add credentials`): `references/cli.md`.

## Estructura que genera `agent-python-strands`
```
<Proyecto>/
├── agentcore/agentcore.json      ← runtimes, memories, agentCoreGateways, credentials...
├── agentcore/aws-targets.json    ← [] hasta el primer deploy
├── agentcore/.env.local          ← variables para `agentcore dev` (gitignored)
├── agentcore/cdk/                ← infraestructura generada (no editar a mano)
└── app/agent/
    ├── main.py                   ← BedrockAgentCoreApp + @app.entrypoint + Agent
    ├── model/load.py             ← load_model(): BedrockModel(model_id=...)
    ├── memory/session.py         ← AgentCoreMemorySessionManager (usa MEMORY_<NOMBRE>_ID)
    ├── parse.py                  ← payload: prompt | messages, actorId
    └── pyproject.toml            ← dependencias (uv add <paquete>)
```
Payload del Runtime: `{"prompt": "...", "actorId": "..."}`. La sesión llega en el header `X-Amzn-Bedrock-AgentCore-Runtime-Session-Id` (`context.session_id`); reutilízala para continuar una conversación.

## Patrones de código
Ver `references/strands.md`: herramientas `@tool`, agentes como herramienta (`as_tool`), Graph, Swarm, salida estructurada, Guardrails, MCP/Gateway y pruebas con pytest.

## Probar sin Bedrock (modelo local)
`model/load.py` puede devolver `OllamaModel` cuando `LOCAL_MODEL=ollama` (en `agentcore/.env.local`). Requiere `uv add "strands-agents[ollama]"` en `app/agent`. Verificado con `agentcore dev` + `invoke --local`. Ejemplo en `references/strands.md`.
