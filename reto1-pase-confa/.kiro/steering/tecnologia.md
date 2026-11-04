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
| Frontend | **Angular** (versión estable actual, componentes *standalone* y *signals*) como PWA: `npx @angular/cli@latest new frontend --routing --style=scss` y `ng add @angular/pwa` (service worker de Angular) |
| Backend | Python en AWS Lambda detrás de API Gateway (API Puerta, Eventos, Consultas, Asistente, Virtual, Purga) |
| Infraestructura | AWS CDK propio en `infra/` para Lambdas, API Gateway, Cognito, S3, CloudFront, WAF, EventBridge. AgentCore lo maneja su CLI |
| Datos | RDS PostgreSQL del evento con **esquema propio** (migraciones versionadas en `backend/db/migrations/`). Mocks con contrato documentado para lo que no exista |
| Pruebas | pytest (herramientas, reglas, contingencias y seguridad); Vitest con `ng test` para la lógica sin conexión del frontend (`puerta-offline`); casos de evaluación para el comportamiento del agente |

## Estructura del repositorio
```
<proyecto-agentcore>/        ← creado con agentcore create
  agentcore/agentcore.json   ← recursos declarados (runtimes, memories, gateways)
  agentcore/aws-targets.json ← cuenta y región de despliegue
  app/<agente>/main.py       ← agente Strands (entrypoint)
  app/<agente>/tools/        ← herramientas @tool
  app/<agente>/tests/        ← pytest
backend/                     ← Lambdas en Python
  apis/<api>/                ← puerta, eventos, consultas, asistente, virtual, purga
  comun/                     ← reglas compartidas (semáforo, documentos, ClienteFacial)
  db/migrations/             ← esquema propio versionado
  tests/                     ← pytest
infra/                       ← AWS CDK (todo lo que no es AgentCore)
frontend/                    ← Angular (PWA)
  src/app/puerta-offline/    ← lógica sin conexión en TypeScript puro, con pruebas Vitest
mocks/                       ← mocks con su contrato (OpenAPI)
docs/                        ← working-backwards.md, presentacion/
.kiro/specs/<slug>/          ← requirements.md, design.md, tasks.md
```

## Convenciones
- Python con type hints. Cada `@tool` con docstring: qué hace, Args y Returns.
- Angular: componentes *standalone*, `signals` para el estado, `HttpClient` con interceptor que agrega el JWT de Cognito, plantillas sin `bypassSecurityTrust*` ni `innerHTML` con datos externos, textos en español. Ningún secreto en `environment.ts`.
- Configuración por variables de entorno (`agentcore/.env.local` en local; nunca en git).
- Región: **us-east-1** (confirmado). IDs de modelo con perfil de inferencia (`us.` o `global.`); Claude Haiku 4.5 habilitado.
- Detalle técnico: skill `agentcore-strands`.
