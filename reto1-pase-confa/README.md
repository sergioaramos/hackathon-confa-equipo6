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

Cómo correr la demo completa en 3 comandos: pendiente (tarea 101).
