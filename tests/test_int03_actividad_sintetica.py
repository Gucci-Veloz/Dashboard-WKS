import sqlite3
import sys

import pytest

TABLAS_POR_TIPO = {
    "pago": "pagos",
    "contrato": "contratos",
    "inquilino": "inquilinos",
    "oficina": "oficinas",
}


def _app_fresco():
    for modulo in list(sys.modules):
        if modulo == "app" or modulo.startswith("app."):
            del sys.modules[modulo]


@pytest.fixture()
def base_con_atencion(tmp_path, monkeypatch):
    base_temporal = tmp_path / "works.db"
    monkeypatch.setenv("WORKS_DB", str(base_temporal))
    _app_fresco()

    from app.db.migrar import migrar
    from app.fuentes.cargar import cargar

    migrar()
    cargar("sintetica", escenario="con_atencion")
    return base_temporal


def test_actividad_sintetica_es_toda_sintetica_y_referencias_existen(base_con_atencion):
    from app.db.conexion import conectar
    from app.fuentes.actividad_sintetica import cargar_actividad_sintetica

    cargar_actividad_sintetica()

    conexion = conectar()
    try:
        conexion.row_factory = sqlite3.Row
        filas = conexion.execute("SELECT * FROM actividad").fetchall()
        assert len(filas) == 4

        for fila in filas:
            assert fila["actor"] == "vania"
            assert fila["origen_dato"] == "sintetico"

            tipo, _, id_referencia = fila["referencia"].partition("-")
            tabla = TABLAS_POR_TIPO[tipo]
            existe = conexion.execute(
                f"SELECT 1 FROM {tabla} WHERE id = ?", (id_referencia,)
            ).fetchone()
            assert existe is not None, f"referencia {fila['referencia']!r} no existe"
    finally:
        conexion.close()
