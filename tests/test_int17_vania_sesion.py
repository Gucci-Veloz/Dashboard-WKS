from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from app.db.conexion import conectar
from app.db.migrar import migrar
from app.main import app
from app.seguridad import sesion
from app.seguridad.admin import desactivar_cuenta, revocar_sesiones


CREDENCIAL = {"Authorization": "Bearer token-de-prueba"}
GRECIA = "+520000000002"
DAVID = "+520000000001"


def _clientes_independientes(monkeypatch, tmp_path):
    monkeypatch.setenv("WORKS_DB", str(tmp_path / "works.db"))
    monkeypatch.setenv("WORKS_TOKEN_VANIA", "token-de-prueba")
    monkeypatch.setenv("WORKS_WHATSAPP_DAVID", DAVID)
    monkeypatch.setenv("WORKS_WHATSAPP_GRECIA", GRECIA)
    migrar()
    cliente_usuario = TestClient(app, base_url="https://testserver")
    cliente_vania = TestClient(app, base_url="https://testserver")

    # El fixture histórico crea sesiones al construir TestClient. Esta prueba
    # controla explícitamente qué sesiones persisten y qué cookies tiene cada cliente.
    conexion = conectar()
    try:
        conexion.execute("DELETE FROM sesiones")
        conexion.commit()
    finally:
        conexion.close()
    cliente_usuario.cookies.clear()
    cliente_vania.cookies.clear()
    assert cliente_usuario is not cliente_vania
    return cliente_usuario, cliente_vania


def _sesion_de(cliente, numero):
    enlace = cliente.post("/api/acceso/enlace", params={"numero_whatsapp": numero}, headers=CREDENCIAL)
    assert enlace.status_code == 200
    token = enlace.json()["enlace"].split("token=", 1)[1]
    assert cliente.get("/api/acceso/entrar", params={"token": token}).status_code == 200


def _vencer_sesiones(persona):
    conexion = conectar()
    try:
        conexion.execute(
            "UPDATE sesiones SET vence_en = ? WHERE persona = ?",
            ((sesion.ahora() - timedelta(seconds=1)).isoformat(), persona),
        )
        conexion.commit()
    finally:
        conexion.close()


def _escribir(cliente, numero, credencial=CREDENCIAL):
    return cliente.post(
        "/api/oficinas",
        json={"numero": "204"},
        headers={**credencial, "X-Works-Solicitante": numero},
    )


def test_vania_sin_sesion_de_grecia_recibe_sin_sesion(monkeypatch, tmp_path):
    _, cliente_vania = _clientes_independientes(monkeypatch, tmp_path)

    respuesta = _escribir(cliente_vania, GRECIA)

    assert respuesta.status_code == 401
    assert respuesta.json()["codigo"] == "sin_sesion"


@pytest.mark.parametrize(
    ("numero_con_sesion", "numero_solicitante"),
    [(DAVID, GRECIA), (GRECIA, DAVID)],
)
def test_sesion_de_otra_persona_no_autoriza(
    monkeypatch, tmp_path, numero_con_sesion, numero_solicitante
):
    cliente_usuario, cliente_vania = _clientes_independientes(monkeypatch, tmp_path)
    _sesion_de(cliente_usuario, numero_con_sesion)

    respuesta = _escribir(cliente_vania, numero_solicitante)

    assert respuesta.status_code == 401
    assert respuesta.json()["codigo"] == "sin_sesion"


def test_vania_independiente_sin_cookie_crea_pendiente_server_side(monkeypatch, tmp_path):
    cliente_usuario, cliente_vania = _clientes_independientes(monkeypatch, tmp_path)
    _sesion_de(cliente_usuario, GRECIA)
    assert sesion.NOMBRE_COOKIE in cliente_usuario.cookies
    assert sesion.NOMBRE_COOKIE not in cliente_vania.cookies

    respuesta = _escribir(cliente_vania, GRECIA)

    assert respuesta.status_code == 201
    assert sesion.NOMBRE_COOKIE not in cliente_vania.cookies
    assert cliente_vania.get("/api/oficinas", headers=CREDENCIAL).json() == []
    pendiente = cliente_vania.get("/api/cambios", headers=CREDENCIAL).json()[0]
    assert pendiente["solicitante"] == "grecia"
    assert pendiente["ejecutor"] == "vania"


def test_numero_desconocido_o_del_desarrollador_recibe_403(monkeypatch, tmp_path):
    _, cliente_vania = _clientes_independientes(monkeypatch, tmp_path)
    for numero in ("+520000000003", "+520000000004"):
        assert _escribir(cliente_vania, numero).status_code == 403


def test_bearer_invalido_no_autoriza_aunque_haya_sesion(monkeypatch, tmp_path):
    cliente_usuario, cliente_vania = _clientes_independientes(monkeypatch, tmp_path)
    _sesion_de(cliente_usuario, DAVID)

    respuesta = _escribir(
        cliente_vania, DAVID, {"Authorization": "Bearer token-incorrecto"}
    )

    assert respuesta.status_code == 401
    assert respuesta.json()["codigo"] == "sin_sesion"


def test_sesion_revocada_no_autoriza(monkeypatch, tmp_path):
    cliente_usuario, cliente_vania = _clientes_independientes(monkeypatch, tmp_path)
    _sesion_de(cliente_usuario, DAVID)
    revocar_sesiones("david")

    respuesta = _escribir(cliente_vania, DAVID)

    assert respuesta.status_code == 401
    assert respuesta.json()["codigo"] == "sin_sesion"


def test_sesion_vencida_no_autoriza(monkeypatch, tmp_path):
    cliente_usuario, cliente_vania = _clientes_independientes(monkeypatch, tmp_path)
    _sesion_de(cliente_usuario, DAVID)
    _vencer_sesiones("david")

    respuesta = _escribir(cliente_vania, DAVID)

    assert respuesta.status_code == 401
    assert respuesta.json()["codigo"] == "sin_sesion"


def test_cuenta_inactiva_no_autoriza_sesion_persistida(monkeypatch, tmp_path):
    cliente_usuario, cliente_vania = _clientes_independientes(monkeypatch, tmp_path)
    _sesion_de(cliente_usuario, DAVID)
    desactivar_cuenta("david")

    respuesta = _escribir(cliente_vania, DAVID)

    assert respuesta.status_code == 401
    assert respuesta.json()["codigo"] == "sin_sesion"


def test_confirmar_y_descartar_por_vania_exigen_sesion_y_mismo_solicitante(
    monkeypatch, tmp_path
):
    cliente_usuario, cliente_vania = _clientes_independientes(monkeypatch, tmp_path)
    _sesion_de(cliente_usuario, GRECIA)
    pendiente = _escribir(cliente_vania, GRECIA).json()

    _sesion_de(cliente_usuario, DAVID)
    confirmacion_ajena = cliente_vania.post(
        f"/api/cambios/{pendiente['id']}/confirmar",
        headers={**CREDENCIAL, "X-Works-Solicitante": DAVID},
    )
    assert confirmacion_ajena.status_code == 400
    assert "Solo la persona" in confirmacion_ajena.json()["detail"]

    confirmacion = cliente_vania.post(
        f"/api/cambios/{pendiente['id']}/confirmar",
        headers={**CREDENCIAL, "X-Works-Solicitante": GRECIA},
    )
    assert confirmacion.status_code == 200
    assert cliente_vania.get("/api/oficinas", headers=CREDENCIAL).json()[0]["numero"] == "204"

    otro_pendiente = cliente_vania.put(
        "/api/oficinas/1",
        json={"estatus": "ocupada"},
        headers={**CREDENCIAL, "X-Works-Solicitante": GRECIA},
    )
    assert otro_pendiente.status_code == 200
    revocar_sesiones("grecia")
    descarte = cliente_vania.post(
        f"/api/cambios/{otro_pendiente.json()['id']}/descartar",
        headers={**CREDENCIAL, "X-Works-Solicitante": GRECIA},
    )
    assert descarte.status_code == 401
    assert descarte.json()["codigo"] == "sin_sesion"
