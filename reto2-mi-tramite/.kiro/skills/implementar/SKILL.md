---
name: implementar
description: Fase 4. Implementa UNA tarea de .kiro/specs/<slug>/tasks.md por invocación con ciclo TDD (rojo, verde, refactor) y la marca como hecha. Acepta el número de tarea o "siguiente". Úsala después de /spec-tareas.
---

# Implementar una tarea

Argumento: número de tarea (`3`) o vacío para la **primera sin marcar**. Si se pasa `bloque`, encadena las tareas del bloque actual y se detiene en el primer fallo.

## Ciclo
1. Lee **solo** la tarea, sus requisitos referenciados y la sección pertinente de `design.md`. No recorras el repo entero.
2. Si la tarea es de lógica crítica (herramienta, regla, contingencia, seguridad):
   - **Rojo**: escribe la prueba pytest primero y córrela; debe fallar por la razón correcta.
   - **Verde**: implementación mínima para pasarla.
   - **Refactor**: limpia sin cambiar el comportamiento; vuelve a correr la prueba.
3. Si es comportamiento del agente: escribe primero el caso de evaluación (pregunta → herramienta esperada y criterio de la respuesta) y verifica con el agente en local (`agentcore dev` + `agentcore invoke --local`).
4. Si es frontend o infraestructura: implementa y verifica a mano, diciendo qué verificaste.
5. Para todo código de agentes, CLI o AgentCore, **usa la skill `agentcore-strands`**. No uses comandos ni APIs de memoria.
6. Marca la tarea `- [x]` en `tasks.md`.
7. Reporta en 3 líneas: qué hiciste, cómo lo verificaste y cuál es la siguiente tarea.

## Reglas
- Si la tarea exige algo que la spec no dice, **detente y avisa**: primero se corrige la spec (es evidencia para el jurado).
- Sin secretos en el código: variables de entorno, AgentCore Identity o roles.
- Respeta `.kiro/steering/seguridad.md`: ninguna imagen facial persistida y ningún diagnóstico expuesto.
- Prueba de la tarea, no la suite entera. La suite completa corre en la auditoría del bloque.
- Al cerrar el último bloque, recuerda la tarea de auditoría del bloque.
