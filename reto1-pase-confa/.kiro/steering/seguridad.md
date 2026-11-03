---
inclusion: always
---
# Seguridad, privacidad e IA responsable (Ley 1581 de 2012)

Los dos retos tocan **datos sensibles**: biometría (reto 1) y salud (incapacidades, reto 2). Esta dimensión vale 10 puntos y se evalúa en el código, no en las diapositivas.

## Reglas obligatorias
1. **Datos:** solo ficticios o los que la organización entregue para el evento. Fotos solo de personas que lo autoricen (el equipo).
2. **Biometría:** **nunca** guardar imágenes en RDS ni en logs. Se guarda solo la cédula y el resultado de la validación. Las fotos de validación se descartan.
3. **Consentimiento:** paso explícito antes de usar el rostro. Quien no acepte usa QR o documento: la alternativa sin biometría es un derecho, no solo una contingencia.
4. **Salud:** el aprobador ve que hay una incapacidad y sus fechas, **nunca** el diagnóstico. El dato restringido no sale de la base de datos hacia quien no debe verlo.
5. **Residencia:** no subir datos de CONFA a herramientas fuera de la cuenta AWS del evento.
6. **Secretos:** nada de credenciales en el código ni en el repo. Roles de IAM, variables de entorno y AgentCore Identity.
7. **Mínimo privilegio:** cada herramienta y cada agente con solo los permisos que necesita.
8. **Trazabilidad:** registrar quién aprobó qué y cuándo.
9. **Cifrado:** HTTPS en tránsito; cifrado en reposo en RDS y en la memoria.
10. **Retención:** definir cuánto vive cada dato (memoria de AgentCore: `eventExpiryDuration`).

## Capas de defensa (en este orden)
1. No guardar lo que no hace falta (minimización).
2. Las herramientas devuelven solo lo que el usuario puede ver.
3. IAM y AgentCore Identity: quién invoca y con qué credenciales sale el agente.
4. Bedrock Guardrails como red final: PII (cédula con regex propia), temas denegados, ataques de prompt.

## Humano en el ciclo
El agente **propone**; una persona **decide**. Ninguna aprobación la hace el agente solo.
