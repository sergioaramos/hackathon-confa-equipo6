"""Carga del modelo de Bedrock del asistente de eventos (design.md, Modelos de Bedrock)."""

import os

from strands.models.bedrock import BedrockModel

MODELO_POR_DEFECTO = "us.anthropic.claude-haiku-4-5-20251001-v1:0"


def load_model() -> BedrockModel:
    """Devuelve el cliente de Bedrock con Claude Haiku 4.5 y temperatura 0.

    El ID sale de la variable de entorno ``MODELO_BEDROCK`` (perfil de inferencia
    ``us.``); si no está, se usa Claude Haiku 4.5. Las credenciales salen del rol
    de IAM del Runtime o del perfil local, nunca del código.

    Returns:
        BedrockModel configurado para el agente.
    """
    model_id = os.getenv("MODELO_BEDROCK", MODELO_POR_DEFECTO)
    return BedrockModel(model_id=model_id, temperature=0)
