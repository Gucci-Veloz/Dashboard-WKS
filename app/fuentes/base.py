from abc import ABC, abstractmethod
from typing import Optional

AREAS = ("oficinas", "inquilinos", "contratos", "pagos")


class FuenteDatos(ABC):
    """Contrato de cualquier fuente de datos de las cuatro áreas.

    `obtener_registros` entrega un diccionario con una lista por área
    (`oficinas`, `inquilinos`, `contratos`, `pagos`), con los campos ya
    normalizados a las columnas de `app/db/migraciones/001_areas.sql`.
    """

    @abstractmethod
    def obtener_registros(self, escenario: Optional[str] = None) -> dict:
        raise NotImplementedError
