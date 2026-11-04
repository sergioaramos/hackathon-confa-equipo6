# Working Backwards — Reto 1: experiencia y control de eventos

> BORRADOR v4 (4 nov 2026). **Núcleo:** que el asistente entre rápido y que CONFA lo reconozca. **Añadido (no es el núcleo):** que empresas externas soliciten eventos y CONFA los apruebe. Lo marcado [supuesto] se valida en el kickoff. Lo marcado **(Deseable)** no está en el MVP de la demo; el alcance vigente está en `.kiro/specs/pase-confa/requirements.md`.

## Reto
Centralizar y digitalizar el ciclo de vida de los eventos de CONFA. El foco es el control de acceso en sitio (con o sin internet), con reconocimiento de la persona y consolidación de asistencia en tiempo real. La solicitud y aprobación de eventos externos se suma como complemento.

## Tipos de evento (los tres casos de uso)
| Tipo | Quién lo organiza | Ejemplo | Cómo se entra | Prioridad |
|---|---|---|---|---|
| Externo | Empresa afiliada, en una sede de CONFA (la solicitud de sede es Deseable) | Encuentro de Arquitectos S.A. en La Rochela | Cara, QR o documento | MVP |
| Interno | Un área de CONFA | "Encuentro con el Director" | Cara, QR o documento uno a uno; foto grupal (Deseable) | MVP |
| Individual administrado por CONFA | CONFA | Pasadía en un centro recreacional | Cara (identidad ya existente), QR o documento | Deseable |
| Virtual o híbrido | Cualquiera de los anteriores | Charla en línea, o evento presencial con transmisión | Virtual: enlace personal y cédula. Híbrido: presencial más virtual en un solo informe | Deseable |

## 1. Cliente
- **Principal (junto): el asistente y el logístico en la puerta.** El **asistente** (empleado de la empresa, afiliado, familia en un pasadía) hace fila al sol y quiere entrar rápido. **Puede no tener conocimiento de tecnología**: no sabe instalar una app ni mostrar un QR. Uno de cada cuatro no tiene el rostro registrado y puede no tener internet. El **logístico parado en la entrada** necesita reconocerlo y saber qué hacer, sin buscar nada. Quien organiza (empresa afiliada o área de CONFA) es el mismo que gestiona la puerta en sus eventos.
- **Secundario (añadido): la empresa afiliada que solicita un evento y el aprobador de CONFA** que acepta la reserva según disponibilidad.

## 2. Problema
**El mayor problema es la identificación de la persona**, ya sea de forma masiva (cientos en minutos) o individual (una familia en un pasadía). Todo lo demás (fila, papel, consolidación) nace de que identificar a alguien hoy es buscarlo a mano. El logístico en la puerta no tiene a la mano quién es la persona, a qué evento tiene derecho ni si ya entró.
También **hay eventos virtuales e híbridos**: quien se conecta en línea no pasa por ninguna puerta, y hoy su asistencia se cuenta aparte o no se cuenta, así que la asistencia total de un evento híbrido no se puede consolidar.
Además, **hay eventos sin registro previo** (por ejemplo, entrada abierta a afiliados o a quienes se presenten ese día): no existe lista contra la cual validar, y hay que identificar y registrar a la persona en el momento.

**Para el asistente:** filas largas, bajo calor, para entrar a un evento al que fue invitado. En un pasadía, esa espera le quita tiempo de disfrute.
**Para el logístico:** valida a cada persona a mano en un listado de papel (30–40 s cada una), sin saber cuántos han entrado, y al final transcribe para consolidar.
**Añadido, para quien solicita el evento y para CONFA:** pedir una sede implica preguntar por disponibilidad y esperar respuesta, sin una vista única de disponibilidad ni de solicitudes.

**Consecuencias:**
- Evento masivo de ~6.000 asistentes: ~9,7 h de flujo repartido en 6 puertas.
- Horas de consolidación manual al cierre.
- Papel impreso en cada evento.
- Si falla internet en el sitio, hoy la única alternativa es el papel.

| Cifra | Etiqueta | Fuente |
|---|---|---|
| 30–40 s por asistente con listado manual | [vendor] | Fielddrive, referencia del sector |
| ~6.000 asistentes por evento masivo | [oficial] | Informe de Gestión 2025: 12.086 asistentes en 2 eventos de La Rochela |
| ~9,7 h de flujo con 6 puertas | [supuesto] | 6.000 × 35 s ÷ 6 puertas |
| Horas de consolidación | [supuesto] | Validar en el kickoff |

## 3. Beneficio principal
**Ingreso en segundos, con o sin internet:** el logístico sabe quién es cada persona en segundos y la deja entrar, ya sea con su cara, su QR o su documento, tenga o no registro previo, sin buscarla en papel. Solicitar eventos, administrar y consolidar son complementos que apoyan ese beneficio; no son beneficios separados.

Cómo se reflejan los demás atributos que pidió el equipo (son criterios de diseño, no beneficios):
| Atributo | Traducción medible |
|---|---|
| Tiempos | Segundos por asistente; minutos de fila |
| Gestión y administración | Solicitud, aprobación y asistencia en un solo lugar; sin listados |
| Disponibilidad | La puerta sigue validando sin internet y sincroniza al reconectar |
| Usabilidad | El personal opera con un toque; el organizador pregunta en lenguaje natural; crear un evento con una frase es Deseable |
| Innovación | Rostro como llave de entrada sobre la identidad que CONFA ya tiene |

## 4. Evidencia
| # | Evidencia | Etiqueta | Qué prueba |
|---|---|---|---|
| 1 | El enunciado reconoce "cuellos de botella, filas, papel y listados manuales" y que el personal "no siempre accede de forma rápida y segura" a la plataforma en sitio | [oficial] | Que el dolor existe |
| 2 | Identidad digital biométrica de 268.724 personas y reconocimiento facial en los centros recreacionales (Informe 2025) | [oficial] | Que la solución se apoya en algo que CONFA ya opera, incluidos los pasadías |
| 3 | ~75 % de cobertura (268.724 / 356.123) → ~1 de cada 4 usará QR o documento | [oficial + cálculo] | Que la alternativa es un flujo principal |
| 4 | 44 eventos empresariales; 12.086 asistentes en 2 eventos masivos; 15.803 usos en eventos y bienestar (Informe 2025) | [oficial] | Que el problema se repite |
| 5 | Listado manual 30–40 s [vendor: Fielddrive, referencia del sector]; Fielddrive publica registros de unos 6 s por persona con su sistema ([fielddrive.com](https://www.fielddrive.com/blog/event-attendance-tracker-methods)); QR 15–20 s y facial 3–10 s [supuesto: rangos del sector sin una fuente única verificada; se reemplazan por la medición de la demo] | [vendor] + [supuesto] | Orden de magnitud de la mejora |
| 6 | Las empresas afiliadas preguntan disponibilidad, reservan y CONFA acepta | [equipo, conocimiento del proceso] | Que existe el flujo de solicitud y aprobación |
| 7 | El asistente puede no tener internet en el sitio | [equipo] | Que el modo sin conexión es requisito, no extra |
| 8 | CONFA realiza eventos virtuales e híbridos además de presenciales | [equipo] | Que la asistencia debe consolidarse por canal; validar en el kickoff |
| 9 | Preguntas a mentores de CONFA en el kickoff (duración de ingreso, puertas, consolidación, conectividad en sedes) | [kickoff] | Convierte supuestos en datos |

## 5. Experiencia

### 5.1 Organizador (empresa afiliada o área de CONFA)
> Los pasos 1 a 3 de "Antes" (solicitud de sede y aprobación) son el **añadido**: no bloquean el núcleo. El núcleo empieza en el paso 4 y en "El día del evento"; si el evento ya existe, se crea directamente.

**Antes**
1. **(Deseable)** Escribe "Encuentro de afiliados, sábado 9 a. m., La Rochela, 300 personas" y el sistema arma el borrador del evento; ve qué sedes están disponibles ese día. En el MVP, el organizador llena el formulario del evento.
2. **(Deseable)** Elige la sede y envía la solicitud. Si es un evento interno de CONFA, se crea directamente.
3. **(Deseable)** CONFA aprueba (o propone otra fecha). El organizador recibe el aviso y el evento queda confirmado.
4. Carga a los invitados con la plantilla CSV y descarga sus QR para compartirlos (por ejemplo, por WhatsApp o impresos). Se sugiere guardar el QR en el celular para usarlo sin internet. El envío por correo es Deseable.

**El día del evento**
5. Abre el evento desde su celular o tableta con acceso rápido y seguro. Antes de salir, descarga la lista del evento al dispositivo.
6. En la puerta, el logístico lee un aviso corto y el asistente acepta con un toque; mira la cámara y en ~4–5 s, incluido ese toque, aparece "Bienvenida, Ana Gómez". Si no lo reconoce o prefiere no usar el rostro, muestra el QR (sirve sin internet). Sin QR, se digita la cédula.
7. Sin conexión, el dispositivo valida contra la lista descargada y guarda los ingresos. Al volver la señal, sincroniza solo, y la pantalla avisa "N ingresos pendientes de enviar".
8. Pregunta "¿cuántos han entrado y quién falta?" y recibe la respuesta al instante. Sin conexión, el asistente no está disponible y la pantalla de la puerta muestra el conteo local de ese dispositivo.

**Al cierre**
9. El informe de asistencia está listo; no hay nada que transcribir.

### 5.1b Lo que ve el logístico de cada persona
Al identificar a alguien, la pantalla muestra en una sola vista, por ahora solo lo mínimo: nombre, evento y si ya ingresó (hora y puerta), más una señal clara: verde pasa, ámbar revisar, rojo no autorizado, con el motivo en palabras simples. **Nunca** muestra diagnósticos ni datos de salud.

### 5.1c Eventos sin registro previo y personas no inscritas
1. El organizador crea el evento marcándolo como "sin inscripción previa".
2. En la puerta, el sistema identifica a la persona con su rostro o su cédula contra la identidad que CONFA ya tiene.
3. Si es afiliada o conocida, se registra la asistencia en ese momento. Si no existe, el logístico la registra con cédula, nombre, teléfono y correo (con su consentimiento) en unos pocos toques, y se le genera su QR.
4. Si el evento tiene lista y llega alguien no inscrito, aparece en ámbar "no inscrita" y el logístico decide registrarla o rechazarla. **(Deseable)** Sin internet, el registro queda guardado y se envía al volver la señal.
5. Si el rostro identifica a alguien cuyo nombre no está en la base (la API facial solo devuelve el documento), aparece en ámbar "Identificado, faltan datos" y se abre el registro con el documento ya diligenciado.
6. La asistencia se consolida igual que en un evento con lista.

### 5.1d Consultas y reportes en lenguaje natural (texto; voz como Deseable)
- El organizador o el logístico preguntan en sus palabras: "¿cuántos han entrado?", "¿quién falta de Arquitectos S.A.?", "¿ya entró Ana Gómez?", "hazme el reporte de asistencia". El sistema responde en pantalla y, con voz, también en voz alta.
- Solo consulta: no cambia la asistencia ni aprueba nada.
- La voz es una *interfaz*, no una biometría. Identificar a una persona por su voz queda fuera de alcance. Ver pregunta abierta 9.

### 5.1e Eventos virtuales e híbridos (Deseable)
1. Al crear el evento, el organizador elige presencial, virtual o híbrido, y pega el enlace de la reunión (Teams, Zoom u otro) si aplica.
2. Cada inscrito recibe un enlace personal. Al conectarse, confirma su cédula en una página sencilla, sin instalar nada ni usar el rostro, y su asistencia queda registrada.
3. En un evento híbrido, el panel muestra en un solo lugar cuántos entraron en persona y cuántos se conectaron, y si alguien hizo ambas cosas se cuenta una sola vez.
4. El informe final trae la asistencia presencial y virtual consolidada.

### 5.2 Asistente
1. Si está inscrito, recibe del organizador su QR (por WhatsApp, impreso o, como Deseable, por correo) y el aviso de privacidad. **(Deseable)** En eventos internos puede aceptar, aparte, salir en la foto grupal. Si no tiene conocimiento de tecnología, no necesita hacer nada antes: llega, muestra su cédula o mira la cámara.
2. En la puerta, el logístico le lee un aviso corto y le pregunta si acepta usar su rostro; en un punto fijo, el asistente lee el aviso en la pantalla y toca "Acepto" él mismo. Puede aceptar o elegir QR o documento: es un derecho, no un castigo. A los menores no se les aplica reconocimiento facial.
3. El logístico lo guía; él solo mira la cámara o muestra su documento. Sin internet, el rostro no está disponible: se valida con QR o cédula.
4. Ve "Bienvenida" y pasa. **(Deseable)** En un pasadía, la misma validación le sirve para entrar al centro recreacional.

### 5.3 Aprobador de CONFA (Deseable, fuera de la demo)
1. Ve las solicitudes pendientes con fecha, sede, aforo y calendario de disponibilidad.
2. Aprueba, rechaza o propone otra fecha. Queda registrado quién aprobó qué y cuándo.

**Privacidad:** consentimiento antes de usar el rostro. La foto nunca se guarda: solo la cédula y la hora. A los niños no se les aplica reconocimiento facial; valida el QR o el documento del acudiente. El aprobador no ve datos sensibles de los asistentes.

### 5.4 Mockups del organizador
Versión visual en el artefacto "Mockups organizador v2" de la sesión (crear evento con modalidad, puerta con persona identificada y no inscrita, panel híbrido, sin internet). En el MVP, la modalidad es solo presencial y la foto grupal, la solicitud de sede y el panel híbrido son Deseables. El esquema ASCII siguiente es la primera versión de tres pantallas, ajustada al MVP:

```
[1] Crear evento (la disponibilidad de sedes es Deseable)
+------------------------------------------+
| Nuevo evento                             |
| "Encuentro de afiliados, sábado 9 a. m., |
|  La Rochela, 300 personas"       [Crear] |
| ---------------------------------------- |
| Sede        Fecha     Disponibilidad     |
| La Rochela  sáb 7 nov  ● Disponible      |
| Sede Centro sáb 7 nov  ○ Ocupada         |
|                       [Enviar solicitud] |
+------------------------------------------+

[2] Panel en vivo (puerta)
+------------------------------------------+
| Encuentro de afiliados     ● En línea    |
| Entraron 212 / 300    Faltan 88          |
| [=========>     ] 71 %                   |
| Última entrada: Ana Gómez  3 s           |
| Rostro 74 %  QR 21 %  Cédula 5 %         |
| [Rostro]  [Escanear QR]  [Cédula]        |
+------------------------------------------+

[3] Puerta sin internet
+------------------------------------------+
| ⚠ Sin conexión: validando en el equipo   |
| 18 ingresos pendientes de enviar         |
| Lista descargada: 300 invitados          |
| [Escanear QR]  [Cédula]                  |
+------------------------------------------+
```

## Comunicado de prensa
# CONFA lanza "Pase CONFA" para que entrar a sus eventos tome segundos, con o sin internet
*Manizales, 4 de noviembre de 2026.* Desde hoy, quien llega a un evento de CONFA es reconocido y entra en segundos, y el logístico de la puerta ve de inmediato quién es y qué hacer. Antes, cada persona tomaba entre 30 y 40 segundos mientras la fila crecía bajo el sol y nadie sabía con certeza quién había entrado hasta transcribir los listados. Ahora, el asistente acepta con un toque, mira la cámara y en unos segundos aparece su bienvenida; si no tiene su rostro registrado o prefiere no usarlo, muestra su código QR, aun sin conexión a internet, y quien no lo tiene se valida con su documento. Quien llega sin estar inscrito se registra en el momento. El organizador pregunta cuántos han entrado y quién falta y recibe la respuesta al instante, y al cerrar el evento el informe de asistencia ya está listo. Próximamente, la misma validación llegará a los pasadías de los centros recreacionales, a los eventos virtuales e híbridos y a la solicitud de sedes por parte de las empresas afiliadas.
"Antes la fila le daba la vuelta al parqueadero; ahora la gente pasa casi sin detenerse", cuenta Carolina, auxiliar de logística en La Rochela. *(Cita ilustrativa; reemplazar por una frase real del kickoff.)*
En su primer evento masivo, el tiempo total de ingreso se redujo cerca de un 70 % *(estimado con 6 puertas y tiempos de referencia del sector)*.

## Métricas y supuestos
| Métrica | Antes | Después | Supuesto |
|---|---|---|---|
| Tiempo por asistente | 30–40 s [vendor] | ~4–5 s facial con el toque de consentimiento (diseño); el modelo usa 8 s, conservador; 15–20 s QR [vendor] | 75 % facial (techo: cobertura biométrica), 25 % QR |
| Flujo de ingreso, evento de 6.000 | ~9,7 h | ~2,9 h (−70 %) | 6 puertas; promedio ponderado ~10,4 s (8 s facial, 17,5 s QR) |
| Horas-persona del personal en la puerta | ~58 h | ~17 h (−41 h) | 1 persona por puerta cada instante; 6.000 × 35 s vs 6.000 × 10,4 s |
| Valor del tiempo del personal ahorrado | — | ~$0,6 M COP por evento masivo | [supuesto] $15.000 COP/h; validar costo real |
| Consolidación de asistencia | Horas [supuesto] | Inmediata | Validar en el kickoff |
| Papel | Listados impresos | 0 | — |
| % validados sin buscar en papel | 0 % | ~75 % como techo (cobertura biométrica); menos en eventos con menores, sin consentimiento o sin internet, que van por QR o cédula | Cobertura biométrica [oficial] |
| Ingreso sin internet | No posible sin papel | Sí, con lista descargada | Dispositivo con lista previa |

### Espera en fila (modelo de cola)
Las horas anteriores son tiempo de atención en la puerta. Lo que vive el asistente es la **espera en la fila**, que es mucho mayor. Modelo simple de flujo [supuesto]: la gente llega de manera uniforme durante la ventana de llegada; cuando llega más rápido de lo que las puertas atienden, la fila crece; la espera promedio es (llegadas ÷ capacidad − 1) × ventana ÷ 2.

| Escenario | Supuestos | Espera promedio antes | Espera promedio después | Horas de espera evitadas |
|---|---|---|---|---|
| Evento masivo | 6.000 asistentes, 6 puertas, llegada en 2 h; 35 s antes, 10,4 s después | ~3 h 52 min | ~26 min | ~20.500 h por evento |
| Evento empresarial | 300 asistentes, 1 puerta, llegada en 30 min | ~1 h 13 min | ~11 min | ~310 h por evento |

Si la llegada es más repartida, la fila es menor en ambos casos y el ahorro baja; por eso estas cifras se validan con la duración real del ingreso que dé CONFA en el kickoff.

### Valor anual [supuesto]
Base: 2 eventos masivos y 44 eventos empresariales al año [oficial: Informe de Gestión 2025]; tamaño del evento empresarial y horas de consolidación [supuesto].

| Concepto | Cálculo | Horas al año | Valor al año |
|---|---|---|---|
| Atención en la puerta (personal) | 2 × 6.000 + 44 × 300 asistentes, × 24,6 s ahorrados | ~172 h | |
| Consolidación de listados (personal) | 2 masivos × 4 h + 44 empresariales × 1 h [supuesto] | 52 h | |
| **Total personal** | ~224 h × $15.000/h [supuesto] | ~224 h | **~$3,4 M** |
| **Espera de asistentes** | 2 × 20.500 h + 44 × 310 h; valorada a $7.500/h, la mitad del costo hora del personal, convención usual para el tiempo no laboral [supuesto] | ~54.600 h | **~$409 M** |

El ahorro en personal es pequeño; el valor está en devolverle a los afiliados unas 54.600 horas al año que hoy pasan en fila, buena parte al sol. Además: cero listados impresos y consolidación inmediata.

## Preguntas abiertas para el kickoff
1. ¿Cuánto dura hoy el ingreso a un evento grande y cuántas puertas usan?
2. ¿Cuánto tardan en consolidar la asistencia?
3. ¿Cuál es la latencia de la API facial y acepta recortes de una foto grupal?
4. ¿Se permite registrar en sitio a personas no inscritas?
5. ¿Cómo gestiona hoy CONFA las solicitudes de sede: correo, llamada, sistema? ¿Quién aprueba y en cuánto tiempo?
6. ¿Hay calendario de disponibilidad de sedes en una base de datos o es manual?
7. ¿Qué sedes tienen mala conectividad? ¿El modo sin internet es del dispositivo de la puerta, del QR del asistente, o de ambos?
8. ¿Los pasadías ya usan el reconocimiento facial en la entrada? ¿Se integra o se reutiliza?
9. "Voz para entrar a CONFA": ¿es hablarle al sistema (comandos, decir la cédula) o identificar a la persona por su voz? Si es lo segundo, ¿CONFA tiene un servicio de voz y base de huellas de voz, o no?
10. En eventos sin registro previo, ¿contra qué base se identifica a la persona (la identidad digital de CONFA, afiliados, otra) y se permite registrar a quien no existe?
11. ¿Qué datos de la persona puede ver el logístico en la puerta (empresa, categoría, acompañantes)?
12. Perfil del asistente sin conocimiento de tecnología: ¿qué porcentaje y qué canal funciona mejor (documento en papel, ayuda del logístico)?
13. Eventos virtuales e híbridos: ¿qué plataforma usa CONFA (Teams, Zoom u otra) y cómo cuenta hoy la asistencia en línea?
14. Sin conexión no hay reconocimiento facial local: ¿es aceptable que sin internet se valide solo con QR y cédula?
