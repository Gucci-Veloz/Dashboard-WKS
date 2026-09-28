import sys
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
FUENTES_DIR = BASE_DIR / "app" / "fuentes"


def _app_fresco():
    for modulo in list(sys.modules):
        if modulo == "app" or modulo.startswith("app."):
            del sys.modules[modulo]


@pytest.fixture()
def conexion(tmp_path, monkeypatch):
    base_temporal = tmp_path / "works.db"
    monkeypatch.setenv("WORKS_DB", str(base_temporal))
    _app_fresco()

    from app.db.migrar import migrar
    from app.db.conexion import conectar

    migrar()
    conexion = conectar()
    yield conexion
    conexion.close()


def _escribir_fuente_falsa(nombre_modulo, nombre_clase, cuerpo_metodo):
    archivo = FUENTES_DIR / f"{nombre_modulo}.py"
    archivo.write_text(
        "from app.fuentes.base import FuenteDatos\n\n\n"
        f"class {nombre_clase}(FuenteDatos):\n"
        "    def obtener_registros(self, escenario=None):\n"
        f"{cuerpo_metodo}\n"
    )
    return archivo


def test_fuente_falsa_se_carga(conexion):
    archivo = _escribir_fuente_falsa(
        "pruebadat05",
        "FuentePruebadat05",
        "        return {\n"
        "            'oficinas': [\n"
        "                {'tipo': 'privada', 'numero': '204', 'origen_dato': 'sintetico'}\n"
        "            ],\n"
        "            'inquilinos': [],\n"
        "            'contratos': [],\n"
        "            'pagos': [],\n"
        "        }",
    )
    try:
        _app_fresco()
        from app.fuentes.cargar import cargar

        cargar("pruebadat05", conexion=conexion)
        total = conexion.execute("SELECT COUNT(*) FROM oficinas").fetchone()[0]
        assert total == 1
    finally:
        archivo.unlink()


def test_fuente_excel_falla_con_mensaje():
    _app_fresco()
    from app.fuentes.cargar import resolver_fuente
    from app.fuentes.excel import MENSAJE_NO_DISPONIBLE

    with pytest.raises(RuntimeError, match=MENSAJE_NO_DISPONIBLE):
        resolver_fuente("excel").obtener_registros()


def test_carga_que_falla_a_medias_no_deja_datos_parciales(conexion):
    archivo = _escribir_fuente_falsa(
        "pruebafalladat05",
        "FuentePruebafalladat05",
        "        return {\n"
        "            'oficinas': [\n"
        "                {'tipo': 'privada', 'numero': '204', 'origen_dato': 'sintetico'}\n"
        "            ],\n"
        "            'inquilinos': [],\n"
        "            'contratos': [],\n"
        "            'pagos': [\n"
        "                {'precio': 100}\n"
        "            ],\n"
        "        }",
    )
    try:
        _app_fresco()
        from app.fuentes.cargar import cargar

        with pytest.raises(Exception):
            cargar("pruebafalladat05", conexion=conexion)

        total_oficinas = conexion.execute("SELECT COUNT(*) FROM oficinas").fetchone()[0]
        total_pagos = conexion.execute("SELECT COUNT(*) FROM pagos").fetchone()[0]
        assert total_oficinas == 0
        assert total_pagos == 0
    finally:
        archivo.unlink()
