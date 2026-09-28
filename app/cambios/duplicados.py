"""Criterios aprobados para avisar de posibles registros duplicados."""

from __future__ import annotations

import unicodedata
from datetime import date
from typing import Any


def _texto_normalizado(valor: Any) -> str:
    texto = " ".join(str(valor or "").split()).casefold()
    return "".join(
        caracter for caracter in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caracter) != "Mn"
    )


def _fecha(valor: Any) -> date | None:
    if not valor:
        return None
    try:
        return date.fromisoformat(str(valor))
    except ValueError:
        return None


def _resultado(area: str, fila: dict, resumen: str) -> dict:
    return {"area": area, "id": fila["id"], "resumen": resumen}


def buscar_posible_duplicado(conexion, area: str, valores: dict) -> dict | None:
    """Devuelve la primera coincidencia oficial según las reglas aprobadas."""
    if area == "oficinas":
        numero = valores.get("numero")
        if numero is None:
            return None
        fila = conexion.execute("SELECT * FROM oficinas WHERE numero = ? ORDER BY id LIMIT 1", (numero,)).fetchone()
        return _resultado(area, fila, f"Oficina {fila['numero']}") if fila else None

    if area == "inquilinos":
        titular = _texto_normalizado(valores.get("titular"))
        contacto = valores.get("contacto")
        for fila in conexion.execute("SELECT * FROM inquilinos ORDER BY id").fetchall():
            if titular and titular == _texto_normalizado(fila["titular"]):
                return _resultado(area, fila, f"Inquilino {fila['titular']}")
            if contacto is not None and contacto == fila["contacto"]:
                return _resultado(area, fila, f"Inquilino {fila['titular']}")
        return None

    if area == "contratos":
        inicio, fin = _fecha(valores.get("inicio")), _fecha(valores.get("fin"))
        if not inicio or not fin or inicio > fin:
            return None
        filas = conexion.execute(
            "SELECT * FROM contratos WHERE oficina_id = ? AND inquilino_id = ? ORDER BY id",
            (valores.get("oficina_id"), valores.get("inquilino_id")),
        ).fetchall()
        for fila in filas:
            inicio_existente, fin_existente = _fecha(fila["inicio"]), _fecha(fila["fin"])
            if inicio_existente and fin_existente and inicio <= fin_existente and inicio_existente <= fin:
                return _resultado(area, fila, f"Contrato {fila['id']}")
        return None

    if area == "pagos":
        fecha = _fecha(valores.get("fecha_pago"))
        precio = valores.get("precio")
        if not fecha or precio is None:
            return None
        filas = conexion.execute(
            "SELECT * FROM pagos WHERE contrato_id = ? AND precio = ? ORDER BY id",
            (valores.get("contrato_id"), precio),
        ).fetchall()
        for fila in filas:
            fecha_existente = _fecha(fila["fecha_pago"])
            if fecha_existente and (fecha.year, fecha.month) == (fecha_existente.year, fecha_existente.month):
                return _resultado(area, fila, f"Pago {fila['id']}")
        return None

    raise ValueError("El área indicada no es válida.")
