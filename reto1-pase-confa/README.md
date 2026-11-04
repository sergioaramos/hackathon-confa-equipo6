# Pase CONFA

Ingreso a eventos de CONFA en segundos, con rostro, QR o documento, con o sin internet. Reto 1 de la hackathon CONFA × AWS.

- Spec: `.kiro/specs/pase-confa/` (requisitos, diseño y tareas).
- Working Backwards: `docs/working-backwards.md`.

## Estructura
```
backend/     Lambdas en Python (apis/, comun/, db/migrations/, tests/)
infra/       AWS CDK (todo lo que no es AgentCore)
frontend/    PWA en Angular
mocks/       mocks con su contrato (OpenAPI)
```

## Ramas
- `main`: versión estable; se actualiza por *pull request*.
- `feature/backend`: APIs, base de datos, agente e infraestructura.
- `feature/frontend`: PWA en Angular.

## Correr las pruebas del backend
```
cd backend
uv sync
uv run pytest
```
Las pruebas siempre usan el mock de la API facial: si `FACIAL_MODO=real`, la suite se detiene.

Las pruebas levantan su propio PostgreSQL embebido (`pgserver`), sin Docker. Para desarrollo, `uv run python -m db.local` levanta una base en `backend/.pgdata` (no se versiona) solo en `127.0.0.1`, aplica las migraciones, carga la semilla ficticia e imprime el `PASE_DB_URL`. La semilla usa documentos del rango `99000000NN`; los rostros reales del equipo nunca van en el repositorio.

## Correr el agente en local
Proyecto AgentCore en `PaseConfa/` (plantilla `agent-python-strands`). Crea `PaseConfa/agentcore/.env.local` (no se versiona) con:
```
AWS_PROFILE=hackathon-confa
AWS_REGION=us-east-1
MODELO_BEDROCK=us.anthropic.claude-haiku-4-5-20251001-v1:0
```
Luego:
```
cd PaseConfa
agentcore dev --mode headless
```
En Windows PowerShell, `agentcore invoke --payload` parte el JSON por las comillas. Para probar, llama directo al servidor local:
```powershell
$cuerpo = @{ prompt = '¿Cuántos han entrado?'; actorId = 'u1' } | ConvertTo-Json -Compress
Invoke-WebRequest -Uri http://127.0.0.1:8080/invocations -Method Post -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($cuerpo)) -UseBasicParsing
```

Cómo correr la demo completa en 3 comandos: pendiente (tarea 101).
