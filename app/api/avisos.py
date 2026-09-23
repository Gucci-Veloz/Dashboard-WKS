from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Response

from app.api.estado import _leer_datos, _origen_datos
from app.db.conexion import conectar
from app.estado.reglas import calcular_estado
from app.seguridad.actor import actor_actual

router = APIRouter()


@router.get("/api/vania/avisos")
def avisos_agrupados(actor: str = Depends(actor_actual)):
    if actor != "vania":
        raise HTTPException(status_code=401)

    conexion = conectar()
    try:
        datos, origenes = _leer_datos(conexion)
    finally:
        conexion.close()

    estado = calcular_estado(
        datos,
        date.today(),
        _origen_datos(origenes),
        generado_en=datetime.now().isoformat(),
    )
    asuntos = estado["asuntos"]
    if not asuntos:
        return Response(status_code=204)

    frases = [asunto["frase"] for asunto in asuntos]
    mensaje = estado["conclusion"]["frase"] + " " + " ".join(frases)

    return {
        "mensaje": mensaje,
        "cantidad": len(asuntos),
        "asuntos": asuntos,
    }
