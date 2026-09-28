from datetime import date, datetime

from fastapi import APIRouter

from app.db.conexion import conectar_con_filas
from app.estado.reglas import calcular_estado

router = APIRouter()

AREAS = ("oficinas", "inquilinos", "contratos", "pagos")


def _leer_datos(conexion) -> tuple:
    datos = {}
    origenes = set()
    for area in AREAS:
        filas = conexion.execute(f"SELECT * FROM {area}").fetchall()
        registros = [dict(fila) for fila in filas]
        datos[area] = registros
        for registro in registros:
            origenes.add(registro.get("origen_dato"))
    return datos, origenes


def _origen_datos(origenes: set) -> str:
    origenes_sin_vacios = {o for o in origenes if o}
    if origenes_sin_vacios and origenes_sin_vacios <= {"sintetico"}:
        return "sintetico"
    return "real"


@router.get("/api/estado")
def obtener_estado() -> dict:
    conexion = conectar_con_filas()
    try:
        datos, origenes = _leer_datos(conexion)
    finally:
        conexion.close()

    origen_datos = _origen_datos(origenes)
    return calcular_estado(
        datos,
        date.today(),
        origen_datos,
        generado_en=datetime.now().isoformat(),
    )
