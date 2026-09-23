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


def _crear_oficina_e_inquilino(cliente):
    oficina = cliente.post("/api/oficinas", json={"numero": "204"}).json()
    inquilino = cliente.post("/api/inquilinos", json={"titular": "Titular Sintético 01"}).json()
    return oficina["id"], inquilino["id"]


def test_ciclo_completo_contratos(cliente):
    oficina_id, inquilino_id = _crear_oficina_e_inquilino(cliente)

    creado = cliente.post(
        "/api/contratos",
        json={
            "oficina_id": oficina_id,
            "inquilino_id": inquilino_id,
            "inicio": "2026-01-01",
            "fin": "2026-12-31",
        },
    )
    assert creado.status_code == 201
    cuerpo = creado.json()
    assert cuerpo["origen_dato"] == "manual"
    contrato_id = cuerpo["id"]

    listado = cliente.get("/api/contratos")
    assert any(c["id"] == contrato_id for c in listado.json())

    vista = cliente.get(f"/api/contratos/{contrato_id}")
    assert vista.status_code == 200

    editado = cliente.put(
        f"/api/contratos/{contrato_id}",
        json={
            "oficina_id": oficina_id,
            "inquilino_id": inquilino_id,
            "inicio": "2026-01-01",
            "fin": "2027-01-31",
        },
    )
    assert editado.status_code == 200
    assert editado.json()["fin"] == "2027-01-31"

    eliminado = cliente.delete(f"/api/contratos/{contrato_id}")
    assert eliminado.status_code == 204

    tras_borrar = cliente.get(f"/api/contratos/{contrato_id}")
    assert tras_borrar.status_code == 404


def test_contrato_inexistente_da_mensaje_humano(cliente):
    respuesta = cliente.get("/api/contratos/999")
    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "No existe un contrato con ese número de registro."


def test_crear_contrato_con_oficina_inexistente_falla_con_mensaje_humano(cliente):
    _, inquilino_id = _crear_oficina_e_inquilino(cliente)
    respuesta = cliente.post(
        "/api/contratos",
        json={"oficina_id": 9999, "inquilino_id": inquilino_id, "inicio": "2026-01-01", "fin": "2026-12-31"},
    )
    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == "La oficina indicada no existe."


def test_cada_escritura_deja_actividad_con_actor_correcto(cliente):
    from app.db.conexion import conectar

    oficina_id, inquilino_id = _crear_oficina_e_inquilino(cliente)
    creado = cliente.post(
        "/api/contratos",
        json={"oficina_id": oficina_id, "inquilino_id": inquilino_id, "inicio": "2026-01-01", "fin": "2026-12-31"},
    )
    contrato_id = creado.json()["id"]

    conexion = conectar()
    fila = conexion.execute(
        "SELECT actor, area, referencia, tipo FROM actividad WHERE area='contratos' ORDER BY id DESC LIMIT 1"
    ).fetchone()
    assert fila[0] == "dashboard"
    assert fila[1] == "contratos"
    assert fila[2] == str(contrato_id)
    assert fila[3] == "solicitada"
    conexion.close()

    cliente.put(
        f"/api/contratos/{contrato_id}",
        json={"oficina_id": oficina_id, "inquilino_id": inquilino_id, "inicio": "2026-01-01", "fin": "2027-01-31"},
        headers={"Authorization": "Bearer token-de-prueba"},
    )
    conexion = conectar()
    fila = conexion.execute(
        "SELECT actor FROM actividad WHERE area='contratos' ORDER BY id DESC LIMIT 1"
    ).fetchone()
    assert fila[0] == "vania"
    conexion.close()
