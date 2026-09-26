from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.cambios.servicio import crear_pendiente
from app.cambios.duplicados import buscar_posible_duplicado
from app.db.conexion import conectar_con_filas
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
    observaciones: Optional[str] = None
    crear_de_todos_modos: bool = False


def _obtener(conexion, oficina_id: int):
    fila = conexion.execute("SELECT * FROM oficinas WHERE id = ?", (oficina_id,)).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail=MENSAJE_NO_EXISTE)
    return dict(fila)


@router.get("/api/oficinas")
def listar_oficinas() -> list:
    conexion = conectar_con_filas()
    try:
        filas = conexion.execute("SELECT * FROM oficinas ORDER BY id").fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/api/oficinas/{oficina_id}")
def ver_oficina(oficina_id: int) -> dict:
    conexion = conectar_con_filas()
    try:
        return _obtener(conexion, oficina_id)
    finally:
        conexion.close()


def _pendiente(operacion: str, actor, valores: dict, oficina_id: int | None = None) -> dict:
    solicitante = getattr(actor, "solicitante", None)
    if solicitante is None:
        raise HTTPException(status_code=403, detail="No se identificó a la persona que solicitó el cambio.")
    try:
        cambio = crear_pendiente(
            area="oficinas", operacion=operacion, registro_id=oficina_id,
            valores_nuevos=valores, observaciones=valores.pop("observaciones", None),
            solicitante=solicitante, ejecutor=solicitante if actor.ejecutor == "dashboard" else actor.ejecutor,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"id": cambio["id"], "resumen": f"Cambio pendiente de confirmar para la oficina {valores.get('numero') or oficina_id or ''}."}


@router.post("/api/oficinas", status_code=201)
def crear_oficina(entrada: OficinaEntrada, actor=Depends(actor_actual)) -> dict:
    valores = entrada.model_dump(exclude={"crear_de_todos_modos"})
    conexion = conectar_con_filas()
    try:
        duplicado = buscar_posible_duplicado(conexion, "oficinas", valores)
    finally:
        conexion.close()
    if duplicado and not entrada.crear_de_todos_modos:
        return JSONResponse(status_code=409, content={"mensaje": "Ya existe un registro similar. ¿Quieres revisarlo antes de crear otro?", "posible_duplicado": duplicado})
    return _pendiente("alta", actor, valores)


@router.put("/api/oficinas/{oficina_id}")
def editar_oficina(
    oficina_id: int, entrada: OficinaEntrada, actor: str = Depends(actor_actual)
) -> dict:
    conexion = conectar_con_filas()
    try:
        _obtener(conexion, oficina_id)
    finally:
        conexion.close()
    return _pendiente(
        "modificacion", actor,
        entrada.model_dump(exclude={"crear_de_todos_modos"}), oficina_id,
    )


@router.delete("/api/oficinas/{oficina_id}")
def eliminar_oficina(oficina_id: int, observaciones: str | None = None, actor=Depends(actor_actual)) -> dict:
    conexion = conectar_con_filas()
    try:
        _obtener(conexion, oficina_id)
    finally:
        conexion.close()
    return _pendiente("baja", actor, {"observaciones": observaciones}, oficina_id)
