import sys
from pathlib import Path

from fastapi.testclient import TestClient

BASE_DIR = Path(__file__).resolve().parent.parent
API_DIR = BASE_DIR / "app" / "api"
MAIN_PY = BASE_DIR / "app" / "main.py"


def _app_fresco():
    for modulo in list(sys.modules):
        if modulo == "app" or modulo.startswith("app."):
            del sys.modules[modulo]
    from app.main import app

    return app


def test_salud_responde_ok():
    cliente = TestClient(_app_fresco())
    respuesta = cliente.get("/api/salud")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"ok": True}


def test_router_nuevo_se_registra_solo_sin_tocar_main():
    contenido_main_antes = MAIN_PY.read_text()
    archivo_temporal = API_DIR / "temporal_prueba.py"
    archivo_temporal.write_text(
        "from fastapi import APIRouter\n"
        "\n"
        "router = APIRouter()\n"
        "\n"
        "\n"
        "@router.get('/api/temporal-prueba')\n"
        "def temporal() -> dict:\n"
        "    return {'ok': True}\n"
    )
    try:
        cliente = TestClient(_app_fresco())
        respuesta = cliente.get("/api/temporal-prueba")
        assert respuesta.status_code == 200
        assert respuesta.json() == {"ok": True}
    finally:
        archivo_temporal.unlink()

    assert MAIN_PY.read_text() == contenido_main_antes
