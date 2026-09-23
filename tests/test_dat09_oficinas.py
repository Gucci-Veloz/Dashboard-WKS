import sys
from pathlib import Path

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
    conexion.row_factory = None
    fila = conexion.execute(
        "SELECT actor, area, referencia, tipo, origen_dato FROM actividad ORDER BY id DESC LIMIT 1"
    ).fetchone()
    return fila


def test_ciclo_completo_oficinas(cliente):
    creada = cliente.post(
        "/api/oficinas", json={"tipo": "privada", "numero": "204", "piso": "2", "m2": 20.5}
    )
    assert creada.status_code == 201
    cuerpo = creada.json()
    assert cuerpo["numero"] == "204"
    assert cuerpo["origen_dato"] == "manual"
    oficina_id = cuerpo["id"]

    listado = cliente.get("/api/oficinas")
    assert listado.status_code == 200
    assert any(o["id"] == oficina_id for o in listado.json())

    vista = cliente.get(f"/api/oficinas/{oficina_id}")
    assert vista.status_code == 200
    assert vista.json()["numero"] == "204"

    editada = cliente.put(
        f"/api/oficinas/{oficina_id}",
        json={"tipo": "privada", "numero": "204", "piso": "2", "m2": 22.0, "estatus": "ocupada"},
    )
    assert editada.status_code == 200
    assert editada.json()["m2"] == 22.0

    eliminada = cliente.delete(f"/api/oficinas/{oficina_id}")
    assert eliminada.status_code == 204

    tras_borrar = cliente.get(f"/api/oficinas/{oficina_id}")
    assert tras_borrar.status_code == 404


def test_oficina_inexistente_da_mensaje_humano(cliente):
    respuesta = cliente.get("/api/oficinas/999")
    assert respuesta.status_code == 404
    assert "%" not in respuesta.json()["detail"]
    assert respuesta.json()["detail"] == "No existe una oficina con ese número de registro."


def test_cada_escritura_deja_actividad_con_actor_correcto(cliente, tmp_path, monkeypatch):
    from app.db.conexion import conectar

    creada = cliente.post("/api/oficinas", json={"numero": "301"})
    oficina_id = creada.json()["id"]

    conexion = conectar()
    fila = _ultima_actividad(conexion)
    assert fila[0] == "dashboard"
    assert fila[1] == "oficinas"
    assert fila[2] == str(oficina_id)
    assert fila[3] == "solicitada"
    assert fila[4] == "real"
    conexion.close()

    editada = cliente.put(
        f"/api/oficinas/{oficina_id}",
        json={"numero": "301"},
        headers={"Authorization": "Bearer token-de-prueba"},
    )
    assert editada.status_code == 200

    conexion = conectar()
    fila = _ultima_actividad(conexion)
    assert fila[0] == "vania"
    conexion.close()

    cliente.delete(f"/api/oficinas/{oficina_id}")
    conexion = conectar()
    fila = _ultima_actividad(conexion)
    assert fila[0] == "dashboard"
    assert fila[3] == "solicitada"
    conexion.close()
