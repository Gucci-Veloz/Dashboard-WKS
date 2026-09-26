"""Enlaces de acceso y sesiones locales de Works."""

from __future__ import annotations

import hashlib
import json
import os
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi import HTTPException

from app.db.conexion import conectar, ruta_base_datos

ZONA_HORARIA = ZoneInfo("America/Mexico_City")
NOMBRE_COOKIE = "works_sesion"


def ahora() -> datetime:
    return datetime.now(ZONA_HORARIA)


def _hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def persona_por_whatsapp(numero: str | None) -> str | None:
    if not numero:
        return None
    for persona, telefono in leer_telefonos().items():
        if numero == telefono:
            return persona
    for persona in ("david", "grecia"):
        if numero == os.environ.get(f"WORKS_WHATSAPP_{persona.upper()}"):
            return persona
    return None


def ruta_telefonos() -> Path:
    """Devuelve la configuración local de teléfonos, siempre fuera del código."""
    configurada = os.environ.get("WORKS_CUENTAS_CONFIG")
    if configurada:
        return Path(configurada)
    return ruta_base_datos().parent / "works_cuentas.json"


def leer_telefonos() -> dict[str, str]:
    ruta = ruta_telefonos()
    if not ruta.is_file():
        return {}
    with ruta.open(encoding="utf-8") as archivo:
        datos = json.load(archivo)
    if not isinstance(datos, dict):
        return {}
    return {
        persona: telefono
        for persona, telefono in datos.items()
        if persona in {"david", "grecia"} and isinstance(telefono, str)
    }


def vencimiento_sesion(momento: datetime) -> datetime:
    local = momento.astimezone(ZONA_HORARIA)
    hora = 23 if local.hour >= 18 else 18
    minuto = 59 if local.hour >= 18 else 0
    segundo = 59 if local.hour >= 18 else 0
    return local.replace(hour=hora, minute=minuto, second=segundo, microsecond=0)


def crear_enlace(persona: str, momento: datetime | None = None) -> dict:
    momento = momento or ahora()
    token = secrets.token_urlsafe(32)
    vence_en = momento + timedelta(minutes=10)
    conexion = conectar()
    try:
        cuenta = conexion.execute(
            "SELECT activa FROM cuentas WHERE persona = ?", (persona,)
        ).fetchone()
        if cuenta is None or not cuenta[0]:
            raise HTTPException(status_code=403)
        conexion.execute(
            """
            INSERT INTO enlaces_acceso (persona, token_hash, creado_en, vence_en)
            VALUES (?, ?, ?, ?)
            """,
            (persona, _hash(token), momento.isoformat(), vence_en.isoformat()),
        )
        conexion.commit()
    finally:
        conexion.close()
    return {"token": token, "vence_en": vence_en.isoformat()}


def consumir_enlace(token: str, momento: datetime | None = None) -> dict:
    momento = momento or ahora()
    conexion = conectar()
    try:
        conexion.execute("BEGIN IMMEDIATE")
        enlace = conexion.execute(
            """
            SELECT id, persona, vence_en, usado_en FROM enlaces_acceso
            WHERE token_hash = ?
            """,
            (_hash(token),),
        ).fetchone()
        if enlace is None or enlace[3] is not None or datetime.fromisoformat(enlace[2]) < momento:
            conexion.rollback()
            raise HTTPException(status_code=401, detail={"codigo": "enlace_invalido"})
        sesion = secrets.token_urlsafe(32)
        vence_en = vencimiento_sesion(momento)
        conexion.execute(
            "UPDATE enlaces_acceso SET usado_en = ? WHERE id = ?",
            (momento.isoformat(), enlace[0]),
        )
        conexion.execute(
            """
            INSERT INTO sesiones (persona, token_hash, creado_en, vence_en)
            VALUES (?, ?, ?, ?)
            """,
            (enlace[1], _hash(sesion), momento.isoformat(), vence_en.isoformat()),
        )
        conexion.commit()
        return {"persona": enlace[1], "token": sesion, "vence_en": vence_en.isoformat()}
    finally:
        conexion.close()


def persona_de_sesion(token: str | None, momento: datetime | None = None) -> str | None:
    if not token:
        return None
    momento = momento or ahora()
    conexion = conectar()
    try:
        fila = conexion.execute(
            """
            SELECT sesiones.persona
            FROM sesiones JOIN cuentas ON cuentas.persona = sesiones.persona
            WHERE sesiones.token_hash = ? AND sesiones.revocada_en IS NULL
              AND sesiones.vence_en >= ? AND cuentas.activa = 1
            """,
            (_hash(token), momento.isoformat()),
        ).fetchone()
        return fila[0] if fila else None
    finally:
        conexion.close()
