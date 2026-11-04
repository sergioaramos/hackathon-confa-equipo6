"""Configuración global de pytest para el backend."""

import os

import pytest

from comun.config import ModoFacialInseguro, exigir_modo_facial_de_pruebas


def pytest_configure(config: pytest.Config) -> None:
    """Detiene la suite antes de correr si apunta a la API facial real (Req 13.8)."""
    try:
        exigir_modo_facial_de_pruebas(os.environ)
    except ModoFacialInseguro as error:
        raise pytest.UsageError(str(error)) from error
