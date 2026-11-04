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

## Pendientes de decisión del equipo
1. Subir el Requisito 11 (consultas por texto) a MVP.
2. Recorte del MVP: virtual e híbrido (15), foto grupal (10), duplicados entre dispositivos (7.5) y registro offline (7.8).
3. Rehacer las métricas de impacto con modelo de cola y valor anual en pesos.
