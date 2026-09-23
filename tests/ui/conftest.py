"""Fixtures de Playwright para las pruebas de UI. UI-01.

Levanta el servicio en un puerto libre elegido al momento (no fijo),
porque más de un agente puede correr pruebas de UI al mismo tiempo.
"""

import socket
import sys
import threading
import time
from pathlib import Path

import pytest
import uvicorn

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

VIEWPORT_MOVIL = {"width": 390, "height": 844}
VIEWPORT_ESCRITORIO = {"width": 1280, "height": 800}


def _puerto_libre():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def servicio_url():
    from app.main import app

    puerto = _puerto_libre()
    config = uvicorn.Config(app, host="127.0.0.1", port=puerto, log_level="warning")
    servidor = uvicorn.Server(config)

    hilo = threading.Thread(target=servidor.run, daemon=True)
    hilo.start()

    for _ in range(100):
        if servidor.started:
            break
        time.sleep(0.05)

    yield f"http://127.0.0.1:{puerto}"

    servidor.should_exit = True
    hilo.join(timeout=5)


@pytest.fixture(params=["movil", "escritorio"])
def viewport(request):
    return VIEWPORT_MOVIL if request.param == "movil" else VIEWPORT_ESCRITORIO


@pytest.fixture
def pagina_con_viewport(page, viewport):
    page.set_viewport_size(viewport)
    return page
