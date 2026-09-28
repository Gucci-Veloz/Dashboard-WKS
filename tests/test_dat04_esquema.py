import sqlite3
import sys

import pytest


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


COLUMNAS_ESPERADAS = {
    "oficinas": {"tipo", "numero", "piso", "m2", "estatus", "origen_dato", "extras"},
    "inquilinos": {"titular", "contacto", "origen_dato", "extras"},
    "contratos": {
        "oficina_id",
        "inquilino_id",
        "inicio",
        "fin",
        "alerta_renovacion",
        "origen_dato",
        "extras",
    },
    "pagos": {
        "contrato_id",
        "precio",
        "deposito_garantia",
        "fecha_pago",
        "forma_pago",
        "estatus_pago",
        "origen_dato",
        "extras",
    },
}


def test_columnas_existen(conexion):
    for tabla, columnas_esperadas in COLUMNAS_ESPERADAS.items():
        filas = conexion.execute(f"PRAGMA table_info({tabla})").fetchall()
        columnas = {fila[1] for fila in filas}
        faltantes = columnas_esperadas - columnas
        assert not faltantes, f"{tabla}: faltan columnas {faltantes}"


def test_insertar_sin_origen_dato_falla(conexion):
    with pytest.raises(sqlite3.IntegrityError):
        conexion.execute("INSERT INTO oficinas (tipo, numero) VALUES ('privada', '204')")


def test_insertar_con_origen_dato_invalido_falla(conexion):
    with pytest.raises(sqlite3.IntegrityError):
        conexion.execute(
            "INSERT INTO oficinas (tipo, numero, origen_dato) VALUES ('privada', '204', 'inventado')"
        )


def test_insertar_con_origen_dato_valido_funciona(conexion):
    conexion.execute(
        "INSERT INTO oficinas (tipo, numero, origen_dato) VALUES ('privada', '204', 'sintetico')"
    )
    conexion.commit()
    total = conexion.execute("SELECT COUNT(*) FROM oficinas").fetchone()[0]
    assert total == 1
