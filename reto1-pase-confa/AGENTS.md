# AGENTS.md — Reglas del proyecto (hackathon CONFA × AWS)

## Contexto
Solución con agentes de IA para un reto de CONFA (Caja de Compensación Familiar de Caldas). Ver `.kiro/steering/producto.md` para el reto, el cliente y el comunicado de prensa.

## Flujo obligatorio
Spec primero: `docs/working-backwards.md` → `.kiro/specs/<slug>/requirements.md` → `design.md` → `tasks.md` → código.
- Ningún código sin tarea en `tasks.md`. Si hay que hacer algo que no está en la spec, primero se actualiza la spec.
- Una tarea por vez. Al terminarla, se marca `- [x]`.

## Stack
- Agentes: **Strands Agents** (Python). Despliegue: **Amazon Bedrock AgentCore** con la CLI `@aws/agentcore` (no el starter toolkit viejo).
- Modelos: Amazon Bedrock, elegidos por tarea (ver `design.md`).
- Frontend: Angular (PWA). Backend: Lambdas en Python. Datos: RDS del evento con esquema propio; lo que no exista se simula con mocks con contrato documentado.
- Detalle técnico verificado: skill `agentcore-strands`.

## Reglas de código
- TDD en lo crítico: herramientas de los agentes, reglas de negocio, contingencias y reglas de seguridad. El frontend no exige TDD, salvo la lógica sin conexión (`puerta-offline`), que es contingencia y se prueba con Vitest.
- Cada `@tool` con type hints y docstring que diga qué hace, qué recibe y qué devuelve.
- Lo determinista es código, no LLM.
- Respuestas al usuario en español, con el tono de CONFA ("Contigo, con todo").

## Seguridad (no negociable)
Ver `.kiro/steering/seguridad.md`. En resumen: nada de credenciales en el código, no se guardan imágenes faciales, el aprobador nunca ve diagnósticos, solo datos ficticios o entregados para el evento.
