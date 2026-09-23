import argparse
import importlib
from typing import Optional

from app.db.conexion import conectar
from app.fuentes.base import AREAS, FuenteDatos


def resolver_fuente(nombre: str) -> FuenteDatos:
    modulo = importlib.import_module(f"app.fuentes.{nombre}")
    nombre_clase = f"Fuente{nombre.capitalize()}"
    clase = getattr(modulo, nombre_clase, None)
    if clase is None:
        raise RuntimeError(f"la fuente '{nombre}' no define la clase {nombre_clase}")
    return clase()


def cargar(fuente: str, escenario: Optional[str] = None, conexion=None) -> None:
    """Vacía y carga las cuatro áreas dentro de una sola transacción.

    Si algo falla a medias, no queda ningún dato parcial: se revierte todo.
    """
    fuente_datos = resolver_fuente(fuente)
    registros = fuente_datos.obtener_registros(escenario)

    cerrar_al_final = conexion is None
    if conexion is None:
        conexion = conectar()
    try:
        for area in AREAS:
            conexion.execute(f"DELETE FROM {area}")
        for area in AREAS:
            for registro in registros.get(area, []):
                columnas = ", ".join(registro.keys())
                marcadores = ", ".join("?" for _ in registro)
                conexion.execute(
                    f"INSERT INTO {area} ({columnas}) VALUES ({marcadores})",
                    tuple(registro.values()),
                )
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        if cerrar_al_final:
            conexion.close()


def main() -> None:
    analizador = argparse.ArgumentParser(description="Carga una fuente de datos de Works.")
    analizador.add_argument("--fuente", required=True)
    analizador.add_argument("--escenario", default=None)
    args = analizador.parse_args()
    cargar(args.fuente, args.escenario)
    print(f"Fuente '{args.fuente}' cargada.")


if __name__ == "__main__":
    main()
