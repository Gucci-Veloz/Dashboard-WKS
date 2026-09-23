import sqlite3
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.actividad.registrar import registrar
from app.db.conexion import conectar
from app.seguridad.actor import actor_actual

router = APIRouter()

MENSAJE_NO_EXISTE = "No existe una oficina con ese número de registro."


class OficinaEntrada(BaseModel):
    tipo: Optional[str] = None
    numero: Optional[str] = None
    piso: Optional[str] = None
    m2: Optional[float] = None
    estatus: Optional[str] = None
    extras: Optional[str] = None


def _conectar_con_filas() -> sqlite3.Connection:
    conexion = conectar()
    conexion.row_factory = sqlite3.Row
    return conexion


def _obtener(conexion, oficina_id: int):
    fila = conexion.execute("SELECT * FROM oficinas WHERE id = ?", (oficina_id,)).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail=MENSAJE_NO_EXISTE)
    return dict(fila)


@router.get("/api/oficinas")
def listar_oficinas() -> list:
    conexion = _conectar_con_filas()
    try:
        filas = conexion.execute("SELECT * FROM oficinas ORDER BY id").fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/api/oficinas/{oficina_id}")
def ver_oficina(oficina_id: int) -> dict:
    conexion = _conectar_con_filas()
    try:
        return _obtener(conexion, oficina_id)
    finally:
        conexion.close()


@router.post("/api/oficinas", status_code=201)
def crear_oficina(entrada: OficinaEntrada, actor: str = Depends(actor_actual)) -> dict:
    conexion = _conectar_con_filas()
    try:
        cursor = conexion.execute(
            """
            INSERT INTO oficinas (tipo, numero, piso, m2, estatus, origen_dato, extras)
            VALUES (?, ?, ?, ?, ?, 'manual', ?)
            """,
            (entrada.tipo, entrada.numero, entrada.piso, entrada.m2, entrada.estatus, entrada.extras),
        )
        conexion.commit()
        oficina_id = cursor.lastrowid
        oficina = _obtener(conexion, oficina_id)
    finally:
        conexion.close()

    registrar(
        actor=actor,
        tipo="solicitada",
        accion="crear_oficina",
        area="oficinas",
        referencia=str(oficina_id),
        resumen=f"Se creó la oficina {entrada.numero or oficina_id}.",
        origen_dato="real",
    )
    return oficina


@router.put("/api/oficinas/{oficina_id}")
def editar_oficina(
    oficina_id: int, entrada: OficinaEntrada, actor: str = Depends(actor_actual)
) -> dict:
    conexion = _conectar_con_filas()
    try:
        _obtener(conexion, oficina_id)
        conexion.execute(
            """
            UPDATE oficinas
            SET tipo = ?, numero = ?, piso = ?, m2 = ?, estatus = ?, extras = ?,
                actualizado_en = datetime('now')
            WHERE id = ?
            """,
            (
                entrada.tipo,
                entrada.numero,
                entrada.piso,
                entrada.m2,
                entrada.estatus,
                entrada.extras,
                oficina_id,
            ),
        )
        conexion.commit()
        oficina = _obtener(conexion, oficina_id)
    finally:
        conexion.close()

    registrar(
        actor=actor,
        tipo="solicitada",
        accion="editar_oficina",
        area="oficinas",
        referencia=str(oficina_id),
        resumen=f"Se editó la oficina {entrada.numero or oficina_id}.",
        origen_dato="real",
    )
    return oficina


@router.delete("/api/oficinas/{oficina_id}", status_code=204)
def eliminar_oficina(oficina_id: int, actor: str = Depends(actor_actual)) -> None:
    conexion = _conectar_con_filas()
    try:
        _obtener(conexion, oficina_id)
        conexion.execute("DELETE FROM oficinas WHERE id = ?", (oficina_id,))
        conexion.commit()
    finally:
        conexion.close()

    registrar(
        actor=actor,
        tipo="solicitada",
        accion="eliminar_oficina",
        area="oficinas",
        referencia=str(oficina_id),
        resumen=f"Se eliminó la oficina {oficina_id}.",
        origen_dato="real",
    )
