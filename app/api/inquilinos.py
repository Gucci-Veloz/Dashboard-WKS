from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.cambios.servicio import crear_pendiente
from app.db.conexion import conectar_con_filas
from app.seguridad.actor import actor_actual

router = APIRouter()

MENSAJE_NO_EXISTE = "No existe un inquilino con ese número de registro."


class InquilinoEntrada(BaseModel):
    titular: Optional[str] = None
    contacto: Optional[str] = None
    extras: Optional[str] = None
    observaciones: Optional[str] = None


def _obtener(conexion, inquilino_id: int):
    fila = conexion.execute("SELECT * FROM inquilinos WHERE id = ?", (inquilino_id,)).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail=MENSAJE_NO_EXISTE)
    return dict(fila)


@router.get("/api/inquilinos")
def listar_inquilinos() -> list:
    conexion = conectar_con_filas()
    try:
        filas = conexion.execute("SELECT * FROM inquilinos ORDER BY id").fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/api/inquilinos/{inquilino_id}")
def ver_inquilino(inquilino_id: int) -> dict:
    conexion = conectar_con_filas()
    try:
        return _obtener(conexion, inquilino_id)
    finally:
        conexion.close()


def _pendiente(operacion: str, actor, valores: dict, inquilino_id: int | None = None) -> dict:
    solicitante = getattr(actor, "solicitante", None)
    if solicitante is None:
        raise HTTPException(status_code=403, detail="No se identificó a la persona que solicitó el cambio.")
    try:
        cambio = crear_pendiente(
            area="inquilinos", operacion=operacion, registro_id=inquilino_id,
            valores_nuevos=valores, observaciones=valores.pop("observaciones", None),
            solicitante=solicitante, ejecutor=solicitante if actor.ejecutor == "dashboard" else actor.ejecutor,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"id": cambio["id"], "resumen": f"Cambio pendiente de confirmar para {valores.get('titular') or inquilino_id or 'el inquilino'}."}


@router.post("/api/inquilinos", status_code=201)
def crear_inquilino(entrada: InquilinoEntrada, actor=Depends(actor_actual)) -> dict:
    return _pendiente("alta", actor, entrada.model_dump())


@router.put("/api/inquilinos/{inquilino_id}")
def editar_inquilino(
    inquilino_id: int, entrada: InquilinoEntrada, actor: str = Depends(actor_actual)
) -> dict:
    conexion = conectar_con_filas()
    try:
        _obtener(conexion, inquilino_id)
    finally:
        conexion.close()
    return _pendiente("modificacion", actor, entrada.model_dump(), inquilino_id)


@router.delete("/api/inquilinos/{inquilino_id}")
def eliminar_inquilino(inquilino_id: int, observaciones: str | None = None, actor=Depends(actor_actual)) -> dict:
    conexion = conectar_con_filas()
    try:
        _obtener(conexion, inquilino_id)
    finally:
        conexion.close()
    return _pendiente("baja", actor, {"observaciones": observaciones}, inquilino_id)
