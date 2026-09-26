from fastapi.testclient import TestClient

from app.db.conexion import conectar
from app.db.migrar import migrar
from app.main import app
from app.seguridad import sesion


CREDENCIAL = {"Authorization": "Bearer token-de-prueba"}
GRECIA = "+520000000002"
DAVID = "+520000000001"


def _cliente(monkeypatch, tmp_path):
    monkeypatch.setenv("WORKS_DB", str(tmp_path / "works.db"))
    monkeypatch.setenv("WORKS_TOKEN_VANIA", "token-de-prueba")
    monkeypatch.setenv("WORKS_WHATSAPP_DAVID", DAVID)
    monkeypatch.setenv("WORKS_WHATSAPP_GRECIA", GRECIA)
    migrar()
    return TestClient(app, base_url="https://testserver")


def _sesion_de(cliente, numero):
    enlace = cliente.post("/api/acceso/enlace", params={"numero_whatsapp": numero}, headers=CREDENCIAL)
    token = enlace.json()["enlace"].split("token=", 1)[1]
    assert cliente.get("/api/acceso/entrar", params={"token": token}).status_code == 200


def _revocar(persona):
    conexion = conectar()
    try:
        conexion.execute("UPDATE sesiones SET revocada_en = '2026-09-26T00:00:00-06:00' WHERE persona = ?", (persona,))
        conexion.commit()
    finally:
        conexion.close()


def _escribir(cliente, numero):
    return cliente.post("/api/oficinas", json={"numero": "204"}, headers={**CREDENCIAL, "X-Works-Solicitante": numero})


def test_vania_sin_sesion_de_grecia_recibe_sin_sesion(monkeypatch, tmp_path):
    cliente = _cliente(monkeypatch, tmp_path)
    _revocar("grecia")
    respuesta = _escribir(cliente, GRECIA)
    assert respuesta.status_code == 401
    assert respuesta.json()["codigo"] == "sin_sesion"


def test_sesion_de_david_no_autoriza_instruccion_de_grecia(monkeypatch, tmp_path):
    cliente = _cliente(monkeypatch, tmp_path)
    _sesion_de(cliente, DAVID)
    respuesta = _escribir(cliente, GRECIA)
    assert respuesta.status_code == 401
    assert respuesta.json()["codigo"] == "sin_sesion"


def test_vania_con_sesion_de_grecia_crea_pendiente(monkeypatch, tmp_path):
    cliente = _cliente(monkeypatch, tmp_path)
    _sesion_de(cliente, GRECIA)
    respuesta = _escribir(cliente, GRECIA)
    assert respuesta.status_code == 201
    pendiente = cliente.get("/api/cambios").json()[0]
    assert pendiente["solicitante"] == "grecia"
    assert pendiente["ejecutor"] == "vania"


def test_numero_desconocido_o_del_desarrollador_recibe_403(monkeypatch, tmp_path):
    cliente = _cliente(monkeypatch, tmp_path)
    _sesion_de(cliente, GRECIA)
    for numero in ("+520000000003", "+520000000004"):
        assert _escribir(cliente, numero).status_code == 403
