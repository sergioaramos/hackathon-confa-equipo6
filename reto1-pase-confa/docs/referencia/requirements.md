> **Borrador de referencia** preparado antes del evento. La spec oficial se genera en Kiro durante la hackathon en `.kiro/specs/pase-confa/`, usando este archivo como insumo.

# Requisitos: Pase CONFA

## Introducción
El personal logístico de CONFA valida hoy el ingreso a los eventos con listados de papel: 30-40 s por persona, filas de horas en eventos masivos y sin saber quién entró hasta consolidar a mano. Pase CONFA permite validar a cada asistente en segundos con el reconocimiento facial que CONFA ya opera, con QR o documento como alternativa, y consultar la asistencia en tiempo real. Cubre los tres tipos de evento del reto: con inscripción previa, interno sin registro y externo por documento.

## Requisitos

### Requisito 1: Creación del evento [Deseable]
**Historia:** Como organizador, quiero crear un evento describiéndolo en una frase, para no llenar formularios.
_Origen: WB-P5 paso 1_

#### Criterios de aceptación
1.1 WHEN el organizador describe un evento en lenguaje natural THE SYSTEM SHALL extraer nombre, fecha, hora, lugar, tipo de evento y cupo, y mostrarlos para confirmación antes de crearlo.
1.2 IF falta un dato obligatorio (fecha o lugar) THEN THE SYSTEM SHALL preguntarlo en lugar de suponerlo.
1.3 THE SYSTEM SHALL clasificar el evento en uno de tres tipos: con inscripción previa, interno sin registro o externo por documento.

### Requisito 2: Inscripción y ticket QR [MVP]
**Historia:** Como asistente, quiero recibir un código QR al inscribirme, para entrar aunque no tenga mi rostro registrado.
_Origen: WB-P1 (secundario), WB-P4 #3_

#### Criterios de aceptación
2.1 WHEN se inscribe una persona con su cédula THE SYSTEM SHALL generar un código QR único y firmado, asociado a la persona y al evento.
2.2 THE SYSTEM SHALL permitir inscribir personas por documento de identidad (eventos externos, como los de preescolar).
2.3 IF el QR presentado corresponde a otro evento, fue alterado o ya se usó THEN THE SYSTEM SHALL rechazarlo e indicar el motivo.

### Requisito 3: Validación facial en la puerta [MVP]
**Historia:** Como personal logístico, quiero validar a cada asistente apuntando la cámara, para que la fila avance en segundos.
_Origen: WB-P2, WB-P3, WB-P5 paso 4_

#### Criterios de aceptación
3.1 WHEN el personal captura la foto de un asistente THE SYSTEM SHALL enviarla a la API facial de CONFA y mostrar el resultado en menos de 3 s (sin contar la latencia de la API, por medir en el kickoff).
3.2 WHEN la API devuelve una cédula inscrita en el evento THE SYSTEM SHALL marcar la asistencia con la hora y mostrar "Bienvenido/a, <nombre>".
3.3 IF la API no reconoce el rostro THEN THE SYSTEM SHALL ofrecer de inmediato la validación por QR o documento.
3.4 IF la cédula reconocida no está inscrita en el evento THEN THE SYSTEM SHALL mostrar "no inscrito" y ofrecer el registro en sitio cuando el evento lo permita.
3.5 IF la persona ya ingresó THEN THE SYSTEM SHALL avisarlo con la hora del primer ingreso y no duplicar la asistencia.
3.6 IF la API facial no responde en 5 s THEN THE SYSTEM SHALL pasar a QR o documento sin bloquear la fila.

### Requisito 4: Contingencia por QR y documento [MVP]
**Historia:** Como personal logístico, quiero validar con QR o con la cédula a quien no tiene rostro registrado, para que nadie se quede por fuera.
_Origen: WB-P4 #3 (1 de cada 4)_

#### Criterios de aceptación
4.1 WHEN el personal escanea un QR válido THE SYSTEM SHALL marcar la asistencia en menos de 2 s.
4.2 WHEN el personal digita una cédula THE SYSTEM SHALL validarla contra los inscritos y marcar la asistencia.
4.3 THE SYSTEM SHALL registrar el método de validación (facial, QR o documento) de cada ingreso.

### Requisito 5: Asistencia masiva por foto grupal [Deseable]
**Historia:** Como organizador de un evento interno sin registro, quiero marcar la asistencia con una foto del auditorio, para no pasar listas.
_Origen: caso de uso "Encuentro con el Director"_

#### Criterios de aceptación
5.1 WHEN se carga una foto grupal THE SYSTEM SHALL detectar cada rostro, validarlo con la API facial y marcar la asistencia de los reconocidos.
5.2 THE SYSTEM SHALL informar cuántos rostros detectó, cuántos reconoció y cuántos no.

### Requisito 6: Consulta en lenguaje natural [MVP]
**Historia:** Como personal logístico, quiero preguntar "¿cuántos han entrado y quién falta de la empresa X?", para tener control sin revisar listados.
_Origen: WB-P2 (trabaja a ciegas), WB-P5 paso 7_

#### Criterios de aceptación
6.1 WHEN el personal hace una pregunta sobre la asistencia THE SYSTEM SHALL responder en español con cifras obtenidas de los datos del evento, nunca estimadas por el modelo.
6.2 THE SYSTEM SHALL responder preguntas de conteo total, conteo por empresa o grupo, ausentes por empresa y ritmo de ingreso.
6.3 IF la pregunta no es sobre el evento THEN THE SYSTEM SHALL indicar amablemente que solo responde sobre la asistencia del evento.

### Requisito 7: Tablero en tiempo real [MVP]
**Historia:** Como personal logístico, quiero ver el conteo de ingresos en vivo, para saber cómo va la puerta.
_Origen: requisito del reto "tiempo real"_

#### Criterios de aceptación
7.1 WHILE el evento está abierto THE SYSTEM SHALL mostrar ingresados, inscritos y porcentaje, actualizados en menos de 5 s.
7.2 THE SYSTEM SHALL mostrar el desglose por método de validación (facial, QR, documento).

### Requisito 8: Informe de cierre [Deseable]
**Historia:** Como organizador, quiero el informe de asistencia al cerrar el evento, para no consolidar a mano.
_Origen: WB-P2 (consolidación manual), WB-P5 paso 9_

#### Criterios de aceptación
8.1 WHEN el organizador cierra el evento THE SYSTEM SHALL generar un informe con asistencia total, por empresa, por método y por franja horaria.

### Requisito 9: Acceso seguro del personal [MVP]
**Historia:** Como personal logístico, quiero entrar rápido y de forma segura a la aplicación, para empezar a validar sin demoras.
_Origen: enunciado del reto ("acceso rápido y seguro")_

#### Criterios de aceptación
9.1 THE SYSTEM SHALL exigir autenticación del personal antes de validar ingresos o consultar asistencia.
9.2 THE SYSTEM SHALL permitir al personal operar solo los eventos que tiene asignados.

### Requisito 10: Privacidad y seguridad (Ley 1581) [MVP]
**Historia:** Como asistente, quiero que mis datos biométricos se usen solo para validar mi ingreso, para confiar en CONFA.
_Origen: steering seguridad.md_

#### Criterios de aceptación
10.1 THE SYSTEM SHALL NOT almacenar imágenes faciales en la base de datos, en logs ni en la memoria del agente; solo la cédula, la hora y el método.
10.2 WHEN se va a validar un rostro THE SYSTEM SHALL mostrar un aviso de consentimiento y la alternativa sin biometría.
10.3 IF el evento es de preescolar THEN THE SYSTEM SHALL NOT aplicar reconocimiento facial a menores; el ingreso se valida con el QR o el documento del acudiente.
10.4 THE SYSTEM SHALL enmascarar los números de cédula en las respuestas del asistente conversacional.
10.5 IF alguien intenta que el asistente revele datos personales fuera del alcance de su evento THEN THE SYSTEM SHALL rechazarlo.

## Aclaraciones (3 nov 2026)
1. El personal opera desde una aplicación web en celular o tableta, con la cámara del navegador.
2. El objetivo de 3 s (3.1) se ajusta cuando se mida la latencia de la API facial en el kickoff.
3. El registro en sitio de no inscritos (3.4) es configurable por evento y viene apagado por defecto.
4. La foto grupal (requisito 5) sigue como Deseable hasta confirmar que la API facial acepta recortes.
5. Informe de cierre (requisito 8): vista en la aplicación + exportación a CSV.

## Fuera de alcance
Pagos y boletería; enrolamiento facial de nuevas personas (lo hace CONFA en sus canales); integración con sistemas distintos de la API facial y la RDS del evento.

## Matriz de trazabilidad
| Pregunta WB | Requisitos |
|---|---|
| P1 Cliente | 3, 4, 6, 7, 9 |
| P2 Problema | 3, 6, 7, 8 |
| P3 Beneficio (ingreso en segundos) | 3, 4 |
| P4 Evidencia (1 de cada 4 sin rostro) | 2, 4 |
| P5 Experiencia | 1-8 |
| Seguridad (Ley 1581) | 9, 10 |
| Casos de uso del reto | Con inscripción: 2-4 · Sin registro: 5 · Por documento: 2.2, 4.2, 10.3 |
