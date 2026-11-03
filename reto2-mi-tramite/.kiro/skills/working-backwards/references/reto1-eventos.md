# Reto 1: experiencia y control de eventos (resumen de la guía oficial)

**Reto:** centralizar y digitalizar el ciclo de vida del evento: creación, inscripción, tickets, control de acceso en sitio y consolidación de asistencia en tiempo real.

## Usuarios
- Asistentes en tres casos: con inscripción previa, internos sin registro, externos registrados por documento.
- Personal logístico y administrativo en la puerta.
- Organizadores.

## Casos de uso que deben cubrirse (Ajuste al reto: 15 pts)
| Tipo | Ejemplo | Necesidad |
|---|---|---|
| Con inscripción previa | Afiliados o empresas | Registro, ticket, validación |
| Interno sin registro | "Encuentro con el Director" | Marcado masivo de asistencia |
| Externo por documento | Preescolar | Registro con documento; no todos tienen enrolamiento facial |

## Requisitos tecnológicos
- Reconocimiento facial como motor principal (1 a 1, o varios rostros por video o foto).
- Contingencia para no enrolados: QR u otro método.
- Control de acceso y consolidación en tiempo real.
- Acceso rápido y seguro del personal logístico.

## Recursos del evento
- **API facial de CONFA** (API Gateway + Lambda): recibe una foto y devuelve la cédula. Endpoint y autenticación en el kickoff. Solo identifica **quién**; la solución decide **qué hacer**.
- **RDS del evento**: eventos, inscritos, asistencia.
- Integrarse con la API real suma evidencia en Ajuste al reto y en Arquitectura.

## Métricas sugeridas
Tiempo de ingreso por asistente (antes/después) · longitud y duración de filas · papel y listados eliminados · tiempo de consolidación · % validados sin intervención manual.

## Ángulos con evidencia (ver evidencia-y-supuestos.md)
- CONFA ya tiene 268.724 personas con identidad digital: el reto es llevar esa identidad a los eventos, no construir reconocimiento facial.
- ~75 % de cobertura biométrica → ~1 de cada 4 asistentes usará QR: la contingencia es un flujo principal.
- Varios rostros: Amazon Rekognition `DetectFaces` recorta las caras de una foto grupal y cada una pasa por la API facial.

## Desafíos
- La API solo expone la foto → cédula; la captura de varios rostros hay que resolverla.
- Datos biométricos: no guardar imágenes.
