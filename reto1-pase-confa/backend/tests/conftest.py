"""Base de datos de pruebas: PostgreSQL embebido (pgserver), limpio en cada prueba.

Si se define ``PASE_DB_URL_PRUEBAS``, se usa esa base en lugar del servidor embebido.
Nunca apuntes esa variable a la RDS del evento: cada prueba borra el esquema.
"""

import os
from collections.abc import Iterator

import psycopg
import pytest


@pytest.fixture(scope="session")
def url_bd(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    """URL de una base PostgreSQL desechable para toda la sesión de pruebas."""
    externa = os.environ.get("PASE_DB_URL_PRUEBAS")
    if externa:
        yield externa
        return
    import pgserver

    servidor = pgserver.get_server(tmp_path_factory.mktemp("pgdata"), cleanup_mode="stop")
    try:
        yield servidor.get_uri()
    finally:
        servidor.cleanup()


@pytest.fixture
def conexion(url_bd: str) -> Iterator[psycopg.Connection]:
    """Conexión con el esquema ``public`` vacío; cada prueba aplica lo que necesita."""
    with psycopg.connect(url_bd, autocommit=True) as conn:
        conn.execute("DROP SCHEMA IF EXISTS public CASCADE")
        conn.execute("CREATE SCHEMA public")
        yield conn
