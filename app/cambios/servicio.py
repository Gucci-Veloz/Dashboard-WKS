"""Ciclo de cambios confirmado para las cuatro áreas del Dashboard."""

from __future__ import annotations

import json
from collections.abc import Mapping

from app.db.conexion import conectar_con_filas

AREAS = {
    "oficinas": {"tipo", "numero", "piso", "m2", "estatus", "origen_dato", "extras"},
    "inquilinos": {"titular", "contacto", "origen_dato", "extras"},
    "contratos": {
        "oficina_id",
        "inquilino_id",
        "inicio",
        "fin",
        "alerta_renovacion",
        "origen_dato",
        "extras",
    },
    "pagos": {
        "contrato_id",
        "precio",
        "deposito_garantia",
        "fecha_pago",
        "forma_pago",
        "estatus_pago",
        "origen_dato",
        "extras",
    },
}

OPERACIONES = {"alta", "modificacion", "baja"}
PERSONAS = {"david", "grecia"}
EJECUTORES = {*PERSONAS, "vania"}


def _validar_area(area: str) -> None:
    if area not in AREAS:
        raise ValueError("El área indicada no es válida.")


def _validar_valores(area: str, valores: Mapping | None) -> dict:
    resultado = dict(valores or {})
    desconocidos = set(resultado) - AREAS[area]
    if desconocidos:
        raise ValueError("El cambio incluye campos que no pertenecen al registro.")
    return resultado


def _registro_oficial(conexion, area: str, registro_id: int) -> dict:
    fila = conexion.execute(f"SELECT * FROM {area} WHERE id = ?", (registro_id,)).fetchone()
    if fila is None:
        raise ValueError("No existe el registro que se quiere cambiar.")
    return dict(fila)


def _serializar(valores: Mapping) -> str:
    return json.dumps(dict(valores), ensure_ascii=False, sort_keys=True)


def _fila_cambio(fila) -> dict:
    cambio = dict(fila)
    cambio["valores_anteriores"] = json.loads(cambio["valores_anteriores"])
    cambio["valores_nuevos"] = json.loads(cambio["valores_nuevos"])
    return cambio


def purgar_vencidos(conexion=None) -> int:
    propia = conexion is None
    if propia:
        conexion = conectar_con_filas()
    try:
        cursor = conexion.execute(
            "DELETE FROM cambios WHERE estado = 'pendiente' AND vence_en <= datetime('now')"
        )
        if propia:
            conexion.commit()
        return cursor.rowcount
    finally:
        if propia:
            conexion.close()


def crear_pendiente(
    *,
    area: str,
    operacion: str,
    solicitante: str,
    ejecutor: str,
    valores_nuevos: Mapping | None = None,
    registro_id: int | None = None,
    observaciones: str | None = None,
) -> dict:
    """Guarda una intención de cambio sin alterar el dato oficial."""
    _validar_area(area)
    if operacion not in OPERACIONES:
        raise ValueError("La operación indicada no es válida.")
    if solicitante not in PERSONAS:
        raise ValueError("El solicitante debe ser David o Grecia.")
    if ejecutor not in EJECUTORES:
        raise ValueError("El ejecutor indicado no es válido.")
    if operacion == "alta" and registro_id is not None:
        raise ValueError("Un alta no puede tener un registro previo.")
    if operacion != "alta" and registro_id is None:
        raise ValueError("Este cambio requiere el registro que se quiere modificar.")

    nuevos = _validar_valores(area, valores_nuevos)
    if operacion == "alta":
        nuevos.setdefault("origen_dato", "manual")

    conexion = conectar_con_filas()
    try:
        purgar_vencidos(conexion)
        anteriores = {} if operacion == "alta" else _registro_oficial(conexion, area, registro_id)
        cursor = conexion.execute(
            """
            INSERT INTO cambios (
                vence_en, estado, area, registro_id, operacion, valores_anteriores,
                valores_nuevos, observaciones, solicitante, ejecutor
            ) VALUES (datetime('now', '+24 hours'), 'pendiente', ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                area,
                registro_id,
                operacion,
                _serializar(anteriores),
                _serializar(nuevos),
                observaciones,
                solicitante,
                ejecutor,
            ),
        )
        conexion.commit()
        fila = conexion.execute("SELECT * FROM cambios WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return _fila_cambio(fila)
    finally:
        conexion.close()


def confirmar(cambio_id: int, persona: str) -> dict:
    """Confirma un pendiente y aplica su operación en la misma transacción."""
    if persona not in PERSONAS:
        raise ValueError("Solo David o Grecia pueden confirmar un cambio.")

    conexion = conectar_con_filas()
    try:
        candidato = conexion.execute(
            "SELECT * FROM cambios WHERE id = ? AND estado = 'pendiente'", (cambio_id,)
        ).fetchone()
        purgar_vencidos(conexion)
        if candidato is not None and candidato["vence_en"] <= conexion.execute(
            "SELECT datetime('now')"
        ).fetchone()[0]:
            conexion.commit()
            raise ValueError("El cambio pendiente venció y ya no se puede confirmar.")

        fila = conexion.execute(
            "SELECT * FROM cambios WHERE id = ? AND estado = 'pendiente'", (cambio_id,)
        ).fetchone()
        if fila is None:
            raise ValueError("No existe un cambio pendiente con ese número.")
        if fila["solicitante"] != persona:
            raise ValueError("Solo la persona que solicitó el cambio puede confirmarlo.")

        cambio = _fila_cambio(fila)
        area = cambio["area"]
        nuevos = cambio["valores_nuevos"]
        if cambio["operacion"] == "alta":
            columnas = list(nuevos)
            marcadores = ", ".join("?" for _ in columnas)
            cursor = conexion.execute(
                f"INSERT INTO {area} ({', '.join(columnas)}) VALUES ({marcadores})",
                [nuevos[columna] for columna in columnas],
            )
            registro_id = cursor.lastrowid
        elif cambio["operacion"] == "modificacion":
            _registro_oficial(conexion, area, cambio["registro_id"])
            asignaciones = [f"{columna} = ?" for columna in nuevos]
            asignaciones.append("actualizado_en = datetime('now')")
            conexion.execute(
                f"UPDATE {area} SET {', '.join(asignaciones)} WHERE id = ?",
                [nuevos[columna] for columna in nuevos] + [cambio["registro_id"]],
            )
            registro_id = cambio["registro_id"]
        else:
            _registro_oficial(conexion, area, cambio["registro_id"])
            conexion.execute(f"DELETE FROM {area} WHERE id = ?", (cambio["registro_id"],))
            registro_id = cambio["registro_id"]

        conexion.execute(
            """
            UPDATE cambios
            SET estado = 'confirmado', registro_id = ?, confirmado_en = datetime('now')
            WHERE id = ?
            """,
            (registro_id, cambio_id),
        )
        conexion.commit()
        confirmacion = conexion.execute("SELECT * FROM cambios WHERE id = ?", (cambio_id,)).fetchone()
        return _fila_cambio(confirmacion)
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def descartar(cambio_id: int, persona: str) -> dict:
    """Descarta un pendiente sin modificar el dato oficial."""
    if persona not in PERSONAS:
        raise ValueError("Solo David o Grecia pueden descartar un cambio.")

    conexion = conectar_con_filas()
    try:
        purgar_vencidos(conexion)
        fila = conexion.execute(
            "SELECT * FROM cambios WHERE id = ? AND estado = 'pendiente'", (cambio_id,)
        ).fetchone()
        if fila is None:
            raise ValueError("No existe un cambio pendiente con ese número.")
        if fila["solicitante"] != persona:
            raise ValueError("Solo la persona que solicitó el cambio puede descartarlo.")

        cambio = _fila_cambio(fila)
        conexion.execute("DELETE FROM cambios WHERE id = ?", (cambio_id,))
        conexion.commit()
        return cambio
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def pendientes(area: str, registro_id: int | None = None) -> list[dict]:
    _validar_area(area)
    conexion = conectar_con_filas()
    try:
        purgar_vencidos(conexion)
        consulta = "SELECT * FROM cambios WHERE area = ? AND estado = 'pendiente'"
        parametros: list = [area]
        if registro_id is not None:
            consulta += " AND registro_id = ?"
            parametros.append(registro_id)
        filas = conexion.execute(consulta + " ORDER BY id", parametros).fetchall()
        conexion.commit()
        return [_fila_cambio(fila) for fila in filas]
    finally:
        conexion.close()


def historial(area: str, registro_id: int) -> list[dict]:
    _validar_area(area)
    conexion = conectar_con_filas()
    try:
        purgar_vencidos(conexion)
        filas = conexion.execute(
            """
            SELECT * FROM cambios
            WHERE area = ? AND registro_id = ? AND estado = 'confirmado'
            ORDER BY id
            """,
            (area, registro_id),
        ).fetchall()
        conexion.commit()
        return [_fila_cambio(fila) for fila in filas]
    finally:
        conexion.close()
