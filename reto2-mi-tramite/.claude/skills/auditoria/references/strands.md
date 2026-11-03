# Lente: strands (buenas prácticas de agentes) — Arquitectura agéntica, 15 pts

Referencia de APIs correctas: skill `agentcore-strands`.

## Herramientas (`@tool`)
- [ ] Cada herramienta tiene **type hints** completos y un **docstring** con qué hace, Args y Returns. Es lo que lee el modelo: un docstring vago produce llamadas equivocadas.
- [ ] Nombres en verbo + objeto, sin ambigüedad entre herramientas (`registrar_asistencia` frente a `consultar_asistencia`).
- [ ] Las herramientas **manejan sus errores** y devuelven un mensaje útil ("cédula no inscrita en el evento ev1") en lugar de lanzar excepciones crudas.
- [ ] Las herramientas son **deterministas y probables sin LLM** (la lógica vive en la herramienta, no en el prompt).
- [ ] **El alcance no es parámetro de la herramienta**: evento, colaborador o usuario van fijos en código o salen del JWT. Si el `@tool` recibe `evento_id`/`colaborador_id`, un prompt malicioso puede consultar datos ajenos (hallazgo real del laboratorio del reto 1).
- [ ] Ninguna herramienta devuelve más datos de los necesarios (tokens y privacidad).
- [ ] Timeouts en las llamadas HTTP a APIs externas (API facial, mocks).

## Agentes
- [ ] **Lo determinista no pasa por el LLM** (validación en la puerta, ejecución de rutas, cálculos).
- [ ] Cada agente extra está justificado (modelo distinto, permisos distintos o prompt inmanejable), como dice `design.md`.
- [ ] El patrón (agente único / `as_tool` / Graph / Workflow / Swarm) coincide con el diseño. No hay Swarm en el camino crítico de la demo.
- [ ] El **modelo de cada agente** coincide con la tabla de `design.md`; temperatura 0 en clasificación y extracción.
- [ ] El system prompt define rol, contexto de CONFA, idioma español, límites ("nunca inventes cifras: usa herramientas") y tono.
- [ ] El tono se describe con adjetivos; **no** hay lemas entre comillas (el modelo los copia literal) y hay reglas de formato explícitas (sin emojis, sin markdown, largo máximo) con un ejemplo de respuesta.
- [ ] Una sola fábrica del agente (`crear_agente`) usada por `main.py` y por las pruebas; `conversation_manager` con ventana (no `NullConversationManager`).
- [ ] Se usa **salida estructurada** (`structured_output_model`) donde el código consume la respuesta, en vez de parsear texto.
- [ ] Graph y Swarm con límites (`set_execution_timeout`, `max_handoffs`) para evitar ciclos.
- [ ] Streaming de respuestas hacia el frontend (`stream_async`) donde el usuario espera.
- [ ] El agente se construye una vez por sesión, no en cada llamada (la plantilla usa `lru_cache`).

## Anti-patrones
- [ ] Prompts gigantes con reglas de negocio que deberían ser código.
- [ ] Parseo de texto libre con regex sobre la respuesta del LLM.
- [ ] IDs de modelo sin prefijo de perfil de inferencia, o modelos no habilitados en la cuenta.
- [ ] APIs viejas: `bedrock-agentcore-starter-toolkit`, `agentcore configure/launch`.
