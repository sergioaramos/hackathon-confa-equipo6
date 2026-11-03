# Lente: seguridad (Ley 1581 de 2012) — 10 pts

## Bloqueantes
- [ ] **Credenciales en el código o en el repo**: claves de AWS (`AKIA`, `ASIA`), tokens, contraseñas, `.env` versionado, cadenas de conexión con contraseña. `agentcore/.env.local` debe estar en `.gitignore`.
- [ ] **Imágenes faciales persistidas**: buscar escrituras de bytes o base64 de imágenes en RDS, S3, logs, la memoria de AgentCore o archivos. Solo se guarda la cédula y el resultado.
- [ ] **Diagnóstico expuesto**: ninguna herramienta, endpoint o respuesta para aprobadores incluye el diagnóstico o la descripción médica de una incapacidad.
- [ ] **Datos reales** de personas sin autorización (cédulas, nombres o fotos que no sean ficticios o del equipo).
- [ ] Logs que imprimen payloads completos con PII o imágenes.

## Importantes
- [ ] **Consentimiento**: existe un paso explícito antes de usar el rostro, y la alternativa QR o documento está disponible para quien no acepte.
- [ ] **Minimización**: las herramientas devuelven solo los campos que el usuario puede ver (no `SELECT *` hacia el agente).
- [ ] **Control de acceso**: el personal logístico o el aprobador se autentica (Identity / JWT); una persona no puede consultar las solicitudes de otra.
- [ ] **Guardrails** configurados en el modelo del agente que habla con usuarios: ataques de prompt, PII (regex de cédula), temas denegados del reto.
- [ ] **Mínimo privilegio**: los roles de IAM no usan `*` en acciones ni recursos sin justificación.
- [ ] **Retención**: `eventExpiryDuration` de la memoria definido y justificado; la memoria no guarda datos de salud.
- [ ] **Trazabilidad**: se registra quién aprobó qué y cuándo (reto 2) y quién validó el ingreso (reto 1).
- [ ] HTTPS en las integraciones; cifrado en reposo de RDS.

## Menores
- [ ] Mensajes de error que filtran detalles internos (stack traces, nombres de tablas) al usuario.
- [ ] Datos de demo marcados como ficticios.

## Evidencia para el jurado
Lista lo bien hecho como frases listas para la diapositiva de seguridad: "La foto nunca se guarda: solo la cédula y el resultado", etc.
