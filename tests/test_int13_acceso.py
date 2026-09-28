from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi.testclient import TestClient

from app.db.migrar import migrar
from app.main import app
from app.seguridad import sesion


ZONA = ZoneInfo("America/Mexico_City")
CREDENCIAL = {"Authorization": "Bearer token-de-prueba"}


def _cliente(monkeypatch, tmp_path):
    monkeypatch.setenv("WORKS_DB", str(tmp_path / "works.db"))
    monkeypatch.setenv("WORKS_TOKEN_VANIA", "token-de-prueba")
    monkeypatch.setenv("WORKS_WHATSAPP_DAVID", "+520000000001")
    monkeypatch.setenv("WORKS_WHATSAPP_GRECIA", "+520000000002")
    migrar()
    return TestClient(app, base_url="https://testserver")


def _enlace(cliente, numero):
    respuesta = cliente.post("/api/acceso/enlace", params={"numero_whatsapp": numero}, headers=CREDENCIAL)
    assert respuesta.status_code == 200
    return respuesta.json()["enlace"].split("token=", 1)[1]


def test_enlace_es_de_un_solo_uso_y_cookie_segura(monkeypatch, tmp_path):
    cliente = _cliente(monkeypatch, tmp_path)
    token = _enlace(cliente, "+520000000001")
    primera = cliente.get("/api/acceso/entrar", params={"token": token})
    assert primera.status_code == 200
    assert "Secure" in primera.headers["set-cookie"]
    assert "HttpOnly" in primera.headers["set-cookie"]
    assert "SameSite=strict" in primera.headers["set-cookie"]
    assert cliente.get("/api/acceso/entrar", params={"token": token}).status_code == 401


def test_enlace_a_los_once_minutos_falla(monkeypatch, tmp_path):
    cliente = _cliente(monkeypatch, tmp_path)
    fijo = datetime(2026, 9, 26, 10, tzinfo=ZONA)
    monkeypatch.setattr(sesion, "ahora", lambda: fijo)
    token = _enlace(cliente, "+520000000001")
    monkeypatch.setattr(sesion, "ahora", lambda: fijo + timedelta(minutes=11))
    assert cliente.get("/api/acceso/entrar", params={"token": token}).status_code == 401


def test_sesion_vence_a_las_horas_indicadas(monkeypatch, tmp_path):
    cliente = _cliente(monkeypatch, tmp_path)
    diecisiete = datetime(2026, 9, 26, 17, tzinfo=ZONA)
    monkeypatch.setattr(sesion, "ahora", lambda: diecisiete)
    token = _enlace(cliente, "+520000000002")
    cliente.get("/api/acceso/entrar", params={"token": token})
    assert sesion.persona_de_sesion(cliente.cookies[sesion.NOMBRE_COOKIE], diecisiete.replace(hour=18)) == "grecia"
    assert sesion.persona_de_sesion(cliente.cookies[sesion.NOMBRE_COOKIE], diecisiete.replace(hour=18, minute=1)) is None
    diecinueve = datetime(2026, 9, 26, 19, tzinfo=ZONA)
    monkeypatch.setattr(sesion, "ahora", lambda: diecinueve)
    token = _enlace(cliente, "+520000000002")
    cliente.get("/api/acceso/entrar", params={"token": token})
    assert sesion.persona_de_sesion(cliente.cookies[sesion.NOMBRE_COOKIE], diecinueve.replace(hour=23, minute=59)) == "grecia"


def test_dos_dispositivos_y_acceso_protegido(monkeypatch, tmp_path):
    primero = _cliente(monkeypatch, tmp_path)
    segundo = TestClient(app, base_url="https://testserver")
    assert primero.get("/api/estado").status_code == 401
    token = _enlace(primero, "+520000000002")
    primero.get("/api/acceso/entrar", params={"token": token})
    token = _enlace(primero, "+520000000002")
    segundo.get("/api/acceso/entrar", params={"token": token})
    assert primero.get("/api/estado").status_code == 200
    assert segundo.get("/api/estado").status_code == 200
    assert primero.get("/api/estado", headers=CREDENCIAL).status_code == 200
    creada = primero.post("/api/oficinas", json={"numero": "999"})
    assert creada.status_code == 201
    confirmada = primero.post(f"/api/cambios/{creada.json()['id']}/confirmar")
    assert confirmada.status_code == 200
    actividad = primero.get("/api/actividad").json()["resultados"]
    assert actividad[0]["persona"] == "grecia"


def test_no_entrega_enlace_a_numero_desconocido_o_desarrollador(monkeypatch, tmp_path):
    cliente = _cliente(monkeypatch, tmp_path)
    for numero in ("+520000000003", "+520000000004"):
        assert cliente.post("/api/acceso/enlace", params={"numero_whatsapp": numero}, headers=CREDENCIAL).status_code == 403
