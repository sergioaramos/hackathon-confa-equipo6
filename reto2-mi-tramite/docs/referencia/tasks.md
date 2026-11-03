> **Borrador de referencia** preparado antes del evento. La spec oficial se genera en Kiro durante la hackathon en `.kiro/specs/mi-tramite/`, usando este archivo como insumo.

# Tareas: Mi Trámite CONFA

Convenciones: `[P]` = en paralelo (repartir entre los integrantes). TDD en lo crítico: la tarea de pruebas (rojo) va antes de la de implementación (verde). Todo requisito MVP está en los bloques 1 a 4.

## Bloque 1 · Punta a punta mínimo: vacaciones con aprobación del líder (meta: miércoles antes de las 4:00 p. m.)
- [ ] 1. Proyecto con `agentcore create --name MiTramite --template agent-python-strands`; ajustar memoria (`SUMMARIZATION,USER_PREFERENCE`, 30 días) y `session.py`; una sola fábrica `crear_agente`
  - Hecha cuando: `agentcore dev` + `agentcore invoke --runtime agent --local` responden
  - _Requisitos: 1_
- [ ] 2. [P] Esquema de datos (tipos_tramite, solicitudes, eventos_solicitud, aprobaciones_pendientes) + tipos "vacaciones" (ruta `[lider]`) y "certificado laboral" (ruta `[gth]`) publicados + datos ficticios
  - _Requisitos: 4, 6.1_
- [ ] 3. [P] Mock de RR. HH. con su contrato OpenAPI (colaborador, líder, aprobadores por rol o área, días disponibles, festivos de Colombia)
  - _Requisitos: 2.1, 4.1_
- [ ] 3b. Identidad simulada: usuario de prueba firmado en la sesión, del que salen el colaborador y su rol (se reemplaza por Cognito en la tarea 27); prueba de que una herramienta no puede actuar por otra persona
  - _Requisitos: 6.4, 9.2_
- [ ] 4. Pruebas del motor de rutas: ruta de un paso, aprobar cierra, rechazar cierra con comentario, la solicitud conserva la versión del tipo (rojo)
  - _Requisitos: 4.1, 4.3, 4.4, 5.2_
- [ ] 5. Implementar `siguiente_paso(config, solicitud, decision)` y el registro de eventos (verde)
  - _Requisitos: 4.1, 4.3, 4.4, 6.1_
- [ ] 6. Pruebas de reglas y radicación: días hábiles con festivos (15-26 dic = 8), días insuficientes, fechas invertidas, adjunto requerido faltante, radicado asignado, primer pendiente en la bandeja del líder (rojo)
  - _Requisitos: 1.5, 1.6, 2.1-2.3, 5.1_
- [ ] 7. Implementar API Solicitudes: radicar, consultar línea de tiempo, bandeja, aprobar/rechazar (verde); cada quien ve solo lo suyo
  - _Requisitos: 1.5, 2, 5.1, 5.2, 6.2, 6.4_
- [ ] 8. Casos de evaluación del asistente: pregunta lo que falta; muestra el resumen y radica solo tras confirmar; "¿en qué va mi solicitud?" usa la herramienta; trámite inexistente → lista los disponibles
  - _Requisitos: 1.1-1.4, 6.3_
- [ ] 9. Asistente con herramientas de alcance fijo (`dias_disponibles`, `tramites_disponibles`, `radicar_solicitud`, `estado_de_mis_solicitudes`) y el system prompt del diseño
  - Hecha cuando: los casos de la tarea 8 pasan con `agentcore dev`
  - _Requisitos: 1, 2, 6.3_
- [ ] 10. [P] Pantallas mínimas: chat con subida de adjuntos + mis solicitudes con línea de tiempo; bandeja del líder
  - _Requisitos: 1, 1.6, 5, 6.2_
- [ ] 11. `agentcore deploy` (antes: checklist de `/auditoria agentcore`) e invocar el agente desplegado con cifras reales
- [ ] 12. Auditar el bloque: `/auditoria codigo tests strands seguridad` y guardar el informe en `docs/auditorias/`

## Bloque 2 · Rutas completas, trazabilidad y correos
- [ ] 13. Pruebas: ruta líder → GTH; ruta con un área (`area:nomina`) resuelta a su aprobador; escalamiento "vacaciones > 10 días hábiles → agregar GTH" (14-31 dic = 13 hábiles) (rojo)
  - _Requisitos: 4.1, 4.2_
- [ ] 14. Implementar rutas multipaso y condiciones (verde)
  - _Requisitos: 4.1, 4.2_
- [ ] 15. Pruebas e implementación del notificador: correo al colaborador y al siguiente aprobador en cada cambio, sin adjuntos ni diagnósticos (buzón simulado en local, SES en el evento)
  - _Requisitos: 7.1, 7.2_
- [ ] 16. Línea de tiempo completa en la pantalla (hechos, actual con responsable, pendientes)
  - _Requisitos: 6.2_
- [ ] 17. Auditar el bloque: `/auditoria codigo tests`

## Bloque 3 · Incapacidades
- [ ] 18. Tipo "incapacidad" con adjunto obligatorio y ruta `[lider, gth]`
  - _Requisitos: 3, 4_
- [ ] 19. Pruebas deterministas (rojo): la vista del aprobador, el correo, los logs y la memoria de una incapacidad no contienen diagnóstico; el archivo solo lo abre el rol GTH; `radicar_solicitud` rechaza una incapacidad sin soporte validado
  - _Requisitos: 3.2, 3.3, 3.4, 5.3, 7.2, 10.1_
- [ ] 19b. Aviso de tratamiento de datos de salud y aceptación explícita antes de adjuntar el soporte (prueba + pantalla)
  - _Requisitos: 3.5_
- [ ] 20. Implementar almacenamiento cifrado (S3 + KMS) y vistas sin diagnóstico (verde)
  - _Requisitos: 3.3, 3.4, 5.3_
- [ ] 21. Herramienta `validar_soporte` con Nova 2 Lite que extrae solo fechas, entidad y firma; casos de evaluación con un soporte completo y uno incompleto (ficticios)
  - _Requisitos: 3.1, 3.2, 3.3_
- [ ] 22. Auditar el bloque: `/auditoria codigo tests seguridad`

## Bloque 4 · Trámites sin programar y seguridad
- [ ] 23. Pruebas del esquema `TramiteConfig`: configuraciones válidas e inválidas (ruta vacía, paso desconocido, condición mal formada) (rojo)
  - _Requisitos: 8.2_
- [ ] 24. Implementar el esquema y la publicación con confirmación de GTH; publicar no despliega código; modificar un trámite publica una versión nueva sin tocar las solicitudes en curso (verde)
  - _Requisitos: 8.2, 8.3, 8.4, 8.5_
- [ ] 25. Agente diseñador (Sonnet, salida estructurada) como segundo runtime del proyecto (`agentcore add runtime`) + caso de evaluación "permiso por estudio: líder y luego GTH, con certificado de la universidad"
  - _Requisitos: 8.1_
- [ ] 26. [P] Pantalla Configurador de GTH: describir → revisar propuesta → publicar
  - _Requisitos: 8_
- [ ] 27. Cognito con roles (reemplaza la identidad simulada de la tarea 3b); JWT validado en API y Runtime (AgentCore Identity)
  - _Requisitos: 9.1, 9.2_
- [ ] 27b. Verificar las trazas en AgentCore Observability y preparar la vista para la demo
- [ ] 28. Guardrail de Bedrock (diagnósticos, datos de otros, cédula enmascarada, ataques de prompt) + casos de evaluación de seguridad
  - _Requisitos: 10.1, 10.2, 10.4_
- [ ] 29. Prueba: ninguna herramienta ni agente puede aprobar o rechazar
  - _Requisitos: 10.3_
- [ ] 30. Auditar el bloque: `/auditoria seguridad agentcore strands`

## Bloque 5 · AgentCore Gateway
- [ ] 31. `agentcore add gateway` + targets OpenAPI (API Solicitudes y mock de RR. HH.); el asistente las consume por MCP (plan B: `@tool` HTTP)
- [ ] 32. Auditar el bloque: `/auditoria agentcore`

## Bloque 6 · Deseables
- [ ] 33. Tablero de GTH (ciclo promedio por tipo, pendientes por aprobador)
  - _Requisitos: 11.1_
- [ ] 34. Recordatorio a las 24 h sin respuesta
  - _Requisitos: 12.1_

## Bloque 7 · Verificación y entrega
- [ ] 35. Datos de demo y guion: vacaciones aprobadas (15-26 dic), vacaciones escaladas a GTH (14-31 dic), un rechazo con comentario, incapacidad con soporte incompleto y luego completo, trámite nuevo creado en vivo
- [ ] 36. `/auditoria agentcore seguridad` + `agentcore deploy` final
- [ ] 37. `/auditoria spec-rubrica` (guardar en `docs/auditorias/`)
- [ ] 38. `/presentacion`

## Trazabilidad (revisada criterio por criterio)
| Criterio | Tareas | | Criterio | Tareas |
|---|---|---|---|---|
| 1.1-1.4 | 8, 9 | | 5.2 | 4, 7 |
| 1.5 | 6, 7 | | 5.3 | 19, 20 |
| 1.6 | 6, 7, 10 | | 6.1 | 2, 5 |
| 2.1-2.3 | 3, 6, 7 | | 6.2 | 7, 10, 16 |
| 3.1 | 21 | | 6.3 | 8, 9 |
| 3.2 | 19, 21 | | 6.4 | 3b, 7 |
| 3.3 | 19, 20, 21 | | 7.1, 7.2 | 15, 19 |
| 3.4 | 19, 20 | | 8.1 | 25 |
| 3.5 | 19b | | 8.2-8.5 | 23, 24, 26 |
| 4.1 | 3, 4, 5, 13, 14 | | 9.1 | 27 |
| 4.2 | 13, 14 | | 9.2 | 3b, 27 |
| 4.3, 4.4 | 4, 5 | | 10.1 | 19, 28 |
| 5.1 | 6, 7 | | 10.2, 10.4 | 28 |
| | | | 10.3 | 29 |

Todos los criterios MVP tienen tarea y están en los bloques 1-4. Riesgos: Gateway con autenticación (tarea 31, con plan B) y la calidad de la lectura de soportes con imágenes ficticias (tarea 21).
