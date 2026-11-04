"""Semilla ficticia para desarrollo y pruebas (Req 13.8: solo datos ficticios).

Los documentos usan el rango 99000000NN para no coincidir con cédulas reales conocidas.
Los integrantes del equipo que autorizan su rostro NO van aquí: se cargan aparte, fuera
del repositorio, para no versionar datos personales reales.

Uso: ``PASE_DB_URL=postgresql://... uv run python -m db.sembrar``
"""

import os
import sys
import uuid
from datetime import date, time

import psycopg

SEDE_DEMO_ID = uuid.UUID("5ede0000-0000-4000-8000-000000000001")
EVENTO_DEMO_ID = uuid.UUID("e0e00000-0000-4000-8000-000000000001")
EVENTO_INTERNO_ID = uuid.UUID("e0e00000-0000-4000-8000-000000000002")

SUB_ORGANIZADOR_DEMO = "sub-organizador-demo"
SUB_LOGISTICO_DEMO = "sub-logistico-demo"
SUB_PUNTO_FIJO_DEMO = "sub-punto-fijo-demo"

_INSCRITOS: list[tuple[str, str, str, str, bool]] = [
    # tipo_doc, numero_doc, nombre, empresa, es_menor
    ("C", "9900000001", "Ana Gómez", "Arquitectos S.A.", False),
    ("C", "9900000002", "Luis Mora", "Arquitectos S.A.", False),
    ("C", "9900000003", "Marta Ríos", "Arquitectos S.A.", False),
    ("C", "9900000004", "Jorge Salazar", "Arquitectos S.A.", False),
    ("C", "9900000005", "Paula Henao", "Arquitectos S.A.", False),
    ("C", "9900000006", "Andrés Ocampo", "Arquitectos S.A.", False),
    ("C", "9900000007", "Lucía Giraldo", "Arquitectos S.A.", False),
    ("C", "9900000008", "Camilo Arango", "Arquitectos S.A.", False),
    ("C", "9900000009", "Sofía Duque", "Arquitectos S.A.", False),
    ("C", "9900000010", "Mateo Valencia", "Arquitectos S.A.", False),
    ("C", "9900000011", "Valentina Osorio", "Café Caldas", False),
    ("C", "9900000012", "Santiago Cardona", "Café Caldas", False),
    ("C", "9900000013", "Isabel Restrepo", "Café Caldas", False),
    ("C", "9900000014", "Daniel Marín", "Café Caldas", False),
    ("C", "9900000015", "Laura Castaño", "Café Caldas", False),
    ("E", "9900000016", "Miguel Torres", "Café Caldas", False),
    ("C", "9900000017", "Carolina López", "Café Caldas", False),
    ("C", "9900000018", "Felipe Quintero", "Café Caldas", False),
    ("P", "9900000019", "Daniela Ruiz", "Café Caldas", False),
    ("T", "9900000020", "Tomás Gómez", "Arquitectos S.A.", True),
]

_SOLO_IDENTIDAD_CONFA: list[tuple[str, str, str]] = [
    ("C", "9900000021", "Rosa Bedoya"),
    ("C", "9900000022", "Hernán Zuluaga"),
]

_PERSONAL: list[tuple[str, str, str]] = [
    (SUB_ORGANIZADOR_DEMO, "organizador.demo@ejemplo.com", "Organizador Demo"),
    (SUB_LOGISTICO_DEMO, "logistico.demo@ejemplo.com", "Logístico Demo"),
    (SUB_PUNTO_FIJO_DEMO, "punto.fijo.demo@ejemplo.com", "Punto Fijo Demo"),
]


def sembrar(conn: psycopg.Connection) -> None:
    """Carga el escenario de demo; se puede correr varias veces sin duplicar.

    Escenario: 1 sede (aforo 400), 1 evento externo presencial abierto (cupo 300)
    con 20 inscritos (1 menor), 1 evento interno, 2 personas solo en la identidad de
    CONFA y personal de prueba con roles por evento.

    Args:
        conn: conexión a una base con las migraciones aplicadas.
    """
    with conn.transaction():
        conn.execute(
            "INSERT INTO sedes (id, nombre, aforo) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
            (SEDE_DEMO_ID, "La Rochela", 400),
        )
        for evento_id, nombre, tipo, cupo in (
            (EVENTO_DEMO_ID, "Encuentro de afiliados Arquitectos S.A.", "externo", 300),
            (EVENTO_INTERNO_ID, "Encuentro con el Director", "interno", 100),
        ):
            conn.execute(
                """
                INSERT INTO eventos (id, nombre, fecha, hora, sede_id, tipo, cupo, creado_por)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                """,
                (evento_id, nombre, date(2026, 11, 7), time(9, 0), SEDE_DEMO_ID, tipo, cupo,
                 SUB_ORGANIZADOR_DEMO),
            )
        for tipo_doc, numero_doc, nombre, _empresa, es_menor in _INSCRITOS:
            conn.execute(
                """
                INSERT INTO personas (tipo_doc, numero_doc, nombre, es_menor, origen)
                VALUES (%s, %s, %s, %s, 'confa') ON CONFLICT DO NOTHING
                """,
                (tipo_doc, numero_doc, nombre, es_menor),
            )
        for tipo_doc, numero_doc, nombre in _SOLO_IDENTIDAD_CONFA:
            conn.execute(
                """
                INSERT INTO personas (tipo_doc, numero_doc, nombre, origen)
                VALUES (%s, %s, %s, 'confa') ON CONFLICT DO NOTHING
                """,
                (tipo_doc, numero_doc, nombre),
            )
        for tipo_doc, numero_doc, nombre, empresa, _es_menor in _INSCRITOS:
            conn.execute(
                """
                INSERT INTO inscripciones (evento_id, tipo_doc, numero_doc, nombre_cargado, empresa)
                VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
                """,
                (EVENTO_DEMO_ID, tipo_doc, numero_doc, nombre, empresa),
            )
        for sub, email, nombre in _PERSONAL:
            conn.execute(
                "INSERT INTO personal (sub, email, nombre) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                (sub, email, nombre),
            )
        for sub, evento_id, rol in (
            (SUB_ORGANIZADOR_DEMO, EVENTO_DEMO_ID, "organizador"),
            (SUB_LOGISTICO_DEMO, EVENTO_DEMO_ID, "logistico"),
            (SUB_PUNTO_FIJO_DEMO, EVENTO_DEMO_ID, "punto_fijo"),
            (SUB_ORGANIZADOR_DEMO, EVENTO_INTERNO_ID, "organizador"),
        ):
            conn.execute(
                """
                INSERT INTO personal_eventos (sub, evento_id, rol, asignado_por)
                VALUES (%s, %s, %s, 'semilla') ON CONFLICT DO NOTHING
                """,
                (sub, evento_id, rol),
            )


def main() -> int:
    """Punto de entrada de línea de comandos; lee la conexión de ``PASE_DB_URL``."""
    url = os.environ.get("PASE_DB_URL")
    if not url:
        print("Falta la variable PASE_DB_URL.", file=sys.stderr)
        return 2
    with psycopg.connect(url, autocommit=True) as conn:
        sembrar(conn)
    print("Semilla ficticia cargada.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
