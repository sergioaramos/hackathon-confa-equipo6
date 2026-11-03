---
name: working-backwards
description: Fase 0 de la hackathon CONFA. Guía las 5 preguntas de Working Backwards de Amazon (cliente, problema, beneficio, evidencia, experiencia) y redacta el comunicado de prensa. Úsala al elegir el reto, antes de cualquier spec o código.
---

# Working Backwards

Objetivo: definir cliente y problema **antes** de la tecnología. Produce `docs/working-backwards.md` y llena `.kiro/steering/producto.md`. Vale 10 puntos de la rúbrica y alimenta Impacto de negocio (20), la apertura de la demo y los requisitos.

## Regla principal
**Pregunta y estructura; no inventes el negocio.** El jurado quiere "respuestas propias con evidencia de conocimiento de CONFA". Propón borradores solo cuando el equipo lo pida, y márcalos como borrador.

## Proceso
1. Pregunta qué reto eligieron y lee la referencia: `references/reto1-eventos.md` o `references/reto2-gth.md`. Lee también `evidencia-y-supuestos.md` si existe.
2. Haz las 5 preguntas **de a una**, y critica cada respuesta antes de pasar a la siguiente:

| # | Pregunta | Criterio para aceptarla | Trampa a señalar |
|---|---|---|---|
| 1 | ¿Quién es el cliente? | Persona concreta **y momento** en que sufre. Nombrar también al cliente secundario (quien atiende o aprueba) | "Los usuarios", "todos los afiliados" |
| 2 | ¿Cuál es su problema? | Dolor en lenguaje humano + **consecuencia medible** | Describir la falta de tecnología ("no tienen IA") |
| 3 | ¿Cuál es el beneficio más importante? | **Uno solo** | Listas de beneficios |
| 4 | ¿Cómo sabemos qué necesita? | Evidencia etiquetada: [oficial], [vendor], [supuesto], [encuesta kickoff] | Cifras sin fuente |
| 5 | ¿Cómo es su experiencia? | Paso a paso **desde los ojos del cliente**, con la contingencia incluida | Describir la arquitectura |

3. Sugiere la **encuesta a mano alzada del kickoff** (los participantes son colaboradores de CONFA y clientes reales del reto 2) si falta evidencia.
4. Redacta el comunicado de prensa con la plantilla de abajo. **Sin** "IA", "agente", "AWS" ni "Bedrock": habla de la vida del cliente. La cita del comunicado es ilustrativa por convención: en el documento márcala así y, si es posible, reemplázala por una frase real del kickoff.
5. Recalcula cada cifra derivada (multiplicaciones, porcentajes) antes de escribirla. **Lleva el impacto a pesos** cuando sea posible (horas × costo por hora supuesto, marcado [supuesto]) y nombra la fuente de cada referencia de vendor: Impacto vale 20 puntos y las horas solas pesan menos que el dinero.
6. Escribe `docs/working-backwards.md` y llena `.kiro/steering/producto.md`.
7. Cierra diciendo que el siguiente paso es `/spec-requisitos`.

## Plantilla del comunicado
```
# CONFA lanza <nombre> para <cliente>
*Manizales, <fecha>.* <Beneficio principal en una frase.> <Cómo era antes: el dolor y su consecuencia.>
<Cómo es ahora: la experiencia en 2-3 pasos, incluida la alternativa para quien no puede usar el flujo principal.>
"<Cita creíble de un usuario>", cuenta <nombre>, <rol>.
<Métrica de impacto de las primeras semanas, con su supuesto entre paréntesis.>
```

## Formato de `docs/working-backwards.md`
Secciones: Reto · 5 preguntas (con la evidencia etiquetada) · Comunicado · Métricas y supuestos · Preguntas abiertas para el kickoff.
