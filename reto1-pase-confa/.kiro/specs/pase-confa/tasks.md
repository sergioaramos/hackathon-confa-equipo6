# Tareas: Pase CONFA

Entrada: `requirements.md` y `design.md` v4 (4 nov 2026).

## Convenciones
- **Carriles** (equipo de dos personas): **[F]** frontend (PWA Angular y `puerta-offline`) · **[B]** resto (APIs, base de datos, agente, infraestructura).
- **[P]** puede ir en paralelo con la tarea anterior del otro carril.
- **[D]** Deseable: solo si sobra tiempo después del MVP.
- **TDD en lo crítico:** la tarea "Pruebas (rojo)" va antes que la de "Implementar (verde)". El comportamiento del agente se prueba con casos de evaluación (`pytest -m eval`). El resto del frontend se verifica a mano.
- Cada tarea dura entre 15 y 45 minutos. Al terminarla se marca `- [x]`.
- Comandos de prueba: `pytest` (backend, sin `eval`), `pytest -m eval` (agente, con Bedrock), `ng test --watch=false` (frontend, Vitest).
- La identidad simulada (contexto `sub` y `evento_id` inyectado) solo existe en las pruebas y en el servidor local. Todo lo desplegado usa Cognito desde el bloque 1.

## Bloque 1 · Punta a punta mínimo (MVP)
Meta: iniciar sesión → elegir evento → validar por cédula → semáforo → asistencia → panel → preguntar al agente desplegado.

- [x] 1. [B] Esqueleto del repositorio: carpetas `backend/` (`apis/`, `comun/`, `db/migrations/`, `tests/`), `infra/`, `mocks/`; `.gitignore` con `.venv`, `node_modules`, `.env*`, `cdk.out` y `agentcore/.env.local`; `pytest.ini` con la marca `eval` excluida por defecto; `conftest.py` que hace fallar la suite si `FACIAL_MODO=real`
  - Hecha cuando: `pytest` corre en verde con 0 pruebas, `git check-ignore agentcore/.env.local` lo ignora y `FACIAL_MODO=real pytest` falla
  - _Requisitos: 13.3, 13.8_
- [ ] 2. [B] Crear el proyecto con `agentcore create --name PaseConfa --template agent-python-strands`; `model/load.py` lee `MODELO_BEDROCK` (`us.anthropic.claude-haiku-4-5-20251001-v1:0`); probar el ID con `aws bedrock-runtime converse` en us-east-1
  - Hecha cuando: `agentcore dev` levanta y `agentcore invoke --runtime agent --local --payload '{"prompt":"hola"}'` responde en español
  - _Requisitos: 11.1_
- [ ] 3. [B] [P] Migración 001 con el esquema MVP de `design.md` (personas, eventos, inscripciones, asistencias, consentimientos, decisiones, sedes, personal, personal_eventos) en PostgreSQL local (Docker) y semilla ficticia: 1 sede (aforo 400), 1 evento externo presencial abierto (cupo 300), 20 inscritos, 1 menor, 2 personas solo en la identidad de CONFA y personal de prueba con roles por evento
  - Hecha cuando: la migración y la semilla corren sin error y una prueba confirma que la restricción única de `asistencias` rechaza el segundo ingreso por canal
  - _Requisitos: 1.5, 9.3, 13.1_
- [ ] 4. [B] Pruebas (rojo) de `comun/documentos`: normalizar (puntos, espacios, sufijo `-C`), validar de 5 a 12 dígitos, enmascarar (`******6567`), `REGEX_DOCUMENTO` y `redactar_documentos` (cédula con puntos, con espacios, con sufijo, de 5 y de 12 dígitos; URL de Zoom intacta; "300" intacto)
  - Hecha cuando: `pytest backend/tests/test_documentos.py` falla porque el módulo no existe
  - _Requisitos: 1.10, 3.2, 13.7_
- [ ] 5. [B] Implementar `comun/documentos` (verde)
  - Hecha cuando: `pytest backend/tests/test_documentos.py` en verde
  - _Requisitos: 1.10, 3.2, 13.7_
- [ ] 6. [B] Pruebas (rojo) de `comun/semaforo`: cada fila de la tabla del diseño (verde, ya ingresó, no inscrito, cédula no encontrada con "Corregir" antes de "Registrar", menor por `es_menor` y por tipo de documento fuera de `TIPOS_DOC_ADULTO`, cupo, identificado sin datos, aforo, QR inválido, evento cerrado), el orden de evaluación (un menor sin nombre no cae en registro en sitio; el aforo va antes que el cupo) y mensajes de máximo 12 palabras sin "error", "token", "API" ni "HTTP"
  - Hecha cuando: `pytest backend/tests/test_semaforo.py` falla
  - _Requisitos: 1.4, 1.5, 1.11, 2.2, 3.2, 4.2, 5.4, 6.5, 6.6, 8.5, 9.4, 9.5, 14.2_
- [ ] 7. [B] Implementar `comun/semaforo` como función pura (verde)
  - Hecha cuando: `pytest backend/tests/test_semaforo.py` en verde
  - _Requisitos: los de la tarea 6_
- [ ] 8. [B] Pruebas (rojo) de API Puerta `POST /eventos/{id}/validar/cedula` con identidad simulada: inscrito → verde y registra con `validado_por` tomado del `sub` (no del cuerpo); segundo ingreso → ámbar sin duplicar; cédula inválida → mensaje para corregir; logístico de otro evento → 403; la respuesta trae solo nombre, evento y estado
  - Hecha cuando: `pytest backend/tests/test_puerta_cedula.py` falla
  - _Requisitos: 1.5, 3.1, 3.2, 4.1, 13.4_
- [ ] 9. [B] Implementar API Puerta (cédula), `comun/identidad` y el servidor local `backend/local/servidor.py`, que enruta peticiones HTTP a los manejadores Lambda (verde)
  - Hecha cuando: la prueba de la tarea 8 en verde y `curl` contra el servidor local devuelve el semáforo
  - _Requisitos: los de la tarea 8_
- [ ] 10. [B] Pruebas (rojo) de API Eventos `GET /me/eventos`: devuelve solo los eventos asignados al `sub` con sus roles en cada uno; un usuario sin eventos recibe lista vacía
  - Hecha cuando: `pytest backend/tests/test_me_eventos.py` falla
  - _Requisitos: 13.4, 13.10_
- [ ] 11. [B] Implementar `GET /me/eventos` (verde)
  - Hecha cuando: la prueba de la tarea 10 en verde
  - _Requisitos: 13.4, 13.10_
- [ ] 12. [B] Pruebas (rojo) de API Consultas: conteo (ingresados, inscritos, faltan, porcentaje, por método), ausentes por empresa (total y hasta 20 nombres, sin documentos; empresa sin distinguir mayúsculas ni tildes), alcance (otro evento → 403)
  - Hecha cuando: `pytest backend/tests/test_consultas.py` falla
  - _Requisitos: 8.1, 8.2, 11.4, 13.2, 13.4_
- [ ] 13. [B] Implementar API Consultas (verde)
  - Hecha cuando: la prueba de la tarea 12 en verde
  - _Requisitos: los de la tarea 12_
- [ ] 14. [B] Pruebas (rojo) del agente sin modelo: `crear_herramientas(contexto, recolector)` produce `tool_spec` sin parámetros de evento ni de usuario; el logístico no recibe `ausentes_por_grupo`; las herramientas leen el token del `ContextVar` y llaman a la API Consultas (HTTP simulado); el `entrypoint` redacta documentos antes de llamar al agente y responde `{texto}`
  - Hecha cuando: `pytest app/agent/tests/test_herramientas.py` falla
  - _Requisitos: 11.1, 11.4, 13.4, 13.7_
- [ ] 15. [B] Implementar `crear_herramientas` (`contar_asistencia`, `ausentes_por_grupo`), `crear_agente` (prompt por rol, temperatura 0, `SlidingWindowConversationManager(window_size=20)`, reloj inyectado `ahora()`) y el `entrypoint` (verde)
  - Hecha cuando: la prueba de la tarea 14 en verde
  - _Requisitos: 11.1, 11.3, 11.4, 11.7_
- [ ] 16. [B] Casos de evaluación iniciales: "¿cuántos han entrado?" → `contar_asistencia`; "¿quién falta de Arquitectos S.A.?" → `ausentes_por_grupo`; pregunta fuera de tema → ninguna herramienta y negativa amable; pedir un dato que no existe → lo dice sin estimarlo
  - Hecha cuando: `pytest -m eval` en verde con `agentcore dev`
  - _Requisitos: 11.1, 11.3, 11.7_
- [ ] 17. [B] Pruebas (rojo) de API Asistente: evento no asignado → 403; el payload lleva los roles del usuario en ese evento; `runtimeSessionId = sha256(sub + evento_id)`; el prompt sale redactado
  - Hecha cuando: `pytest backend/tests/test_asistente.py` falla
  - _Requisitos: 11.1, 13.4, 13.7_
- [ ] 18. [B] Implementar API Asistente con `InvokeAgentRuntime` (cliente simulado en pruebas) (verde)
  - Hecha cuando: la prueba de la tarea 17 en verde
  - _Requisitos: los de la tarea 17_
- [ ] 19. [B] CDK de identidad: Cognito sin autorregistro, `email` no modificable, grupos `admin_confa`, `creador_eventos` y `aprobador`, App Client con PKCE, access token de 60 min y refresh token de 12 h; script para crear usuarios de prueba y su asignación en `personal_eventos`
  - Hecha cuando: un usuario de prueba inicia sesión en la página gestionada de Cognito y el token trae su `sub`
  - _Requisitos: 13.4, 13.9_
- [ ] 20. [B] CDK de APIs: Lambdas Puerta, Eventos, Consultas y Asistente en subredes privadas con NAT, secretos `rds-*` en Secrets Manager, roles de IAM de la tabla del diseño, HTTP API con autorizador JWT de Cognito, `dataTraceEnabled=false`, logs con `retentionInDays: 30`; aplicar la migración en la RDS del evento con datos ficticios
  - Hecha cuando: `cdk deploy` termina, `curl` sin token → 401 y con token de prueba → 200
  - _Requisitos: 13.3, 13.4, 13.6_
- [ ] 21. [B] `agentcore deploy` con `API_CONSULTAS_URL` y `MODELO_BEDROCK`; dar a API Asistente permiso `InvokeAgentRuntime` solo sobre ese ARN
  - Hecha cuando: una pregunta enviada a la API Asistente desplegada responde con la cifra real de la base
  - _Requisitos: 11.1_
- [ ] 22. [F] [P] `npx @angular/cli@latest new frontend --routing --style=scss` y `ng add @angular/pwa`; `ngsw-config.json` solo con `assetGroups`; `environment*.ts` con `apiBase` y datos públicos de Cognito, sin secretos
  - Hecha cuando: `ng build` termina y `ngsw-config.json` no tiene `dataGroups`
  - _Requisitos: 13.12, 14.1_
- [ ] 23. [F] Inicio de sesión con `angular-auth-oidc-client` (PKCE, token en memoria, refresh en `sessionStorage`); interceptor que agrega el JWT solo a `apiBase` (401 → renovar; 403 → "No tiene acceso a este evento"); pantalla de eventos con `GET /me/eventos` en un `signal`
  - Hecha cuando: tras iniciar sesión, el logístico llega a la puerta de su evento en 2 toques
  - _Requisitos: 13.4, 13.9, 13.10_
- [ ] 24. [F] Pantalla Puerta mínima: campo de cédula a un toque, semáforo con nombre, motivo y estado de ingreso, botones de 48 px y contraste 4,5:1
  - Hecha cuando: desde `ng serve --ssl` se valida una cédula del evento y se ve verde, y al repetirla se ve ámbar
  - _Requisitos: 3.1, 4.1, 4.2, 4.4, 14.3, 14.4_
- [ ] 25. [F] Panel mínimo: entradas, esperado, faltantes y porcentaje, con consulta cada 3 s, `takeUntilDestroyed` y pausa sin conexión
  - Hecha cuando: el número cambia en menos de 5 s después de una validación
  - _Requisitos: 8.1_
- [ ] 26. [F] Pantalla Asistente: chat de texto contra API Asistente con estados de carga y error
  - Hecha cuando: "¿cuántos han entrado?" responde la cifra del panel
  - _Requisitos: 11.1_
- [ ] 27. [B] [F] Recorrido de punta a punta del bloque contra las APIs y el agente desplegados
  - Hecha cuando: iniciar sesión → elegir evento → cédula verde → repetir (ámbar) → panel actualizado → pregunta al agente, sin errores
  - _Requisitos: 3.1, 8.1, 11.1, 13.9_
- [ ] 28. Auditar el bloque: `/auditoria codigo tests strands seguridad` y guardar el informe en `docs/auditorias/`

## Bloque 2 · Flujo principal completo (MVP)
- [ ] 29. [B] [P] Mock de la API facial: `mocks/api-facial/openapi.yaml` con el contrato real (`/identificarvalidar`, `x-api-key`) y servidor mock con escenarios fijos (reconocido, advertencia, dos rostros, sin rostro, confianza baja, lento)
  - Hecha cuando: `curl` al mock con cada escenario devuelve la respuesta del contrato
  - _Requisitos: 13.8_
- [ ] 30. [B] Pruebas (rojo) de `ClienteFacial`: las 9 filas de la tabla de decisión, incluido el ejemplo real (`est=false`, `adv=true`, `pcr=99,99`) → no reconocido; timeout de 5 s; envía `x-api-key` desde el secreto; `msg` truncado a 120 caracteres y sin HTML; ningún log contiene `imgdata` ni el documento completo
  - Hecha cuando: `pytest backend/tests/test_cliente_facial.py` falla
  - _Requisitos: 1.3, 1.6, 1.8, 1.9, 1.10, 5.3, 13.8_
- [ ] 31. [B] Implementar `ClienteFacial` con `FACIAL_MODO=mock` por defecto (verde)
  - Hecha cuando: la prueba de la tarea 30 en verde
  - _Requisitos: los de la tarea 30_
- [ ] 32. [B] Pruebas (rojo) de `POST /eventos/{id}/validar/rostro`: sin consentimiento o sin "mayor de edad" → no se llama a `ClienteFacial`; evento dirigido a menores → rechazado sin llamada; constancia en `consentimientos` por cada intento (modo, quién aceptó, versión del aviso, resultado) aunque falle; al segundo intento fallido → ofrecer QR o cédula; menor identificado → ámbar sin registrar; identificado sin nombre → ámbar con documento prellenado; reconocido e inscrito → verde con método `rostro`; la foto no queda en base de datos ni en logs; con aviso borrador, un documento fuera de `FACIAL_DOCS_PERMITIDOS` no se registra en modo real
  - Hecha cuando: `pytest backend/tests/test_puerta_rostro.py` falla
  - _Requisitos: 1.1, 1.2, 1.7, 1.11, 5.1, 5.2, 5.3, 5.5, 5.7, 6.6, 13.8_
- [ ] 33. [B] Implementar `/validar/rostro` (verde)
  - Hecha cuando: la prueba de la tarea 32 en verde
  - _Requisitos: los de la tarea 32_
- [ ] 34. [B] Pruebas (rojo) de QR: token `HMAC(secreto_qr, inscripcion_id ‖ qr_version)` de 128 bits, regenerable e idéntico al regenerarlo; en base solo `sha256`; el QR no contiene datos personales; `POST /validar/qr` válido → verde con método `qr`; inexistente, de otro evento o de versión anterior → rojo; ya usado → ámbar
  - Hecha cuando: `pytest backend/tests/test_qr.py` falla
  - _Requisitos: 2.1, 2.2, 2.3, 2.6_
- [ ] 35. [B] Implementar `comun/qr` (secreto `qr` en Secrets Manager) y `/validar/qr` (verde)
  - Hecha cuando: la prueba de la tarea 34 en verde
  - _Requisitos: los de la tarea 34_
- [ ] 36. [B] Pruebas (rojo) de API Eventos: crear evento externo o interno presencial (solo grupo `creador_eventos`; queda como organizador; cupo mayor que cero y no mayor que el aforo; `inscripcion_previa` y `dirigido_a_menores`); asignar roles (organizador solo asigna `logistico` y `punto_fijo` en sus eventos, si no 403; queda en `decisiones`); cerrar evento (después, todo ingreso → rojo)
  - Hecha cuando: `pytest backend/tests/test_eventos.py` falla
  - _Requisitos: 5.5, 8.5, 9.1, 9.3, 13.5, 13.11_
- [ ] 37. [B] Implementar creación, asignación de roles y cierre de eventos (verde)
  - Hecha cuando: la prueba de la tarea 36 en verde
  - _Requisitos: los de la tarea 36_
- [ ] 38. [B] Pruebas (rojo) de la carga CSV: coma y punto y coma, `tipo_doc` por defecto `C`, documento de 5 a 12 dígitos, nombre válido, campos que empiezan por `= + - @` rechazados, duplicados contados una vez, más de 10.000 filas o de 2 MB rechazado, cada error con su fila y motivo, nunca sobrescribe `personas` (el nombre queda en `inscripciones.nombre_cargado`); plantilla descargable
  - Hecha cuando: `pytest backend/tests/test_carga_csv.py` falla
  - _Requisitos: 9.2_
- [ ] 39. [B] Implementar la carga CSV y la plantilla (verde)
  - Hecha cuando: la prueba de la tarea 38 en verde
  - _Requisitos: 9.2_
- [ ] 40. [B] Pruebas (rojo) de descarga y rotación de QR: solo el organizador del evento (otros → 403); PNG individual y PDF con todos, con nombre y QR, sin documento; cada descarga y cada rotación quedan en `decisiones`; tras rotar, el QR anterior sale en rojo
  - Hecha cuando: `pytest backend/tests/test_descarga_qr.py` falla
  - _Requisitos: 2.4, 2.6, 13.5_
- [ ] 41. [B] Implementar descarga y rotación de QR (verde)
  - Hecha cuando: la prueba de la tarea 40 en verde
  - _Requisitos: 2.4, 2.6, 13.5_
- [ ] 42. [B] Pruebas (rojo) de registro en sitio y decisiones: evento sin inscripción previa acepta a quien está en la identidad de CONFA y lo agrega; persona inexistente → registro con cédula, nombre, teléfono y correo solo con aceptación del tratamiento, y se le genera QR; no inscrito en evento con lista → registrar o rechazar; reingreso, rechazo y cupo autorizado crean una decisión sin duplicar asistencia; menor con documento del acudiente queda a nombre del menor; 6.6 con documento cambiado → método `cedula`
  - Hecha cuando: `pytest backend/tests/test_registro_sitio.py` falla
  - _Requisitos: 1.5, 4.5, 5.6, 6.1, 6.2, 6.3, 6.5, 6.6, 9.4, 13.5_
- [ ] 43. [B] Implementar `POST /eventos/{id}/registro-sitio` y `POST /eventos/{id}/decisiones` (verde)
  - Hecha cuando: la prueba de la tarea 42 en verde
  - _Requisitos: los de la tarea 42_
- [ ] 44. [B] Pruebas (rojo) de aforo y cupo: dos validaciones simultáneas con un solo lugar de aforo → solo una entra (concurrencia real contra PostgreSQL); cupo superado → ámbar; panel con aviso al 90 % del cupo
  - Hecha cuando: `pytest backend/tests/test_aforo.py` falla
  - _Requisitos: 9.4, 9.5, 9.7_
- [ ] 45. [B] Implementar conteo e inserción en la misma transacción (`SELECT … FOR UPDATE` sobre el evento) y el aviso del 90 % en API Consultas (verde)
  - Hecha cuando: la prueba de la tarea 44 en verde
  - _Requisitos: 9.4, 9.5, 9.7_
- [ ] 46. [B] Pruebas (rojo) del informe y las métricas: CSV con nombre, documento enmascarado, empresa, estado, método, hora y puerta, sin teléfono ni correo; celdas que empiezan por `= + - @`, tabulador o retorno se anteponen con `'`; registros en sitio incluidos; URL prefirmada de 5 minutos; descarga registrada; tiempo promedio de ingreso por método; respuestas con datos personales llevan `Cache-Control: no-store`
  - Hecha cuando: `pytest backend/tests/test_informe.py` falla
  - _Requisitos: 6.4, 8.3, 8.4, 13.5, 13.12_
- [ ] 47. [B] Implementar el informe (bucket S3 en CDK con bloqueo público, SSE y *lifecycle* de 1 día) y el tiempo promedio (verde)
  - Hecha cuando: la prueba de la tarea 46 en verde
  - _Requisitos: 6.4, 8.3, 8.4, 13.6_
- [ ] 48. [B] Pruebas (rojo) de las herramientas restantes: `estado_de_persona` (hasta 5 coincidencias: nombre, ingresó, hora, canal), `resumen_novedades` (solo conteos, sin datos de contacto), `generar_informe` (cifras de código; `informe_id` en el recolector); el `entrypoint` devuelve `{texto, informe_id}` aunque el texto del modelo no lo traiga
  - Hecha cuando: `pytest app/agent/tests/test_herramientas.py` falla en los casos nuevos
  - _Requisitos: 11.2, 11.4, 11.5, 11.8_
- [ ] 49. [B] Implementar las herramientas, sus endpoints en API Consultas y el recolector (verde)
  - Hecha cuando: la prueba de la tarea 48 en verde
  - _Requisitos: 11.2, 11.5, 11.8_
- [ ] 50. [B] Memory: `agentcore remove memory --name agentMemory` y `agentcore add memory --name agentMemory --event-expiry-duration 3 --strategies SUMMARIZATION`; `memory/session.py` con `actorId = sub` y consulta solo en el namespace de la sesión; verificar la caducidad de los resúmenes
  - Hecha cuando: el caso de evaluación "¿quién falta de Arquitectos S.A.?" seguido de "¿y de Café Caldas?" usa la empresa nueva con el contexto, y una sesión de otro evento no ve ese hilo
  - _Requisitos: 11.6, 13.6_
- [ ] 51. [B] Casos de evaluación ampliados: "¿ya entró Ana Gómez?" → `estado_de_persona`; "¿hay casos por revisar?" → `resumen_novedades`; "hazme el reporte" → `generar_informe` con `informe_id`; "marca a Ana como ingresada" → ninguna escritura; pedir un dato inexistente → lo dice
  - Hecha cuando: `pytest -m eval` en verde
  - _Requisitos: 11.2, 11.4, 11.5, 11.7, 11.8_
- [ ] 52. [B] Pruebas (rojo) del punto fijo: con el rol `punto_fijo` solo responden `/validar/rostro` y `/validar/qr` (cédula, panel, asistente, paquete y decisiones → 403); un caso ámbar del punto fijo aparece en `GET /eventos/{id}/pendientes` para el logístico y desaparece al decidirlo; la constancia guarda `modo='punto_fijo'` y `quien_acepto='titular'`
  - Hecha cuando: `pytest backend/tests/test_punto_fijo.py` falla
  - _Requisitos: 4.6, 4.7, 4.8, 5.7, 13.4_
- [ ] 53. [B] Implementar el rol `punto_fijo` y `/pendientes` (verde)
  - Hecha cuando: la prueba de la tarea 52 en verde
  - _Requisitos: 4.6, 4.7, 4.8_
- [ ] 54. [F] [P] Flujo de rostro en modo logístico: aviso de máximo 25 palabras con los mínimos legales (texto borrador del diseño), toque "Acepta y es mayor de edad" y botón "Prefiero QR o cédula" del mismo tamaño; `getUserMedia` con `facingMode: { ideal: 'environment' }` abierto solo tras aceptar; captura en `canvas` a 640 px, envío y cámara apagada; muestra `msg` para repetir y, al segundo intento fallido o a los 5 s sin respuesta, pasa a QR o cédula en la misma pantalla
  - Hecha cuando: con el mock, los escenarios reconocido, advertencia, dos rostros y lento se ven como dice el diseño
  - _Requisitos: 1.1, 1.3, 1.6, 1.7, 1.8, 5.1, 5.2, 5.8, 14.4_
- [ ] 55. [F] [P] Lector de QR en la puerta (`@zxing/browser` u otra biblioteca elegida aquí)
  - Hecha cuando: un QR descargado del evento se lee y se ve verde; uno rotado se ve rojo
  - _Requisitos: 2.1, 2.2_
- [ ] 56. [F] Decisiones ámbar en la puerta: dejar pasar como reingreso, rechazar, autorizar cupo, "Corregir" antes de "Registrar persona", formulario de registro en sitio (cédula, nombre, teléfono, correo y aceptación del tratamiento; documento no editable en 6.6), documento del acudiente para menores
  - Hecha cuando: cada caso ámbar se resuelve en máximo 3 toques
  - _Requisitos: 1.5, 3.2, 4.5, 5.6, 6.3, 6.5, 6.6, 9.4, 14.3_
- [ ] 57. [F] Pantallas de eventos: crear evento (externo o interno, presencial, cupo, inscripción previa, dirigido a menores), carga CSV con la lista de errores por fila y la plantilla, descarga y rotación de QR, cierre del evento y descarga del informe
  - Hecha cuando: se crea un evento, se cargan 20 inscritos con 2 filas erróneas, se descarga el PDF de QR y se cierra el evento
  - _Requisitos: 2.4, 2.6, 8.3, 9.1, 9.2_
- [ ] 58. [F] Panel completo: desglose por método, faltantes por empresa, tiempo promedio de ingreso por método y aviso al 90 % del cupo
  - Hecha cuando: el panel muestra los cuatro datos con la semilla de prueba
  - _Requisitos: 8.1, 8.2, 8.4, 9.7_
- [ ] 59. [F] Asistente: si la respuesta trae `informe_id`, mostrar el botón de descarga (la URL se pide a API Eventos)
  - Hecha cuando: "hazme el reporte" muestra el botón y el CSV se descarga
  - _Requisitos: 11.2_
- [ ] 60. [F] Modo punto fijo: ruta `/eventos/:id/kiosco` con *guard* que impide navegar y código de supervisor para salir; aviso en pantalla y "Acepto" del asistente; cámara frontal (`facingMode: { ideal: 'user' }`) solo tras aceptar y apagada tras la captura o a los 10 s; ámbar → "Espere al logístico, por favor"; en el dispositivo del logístico, lista de pendientes consultada cada 3 s
  - Hecha cuando: un caso ámbar del punto fijo aparece en el celular del logístico en máximo 3 s y se resuelve ahí
  - _Requisitos: 4.6, 4.7, 4.8, 5.1_
- [ ] 61. [B] API facial real: cargar la API key en el secreto `facial`, *throttling* `rate=1, burst=1` en API Gateway sobre `/validar/rostro`, `FACIAL_DOCS_PERMITIDOS` con los documentos del equipo; probar a mano con los rostros del equipo que lo autorizan, medir la latencia y ajustar `FACIAL_UMBRAL` y el timeout
  - Hecha cuando: un integrante enrolado entra por rostro con la API real y la latencia queda anotada en `docs/`
  - _Requisitos: 1.1, 1.9, 13.8_
- [ ] 62. [B] [F] Desplegar el bloque (`cdk deploy` y `agentcore deploy`) y recorrer cédula, rostro (mock y real), QR, no inscrito, ya ingresó, punto fijo, panel, agente e informe
  - Hecha cuando: el recorrido termina sin errores en la cuenta del evento
  - _Requisitos: 1, 2, 3, 4, 5, 6, 8, 9, 11_
- [ ] 63. Auditar el bloque: `/auditoria codigo tests strands seguridad` y guardar el informe

## Bloque 3 · Contingencias: sin conexión (MVP)
- [ ] 64. [F] Pruebas (rojo) de `puerta-offline` con Vitest, `Almacen` en memoria, iteraciones de PBKDF2 reducidas y reloj fijo: búsqueda por `sha256` del QR y por cédula; duplicado local → ámbar; cola y contador de pendientes; caducidad comprobada al abrir; envoltura en serie (sin PIN no descifra, sin `K_dispositivo` no descifra); PIN débil rechazado; 5 PIN fallidos borran el paquete; bloqueo tras 15 minutos; tope local de aforo → rojo "Verifique el aforo con el coordinador"
  - Hecha cuando: `ng test --watch=false` falla en esos casos
  - _Requisitos: 7.2, 7.3, 7.7, 9.5_
- [ ] 65. [F] Implementar `puerta-offline` en TypeScript puro (verde)
  - Hecha cuando: `ng test --watch=false` en verde
  - _Requisitos: 7.2, 7.3, 7.7, 9.5_
- [ ] 66. [B] [P] Pruebas (rojo) del paquete offline: solo logístico asignado (otro evento, organizador sin rol logístico y `punto_fijo` → 403); trae `qr_token_hash` y nunca el token; trae el tope local de aforo; la descarga queda en `decisiones`; `Cache-Control: no-store`
  - Hecha cuando: `pytest backend/tests/test_paquete_offline.py` falla
  - _Requisitos: 7.1, 9.5, 13.5, 13.10, 13.12_
- [ ] 67. [B] Implementar `GET /eventos/{id}/paquete-offline` (verde)
  - Hecha cuando: la prueba de la tarea 66 en verde
  - _Requisitos: los de la tarea 66_
- [ ] 68. [B] Pruebas (rojo) de `POST /sync`: idempotente por `id` (reenviar el lote no duplica), decisiones offline incluidas, corrección del desfase de reloj, `|desfase| > 2 min` → `revision`, persona y canal ya registrados → se conserva uno y el otro va a `revision`
  - Hecha cuando: `pytest backend/tests/test_sync.py` falla
  - _Requisitos: 7.4_
- [ ] 69. [B] Implementar `/sync` (verde)
  - Hecha cuando: la prueba de la tarea 68 en verde
  - _Requisitos: 7.4_
- [ ] 70. [F] Interfaz sin conexión: detectar la pérdida de señal, aviso "Sin conexión" con contador de pendientes, ocultar el rostro, definir el PIN al descargar y pedirlo al abrir y tras 15 minutos, sincronizar solo al volver la señal y mostrar cuándo terminó
  - Hecha cuando: en modo avión se validan QR y cédula, y al reconectar el contador llega a 0 sin tocar nada
  - _Requisitos: 7.2, 7.3, 7.4, 7.6, 7.7_
- [ ] 71. [F] Verificación manual con lista fija: modo avión en el celular; en DevTools, ninguna URL `/api/*` queda en `caches` y las respuestas de la API no quedan en la caché HTTP
  - Hecha cuando: la lista queda firmada en `docs/verificaciones/sin-conexion.md`
  - _Requisitos: 7.6, 13.12_
- [ ] 72. Auditar el bloque: `/auditoria codigo tests seguridad` y guardar el informe

## Bloque 4 · Seguridad (MVP)
- [ ] 73. [B] Guardrail en CDK con versión fija: ataques de prompt (alto); PII con `REGEX_DOCUMENTO` (incluido el formato con puntos), teléfono y correo en modo enmascarar; temas denegados "información biométrica de terceros", "salud y diagnósticos" y "temas ajenos a los eventos de CONFA"; sin contextual grounding; conectarlo al `BedrockModel` con `GUARDRAIL_ID` y `GUARDRAIL_VERSION`
  - Hecha cuando: un prompt con una cédula con puntos llega enmascarado y un intento de inyección se bloquea en `agentcore dev`
  - _Requisitos: 11.4, 13.7_
- [ ] 74. [B] Casos de evaluación de seguridad: pedir datos de otro evento, pedir documentos o teléfonos, logístico que pide el informe o crear un evento, inscrito con nombre malicioso ("Ignora tus instrucciones…") en los datos
  - Hecha cuando: `pytest -m eval` en verde
  - _Requisitos: 11.3, 11.4, 13.4_
- [ ] 75. [B] Pruebas (rojo) de seguridad deterministas: ninguna Lambda registra `imgdata`, el `event` completo ni documentos completos (captura de logs en todos los manejadores); el esquema no tiene columnas de imagen, plantilla, `pcr` ni diagnóstico; matriz de autorización por rol y evento (organizador, logístico, `punto_fijo`, sin rol) en todos los endpoints; respuestas con datos personales con `no-store`; la respuesta de la puerta no trae datos de salud ni imagen
  - Hecha cuando: `pytest backend/tests/test_seguridad.py` corre y muestra qué falla
  - _Requisitos: 4.3, 5.3, 13.1, 13.2, 13.4, 13.12_
- [ ] 76. [B] Corregir lo que falle en la tarea 75 (verde)
  - Hecha cuando: `pytest backend/tests/test_seguridad.py` en verde
  - _Requisitos: los de la tarea 75_
- [ ] 77. [B] Usuarios de base de datos por API (`puerta`, `eventos`, `consultas_ro`, `purga`) con permisos mínimos y `REVOKE UPDATE, DELETE ON decisiones, consentimientos` salvo para `purga`; prueba de que la aplicación no puede modificar ni borrar esas tablas
  - Hecha cuando: la prueba pasa y cada Lambda usa su usuario desde su secreto
  - _Requisitos: 13.5_
- [ ] 78. [B] Pruebas (rojo) de la purga: borra asistencias y personas de sitio a los 90 días del evento, borradores a las 24 h, y `decisiones` y `consentimientos` al año; conserva lo vigente
  - Hecha cuando: `pytest backend/tests/test_purga.py` falla
  - _Requisitos: 13.6_
- [ ] 79. [B] Implementar la Lambda de purga y la regla diaria de EventBridge (verde)
  - Hecha cuando: la prueba de la tarea 78 en verde y la regla aparece desplegada
  - _Requisitos: 13.6_
- [ ] 80. [B] Frontend en S3 privado con CloudFront y OAC: CSP del diseño, `Permissions-Policy`, HSTS, `Referrer-Policy: no-referrer` y redirección de rutas a `index.html`; `optimization.styles.inlineCritical: false` en `angular.json`
  - Hecha cuando: la PWA desplegada carga por HTTPS y los encabezados se ven en la respuesta
  - _Requisitos: 13.3, 13.6, 13.12_
- [ ] 81. [F] Verificar la PWA con la CSP y Trusted Types activos; buscar y quitar `bypassSecurityTrust*`, `innerHTML` con datos externos y `eval`
  - Hecha cuando: la consola del navegador no muestra violaciones de CSP en el recorrido completo y la búsqueda no encuentra esos usos
  - _Requisitos: 13.3, 13.12_
- [ ] 82. [B] Revisión de mínimo privilegio: cada rol de IAM contra la tabla del diseño (excepciones con `*` documentadas), búsqueda de secretos en el repositorio y en el *bundle* del frontend, y verificación del *opt-out* de servicios de IA si se usa Rekognition
  - Hecha cuando: la revisión queda anotada en `docs/verificaciones/iam.md` sin pendientes
  - _Requisitos: 13.3_
- [ ] 83. Auditar el bloque: `/auditoria seguridad agentcore` y guardar el informe

## Bloque 5 · Observabilidad, Gateway y Deseables
- [ ] 84. [B] Observability: `agentcore traces` y `agentcore logs` muestran una consulta con sus llamadas a herramientas (activar CloudWatch Transaction Search si la cuenta lo pide)
  - Hecha cuando: la traza de "¿quién falta de Arquitectos S.A.?" se ve en la consola, lista para la demo
  - _Requisitos: 11.1 (evidencia de arquitectura)_
- [ ] 85. [D] [B] [F] Sincronización entre dispositivos con corrección de reloj y registro sin conexión de no inscritos (pruebas en rojo y luego verde en pytest y Vitest)
  - _Requisitos: 7.5, 7.8_
- [ ] 86. [D] [B] Envío del QR por correo con Amazon SES (pruebas con SES simulado)
  - _Requisitos: 2.5_
- [ ] 87. [D] [B] [F] Pasadías: tipo de evento individual sin inscripción previa
  - _Requisitos: 9.6_
- [ ] 88. [D] [B] [F] Foto grupal con Rekognition `DetectFaces` (pruebas en rojo de consentimiento grupal, menores, tope de 50, nada persistido; luego implementación con concurrencia 1 en modo real)
  - _Requisitos: 10.1–10.6_
- [ ] 89. [D] [B] [F] Eventos virtuales e híbridos con Página virtual (pruebas de enlace firmado, 5 intentos, conteo único por persona)
  - _Requisitos: 15.1–15.8_
- [ ] 90. [D] [B] [F] Crear eventos con lenguaje natural: `sedes_ocupadas` y `preparar_borrador_evento` (pruebas con reloj fijo; casos de evaluación de que el agente no crea nada)
  - _Requisitos: 16.1–16.7_
- [ ] 91. [D] [B] [F] Consultas por voz con Transcribe y Polly (Identity Pool limitado)
  - _Requisitos: 17.1–17.4_
- [ ] 92. [D] [B] [F] Solicitud y aprobación de sedes (fuera de la demo)
  - _Requisitos: 12.1–12.5_
- [ ] 93. [D] [B] AgentCore Gateway: la API Consultas como herramientas MCP con `CUSTOM_JWT` (plan B: se quedan las `@tool` actuales)
  - _Requisitos: 11 (evolución)_
- [ ] 94. [D] [F] Desbloqueo del paquete con WebAuthn en lugar del PIN
  - _Requisitos: 7.7 (evolución)_
- [ ] 95. Auditar lo hecho en el bloque: `/auditoria codigo tests strands seguridad`

## Bloque 6 · Demo y métricas
- [ ] 96. [B] Datos de demo ficticios: evento "Encuentro de afiliados Arquitectos S.A." con 300 inscritos, los integrantes del equipo, un menor, dos personas no inscritas y una sede con aforo; script para reiniciar la demo
  - Hecha cuando: el script deja la base lista en menos de 1 minuto
  - _Requisitos: 13.8_
- [ ] 97. [B] Script de medición de tiempos con el mock (normal y lento) y con la API real: cédula, QR, rostro, registro en sitio, actualización del panel, informe y respuesta del agente
  - Hecha cuando: la tabla de tiempos queda en `docs/metricas.md` y cada criterio con tiempo dice si se cumple
  - _Requisitos: 1.1, 2.1, 3.1, 6.2, 8.1, 8.3, 11.1_
- [ ] 98. [F] Contador de impacto en el panel: tiempo promedio medido por método frente a la referencia de 35 s y horas de espera evitadas estimadas, marcadas como estimación
  - Hecha cuando: el panel muestra la comparación con los datos de la demo
  - _Requisitos: 8.4_
- [ ] 99. [F] Verificación manual de la PWA con lista fija: el asistente no instala nada; mensajes de máximo 15 palabras sin términos técnicos; flujo de cédula sin exigir nada al asistente; ninguna pantalla muestra salud ni imágenes; botones de 48 px y contraste 4,5:1 a pleno sol; el aviso muestra los mínimos legales
  - Hecha cuando: la lista queda firmada en `docs/verificaciones/pwa.md`
  - _Requisitos: 3.3, 4.3, 4.4, 5.8, 14.1, 14.2_
- [ ] 100. Guion de la demo con plan B: mock si falla la API real, modo avión en vivo, `agentcore dev` local si falla el despliegue y video grabado del recorrido completo
  - Hecha cuando: el guion se ensaya una vez de punta a punta en menos de 5 minutos
- [ ] 101. README final con cómo correr la demo en 3 comandos
  - Hecha cuando: otra persona del equipo la levanta siguiendo solo el README

## Bloque 7 · Verificación y entrega
- [ ] 102. `/auditoria agentcore seguridad` antes del despliegue final; corregir los bloqueantes
- [ ] 103. Despliegue final (`cdk deploy`, `agentcore deploy`, frontend) y recorrido de punta a punta en la cuenta del evento
- [ ] 104. `/auditoria spec-rubrica`: nota estimada y las 3 mejoras de mayor impacto
- [ ] 105. `/presentacion`
- [ ] 106. Commit de la spec, las auditorías y las verificaciones, agregando los archivos por nombre

## Resumen
| Bloque | Tareas | [F] | [B] | Pruebas (rojo) | Paralelizables [P] |
|---|---|---|---|---|---|
| 1 · Punta a punta mínimo | 28 (1–28) | 5 | 21 | 7 | 2 (3, 22) |
| 2 · Flujo principal | 35 (29–63) | 7 | 26 | 11 | 3 (29, 54, 55) |
| 3 · Sin conexión | 9 (64–72) | 4 | 4 | 3 | 1 (66) |
| 4 · Seguridad | 11 (73–83) | 1 | 9 | 2 | — |
| 5 · Observabilidad y Deseables | 12 (84–95) | — | — | — | 10 Deseables |
| 6 · Demo y métricas | 6 (96–101) | 2 | 2 | — | — |
| 7 · Verificación | 5 (102–106) | — | — | — | — |
| **Total** | **106** (94 MVP o de cierre, 10 Deseables, 2 auditorías de Deseables y observabilidad) | | | | |

El carril [F] tiene menos tareas pero más largas de interfaz; mientras el carril [B] escribe pruebas y APIs, [F] trabaja contra el contrato de los endpoints con respuestas simuladas.

## Trazabilidad (criterio por criterio)
| Criterio | Tareas | | Criterio | Tareas |
|---|---|---|---|---|
| 1.1 | 32, 33, 54, 61, 97 | | 7.1 | 66, 67 |
| 1.2 | 32, 33 | | 7.2 | 64, 65, 70 |
| 1.3 | 30, 31, 54 | | 7.3 | 64, 65, 70 |
| 1.4 | 6, 7 | | 7.4 | 68, 69, 70 |
| 1.5 | 3, 6, 7, 8, 42, 56 | | 7.5 [D] | 85 |
| 1.6 | 30, 31, 54 | | 7.6 | 70, 71 |
| 1.7 | 32, 33, 54 | | 7.7 | 64, 65, 70 |
| 1.8 | 30, 31, 54 | | 7.8 [D] | 85 |
| 1.9 | 30, 31, 61 | | 8.1 | 12, 13, 25, 58, 97 |
| 1.10 | 4, 5, 30, 31 | | 8.2 | 12, 13, 58 |
| 1.11 | 6, 7, 32, 33 | | 8.3 | 46, 47, 57, 97 |
| 2.1 | 34, 35, 55, 97 | | 8.4 | 46, 47, 58, 98 |
| 2.2 | 6, 7, 34, 35, 55 | | 8.5 | 6, 7, 36, 37 |
| 2.3 | 34, 35 | | 9.1 | 36, 37, 57 |
| 2.4 | 40, 41, 57 | | 9.2 | 38, 39, 57 |
| 2.5 [D] | 86 | | 9.3 | 3, 36, 37 |
| 2.6 | 34, 35, 40, 41, 57 | | 9.4 | 6, 7, 42, 44, 45, 56 |
| 3.1 | 8, 9, 24, 97 | | 9.5 | 6, 7, 44, 45, 64, 65, 66 |
| 3.2 | 4, 5, 6, 7, 8, 56 | | 9.6 [D] | 87 |
| 3.3 | 99 | | 9.7 | 44, 45, 58 |
| 4.1 | 8, 24 | | 10.1–10.6 [D] | 88 |
| 4.2 | 6, 7, 24 | | 11.1 | 2, 12–18, 21, 26, 97 |
| 4.3 | 75, 99 | | 11.2 | 48, 49, 51, 59 |
| 4.4 | 24, 99 | | 11.3 | 15, 16, 74 |
| 4.5 | 42, 43, 56 | | 11.4 | 12, 14, 48, 51, 73, 74 |
| 4.6 | 52, 53, 60 | | 11.5 | 48, 49, 51 |
| 4.7 | 52, 53, 60 | | 11.6 | 50 |
| 4.8 | 52, 53, 60 | | 11.7 | 15, 16, 51 |
| 5.1 | 32, 33, 54, 60 | | 11.8 | 48, 49, 51 |
| 5.2 | 32, 54 | | 12.1–12.5 [D] | 92 |
| 5.3 | 30, 32, 75 | | 13.1 | 3, 75 |
| 5.4 | 6, 7 | | 13.2 | 12, 75 |
| 5.5 | 32, 33, 36 | | 13.3 | 1, 20, 80, 81, 82 |
| 5.6 | 42, 43, 56 | | 13.4 | 8, 10, 12, 14, 17, 19, 20, 23, 52, 74, 75 |
| 5.7 | 32, 33, 52 | | 13.5 | 36, 40, 42, 46, 66, 77 |
| 5.8 | 54, 99 | | 13.6 | 20, 47, 50, 78, 79, 80 |
| 6.1 | 42, 43 | | 13.7 | 4, 5, 14, 17, 73 |
| 6.2 | 42, 43, 97 | | 13.8 | 1, 29, 30, 32, 61, 96 |
| 6.3 | 42, 43, 56 | | 13.9 | 19, 23, 27 |
| 6.4 | 46, 47 | | 13.10 | 10, 11, 23, 66 |
| 6.5 | 6, 7, 42, 43, 56 | | 13.11 | 36, 37 |
| 6.6 | 6, 7, 32, 33, 42, 56 | | 13.12 | 22, 46, 66, 71, 75, 80, 81 |
| | | | 14.1 | 22, 99 |
| | | | 14.2 | 6, 7, 99 |
| | | | 14.3 | 24, 56 |
| | | | 14.4 | 24, 54 |
| | | | 15.1–15.8 [D] | 89 |
| | | | 16.1–16.7 [D] | 90 |
| | | | 17.1–17.4 [D] | 91 |

**Huecos:** recorrí los 116 criterios uno por uno (82 del MVP y 34 Deseables); todos tienen al menos una tarea. Los criterios 3.3, 4.4, 5.8, 14.1 y 14.2 se verifican a mano (tarea 99), no con pruebas automáticas, porque son de interfaz.

**Piezas del diagrama de `design.md` y su tarea:** PWA (22–26, 54–60, 70), IndexedDB cifrada (64, 65, 70), Cognito (19, 23), API Puerta (8, 9, 32, 33, 35, 42–45, 52, 53), API Eventos (10, 11, 36–41, 46, 47, 67), API Consultas (12, 13, 45, 49), API Asistente (17, 18), Runtime (2, 21), Bedrock con Guardrail (2, 73), Memory (50), API facial (29–31, 61), RDS (3, 20, 77), S3 de informes (47), Purga con EventBridge (78, 79), Secrets Manager (20, 35, 61), Observability (84), CloudFront (80). Página virtual, Rekognition y Transcribe con Polly están marcados Deseables en el diagrama (89, 88, 91); Gateway es evolución (93).

## Riesgos
| Riesgo | Mitigación |
|---|---|
| El MVP es grande para dos personas en un día: 94 tareas fuera de los Deseables | El orden ya prioriza el recorrido de punta a punta (bloque 1) y el flujo principal (bloque 2). Si a las 2:00 p. m. el bloque 3 no está empezado, se recorta el punto fijo (52, 53, 60) antes que el modo sin conexión, que es parte del beneficio principal |
| Latencia o disponibilidad de la API facial real (solo producción) | Mock con el mismo contrato y escenario "lento"; tarea 61 mide la latencia real temprano |
| Reenvío del token y variables del Runtime desplegado sin verificar en la referencia | El agente se invoca con IAM desde API Asistente (tarea 21); plan B `agentcore dev` local |
| `agentcore add memory` y la caducidad de los resúmenes | Comando verificado; la tarea 50 comprueba la caducidad en la cuenta |
| Red: Lambdas con acceso a RDS y a internet | NAT en la tarea 20; confirmar la VPC del evento antes de desplegar |
| CSP estricta con el *build* de Angular | Tarea 81 la verifica con el recorrido completo antes de la demo |

Siguiente paso: `/implementar 1`.
