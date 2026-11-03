---
name: presentacion
description: Arma la presentación final de 10 minutos de la hackathon CONFA - diapositivas HTML animadas en un solo archivo (cronómetro, notas del presentador, cifras animadas, diagrama que se dibuja por pasos, exportable a PDF), guion con tiempos, guion de la demo con plan B, preguntas probables del jurado y autoevaluación con la rúbrica. Úsala el jueves temprano o cuando haya demo de punta a punta.
---

# Presentación

Salidas en `docs/presentacion/`:
- `index.html`: las diapositivas, copiadas de `assets/plantilla.html` y llenadas.
- `guion.md`: guion por bloques, guion de la demo, plan B y preguntas del jurado.
- `presentacion.pdf`: respaldo (lo exporta el equipo; ver abajo).

## Fuentes (no inventes nada)
`docs/working-backwards.md`, `.kiro/steering/producto.md`, `.kiro/specs/<slug>/design.md` (arquitectura, modelos, seguridad, preguntas del jurado), `evidencia-y-supuestos.md` y lo que realmente funciona en la demo. Si una cifra no tiene fuente o supuesto, pregunta.

## Estructura (10 min; pasarse de 11 resta 1★, de 12 resta 2★)
| # | Diapositiva | Tiempo | Rúbrica |
|---|---|---|---|
| 1 | Portada: nombre + beneficio en una frase | 0:20 | Demo |
| 2 | Cliente: una persona concreta + cita | 0:40 | Working Backwards |
| 3 | Problema: dolor + 2 cifras con fuente | 0:50 | WB, Impacto |
| 4 | Comunicado de prensa | 0:30 | WB |
| 5 | **DEMO EN VIVO**, desde los ojos del cliente, con la contingencia y la traza | 3:30 | Demo, Ajuste al reto |
| 6 | Arquitectura (se dibuja por pasos) + dónde NO usamos IA | 1:00 | Arquitectura |
| 7 | Un modelo para cada tarea | 0:40 | Arquitectura |
| 8 | Seguridad por capas (Ley 1581) | 0:40 | Seguridad |
| 9 | Impacto en números con supuestos | 0:50 | **Impacto (20 pts)** |
| 10 | Think Big: lo que viene | 0:30 | Think Big |
| 11 | Cierre: volver al cliente | 0:20 | Demo |

Abrir con el cliente, no con la arquitectura. Cerrar con el impacto.

## Cómo llenar la plantilla
1. Copia `assets/plantilla.html` a `docs/presentacion/index.html`. **Sin dependencias externas**: todo va dentro del archivo, porque el WiFi del evento puede fallar.
2. Reemplaza cada `EDITAR` (`grep -n EDITAR` debe quedar vacío). Textos cortos: máximo 3 ideas por diapositiva.
3. Mecánicas disponibles:
   - Clase `f`: el elemento aparece al avanzar (un paso por elemento, en orden).
   - Cifra animada: `<div class="cifra" data-count="70" data-prefijo="−" data-sufijo="%">0</div>`. **Sufijo corto** (`%`, `s`, `h`); las palabras van en el texto de abajo, porque un sufijo largo desborda la tarjeta.
   - Citas: si la persona no es real (un comunicado o una persona ilustrativa), dilo en el `<small>` de la cita. El jurado premia la evidencia, no los testimonios inventados.
   - Diagrama: cada `<g class="nodo f">` y cada `<path class="flecha">` aparecen por pasos. Ajusta las coordenadas del `viewBox` 1000×300 al diseño real.
   - Notas del presentador: `<aside class="notas">` en cada diapositiva (tecla `N`).
   - Colores en `:root` (`--marca`, `--acento`).
4. Teclas: ←/→ avanzar, `N` notas, `F` pantalla completa, `T` iniciar o pausar el cronómetro (cambia de color al minuto 9 y se pone rojo al pasar de 10), `R` reiniciar el reloj.
5. **PDF de respaldo**: abrir en Chrome → Imprimir → Guardar como PDF → horizontal, márgenes: ninguno, con gráficos de fondo. Sale una diapositiva por página, sin animaciones y con las cifras en su valor final. También desde la terminal (macOS; en Windows, la ruta de `chrome.exe`):
   ```bash
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --no-pdf-header-footer \
     --print-to-pdf=docs/presentacion/presentacion.pdf "file://$PWD/docs/presentacion/index.html"
   ```
6. **Revisa el PDF página por página** antes de darlo por bueno: textos que desbordan, cifras y diagramas.

## guion.md
- **Guion por diapositiva**, con tiempos acumulados y quién habla.
- **Guion de la demo**: pasos exactos, datos de prueba (ficticios), qué se dice en cada paso, y la contingencia mostrada en vivo (no enrolado → QR; adjunto ilegible).
- **Plan B**: si falla el despliegue, `agentcore dev` en local; si falla todo, un video corto de respaldo (máximo 60 s). La guía valora más una demo real con tropiezo que solo diapositivas.
- **Preguntas probables del jurado (10)**, con su respuesta en una o dos líneas: ¿por qué ese modelo?, ¿por qué N agentes?, ¿dónde viven los datos biométricos?, ¿qué pasa si la API facial falla?, ¿cómo se integra con los sistemas de CONFA?, ¿cuánto cuesta operarlo?, ¿cómo escala?, ¿qué recuerda la memoria y por cuánto tiempo?, ¿qué guardrails usan?, ¿cómo crea GTH un trámite sin programar? (o su equivalente del reto 1).
- **Autoevaluación**: ejecuta la lente `spec-rubrica` de `/auditoria` y anota las 3 mejoras de último momento.
