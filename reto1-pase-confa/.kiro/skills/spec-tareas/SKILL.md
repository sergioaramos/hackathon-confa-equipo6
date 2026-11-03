---
name: spec-tareas
description: Fase 3 de la spec (PASOS). Descompone design.md en .kiro/specs/<slug>/tasks.md con tareas pequeñas trazables a los requisitos, TDD embebido y un primer recorrido de punta a punta. Úsala después de /spec-diseno y antes de /implementar.
---

# Spec 3 · Tareas

Entrada: `requirements.md` + `design.md`. Salida: `.kiro/specs/<slug>/tasks.md`.

## Reglas
1. **Tareas pequeñas** (15-45 min cada una), ordenadas por dependencia. Marca `[P]` las que pueden ir en paralelo; sirve para repartir entre los 3 integrantes.
2. **Cada tarea verificable y trazable**, en formato Kiro:
   ```
   - [ ] 3. Implementar la herramienta registrar_asistencia
     - Hecha cuando: pytest tests/test_asistencia.py en verde
     - _Requisitos: 2.1, 2.3_
   ```
3. **TDD embebido en lo crítico**: herramientas `@tool`, reglas de negocio, contingencias y reglas de seguridad. Cada bloque empieza con la tarea de escribir sus pruebas (en rojo) y termina con la de ponerlas en verde. El comportamiento del agente se prueba con **casos de evaluación** (ante la pregunta X, el agente llama la herramienta Y). El frontend no lleva TDD.
4. **Primero el recorrido de punta a punta (bloque 1, MVP)**: la versión más simple que funcione desde la pantalla del cliente hasta el dato, desplegada en AgentCore. Regla de la guía: algo funcionando el **miércoles en la tarde**. Después se profundiza.
5. **Bloques**:
   - **1 · Punta a punta mínimo**: proyecto `agentcore create`, una herramienta con su mock, agente, `agentcore dev`, pantalla mínima, `agentcore deploy`.
   - **2 · Flujo principal completo**.
   - **3 · Contingencias**.
   - **4 · Seguridad**: Guardrails, control de acceso, minimización.
   - **5 · Memory / Gateway / integraciones reales**.
   - **6 · Demo y métricas**: datos ficticios de demo, contadores de impacto.
   - **7 · Verificación**: auditorías y ensayo.
6. **Cierre de cada bloque**: una tarea "Auditar el bloque" con `/auditoria codigo tests strands` (y `seguridad` si tocó datos).
7. **Último bloque**: `/auditoria agentcore seguridad` antes del deploy final, `/auditoria spec-rubrica` y `/presentacion`.
8. **Trazabilidad**: todo criterio de `requirements.md` aparece en al menos una tarea. Si no, repórtalo como hueco. **No escribas "Huecos: ninguno" sin recorrer criterio por criterio**: en el laboratorio quedaron sin tarea la inscripción, el registro en sitio y el ritmo de ingreso.
9. **Todo requisito MVP en los bloques 1 a 4.** Si un MVP cae en un bloque tardío (por ejemplo, el tablero en tiempo real), muévelo o márcalo como riesgo.
10. **Identidad desde el bloque 1.** Si las herramientas sacan el usuario o su alcance de la sesión, el bloque 1 lleva una identidad simulada (usuario de prueba en la sesión) con su prueba de que nadie actúa por otra persona; Cognito la reemplaza después. Sin esto, el primer despliegue queda sin control de acceso.
11. **Toda pieza del diagrama de `design.md` tiene tarea** (Identity, Observability, cada Runtime, cada target de Gateway). Lo que no tenga tarea se quita del diagrama o se marca como evolución.
12. **Las reglas de seguridad críticas llevan prueba determinista**, no solo caso de evaluación del LLM (por ejemplo, "radicar rechaza una incapacidad sin soporte validado", "los logs no contienen el diagnóstico").

## Cierre
Reporta el número de tareas por bloque, las paralelizables, los huecos y el siguiente paso: `/implementar`.
