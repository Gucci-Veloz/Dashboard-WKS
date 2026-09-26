"""Rutas para consultar y confirmar los cambios pendientes."""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException, Query

from app.actividad.registrar import registrar
from app.cambios.servicio import AREAS, confirmar, descartar, purgar_vencidos
from app.db.conexion import conectar_con_filas
from app.seguridad.actor import actor_actual

router = APIRouter()


def _cambio_publico(fila) -> dict:
    cambio = dict(fila)
    cambio["valores_anteriores"] = json.loads(cambio["valores_anteriores"])
    cambio["valores_nuevos"] = json.loads(cambio["valores_nuevos"])
    return cambio


@router.get("/api/cambios")
def listar_cambios(
    area: str | None = Query(default=None),
    registro_id: int | None = Query(default=None),
    estado: str = Query(default="pendiente"),
) -> list[dict]:
    if area is not None and area not in AREAS:
        raise HTTPException(status_code=400, detail="El área indicada no es válida.")
    if estado not in {"pendiente", "confirmado"}:
        raise HTTPException(status_code=400, detail="El estado indicado no es válido.")
    conexion = conectar_con_filas()
    try:
        purgar_vencidos(conexion)
        filtros = ["estado = ?"]
        parametros: list = [estado]
        if area is not None:
            filtros.append("area = ?")
            parametros.append(area)
        if registro_id is not None:
            filtros.append("registro_id = ?")
            parametros.append(registro_id)
        filas = conexion.execute(
            f"SELECT * FROM cambios WHERE {' AND '.join(filtros)} ORDER BY id", parametros
        ).fetchall()
        conexion.commit()
        return [_cambio_publico(fila) for fila in filas]
    finally:
        conexion.close()


@router.post("/api/cambios/{cambio_id}/confirmar")
def confirmar_cambio(cambio_id: int, actor=Depends(actor_actual)) -> dict:
    solicitante = getattr(actor, "solicitante", None)
    if solicitante is None:
        raise HTTPException(status_code=403, detail="No se identificó a la persona que confirma el cambio.")
    try:
        cambio = confirmar(cambio_id, solicitante)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    registrar(
        actor=actor,
        tipo="solicitada",
        accion=f"confirmar_{cambio['operacion']}_{cambio['area']}",
        area=cambio["area"],
        referencia=str(cambio["registro_id"]),
        resumen="Se confirmó el cambio solicitado.",
        origen_dato="real",
    )
    return cambio


@router.post("/api/cambios/{cambio_id}/descartar")
def descartar_cambio(cambio_id: int, actor=Depends(actor_actual)) -> dict:
    solicitante = getattr(actor, "solicitante", None)
    if solicitante is None:
        raise HTTPException(status_code=403, detail="No se identificó a la persona que descarta el cambio.")
    try:
        cambio = descartar(cambio_id, solicitante)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    registrar(
        actor=actor,
        tipo="solicitada",
        accion=f"descartar_{cambio['operacion']}_{cambio['area']}",
        area=cambio["area"],
        referencia=str(cambio["registro_id"]),
        resumen="Se descartó el cambio solicitado.",
        origen_dato="real",
    )
    return cambio
