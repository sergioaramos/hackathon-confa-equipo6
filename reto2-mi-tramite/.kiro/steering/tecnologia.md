---
inclusion: always
---
# Tecnología

## Stack
| Capa | Herramienta |
|---|---|
| Agentes | Strands Agents (Python ≥ 3.10) |
| Ejecución | Amazon Bedrock AgentCore: Runtime + Memory y/o Gateway (+ Identity, Observability) |
| CLI | `@aws/agentcore` (`agentcore create/dev/deploy/invoke`). **No** usar `bedrock-agentcore-starter-toolkit` ni `agentcore configure/launch` |
| Modelos | Amazon Bedrock, por tarea (tabla en `design.md`) |
| Seguridad del modelo | Amazon Bedrock Guardrails |
| Frontend | React + Vite (`npm create vite@latest`) |
| Datos | RDS del evento (CONFA entrega la conexión en el kickoff). Mocks con contrato documentado para lo que no exista |
| Pruebas | pytest (herramientas y reglas); casos de evaluación para el comportamiento del agente |

## Estructura del repositorio
```
<proyecto-agentcore>/        ← creado con agentcore create
  agentcore/agentcore.json   ← recursos declarados (runtimes, memories, gateways)
  agentcore/aws-targets.json ← cuenta y región de despliegue
  app/<agente>/main.py       ← agente Strands (entrypoint)
  app/<agente>/tools/        ← herramientas @tool
  app/<agente>/tests/        ← pytest
frontend/                    ← React + Vite
mocks/                       ← mocks con su contrato (OpenAPI)
docs/                        ← working-backwards.md, presentacion/
.kiro/specs/<slug>/          ← requirements.md, design.md, tasks.md
```

## Convenciones
- Python con type hints. Cada `@tool` con docstring: qué hace, Args y Returns.
- Configuración por variables de entorno (`agentcore/.env.local` en local; nunca en git).
- Región: la del evento (confirmar en el kickoff). IDs de modelo con perfil de inferencia (`us.` o `global.`).
- Detalle técnico: skill `agentcore-strands`.
