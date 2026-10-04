"""Reglas de identidad para las escrituras solicitadas a Vania."""

from __future__ import annotations

from fastapi import HTTPException

from app.seguridad.sesion import persona_por_whatsapp, persona_tiene_sesion_vigente


def solicitante_con_sesion(numero_whatsapp: str | None) -> str:
    """Resuelve a quien instruyó a Vania y exige una sesión server-side propia."""
    persona = persona_por_whatsapp(numero_whatsapp)
    if persona is None:
        raise HTTPException(status_code=403)
    if not persona_tiene_sesion_vigente(persona):
        raise HTTPException(status_code=401, detail={"codigo": "sin_sesion"})
    return persona
