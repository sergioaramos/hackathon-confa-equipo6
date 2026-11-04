# Requisitos: Pase CONFA

## Introducción
Quien llega a un evento de CONFA (empleado de una empresa afiliada, afiliado, familia en un pasadía) hace fila porque el logístico lo busca a mano en un listado de papel: 30–40 s por persona. Pase CONFA identifica a cada asistente en segundos (rostro, QR o documento), muestra al logístico quién es y qué hacer, funciona sin internet y consolida la asistencia en tiempo real; también atiende a quien llega sin estar registrado en el evento. La solicitud y aprobación de sedes por empresas externas es un añadido.

Convenciones: [MVP] debe funcionar de punta a punta hoy miércoles a las 4:00 p. m.; [Deseable] se hace si sobra tiempo. Un criterio marcado [Deseable] dentro de un requisito MVP también se hace solo si sobra tiempo. Las cifras marcadas [supuesto] se validan en el kickoff.

**Alcance MVP** (decisión del equipo, 4 nov, tras la auditoría): requisitos 1–9, 11, 13 y 14, sin los criterios 2.5, 7.5, 7.8 y 9.6. **Deseable:** 10 (foto grupal), 12 (sedes, fuera de la demo), 15 (virtual e híbrido), 16 (crear eventos con lenguaje natural), 17 (voz), 2.5 (QR por correo), 7.5, 7.8 y 9.6 (pasadías).

## Requisitos

### Requisito 1: Ingreso por reconocimiento facial [MVP]
**Historia:** Como asistente, quiero entrar solo mirando la cámara, para no hacer fila ni mostrar nada.
_Origen: WB-P3 (beneficio), WB-P5 (experiencia)_

#### Criterios de aceptación
1.1 WHEN el logístico captura la foto de un asistente que aceptó el uso del rostro (5.1) THE SYSTEM SHALL enviarla a la API facial de CONFA y mostrar el resultado en menos de 5 s en el percentil 95, sin contar el toque de consentimiento [supuesto].
1.2 WHEN la API facial devuelve una cédula inscrita en el evento THE SYSTEM SHALL registrar la asistencia con cédula, hora, puerta y método "rostro", y mostrar "Bienvenida/o, <nombre>".
1.3 IF la API facial no reconoce el rostro o no responde en 5 s THEN THE SYSTEM SHALL ofrecer en la misma pantalla el QR y la cédula como siguiente paso, sin reiniciar el flujo.
1.4 IF la API devuelve una cédula que no está inscrita en el evento THEN THE SYSTEM SHALL mostrar estado "revisar" con el motivo y permitir al logístico decidir.
1.5 WHEN la persona ya registró ingreso en ese evento por cualquier método THE SYSTEM SHALL mostrar estado ámbar "ya ingresó" con hora y puerta, NOT registrar un segundo ingreso, y permitir al logístico dejarla pasar como reingreso registrando esa decisión.
1.6 IF la API facial responde con validación no exitosa (`est = false`) o con advertencia (`adv = true`) THEN THE SYSTEM SHALL NOT registrar la asistencia aunque la respuesta traiga un documento, y SHALL mostrar al logístico la indicación de la API (`msg`) para repetir la foto.
1.7 IF tras 2 intentos fallidos la validación facial sigue sin ser exitosa THEN THE SYSTEM SHALL ofrecer QR o cédula y NOT pedir un tercer intento.
1.8 IF la API indica más de un rostro en la foto (`cnt` distinto de 1) THEN THE SYSTEM SHALL pedir una foto con una sola persona, porque la API admite una cara por solicitud.
1.9 THE SYSTEM SHALL aceptar una identificación facial solo si `est = true`, `adv = false`, `cnt = 1` y la confianza (`pcr`) es mayor o igual a un umbral configurable (95 [supuesto]).
1.10 WHEN la API devuelve el documento con sufijo de tipo (por ejemplo, "1053846567-C") THE SYSTEM SHALL separar número y tipo de documento y buscar a la persona por ambos.
1.11 IF la persona identificada por rostro consta como menor de edad, o su tipo de documento no está en la lista de tipos de adulto (cédula de ciudadanía, cédula de extranjería, pasaporte [supuesto: `C`, `E`, `P`]; cualquier otro tipo o uno desconocido cuenta como menor) THEN THE SYSTEM SHALL NOT registrar el ingreso por rostro y SHALL pedir QR o documento del acudiente (segunda barrera; la primera es 5.1 y 5.5).

### Requisito 2: Ingreso por QR [MVP]
**Historia:** Como asistente sin rostro registrado, quiero entrar con mi QR, para no depender de la cámara.
_Origen: WB-P2 (problema), WB-P4 (evidencia 3: ~1 de cada 4 sin rostro)_

#### Criterios de aceptación
2.1 WHEN el logístico escanea un QR válido THE SYSTEM SHALL registrar la asistencia con método "QR" y mostrar el resultado en menos de 2 s [supuesto].
2.2 IF el QR no existe, no corresponde al evento o el evento está cerrado THEN THE SYSTEM SHALL mostrar estado rojo con el motivo en lenguaje simple; IF el QR ya fue usado THEN THE SYSTEM SHALL aplicar 1.5.
2.3 THE SYSTEM SHALL generar por inscrito un QR con un código no adivinable (al menos 128 bits), regenerable en el servidor y sin datos personales, y guardar solo su huella (hash).
2.4 WHEN se inscribe una persona a un evento presencial THE SYSTEM SHALL generar su QR y permitir **solo al organizador del evento** descargarlo (individual o todos en un archivo con nombre y QR, sin documento), registrando cada descarga. El envío por correo es Deseable (2.5).
2.5 [Deseable] WHEN el organizador lo pida THE SYSTEM SHALL enviar a cada inscrito con correo su QR por correo electrónico.
2.6 WHEN el organizador rota los QR de una persona o de todo el evento THE SYSTEM SHALL invalidar los anteriores, que en la puerta salen en rojo.

### Requisito 3: Ingreso por documento o cédula [MVP]
**Historia:** Como asistente sin rostro ni QR, quiero entrar con mi documento, para que nadie se quede por fuera.
_Origen: WB-P5 (experiencia, contingencia)_

#### Criterios de aceptación
3.1 WHEN el logístico digita una cédula THE SYSTEM SHALL buscarla entre los inscritos del evento y mostrar el resultado en menos de 2 s [supuesto].
3.2 IF la cédula tiene formato inválido (no son de 5 a 12 dígitos) THEN THE SYSTEM SHALL indicarlo y permitir corregirla; IF tiene formato válido pero no se encuentra THEN THE SYSTEM SHALL mostrar ámbar con la opción "Corregir" primero y "Registrar persona" (6.3) después.
3.3 WHILE el flujo de documento esté activo THE SYSTEM SHALL NOT exigir al asistente ningún dispositivo ni acción distinta de mostrar o decir su número de documento al logístico.

### Requisito 4: Vista del logístico en la puerta [MVP]
**Historia:** Como logístico parado en la entrada, quiero ver quién es la persona y qué hacer, para decidir sin buscar nada.
_Origen: WB-P1 (cliente), WB-P2 (problema)_

#### Criterios de aceptación
4.1 WHEN se identifica a una persona THE SYSTEM SHALL mostrar solo su nombre, el evento y su estado de ingreso (nuevo, o ya ingresó con hora y puerta).
4.2 THE SYSTEM SHALL mostrar un semáforo: verde (pasa y queda registrado), ámbar (el logístico decide) o rojo (no autorizado), con el motivo en una frase de máximo 12 palabras.
4.3 THE SYSTEM SHALL NOT mostrar al logístico diagnósticos, datos de salud ni imágenes del rostro.
4.4 THE SYSTEM SHALL ofrecer botones de acción de al menos 48 px de alto, legibles a pleno sol (contraste mínimo 4,5:1).
4.5 WHEN el logístico confirma o rechaza un caso ámbar THE SYSTEM SHALL registrar quién decidió, qué y cuándo.
4.6 THE SYSTEM SHALL ofrecer dos modos de puerta: "logístico" (celular o tableta en la mano, cámara trasera, el logístico lee el aviso y toca) y "punto fijo" (dispositivo fijo con cámara frontal frente al asistente, el aviso se muestra en pantalla y el asistente toca él mismo "Acepto").
4.7 WHILE un dispositivo esté en modo punto fijo THE SYSTEM SHALL usar una sesión que solo permita validar por rostro y QR, mostrar solo el nombre y el semáforo, impedir navegar a otras pantallas sin el código de supervisor del logístico, abrir la cámara solo después de "Acepto" y apagarla tras la captura o a los 10 s.
4.8 WHEN en punto fijo un caso queda en ámbar THE SYSTEM SHALL mostrar "Espere al logístico, por favor" y enviar el caso al dispositivo del logístico para que decida en máximo 3 s.

### Requisito 5: Consentimiento y alternativa sin biometría [MVP]
**Historia:** Como asistente, quiero decidir si uso mi rostro, para no ser obligado a ello.
_Origen: WB-P5 (privacidad), seguridad.md regla 3_

#### Criterios de aceptación
5.1 WHEN un asistente va a ser validado con el rostro THE SYSTEM SHALL mostrar un aviso de máximo 25 palabras tomado de la autorización de tratamiento de datos (habeas data) de CONFA, con referencia a su política completa, y pedir un toque de aceptación que incluya la confirmación "es mayor de edad", antes de abrir la cámara. En modo logístico lo lee el logístico; en punto fijo lo lee y toca el asistente (4.6).
5.2 IF el asistente no acepta o no es mayor de edad THEN THE SYSTEM SHALL abrir QR o cédula en el mismo toque, sin pasos adicionales.
5.3 WHEN el reconocimiento termina (con o sin éxito) THE SYSTEM SHALL descartar la foto y NOT guardarla en RDS, logs, almacenamiento del dispositivo ni memoria del agente.
5.4 WHILE la persona conste como menor de edad en el paquete o en la inscripción THE SYSTEM SHALL NOT ofrecer reconocimiento facial y SHALL validar con QR o documento del acudiente.
5.5 WHILE el evento esté marcado como dirigido a menores (por ejemplo, preescolar) THE SYSTEM SHALL desactivar la cámara de validación y la foto grupal para todo el evento.
5.6 WHEN un menor ingresa con QR o documento del acudiente THE SYSTEM SHALL registrar la asistencia a nombre del menor, con el documento del acudiente en la decisión.
5.7 WHEN se hace un intento de validación facial THE SYSTEM SHALL registrar la constancia del consentimiento (evento, puerta, logístico, modo, quién aceptó, hora, versión del aviso y resultado), sin imagen, aunque el ingreso no se complete.
5.8 THE SYSTEM SHALL mostrar en el aviso, como mínimo, que CONFA es el responsable, que el rostro se usa solo para validar el ingreso al evento, que es opcional y que existe la alternativa de QR o documento.

### Requisito 6: Eventos sin registro previo [MVP]
**Historia:** Como logístico de un evento abierto, quiero identificar y registrar a quien llega sin inscripción, para no frenar la fila.
_Origen: WB-P2 (problema: eventos sin registro previo)_

#### Criterios de aceptación
6.1 WHEN se crea un evento marcado "sin inscripción previa" THE SYSTEM SHALL aceptar en la puerta a cualquier persona identificada por rostro o cédula en la identidad de CONFA.
6.2 WHEN una persona sin inscripción es identificada THE SYSTEM SHALL registrar su asistencia y agregarla al evento en el momento, en menos de 5 s [supuesto].
6.3 IF la persona no existe en la identidad de CONFA ni en el evento THEN THE SYSTEM SHALL permitir registrarla con cédula, nombre, teléfono y correo (datos mínimos), previa aceptación del tratamiento de datos, y generarle su QR.
6.4 THE SYSTEM SHALL incluir estas asistencias en el panel (8.1) y en el informe (8.3) con los mismos campos que las de eventos con lista.
6.5 IF la persona llega sin estar inscrita en un evento con lista THEN THE SYSTEM SHALL mostrar estado ámbar "no inscrita" y permitir al logístico registrarla en sitio con los mismos datos mínimos o rechazarla.
6.6 IF la API facial identifica un documento que no tiene nombre en la base del evento (la API devuelve solo el documento) THEN THE SYSTEM SHALL mostrar ámbar "Identificado, faltan datos" y abrir el registro en sitio con el documento ya diligenciado y no editable; IF el logístico cambia el documento THEN THE SYSTEM SHALL registrar el ingreso con método "cédula".

### Requisito 7: Funcionamiento sin conexión [MVP]
**Historia:** Como logístico en una sede con mala señal, quiero seguir validando sin internet, para que la fila no se detenga.
_Origen: WB-P2 (consecuencia), WB-P4 (evidencia 7)_

#### Criterios de aceptación
7.1 WHEN el logístico abre un evento con conexión THE SYSTEM SHALL permitir descargar al dispositivo la lista de inscritos y los identificadores de QR del evento.
7.2 WHILE el dispositivo no tenga conexión THE SYSTEM SHALL validar QR y cédula contra la lista descargada y registrar los ingresos localmente.
7.3 WHILE el dispositivo no tenga conexión THE SYSTEM SHALL mostrar un aviso visible "Sin conexión" y el número de ingresos pendientes de envío.
7.4 WHEN regresa la conexión THE SYSTEM SHALL enviar los ingresos pendientes sin intervención del usuario y mostrar cuándo terminó.
7.5 [Deseable] IF una misma persona fue registrada en dos dispositivos sin conexión THEN THE SYSTEM SHALL conservar el ingreso con la hora más temprana del dispositivo, corregida por el desfase de su reloj, y marcar el duplicado para revisión.
7.6 WHILE no haya conexión THE SYSTEM SHALL NOT usar reconocimiento facial (no hay modelo facial local) y SHALL ofrecer QR y cédula como métodos de validación.
7.7 THE SYSTEM SHALL cifrar la lista descargada con una clave protegida por un PIN de 6 dígitos que define el propio logístico al descargarla y que nunca sale del dispositivo, pedir el PIN al abrir la puerta y tras 15 minutos sin uso, y borrarla al cerrar el evento, al vencer su caducidad (comprobada al abrir la aplicación) o tras 5 PIN fallidos.
7.8 [Deseable] IF, sin conexión, la cédula digitada no está en la lista descargada THEN THE SYSTEM SHALL permitir registrar a la persona localmente como "no inscrita" con cédula, nombre, teléfono y correo, y enviarla al volver la conexión.

### Requisito 8: Panel en vivo y consolidación [MVP]
**Historia:** Como organizador, quiero saber quién entró y quién falta, para cerrar el evento sin transcribir listados.
_Origen: WB-P2 (problema), WB-P4 (métricas)_

#### Criterios de aceptación
8.1 WHILE el evento esté abierto THE SYSTEM SHALL mostrar entradas, total esperado, faltantes, porcentaje y desglose por método (rostro, QR, cédula; virtual cuando exista el Requisito 15) con actualización en menos de 5 s [supuesto].
8.2 WHEN el organizador pregunta quién falta, opcionalmente filtrando por empresa, THE SYSTEM SHALL listar los inscritos sin ingreso.
8.3 WHEN el organizador cierra el evento THE SYSTEM SHALL generar el informe de asistencia (nombre, documento enmascarado, empresa, estado, método, hora y puerta; sin teléfono ni correo) descargable en CSV en menos de 10 s [supuesto], con las celdas que empiezan por `= + - @` neutralizadas, por un enlace que vence a los 5 minutos.
8.4 THE SYSTEM SHALL calcular y mostrar el tiempo promedio de ingreso por asistente, por método, para medir la mejora.
8.5 WHILE el evento esté cerrado THE SYSTEM SHALL rechazar nuevos ingresos con estado rojo "El evento ya está cerrado".

### Requisito 9: Crear evento e inscribir asistentes [MVP]
**Historia:** Como organizador, quiero crear el evento y cargar a mis invitados, para que la puerta tenga a quién validar.
_Origen: WB-P5 (experiencia, "Antes"), reto: creación e inscripción_

#### Criterios de aceptación
9.1 WHEN el organizador describe el evento (nombre, fecha, sede, aforo, tipo) THE SYSTEM SHALL crearlo y mostrarlo en la lista de eventos.
9.2 WHEN el organizador carga un archivo CSV (UTF-8, separado por comas o punto y coma, máximo 10.000 filas y 2 MB) con las columnas `tipo_doc` (opcional, por defecto C), `numero_doc`, `nombre`, `empresa` (opcional) y `correo` (opcional) THE SYSTEM SHALL validarlo (incluido rechazar campos que empiecen por `= + - @`), quitar duplicados, informar cada fila con error y su motivo, y registrar las válidas sin sobrescribir los datos de personas ya existentes. THE SYSTEM SHALL ofrecer una plantilla descargable.
9.3 THE SYSTEM SHALL soportar en el MVP los tipos de evento externo e interno en modalidad presencial; el tipo individual administrado por CONFA (pasadía) y las modalidades virtual e híbrida son Deseables (9.6 y Requisito 15).
9.4 IF un ingreso supera el cupo del evento THEN THE SYSTEM SHALL mostrar estado ámbar "Se superó el cupo" y registrar el ingreso solo si el logístico asignado lo autoriza, dejando la decisión registrada.
9.5 IF un ingreso supera el aforo de la sede THEN THE SYSTEM SHALL mostrar estado rojo "Aforo de la sede completo" y NOT permitir el ingreso, aunque dos puertas validen al mismo tiempo; este límite es de seguridad y nadie lo puede saltar desde la aplicación. WHILE no haya conexión THE SYSTEM SHALL aplicar un tope local por dispositivo y, al alcanzarlo, mostrar rojo "Verifique el aforo con el coordinador".
9.6 [Deseable] THE SYSTEM SHALL soportar eventos individuales administrados por CONFA (pasadías), sin inscripción previa.
9.7 WHILE la asistencia llegue al 90 % del cupo THE SYSTEM SHALL mostrar un aviso en el panel del organizador.

### Requisito 10: Marcado masivo por foto grupal [Deseable]
**Historia:** Como organizador de un evento interno, quiero marcar la asistencia de todo un auditorio con una foto, para no llamar a lista.
_Origen: reto (caso "Encuentro con el Director")_

#### Criterios de aceptación
10.1 WHEN el logístico toma una foto grupal en un evento con inscripción previa THE SYSTEM SHALL detectar los rostros, enviarlos uno a uno a la API facial y marcar la asistencia solo de los identificados que dieron consentimiento de foto grupal al inscribirse.
10.2 WHEN termina el proceso THE SYSTEM SHALL mostrar cuántos fueron marcados, cuántos rostros no se reconocieron y cuántos se descartaron por falta de consentimiento o por ser menores.
10.3 THE SYSTEM SHALL NOT guardar la foto grupal ni los recortes tras el procesamiento.
10.4 WHEN el logístico va a tomar la foto grupal THE SYSTEM SHALL mostrar un aviso para leer en voz alta que invite a quien no quiera salir en la foto a retirarse del encuadre y validar con QR o cédula.
10.5 IF el evento no tiene inscripción previa o está dirigido a menores THEN THE SYSTEM SHALL NOT ofrecer la foto grupal.
10.6 WHEN la persona se inscribe a un evento interno THE SYSTEM SHALL pedirle, por separado y de forma opcional, el consentimiento de foto grupal.

### Requisito 11: Consultas y reportes en lenguaje natural por texto [MVP]
**Historia:** Como organizador o logístico, quiero preguntar en mis palabras ("¿cuántos han entrado?", "¿quién falta de Arquitectos S.A.?", "hazme el reporte de asistencia"), para obtener datos y reportes sin navegar pantallas.
_Origen: WB-P1 (cliente), WB-P5 (experiencia, "Durante y al cierre"), complemento "consultas y reportería"_

#### Criterios de aceptación
11.1 WHEN el usuario pregunta por texto sobre la asistencia del evento THE SYSTEM SHALL responder en pantalla en menos de 5 s en el percentil 90 [supuesto], con cifras tomadas de los datos.
11.2 WHEN el usuario pide un reporte en lenguaje natural THE SYSTEM SHALL generar el mismo informe de asistencia de 8.3 y ofrecer su descarga.
11.3 IF la intención es ambigua o la pregunta no es sobre el evento THEN THE SYSTEM SHALL pedir aclarar o decir que no puede ayudar con eso, sin ejecutar ninguna acción.
11.4 THE SYSTEM SHALL responder solo con datos del evento asignado y del rol del usuario, sin documentos, teléfonos, correos ni datos de salud, y NOT permitir que una consulta modifique asistencia, eventos ni aprobaciones.
11.5 WHEN el usuario pregunta por una persona ("¿ya entró Ana Gómez?") THE SYSTEM SHALL responder si ingresó, a qué hora y por qué canal, con máximo 5 coincidencias por nombre.
11.6 WHEN el usuario hace una pregunta que depende de la anterior ("¿y de la empresa Y?") THE SYSTEM SHALL resolverla con el contexto de la misma conversación.
11.7 IF el dato no está disponible en las herramientas THEN THE SYSTEM SHALL decirlo y NOT estimarlo.
11.8 WHEN el usuario pregunta por novedades ("¿cuántos se registraron en sitio?", "¿hay casos por revisar?") THE SYSTEM SHALL responder solo con conteos (registros en sitio, reingresos, ingresos con cupo superado, rechazos e ingresos marcados para revisión), sin datos de contacto.

### Requisito 12: Solicitud y aprobación de eventos externos [Deseable, añadido]
**Historia:** Como empresa afiliada, quiero pedir una sede y saber si está disponible, para organizar mi evento; y como aprobador de CONFA, quiero aceptar o rechazar, para controlar la ocupación.
_Origen: WB-P1 (cliente secundario, añadido)_

#### Criterios de aceptación
12.1 WHEN la empresa consulta una fecha THE SYSTEM SHALL mostrar las sedes disponibles y ocupadas ese día.
12.2 WHEN la empresa envía la solicitud THE SYSTEM SHALL dejarla en estado "pendiente" y notificar al aprobador.
12.3 WHEN el aprobador acepta, rechaza o propone otra fecha THE SYSTEM SHALL notificar a la empresa y registrar quién decidió, qué y cuándo.
12.4 IF dos solicitudes piden la misma sede y fecha THEN THE SYSTEM SHALL NOT aprobar ambas automáticamente.
12.5 THE SYSTEM SHALL NOT permitir que la decisión la tome un agente de IA; solo una persona aprueba.

### Requisito 13: Seguridad, privacidad y trazabilidad [MVP]
**Historia:** Como CONFA, quiero cumplir la Ley 1581 de 2012, para proteger a los asistentes.
_Origen: seguridad.md (reglas 1 a 10)_

#### Criterios de aceptación
13.1 THE SYSTEM SHALL guardar solo: de la persona, documento, nombre y, si se registró en sitio, teléfono y correo; de cada ingreso, método, canal, hora, puerta, logístico y tiempo de validación; de cada intento facial, la constancia de 5.7. THE SYSTEM SHALL NOT guardar imágenes, plantillas biométricas ni la confianza del reconocimiento por persona.
13.2 THE SYSTEM SHALL devolver a cada rol solo los datos que puede ver; el diagnóstico nunca sale de la base de datos hacia el logístico ni el aprobador.
13.3 THE SYSTEM SHALL leer todas las credenciales (API facial, base de datos, claves) de Secrets Manager o de roles de IAM, y NOT tenerlas en el código, en el repositorio ni en el navegador.
13.4 WHEN un usuario del personal ingresa con una cuenta creada por un administrador de CONFA THE SYSTEM SHALL autenticarlo y darle acceso solo a los eventos que tiene asignados y, en cada uno, a las acciones de los roles que tiene en ese evento (organizador, logístico, punto fijo; puede tener varios), identificándolo por su identificador inmutable de cuenta y no por su correo; IF pide datos de otro evento THEN THE SYSTEM SHALL responder 403.
13.5 THE SYSTEM SHALL registrar quién hizo qué y cuándo en: decisiones ámbar, registro en sitio, reingreso, cupo superado, confirmación de eventos, asignación de roles, aprobación de sedes, descarga del paquete offline, descarga y rotación de QR y exportación del informe; y NOT permitir modificar ni borrar esos registros.
13.6 THE SYSTEM SHALL usar HTTPS en tránsito, cifrado en reposo, y borrar cada dato al cumplir su retención (ingresos y personas registradas en sitio: 90 días tras el evento [supuesto]; registros de trazabilidad y constancias de consentimiento: 1 año [supuesto]; memoria del agente: 3 días; logs: 30 días).
13.7 WHEN el texto de un usuario contenga un número de documento (con o sin puntos, espacios o sufijo de tipo) THE SYSTEM SHALL reemplazarlo antes de enviarlo al modelo, y THE SYSTEM SHALL enmascararlo en logs y en las respuestas del modelo.
13.8 THE SYSTEM SHALL usar solo datos ficticios o los entregados por CONFA para el evento. La API facial es solo de producción: las pruebas automáticas usan siempre el mock y fallan si se configura la API real; la API real se usa a mano, con un máximo de 1 petición por segundo aplicado en la entrada de la API, y mientras el aviso sea un borrador solo con documentos del equipo que lo autoricen.
13.9 WHEN un logístico asignado inicia sesión THE SYSTEM SHALL mostrar la puerta de su evento en máximo 2 toques y mantener la sesión hasta el cierre del evento, con un máximo de 12 horas.
13.10 WHEN un logístico tiene varios eventos asignados el mismo día THE SYSTEM SHALL permitirle elegir el evento al entrar y tener un paquete offline por evento.
13.11 IF un organizador intenta asignar en un evento un rol distinto de logístico o punto fijo, o asignar roles en un evento que no es suyo THEN THE SYSTEM SHALL responder 403.
13.12 THE SYSTEM SHALL enviar las respuestas con datos personales con la indicación de no guardarlas en la caché del navegador, y NOT guardar datos personales en la caché del service worker.

### Requisito 14: Usabilidad para quien no conoce la tecnología [MVP]
**Historia:** Como asistente sin conocimiento de tecnología, quiero entrar sin instalar ni aprender nada, para no sentirme excluido.
_Origen: WB-P1 (cliente), complemento (asistente sin tecnología)_

#### Criterios de aceptación
14.1 THE SYSTEM SHALL permitir que el asistente entre sin instalar una aplicación ni crear una cuenta.
14.2 THE SYSTEM SHALL mostrar mensajes en español, de máximo 15 palabras, sin términos técnicos (sin "error", "token", "API", "HTTP") y con trato cálido.
14.3 WHEN un asistente tenga dificultades THE SYSTEM SHALL permitir al logístico completar el ingreso con la cédula en máximo 3 toques.
14.4 THE SYSTEM SHALL permitir al logístico iniciar una validación (rostro, QR o cédula) con un solo toque desde la pantalla principal.

### Requisito 15: Eventos virtuales e híbridos [Deseable]
**Historia:** Como organizador, quiero que mi evento pueda ser virtual o híbrido, para contar la asistencia de quienes entran en persona y de quienes se conectan.
_Origen: WB-P2 (problema: asistencia virtual no consolidada), WB-P5 (experiencia 5.1e)_

#### Criterios de aceptación
15.1 WHEN el organizador crea un evento THE SYSTEM SHALL pedir la modalidad: presencial, virtual o híbrida.
15.2 WHEN el evento es virtual o híbrido THE SYSTEM SHALL aceptar el enlace de la reunión (Teams, Zoom u otro) y mostrarlo a los inscritos sin alojar la transmisión.
15.3 WHEN un inscrito se conecta THE SYSTEM SHALL registrar su asistencia virtual al confirmar su cédula en una página con enlace personal único, sin instalar nada.
15.4 THE SYSTEM SHALL NOT aplicar reconocimiento facial a la asistencia virtual.
15.5 WHILE el evento sea híbrido THE SYSTEM SHALL consolidar en un solo panel e informe la asistencia presencial y virtual, con el canal de cada persona.
15.6 IF una persona registra asistencia presencial y virtual en el mismo evento THEN THE SYSTEM SHALL contarla una sola vez y conservar ambos registros.
15.7 IF el evento es virtual THEN THE SYSTEM SHALL NOT exigir puertas, QR de ingreso ni modo sin conexión.
15.8 IF la cédula no coincide con la del enlace personal THEN THE SYSTEM SHALL mostrar un mensaje genérico sin revelar el nombre, y bloquear el enlace tras 5 intentos fallidos.

### Requisito 16: Crear eventos con lenguaje natural [Deseable]
**Historia:** Como organizador, quiero describir mi evento en una frase, para crearlo sin llenar un formulario largo.
_Origen: WB-P5 (experiencia, "Antes", paso 1: "el organizador describe el evento en una frase"), idea del equipo (propuesta de solución)_

#### Criterios de aceptación
16.1 WHEN el organizador describe el evento por texto o voz (por ejemplo, "Encuentro de afiliados de Arquitectos S.A., sábado 9 a. m., La Rochela, 300 personas, híbrido") THE SYSTEM SHALL proponer un borrador con nombre, fecha, hora, sede, tipo, modalidad, cupo e inscripción previa en menos de 8 s [supuesto].
16.2 WHEN la descripción usa fechas relativas ("el sábado", "mañana") THE SYSTEM SHALL resolverlas con la fecha actual en la zona horaria de Colombia (America/Bogota) y mostrar la fecha calculada en el borrador.
16.3 IF falta un dato obligatorio o es ambiguo (sede inexistente, hora sin a. m. o p. m., modalidad virtual sin enlace) THEN THE SYSTEM SHALL preguntar por ese dato y NOT inventarlo.
16.4 WHEN se genera el borrador THE SYSTEM SHALL mostrarlo en el mismo formulario del requisito 9, editable, y crear el evento solo cuando la persona confirme.
16.5 THE SYSTEM SHALL validar el borrador con las mismas reglas del formulario (fecha no pasada, sede existente, cupo mayor que cero y no mayor que el aforo de la sede, modalidad válida, enlace si es virtual o híbrido) antes de permitir confirmarlo.
16.6 THE SYSTEM SHALL NOT crear, modificar ni eliminar eventos sin confirmación humana, ni inscribir personas a partir de la descripción.
16.7 IF la sede pedida ya tiene un evento confirmado en esa fecha THEN THE SYSTEM SHALL avisarlo en el borrador antes de la confirmación.

### Requisito 17: Consultas por voz [Deseable]
**Historia:** Como logístico con las manos ocupadas, quiero hacer las consultas del Requisito 11 hablando, para no teclear.
_Origen: complemento "voz" del equipo_

#### Criterios de aceptación
17.1 WHEN el usuario hace por voz una consulta del Requisito 11 THE SYSTEM SHALL transcribirla, responder en pantalla y leer la respuesta en voz alta en menos de 7 s en el percentil 90 [supuesto].
17.2 IF la transcripción tiene baja confianza THEN THE SYSTEM SHALL pedir repetir o escribir, sin ejecutar nada.
17.3 THE SYSTEM SHALL procesar el audio dentro de la cuenta AWS del evento y NOT guardarlo.
17.4 THE SYSTEM SHALL NOT identificar personas por su huella de voz.

## Fuera de alcance
- Pagos y venta de boletería.
- Integración con sistemas de CONFA distintos de la API facial y la RDS del evento.
- Identificación de personas por su voz (biometría de voz) y cédula dicha en voz alta al sistema.
- Reconocimiento de varios rostros por video: la API facial admite un rostro por solicitud; el caso masivo se cubre con foto grupal (Req 10).
- Registro de salidas y control de reingresos más allá de la decisión del logístico (1.5).
- Reconocimiento facial sin conexión (no hay modelo local).
- Datos del asistente en la puerta más allá de nombre, evento y estado de ingreso (empresa, categoría, acompañantes): fase posterior.
- Reconocimiento facial de menores de edad.
- Aprobación automática de eventos por un agente de IA.
- Aplicación nativa instalable para el asistente.
- Alojar o transmitir la reunión virtual, y verificar presencia real durante la sesión (solo se registra la conexión inicial).

## Matriz de trazabilidad
| Pregunta Working Backwards | Requisitos |
|---|---|
| P1 Cliente (asistente, logístico; añadido: empresa y aprobador) | 4, 11, 12, 13.9, 14, 17 |
| P2 Problema (identificación, fila, papel, sin registro previo, sin internet, virtual sin consolidar) | 1, 2, 3, 6, 7, 8, 15 |
| P3 Beneficio (ingreso en segundos, con o sin internet) | 1, 2, 3, 7, 11 |
| P4 Evidencia y métricas | 2, 7, 8.4 |
| P5 Experiencia (con contingencia y privacidad) | 1, 2, 3, 5, 9, 10, 15, 16 |
| Seguridad (seguridad.md) | 1.6–1.11, 5, 10.1–10.6, 11.4, 12.5, 13, 15.8, 16.6, 17.3 |

## Casos de uso del reto
| Caso | Cobertura | Prioridad |
|---|---|---|
| Con inscripción previa (afiliados o empresas) | 1, 2, 3, 9 | MVP |
| Interno sin registro ("Encuentro con el Director") | 6 (cédula o rostro uno a uno, varias puertas) | MVP |
| Interno masivo con foto grupal | 10 | Deseable |
| Externo por documento (preescolar) | 3, 5.4–5.6, 6.3 | MVP |
| Individual administrado por CONFA (pasadía) | 9.6 | Deseable |
| Virtual e híbrido (complemento del equipo, WB §5.1e) | 15 | Deseable |

## Requisitos funcionales oficiales del reto
| Requisito oficial | Criterio | Prioridad |
|---|---|---|
| Reconocimiento facial como motor principal: 1 a 1 | 1.1, 1.6–1.11 | MVP |
| Reconocimiento facial: varios rostros por foto | 10.1 (en el MVP el caso masivo se atiende 1 a 1 en varias puertas o puntos fijos) | Deseable |
| Creación del evento | 9 (formulario); 16 (lenguaje natural) | MVP; Deseable |
| Contingencia para no enrolados: QR u otro método | 1.3, 2, 3 | MVP |
| Control de acceso y consolidación en tiempo real | 8.1, 8.3 | MVP |
| Acceso rápido y seguro del personal logístico | 13.4, 13.9, 13.10, 14.4 | MVP |
| No guardar imágenes | 5.3, 13.1 | MVP |
