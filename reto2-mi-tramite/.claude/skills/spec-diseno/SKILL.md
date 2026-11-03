---
name: spec-diseno
description: Fase 2 de la spec (CÓMO). Convierte requirements.md en .kiro/specs/<slug>/design.md con arquitectura, diagrama Mermaid, patrón de agentes, modelos de Bedrock justificados por tarea, piezas de AgentCore y capas de seguridad. Úsala después de /spec-requisitos.
---

# Spec 2 · Diseño (CÓMO)

Entrada: `requirements.md`. Salida: `.kiro/specs/<slug>/design.md`. Aquí se decide la **arquitectura agéntica** (15 pts) y se prepara la defensa ante el jurado.

Antes de decidir, lee `references/decisiones.md` (guías de patrón, modelos, AgentCore y seguridad). Para nombres de servicios, IDs y comandos, usa la skill `agentcore-strands`.

## Decisiones obligatorias (en este orden)
1. **Qué NO es IA.** Recorre los requisitos y marca lo determinista (reglas fijas, flujos siempre iguales, validaciones exactas) como código o servicio. Decir dónde no se usa IA demuestra criterio (Invent & Simplify).
2. **Agentes y patrón.** Empieza por un solo agente; agrega otro solo si cumple una razón de `decisiones.md` (modelo distinto, permisos distintos o prompt inmanejable). Elige el patrón por componente.
3. **Modelo por tarea**, con la fórmula de una línea: "Para <tarea> usamos <modelo> porque <criterio>; uno más grande no mejora el resultado y sí aumenta <costo/latencia>".
4. **AgentCore**: Runtime + Memory y/o Gateway como mínimo, cada pieza con su razón. Memory: qué se recuerda, por cuánto tiempo y qué **nunca** se guarda.
5. **Integraciones**: API facial / RDS / mocks (con contrato OpenAPI) / Step Functions / SES, según el reto.
6. **Seguridad** por capas (ver `.kiro/steering/seguridad.md`) y Guardrails concretos.

## Plantilla de design.md
```markdown
# Diseño: <nombre>
## Resumen
## Arquitectura          ← diagrama Mermaid (flowchart LR) del cliente al dato
## Componentes           ← tabla: componente | tipo (agente/código/servicio) | responsabilidad | requisitos
## Agentes               ← por agente: patrón, modelo, herramientas (@tool con firma), system prompt resumido
## Modelos de Bedrock    ← tabla: tarea | modelo | justificación (fórmula de una línea)
## AgentCore             ← tabla: pieza | uso | por qué
## Datos                 ← modelo de datos (tablas RDS) + contratos de mocks
## Flujos                ← sequenceDiagram del flujo principal y de la contingencia
## Seguridad             ← capas 1-4, Guardrails, retención, consentimiento
## Manejo de errores     ← qué pasa si falla cada integración
## Estrategia de pruebas ← qué lleva TDD (pytest) y qué lleva casos de evaluación
## Decisiones y alternativas descartadas
## Preguntas probables del jurado ← 5 preguntas con la respuesta de una línea
```

## Reglas
- Cada componente referencia los requisitos que cumple (`Req 1.2`). Si un requisito no tiene componente, es un hueco: repórtalo.
- Los diagramas deben poder ir tal cual a la presentación.
- Nada de servicios "por si acaso": cada pieza con su razón.

Cierra con los huecos encontrados y el siguiente paso: `/spec-tareas`.
