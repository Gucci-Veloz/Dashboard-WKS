"""Ruta para consultar el reporte diario de cambios confirmados."""

from datetime import date

from fastapi import APIRouter, HTTPException, Query

from app.cambios.reporte import reporte_del_dia

router = APIRouter()


@router.get("/api/reporte")
def obtener_reporte(fecha: str | None = Query(default=None)) -> list[dict]:
    try:
        dia = date.fromisoformat(fecha) if fecha else None
    except ValueError as error:
        raise HTTPException(status_code=400, detail="La fecha debe usar el formato AAAA-MM-DD.") from error
    return reporte_del_dia(dia)
