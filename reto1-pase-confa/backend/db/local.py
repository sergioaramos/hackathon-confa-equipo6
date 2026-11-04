"""PostgreSQL local para desarrollo, sin Docker (pgserver embebido).

Uso: ``uv run python -m db.local`` levanta el servidor en ``backend/.pgdata``
(no se versiona), aplica las migraciones, carga la semilla ficticia e imprime
la URL para usarla como ``PASE_DB_URL``.
"""

import sys
from pathlib import Path

import pgserver
import psycopg

from db.migrar import aplicar_migraciones
from db.sembrar import sembrar

CARPETA_DATOS = Path(__file__).resolve().parent.parent / ".pgdata"


def levantar() -> str:
    """Levanta (o reutiliza) el servidor local y deja la base lista.

    Returns:
        URL de conexión al servidor local.
    """
    servidor = pgserver.get_server(CARPETA_DATOS, cleanup_mode=None)
    url = servidor.get_uri()
    with psycopg.connect(url, autocommit=True) as conn:
        aplicadas = aplicar_migraciones(conn)
        sembrar(conn)
    print("Migraciones aplicadas: " + (", ".join(aplicadas) if aplicadas else "ninguna (al día)"))
    print("Semilla ficticia cargada.")
    return url


if __name__ == "__main__":
    print(f"PASE_DB_URL={levantar()}")
    sys.exit(0)
