# Lente: agentcore (infraestructura y despliegue) — Arquitectura agéntica, 15 pts

## Antes de `agentcore deploy`
- [ ] `agentcore/agentcore.json` declara solo lo que usa el diseño: Runtime + Memory y/o Gateway, cada uno con su razón en `design.md`.
- [ ] Credenciales de la cuenta correcta activas: `aws sts get-caller-identity` (desarrollo: cuenta del proveedor; despliegue final: cuenta de CONFA, según el kickoff).
- [ ] `agentcore/aws-targets.json`: la plantilla lo deja en `[]` y el primer `deploy` crea el target por defecto con la cuenta y región de las credenciales activas. Verifica que esa sea la cuenta y región del evento (`agentcore status` después del deploy).
- [ ] El modelo responde en esa cuenta y región **antes** de desplegar: `aws bedrock-runtime converse --model-id <id de load.py> --region <r> --messages '[{"role":"user","content":[{"text":"ok"}]}]'`. `deploy` no detecta un modelo sin acceso: falla en la primera invocación.
- [ ] La versión de Python de `runtimeVersion` (agentcore.json) coincide con lo que resuelve `uv.lock`; si `agentcore build` falla al empaquetar, bajar la versión.
- [ ] Dependencias de sistema declaradas: si se usa `zoneinfo`, agregar `uv add tzdata`.
- [ ] Variables de entorno que el código necesita en el Runtime (`MODELO_BEDROCK`, `EVENTO_ACTIVO`, URL de APIs): definidas para el despliegue, no solo en `.env.local` (que no se despliega).
- [ ] El agente desplegado no lee datos locales (SQLite, archivos) que en el Runtime estarían vacíos o congelados: debe consumir la RDS o la API del evento. Después del deploy, verifica que una consulta devuelve cifras reales y no 0.
- [ ] `actorId` y `session_id` no caen a valores por defecto (`"default"`) cuando hay Memory: las personas quedarían mezcladas.
- [ ] `agentcore dev` + `agentcore invoke --runtime <n> --local` funcionan antes de desplegar.
- [ ] Dependencias en `app/<agente>/pyproject.toml` (agregadas con `uv add`), incluidas las que usa el código; no hay imports de paquetes no declarados.
- [ ] `model/load.py` usa un ID de modelo **habilitado en la cuenta** y con perfil de inferencia (`us.`/`global.`); el modo `LOCAL_MODEL=ollama` no queda activo en el despliegue.
- [ ] Nada de credenciales en `agentcore.json`, `pyproject.toml` ni en el código. Las API keys van en `agentcore add credentials` (AgentCore Identity).

## Memory
- [ ] `eventExpiryDuration` justificado (3-365 días).
- [ ] Estrategias necesarias y no todas por defecto (la plantilla trae SEMANTIC, USER_PREFERENCE, SUMMARIZATION y EPISODIC con `eventExpiryDuration: 30`: quitar las que no se usen y ajustar la retención a lo que promete el diseño).
- [ ] `memory/session.py` (`retrieval_config`) solo consulta los namespaces de las estrategias declaradas.
- [ ] `actorId` real del usuario en el payload (no `"default"`), para que la memoria no se mezcle entre personas.
- [ ] No se guardan datos sensibles en la memoria (diagnósticos, imágenes).

## Gateway (N/A si el diseño aún no lo incluye en el bloque auditado)
- [ ] Autorizador definido (`AWS_IAM` o `CUSTOM_JWT`); `NONE` solo con justificación.
- [ ] Targets con contrato (OpenAPI) y nombres de herramientas claros.
- [ ] La URL y el token del gateway llegan al agente por variable de entorno o Identity, no escritos en el código.

## Observabilidad y demo
- [ ] `agentcore traces` y `agentcore logs` muestran la ejecución (para enseñar en la demo cómo razonó el agente).
- [ ] Hay un plan B si el despliegue falla: correr con `agentcore dev` en local, más un video corto de respaldo.
- [ ] Se probó el endpoint desplegado con `agentcore invoke --runtime <n> --payload ...` y la sesión se mantiene con `--session-id`.
