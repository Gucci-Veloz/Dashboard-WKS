from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.cambios.servicio import crear_pendiente
from app.cambios.duplicados import buscar_posible_duplicado
from app.db.conexion import conectar_con_filas
from app.seguridad.actor import actor_actual

router = APIRouter()

MENSAJE_NO_EXISTE = "No existe un pago con ese número de registro."
MENSAJE_CONTRATO_INEXISTENTE = "El contrato indicado no existe."
MENSAJE_SIN_PAGO_PENDIENTE = "No hay un pago pendiente para ese contrato."


class PagoEntrada(BaseModel):
    contrato_id: Optional[int] = None
    precio: Optional[float] = None
    deposito_garantia: Optional[float] = None
    fecha_pago: Optional[str] = None
    forma_pago: Optional[str] = None
    estatus_pago: Optional[str] = None
    extras: Optional[str] = None
    observaciones: Optional[str] = None
    crear_de_todos_modos: bool = False


class RegistrarPagoEntrada(BaseModel):
    contrato_id: int
    periodo: Optional[str] = None
    forma_pago: str
    observaciones: Optional[str] = None


def _obtener(conexion, pago_id: int):
    fila = conexion.execute("SELECT * FROM pagos WHERE id = ?", (pago_id,)).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail=MENSAJE_NO_EXISTE)
    return dict(fila)


def _validar_contrato(conexion, entrada: PagoEntrada) -> None:
    if entrada.contrato_id is not None:
        existe = conexion.execute(
            "SELECT 1 FROM contratos WHERE id = ?", (entrada.contrato_id,)
        ).fetchone()
        if existe is None:
            raise HTTPException(status_code=400, detail=MENSAJE_CONTRATO_INEXISTENTE)


def _numero_oficina_de_contrato(conexion, contrato_id: int) -> str:
    fila = conexion.execute(
        """
        SELECT oficinas.numero AS numero
        FROM contratos
        JOIN oficinas ON oficinas.id = contratos.oficina_id
        WHERE contratos.id = ?
        """,
        (contrato_id,),
    ).fetchone()
    return fila["numero"] if fila else "?"


@router.get("/api/pagos")
def listar_pagos() -> list:
    conexion = conectar_con_filas()
    try:
        filas = conexion.execute("SELECT * FROM pagos ORDER BY id").fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/api/pagos/{pago_id}")
def ver_pago(pago_id: int) -> dict:
    conexion = conectar_con_filas()
    try:
        return _obtener(conexion, pago_id)
    finally:
        conexion.close()


def _pendiente(operacion: str, actor, valores: dict, pago_id: int | None = None) -> dict:
    solicitante = getattr(actor, "solicitante", None)
    if solicitante is None:
        raise HTTPException(status_code=403, detail="No se identificó a la persona que solicitó el cambio.")
    try:
        cambio = crear_pendiente(
            area="pagos", operacion=operacion, registro_id=pago_id,
            valores_nuevos=valores, observaciones=valores.pop("observaciones", None),
            solicitante=solicitante, ejecutor=solicitante if actor.ejecutor == "dashboard" else actor.ejecutor,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"id": cambio["id"], "resumen": f"Cambio pendiente de confirmar para el pago {pago_id or ''}."}


@router.post("/api/pagos", status_code=201)
def crear_pago(entrada: PagoEntrada, actor=Depends(actor_actual)) -> dict:
    valores = entrada.model_dump(exclude={"crear_de_todos_modos"})
    conexion = conectar_con_filas()
    try:
        _validar_contrato(conexion, entrada)
        duplicado = buscar_posible_duplicado(conexion, "pagos", valores)
    finally:
        conexion.close()
    valores["estatus_pago"] = valores["estatus_pago"] or "pendiente"
    if duplicado and not entrada.crear_de_todos_modos:
        return JSONResponse(status_code=409, content={"mensaje": "Ya existe un registro similar. ¿Quieres revisarlo antes de crear otro?", "posible_duplicado": duplicado})
    return _pendiente("alta", actor, valores)


@router.put("/api/pagos/{pago_id}")
def editar_pago(pago_id: int, entrada: PagoEntrada, actor: str = Depends(actor_actual)) -> dict:
    conexion = conectar_con_filas()
    try:
        _obtener(conexion, pago_id)
        _validar_contrato(conexion, entrada)
    finally:
        conexion.close()
    return _pendiente(
        "modificacion", actor,
        entrada.model_dump(exclude={"crear_de_todos_modos"}), pago_id,
    )


@router.delete("/api/pagos/{pago_id}")
def eliminar_pago(pago_id: int, observaciones: str | None = None, actor=Depends(actor_actual)) -> dict:
    conexion = conectar_con_filas()
    try:
        _obtener(conexion, pago_id)
    finally:
        conexion.close()
    return _pendiente("baja", actor, {"observaciones": observaciones}, pago_id)


@router.post("/api/pagos/registrar")
def registrar_pago(entrada: RegistrarPagoEntrada, actor=Depends(actor_actual)) -> dict:
    """Marca como pagado el pago pendiente de un contrato. Es la operación que
    usan tanto el Dashboard como Vania (por ejemplo: "Vania, registra que la
    oficina 204 pagó septiembre por transferencia")."""
    conexion = conectar_con_filas()
    try:
        fila = conexion.execute(
            """
            SELECT * FROM pagos
            WHERE contrato_id = ? AND estatus_pago = 'pendiente'
            ORDER BY id LIMIT 1
            """,
            (entrada.contrato_id,),
        ).fetchone()
        if fila is None:
            raise HTTPException(status_code=404, detail=MENSAJE_SIN_PAGO_PENDIENTE)

        pago_id = fila["id"]
    finally:
        conexion.close()
    return _pendiente(
        "modificacion", actor,
        {"estatus_pago": "pagado", "forma_pago": entrada.forma_pago,
         "fecha_pago": date.today().isoformat(), "observaciones": entrada.observaciones},
        pago_id,
    )
