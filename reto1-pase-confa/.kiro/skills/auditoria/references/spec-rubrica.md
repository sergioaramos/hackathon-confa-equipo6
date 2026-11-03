# Lente: spec-rubrica (trazabilidad y nota estimada)

## Trazabilidad
- [ ] Working Backwards → requisitos: cada requisito cita su pregunta de origen (matriz al final de `requirements.md`).
- [ ] Requisitos → diseño: cada requisito tiene componente en `design.md`.
- [ ] Diseño → tareas → código: cada tarea marcada `[x]` tiene código y prueba; **no hay código importante sin tarea** (es evidencia de Kiro).
- [ ] La spec refleja lo construido: si el equipo cambió de idea, la spec se actualizó.
- [ ] La afirmación "Huecos: ninguno" de `tasks.md` es cierta: recorre cada criterio MVP y comprueba que tenga tarea. Los requisitos MVP deben quedar en los primeros bloques, no al final.
- [ ] Las cifras del Working Backwards cuadran (recalcula la aritmética) y las citas o testimonios ficticios están marcados como ilustrativos.
- [ ] Cada requisito funcional oficial del reto (`working-backwards/references/`) tiene un criterio con sus palabras clave.
- [ ] El impacto está en pesos (o justifica por qué no) y cada referencia de vendor nombra su fuente.
- [ ] Toda pieza del diagrama de arquitectura tiene tarea; la identidad existe desde el bloque 1 si las herramientas dependen de ella.
- [ ] Cada bloque cerrado tiene su informe de auditoría guardado en `docs/auditorias/` (evidencia).
- [ ] El código de plantilla generado por `agentcore create` (`parse.py`, `memory/`, partes de `main.py`) no cuenta como "código sin tarea".

## Nota estimada (rúbrica oficial, 100 pts)
Califica de 1 a 5 estrellas con evidencia concreta; puntos = estrellas ÷ 5 × peso.

| # | Dimensión | Peso | 5★ exige |
|---|---|---|---|
| 1 | Demo y presentación | 10 | Demo en vivo en ≤ 10 min, storytelling del cliente, cierre contundente (solo video o diapositivas: máximo 3★) |
| 2 | Working Backwards | 10 | Las 5 preguntas con evidencia y obsesión por el cliente |
| 3 | Ajuste al reto | 15 | Requisitos clave, casos de uso y contingencias |
| 4 | Think Big / Invent & Simplify | 10 | Innovador y simple de usar y operar |
| 5 | Impacto de negocio | 20 | Valor para CONFA cuantificado con métricas del reto y supuestos explícitos |
| 6 | Uso de Kiro | 10 | Specs y steering bien definidos y visibles en el repo |
| 7 | Arquitectura agéntica | 15 | AgentCore (Runtime, Memory y/o Gateway) con modelos justificados por tarea; integrable con CONFA |
| 8 | Seguridad e IA responsable | 10 | Ley 1581: consentimiento, cifrado, control de acceso, guardrails |

Anclas de tiempo: ≤ 10 min no resta; hasta 11 min resta 1★; más de 12 min o presentación cortada resta 2★. La integración con la API facial real suma en las dimensiones 3 y 7.

Reglas de puntaje: estrellas enteras (si dudas entre dos, la menor). Califica lo que **funciona y se puede mostrar hoy**; la spec sin código no sube Ajuste al reto ni Arquitectura más allá de 2★.

## Salida
1. Tabla con estrellas, puntos y evidencia por dimensión, más el total estimado **actual** y el **proyectado** si se completan los bloques planificados.
2. **Las 3 acciones que más puntos suben por hora de trabajo** (empezando por las dimensiones de mayor peso: Impacto 20, Ajuste 15, Arquitectura 15).
