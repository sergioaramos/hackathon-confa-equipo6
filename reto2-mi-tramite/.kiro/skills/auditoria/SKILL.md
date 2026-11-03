---
name: auditoria
description: Audita el desarrollo de la hackathon con una o varias lentes - seguridad (Ley 1581), strands (buenas prácticas de agentes), agentcore (infraestructura), codigo (calidad), tests (TDD y cobertura de criterios) y spec-rubrica (trazabilidad y nota estimada). Úsala al cerrar un bloque de tareas, antes de desplegar y antes de presentar. Uso - /auditoria <lente...> | todo.
---

# Auditoría

**Solo lectura: no modifica archivos.** Reporta hallazgos y el equipo decide qué se corrige (con `/implementar` o ajustando la spec).

## Lentes
| Lente | Checklist | Cuándo |
|---|---|---|
| `seguridad` | `references/seguridad.md` | Al cerrar un bloque que tocó datos, y antes de desplegar |
| `strands` | `references/strands.md` | Al cerrar un bloque de agentes |
| `agentcore` | `references/agentcore.md` | Antes de `agentcore deploy` |
| `codigo` | `references/codigo.md` | Al cerrar cada bloque |
| `tests` | `references/tests.md` | Al cerrar cada bloque |
| `spec-rubrica` | `references/spec-rubrica.md` | Jueves, antes de presentar |

`todo` = las seis. Sin argumento: pregunta cuáles, sugiriendo según el momento (último bloque cerrado en `tasks.md`).

## Proceso
1. **Alcance**: por defecto, lo cambiado desde el último commit (`git diff` + archivos sin seguimiento). Con `completo`, todo el repo.
2. Lee el checklist de cada lente y revisa **solo** lo que aplica a ese alcance.
3. Cada hallazgo debe ser **concreto y verificable**: archivo:línea, qué falla, por qué importa (requisito, regla o dimensión de la rúbrica) y cómo arreglarlo. Nada de "podría mejorarse" sin evidencia.
4. Si hay varias lentes y el entorno permite subagentes en paralelo (Claude Code: `auditor-<lente>`), delega una lente por subagente y consolida.

## Formato del informe
```
## Auditoría: <lentes> · <alcance> · <fecha>
### 🔴 Bloqueantes (impiden la demo o violan una regla de seguridad)
- [lente] archivo:línea — problema → arreglo (ref: Req x.y / regla / rúbrica)
### 🟠 Importantes (restan puntos)
### 🟡 Menores
### ✅ Bien hecho (para mencionar al jurado)
### Veredicto: LISTO | LISTO CON AJUSTES | NO LISTO
```
Máximo 15 hallazgos, ordenados por severidad. Si una lente no encuentra nada, dilo en una línea.

Quien invoca la auditoría (no el auditor, que es de solo lectura) guarda el informe en `docs/auditorias/<fecha>-<lentes>.md`: es la evidencia de que cada bloque se auditó.
