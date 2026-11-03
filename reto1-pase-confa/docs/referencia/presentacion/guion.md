# Guion · Pase CONFA (10 minutos + 5 de preguntas)

Presentador principal: Sergio · Demo: Luis David (ajustar en el ensayo).
Teclas: `T` arranca el cronómetro, `N` muestra las notas, ←/→ avanzan.

## Guion por diapositiva
| # | Diapositiva | Quién | Duración | Acumulado | Mensaje clave |
|---|---|---|---|---|---|
| 1 | Portada | Sergio | 0:20 | 0:20 | "Entrar a un evento de CONFA debería tomar segundos" |
| 2 | Cliente | Sergio | 0:40 | 1:00 | Carolina en la puerta, con el listado en papel |
| 3 | Problema | Sergio | 0:50 | 1:50 | 35 s por persona; 12.086 asistentes en dos eventos; horas de fila |
| 4 | Comunicado | Sergio | 0:30 | 2:20 | "Así lo anunciaríamos" → paso a la demo |
| 5 | **Demo en vivo** | Luis David | 3:30 | 5:50 | Rostro, contingencia QR/cédula y pregunta al agente |
| 6 | Arquitectura | Sergio | 1:00 | 6:50 | La puerta es código; la conversación es un agente |
| 7 | Modelos | Sergio | 0:40 | 7:30 | Un modelo por tarea, y ninguno donde sobra |
| 8 | Seguridad | Sergio | 0:40 | 8:10 | La foto nunca se guarda; menores sin reconocimiento facial |
| 9 | Impacto | Sergio | 0:50 | 9:00 | −70 % de tiempo de ingreso, 75 % sin intervención, cero papel |
| 10 | Think Big | Sergio | 0:30 | 9:30 | Piloto → foto grupal y voz → todos los eventos |
| 11 | Cierre | Sergio | 0:20 | 9:50 | "La puerta deja de ser una fila" |

Margen: 10 s. Si a las 6:50 vamos tarde, saltar los detalles de la diapositiva 7 y decir solo la regla "un modelo por tarea".

## Guion de la demo (3:30)
Datos ficticios: evento `ev-001` "Encuentro de afiliados Arquitectos S.A.", 10 inscritos.

| Paso | Acción | Qué se dice |
|---|---|---|
| 1 (0:00) | Abrir la pantalla Puerta ya autenticado | "Carolina entra con su usuario; solo ve su evento" |
| 2 (0:20) | Aviso de consentimiento → Ana mira la cámara | "Ana acepta, y…" (arrancar cronómetro) "…entró en N segundos" |
| 3 (1:00) | Validar de nuevo a Ana | "Si alguien intenta entrar dos veces, el sistema lo detecta" |
| 4 (1:20) | Luis "no tiene rostro registrado" → botón "Prefiero QR" → cédula | "Uno de cada cuatro asistentes entra así, en segundos" |
| 5 (2:10) | En el asistente: "¿Cuántos han entrado y quién falta de ARQUITECTOS S.A.?" | "Las cifras salen de los datos, no del modelo" |
| 6 (2:50) | Mostrar la traza en AgentCore Observability | "Así razonó: llamó dos herramientas y respondió" |
| 7 (3:20) | Volver a la presentación | — |

## Plan B
1. Si falla la API facial: mostrar la contingencia (es parte del producto: a los 5 s pasa a QR o cédula).
2. Si falla el despliegue en AgentCore: correr `agentcore dev` en el portátil y `agentcore invoke --runtime agent --local`.
3. Si falla todo: video de respaldo de 60 s (grabarlo el jueves temprano) y seguir con la presentación.

## Preguntas probables del jurado
1. **¿Por qué ese modelo?** Las preguntas son consultas con herramientas; Haiku 4.5 las resuelve igual que Sonnet, más rápido y más barato.
2. **¿Por qué un solo agente?** No hay razón de modelo, permisos ni prompt para separar; más agentes serían más latencia y costo.
3. **¿Dónde viven los datos biométricos?** En nuestra solución, en ningún lado: la foto pasa en memoria a la API de CONFA y se descarta. Guardamos cédula, hora y método.
4. **¿Qué pasa si la API facial falla?** A los 5 s la pantalla ofrece QR o cédula; la fila no se detiene.
5. **¿Cómo se integra con los sistemas de CONFA?** Usa la API facial existente y la RDS del evento; las consultas se exponen por AgentCore Gateway para reutilizarlas.
6. **¿Cuánto cuesta operarlo?** La puerta no usa LLM (costo casi cero por ingreso); el agente solo se usa cuando el personal pregunta. Pendiente: estimar con los precios de la cuenta del evento.
7. **¿Cómo escala?** Runtime y Lambda son serverless; la base evita duplicados con una restricción única aunque haya varias puertas.
8. **¿Qué recuerda la memoria y por cuánto tiempo?** La conversación del turno, 3 días, solo resúmenes; nunca imágenes ni cédulas.
9. **¿Qué guardrails usan?** Ataques de prompt, cédula enmascarada con regex propia y tema denegado de biometría de terceros.
10. **¿Y los niños en eventos de preescolar?** No se les aplica reconocimiento facial: valida el QR o el documento del acudiente (Ley 1581, art. 7).

## Autoevaluación
Correr `/auditoria spec-rubrica` y anotar aquí las 3 mejoras de último momento.
