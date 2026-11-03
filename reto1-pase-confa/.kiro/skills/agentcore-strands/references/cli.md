# AgentCore CLI 1.0.1: referencia (salida real de `--help`, 3 nov 2026)

## Plantillas de `agentcore create --template`
| Plantilla | Para |
|---|---|
| `agent-python-strands` | **La de la hackathon**: Strands + AgentCore Memory, Bedrock u otro proveedor |
| `agent-python-strands-container` | Igual, desplegada como contenedor (agrega un Dockerfile) |
| `a2a-python-strands` | Agente que habla protocolo A2A |
| `agui-python-strands` | Agente con protocolo AG-UI (frontend con streaming) |
| `mcp-python-fastmcp` | Servidor MCP con herramientas (FastMCP) |
| `agent-python-minimal` | Python sin framework |
| `empty` | Proyecto sin runtime (por defecto) |

Opciones de `create`: `--name` (obligatorio), `--template`, `--skip-install`, `--skip-git`. Globales: `--region`, `--json`, `--debug`.
Sin flags, `agentcore create` abre un asistente que pregunta el proveedor del modelo (Bedrock, Anthropic, OpenAI, compatible con OpenAI, Gemini, LiteLLM).

## Comandos
| Comando | Uso |
|---|---|
| `create`, `add`, `remove`, `export`, `migrate` | Proyecto y recursos |
| `dev [--mode browser\|headless] [--port] [--no-traces] [--agent]` | Correr en local (puerto 8080) |
| `build`, `deploy [--target]`, `status` | Construir y desplegar (CDK) |
| `invoke --runtime\|--harness\|--gateway <n> [--local] [--payload] [--session-id] [--user-id]` | Invocar |
| `logs`, `traces` | Observabilidad |
| `runtime`, `gateway`, `memory`, `identity`, `eval` | Inspeccionar recursos desplegados |

## Recursos con `agentcore add`
```bash
# Memoria: retención de eventos crudos en días (3-365) y estrategias de largo plazo
agentcore add memory --name memoriaColaborador --event-expiry-duration 30 \
  --strategies SEMANTIC,USER_PREFERENCE,SUMMARIZATION     # también EPISODIC

# Gateway: APIs → herramientas MCP
agentcore add gateway --name herramientas --authorizer-type AWS_IAM     # o CUSTOM_JWT o NONE
agentcore add gateway --name herramientas --enable-semantic-search

# Targets del gateway (targetType: openApiSchema, lambdaFunctionArn, apiGateway, mcpServer, httpRuntime, smithyModel...)
agentcore add gateway-target --gateway herramientas --endpoint https://mi-mcp.example.com/mcp
agentcore add gateway-target --gateway herramientas --target-configuration file://target.json

# Credenciales (AgentCore Identity): API keys u OAuth fuera del código
agentcore add credentials api-key ...
agentcore add credentials oauth ...

# Otros: runtime, runtime-endpoint, harness, policy-engine, policy (Cedar), evaluator, online-eval
```
`add` solo modifica `agentcore/agentcore.json`; los recursos se crean con `agentcore deploy`.

## Variables de entorno que inyecta AgentCore
- `MEMORY_<NOMBRE_EN_MAYÚSCULAS>_ID`: por ejemplo, la memoria `agentMemory` → `MEMORY_AGENTMEMORY_ID`.
- `AWS_REGION`.
- `LOCAL_DEV=1` en `agentcore dev`.

## No verificado de punta a punta (verificar en la cuenta del evento)
- Cómo recibe el agente la URL del Gateway desplegado: consultarla con `agentcore status --json` o `agentcore gateway` y pasarla por variable de entorno.
- Un Gateway con `AWS_IAM` exige firmar las peticiones MCP con SigV4. Si complica, usa `CUSTOM_JWT` o, como plan B, llama la API directamente desde un `@tool`.
- `agentcore deploy` en la cuenta del evento (no se pudo probar: la cuenta de práctica no tiene cuota de Bedrock).
