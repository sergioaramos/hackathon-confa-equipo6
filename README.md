# Equipo 6 · Agentic Mindset Hackathon CONFA × AWS

Sergio Ramos (líder) · Luis David Agudelo · 4 y 5 de noviembre de 2026 · Manizales

Repo privado del equipo. Hay **una carpeta por reto**; mañana se elige una y se trabaja solo en esa.

| Carpeta | Reto | Solución propuesta |
|---|---|---|
| `reto1-pase-confa/` | 1 · Experiencia y control de eventos | **Pase CONFA**: ingreso en segundos con rostro, QR o cédula; asistente que responde quién entró y quién falta |
| `reto2-mi-tramite/` | 2 · Autogestión de solicitudes de GTH | **Mi Trámite CONFA**: radicar en lenguaje natural, ver siempre en qué va, rutas que GTH crea sin programar |

Cada carpeta ya trae:
- `.kiro/skills/`: las 8 skills del [kit](https://github.com/sergioaramos/kit-hackathon-confa) (Working Backwards → spec → implementar → auditoría → presentación).
- `.kiro/steering/`: `producto.md` ya lleno con el reto, `tecnologia.md` y `seguridad.md` (Ley 1581).
- `.claude/`: las mismas skills y los 6 auditores para Claude Code.
- `docs/working-backwards.md`: las 5 preguntas y el comunicado de prensa.
- `docs/referencia/`: **borradores** de `requirements.md`, `design.md` y `tasks.md` hechos en la preparación (y la presentación en el reto 1).
- `evidencia-y-supuestos.md`, `scripts/revisar_secretos.py`.

`idea-plataforma.md` tiene los textos para registrar la idea en la plataforma (una sola por equipo).

## Mañana, paso a paso

**8:00 · Kickoff**
1. Elegir el reto.
2. Preguntar a los mentores: modelos de Bedrock y región habilitados en la cuenta del evento; endpoint de la API facial y datos de la RDS; datos reales de filas (reto 1) o de solicitudes de GTH (reto 2).
3. Encuesta a mano alzada a los participantes (ver `docs/working-backwards.md`, preguntas abiertas).
4. Actualizar `docs/working-backwards.md` con lo aprendido (`/working-backwards`).

**9:00 · Spec en Kiro** (abrir en Kiro **la carpeta del reto**, no la raíz del repo)
1. `/spec-requisitos` usando `docs/referencia/requirements.md` como punto de partida y lo nuevo del kickoff.
2. `/spec-diseno` con `docs/referencia/design.md`.
3. `/spec-tareas` con `docs/referencia/tasks.md`.

Las specs oficiales quedan en `.kiro/specs/<slug>/`, hechas en Kiro durante el evento. Los borradores aceleran, pero no reemplazan ese paso.

**10:30 · Construir**
- `/implementar` una tarea a la vez, con TDD en lo crítico.
- Al cerrar cada bloque: `/auditoria codigo tests strands` (y `seguridad` si tocó datos). Guardar el informe en `docs/auditorias/`.
- Meta: **algo funcionando de punta a punta a las 4:00 p. m.**, desplegado en AgentCore.

**Jueves 8:00 · Pulir**
- `/auditoria spec-rubrica` → las 3 mejoras de último momento.
- `/presentacion` (en el reto 1 ya hay un borrador en `docs/referencia/presentacion/`).
- Ensayar con el cronómetro: **10 minutos máximo**.

## Reparto sugerido (ajustar)
| | Sergio | Luis David |
|---|---|---|
| Mañana | Spec y agente (Strands + AgentCore) | Datos, mocks y pantallas |
| Tarde | Integración y despliegue | Demo y guion |
| Jueves | Presentación | Ensayo y video de respaldo |

## Reglas que no se negocian
- Solo datos ficticios o entregados para el evento. Ninguna foto, cédula o incapacidad real.
- Nada de credenciales en el código: `python scripts/revisar_secretos.py` antes de cada commit.
- Ningún código sin tarea en `tasks.md`; si cambia la idea, se cambia primero la spec.
- Confirmar con la organización el uso de Claude Code (cuenta corporativa) durante el evento; Kiro es la herramienta principal.
