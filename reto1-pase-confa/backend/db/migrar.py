"""Aplica las migraciones SQL versionadas de ``db/migrations`` en orden.

Uso: ``PASE_DB_URL=postgresql://... uv run python -m db.migrar``
"""

import os
import sys
from pathlib import Path

import psycopg

CARPETA_MIGRACIONES = Path(__file__).parent / "migrations"


def aplicar_migraciones(conn: psycopg.Connection, carpeta: Path = CARPETA_MIGRACIONES) -> list[str]:
    """Aplica, cada una en su propia transacción, las migraciones que falten.

    Args:
        conn: conexión a PostgreSQL.
        carpeta: carpeta con archivos ``NNN_nombre.sql``.

    Returns:
        Versiones aplicadas en esta llamada (vacía si ya estaban todas).
    """
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS migraciones_aplicadas (
            version     text PRIMARY KEY,
            aplicada_en timestamptz NOT NULL DEFAULT now()
        )
        """
    )
    ya_aplicadas = {fila[0] for fila in conn.execute("SELECT version FROM migraciones_aplicadas")}
    aplicadas: list[str] = []
    for archivo in sorted(carpeta.glob("*.sql")):
        version = archivo.stem
        if version in ya_aplicadas:
            continue
        with conn.transaction():
            conn.execute(archivo.read_text(encoding="utf-8"))
            conn.execute("INSERT INTO migraciones_aplicadas (version) VALUES (%s)", (version,))
        aplicadas.append(version)
    return aplicadas


def main() -> int:
    """Punto de entrada de línea de comandos; lee la conexión de ``PASE_DB_URL``."""
    url = os.environ.get("PASE_DB_URL")
    if not url:
        print("Falta la variable PASE_DB_URL.", file=sys.stderr)
        return 2
    with psycopg.connect(url, autocommit=True) as conn:
        aplicadas = aplicar_migraciones(conn)
    print("Migraciones aplicadas: " + (", ".join(aplicadas) if aplicadas else "ninguna (al día)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
