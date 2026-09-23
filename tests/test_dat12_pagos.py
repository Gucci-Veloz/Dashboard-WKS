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
    monkeypatch.setenv("WORKS_TOKEN_VANIA", "token-de-prueba")
    _app_fresco()

    from app.db.migrar import migrar

    migrar()

    from app.main import app

    return TestClient(app)


def _crear_oficina_inquilino_contrato_y_pago(cliente):
    oficina = cliente.post("/api/oficinas", json={"numero": "204"}).json()
    inquilino = cliente.post("/api/inquilinos", json={"titular": "Titular Sintético 01"}).json()
    contrato = cliente.post(
        "/api/contratos",
        json={
            "oficina_id": oficina["id"],
            "inquilino_id": inquilino["id"],
            "inicio": "2026-01-01",
            "fin": "2026-12-31",
        },
    ).json()
    pago = cliente.post(
        "/api/pagos",
        json={"contrato_id": contrato["id"], "precio": 5000, "estatus_pago": "pendiente"},
    ).json()
    return oficina, contrato, pago


def test_ciclo_crud_pagos(cliente):
    _, contrato, pago = _crear_oficina_inquilino_contrato_y_pago(cliente)

    listado = cliente.get("/api/pagos")
    assert any(p["id"] == pago["id"] for p in listado.json())

    vista = cliente.get(f"/api/pagos/{pago['id']}")
    assert vista.status_code == 200

    editado = cliente.put(
        f"/api/pagos/{pago['id']}",
        json={"contrato_id": contrato["id"], "precio": 5200, "estatus_pago": "pendiente"},
    )
    assert editado.status_code == 200
    assert editado.json()["precio"] == 5200

    eliminado = cliente.delete(f"/api/pagos/{pago['id']}")
    assert eliminado.status_code == 204


def test_registrar_pago_cambia_estatus_y_deja_actividad(cliente):
    from app.db.conexion import conectar

    _, contrato, pago = _crear_oficina_inquilino_contrato_y_pago(cliente)

    respuesta = cliente.post(
        "/api/pagos/registrar",
        json={"contrato_id": contrato["id"], "periodo": "septiembre", "forma_pago": "transferencia"},
    )
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["estatus_pago"] == "pagado"
    assert cuerpo["forma_pago"] == "transferencia"

    conexion = conectar()
    fila = conexion.execute(
        "SELECT actor, accion, area, referencia FROM actividad WHERE accion='registrar_pago' ORDER BY id DESC LIMIT 1"
    ).fetchone()
    conexion.close()
    assert fila[0] == "dashboard"
    assert fila[2] == "pagos"
    assert fila[3] == str(pago["id"])


def test_registrar_pago_sin_pendiente_falla_con_mensaje_humano(cliente):
    _, contrato, pago = _crear_oficina_inquilino_contrato_y_pago(cliente)
    cliente.post(
        "/api/pagos/registrar",
        json={"contrato_id": contrato["id"], "periodo": "septiembre", "forma_pago": "transferencia"},
    )
    respuesta = cliente.post(
        "/api/pagos/registrar",
        json={"contrato_id": contrato["id"], "periodo": "octubre", "forma_pago": "efectivo"},
    )
    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "No hay un pago pendiente para ese contrato."


def test_registrar_pago_quita_un_asunto_del_estado(cliente):
    from app.fuentes.cargar import cargar

    cargar("sintetica", escenario="con_atencion")

    antes = cliente.get("/api/estado").json()
    assert antes["conclusion"]["cantidad"] == 3
    asunto_pago = next(a for a in antes["asuntos"] if a["area"] == "pagos")
    contrato_id_pendiente = 8  # ver app/fuentes/sintetica.py: INDICE_PAGO_PENDIENTE

    respuesta = cliente.post(
        "/api/pagos/registrar",
        json={"contrato_id": contrato_id_pendiente, "periodo": "septiembre", "forma_pago": "transferencia"},
    )
    assert respuesta.status_code == 200

    despues = cliente.get("/api/estado").json()
    assert despues["conclusion"]["cantidad"] == 2
    assert not any(a["area"] == "pagos" for a in despues["asuntos"])
    assert asunto_pago["area"] == "pagos"
