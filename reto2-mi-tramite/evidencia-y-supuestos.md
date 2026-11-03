# Evidencia y supuestos — Hackathon CONFA × AWS

> Regla de la rúbrica: "si se estiman valores, explicar los supuestos; no inventar cifras".
> Etiquetas: **[oficial]** dato publicado por CONFA · **[vendor]** caso de un proveedor (sesgado, usar como referencia) · **[supuesto]** estimación nuestra, validar en el kickoff.

## 1. CONFA en cifras (Informe de Gestión 2025)

Fuente: https://confa.co/wp-content/uploads/2026/04/INFORME-DE-GESTION-2025-V4.pdf (verificado el 30 oct 2026).

| Dato | Valor | Tipo |
|---|---|---|
| Empresas afiliadas | 14.984 (+5,51 %) | [oficial] |
| Trabajadores afiliados | 173.055 | [oficial] |
| Población afiliada total | 356.123 | [oficial] |
| Personas con identidad digital (enrolamiento biométrico) | **268.724** | [oficial] |
| Reconocimiento facial | Ya en uso para el ingreso a centros recreacionales y en un piloto en máquinas de Versalles | [oficial] |
| Eventos empresariales | 44 eventos para 19 empresas, más de $1.749 millones | [oficial] |
| Eventos masivos en La Rochela (50 años) | 2 eventos, 12.086 asistentes en preventa | [oficial] |
| Usos en eventos y planes de bienestar | 15.803 | [oficial] |
| Colaboradores de CONFA | ~1.200 (Revista Confa, mayo 2026; no es cifra exacta) | [oficial, aproximado] |

**Lectura clave:** CONFA ya tiene la identidad biométrica de 268.724 personas. El reto 1 no consiste en construir reconocimiento facial, sino en **llevar esa identidad digital al ciclo completo de los eventos**.

## 2. Reto 1: eventos

### Referencias externas
| Dato | Valor | Tipo |
|---|---|---|
| Búsqueda manual en un listado | 30–40 s por asistente | [vendor] Fielddrive |
| Check-in con QR | 15–20 s | [vendor] Fielddrive |
| Check-in facial | 3–10 s (EventX); 9 s (Spring Masterminds); 15–20 s (Zenus) | [vendor] |

### Estimaciones
**a) Cuántos necesitan la contingencia QR**
- 268.724 enrolados ÷ 356.123 afiliados ≈ **75 %**, así que **~1 de cada 4 asistentes afiliados necesitaría QR o documento**.
- [supuesto] Los enrolados son afiliados. Puede haber no afiliados enrolados, así que el porcentaje real de cobertura podría ser menor.
- Uso en el pitch: el QR no es un caso marginal. Es un flujo que usará una de cada cuatro personas, y además respeta a quien no quiere usar biometría.

**b) Evento masivo (tipo La Rochela)**
- [oficial] 12.086 asistentes en 2 eventos, o sea **~6.000 por evento**.
- [supuesto] 6 puntos de ingreso, 35 s por persona con listado manual y 8 s con reconocimiento facial.
- Manual: 6.000 × 35 s ÷ 6 puertas ≈ **9,7 horas de flujo de ingreso**.
- Facial: 6.000 × 8 s ÷ 6 puertas ≈ **2,2 horas**.
- Con el 25 % por QR a 18 s: 6.000 × (0,75 × 8 + 0,25 × 18) ÷ 6 ≈ **2,9 horas**.
- Resultado: **~70 % menos tiempo de ingreso**. Es ilustrativo y depende de los supuestos.

**c) Evento interno sin registro ("Encuentro con el Director")**
- [supuesto] 300 colaboradores y 20 s por firma en un listado de papel, más ~1 minuto por persona para transcribir y consolidar.
- Hoy: ~1,7 h de firmas en la entrada más ~5 h de consolidación manual.
- Con foto grupal y detección de múltiples rostros: asistencia consolidada **en minutos**, sin papel.

**Validar en el kickoff:** cuántos asistentes tiene un evento típico, cuántas puertas, cuánto dura la fila hoy y cuánto tardan en consolidar la asistencia.

## 3. Reto 2: solicitudes de GTH

### Referencias externas
| Dato | Valor | Tipo |
|---|---|---|
| Ciclo de aprobación de permisos con flujo automático | De 3–5 días a menos de 24 h | [vendor] varios |
| Consultas sobre ausencias tras un portal de autoservicio | −65 % | [vendor] Apps365 |
| Costo de una consulta a RR. HH. por teléfono vs. autoservicio | ~$10,91 vs. ~$5,48 | estudio antiguo atribuido a Gartner (de segunda mano) |
| Incapacidades en Colombia | El empleador paga los días 1–2; la EPS desde el día 3. El empleador tramita el recobro (Decreto Ley 019 de 2012, art. 121) | norma; verificar el detalle antes de citarlo |

### Estimaciones
**a) Volumen de solicitudes**
- [oficial, aproximado] ~1.200 colaboradores.
- [supuesto] ~5 trámites por colaborador al año: 1–2 de vacaciones, 2 certificados, 1 incapacidad, 1 permiso.
- Resultado: **~6.000 solicitudes al año, unas 500 al mes**.

**b) Consultas de "¿en qué va lo mío?"**
- [supuesto] Una consulta de estado por solicitud, y 5 minutos de GTH para atenderla.
- 500 × 5 min ≈ **42 horas al mes de GTH respondiendo estados**, unas 5 jornadas.
- Con trazabilidad visible, si se aplica la referencia de −65 %: **~27 horas al mes liberadas**.

**c) Ciclo de aprobación**
- [supuesto] Hoy, 3–5 días para una solicitud de varias aprobaciones (referencia de vendors).
- Meta del pitch: menos de 24 h para el caso de solo el líder, medido con las marcas de tiempo que el propio sistema registra.

**d) Incapacidades (ángulo financiero, por verificar)**
- Si el soporte llega incompleto, se demora el recobro a la EPS que CONFA tramita como empleador.
- Que el agente valide el soporte en el momento de radicarlo reduce esos reprocesos.

**Validar en el kickoff:** encuesta a mano alzada a los 17 participantes, que son clientes reales del reto 2:
1. ¿Quién ha tenido que preguntar en qué va una solicitud?
2. ¿Cuánto tardó su última aprobación de vacaciones?
3. ¿A quién se le ha perdido una solicitud?

## 4. Datos que no se encontraron (no inventar)
- El número exacto de colaboradores de CONFA.
- Los tiempos reales de las filas en eventos de CONFA.
- El volumen de solicitudes de GTH, los tiempos de aprobación y las incapacidades al año.
- Un estudio independiente (que no sea de vendor) sobre tiempos de check-in.
