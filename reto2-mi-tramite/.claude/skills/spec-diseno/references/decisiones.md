# Guías de decisión para el diseño

## 1. ¿Agente o código?
| Agente (LLM) | Código / servicio |
|---|---|
| Entrada en lenguaje natural ambiguo | Entrada estructurada (formulario, foto → API) |
| Hay que decidir entre opciones o interpretar | Siempre se hace lo mismo |
| Redactar, resumir, explicar | Regla fija, cálculo exacto, flujo de aprobación definido |

Ejemplos: la validación en la puerta (foto → API facial → RDS → marcar) es **código** porque la latencia importa. La ruta de aprobación ya definida la ejecuta **Step Functions**. Convertir "crea un trámite de permiso por estudio que apruebe el líder y luego GTH" en la configuración de esa ruta es **agente**.

## 2. ¿Uno o varios agentes?
Agrega un agente solo si se cumple al menos una:
- Necesita un **modelo distinto** (barato para clasificar, potente para razonar).
- Necesita **permisos o reglas distintas** (el que ve incapacidades no es el que habla con todos).
- Un solo system prompt se vuelve **enorme y contradictorio**.

Costo de cada agente extra: más llamadas, más latencia, más difícil de depurar.

## 2b. Alcance de las herramientas
El **alcance** de los datos (qué evento, qué colaborador, qué usuario) nunca lo decide el modelo: va fijo en el código de la herramienta o sale de la identidad autenticada (JWT). Las herramientas solo reciben los parámetros que el usuario puede variar legítimamente (por ejemplo, la empresa por la que pregunta). Documenta las firmas así en el diseño: `ausentes_por_grupo(empresa)`, no `ausentes_por_grupo(evento_id, empresa)`.

## 2c. Reglas de negocio configurables: dato, no código
Cuando el reto pide "configurar sin programar" (rutas, trámites, tipos de evento), modela la regla como **datos validados contra un esquema** (Pydantic/JSON Schema) y un **motor determinista** que los interpreta. El agente solo **propone** la configuración; una persona la publica. Versiona las configuraciones para que un cambio no altere lo que ya está en curso.

## 2d. Privacidad: redacta con precisión
No escribas "nadie ve el dato" si un modelo lo procesa o un rol lo puede abrir. Di exactamente qué se procesa, qué se persiste, dónde y quién accede: "el modelo procesa la imagen sin guardarla; el diagnóstico no se extrae ni se persiste; el archivo cifrado solo lo abre GTH". El jurado de seguridad lo nota.

## 3. Patrones de Strands
| Situación | Patrón | Strands |
|---|---|---|
| Un agente con herramientas alcanza | Agente único | `Agent(tools=[...])` |
| Chat de entrada + temas separables | Agentes como herramienta | `especialista.as_tool()` o un `@tool` que llama a un `Agent` |
| Proceso con pasos y decisiones conocidos, auditable | Graph | `GraphBuilder().add_node/add_edge(condition=...)` |
| Tareas fijas con dependencias, algunas en paralelo | Workflow | herramienta `workflow` de strands-agents-tools |
| Tarea abierta o creativa, el orden no importa | Swarm | `Swarm([a, b, c])` (poco predecible: evitar en el camino de la demo) |

Predecibilidad: Workflow > Graph > Agentes como herramienta > Swarm. **En una demo en vivo, prioriza lo predecible.**

## 4. Modelos de Bedrock (catálogo verificado el 3 nov 2026; confirmar cuáles habilita la cuenta del evento)
| Nivel | Modelo | Modalidad | Para |
|---|---|---|---|
| Ligero | Amazon Nova Micro | Texto | Clasificar intención o tipo de trámite, extraer campos (temperatura 0) |
| Ligero multimodal | Amazon Nova Lite / Nova 2 Lite | Texto, imagen, video | Leer soportes o fotos a bajo costo |
| Intermedio | Claude Haiku 4.5 / 5.5 | Texto, imagen | Conversación ágil con herramientas; agentes especialistas |
| Potente | Claude Sonnet 4.6 / 5 / 5.5 | Texto, imagen | Orquestador; generar configuraciones desde lenguaje natural |
| Tope | Claude Opus, Fable | Texto, imagen | Rara vez se justifica en la hackathon |
| Voz | Amazon Nova 2 Sonic / 2.5 Sonic | Voz ↔ voz | Agente conversacional por voz (Think Big) |
| Embeddings | Titan Embed v2, Cohere multilingual, Nova 2 multimodal embeddings | → vector | Búsqueda en documentos (reglamento de GTH) |
| Visión (no es Bedrock) | Amazon Rekognition `DetectFaces` | Imagen | Detectar y recortar varias caras de una foto grupal |

Criterios: calidad · latencia · costo (tokens de entrada y salida) · modalidad · español. Regla: el modelo **más pequeño** que haga bien la tarea.

## 5. AgentCore
| Pieza | Úsala cuando | Justificación típica |
|---|---|---|
| Runtime | Siempre | Serverless, una microVM por sesión (aislamiento entre usuarios) |
| Memory | Hay que recordar entre sesiones | "Recordamos X por N días; nunca guardamos Y" |
| Gateway | Hay APIs existentes (API facial, mock OpenAPI, Lambda) | Las convierte en herramientas MCP con autenticación, sin wrappers |
| Identity | Hay que controlar quién invoca o con qué credencial sale el agente | Credenciales fuera del código; acceso del personal logístico |
| Observability | Siempre (viene activa) | Mostrar en la demo cómo razonó el agente |

El jurado valora Runtime + Memory y/o Gateway **bien justificados**, no piezas encendidas sin propósito.

## 6. Guardrails por reto
| Reto | Filtros |
|---|---|
| Ambos | Ataques de prompt; contenido dañino; PII con regex para la cédula colombiana (`\b\d{6,10}\b`, ajustar); grounding en respuestas con cifras |
| Reto 1 | Tema denegado: "información biométrica de terceros" |
| Reto 2 | Tema denegado: "diagnósticos médicos de colaboradores"; bloquear consultas sobre solicitudes de otras personas |
