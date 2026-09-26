"""Consulta del reporte diario a partir del historial de cambios."""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

from app.db.conexion import conectar_con_filas

ZONA_QUERETARO = ZoneInfo("America/Mexico_City")

_NOMBRES_AREA = {
    "oficinas": "oficina",
    "inquilinos": "inquilino",
    "contratos": "contrato",
    "pagos": "pago",
}
_NOMBRES_CAMPO = {
    "m2": "m²",
    "estatus_pago": "estatus",
}


def _momento_local(valor: str) -> datetime:
    momento = datetime.fromisoformat(valor.replace("Z", "+00:00"))
    if momento.tzinfo is None:
        momento = momento.replace(tzinfo=timezone.utc)
    return momento.astimezone(ZONA_QUERETARO)


def _valores(fila, columna: str) -> dict:
    return json.loads(fila[columna])


def _concepto(fila, nuevos: dict) -> str:
    if fila["area"] == "pagos":
        estatus = nuevos.get("estatus_pago") or _valores(fila, "valores_anteriores").get("estatus_pago")
        return str(estatus or "Pago").capitalize()
    nombre = _NOMBRES_AREA[fila["area"]]
    if fila["operacion"] == "alta":
        return f"Alta de {nombre}"
    if fila["operacion"] == "baja":
        return f"Baja de {nombre}"
    campo = next(iter(nuevos), None)
    return f"Cambio de {_NOMBRES_CAMPO.get(campo, campo or nombre)}"


def _inquilino(conexion, fila, nuevos: dict) -> str:
    if fila["area"] == "inquilinos":
        return nuevos.get("titular") or _valores(fila, "valores_anteriores").get("titular") or "—"

    anteriores = _valores(fila, "valores_anteriores")
    datos = {**anteriores, **nuevos}
    if fila["area"] == "contratos":
        inquilino_id = datos.get("inquilino_id")
    elif fila["area"] == "pagos":
        contrato_id = datos.get("contrato_id")
        contrato = conexion.execute(
            "SELECT inquilino_id FROM contratos WHERE id = ?", (contrato_id,)
        ).fetchone()
        inquilino_id = contrato["inquilino_id"] if contrato else None
    else:
        return "—"
    if inquilino_id is None:
        return "—"
    inquilino = conexion.execute(
        "SELECT titular FROM inquilinos WHERE id = ?", (inquilino_id,)
    ).fetchone()
    return inquilino["titular"] if inquilino and inquilino["titular"] else "—"


def reporte_del_dia(fecha: date | None = None) -> list[dict]:
    """Devuelve únicamente los cambios confirmados durante la fecha local indicada."""
    objetivo = fecha or datetime.now(ZONA_QUERETARO).date()
    conexion = conectar_con_filas()
    try:
        filas = conexion.execute(
            "SELECT * FROM cambios WHERE estado = 'confirmado' AND confirmado_en IS NOT NULL ORDER BY id"
        ).fetchall()
        reporte = []
        for fila in filas:
            momento = _momento_local(fila["confirmado_en"])
            if momento.date() != objetivo:
                continue
            nuevos = _valores(fila, "valores_nuevos")
            reporte.append({
                "id": fila["id"],
                "fecha": momento.strftime("%Y-%m-%d %H:%M"),
                "inquilino": _inquilino(conexion, fila, nuevos),
                "concepto": _concepto(fila, nuevos),
                "observaciones": fila["observaciones"],
                "solicitante": fila["solicitante"],
                "ejecutor": fila["ejecutor"],
            })
        return reporte
    finally:
        conexion.close()
