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


def _ultima_actividad(conexion):
    fila = conexion.execute(
        "SELECT actor, area, referencia, tipo, origen_dato FROM actividad ORDER BY id DESC LIMIT 1"
    ).fetchone()
    return fila


def test_ciclo_completo_inquilinos(cliente):
    creado = cliente.post(
        "/api/inquilinos", json={"titular": "Titular Sintético 01", "contacto": "correo@ej.com"}
    )
    assert creado.status_code == 201
    cuerpo = creado.json()
    assert cuerpo["titular"] == "Titular Sintético 01"
    assert cuerpo["origen_dato"] == "manual"
    inquilino_id = cuerpo["id"]

    listado = cliente.get("/api/inquilinos")
    assert listado.status_code == 200
    assert any(i["id"] == inquilino_id for i in listado.json())

    vista = cliente.get(f"/api/inquilinos/{inquilino_id}")
    assert vista.status_code == 200

    editado = cliente.put(
        f"/api/inquilinos/{inquilino_id}",
        json={"titular": "Titular Sintético 01", "contacto": "nuevo@ej.com"},
    )
    assert editado.status_code == 200
    assert editado.json()["contacto"] == "nuevo@ej.com"

    eliminado = cliente.delete(f"/api/inquilinos/{inquilino_id}")
    assert eliminado.status_code == 204

    tras_borrar = cliente.get(f"/api/inquilinos/{inquilino_id}")
    assert tras_borrar.status_code == 404


def test_inquilino_inexistente_da_mensaje_humano(cliente):
    respuesta = cliente.get("/api/inquilinos/999")
    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "No existe un inquilino con ese número de registro."


def test_cada_escritura_deja_actividad_con_actor_correcto(cliente):
    from app.db.conexion import conectar

    creado = cliente.post("/api/inquilinos", json={"titular": "Titular Sintético 02"})
    inquilino_id = creado.json()["id"]

    conexion = conectar()
    fila = _ultima_actividad(conexion)
    assert fila[0] == "dashboard"
    assert fila[1] == "inquilinos"
    assert fila[2] == str(inquilino_id)
    assert fila[3] == "solicitada"
    assert fila[4] == "real"
    conexion.close()

    cliente.put(
        f"/api/inquilinos/{inquilino_id}",
        json={"titular": "Titular Sintético 02"},
        headers={"Authorization": "Bearer token-de-prueba"},
    )
    conexion = conectar()
    fila = _ultima_actividad(conexion)
    assert fila[0] == "vania"
    conexion.close()
