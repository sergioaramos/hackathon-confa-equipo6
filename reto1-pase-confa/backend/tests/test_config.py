"""Pruebas de la guarda que impide correr pruebas contra la API facial de producción (Req 13.8)."""

import pytest

from comun.config import ModoFacialInseguro, exigir_modo_facial_de_pruebas


def test_sin_variable_se_permite_porque_el_modo_por_defecto_es_mock() -> None:
    exigir_modo_facial_de_pruebas({})


def test_modo_mock_se_permite() -> None:
    exigir_modo_facial_de_pruebas({"FACIAL_MODO": "mock"})


@pytest.mark.parametrize("valor", ["real", "REAL", " Real "])
def test_modo_real_se_rechaza(valor: str) -> None:
    with pytest.raises(ModoFacialInseguro):
        exigir_modo_facial_de_pruebas({"FACIAL_MODO": valor})


def test_modo_desconocido_se_rechaza() -> None:
    with pytest.raises(ModoFacialInseguro):
        exigir_modo_facial_de_pruebas({"FACIAL_MODO": "produccion"})
