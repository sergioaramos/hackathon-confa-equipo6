---
inclusion: always
---
# Producto: Pase CONFA

## CONFA
Caja de Compensación Familiar de Caldas (Manizales). Lema: "Contigo, con todo". Atiende a 14.984 empresas, 173.055 trabajadores afiliados y 356.123 personas en total (Informe de Gestión 2025). Ya tiene identidad digital biométrica de 268.724 personas y usa reconocimiento facial en sus centros recreacionales. La solución se **suma** a ese ecosistema.

## Reto elegido
Reto 1: experiencia y control de eventos.

## Cliente
- Principal: el asistente (que entre rápido; uno de cada cuatro sin rostro registrado; puede no tener internet ni conocimiento de tecnología) y el logístico en la puerta (que lo reconozca y sepa qué hacer).
- Añadido (no es el núcleo): la empresa afiliada que solicita un evento y el aprobador de CONFA que acepta la reserva.
- Tipos de evento: externo por reserva, interno, e individual administrado por CONFA (pasadías en centros recreacionales).

## Problema
Identificar a cada persona es el cuello de botella. En la puerta, validación manual con listados de papel: 30-40 s por persona, filas largas bajo el sol, sin visibilidad de quién entró, consolidación manual al cierre y sin alternativa si falla internet.

## Complementos (4 nov)
- Mayor problema: identificar a la persona, de forma masiva o individual. El logístico en la entrada debe ver quién es y qué hacer, sin diagnósticos.
- Voz solo como interfaz para consultas y reportes (Deseable); la voz como biometría y la cédula dicha al sistema quedan fuera de alcance.
- Asistente puede no tener conocimiento de tecnología.
- Hay eventos sin registro previo: se identifica y registra en el momento (datos mínimos: cédula, nombre, teléfono, correo).
- Los eventos pueden ser presenciales, virtuales o híbridos; la asistencia se consolida por canal.
- Sin conexión no hay reconocimiento facial local: se valida con QR y cédula.
- Voz: consultas y reportes en lenguaje natural (Deseable).

## Beneficio principal
Ingreso en segundos, con o sin internet: con la cara, con QR o con documento, sin buscar en papel.

## Comunicado de prensa
Ver `docs/working-backwards.md`.

## Métricas de impacto
- Ingreso de un evento de 6.000 asistentes: ~9,7 h → ~2,9 h de flujo (−70 %) [supuesto: 6 puertas, tiempos de referencia del sector].
- Espera promedio en fila de un evento masivo: ~3 h 52 min → ~26 min [supuesto: llegada uniforme en 2 h].
- ~54.600 horas de espera evitadas al año (2 masivos + 44 empresariales), ~$409 M a $7.500/h [supuesto]; ~224 h de personal, ~$3,4 M a $15.000/h [supuesto].
- ~75 % de validaciones sin buscar en papel, como techo [cobertura biométrica oficial].
- Consolidación inmediata; cero listados impresos.

## Alcance MVP (4 nov)
MVP: requisitos 1–9, 11 (consultas por texto al agente), 13 y 14, con eventos externos e internos presenciales y QR descargable. Deseable: QR por correo, pasadías, foto grupal (10), sedes (12, fuera de la demo), virtual e híbrido (15), crear eventos con lenguaje natural (16), voz (17), sincronización entre dispositivos y registro offline (7.5, 7.8).

## Fuera de alcance
Pagos y venta de boletería; integración con sistemas de CONFA distintos de la API facial y la RDS del evento.
