import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = BASE_DIR / "contratos" / "estado.schema.json"


def _app_fresco():
    for modulo in list(sys.modules):
        if modulo == "app" or modulo.startswith("app."):
            del sys.modules[modulo]


def _validar_contra_esquema(instancia, esquema):
    tipo = esquema.get("type")

    if "enum" in esquema:
        assert instancia in esquema["enum"], f"{instancia!r} no está en {esquema['enum']}"

    if tipo == "object":
        assert isinstance(instancia, dict)
        for campo in esquema.get("required", []):
            assert campo in instancia, f"falta el campo requerido {campo!r}"
        propiedades = esquema.get("properties", {})
        if esquema.get("additionalProperties") is False:
            extra = set(instancia) - set(propiedades)
            assert not extra, f"propiedades no permitidas: {extra}"
        for clave, subesquema in propiedades.items():
            if clave in instancia:
                _validar_contra_esquema(instancia[clave], subesquema)
    elif tipo == "array":
        assert isinstance(instancia, list)
        for elemento in instancia:
            _validar_contra_esquema(elemento, esquema["items"])
    elif tipo == "string":
        assert isinstance(instancia, str)
        assert len(instancia) >= esquema.get("minLength", 0)
    elif tipo == "integer":
        assert isinstance(instancia, int)
        assert instancia >= esquema.get("minimum", instancia)


@pytest.fixture()
def cliente(tmp_path, monkeypatch):
    base_temporal = tmp_path / "works.db"
    monkeypatch.setenv("WORKS_DB", str(base_temporal))
    _app_fresco()

    from app.db.migrar import migrar

    migrar()

    from app.main import app

    return TestClient(app)


def _cargar_escenario(escenario: str) -> None:
    from app.fuentes.cargar import cargar

    cargar("sintetica", escenario=escenario)


def test_estado_tranquilo(cliente):
    _cargar_escenario("tranquilo")
    respuesta = cliente.get("/api/estado")
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["conclusion"]["tipo"] == "tranquilo"
    assert cuerpo["asuntos"] == []
    assert cuerpo["origen_datos"] == "sintetico"


def test_estado_con_atencion(cliente):
    _cargar_escenario("con_atencion")
    respuesta = cliente.get("/api/estado")
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["conclusion"]["tipo"] == "atencion"
    assert [a["area"] for a in cuerpo["asuntos"]] == ["contratos", "pagos", "inquilinos"]
    assert cuerpo["origen_datos"] == "sintetico"


def test_respuesta_valida_contra_el_esquema(cliente):
    esquema = json.loads(SCHEMA_PATH.read_text())
    for escenario in ("tranquilo", "con_atencion"):
        _cargar_escenario(escenario)
        respuesta = cliente.get("/api/estado")
        _validar_contra_esquema(respuesta.json(), esquema)


def test_respuesta_coincide_con_el_motor(cliente):
    _cargar_escenario("con_atencion")
    respuesta = cliente.get("/api/estado")
    cuerpo = respuesta.json()

    from datetime import date

    from app.db.conexion import conectar
    from app.estado.reglas import calcular_estado
    from app.api.estado import _leer_datos, _origen_datos

    conexion = conectar()
    try:
        datos, origenes = _leer_datos(conexion)
    finally:
        conexion.close()

    esperado = calcular_estado(datos, date.today(), _origen_datos(origenes))

    assert cuerpo["conclusion"] == esperado["conclusion"]
    assert cuerpo["asuntos"] == esperado["asuntos"]
    assert cuerpo["indicadores"] == esperado["indicadores"]
