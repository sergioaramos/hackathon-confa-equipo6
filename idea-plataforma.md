# Borradores de la idea para la plataforma (Equipo 6)

> Una sola idea por equipo. Decidir con Luis David cuál se registra. Textos listos para copiar campo por campo.
> Las cifras marcadas como estimadas se validan en el kickoff.

---

## Opción A · Reto 1: Pase CONFA (recomendada)

**Título de la idea**
Pase CONFA: ingreso a eventos en segundos con la identidad digital de CONFA

**Industria**
La más cercana a servicios / sector social (si no aparece, "Otro")

**Estado actual**
CONFA organiza eventos para colegios, afiliados, empresas y colaboradores. Según su Informe de Gestión 2025 (el último publicado, abril de 2026), ese año realizó 44 eventos empresariales y reunió más de 12.000 asistentes en solo dos eventos masivos en La Rochela. Hoy, en la puerta, la validación sigue siendo manual: el personal logístico pide la cédula, busca a la persona en un listado y la marca a mano, lo que toma entre 30 y 40 segundos por asistente (referencia del sector). Al final, la asistencia se consolida transcribiendo esos listados. Al mismo tiempo, CONFA ya cuenta con identidad digital biométrica para 268.724 personas y usa reconocimiento facial en sus centros recreacionales: la capacidad existe, pero no se aprovecha en el control de los eventos.

**Puntos de dolor**
Filas largas en la entrada: un evento de 6.000 personas puede requerir del orden de 9 a 10 horas de flujo de ingreso entre 6 puertas (estimado)
El personal logístico trabaja a ciegas: no sabe cuántos han entrado ni quién falta hasta el cierre
Uno de cada cuatro asistentes no tiene su rostro registrado y necesita otra forma de entrar
Consolidar la asistencia exige horas de transcripción manual y papel en cada evento
El personal no accede de forma rápida y segura a una plataforma de control en sitio
En eventos de preescolar hay menores de edad, cuyos datos tienen protección reforzada

**Resultado esperado**
Cada asistente entra en segundos: con su rostro, con un código QR o con su documento, sin que nadie lo busque en papel. El personal logístico ve en tiempo real cuántos han ingresado y puede preguntar en lenguaje natural "¿quién falta de la empresa X?". Al cerrar el evento, el informe de asistencia está listo sin transcribir nada.

**Propuesta de solución**
Una aplicación web para el personal logístico con dos caminos. La validación en la puerta es código determinista y rápido: la foto va a la API de reconocimiento facial de CONFA, se cruza con los inscritos en la base de datos y se marca la asistencia; si no hay coincidencia, se valida con QR firmado o con la cédula. La foto nunca se guarda. Un agente de IA construido con Strands y desplegado en Amazon Bedrock AgentCore (Runtime, Memory, Gateway e Identity) responde preguntas sobre la asistencia con cifras siempre tomadas de los datos, crea eventos a partir de una descripción en lenguaje natural y genera el informe de cierre. Seguridad según la Ley 1581: consentimiento antes de usar el rostro, alternativa sin biometría, sin reconocimiento facial a menores y Guardrails que enmascaran datos personales.

**Impacto esperado**
Reducción cercana al 70 % del tiempo total de ingreso en eventos masivos (estimado con 6 puertas y tiempos de referencia), alrededor del 75 % de los asistentes validados sin intervención manual, consolidación inmediata de la asistencia y cero listados impresos. Beneficia al personal logístico, a los asistentes y a los organizadores, y lleva a los eventos la inversión que CONFA ya hizo en identidad digital.

---

## Opción B · Reto 2: Mi Trámite CONFA

**Título de la idea**
Mi Trámite CONFA: solicitudes de Talento Humano con trazabilidad total y rutas que GTH configura sin programar

**Industria**
La más cercana a recursos humanos / servicios (si no aparece, "Otro")

**Estado actual**
Los cerca de 1.200 colaboradores de CONFA tramitan vacaciones, incapacidades, certificados y permisos por correo o chat. Las aprobaciones dependen del caso: a veces solo el líder directo, otras veces varias áreas. No hay una vista unificada del estado de cada solicitud, y crear un trámite nuevo o cambiar su ruta de aprobación requiere desarrollo.

**Puntos de dolor**
Las solicitudes se pierden en correos y chats
El colaborador no sabe en qué estado está su trámite ni quién lo tiene
GTH dedica horas a responder "¿en qué va lo mío?": del orden de 40 horas al mes (estimado con ~500 solicitudes mensuales)
Las rutas de aprobación varían y no hay una visión unificada para los aprobadores
Crear un trámite nuevo o cambiar su ruta exige programar
Los soportes de incapacidad llegan incompletos y retrasan el recobro a la EPS
Los datos de salud de las incapacidades requieren protección reforzada

**Resultado esperado**
El colaborador radica su trámite en lenguaje natural, adjunta sus soportes y ve en todo momento en qué paso va. Cada aprobador tiene su bandeja y recibe un correo en cada cambio de estado. GTH crea un trámite nuevo describiéndolo en palabras y el sistema arma su ruta de aprobación sin programar.

**Propuesta de solución**
Un asistente conversacional construido con Strands y desplegado en Amazon Bedrock AgentCore clasifica la solicitud, valida que el soporte esté completo y la radica. Un grafo de pasos (clasificar, validar, radicar) usa un modelo ligero para clasificar y uno multimodal para leer los soportes. Las rutas de aprobación se ejecutan con AWS Step Functions a partir de una configuración que un agente genera desde la descripción en lenguaje natural de GTH. Los correos salen por Amazon SES. AgentCore Memory recuerda el historial del colaborador sin guardar diagnósticos, y el aprobador ve la incapacidad y sus fechas, nunca el diagnóstico. El agente propone y una persona siempre aprueba.

**Impacto esperado**
Trazabilidad completa del 100 % de las solicitudes, ciclo de aprobación de días a horas en los trámites de una sola aprobación, decenas de horas al mes liberadas en GTH y trámites nuevos configurados en minutos en lugar de requerir desarrollo. Beneficia a los colaboradores, a los líderes aprobadores y al equipo de GTH.
