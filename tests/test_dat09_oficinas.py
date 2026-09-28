import sys
import pytest
from fastapi.testclient import TestClient

def _app_fresco():
    for modulo in list(sys.modules):
        if modulo == "app" or modulo.startswith("app."):
            del sys.modules[modulo]

@pytest.fixture()
def cliente(tmp_path, monkeypatch):
    monkeypatch.setenv("WORKS_DB", str(tmp_path / "works.db"))
    _app_fresco()
    from app.db.migrar import migrar
    from app.main import app
    migrar()
    return TestClient(app)

def test_oficina_se_confirma_antes_de_aparecer(cliente):
    creada = cliente.post("/api/oficinas", json={"numero": "204"})
    assert creada.status_code == 201
    assert cliente.get("/api/oficinas").json() == []
    confirmada = cliente.post(f"/api/cambios/{creada.json()['id']}/confirmar")
    assert confirmada.status_code == 200
    oficina_id = confirmada.json()["registro_id"]
    assert cliente.get(f"/api/oficinas/{oficina_id}").json()["numero"] == "204"

def test_oficina_inexistente_da_mensaje_humano(cliente):
    respuesta = cliente.get("/api/oficinas/999")
    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "No existe una oficina con ese número de registro."
