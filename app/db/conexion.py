import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def ruta_base_datos() -> Path:
    valor = os.environ.get("WORKS_DB")
    if valor:
        return Path(valor)
    return BASE_DIR / "var" / "works.db"


def conectar() -> sqlite3.Connection:
    ruta = ruta_base_datos()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(ruta)
    conexion.execute("PRAGMA foreign_keys = ON")
    conexion.row_factory = sqlite3.Row
    return conexion


def conectar_con_filas() -> sqlite3.Connection:
    return conectar()
