---
name: spec-requisitos
description: Fase 1 de la spec (QUÉ). Convierte el Working Backwards y el comunicado de prensa en .kiro/specs/<slug>/requirements.md con historias de usuario y criterios de aceptación en notación EARS, incluidas las contingencias. Úsala después de /working-backwards y antes del diseño.
---

# Spec 1 · Requisitos (QUÉ y PARA QUIÉN)

Entrada: `docs/working-backwards.md` y `.kiro/steering/producto.md`. Salida: `.kiro/specs/<slug>/requirements.md`. **No escribe diseño ni código.**

## Reglas
1. **Todo requisito nace del Working Backwards.** Cada historia cita la pregunta de la que sale (cliente, problema, experiencia). Si algo no se justifica desde el cliente, no entra.
2. Formato Kiro: historia de usuario + criterios EARS numerados (`1.1`, `1.2`...). Palabras clave EARS en inglés y mayúsculas; el resto en español.

| Patrón | Plantilla | Para |
|---|---|---|
| Evento | `WHEN <disparador> THE SYSTEM SHALL <respuesta>` | Flujo normal |
| No deseado | `IF <condición de error> THEN THE SYSTEM SHALL <respuesta>` | **Contingencias** (Ajuste al reto) |
| Estado | `WHILE <estado> THE SYSTEM SHALL <respuesta>` | Tiempo real |
| Siempre | `THE SYSTEM SHALL [NOT] <respuesta>` | Reglas de seguridad |

3. **Cada criterio es verificable**: cifras concretas ("en menos de 3 s"), nunca "rápido" ni "fácil".
4. **Cubre todos los casos de uso del reto** (ver `working-backwards/references/`). Si falta uno, decláralo como fuera de alcance de forma explícita.
5. **Incluye un requisito de seguridad** con las reglas de `.kiro/steering/seguridad.md` que apliquen (minimización, acceso al dato sensible). **El consentimiento va como criterio explícito** (WHEN … THE SYSTEM SHALL mostrar el aviso y pedir aceptación) siempre que se toque biometría o salud.
5b. **Recorre los requisitos funcionales oficiales del reto uno por uno** (`working-backwards/references/`) y verifica que cada uno tenga un criterio con sus mismas palabras clave. En el laboratorio del reto 2 quedó por fuera "radicación con adjuntos" y la edición de rutas existentes.
5c. Si hay cálculos de fechas, define **días hábiles con festivos de Colombia** (y fines de semana) en el criterio.
6. **Prioriza** con MVP / Deseable: el MVP es lo que debe funcionar de punta a punta el miércoles a las 4:00 p. m.
7. Al final, una **matriz de trazabilidad**: pregunta de Working Backwards → requisito.

## Plantilla
```markdown
# Requisitos: <nombre>

## Introducción
<problema y cliente en 3 líneas, desde el comunicado>

## Requisitos

### Requisito 1: <nombre> [MVP]
**Historia:** Como <cliente>, quiero <acción>, para <beneficio>.
_Origen: WB-P5 (experiencia)_

#### Criterios de aceptación
1.1 WHEN ... THE SYSTEM SHALL ...
1.2 IF ... THEN THE SYSTEM SHALL ...

## Fuera de alcance
## Matriz de trazabilidad
| Pregunta WB | Requisitos |
```

## Cierre
Termina con **3 a 5 preguntas de aclaración** (ambigüedades, cifras sin fuente, casos sin cubrir) y espera respuesta antes de dar la fase por cerrada. Luego el siguiente paso es `/spec-diseno`.
