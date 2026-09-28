"""Reglas de identidad para las escrituras solicitadas a Vania."""

from __future__ import annotations

from fastapi import HTTPException

from app.seguridad.sesion import persona_de_sesion, persona_por_whatsapp


def solicitante_con_sesion(numero_whatsapp: str | None, token_sesion: str | None) -> str:
    """Resuelve a quien instruyó a Vania y exige que sea su propia sesión."""
    persona = persona_por_whatsapp(numero_whatsapp)
    if persona is None:
        raise HTTPException(status_code=403)
    if persona_de_sesion(token_sesion) != persona:
        raise HTTPException(status_code=401, detail={"codigo": "sin_sesion"})
    return persona
