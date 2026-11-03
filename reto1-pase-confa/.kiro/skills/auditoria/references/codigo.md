# Lente: codigo (calidad general)

## Correctitud
- [ ] La lógica hace lo que dice la tarea y el requisito citado.
- [ ] Casos límite: listas vacías, `None`, cédulas con espacios o puntos, fechas inválidas, duplicados (la misma persona validada dos veces).
- [ ] Comparaciones de texto en español sin distinguir mayúsculas, tildes ni espacios (empresas, nombres). Ojo: `lower()` de SQLite solo cubre ASCII ("CAFÉ" ≠ "café").
- [ ] Horas guardadas con zona horaria (Lambda y AgentCore corren en UTC; Colombia es UTC-5).
- [ ] Concurrencia razonable: dos puertas marcando a la misma persona no duplican la asistencia (restricción única en la BD).
- [ ] Manejo de errores en cada integración: si la API facial o la BD fallan, el usuario ve un mensaje claro y existe una salida (QR).

## Mantenibilidad
- [ ] Funciones pequeñas, nombres claros en español o inglés (consistentes en el repo).
- [ ] Sin duplicación evidente; utilidades compartidas en un módulo.
- [ ] Configuración por variables de entorno, no constantes mágicas repetidas.
- [ ] Sin código muerto, `print` de depuración ni TODO críticos sin resolver.

## Python
- [ ] Type hints en las funciones públicas.
- [ ] Consultas SQL parametrizadas (nunca f-strings con datos del usuario).
- [ ] Recursos cerrados (`with` para conexiones y archivos). Ojo: `with sqlite3.connect()` hace commit pero no cierra.

## Frontend (React)
- [ ] Estados de carga y error visibles (la demo en vivo los va a mostrar).
- [ ] No hay claves ni endpoints secretos en el bundle del cliente.
- [ ] Textos en español y accesibles (contraste, tamaño legible en el proyector).

## Repo
- [ ] `README` con cómo correr la demo en 3 comandos.
- [ ] `.gitignore` cubre `.venv`, `node_modules`, `.env*`, `cdk.out`.
