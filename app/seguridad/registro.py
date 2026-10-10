"""Oculta datos sensibles en el registro de accesos de Uvicorn.

Uvicorn arma la línea del registro con `record.args` =
(cliente, método, ruta con query, versión http, status). El filtro reemplaza
la ruta antes del formateo, solo en `/api/acceso/`, dejando visible el nombre
de cada parámetro sensible y cambiando su valor por `***`.
"""

import logging

PREFIJO_ACCESO = "/api/acceso/"
PARAMETROS_SENSIBLES = {"numero_whatsapp", "token"}
OCULTO = "***"


def ocultar_query(ruta: str) -> str:
    camino, separador, query = ruta.partition("?")
    if not separador or not camino.startswith(PREFIJO_ACCESO):
        return ruta
    partes = []
    for parte in query.split("&"):
        nombre, igual, _ = parte.partition("=")
        partes.append(f"{nombre}={OCULTO}" if igual and nombre in PARAMETROS_SENSIBLES else parte)
    return f"{camino}?{'&'.join(partes)}"


class FiltroAccesoSensible(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        args = record.args
        if isinstance(args, tuple) and len(args) >= 3 and isinstance(args[2], str):
            record.args = args[:2] + (ocultar_query(args[2]),) + args[3:]
        return True


def instalar_filtro_acceso() -> None:
    registro = logging.getLogger("uvicorn.access")
    if not any(isinstance(f, FiltroAccesoSensible) for f in registro.filters):
        registro.addFilter(FiltroAccesoSensible())
