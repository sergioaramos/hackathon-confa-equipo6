"""Busca credenciales escritas en archivos del repo. Multiplataforma (Windows/macOS/Linux).

Uso:  python scripts/revisar_secretos.py [archivo ...]   (sin argumentos: todo el repo)
Sale con código 1 si encuentra algo.
"""
import pathlib
import re
import sys

PATRONES = {
    "AWS access key": re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b"),
    "AWS secret key": re.compile(r"(?i)aws_secret_access_key\s*[=:]\s*['\"]?[A-Za-z0-9/+=]{40}"),
    "Clave privada": re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "Token o contraseña asignado": re.compile(
        r"(?i)\b(password|passwd|secret|token|api_key|apikey)\b\s*[=:]\s*['\"][^'\"\s]{8,}['\"]"),
    "Cadena de conexión con contraseña": re.compile(r"(?i)\b(postgres(ql)?|mysql)://[^:\s]+:[^@\s]+@"),
}
IGNORAR = {".git", ".venv", "node_modules", "cdk.out", "__pycache__", ".kiro", ".claude"}
EXTENSIONES = {".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".yaml", ".yml", ".toml", ".env", ".md", ".sh", ".ps1"}


def archivos(argumentos: list[str]) -> list[pathlib.Path]:
    if argumentos:
        return [pathlib.Path(a) for a in argumentos if pathlib.Path(a).is_file()]
    return [p for p in pathlib.Path(".").rglob("*")
            if p.is_file() and not IGNORAR & set(p.parts) and (p.suffix in EXTENSIONES or p.name.startswith(".env"))]


def main() -> int:
    hallazgos = []
    for ruta in archivos(sys.argv[1:]):
        try:
            lineas = ruta.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for n, linea in enumerate(lineas, 1):
            for nombre, patron in PATRONES.items():
                if patron.search(linea):
                    hallazgos.append(f"{ruta}:{n}: {nombre}")
    for h in hallazgos:
        print(f"⚠️  {h}")
    if not hallazgos:
        print("✅ Sin credenciales a la vista.")
    return 1 if hallazgos else 0


if __name__ == "__main__":
    sys.exit(main())
