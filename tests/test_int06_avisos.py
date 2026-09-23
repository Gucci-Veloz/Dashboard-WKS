import sys

import pytest
from fastapi.testclient import TestClient


def _app_fresco():
    for modulo in list(sys.modules):
        if modulo == "app" or modulo.startswith("app."):
            del sys.modules[modulo]


@pytest.fixture()
def cliente(tmp_path, monkeypatch):
    base_temporal = tmp_path / "works.db"
    monkeypatch.setenv("WORKS_DB", str(base_temporal))
    monkeypatch.setenv("WORKS_TOKEN_VANIA", "secreto-largo")
    _app_fresco()

    from app.db.migrar import migrar

    migrar()

    from app.main import app

    return TestClient(app)


def _cargar_escenario(escenario: str) -> None:
    from app.fuentes.cargar import cargar

    cargar("sintetica", escenario=escenario)


CREDENCIAL = {"Authorization": "Bearer secreto-largo"}


def test_tranquilo_devuelve_204(cliente):
    _cargar_escenario("tranquilo")
    respuesta = cliente.get("/api/vania/avisos", headers=CREDENCIAL)
    assert respuesta.status_code == 204


def test_con_atencion_devuelve_mensaje_agrupado(cliente):
    _cargar_escenario("con_atencion")

    from app.db.conexion import conectar
    from app.estado.reglas import calcular_estado
    from datetime import date

    respuesta = cliente.get("/api/vania/avisos", headers=CREDENCIAL)
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()

    respuesta_estado = cliente.get("/api/estado")
    estado = respuesta_estado.json()

    assert cuerpo["cantidad"] == estado["conclusion"]["cantidad"]
    assert cuerpo["asuntos"] == estado["asuntos"]
    assert estado["conclusion"]["frase"] in cuerpo["mensaje"]


def test_sin_credencial_falla(cliente):
    _cargar_escenario("con_atencion")
    respuesta = cliente.get("/api/vania/avisos")
    assert respuesta.status_code == 401
