> **Borrador de referencia** preparado antes del evento. La spec oficial se genera en Kiro durante la hackathon en `.kiro/specs/pase-confa/`, usando este archivo como insumo.

# Tareas: Pase CONFA

Convenciones: `[P]` = puede ir en paralelo (repartir entre los 3 integrantes). TDD en lo crítico: la tarea de pruebas va primero (rojo) y la de implementación la pone en verde.

## Bloque 1 · Punta a punta mínimo (MVP; meta: miércoles antes de las 4:00 p. m.)
- [ ] 1. Crear el proyecto con `agentcore create --name PaseConfa --template agent-python-strands` y dejar `model/load.py` con Claude Haiku 4.5 (y modo `LOCAL_MODEL=ollama` para probar sin Bedrock)
  - Hecha cuando: `agentcore dev` levanta y `agentcore invoke --runtime agent --local` responde
  - _Requisitos: 6_
- [ ] 2. [P] Esquema de datos (eventos, inscritos, asistencias) con repositorio y datos de demo ficticios
  - Hecha cuando: se crea la base de datos local con 1 evento y 10 inscritos ficticios
  - _Requisitos: 2, 3, 4, 10.1_
- [ ] 3. Pruebas de `contar_asistencia` y `ausentes_por_grupo` (rojo)
  - Hecha cuando: pytest falla porque las herramientas no existen
  - _Requisitos: 6.1, 6.2_
- [ ] 4. Implementar `contar_asistencia` y `ausentes_por_grupo` (verde)
  - Hecha cuando: las pruebas de la tarea 3 pasan; `ausentes_por_grupo` no devuelve cédulas
  - _Requisitos: 6.1, 6.2, 10.4_
- [ ] 5. Pruebas de la validación por documento: inscrito, no inscrito, ya ingresó (rojo)
  - _Requisitos: 4.2, 3.4, 3.5_
- [ ] 6. Implementar `validar_documento` en el servicio de la puerta (verde)
  - Hecha cuando: las pruebas de la tarea 5 pasan; un segundo ingreso no duplica la asistencia
  - _Requisitos: 4.2, 3.4, 3.5, 4.3_
- [ ] 7. Caso de evaluación del agente: "¿cuántos han entrado?" → `contar_asistencia`; "¿quién falta de X?" → `ausentes_por_grupo`
  - _Requisitos: 6.1, 6.2_
- [ ] 8. Conectar las herramientas al agente con el system prompt del diseño
  - Hecha cuando: el caso de evaluación de la tarea 7 pasa con `agentcore dev`
  - _Requisitos: 6_
- [ ] 9. [P] Pantalla mínima (React): campo de cédula para validar + chat con el asistente
  - Hecha cuando: desde el navegador se valida una cédula y se pregunta cuántos han entrado
  - _Requisitos: 4.2, 6_
- [ ] 10. `agentcore deploy` en la cuenta del evento e invocar el agente desplegado
  - _Requisitos: 6_
- [ ] 11. Auditar el bloque: `/auditoria codigo tests strands seguridad`

## Bloque 2 · Validación facial (flujo principal)
- [ ] 12. [P] Mock de la API facial con el contrato del diseño (`POST /reconocer`)
  - _Requisitos: 3_
- [ ] 13. Pruebas de `validar_rostro`: reconocido e inscrito, no reconocido, no inscrito, ya ingresó, timeout de 5 s (rojo)
  - _Requisitos: 3.1-3.6_
- [ ] 14. Implementar `validar_rostro` con timeout; la imagen nunca se persiste (verde)
  - _Requisitos: 3.1-3.6, 10.1_
- [ ] 15. Pantalla Puerta: cámara del navegador + aviso de consentimiento con "Prefiero QR"
  - _Requisitos: 3, 10.2_
- [ ] 16. Cambiar el mock por la API facial real (endpoint y autenticación del kickoff) y medir su latencia
  - _Requisitos: 3.1_
- [ ] 17. Auditar el bloque: `/auditoria codigo tests seguridad`

## Bloque 3 · Contingencias
- [ ] 18. Pruebas del QR: generar, verificar, alterado, de otro evento, ya usado (rojo)
  - _Requisitos: 2.1, 2.3, 4.1_
- [ ] 19. Implementar QR firmado con HMAC (secreto en Secrets Manager) (verde)
  - _Requisitos: 2.1, 2.3, 4.1_
- [ ] 20. Prueba e implementación: inscrito menor de edad → sin reconocimiento facial
  - _Requisitos: 10.3_
- [ ] 21. [P] Lector de QR en la pantalla Puerta
  - _Requisitos: 4.1_
- [ ] 22. Auditar el bloque: `/auditoria codigo tests seguridad`

## Bloque 4 · Seguridad
- [ ] 23. Guardrail de Bedrock (ataques de prompt, regex de cédula, temas denegados) conectado al modelo del agente
  - _Requisitos: 10.4, 10.5, 6.3_
- [ ] 24. Casos de evaluación: pregunta fuera de tema, intento de obtener cédulas, intento de ver otro evento
  - _Requisitos: 6.3, 10.4, 10.5_
- [ ] 25. Login del personal (Cognito) y validación del JWT en la API y en el Runtime; filtro por eventos asignados
  - _Requisitos: 9.1, 9.2_
- [ ] 26. Auditar el bloque: `/auditoria seguridad agentcore`

## Bloque 5 · AgentCore Memory y Gateway
- [ ] 27. `agentcore add memory` con `--event-expiry-duration 3 --strategies SUMMARIZATION` y `actorId` del usuario real
  - _Requisitos: 6 (preguntas encadenadas)_
- [ ] 28. `agentcore add gateway` + target de la API Consultas; el agente consume las herramientas por MCP (plan B: `@tool` HTTP)
  - _Requisitos: 6_
- [ ] 29. Auditar el bloque: `/auditoria agentcore strands`

## Bloque 6 · Tablero y deseables
- [ ] 30. [P] Tablero en tiempo real: ingresados, inscritos, %, desglose por método (actualizado cada ≤ 5 s)
  - _Requisitos: 7.1, 7.2_
- [ ] 31. Crear evento desde lenguaje natural (`EventoPropuesto` + confirmación) con pruebas de extracción
  - _Requisitos: 1.1-1.3_
- [ ] 32. Informe de cierre + CSV + resumen con Nova Micro
  - _Requisitos: 8.1_
- [ ] 33. Foto grupal con Rekognition `DetectFaces` (si la API facial acepta recortes)
  - _Requisitos: 5.1, 5.2_

## Bloque 7 · Verificación y entrega
- [ ] 34. Datos de demo ficticios y guion de la demo (incluye la contingencia en vivo)
- [ ] 35. `/auditoria agentcore seguridad` + `agentcore deploy` final
- [ ] 36. `/auditoria spec-rubrica` (nota estimada y 3 mejoras)
- [ ] 37. `/presentacion`

## Trazabilidad
Todos los criterios de los requisitos 1-10 tienen al menos una tarea. Huecos: ninguno. Riesgos: la latencia de la API facial (tarea 16) y Gateway con SigV4 (tarea 28, con plan B).
