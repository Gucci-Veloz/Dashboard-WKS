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
    _app_fresco()

    from app.db.migrar import migrar

    migrar()

    from app.main import app

    return TestClient(app)


def _sembrar():
    from app.actividad.registrar import registrar

    registrar(
        actor="dashboard",
        tipo="solicitada",
        accion="confirmar_pago",
        resumen="Se confirmó el pago de la oficina 101.",
        area="pagos",
        referencia="pago-1",
        origen_dato="sintetico",
    )
    registrar(
        actor="vania",
        tipo="detectada",
        accion="contrato_por_vencer",
        resumen="El contrato de la oficina 104 vence en 12 días.",
        area="contratos",
        referencia="contrato-4",
        origen_dato="sintetico",
    )
    registrar(
        actor="vania",
        tipo="automatica",
        accion="contacto_incompleto",
        resumen="El contacto de Titular Sintético 09 está incompleto.",
        area="inquilinos",
        referencia="inquilino-9",
        origen_dato="sintetico",
    )


def test_orden_mas_reciente_primero(cliente):
    _sembrar()
    respuesta = cliente.get("/api/actividad")
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert [r["accion"] for r in cuerpo["resultados"]] == [
        "contacto_incompleto",
        "contrato_por_vencer",
        "confirmar_pago",
    ]
    assert cuerpo["total"] == 3


def test_filtro_por_actor(cliente):
    _sembrar()
    respuesta = cliente.get("/api/actividad", params={"actor": "vania"})
    cuerpo = respuesta.json()
    assert cuerpo["total"] == 2
    assert all(r["actor"] == "vania" for r in cuerpo["resultados"])


def test_filtro_por_area(cliente):
    _sembrar()
    respuesta = cliente.get("/api/actividad", params={"area": "pagos"})
    cuerpo = respuesta.json()
    assert cuerpo["total"] == 1
    assert cuerpo["resultados"][0]["accion"] == "confirmar_pago"


def test_paginacion(cliente):
    _sembrar()
    respuesta = cliente.get("/api/actividad", params={"tamano_pagina": 2, "pagina": 1})
    cuerpo = respuesta.json()
    assert cuerpo["total"] == 3
    assert len(cuerpo["resultados"]) == 2

    respuesta_2 = cliente.get("/api/actividad", params={"tamano_pagina": 2, "pagina": 2})
    cuerpo_2 = respuesta_2.json()
    assert len(cuerpo_2["resultados"]) == 1
    assert cuerpo_2["resultados"][0]["accion"] == "confirmar_pago"
