from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.cambios.servicio import crear_pendiente
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
    observaciones: Optional[str] = None


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


def _pendiente(operacion: str, actor, valores: dict, contrato_id: int | None = None) -> dict:
    solicitante = getattr(actor, "solicitante", None)
    if solicitante is None:
        raise HTTPException(status_code=403, detail="No se identificó a la persona que solicitó el cambio.")
    try:
        cambio = crear_pendiente(
            area="contratos", operacion=operacion, registro_id=contrato_id,
            valores_nuevos=valores, observaciones=valores.pop("observaciones", None),
            solicitante=solicitante, ejecutor=solicitante if actor.ejecutor == "dashboard" else actor.ejecutor,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"id": cambio["id"], "resumen": f"Cambio pendiente de confirmar para el contrato {contrato_id or ''}."}


@router.post("/api/contratos", status_code=201)
def crear_contrato(entrada: ContratoEntrada, actor=Depends(actor_actual)) -> dict:
    conexion = conectar_con_filas()
    try:
        _validar_referencias(conexion, entrada)
    finally:
        conexion.close()
    return _pendiente("alta", actor, entrada.model_dump())


@router.put("/api/contratos/{contrato_id}")
def editar_contrato(
    contrato_id: int, entrada: ContratoEntrada, actor: str = Depends(actor_actual)
) -> dict:
    conexion = conectar_con_filas()
    try:
        _obtener(conexion, contrato_id)
        _validar_referencias(conexion, entrada)
    finally:
        conexion.close()
    return _pendiente("modificacion", actor, entrada.model_dump(), contrato_id)


@router.delete("/api/contratos/{contrato_id}")
def eliminar_contrato(contrato_id: int, observaciones: str | None = None, actor=Depends(actor_actual)) -> dict:
    conexion = conectar_con_filas()
    try:
        _obtener(conexion, contrato_id)
    finally:
        conexion.close()
    return _pendiente("baja", actor, {"observaciones": observaciones}, contrato_id)
