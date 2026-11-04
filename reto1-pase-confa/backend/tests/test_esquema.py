"""Pruebas del esquema MVP y de la semilla ficticia (tarea 3; Req 1.5, 9.3, 13.1)."""

import uuid

import psycopg
import pytest
from psycopg import errors

from db.migrar import aplicar_migraciones
from db.sembrar import (
    EVENTO_DEMO_ID,
    EVENTO_INTERNO_ID,
    SUB_LOGISTICO_DEMO,
    sembrar,
)

TABLAS_MVP = {
    "personas",
    "eventos",
    "inscripciones",
    "asistencias",
    "consentimientos",
    "decisiones",
    "sedes",
    "personal",
    "personal_eventos",
}


@pytest.fixture
def bd(conexion: psycopg.Connection) -> psycopg.Connection:
    """Base con el esquema aplicado y la semilla cargada."""
    aplicar_migraciones(conexion)
    sembrar(conexion)
    return conexion


def _insertar_asistencia(conn: psycopg.Connection, canal: str = "presencial") -> None:
    conn.execute(
        """
        INSERT INTO asistencias (id, evento_id, tipo_doc, numero_doc, canal, metodo,
                                 puerta, validado_por)
        VALUES (%s, %s, 'C', '9900000001', %s, 'cedula', 'Puerta 1', %s)
        """,
        (uuid.uuid4(), EVENTO_DEMO_ID, canal, SUB_LOGISTICO_DEMO),
    )


def test_migraciones_crean_las_tablas_mvp_y_son_idempotentes(conexion: psycopg.Connection) -> None:
    aplicar_migraciones(conexion)
    aplicar_migraciones(conexion)

    tablas = {
        fila[0]
        for fila in conexion.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        )
    }
    assert TABLAS_MVP <= tablas
    aplicadas = conexion.execute("SELECT count(*) FROM migraciones_aplicadas").fetchone()[0]
    assert aplicadas == 1


def test_segundo_ingreso_por_el_mismo_canal_se_rechaza(bd: psycopg.Connection) -> None:
    _insertar_asistencia(bd)

    with pytest.raises(errors.UniqueViolation):
        _insertar_asistencia(bd)


def test_la_misma_persona_puede_tener_un_registro_por_canal(bd: psycopg.Connection) -> None:
    _insertar_asistencia(bd, canal="presencial")
    _insertar_asistencia(bd, canal="virtual")

    total = bd.execute("SELECT count(*) FROM asistencias").fetchone()[0]
    assert total == 2


def test_ingreso_por_rostro_exige_constancia_de_consentimiento(bd: psycopg.Connection) -> None:
    with pytest.raises(errors.CheckViolation):
        bd.execute(
            """
            INSERT INTO asistencias (id, evento_id, tipo_doc, numero_doc, canal, metodo,
                                     puerta, validado_por)
            VALUES (%s, %s, 'C', '9900000001', 'presencial', 'rostro', 'Puerta 1', %s)
            """,
            (uuid.uuid4(), EVENTO_DEMO_ID, SUB_LOGISTICO_DEMO),
        )


def test_constancia_no_guarda_documento_si_no_hubo_reconocimiento(bd: psycopg.Connection) -> None:
    with pytest.raises(errors.CheckViolation):
        bd.execute(
            """
            INSERT INTO consentimientos (evento_id, puerta, usuario, modo, quien_acepto,
                                         version_aviso, mayor_de_edad_declarado, resultado,
                                         tipo_doc, numero_doc)
            VALUES (%s, 'Puerta 1', %s, 'logistico', 'logistico', 'borrador-2026-11-04',
                    true, 'NO_RECONOCIDO', 'C', '9900000001')
            """,
            (EVENTO_DEMO_ID, SUB_LOGISTICO_DEMO),
        )


def test_persona_de_la_identidad_confa_no_guarda_telefono_ni_correo(bd: psycopg.Connection) -> None:
    with pytest.raises(errors.CheckViolation):
        bd.execute(
            """
            INSERT INTO personas (tipo_doc, numero_doc, nombre, telefono, origen)
            VALUES ('C', '1099999999', 'Persona de Prueba', '3000000000', 'confa')
            """
        )


@pytest.mark.parametrize("numero", ["1234", "1234567890123", "10.538.465"])
def test_documento_fuera_de_formato_se_rechaza(bd: psycopg.Connection, numero: str) -> None:
    with pytest.raises(errors.CheckViolation):
        bd.execute(
            "INSERT INTO personas (tipo_doc, numero_doc, nombre, origen) VALUES ('C', %s, 'X', 'confa')",
            (numero,),
        )


def test_esquema_no_tiene_columnas_de_imagen_biometria_ni_salud(bd: psycopg.Connection) -> None:
    columnas = [
        fila[0].lower()
        for fila in bd.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public'"
        )
    ]
    prohibidas = ("imagen", "foto", "img", "plantilla", "biometr", "pcr", "diagnost", "salud")
    encontradas = [c for c in columnas if any(p in c for p in prohibidas)]
    assert encontradas == []


def test_semilla_carga_el_escenario_de_demo(bd: psycopg.Connection) -> None:
    evento = bd.execute(
        "SELECT tipo, modalidad, estado, cupo FROM eventos WHERE id = %s", (EVENTO_DEMO_ID,)
    ).fetchone()
    assert evento == ("externo", "presencial", "abierto", 300)

    inscritos = bd.execute(
        "SELECT count(*) FROM inscripciones WHERE evento_id = %s", (EVENTO_DEMO_ID,)
    ).fetchone()[0]
    assert inscritos == 20

    menores = bd.execute(
        """
        SELECT count(*) FROM inscripciones i
        JOIN personas p USING (tipo_doc, numero_doc)
        WHERE i.evento_id = %s AND p.es_menor
        """,
        (EVENTO_DEMO_ID,),
    ).fetchone()[0]
    assert menores == 1

    solo_identidad = bd.execute(
        """
        SELECT count(*) FROM personas p
        WHERE p.origen = 'confa' AND NOT EXISTS (
            SELECT 1 FROM inscripciones i
            WHERE i.tipo_doc = p.tipo_doc AND i.numero_doc = p.numero_doc
        )
        """
    ).fetchone()[0]
    assert solo_identidad == 2

    aforo = bd.execute(
        "SELECT s.aforo FROM eventos e JOIN sedes s ON s.id = e.sede_id WHERE e.id = %s",
        (EVENTO_DEMO_ID,),
    ).fetchone()[0]
    assert aforo == 400


def test_semilla_asigna_roles_por_evento(bd: psycopg.Connection) -> None:
    roles_demo = {
        fila[0]
        for fila in bd.execute(
            "SELECT rol FROM personal_eventos WHERE evento_id = %s", (EVENTO_DEMO_ID,)
        )
    }
    assert roles_demo == {"organizador", "logistico", "punto_fijo"}

    logistico_en_interno = bd.execute(
        "SELECT count(*) FROM personal_eventos WHERE sub = %s AND evento_id = %s",
        (SUB_LOGISTICO_DEMO, EVENTO_INTERNO_ID),
    ).fetchone()[0]
    assert logistico_en_interno == 0


def test_semilla_es_idempotente(bd: psycopg.Connection) -> None:
    sembrar(bd)

    inscritos = bd.execute(
        "SELECT count(*) FROM inscripciones WHERE evento_id = %s", (EVENTO_DEMO_ID,)
    ).fetchone()[0]
    assert inscritos == 20
