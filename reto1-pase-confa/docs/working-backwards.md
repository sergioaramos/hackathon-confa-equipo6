# Working Backwards — Reto 1: experiencia y control de eventos

> Borrador en construcción (laboratorio del 3 nov 2026).

## Reto
Centralizar y digitalizar el ciclo de vida de los eventos de CONFA (creación, inscripción, tickets, control de acceso en sitio y consolidación en tiempo real) para colegios, afiliados, empresas y colaboradores internos.

## 1. Cliente
- **Principal:** el personal logístico de CONFA en la puerta de un evento, durante los 30 a 60 minutos de ingreso masivo, con una fila de cientos de personas y un listado en papel para validar a cada una.
- **Secundario:** el asistente, que hace fila sin saber cuánto le falta. Uno de cada cuatro no tiene la cara registrada y necesita otra forma de entrar.

## 2. Problema
En cada ingreso masivo, el personal logístico busca a cada asistente a mano en un listado de papel: pide la cédula, pasa hojas y marca con lápiz. Cada persona toma entre 30 y 40 segundos, y la fila crece más rápido de lo que avanza. Cuando llega alguien que no aparece o no está inscrito, todo se detiene mientras se decide qué hacer. El personal no tiene un acceso rápido y seguro a la plataforma desde la puerta, así que trabaja a ciegas: no sabe cuántos han entrado ni quién falta.

**Consecuencias:**
- En un evento masivo de ~6.000 asistentes, el ingreso toma del orden de 9 a 10 horas de flujo repartidas entre 6 puertas.
- Al cierre, alguien pasa horas transcribiendo listados para consolidar la asistencia.
- Se imprime papel en cada evento.

| Cifra | Etiqueta | Fuente |
|---|---|---|
| 30–40 s por asistente con listado manual | [vendor] | Fielddrive, referencia del sector |
| ~6.000 asistentes por evento masivo | [oficial] | Informe de Gestión 2025: 12.086 asistentes en 2 eventos de La Rochela |
| ~9,7 h de flujo con 6 puertas | [supuesto] | 6.000 × 35 s ÷ 6 puertas |
| Horas de consolidación | [supuesto] | Validar en el kickoff |

## 3. Beneficio principal
**Ingreso en segundos:** cada asistente entra en segundos, con su cara o con un QR, sin que nadie lo busque en papel. El control en vivo y el cero papel son consecuencias de este beneficio.

## 4. Evidencia
| # | Evidencia | Etiqueta | Qué prueba |
|---|---|---|---|
| 1 | El enunciado de CONFA reconoce "cuellos de botella, filas, papel y listados manuales" y que el personal "no siempre accede de forma rápida y segura" a la plataforma en sitio | [oficial] | Que el dolor existe: lo dice el cliente |
| 2 | CONFA ya tiene identidad digital biométrica de 268.724 personas y usa reconocimiento facial en el ingreso a sus centros recreacionales (Informe de Gestión 2025) | [oficial] | Que la solución se apoya en algo que CONFA ya opera |
| 3 | ~75 % de cobertura biométrica (268.724 / 356.123) → ~1 de cada 4 asistentes necesitará QR | [oficial + cálculo] | Que la contingencia QR es un flujo principal |
| 4 | 44 eventos empresariales; 12.086 asistentes en 2 eventos masivos de La Rochela; 15.803 usos en eventos y bienestar (Informe 2025) | [oficial] | Que el problema se repite y el impacto escala |
| 5 | Listado manual 30–40 s; QR 15–20 s; facial 3–10 s por persona | [vendor] | Orden de magnitud de la mejora |
| 6 | Pregunta a un mentor de CONFA en el kickoff: duración del ingreso, puertas y tiempo de consolidación | [kickoff] | Convierte los supuestos en datos reales |

En la demo se mide el tiempo de ingreso en vivo con el cronómetro.

## 5. Experiencia (personal logístico)
**Antes del evento**
1. El organizador describe el evento en una frase ("Encuentro de afiliados de Arquitectos S.A., sábado 9 a. m. en La Rochela, 300 inscritos") y queda creado.
2. Cada inscrito recibe su código QR por correo como respaldo.

**En la puerta**
3. El personal entra a la aplicación desde su celular o tableta con acceso rápido y seguro.
4. El asistente mira la cámara: en ~3 s aparece "Bienvenida, Ana Gómez" y la asistencia queda marcada.
5. Si no lo reconoce (~1 de cada 4), la pantalla pide el QR, que se escanea.
6. Sin QR, se digita la cédula y se valida contra los inscritos; si no está inscrito, se puede registrar en el momento.

**Durante y al cierre**
7. El personal pregunta "¿cuántos han entrado y quién falta de Arquitectos S.A.?" y recibe la respuesta al instante.
8. "Encuentro con el Director": una foto del auditorio marca la asistencia de todos los que aparecen.
9. Al cerrar, el informe de asistencia está listo.

**Privacidad:** aviso de consentimiento antes de usar el rostro. La foto nunca se guarda: solo la cédula y la hora. En preescolar, a los niños no se les aplica reconocimiento facial; valida el QR o el documento del acudiente.

## Comunicado de prensa
# CONFA lanza "Pase CONFA" para que su personal logístico valide el ingreso a eventos en segundos
*Manizales, 4 de noviembre de 2026.* Desde hoy, el personal logístico de CONFA valida el ingreso a sus eventos en segundos, sin buscar a nadie en listados de papel. Antes, cada asistente tomaba entre 30 y 40 segundos en la puerta, un evento masivo acumulaba horas de fila y nadie sabía con certeza quién había entrado hasta transcribir los listados al final del día. Ahora, el asistente mira la cámara y en tres segundos aparece su bienvenida. Quien no tiene su rostro registrado, o prefiere no usarlo, muestra el código QR que recibió al inscribirse, y quien no lo tiene se valida con su documento. Desde la misma pantalla, el personal pregunta cuántos han entrado y quién falta, y recibe la respuesta al instante.
"Antes la fila le daba la vuelta al parqueadero; ahora la gente pasa casi sin detenerse", cuenta Carolina, auxiliar de logística en La Rochela.
En su primer evento masivo, el tiempo total de ingreso se redujo cerca de un 70 % *(estimado con 6 puertas y tiempos de referencia del sector)*.

## Métricas y supuestos
| Métrica | Antes | Después | Supuesto |
|---|---|---|---|
| Tiempo por asistente | 30–40 s [vendor] | ~3–8 s facial; 15–20 s QR [vendor] | 75 % facial, 25 % QR |
| Flujo de ingreso, evento de 6.000 | ~9,7 h | ~2,9 h (−70 %) | 6 puertas |
| Consolidación de asistencia | Horas [supuesto] | Inmediata | Validar en el kickoff |
| Papel | Listados impresos | 0 | — |
| % validados sin intervención manual | 0 % | ~75 % | Cobertura biométrica |

## Preguntas abiertas para el kickoff
1. ¿Cuánto dura hoy el ingreso a un evento grande y cuántas puertas usan?
2. ¿Cuánto tardan en consolidar la asistencia?
3. ¿Cuál es la latencia de la API facial y acepta recortes de una foto grupal?
4. ¿Se permite registrar en sitio a personas no inscritas?
