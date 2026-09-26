"""Fixtures de Playwright para las pruebas de UI. UI-01, UI-07.

Levanta el servicio en un puerto libre elegido al momento (no fijo),
porque más de un agente puede correr pruebas de UI al mismo tiempo.
Cada sesión de pruebas usa su propia base SQLite temporal, migrada y
cargada con el escenario sintético "con_atencion" (DAT-06), para que
la aplicación real (no solo las muestras) tenga algo que mostrar
cuando UI-07 la conecta a GET /api/estado.
"""

import os
import socket
import sys
import threading
import time
import urllib.request
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
def servicio_url(tmp_path_factory):
    valor_anterior = os.environ.get("WORKS_DB")
    ruta_db = tmp_path_factory.mktemp("ui-db") / "works.db"
    os.environ["WORKS_DB"] = str(ruta_db)

    from app.db.conexion import conectar
    from app.db.migrar import migrar
    from app.fuentes.cargar import cargar

    migrar()
    conexion = conectar()
    try:
        cargar("sintetica", "con_atencion", conexion)
    finally:
        conexion.close()

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

    if valor_anterior is None:
        os.environ.pop("WORKS_DB", None)
    else:
        os.environ["WORKS_DB"] = valor_anterior


@pytest.fixture(scope="session")
def sesion_de_prueba(servicio_url):
    from app.seguridad.sesion import consumir_enlace, crear_enlace

    enlace = crear_enlace("grecia")
    return consumir_enlace(enlace["token"])["token"]


@pytest.fixture(autouse=True)
def pagina_con_sesion(request, servicio_url, sesion_de_prueba, monkeypatch):
    if "page" not in request.fixturenames:
        yield
        return

    from app.seguridad.sesion import NOMBRE_COOKIE

    pagina = request.getfixturevalue("page")
    pagina.context.add_cookies(
        [{"name": NOMBRE_COOKIE, "value": sesion_de_prueba, "url": servicio_url}]
    )
    abrir_url = urllib.request.urlopen

    def abrir_con_sesion(url, *args, **kwargs):
        if isinstance(url, str) and url.startswith(servicio_url):
            solicitud = urllib.request.Request(url, headers={"Cookie": f"{NOMBRE_COOKIE}={sesion_de_prueba}"})
            return abrir_url(solicitud, *args, **kwargs)
        return abrir_url(url, *args, **kwargs)

    monkeypatch.setattr(urllib.request, "urlopen", abrir_con_sesion)
    yield


@pytest.fixture(params=["movil", "escritorio"])
def viewport(request):
    return VIEWPORT_MOVIL if request.param == "movil" else VIEWPORT_ESCRITORIO


@pytest.fixture
def pagina_con_viewport(page, viewport):
    page.set_viewport_size(viewport)
    return page
