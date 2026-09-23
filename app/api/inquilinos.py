import sqlite3
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.actividad.registrar import registrar
from app.db.conexion import conectar
from app.seguridad.actor import actor_actual

router = APIRouter()

MENSAJE_NO_EXISTE = "No existe un inquilino con ese número de registro."


class InquilinoEntrada(BaseModel):
    titular: Optional[str] = None
    contacto: Optional[str] = None
    extras: Optional[str] = None


def _conectar_con_filas() -> sqlite3.Connection:
    conexion = conectar()
    conexion.row_factory = sqlite3.Row
    return conexion


def _obtener(conexion, inquilino_id: int):
    fila = conexion.execute("SELECT * FROM inquilinos WHERE id = ?", (inquilino_id,)).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail=MENSAJE_NO_EXISTE)
    return dict(fila)


@router.get("/api/inquilinos")
def listar_inquilinos() -> list:
    conexion = _conectar_con_filas()
    try:
        filas = conexion.execute("SELECT * FROM inquilinos ORDER BY id").fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/api/inquilinos/{inquilino_id}")
def ver_inquilino(inquilino_id: int) -> dict:
    conexion = _conectar_con_filas()
    try:
        return _obtener(conexion, inquilino_id)
    finally:
        conexion.close()


@router.post("/api/inquilinos", status_code=201)
def crear_inquilino(entrada: InquilinoEntrada, actor: str = Depends(actor_actual)) -> dict:
    conexion = _conectar_con_filas()
    try:
        cursor = conexion.execute(
            """
            INSERT INTO inquilinos (titular, contacto, origen_dato, extras)
            VALUES (?, ?, 'manual', ?)
            """,
            (entrada.titular, entrada.contacto, entrada.extras),
        )
        conexion.commit()
        inquilino_id = cursor.lastrowid
        inquilino = _obtener(conexion, inquilino_id)
    finally:
        conexion.close()

    registrar(
        actor=actor,
        tipo="solicitada",
        accion="crear_inquilino",
        area="inquilinos",
        referencia=str(inquilino_id),
        resumen=f"Se creó el inquilino {entrada.titular or inquilino_id}.",
        origen_dato="real",
    )
    return inquilino


@router.put("/api/inquilinos/{inquilino_id}")
def editar_inquilino(
    inquilino_id: int, entrada: InquilinoEntrada, actor: str = Depends(actor_actual)
) -> dict:
    conexion = _conectar_con_filas()
    try:
        _obtener(conexion, inquilino_id)
        conexion.execute(
            """
            UPDATE inquilinos
            SET titular = ?, contacto = ?, extras = ?, actualizado_en = datetime('now')
            WHERE id = ?
            """,
            (entrada.titular, entrada.contacto, entrada.extras, inquilino_id),
        )
        conexion.commit()
        inquilino = _obtener(conexion, inquilino_id)
    finally:
        conexion.close()

    registrar(
        actor=actor,
        tipo="solicitada",
        accion="editar_inquilino",
        area="inquilinos",
        referencia=str(inquilino_id),
        resumen=f"Se editó el inquilino {entrada.titular or inquilino_id}.",
        origen_dato="real",
    )
    return inquilino


@router.delete("/api/inquilinos/{inquilino_id}", status_code=204)
def eliminar_inquilino(inquilino_id: int, actor: str = Depends(actor_actual)) -> None:
    conexion = _conectar_con_filas()
    try:
        _obtener(conexion, inquilino_id)
        conexion.execute("DELETE FROM inquilinos WHERE id = ?", (inquilino_id,))
        conexion.commit()
    finally:
        conexion.close()

    registrar(
        actor=actor,
        tipo="solicitada",
        accion="eliminar_inquilino",
        area="inquilinos",
        referencia=str(inquilino_id),
        resumen=f"Se eliminó el inquilino {inquilino_id}.",
        origen_dato="real",
    )
