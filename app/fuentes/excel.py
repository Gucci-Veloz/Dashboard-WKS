from typing import Optional

from app.fuentes.base import FuenteDatos

MENSAJE_NO_DISPONIBLE = "fuente no disponible: el Excel de Works todavía no se entrega"


class FuenteExcel(FuenteDatos):
    def obtener_registros(self, escenario: Optional[str] = None) -> dict:
        raise RuntimeError(MENSAJE_NO_DISPONIBLE)
