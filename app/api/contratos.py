from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.actividad.registrar import registrar
from app.db.conexion import conectar_con_filas
from app.seguridad.actor import actor_actual

router = APIRouter()

MENSAJE_NO_EXISTE = "No existe un contrato con ese número de registro."
MENSAJE_OFICINA_INEXISTENTE = "La oficina indicada no existe."
MENSAJE_INQUILINO_INEXISTENTE = "El inquilino indicado no existe."


class ContratoEntrada(BaseModel):
    oficina_id: Optional[int] = None
    inquilino_id: Optional[int] = None
    inicio: Optional[str] = None
    fin: Optional[str] = None
    alerta_renovacion: Optional[str] = None
    extras: Optional[str] = None


def _obtener(conexion, contrato_id: int):
    fila = conexion.execute("SELECT * FROM contratos WHERE id = ?", (contrato_id,)).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail=MENSAJE_NO_EXISTE)
    return dict(fila)


def _validar_referencias(conexion, entrada: ContratoEntrada) -> None:
    if entrada.oficina_id is not None:
        existe = conexion.execute(
            "SELECT 1 FROM oficinas WHERE id = ?", (entrada.oficina_id,)
        ).fetchone()
        if existe is None:
            raise HTTPException(status_code=400, detail=MENSAJE_OFICINA_INEXISTENTE)
    if entrada.inquilino_id is not None:
        existe = conexion.execute(
            "SELECT 1 FROM inquilinos WHERE id = ?", (entrada.inquilino_id,)
        ).fetchone()
        if existe is None:
            raise HTTPException(status_code=400, detail=MENSAJE_INQUILINO_INEXISTENTE)


@router.get("/api/contratos")
def listar_contratos() -> list:
    conexion = conectar_con_filas()
    try:
        filas = conexion.execute("SELECT * FROM contratos ORDER BY id").fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/api/contratos/{contrato_id}")
def ver_contrato(contrato_id: int) -> dict:
    conexion = conectar_con_filas()
    try:
        return _obtener(conexion, contrato_id)
    finally:
        conexion.close()


@router.post("/api/contratos", status_code=201)
def crear_contrato(entrada: ContratoEntrada, actor: str = Depends(actor_actual)) -> dict:
    conexion = conectar_con_filas()
    try:
        _validar_referencias(conexion, entrada)
        cursor = conexion.execute(
            """
            INSERT INTO contratos
                (oficina_id, inquilino_id, inicio, fin, alerta_renovacion, origen_dato, extras)
            VALUES (?, ?, ?, ?, ?, 'manual', ?)
            """,
            (
                entrada.oficina_id,
                entrada.inquilino_id,
                entrada.inicio,
                entrada.fin,
                entrada.alerta_renovacion,
                entrada.extras,
            ),
        )
        conexion.commit()
        contrato_id = cursor.lastrowid
        contrato = _obtener(conexion, contrato_id)
    finally:
        conexion.close()

    registrar(
        actor=actor,
        tipo="solicitada",
        accion="crear_contrato",
        area="contratos",
        referencia=str(contrato_id),
        resumen=f"Se creó el contrato {contrato_id}.",
        origen_dato="real",
    )
    return contrato


@router.put("/api/contratos/{contrato_id}")
def editar_contrato(
    contrato_id: int, entrada: ContratoEntrada, actor: str = Depends(actor_actual)
) -> dict:
    conexion = conectar_con_filas()
    try:
        _obtener(conexion, contrato_id)
        _validar_referencias(conexion, entrada)
        conexion.execute(
            """
            UPDATE contratos
            SET oficina_id = ?, inquilino_id = ?, inicio = ?, fin = ?, alerta_renovacion = ?,
                extras = ?, actualizado_en = datetime('now')
            WHERE id = ?
            """,
            (
                entrada.oficina_id,
                entrada.inquilino_id,
                entrada.inicio,
                entrada.fin,
                entrada.alerta_renovacion,
                entrada.extras,
                contrato_id,
            ),
        )
        conexion.commit()
        contrato = _obtener(conexion, contrato_id)
    finally:
        conexion.close()

    registrar(
        actor=actor,
        tipo="solicitada",
        accion="editar_contrato",
        area="contratos",
        referencia=str(contrato_id),
        resumen=f"Se editó el contrato {contrato_id}.",
        origen_dato="real",
    )
    return contrato


@router.delete("/api/contratos/{contrato_id}", status_code=204)
def eliminar_contrato(contrato_id: int, actor: str = Depends(actor_actual)) -> None:
    conexion = conectar_con_filas()
    try:
        _obtener(conexion, contrato_id)
        conexion.execute("DELETE FROM contratos WHERE id = ?", (contrato_id,))
        conexion.commit()
    finally:
        conexion.close()

    registrar(
        actor=actor,
        tipo="solicitada",
        accion="eliminar_contrato",
        area="contratos",
        referencia=str(contrato_id),
        resumen=f"Se eliminó el contrato {contrato_id}.",
        origen_dato="real",
    )
