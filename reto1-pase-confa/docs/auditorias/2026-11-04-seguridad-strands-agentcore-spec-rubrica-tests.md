# Auditoría: seguridad · strands · agentcore · spec-rubrica · tests
Alcance: spec (sin código) — `docs/working-backwards.md`, `.kiro/specs/pase-confa/requirements.md`, `.kiro/specs/pase-confa/design.md` v2 · 4 nov 2026 · tres subagentes `auditor` en paralelo.

## Veredictos
| Lente | Veredicto sobre design v2 |
|---|---|
| seguridad | LISTO CON AJUSTES |
| strands + agentcore | LISTO CON AJUSTES |
| spec-rubrica + tests | NO LISTO (nota estimada 50/100 hoy; 84 proyectada) |

## Hallazgos y qué se hizo
| # | Lente | Severidad | Hallazgo | Resolución (design v3 / requirements) |
|---|---|---|---|---|
| S1 | seguridad | 🔴 | Foto grupal sin consentimiento de cada titular | 10.1, 10.4–10.6: solo eventos con inscripción previa, consentimiento grupal en la inscripción, descarte de quien no lo dio, aviso para salir del encuadre |
| S2 | seguridad | 🔴 | Rostro de menores procesado antes de saber la edad | 5.1 toque "Acepta y es mayor de edad"; 5.5 también bloquea foto grupal; 1.11 queda como segunda barrera |
| S3 | seguridad | 🟠 | Consentimiento no demostrable | 5.7 y tabla `consentimientos` por intento, sin imagen; aviso leído en voz alta |
| S4 | seguridad | 🟠 | Paquete offline descifrable por cualquier script | 7.7: clave envuelta con PIN (PBKDF2), caducidad al abrir, borrado tras 5 PIN, CSP; riesgo residual declarado |
| S5 | seguridad | 🟠 | Memoria guarda de más y sin `actorId` | Memory de corto plazo, `actorId = sub`, `sessionId` por usuario y evento; URL del CSV fuera del modelo |
| S6 | seguridad | 🟠 | Regex de cédula no ve puntos ni espacios | `redactar_documentos` con normalización y `REGEX_DOCUMENTO` única; pruebas TDD |
| S7 | seguridad | 🟠 | Mínimo privilegio incompleto; "nadie con `*`" falso | Tabla IAM por componente con excepciones justificadas; usuarios de BD por API; Identity Pool para voz |
| S8 | seguridad | 🟠 | Imagen podría caer en logs; retención sin mecanismo | `dataTraceEnabled=false`, manejador sin `event`, `retentionInDays: 30`, Lambda de purga, bucket S3 con lifecycle |
| S9 | seguridad | 🟠 | Guardrail con huecos | Temas denegados de salud y fuera de tema; versión fija; sin grounding; validación del nombre |
| S10 | seguridad | 🟠 | Trazabilidad incompleta | `REVOKE UPDATE, DELETE`; decisiones offline en la cola; descarga de paquete y exportación registradas; `version_aviso`, `capturado_por` |
| S11 | seguridad | 🟡 | QR y enlace virtual filtrables | QR con token aleatorio y hash; enlace en fragmento, cookie HttpOnly, `Referrer-Policy`, límites por token |
| S12 | seguridad | 🟡 | Redacción de privacidad imprecisa | 13.1 reescrito con la lista real; opt-out de Rekognition [verificar]; responsable y encargado |
| A1 | agentcore | 🔴 | Autenticación al Runtime sin plan B real | API Asistente (Cognito) → `InvokeAgentRuntime` con IAM como camino principal; `CUSTOM_JWT` Deseable |
| A2 | strands | 🔴 | IDs y URLs dentro del texto del modelo | Recolector por invocación; `entrypoint` responde `{texto, borrador_id?, informe_id?}` |
| A3 | strands | 🟠 | `EventoPropuesto` obligatorio impide 16.3 | Parámetros planos y opcionales; `None` → `errores` |
| A4 | strands | 🟠 | Regex rompe URLs | Se apartan las URL antes de redactar |
| A5 | agentcore | 🟠 | Memory sin `actorId` y mezcla de eventos | Ver S5 |
| A6 | strands | 🟠 | Token capturado al construir el agente | Caché por sesión, rol y evento; token en `ContextVar`; prompt por rol |
| A7 | agentcore | 🟠 | IAM de modelos y Nova Micro sin dueño | ID fijo en `MODELO_BEDROCK`; `InvokeModelWithResponseStream`; Nova Micro eliminada |
| A8 | agentcore | 🟠 | Grounding con bloqueos falsos | Eliminado |
| A9 | strands | 🟠 | Latencia sin plan | `ausentes_por_grupo` devuelve 20 nombres; concurrencia aprovisionada; script de medición |
| A10 | strands | 🟠 | Toda la parte agéntica es Deseable | **Pendiente de decisión del equipo** (ver abajo) |
| A11 | agentcore | 🟡 | Falta sección de despliegue | Sección "Despliegue" agregada |
| A12 | agentcore | 🟡 | Observability y retención de trazas | Declarado; `agentcore traces` a ensayar |
| R1 | spec-rubrica | 🔴 | MVP sin agente | **Pendiente de decisión del equipo** |
| R2 | spec-rubrica | 🔴 | Alcance MVP no cabe en el tiempo | **Pendiente de decisión del equipo** |
| R3 | spec-rubrica | 🔴 | Consentimiento contradictorio | Ver S1–S3; tiempo facial único de 4–5 s en todos los documentos |
| R4 | spec-rubrica | 🟠 | Semáforo contradice 4.2, 3.2, 9.4 | "Ya ingresó" en ámbar con reingreso; "Corregir" antes de "Registrar"; 9.4 reescrito; 8.5 evento cerrado |
| R5 | spec-rubrica | 🟠 | Impacto: "miles de horas" mal calculado, tiempos inconsistentes | Frase corregida; 75 % marcado como techo; tiempo facial único. **Modelo de cola y valor anual en pesos: pendiente** |
| R6 | tests | 🟠 | Regla del "primero" offline contradictoria; lógica de cliente sin pruebas | Corrección por desfase de reloj; módulo `puerta-offline` con vitest |
| R7 | spec-rubrica | 🟠 | Trazabilidad incompleta | Componentes con requisitos completos; 11.5–11.7 justifican herramientas y Memory; `ritmo_ingreso` eliminado |
| R8 | spec-rubrica | 🟠 | Huecos frente al reto | 13.9 acceso rápido; 5.6 menores; preescolar → 6.3; video fuera de alcance |
| R9 | spec-rubrica | 🟠 | WB promete voz | "su voz" quitado del beneficio; `producto.md` alineado |
| R10 | tests | 🟠 | Criterios críticos sin prueba | Tabla de pruebas ampliada (3.2, 6.1–6.3, 9.2, 13.4, 15.3, 15.8, `tool_spec`, purga, tiempos) |
| R11 | spec-rubrica | 🟡 | EARS no verificables o redundantes | 3.3, 6.4, 13.1, 13.3, 13.6, 14.2 reescritos; 2.4 solo presencial o híbrido |
| R12 | tests | 🟡 | Fecha fija y regex inconsistentes | Reloj inyectado `ahora()`; `REGEX_DOCUMENTO` única |

## Decisiones del equipo (4 nov)
1. Requisito 11 (consultas por texto) sube a MVP → resuelve A10 y R1.
2. Virtual e híbrido (15), foto grupal (10), 7.5 y 7.8 pasan a Deseable → resuelve R2.
3. Métricas rehechas con modelo de cola y valor anual en pesos en `docs/working-backwards.md` → resuelve R5.

R5 queda **resuelto** con la decisión 3.

## Decisiones del equipo (4 nov, 2.ª ronda)
Frontend en Angular · MVP sin pasadías ni QR por correo · sedes fuera de la demo · esquema de BD propio con datos ficticios · API facial con `x-api-key`, solo producción · us-east-1 con Haiku 4.5 · equipo de 2 (frontend / resto) · roles por evento con cuentas del administrador CONFA · PIN definido por el logístico · modos de puerta logístico y punto fijo · QR solo descargable · reingreso en ámbar · cupo flexible y aforo rígido · CSV con plantilla · `resumen_novedades` · aviso de habeas data (borrador).

---

# Auditoría 2.ª ronda: spec-rubrica · codigo (frontend) · seguridad (delta)
Alcance: documentos tras el cambio a Angular y las decisiones de la 2.ª ronda (design v3 → v4) · 4 nov 2026 · dos subagentes `auditor` en paralelo.

| Lente | Veredicto antes de corregir |
|---|---|
| spec-rubrica + codigo (frontend) | LISTO CON AJUSTES — nota estimada 54/100 hoy, 88 proyectada |
| seguridad (delta) | LISTO CON AJUSTES |

| # | Lente | Sev. | Hallazgo | Resolución |
|---|---|---|---|---|
| C1 | spec | 🔴 | QR no regenerable con solo `sha256(token)` | `token = HMAC(secreto_qr, inscripcion_id ‖ qr_version)`; PNG/PDF en servidor sin documento; rotación (2.6) |
| C2 | spec | 🔴 | Punto fijo: el ámbar no llega al logístico | 4.8 y `GET /eventos/{id}/pendientes` |
| C3 | spec | 🟠 | Comunicado promete Deseables | Comunicado reescrito; "Próximamente: pasadías, virtual e híbrido, sedes" |
| C4 | spec | 🟠 | WB Experiencia y mockup con Deseables sin marcar | Pasos marcados "(Deseable)"; QR compartido por el organizador; mockup sin foto grupal |
| C5 | spec | 🟠 | Tablas del reto sin prioridad | Columna de prioridad; "varios rostros" Deseable; pasadía agregada; 2.4 y 8.1 ajustados |
| C6 | agentcore | 🟠 | Memory: plan sin verificar y contradicción | Comando verificado `--strategies SUMMARIZATION` limitado a la sesión, 3 días |
| C7 | codigo | 🟠 | CSP incompatible con estilos de Angular | CSP completa con `style-src 'unsafe-inline'`, Trusted Types, `inlineCritical: false` |
| C8 | codigo | 🟠 | Guards sin fuente de roles | `GET /me/eventos` en un `signal`; el 403 de la API es la barrera |
| C9 | tests | 🟠 | Vitest sin IndexedDB y PBKDF2 lento | Interfaces `Almacen`, `Cripto` y `ahora()` inyectadas |
| C10 | spec | 🟡 | Numeración 13.x | 13.9–13.12 en orden |
| C11 | spec | 🟡 | Restos (`VITE_*`, región, Haiku 5.5, diagrama) | Corregidos; Página virtual y Rekognition marcados Deseables |
| C12 | codigo | 🟡 | Interceptor, polling, cámara | JWT solo a `apiBase`; `takeUntilDestroyed`; `facingMode: { ideal }`; `ng serve --ssl` |
| C13 | spec | 🟡 | Retención de consentimientos | 1 año, igual que la trazabilidad |
| C14 | spec | 🟡 | Fuente vendor de la evidencia 5 | Fielddrive citado; rangos sin fuente única marcados [supuesto] |
| C15 | spec | 🟡 | Informe de auditoría desactualizado | Esta sección |
| D1 | seguridad | 🔴 | Punto fijo expone una sesión del personal | Rol `punto_fijo` (solo rostro y QR), ruta `/kiosco` bloqueada con código de supervisor, cámara solo tras "Acepto" (4.7) |
| D2 | seguridad | 🔴 | Paquete en caché HTTP; envoltura ambigua; contador | `Cache-Control: no-store`; `ngsw` sin `dataGroups`; envoltura en serie; contador en claro como barrera de uso (13.12) |
| D3 | seguridad | 🟠 | Token de Cognito y CSP sin `connect-src` | PKCE con `angular-auth-oidc-client`, refresh de 12 h, `revokeToken`/`GlobalSignOut`, `connect-src`, `Permissions-Policy` |
| D4 | seguridad | 🟠 | Autorización por correo; quién asigna roles | Llave `sub`; `email` no modificable; grupos `admin_confa`, `creador_eventos`, `aprobador`; 13.11 |
| D5 | seguridad | 🟠 | QR masivo sin control | Solo el organizador, sin documento, registrado (`descargar_qr`), rotación |
| D6 | seguridad | 🟠 | Inyección de fórmulas CSV y sobrescritura | Validación al importar, escape al exportar, `nombre_cargado` en inscripciones, informe enmascarado, URL de 5 min |
| D7 | seguridad | 🟠 | Semáforo sin orden; tipos de documento | Orden de evaluación; lista permitida de adultos; 6.6 no editable |
| D8 | seguridad | 🟠 | Aforo con carreras y sin conexión | Transacción con `FOR UPDATE`; tope local offline (9.5) |
| D9 | seguridad | 🟠 | 1 petición/s no garantizado; pruebas contra producción | *Throttling* en API Gateway; `FACIAL_MODO=mock` por defecto; `conftest.py` |
| D10 | seguridad | 🟠 | Aviso borrador sin mínimos legales | Texto con responsable, finalidad, carácter facultativo y alternativa (5.8); API real solo con documentos del equipo mientras sea borrador |
| D11 | seguridad | 🟡 | `resumen_novedades` | Solo conteos, con prueba |
