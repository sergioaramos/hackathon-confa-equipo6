"""Configuración compartida y guardas de seguridad."""

from collections.abc import Mapping

MODO_FACIAL_POR_DEFECTO = "mock"


class ModoFacialInseguro(RuntimeError):
    """Se intentó correr pruebas automáticas contra la API facial real de CONFA."""


def exigir_modo_facial_de_pruebas(entorno: Mapping[str, str]) -> None:
    """Impide que las pruebas automáticas usen la API facial de producción (Req 13.8).

    La API de CONFA solo existe en producción, así que la suite debe correr siempre
    con el mock. Cualquier valor distinto de ``mock`` se rechaza, también los
    desconocidos, para fallar hacia el lado seguro.

    Args:
        entorno: variables de entorno (por ejemplo, ``os.environ``).

    Raises:
        ModoFacialInseguro: si ``FACIAL_MODO`` tiene un valor distinto de ``mock``.
    """
    modo = entorno.get("FACIAL_MODO", MODO_FACIAL_POR_DEFECTO).strip().lower()
    if modo != MODO_FACIAL_POR_DEFECTO:
        raise ModoFacialInseguro(
            f"FACIAL_MODO={modo!r}: las pruebas automáticas solo corren con el mock "
            "de la API facial. La API real de CONFA es de producción."
        )
