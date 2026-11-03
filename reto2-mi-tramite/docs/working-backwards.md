# Working Backwards — Reto 2: autogestión de solicitudes de GTH

> Borrador para validar (laboratorio del 3 nov 2026).

## Reto
Autogestión centralizada, simple para el colaborador y flexible por dentro, para trámites de Talento Humano: vacaciones, incapacidades, certificados y permisos no remunerados, con rutas de aprobación configurables sin programar y trazabilidad completa.

## 1. Cliente
- **Principal:** el colaborador de CONFA desde que radica un trámite hasta que recibe la respuesta. Ejemplo: quien pide vacaciones para diciembre y necesita saber a tiempo si se las aprobaron.
- **Secundarios:** el líder que aprueba (bandeja propia) y el equipo de GTH, que configura los trámites y hoy responde las preguntas de estado.

## 2. Problema
El colaborador radica su trámite por correo o por chat y, desde ahí, queda a ciegas: no sabe si alguien lo recibió, quién lo tiene ni cuánto falta. Para saberlo tiene que preguntar, y GTH responde esas preguntas una por una en vez de avanzar con los trámites. Las rutas cambian según el caso (solo el líder, varias áreas o escalamiento), así que ni el colaborador ni el aprobador tienen una visión unificada. Las incapacidades llegan muchas veces con soportes incompletos y se devuelven, lo que retrasa el trámite. Crear un trámite nuevo o cambiar su ruta exige que alguien programe.

**Consecuencias:**
- Del orden de 40 horas al mes de GTH respondiendo "¿en qué va lo mío?".
- Ciclos de aprobación de varios días en trámites que podrían resolverse en horas.
- Solicitudes perdidas o reprocesadas, y soportes devueltos.

| Cifra | Etiqueta | Fuente |
|---|---|---|
| ~1.200 colaboradores | [oficial, aproximado] | Revista Confa, mayo de 2026 |
| ~500 solicitudes al mes | [supuesto] | 5-6 trámites por colaborador al año (1-2 vacaciones, 2 certificados, 1 incapacidad, 1 permiso); usamos 5, el valor conservador |
| ~42 h al mes de GTH en consultas de estado | [supuesto] | 500 consultas × 5 min |
| ~$1,2 millones COP al mes (~$15 millones al año) de tiempo de GTH en consultas | [supuesto] | 42 h × ~$30.000 COP por hora de costo empresa de un profesional; validar el costo hora con GTH |
| Ciclo de aprobación de 3 a 5 días | [vendor] | Casos de referencia de software de gestión de ausencias |

## 3. Beneficio principal
**Saber siempre en qué va mi trámite:** el colaborador radica una vez y ve en todo momento en qué paso está, quién lo tiene y qué falta, sin preguntarle a nadie. Radicar en lenguaje natural y que GTH cree trámites sin programar son medios para lograrlo.

## 4. Evidencia
| # | Evidencia | Etiqueta | Qué prueba |
|---|---|---|---|
| 1 | El enunciado del reto: "las solicitudes se pierden en correos o chats y el colaborador no sabe en qué estado están" | [oficial] | Que el dolor existe: lo dice el cliente |
| 2 | ~1.200 colaboradores en CONFA (Revista Confa, mayo 2026) | [oficial, aproximado] | El tamaño del problema |
| 3 | Portales de autogestión: −65 % de consultas sobre ausencias; ciclo de 3-5 días a menos de 24 h | [vendor] | Orden de magnitud de la mejora |
| 4 | En Colombia el empleador paga los días 1-2 de la incapacidad y tramita el recobro a la EPS (Decreto Ley 019 de 2012, art. 121) | [norma, verificar] | Un soporte incompleto tiene costo para CONFA |
| 5 | **Encuesta a mano alzada en el kickoff a los 17 participantes, que son colaboradores de CONFA**: ¿quién ha tenido que preguntar en qué va una solicitud?, ¿cuánto tardó su última aprobación de vacaciones?, ¿a quién se le ha perdido una? | [kickoff] | Evidencia en vivo de los clientes reales |

## 5. Experiencia
**Colaborador**
1. Escribe: "Necesito vacaciones del 15 al 26 de diciembre".
2. El asistente identifica el trámite, muestra los días disponibles y confirma fechas y tipo antes de radicar.
3. Recibe el número de radicado y una línea de tiempo: Radicado → Líder → GTH → Aprobado.
4. En cada cambio de estado recibe un correo, y en cualquier momento puede preguntar "¿en qué va mi solicitud?".

**Incapacidad**
5. Adjunta la foto del soporte. El asistente revisa en el momento que esté completo (fechas, entidad, firma) y, si falta algo, lo dice antes de radicar.
6. El líder ve "incapacidad del 3 al 5 de noviembre"; **nunca ve el diagnóstico**.

**Líder aprobador**
7. Recibe el correo, abre su bandeja, ve la solicitud con el contexto necesario y aprueba o rechaza con un comentario.

**GTH**
8. Escribe: "Crea el trámite permiso por estudio: lo aprueba el líder y luego GTH, y requiere el certificado de la universidad".
9. El sistema propone la ruta y el formulario; GTH revisa, ajusta y lo publica. Queda disponible sin programar.

**Siempre:** el asistente propone y una persona decide; ninguna aprobación la hace el agente.

## Comunicado de prensa
# CONFA lanza "Mi Trámite CONFA" para que sus colaboradores sepan siempre en qué va cada solicitud
*Manizales, 4 de noviembre de 2026.* Desde hoy, los colaboradores de CONFA radican sus vacaciones, incapacidades, certificados y permisos escribiendo lo que necesitan, y ven en todo momento en qué paso va cada trámite y quién lo tiene. Antes, las solicitudes viajaban por correo y chat, se perdían, y para saber su estado había que preguntar; GTH dedicaba horas a responder esas consultas y crear un trámite nuevo exigía programar. Ahora, el colaborador recibe un radicado y una línea de tiempo, cada aprobador tiene su bandeja y un correo avisa cada cambio. Las incapacidades se revisan al radicarlas, para que no se devuelvan por un soporte incompleto, y el líder ve las fechas sin conocer el diagnóstico. GTH crea un trámite nuevo describiéndolo en palabras.
"Antes mandaba el correo y no sabía nada hasta que preguntaba; ahora sé exactamente dónde está mi solicitud", cuenta Andrés, analista de CONFA *(cita ilustrativa: reemplazar por una frase real de la encuesta del kickoff)*.
En su primer mes, las consultas de estado a GTH bajaron cerca de un 65 % *(referencia del sector; supuesto: ~500 solicitudes al mes)*.

## Métricas y supuestos
| Métrica | Antes | Después | Supuesto |
|---|---|---|---|
| Solicitudes con trazabilidad completa | Parcial | 100 % | Toda solicitud se radica en la plataforma |
| Horas de GTH en consultas de estado | ~42 h/mes | ~15 h/mes (−65 %) | 500 solicitudes, 5 min por consulta, referencia de Apps365 (caso de vendor) |
| Costo de esas consultas | ~$1,26 M COP/mes | ~$0,44 M COP/mes (ahorro ~$9,8 M COP/año) | ~$30.000 COP por hora [supuesto] |
| Ciclo de aprobación (solo líder) | 3-5 días | < 24 h | Referencia de vendor; medir con las marcas de tiempo del sistema |
| Tiempo para configurar un trámite nuevo | Requiere desarrollo | Minutos | Demostrado en vivo |
| Soportes de incapacidad devueltos | Sin dato | Validación al radicar | Medir en el piloto |

## Preguntas abiertas para el kickoff
1. ¿Cuántas solicitudes recibe GTH al mes y de qué tipos?
2. ¿Cuánto tarda hoy una aprobación de vacaciones y una incapacidad?
3. ¿Qué datos de la plataforma de RR. HH. podemos simular (contrato del mock)?
4. ¿Quién aprueba cada tipo de trámite hoy?
