from fastapi.testclient import TestClient

from app.db.migrar import migrar
from app.main import app
from app.seguridad import admin, sesion


def _preparar(monkeypatch, tmp_path):
    monkeypatch.setenv("WORKS_DB", str(tmp_path / "works.db"))
    monkeypatch.setenv("WORKS_CUENTAS_CONFIG", str(tmp_path / "cuentas.json"))
    migrar()
    return TestClient(app, base_url="https://testserver")


def test_crear_registra_telefono_fuera_de_git_y_listar(monkeypatch, tmp_path):
    _preparar(monkeypatch, tmp_path)
    admin.crear_cuenta("david", "+520000000001")
    assert sesion.persona_por_whatsapp("+520000000001") == "david"
    assert admin.listar_cuentas() == [
        {"persona": "david", "activa": True, "numero_whatsapp": "+520000000001"},
        {"persona": "grecia", "activa": True, "numero_whatsapp": None},
    ]


def test_revocar_sesiones_impide_volver_a_entrar(monkeypatch, tmp_path):
    cliente = _preparar(monkeypatch, tmp_path)
    admin.crear_cuenta("grecia", "+520000000002")
    enlace = sesion.crear_enlace("grecia")["token"]
    entrada = cliente.get("/api/acceso/entrar", params={"token": enlace})
    assert entrada.status_code == 200
    assert cliente.get("/api/estado").status_code == 200
    admin.revocar_sesiones("grecia")
    assert cliente.get("/api/estado").status_code == 401


def test_desactivar_cuenta_impide_entrar(monkeypatch, tmp_path):
    _preparar(monkeypatch, tmp_path)
    admin.desactivar_cuenta("david")
    try:
        sesion.crear_enlace("david")
    except Exception as error:
        assert error.status_code == 403
    else:
        raise AssertionError("Una cuenta desactivada no debe recibir enlace")
