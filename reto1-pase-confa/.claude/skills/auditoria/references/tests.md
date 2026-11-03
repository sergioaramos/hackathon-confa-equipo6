# Lente: tests (TDD y cobertura de criterios)

## Corre primero
`pytest -q` (o `uv run pytest -q` dentro de `app/<agente>`) y reporta el resultado real: cuántas pasan, cuántas fallan y el error principal. No supongas el resultado.

## Cobertura de la spec
- [ ] Cada criterio de aceptación de los requisitos **MVP** tiene al menos una prueba (pytest o caso de evaluación). Lista los criterios sin prueba.
- [ ] **Contingencias probadas** (patrón IF/THEN): persona no enrolada → QR, API facial caída, adjunto ilegible, trámite inexistente, aprobador ausente.
- [ ] **Reglas de seguridad probadas**: el aprobador no recibe el diagnóstico; no se persiste la imagen; una persona no ve las solicitudes de otra.

## Calidad de las pruebas
- [ ] Las pruebas de herramientas no dependen del LLM ni de la red (mocks de la API facial, la BD y el correo).
- [ ] Hay evidencia de TDD en lo crítico: la prueba existe para cada herramienta y regla (y, si hay historial, se escribió antes o junto con el código).
- [ ] Los casos de evaluación del agente verifican **qué herramienta se usó** (`resultado.metrics.tool_metrics`) y criterios de la respuesta, no el texto exacto.
- [ ] Las aserciones de cifras usan límites de palabra (`\b3\b`): `"2" in texto` pasa con "20 %" o "2026" (falso positivo real del laboratorio). Las listas se verifican completas.
- [ ] Hay casos de evaluación de seguridad: pedir una cédula, consultar fuera del alcance, pregunta fuera de tema.
- [ ] Hay una prueba sin modelo que verifica que las herramientas no exponen el alcance (`tool_spec`).
- [ ] Las reglas de seguridad críticas tienen prueba determinista además del caso de evaluación (el LLM puede fallar; la regla en código no).
- [ ] Los casos de evaluación son pocos, marcados (`@pytest.mark.eval`) y no bloquean la suite rápida.
- [ ] Las pruebas son deterministas (sin fechas actuales ni orden aleatorio sin controlar).

## Fuera de alcance
El frontend no requiere pruebas automatizadas en la hackathon; basta la verificación manual descrita en la tarea.
