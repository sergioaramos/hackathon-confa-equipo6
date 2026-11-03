> **Borrador de referencia** preparado antes del evento. La spec oficial se genera en Kiro durante la hackathon en `.kiro/specs/mi-tramite/`, usando este archivo como insumo.

# Requisitos: Mi Trámite CONFA

## Introducción
Los colaboradores de CONFA radican vacaciones, incapacidades, certificados y permisos por correo o chat, y quedan a ciegas sobre su estado; GTH responde esas consultas una por una y no puede crear trámites ni rutas sin programar. Mi Trámite CONFA permite radicar en lenguaje natural, ver siempre en qué va cada solicitud, aprobar desde una bandeja propia y crear trámites nuevos describiéndolos en palabras. El agente propone; una persona siempre decide.

## Requisitos

### Requisito 1: Radicar en lenguaje natural [MVP]
**Historia:** Como colaborador, quiero pedir un trámite escribiendo lo que necesito, para no buscar formularios.
_Origen: WB-P5 pasos 1-3_

#### Criterios de aceptación
1.1 WHEN el colaborador describe una necesidad THE SYSTEM SHALL identificar el tipo de trámite publicado que corresponde y extraer sus campos (por ejemplo, fechas de inicio y fin).
1.2 THE SYSTEM SHALL mostrar el resumen de la solicitud y pedir confirmación antes de radicarla.
1.3 IF falta un dato obligatorio o la petición es ambigua THEN THE SYSTEM SHALL preguntarlo en lugar de suponerlo.
1.4 IF ningún trámite publicado corresponde THEN THE SYSTEM SHALL decirlo y mostrar los trámites disponibles.
1.5 WHEN se radica una solicitud THE SYSTEM SHALL asignar un número de radicado y mostrarlo.
1.6 IF el tipo de trámite exige adjuntos (por ejemplo, el certificado de la universidad en un permiso por estudio) THEN THE SYSTEM SHALL pedirlos y no radicar hasta recibirlos.

### Requisito 2: Reglas del trámite [MVP]
**Historia:** Como colaborador, quiero saber antes de radicar si mi solicitud cumple las reglas, para no recibir un rechazo evitable.
_Origen: WB-P2 (reprocesos)_

#### Criterios de aceptación
2.1 WHEN se piden vacaciones THE SYSTEM SHALL consultar los días disponibles del colaborador y mostrarlos, contando días hábiles sin fines de semana ni festivos de Colombia.
2.2 IF los días pedidos superan los disponibles THEN THE SYSTEM SHALL informarlo y no radicar.
2.3 IF la fecha de fin es anterior a la de inicio THEN THE SYSTEM SHALL pedir corregirla.

### Requisito 3: Incapacidades y soportes [MVP]
**Historia:** Como colaborador, quiero que me digan al radicar si mi soporte de incapacidad está completo, para que no me lo devuelvan.
_Origen: WB-P2, WB-P5 paso 5_

#### Criterios de aceptación
3.1 WHEN el colaborador adjunta un soporte THE SYSTEM SHALL verificar que contenga fechas de inicio y fin, entidad emisora y firma o sello.
3.2 IF el soporte está incompleto o ilegible THEN THE SYSTEM SHALL indicar qué falta y no radicar.
3.3 THE SYSTEM SHALL NOT extraer, persistir (base de datos, memoria, logs) ni mostrar a aprobadores el diagnóstico; el modelo procesa la imagen sin guardarla.
3.5 WHEN el colaborador va a adjuntar un soporte con datos de salud THE SYSTEM SHALL mostrar el aviso de tratamiento de datos (Ley 1581) y pedir su aceptación explícita.
3.4 THE SYSTEM SHALL almacenar el archivo del soporte cifrado y accesible solo para el rol GTH.

### Requisito 4: Rutas de aprobación configurables [MVP]
**Historia:** Como GTH, quiero que cada trámite siga la ruta que le corresponde, para que el colaborador no tenga que saber a quién enviarlo.
_Origen: enunciado del reto (rutas según el caso)_

#### Criterios de aceptación
4.1 WHEN se radica una solicitud THE SYSTEM SHALL ejecutar la ruta configurada para su tipo: solo líder, líder y luego GTH, varias personas o áreas, o escalamiento por condición, resolviendo cada paso a un aprobador concreto.
4.2 WHEN una condición de escalamiento se cumple (por ejemplo, vacaciones de más de 10 días hábiles) THE SYSTEM SHALL agregar el paso de aprobación definido.
4.3 IF un aprobador rechaza THEN THE SYSTEM SHALL cerrar la solicitud como rechazada con el comentario.
4.4 THE SYSTEM SHALL ejecutar las rutas a partir de su configuración, sin código específico por tipo de trámite.

### Requisito 5: Bandeja del aprobador [MVP]
**Historia:** Como líder, quiero una bandeja con mis pendientes, para aprobar sin buscar correos.
_Origen: enunciado del reto (bandeja por aprobador), WB-P5 paso 7_

#### Criterios de aceptación
5.1 THE SYSTEM SHALL mostrar a cada aprobador solo las solicitudes que tiene pendientes.
5.2 WHEN el aprobador aprueba o rechaza THE SYSTEM SHALL exigir un comentario en el rechazo y avanzar la ruta.
5.3 THE SYSTEM SHALL mostrar al aprobador de una incapacidad solo el tipo y las fechas.

### Requisito 6: Trazabilidad [MVP]
**Historia:** Como colaborador, quiero ver en qué paso va mi solicitud y quién la tiene, para no tener que preguntar.
_Origen: WB-P3 (beneficio principal)_

#### Criterios de aceptación
6.1 THE SYSTEM SHALL registrar cada cambio de estado con fecha, hora, actor y comentario.
6.2 WHEN el colaborador consulta una solicitud THE SYSTEM SHALL mostrar su línea de tiempo: pasos hechos, paso actual con su responsable y pasos pendientes.
6.3 WHEN el colaborador pregunta "¿en qué va mi solicitud?" THE SYSTEM SHALL responder con el estado registrado, nunca estimado por el modelo.
6.4 THE SYSTEM SHALL permitir a cada colaborador consultar solo sus propias solicitudes.

### Requisito 7: Notificaciones [MVP]
**Historia:** Como colaborador y aprobador, quiero un correo en cada cambio, para enterarme sin entrar a revisar.
_Origen: enunciado del reto_

#### Criterios de aceptación
7.1 WHEN cambia el estado de una solicitud THE SYSTEM SHALL enviar un correo al colaborador y al siguiente aprobador.
7.2 THE SYSTEM SHALL NOT incluir diagnósticos ni adjuntos en los correos.

### Requisito 8: Crear trámites sin programar [MVP]
**Historia:** Como GTH, quiero crear un trámite nuevo describiéndolo en palabras, para no depender de desarrollo.
_Origen: enunciado del reto, WB-P5 pasos 8-9_

#### Criterios de aceptación
8.1 WHEN GTH describe un trámite THE SYSTEM SHALL proponer su configuración: nombre, campos, adjuntos requeridos y ruta de aprobación.
8.2 THE SYSTEM SHALL validar la configuración contra un esquema antes de mostrarla.
8.3 THE SYSTEM SHALL NOT publicar un trámite sin confirmación explícita de GTH.
8.4 WHEN GTH publica un trámite THE SYSTEM SHALL dejarlo disponible para radicar sin desplegar código.
8.5 WHEN GTH modifica la ruta o los campos de un trámite existente THE SYSTEM SHALL publicarlo como una versión nueva, sin alterar las solicitudes en curso.

### Requisito 9: Acceso por rol [MVP]
**Historia:** Como CONFA, quiero que cada persona vea solo lo que le corresponde, para proteger los datos de los colaboradores.
_Origen: steering seguridad.md_

#### Criterios de aceptación
9.1 THE SYSTEM SHALL exigir autenticación y distinguir los roles colaborador, aprobador y GTH.
9.2 THE SYSTEM SHALL tomar la identidad del usuario de la sesión autenticada, nunca de lo que escriba en el chat.

### Requisito 10: Privacidad e IA responsable (Ley 1581) [MVP]
**Historia:** Como colaborador, quiero que mis datos de salud estén protegidos, para confiar en el trámite.
_Origen: steering seguridad.md_

#### Criterios de aceptación
10.1 THE SYSTEM SHALL NOT guardar diagnósticos en la memoria del agente, en logs ni en correos.
10.2 IF alguien pide al asistente datos de otro colaborador THEN THE SYSTEM SHALL rechazarlo.
10.3 THE SYSTEM SHALL NOT aprobar ni rechazar solicitudes por sí mismo: solo una persona decide.
10.4 THE SYSTEM SHALL enmascarar números de cédula en las respuestas del asistente.

### Requisito 11: Tablero de GTH [Deseable]
11.1 THE SYSTEM SHALL mostrar a GTH el ciclo promedio por tipo de trámite y los pendientes por aprobador.

### Requisito 12: Recordatorios [Deseable]
12.1 WHILE una solicitud lleva más de 24 h sin respuesta THE SYSTEM SHALL recordar al aprobador por correo.

## Aclaraciones
1. La plataforma de RR. HH. se simula con un mock con contrato OpenAPI: colaborador, líder, aprobadores por rol o área, días disponibles y festivos.
3. Hasta tener Cognito (tarea 27), la identidad se simula con un usuario de prueba firmado en la sesión; la regla "identidad desde la sesión" (9.2) se cumple desde el bloque 1.
4. Tipos sembrados: vacaciones, incapacidad y certificado laboral; "permiso por estudio" se crea en vivo en la demo.
2. En el laboratorio los correos se registran en un buzón simulado; en el evento salen por Amazon SES (en modo sandbox, solo a correos verificados del equipo).

## Fuera de alcance
Nómina y liquidación; recobro real a la EPS; integración real con la plataforma de RR. HH.

## Matriz de trazabilidad
| Pregunta WB | Requisitos |
|---|---|
| P1 Cliente (colaborador, líder, GTH) | 1, 5, 8 |
| P2 Problema | 2, 3, 6 |
| P3 Beneficio (saber en qué va) | 6, 7 |
| P4 Evidencia (consultas de estado) | 6.3 |
| P5 Experiencia | 1-8 |
| Seguridad | 3.3, 3.4, 5.3, 7.2, 9, 10 |
| Requisitos funcionales del reto | Radicar con adjuntos: 1, 3 · Trámites sin programar: 8 · Rutas: 4 · Bandeja: 5 · Correo: 7 · Trazabilidad: 6 |
